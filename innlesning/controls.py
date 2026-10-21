"""Append-only faglige avgjørelser, med eksakt eksportbinding og eksplisitt aktivering."""

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from .maintenance_store import (
    Diagnostic,
    ImportResult,
    export_basis,
    imported,
    now,
    reading,
    reject_large_file,
    save_import,
    writing,
)
from .observations import AmountObservation, Extraction, encode, identity, read_extraction
from .organization_register import REGISTER_SNAPSHOT
from .registers import RegisterSnapshot, read_register
from .sync import read_revision
from .workfiles import MAX_BYTES, FileLimitError, read_file, write_file

EDITABLE = (
    "status",
    "godkjente_felter",
    "godkjent_bruk",
    "korrigert_belop_kr",
    "begrunnelse",
    "kontrollor",
    "bevis_id",
)
LOCKED = (
    "eksport_id",
    "observation_id",
    "extraction_id",
    "dataset",
    "source_system",
    "source_unit_id",
    "revision_id",
    "artifact_sha256",
    "locator",
    "amount_field",
    "interpretation_id",
    "adapter_version",
    "format_version",
    "register_snapshot",
    "control_basis",
    "activation_generation",
    "source_generation",
    "source_observation_id",
    "source_artifact_sha256",
    "raw_value",
    "amount_text",
    "raw_amount_kr",
    "structure_status",
    "professional_status",
    "anomalies",
    "extraction_anomalies",
    "organization",
    "catalogue_status",
    "budget_year",
    "chapter",
    "post",
    "meaning",
    "forgjenger",
    "siste_status",
    "ferskhet",
    "kildekontekst",
)
HEADERS = (*LOCKED, *EDITABLE)
type Context = tuple[Extraction, dict[str, Any], dict[str, Any] | None]
type ContextCache = dict[str, Context]


def define_control_basis(database: Path, description: str) -> str:
    if not description.strip():
        raise ValueError("Kontrollgrunnlag krever beskrivelse")
    identifier = identity("faglig-kontroll-v1", description)
    with writing(database) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO control_bases VALUES (?,?)", (identifier, description)
        )
    return identifier


def _scope(extraction: Extraction) -> str:
    return identity(extraction.dataset, extraction.source_system, extraction.source_unit_id)


def _active(connection: sqlite3.Connection, extraction: Extraction) -> dict[str, Any] | None:
    row = connection.execute(
        "SELECT generation,content FROM control_activations WHERE scope=? "
        "ORDER BY generation DESC LIMIT 1",
        (_scope(extraction),),
    ).fetchone()
    return {**json.loads(row[1]), "generation": row[0]} if row else None


def _basis(extraction: Extraction, register_snapshot: str, control_basis: str) -> dict[str, str]:
    return {
        "extraction_id": extraction.id,
        "register_snapshot": register_snapshot,
        "control_basis": control_basis,
    }


def read_activation(database: Path, extraction_id: str) -> dict[str, Any] | None:
    """Les eksplisitt aktivering uten å aktivere, endre eller velge en tolkning."""
    extraction = read_extraction(database, extraction_id)
    with reading(database) as connection:
        if not connection.execute(
            "SELECT 1 FROM sqlite_master WHERE name='control_activations'"
        ).fetchone():
            return None
        return _active(connection, extraction)


def activate_basis(
    database: Path, extraction_ids: tuple[str, ...], register_snapshot: str, control_basis: str
) -> tuple[int, ...]:
    """En uttrykkelig skriveoperasjon; historisk lesing/eksport aktiverer aldri noe."""
    extractions = tuple(read_extraction(database, i) for i in extraction_ids)
    if not extractions or len({_scope(e) for e in extractions}) != len(extractions):
        raise ValueError("Velg én tolkning per kildeenhet")
    if register_snapshot != REGISTER_SNAPSHOT:
        read_register(database, register_snapshot)
    for e in extractions:
        if e.interpretation.register_snapshot != register_snapshot:
            raise ValueError("Uttrekket må være tolket med det eksplisitte registersnapshotet")
    generations: list[int] = []
    with writing(database) as connection:
        if not connection.execute(
            "SELECT 1 FROM control_bases WHERE id=?", (control_basis,)
        ).fetchone():
            raise ValueError("Ukjent kontrollgrunnlag")
        for e in extractions:
            active = _active(connection, e)
            basis = _basis(e, register_snapshot, control_basis)
            if active and all(active[k] == v for k, v in basis.items()):
                generations.append(active["generation"])
                continue
            generation = active["generation"] + 1 if active else 1
            connection.execute(
                "INSERT INTO control_activations VALUES (?,?,?,?)",
                (_scope(e), generation, encode(basis), now()),
            )
            generations.append(generation)
    return tuple(generations)


def _source(
    connection: sqlite3.Connection, database: Path, extraction: Extraction
) -> dict[str, Any]:
    if extraction.source_system != "storting":
        return {
            "generation": None,
            "revision": extraction.source_revision_id,
            "observation_id": None,
            "sha256": extraction.artifact.sha256,
            "attempt": None,
            "observation_status": None,
        }
    revision = read_revision(database, extraction.source_revision_id)
    decision = revision.report.decision
    assert decision is not None
    row = connection.execute(
        "SELECT generation FROM decision_heads WHERE dataset=? AND session=? AND decision_id=?",
        (revision.dataset, decision.session, decision.id),
    ).fetchone()
    return {
        "generation": row[0],
        "revision": revision.current_revision_id,
        "observation_id": revision.current_observation_id,
        "sha256": revision.current_source_sha256,
        "attempt": revision.latest_attempt_status,
        "observation_status": revision.observation_status,
    }


def _latest(connection: sqlite3.Connection, observation_id: str) -> "ProfessionalDecision | None":
    row = connection.execute(
        "SELECT content FROM professional_decisions WHERE observation_id=? "
        "ORDER BY rowid DESC LIMIT 1",
        (observation_id,),
    ).fetchone()
    return ProfessionalDecision(**json.loads(row[0])) if row else None


@dataclass(frozen=True)
class Evidence:
    id: str
    sha256: str
    version: str
    locator: str
    role: str
    url: str
    parent_sha256: str | None = None
    source_kind: str = "local_original"


def store_evidence(
    database: Path,
    path: Path,
    *,
    version: str,
    locator: str,
    role: str,
    url: str,
    parent_sha256: str | None = None,
) -> Evidence:
    if not all(v.strip() for v in (version, locator, role, url)) or role != "kontrollkilde":
        raise ValueError("Bevis krever versjon, lokator, URL og rolle kontrollkilde")
    if parent_sha256 is not None and (
        len(parent_sha256) != 64 or any(c not in "0123456789abcdef" for c in parent_sha256)
    ):
        raise ValueError("Foreldrehash må være SHA-256")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Bevis overstiger 8 MiB")
    with path.open("rb") as source:
        raw = source.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("Bevis overstiger 8 MiB")
    sha = hashlib.sha256(raw).hexdigest()
    identifier = identity("kontrollbevis-v1", sha, version, locator, role, url, parent_sha256)
    result = Evidence(
        identifier,
        sha,
        version,
        locator,
        role,
        url,
        parent_sha256,
        "derived_excerpt" if parent_sha256 else "local_original",
    )
    with writing(database) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO control_evidence VALUES (?,?,?,?)",
            (identifier, encode(asdict(result)), raw, str(path.resolve())),
        )
    return result


def read_evidence(database: Path, identifier: str) -> Evidence:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT content FROM control_evidence WHERE id=?", (identifier,)
        ).fetchone()
    if not row:
        raise ValueError("Ukjent kontrollbevis")
    return Evidence(**json.loads(row[0]))


def read_evidence_source(database: Path, identifier: str) -> bytes:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT raw FROM control_evidence WHERE id=?", (identifier,)
        ).fetchone()
    if not row:
        raise ValueError("Ukjent kontrollbevis")
    return bytes(row[0])


@dataclass(frozen=True)
class ProfessionalDecision:
    id: str
    observation_id: str
    predecessor: str | None
    created_utc: str
    target_json: str
    status: str
    approved_fields: str
    approved_use: str
    reason: str
    reviewer: str
    evidence_id: str
    corrected_amount_kr: int | None


@dataclass(frozen=True)
class DecisionView:
    decision: ProfessionalDecision
    freshness: str
    source_context_json: str
    superseded_by: str | None = None


def _freshness(
    connection: sqlite3.Connection,
    database: Path,
    target: dict[str, str],
    contexts: ContextCache | None = None,
) -> tuple[str, dict[str, Any]]:
    contexts = contexts if contexts is not None else {}
    identifier = target["extraction_id"]
    if identifier not in contexts:
        extraction = read_extraction(database, identifier)
        contexts[identifier] = (
            extraction,
            _source(connection, database, extraction),
            _active(connection, extraction),
        )
    extraction, source, active = contexts[identifier]
    if (
        not active
        or active["generation"] != int(target["activation_generation"])
        or any(
            active[k] != target[k] for k in ("extraction_id", "register_snapshot", "control_basis")
        )
        or str(source["generation"] or "") != target["source_generation"]
        or source["revision"] != extraction.source_revision_id
    ):
        return "utdatert", source
    if source["attempt"] not in (None, "fullfort") or source["observation_status"] not in (
        None,
        "observert",
    ):
        return "ikke_vurderbar", source
    return "gjeldende", source


def read_decision(database: Path, identifier: str) -> DecisionView:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT content FROM professional_decisions WHERE id=?", (identifier,)
        ).fetchone()
        if row is None:
            raise ValueError("Ukjent faglig avgjørelse")
        decision = ProfessionalDecision(**json.loads(row[0]))
        freshness, source = _freshness(connection, database, json.loads(decision.target_json))
        latest = _latest(connection, decision.observation_id)
        newer = latest.id if latest and latest.id != identifier else None
        return DecisionView(decision, "utdatert" if newer else freshness, encode(source), newer)


def latest_decision(database: Path, observation_id: str) -> DecisionView | None:
    with reading(database) as connection:
        latest = _latest(connection, observation_id)
    return read_decision(database, latest.id) if latest else None


def read_decisions(database: Path, identifiers: tuple[str, ...]) -> tuple[DecisionView, ...]:
    """Les eksakte valgte avgjørelser med delt kilde-/aktiveringskontekst.

    Batchlesing velger ingen ny avgjørelse og endrer ingen godkjenning. Nyere
    avgjørelser sperrer fortsatt den valgte, også når kildeinnholdet vender tilbake.
    """
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Velg ulike avgjørelses-ID-er")
    if not identifiers:
        return ()
    result: list[DecisionView] = []
    with reading(database) as connection:
        contexts: ContextCache = {}
        for identifier in identifiers:
            row = connection.execute(
                "SELECT content FROM professional_decisions WHERE id=?", (identifier,)
            ).fetchone()
            if row is None:
                raise ValueError("Ukjent faglig avgjørelse")
            decision = ProfessionalDecision(**json.loads(row[0]))
            freshness, source = _freshness(
                connection, database, json.loads(decision.target_json), contexts
            )
            latest = _latest(connection, decision.observation_id)
            newer = latest.id if latest and latest.id != identifier else None
            result.append(
                DecisionView(decision, "utdatert" if newer else freshness, encode(source), newer)
            )
    return tuple(result)


def _latest_view(
    connection: sqlite3.Connection, database: Path, observation_id: str, contexts: ContextCache
) -> DecisionView | None:
    decision = _latest(connection, observation_id)
    if decision is None:
        return None
    freshness, source = _freshness(connection, database, json.loads(decision.target_json), contexts)
    return DecisionView(decision, freshness, encode(source))


def _target(
    connection: sqlite3.Connection,
    database: Path,
    extraction: Extraction,
    observation: AmountObservation,
    register_snapshot: str,
    control_basis: str,
    export_id: str,
    contexts: ContextCache | None = None,
    register: RegisterSnapshot | None = None,
) -> dict[str, str]:
    contexts = contexts if contexts is not None else {}
    if extraction.id not in contexts:
        contexts[extraction.id] = (
            extraction,
            _source(connection, database, extraction),
            _active(connection, extraction),
        )
    _, source, active = contexts[extraction.id]
    basis = _basis(extraction, register_snapshot, control_basis)
    if not active or any(active[k] != v for k, v in basis.items()):
        raise ValueError("Aktiver valgt tolkning/register/kontrollgrunnlag uttrykkelig først")
    previous = _latest(connection, observation.id)
    result = {
        "eksport_id": export_id,
        "observation_id": observation.id,
        "extraction_id": extraction.id,
        "dataset": extraction.dataset,
        "source_system": extraction.source_system,
        "source_unit_id": extraction.source_unit_id,
        "revision_id": extraction.source_revision_id,
        "artifact_sha256": extraction.artifact.sha256,
        "locator": observation.pointer.locator,
        "amount_field": observation.pointer.amount_field,
        "interpretation_id": extraction.interpretation.id,
        "adapter_version": extraction.interpretation.adapter_version,
        "format_version": observation.format_version,
        "register_snapshot": register_snapshot,
        "control_basis": control_basis,
        "activation_generation": str(active["generation"]),
        "source_generation": str(source["generation"] or ""),
        "source_observation_id": str(source["observation_id"] or ""),
        "source_artifact_sha256": str(source["sha256"] or ""),
        "raw_value": observation.raw_value,
        "amount_text": observation.amount_text,
        "raw_amount_kr": str(observation.amount_kr) if observation.amount_kr is not None else "",
        "structure_status": observation.structure_status,
        "professional_status": observation.professional_status,
        "anomalies": encode([asdict(a) for a in observation.anomalies]),
        "extraction_anomalies": encode(
            [
                asdict(a)
                for a in extraction.anomalies
                if a.chapter in (None, observation.chapter)
                and a.post in (None, observation.post)
                and a.budget_year in (None, observation.budget_year)
            ]
        ),
        "organization": encode(asdict(observation.organization)),
        "catalogue_status": "bekreftet i valgt snapshot"
        if register is not None
        and register.catalogued(observation.chapter, observation.post, observation.budget_year)
        else "uavklart i valgt snapshot",
        "budget_year": str(observation.budget_year or ""),
        "chapter": observation.chapter or "",
        "post": observation.post or "",
        "meaning": observation.meaning,
        "forgjenger": previous.id if previous else "",
        "siste_status": previous.status if previous else "ikke vurdert",
        "ferskhet": "",
        "kildekontekst": encode(source),
    }
    result["ferskhet"] = _freshness(connection, database, result, contexts)[0]
    return result


def export_controls(
    database: Path,
    extraction_ids: tuple[str, ...],
    output: Path,
    *,
    register_snapshot: str,
    control_basis: str,
    observation_ids: tuple[str, ...] | None = None,
) -> str:
    extractions = tuple(read_extraction(database, i) for i in extraction_ids)
    if not extractions or len(set(extraction_ids)) != len(extraction_ids):
        raise ValueError("Velg ulike eksplisitte uttrekks-ID-er")
    identifier = str(uuid4())
    register = (
        read_register(database, register_snapshot)
        if register_snapshot != REGISTER_SNAPSHOT
        else None
    )
    rows: list[dict[str, str]] = []
    with writing(database) as connection:
        contexts: ContextCache = {}
        for extraction in extractions:
            for observation in extraction.observations:
                if observation_ids is None or observation.id in observation_ids:
                    rows.append(
                        _target(
                            connection,
                            database,
                            extraction,
                            observation,
                            register_snapshot,
                            control_basis,
                            identifier,
                            contexts,
                            register,
                        )
                    )
        if not rows or (
            observation_ids is not None
            and set(observation_ids) != {r["observation_id"] for r in rows}
        ):
            raise ValueError("Velg eksisterende beløpsobservasjoner innen uttrekkene")
        connection.execute(
            "INSERT INTO maintenance_exports VALUES (?,?,?)",
            (identifier, "kontroll", encode({"rows": rows})),
        )
    write_file(database, output, "Kontroll", HEADERS, rows, frozenset(EDITABLE))
    return identifier


def import_controls(database: Path, path: Path) -> ImportResult:
    try:
        raw, rows, errors = read_file(path, HEADERS, "Kontroll")
    except FileLimitError:
        return reject_large_file(database, path, "kontroll", "Kontroll")
    sha = hashlib.sha256(raw).hexdigest()
    identifier = identity("kontrollimport-v1", sha)
    with writing(database) as connection:
        previous = imported(connection, identifier)
        if previous:
            return previous  # Ingen reaktivering, heller ikke etter A → B → A.
        decisions: list[ProfessionalDecision] = []
        expected: dict[str, dict[str, str]] = {}
        contexts: ContextCache = {}
        if not errors:
            try:
                if not rows:
                    raise ValueError("Tom kontrollfil")
                exported = export_basis(connection, rows[0]["eksport_id"], "kontroll")
                expected = {r["observation_id"]: r for r in exported["rows"]}
                if len(rows) != len(expected) or {r["observation_id"] for r in rows} != set(
                    expected
                ):
                    raise ValueError(
                        "Filen må inneholde hver eksportert observasjon nøyaktig én gang"
                    )
            except ValueError as error:
                errors.append(Diagnostic("Kontroll", 0, "eksport_id/observation_id", str(error)))
        if not errors:
            for n, row in enumerate(rows, 2):
                n = int(row.get("__row__", n))

                def fail(field: str, message: str, row_number: int = n) -> None:
                    errors.append(Diagnostic("Kontroll", row_number, field, message))

                target = expected[row["observation_id"]]
                for field in LOCKED:
                    if row[field] != target[field]:
                        fail(field, "Låst kilde-/eksportgrunnlag er endret")
                freshness, _ = _freshness(connection, database, target, contexts)
                if freshness != "gjeldende":
                    fail("ferskhet", f"Grunnlaget er {freshness}; krever ny eksport og avgjørelse")
                current = _latest(connection, target["observation_id"])
                if (current.id if current else "") != target["forgjenger"]:
                    fail("forgjenger", "Nyere avgjørelse finnes; eksporter på nytt")
                status = row["status"]
                if not status:
                    if any(row[k] for k in EDITABLE if k != "status"):
                        fail("status", "Utfylte kontrollfelt krever eksplisitt status")
                    continue
                if status not in {"til_kontroll", "godkjent", "avvist"}:
                    fail("status", "Velg til_kontroll, godkjent eller avvist")
                for field in ("begrunnelse", "kontrollor"):
                    if not row[field].strip():
                        fail(field, "Må være oppgitt")
                for field in EDITABLE:
                    if row[field].lstrip().startswith(("=", "+", "@")):
                        fail(field, "Formeluttrykk er ikke tillatt i kontrollfelt")
                corrected = None
                if row["korrigert_belop_kr"]:
                    try:
                        corrected = int(row["korrigert_belop_kr"])
                        if (
                            str(corrected) != row["korrigert_belop_kr"]
                            or abs(corrected) > 9_007_199_254_740_991
                        ):
                            raise ValueError
                    except ValueError:
                        fail("korrigert_belop_kr", "Krever Excel-eksakte hele kroner")
                fields = (
                    set(row["godkjente_felter"].split(",")) if row["godkjente_felter"] else set()
                )
                if status == "godkjent":
                    if not fields or fields - {"amount_kr", "organization", "catalogue"}:
                        fail("godkjente_felter", "Velg amount_kr, organization og/eller catalogue")
                    if row["godkjent_bruk"] not in {"analysebelop", "kjedegrunnlag", "metadata"}:
                        fail("godkjent_bruk", "Velg analysebelop, kjedegrunnlag eller metadata")
                    if not row["bevis_id"]:
                        fail("bevis_id", "Godkjenning krever eksplisitt eksternt kildebevis")
                    if corrected is not None and "amount_kr" not in fields:
                        fail("godkjente_felter", "Korreksjon krever godkjent amount_kr")
                    if "amount_kr" in fields and not target["raw_amount_kr"] and corrected is None:
                        fail(
                            "korrigert_belop_kr",
                            "Ukjent råbeløp krever uttrykkelig kildebegrunnet korreksjon",
                        )
                    if fields & {"organization", "catalogue"}:
                        register = (
                            read_register(database, target["register_snapshot"])
                            if target["register_snapshot"] != REGISTER_SNAPSHOT
                            else None
                        )
                        year = int(target["budget_year"]) if target["budget_year"] else None
                        from .organization_register import lookup

                        organization = (
                            register.lookup(target["chapter"], year)
                            if register
                            else lookup(target["chapter"], year)
                        )
                        if "organization" in fields and not organization.fdep_nr:
                            fail(
                                "godkjente_felter",
                                "Organisasjonsgodkjenning krever gyldig kapittelkobling",
                            )
                        if "catalogue" in fields and (
                            register is None
                            or not register.catalogued(target["chapter"], target["post"], year)
                        ):
                            fail(
                                "godkjente_felter",
                                "Kataloggodkjenning krever eksplisitt kapittel/post for året",
                            )
                elif corrected is not None or fields or row["godkjent_bruk"]:
                    fail(
                        "status",
                        "Bare godkjent avgjørelse kan godkjenne bruk eller korrigere beløp",
                    )
                if (
                    row["bevis_id"]
                    and not connection.execute(
                        "SELECT 1 FROM control_evidence WHERE id=?", (row["bevis_id"],)
                    ).fetchone()
                ):
                    fail("bevis_id", "Ukjent bevis; lagre den faktiske bevisfilen først")
                decisions.append(
                    ProfessionalDecision(
                        str(uuid4()),
                        target["observation_id"],
                        target["forgjenger"] or None,
                        now(),
                        encode(target),
                        status,
                        row["godkjente_felter"],
                        row["godkjent_bruk"],
                        row["begrunnelse"],
                        row["kontrollor"],
                        row["bevis_id"],
                        corrected,
                    )
                )
        if not errors:
            for decision in decisions:
                connection.execute(
                    "INSERT INTO professional_decisions VALUES (?,?,?,?,?)",
                    (
                        decision.id,
                        decision.observation_id,
                        decision.predecessor,
                        encode(asdict(decision)),
                        decision.created_utc,
                    ),
                )
        result = ImportResult(
            identifier,
            "kontroll",
            tuple(d.id for d in decisions) if not errors else (),
            errors=tuple(errors),
        )
        save_import(connection, result, path, raw, sha)
        return result


def control_report(database: Path, extraction_ids: tuple[str, ...]) -> tuple[dict[str, Any], ...]:
    """Les råobservasjoner, siste avgjørelse og siste kildeforsøk uten å aktivere grunnlag."""
    result: list[dict[str, Any]] = []
    with reading(database) as connection:
        has_decisions = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE name='professional_decisions'"
        ).fetchone()
        for identifier in extraction_ids:
            extraction = read_extraction(database, identifier)
            source = _source(connection, database, extraction)
            for observation in extraction.observations:
                view = latest_decision(database, observation.id) if has_decisions else None
                result.append(
                    {
                        "observation": asdict(observation),
                        "decision": asdict(view) if view else None,
                        "source_context": source,
                    }
                )
    return tuple(result)
