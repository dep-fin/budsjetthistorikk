"""2024-pilot: egne immutable importgrunnlag og separate forsøk, uten B5-aktivering."""

import hashlib
import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4
from zipfile import BadZipFile

from .historical_xlsx import (
    DEFAULT_LIMITS,
    Limits,
    MaterializationBudget,
    decimal_value,
    inventory_workbook,
    multiply,
)
from .observations import (
    AmountObservation,
    Anomaly,
    Artifact,
    DocumentReference,
    Extraction,
    Interpretation,
    Organization,
    SourcePointer,
    encode,
    identity,
    initialize_observations,
    read_extraction,
    save_extraction_in,
)
from .storage import check_schema, read_source

ADAPTER = "historisk-excel-2024-v3"
CONTROL_PROFILES = {
    "G": ("regjeringsforslag", "opprinnelig", "nivaa", "budsjettåret"),
    "H": ("stortingsvedtak", "opprinnelig", "nivaa", "budsjettåret"),
    "I": ("regjeringsforslag", "rnb", "endring", "rnb"),
    "J": ("stortingsvedtak", "rnb", "etter_belop", "etter_rnb"),
    "K": ("stortingsvedtak", "rnb", "endring", "foerste_halvaar"),
    "L": ("stortingsvedtak", "ovrig", "endring", "etter_rnb"),
    "D": ("stortingsvedtak", "valgte_dokumentgrupper", "endring", "valgte_dokumentgrupper"),
}


def candidate_control_basis(column: str, *, component: bool = False) -> dict[str, Any]:
    """A bounded mathematical hypothesis, separate from approved observation axes."""
    if column not in CONTROL_PROFILES or (component and column != "D"):
        raise ValueError("Ingen avgrenset kontrollhypotese for kolonnen")
    figure, stage, meaning, period = CONTROL_PROFILES[column]
    return {
        "budget_year": 2024,
        "unit": "NOK",
        "candidate_multiplier": "1" if column == "D" else "1000000",
        "figure_type": figure,
        "stage": stage,
        "meaning": meaning,
        "period": period,
        "detail_level": "underpost" if component else "post",
        "budget_side": "begge",
        "reference_basis": "avledet_komponentdifferanse" if component else "observert_kildefelt",
    }


STORAGE_VERSION = "historisk-pilot-1"
SCHEMA = """
CREATE TABLE IF NOT EXISTS historical_meta (version TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS historical_attempts (
  attempt_id TEXT PRIMARY KEY, status TEXT NOT NULL, source_sha256 TEXT,
  extraction_id TEXT, options_json TEXT NOT NULL, started_utc TEXT NOT NULL, error TEXT
);
CREATE TABLE IF NOT EXISTS historical_imports (
  extraction_id TEXT PRIMARY KEY REFERENCES amount_extractions(extraction_id),
  content_json TEXT NOT NULL, content_sha256 TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS historical_publications (
  extraction_id TEXT NOT NULL, path TEXT NOT NULL, manifest_sha256 TEXT NOT NULL,
  published_utc TEXT NOT NULL, PRIMARY KEY (extraction_id,path)
);
"""


@dataclass(frozen=True)
class HistoricalAttempt:
    attempt_id: str
    status: str
    source_sha256: str | None
    extraction_id: str | None
    error: str | None = None


@dataclass(frozen=True)
class HistoricalSnapshot:
    extraction: Extraction
    cells: tuple[dict[str, Any], ...]
    candidates: tuple[dict[str, Any], ...]
    column_rules: tuple[dict[str, Any], ...]
    metadata: dict[str, Any]
    predecessor_id: str | None


def initialize_historical(connection: sqlite3.Connection) -> None:
    initialize_observations(connection)
    for statement in SCHEMA.split(";"):
        if statement.strip():
            connection.execute(statement)
    versions = connection.execute("SELECT version FROM historical_meta").fetchall()
    if versions and versions != [(STORAGE_VERSION,)]:
        raise ValueError("Ukjent historisk lagringsversjon")
    connection.execute(
        "INSERT OR IGNORE INTO historical_meta(version) VALUES (?)", (STORAGE_VERSION,)
    )
    # Additive pilottabeller innen kjent schema 5; eldre skrivere bevarer versjonen.
    connection.execute("PRAGMA user_version = 5")


@contextmanager
def _connect(database: Path, *, writable: bool = False) -> Iterator[sqlite3.Connection]:
    if writable:
        database.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(database)
    else:
        connection = sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True)
    try:
        if writable:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("BEGIN IMMEDIATE")
            initialize_historical(connection)
        else:
            check_schema(connection)
            versions = connection.execute("SELECT version FROM historical_meta").fetchall()
            if versions != [(STORAGE_VERSION,)]:
                raise ValueError("Ukjent historisk lagringsversjon")
        with connection:
            yield connection
    finally:
        connection.close()


def read_historical_attempt(database: Path, attempt_id: str) -> HistoricalAttempt:
    with _connect(database) as connection:
        row = connection.execute(
            "SELECT attempt_id,status,source_sha256,extraction_id,error "
            "FROM historical_attempts WHERE attempt_id=?",
            (attempt_id,),
        ).fetchone()
    if row is None:
        raise ValueError("Ukjent historisk importforsøk")
    return HistoricalAttempt(*row)


def stage_historical_workbook(
    database: Path,
    source: Path,
    *,
    budget_year: int,
    year_evidence: str = "uttrykkelig valgt budsjettår fra filinventar",
    predecessor_id: str | None = None,
    interpretation_note: str = "pilotregler-3",
    limits: Limits = DEFAULT_LIMITS,
) -> str:
    if budget_year != 2024 or not year_evidence.strip() or not interpretation_note.strip():
        raise ValueError("Adapteren krever 2024 og uttrykkelig års-/tolkningsgrunnlag")
    if source.resolve() == database.resolve():
        raise ValueError("Original og database må ha forskjellige baner")
    if predecessor_id is not None:
        read_historical_workbook(database, predecessor_id)
    attempt_id = str(uuid4())
    options = {
        "adapter_version": ADAPTER,
        "budget_year": budget_year,
        "year_evidence": year_evidence,
        "predecessor_id": predecessor_id,
        "interpretation_note": interpretation_note,
        "limits": asdict(limits),
        "received_name": source.name,
    }
    with _connect(database, writable=True) as connection:
        connection.execute(
            "INSERT INTO historical_attempts "
            "(attempt_id,status,options_json,started_utc) VALUES (?,?,?,?)",
            (attempt_id, "startet", encode(options), datetime.now(UTC).isoformat()),
        )
    raw: bytes | None = None
    try:
        with source.open("rb") as handle:
            raw = handle.read(limits.max_bytes + 1)
        if len(raw) > limits.max_bytes:
            raw = None  # Overskridelse bevares som feil, ingen oppfunnet fullfilhash.
            raise ValueError("Arbeidsboken overskrider bytegrensen")
        sha = hashlib.sha256(raw).hexdigest()
        with _connect(database, writable=True) as connection:
            connection.execute(
                "INSERT OR IGNORE INTO sources (sha256,raw_response) VALUES (?,?)", (sha, raw)
            )
            connection.execute(
                "UPDATE historical_attempts SET source_sha256=? WHERE attempt_id=?",
                (sha, attempt_id),
            )
    except (OSError, ValueError) as error:
        with _connect(database, writable=True) as connection:
            connection.execute(
                "UPDATE historical_attempts SET status='feilet',error=? WHERE attempt_id=?",
                (str(error), attempt_id),
            )
    return attempt_id


def import_historical_workbook(
    database: Path,
    source: Path,
    *,
    budget_year: int,
    year_evidence: str = "uttrykkelig valgt budsjettår fra filinventar",
    predecessor_id: str | None = None,
    interpretation_note: str = "pilotregler-3",
    limits: Limits = DEFAULT_LIMITS,
) -> HistoricalAttempt:
    attempt_id = stage_historical_workbook(
        database,
        source,
        budget_year=budget_year,
        year_evidence=year_evidence,
        predecessor_id=predecessor_id,
        interpretation_note=interpretation_note,
        limits=limits,
    )
    return resume_historical_import(database, attempt_id)


def column_rules() -> tuple[dict[str, Any], ...]:
    stages = [
        ("G", "Gul bok (f90)", "regjeringsforslag", "opprinnelig", "nivaa"),
        ("H", "Saldert (f120)", "stortingsvedtak", "opprinnelig", "nivaa"),
        ("I", "Endring RNB-prop (f148)", "regjeringsforslag", "rnb", "endring"),
        ("J", "Budsjettets stilling ink. RNB (f150)", "uavklart", "rnb", "etter_belop"),
        ("K", "Tilleggsbevilgninger første halvår (f176)", "uavklart", "uavklart", "endring"),
        ("L", "Tilleggsbevilgninger etter RNB (f177)", "uavklart", "uavklart", "endring"),
        ("M", "Lønnsoppgjør (f179)", "uavklart", "uavklart", "uavklart"),
        ("N", "Nysald-prop", "regjeringsforslag", "nysaldering", "endring"),
    ]
    rules: list[dict[str, Any]] = [
        {
            "version": "historisk-kolonner-1",
            "sheet": "Rådata",
            "column": col,
            "label": label,
            "candidate_multiplier": "1000000",
            "candidate_currency": "NOK",
            "figure_type_candidate": figure,
            "round_candidate": round_,
            "meaning_candidate": meaning,
            "scope": "aggregat",
            "unit_status": "aapen",
            "precision_status": "aapen",
            "stage_status": "aapen",
            "meaning_status": "aapen",
            "professional_status": "til_kontroll",
            "normalization": "ingen godkjent NOK; eksakt Decimal-kandidat uten avrunding",
            "evidence": (
                "docs/research/historisk-excel/pilotkontroll.md; "
                "begrenset kontroll, ingen generell godkjenning"
            ),
        }
        for col, label, figure, round_, meaning in stages
    ]
    rules.append(
        {
            "version": "historisk-kolonner-1",
            "sheet": "Dokumentiltknyntning2024",
            "column": "D",
            "label": "belop",
            "candidate_multiplier": "1",
            "candidate_currency": "NOK",
            "figure_type_candidate": "uavklart",
            "round_candidate": "uavklart",
            "meaning_candidate": "uavklart",
            "scope": "uavklart",
            "unit_status": "aapen",
            "precision_status": "aapen",
            "stage_status": "aapen",
            "meaning_status": "aapen",
            "professional_status": "til_kontroll",
            "normalization": "ingen godkjent NOK; eksakt kandidat",
            "evidence": "pilotkontroll.md: dokumentgrupper og komponenter prøves separat",
        }
    )
    for rule in rules:
        col = rule["column"]
        rule["comparison_profiles"] = (
            [candidate_control_basis(col)]
            + ([candidate_control_basis(col, component=True)] if col == "D" else [])
            if col in CONTROL_PROFILES
            else []
        )
        rule["comparison_profile_status"] = "matematisk hypotese; ingen faglig kolonnegodkjenning"
    return tuple(rules)


def _code(value: str | None) -> str | None:
    if value is not None and len(value) <= 12 and value.isascii() and value.isdigit():
        return str(int(value))
    return None


def _build(
    raw: bytes, options: dict[str, Any], attempt_id: str, started: str
) -> HistoricalSnapshot:
    if options.get("adapter_version") != ADAPTER:
        raise ValueError("Forsøket gjelder en eldre adapter; start et nytt v3-forsøk")
    limits = Limits(**options["limits"])
    inventory = inventory_workbook(raw, limits=limits)
    names = {s["name"] for s in inventory.metadata["sheets"]}
    if not {"Rådata", "Dokumentiltknyntning2024"} <= names:
        raise ValueError("Pilotens to påkrevde ark mangler")
    rules = column_rules()
    interpretation = Interpretation(
        adapter_version=ADAPTER,
        normalization_rule=encode(rules),
        reason=encode(
            {
                k: options[k]
                for k in ("budget_year", "year_evidence", "interpretation_note", "limits")
            }
        ),
    )
    sha = hashlib.sha256(raw).hexdigest()
    rows: dict[tuple[str, int], dict[str, dict[str, Any]]] = {}
    for cell in inventory.cells:
        rows.setdefault((cell["sheet"], cell["row"]), {})[cell["column"]] = cell
    observations: list[AmountObservation] = []
    cells: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    anomalies: list[Anomaly] = []
    budget = MaterializationBudget(limits.serialized_chars)
    budget.charge(inventory.cells)
    budget.charge(inventory.metadata)
    row_contexts: dict[tuple[str, int], tuple[dict[str, Any], str]] = {}
    for key, record in rows.items():
        values = {col: value["resolved_text"] for col, value in record.items()}
        # Reserve every retained raw context before serializing the first copy.
        copies = sum(
            key[1] > 1 and any((r["sheet"], r["column"]) == (key[0], col) for r in rules)
            for col in record
        )
        for _ in range(max(copies, 1)):
            budget.charge(values)
        row_contexts[key] = (values, encode(values))
    for original in inventory.cells:
        cell = dict(original)
        cell["id"] = identity("historisk-celle-1", sha, cell["sheet"], cell["cell"])
        sheet, row, col = cell["sheet"], cell["row"], cell["column"]
        record = rows[(sheet, row)]
        row_values, raw_context = row_contexts[(sheet, row)]
        rule = next((r for r in rules if (r["sheet"], r["column"]) == (sheet, col)), None)
        cell["observation_id"] = None
        cell["disposition"] = (
            "overskrift"
            if row == 1
            else "metadata_referanse"
            if (sheet == "Rådata" and col in "ABCDEF")
            or (sheet == "Dokumentiltknyntning2024" and col in "ABCEFGHIJKLMNO")
            else "uttrykkelig_blank"
            if cell["state"] == "blank"
            else "fravaerende"
            if cell["state"] == "absent"
            else "uavklart"
        )
        if row > 1 and rule is not None:
            chapter_col, post_col, subpost_col = (
                ("B", "C", "D") if sheet == "Rådata" else ("A", "B", "C")
            )
            chapter_raw, post_raw, subpost_raw = (
                row_values.get(k) for k in (chapter_col, post_col, subpost_col)
            )
            issues = [
                Anomaly(
                    "aapen_kolonneregel",
                    "Enhet/presisjon/stadium/omfang krever faglig avklaring",
                    evidence=f"{sheet}!{cell['cell']}",
                ),
                Anomaly(
                    "historisk_organisasjon_uavklart", "Ingen tilbakeprojisering av dagens register"
                ),
                Anomaly(
                    "hierarki_uavklart",
                    "Underpostkode er bevart; ingen automatisk komponentrelasjon",
                ),
            ]
            number = (
                decimal_value(cell["raw_v"], limits)
                if cell["raw_type"] == "n" and not cell["formula_result"]
                else None
            )
            candidate = (
                multiply(number, rule["candidate_multiplier"]) if number is not None else None
            )
            if cell["formula_result"]:
                issues.append(
                    Anomaly(
                        "formelresultat",
                        "Egen formel eller dekket formelområde; cache er ikke kildebeløp",
                        evidence=encode(cell["formula_region"])
                        if cell["formula_region"] is not None
                        else f"{sheet}!{cell['cell']}",
                    )
                )
            if candidate is not None and candidate != candidate.to_integral_value():
                issues.append(
                    Anomaly(
                        "ikke_heltallige_kroner", "Eksakt kandidat har desimaler; ingen avrunding"
                    )
                )
            if candidate is not None and abs(candidate) > 9_007_199_254_740_991:
                issues.append(
                    Anomaly(
                        "utenfor_eksakt_excel_heltall",
                        "Kandidat overskrider Excel-eksakt heltallsgrense",
                    )
                )
            if number is None:
                issues.append(
                    Anomaly(
                        "uavklart_belop",
                        "Blank/fravær/formel/feil/ugyldig numerisk verdi; ingen evaluering",
                    )
                )
            if _code(chapter_raw) is None or _code(post_raw) is None:
                issues.append(
                    Anomaly("uavklart_konto", "Rå kontofelt kan ikke normaliseres sikkert")
                )
            docs = tuple(
                DocumentReference(str(row_values[key]), key, role)
                for key, role in (("E", "forslagsgrunnlag"), ("F", "innstilling"), ("G", "vedtak"))
                if sheet == "Dokumentiltknyntning2024" and row_values.get(key) not in (None, "")
            )
            organization = Organization(
                dep=row_values.get("A") if sheet == "Rådata" else None,
                fdep_nr=row_values.get("L") if sheet != "Rådata" else None,
                gdep_nr=row_values.get("K") if sheet != "Rådata" else None,
                gdep_name=row_values.get("O") if sheet != "Rådata" else None,
                omr_nr=row_values.get("M") if sheet != "Rådata" else None,
                kat_nr=row_values.get("N") if sheet != "Rådata" else None,
                register_source=f"sha256:{sha};{sheet};budsjettår=2024",
                validity_precision="aar; nøyaktige gyldighetsdatoer ukjent",
                null_reason="historisk kildekode bevart; ingen bekreftet registerkobling",
            )
            observation = AmountObservation(
                dataset="historisk",
                source_system="historisk-excel",
                source_unit_id=sha,
                source_revision_id=sha,
                interpretation_id=interpretation.id,
                pointer=SourcePointer(
                    sha,
                    f"{sheet}!{cell['cell']}",
                    col,
                    sheet,
                    row,
                    col,
                    cell["cell"],
                    raw_context,
                ),
                step_id=identity("historisk-kildeledd-1", sha, sheet, row, col),
                raw_value=cell["raw_v"]
                if cell["raw_v"] is not None
                else (cell["resolved_text"] or ""),
                amount_text=cell["resolved_text"] or "",
                amount_kr=None,
                chapter_raw=chapter_raw,
                post_raw=post_raw,
                subpost_raw=subpost_raw,
                chapter=_code(chapter_raw),
                post=_code(post_raw),
                subpost=_code(subpost_raw),
                chapter_name=row_values.get("E") if sheet == "Rådata" else row_values.get("J"),
                purpose=row_values.get("F") if sheet == "Rådata" else row_values.get("H"),
                detail_level="uavklart",
                budget_year=2024,
                year_evidence=options["year_evidence"],
                raw_type=cell["raw_type"] or "fravaerende",
                formula=(cell["formula"] or "") if cell["formula_result"] else None,
                cached_value=cell["cached_value"],
                stage_raw=record.get(col, {}).get("resolved_text") if row == 1 else rule["label"],
                scope=rule["scope"],
                organization=organization,
                documents=docs,
                anomalies=tuple(issues),
                null_reasons=(("amount_kr", "ingen godkjent kolonnetolkning"),),
            )
            budget.charge(asdict(observation))
            observations.append(observation)
            candidate_data = {
                "version": "historisk-kandidat-1",
                "observation_id": observation.id,
                "cell_id": cell["id"],
                "raw_decimal": str(number) if number is not None else None,
                "candidate_kr": str(candidate) if candidate is not None else None,
                "candidate_type": "Decimal-string",
                "candidate_multiplier": rule["candidate_multiplier"],
                "normalized_kr": None,
                "controlled_kr": None,
                "null_reason": "faglig kolonnetolkning aapen",
                "comparison_basis": candidate_control_basis(
                    col, component=sheet != "Rådata" and _code(subpost_raw) != "0"
                )
                if col in CONTROL_PROFILES
                else None,
            }
            candidate_data["id"] = identity("historisk-kandidat-1", observation.id, candidate_data)
            budget.charge(candidate_data)
            candidates.append(candidate_data)
            cell["observation_id"] = observation.id
            cell["disposition"] = "belopsobservasjon"
        elif cell["disposition"] == "uavklart":
            anomalies.append(
                Anomaly(
                    "ukjent_celle", "Innhold bevart uten kjent kolonneregel", evidence=cell["id"]
                )
            )
        cells.append(cell)
    metadata = dict(inventory.metadata)
    metadata["counts"] = {
        "cells": len(cells),
        "physical": sum(c["physical"] for c in cells),
        "absent": sum(c["state"] == "absent" for c in cells),
        "observations": len(observations),
    }
    binding = {
        "inventory_sha256": identity(cells),
        "candidates_sha256": identity(candidates),
        "rules_sha256": identity(rules),
        "metadata_sha256": identity(metadata),
        "observations_sha256": identity(tuple(asdict(o) for o in observations)),
        "predecessor_id": options["predecessor_id"],
        "pilot_storage": STORAGE_VERSION,
    }
    extraction = Extraction(
        "historisk",
        "historisk-excel",
        sha,
        sha,
        interpretation,
        Artifact(
            sha,
            "historisk-2024.xlsx",
            "lokal_original",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            len(raw),
            encode(binding),
        ),
        tuple(observations),
        tuple(anomalies),
        attempt_id,
        started,
    )
    return HistoricalSnapshot(
        extraction, tuple(cells), tuple(candidates), rules, metadata, options["predecessor_id"]
    )


def resume_historical_import(database: Path, attempt_id: str) -> HistoricalAttempt:
    attempt = read_historical_attempt(database, attempt_id)
    if attempt.status != "startet":
        return attempt
    if attempt.source_sha256 is None:
        raise ValueError("Importforsøk har ingen mottatte byte; start et nytt kildeforsøk")
    with _connect(database) as connection:
        row = connection.execute(
            "SELECT options_json,started_utc FROM historical_attempts WHERE attempt_id=?",
            (attempt_id,),
        ).fetchone()
    assert row is not None
    options = json.loads(row[0])
    try:
        raw = read_source(database, attempt.source_sha256)
        if hashlib.sha256(raw).hexdigest() != attempt.source_sha256:
            raise ValueError("Mottatte byte stemmer ikke med forsøksbindingen")
        snapshot = _build(raw, options, attempt_id, row[1])
    except (ValueError, OSError, BadZipFile, RuntimeError) as error:
        with _connect(database, writable=True) as connection:
            connection.execute(
                "UPDATE historical_attempts SET status='feilet',error=? WHERE attempt_id=?",
                (str(error), attempt_id),
            )
        return read_historical_attempt(database, attempt_id)
    with _connect(database, writable=True) as connection:
        existing = connection.execute(
            "SELECT 1 FROM historical_imports WHERE extraction_id=?", (snapshot.extraction.id,)
        ).fetchone()
        if not existing:
            content = encode(
                {
                    "cells": snapshot.cells,
                    "candidates": snapshot.candidates,
                    "column_rules": snapshot.column_rules,
                    "metadata": snapshot.metadata,
                    "predecessor_id": snapshot.predecessor_id,
                }
            )
            save_extraction_in(connection, snapshot.extraction, raw)
            connection.execute(
                "INSERT INTO historical_imports "
                "(extraction_id,content_json,content_sha256) VALUES (?,?,?)",
                (snapshot.extraction.id, content, hashlib.sha256(content.encode()).hexdigest()),
            )
        else:
            preserved = read_extraction(database, snapshot.extraction.id)
            save_extraction_in(
                connection,
                replace(
                    snapshot.extraction,
                    import_id=preserved.import_id,
                    imported_utc=preserved.imported_utc,
                ),
                raw,
            )
        connection.execute(
            "UPDATE historical_attempts SET status='lagret',extraction_id=? WHERE attempt_id=?",
            (snapshot.extraction.id, attempt_id),
        )
    read_historical_workbook(database, snapshot.extraction.id)
    return read_historical_attempt(database, attempt_id)


def read_historical_workbook(database: Path, extraction_id: str | None) -> HistoricalSnapshot:
    if extraction_id is None:
        raise ValueError("Eksakt uttrekks-ID kreves")
    with _connect(database) as connection:
        row = connection.execute(
            "SELECT content_json,content_sha256 FROM historical_imports WHERE extraction_id=?",
            (extraction_id,),
        ).fetchone()
    if row is None or hashlib.sha256(row[0].encode()).hexdigest() != row[1]:
        raise ValueError("Ukjent eller skadet historisk uttrekk")
    extraction = read_extraction(database, extraction_id)
    if extraction.id != extraction_id:
        raise ValueError("Lagret uttrekk har feil identitet")
    data = json.loads(row[0])
    binding = json.loads(extraction.artifact.metadata_json)
    if binding.get("observations_sha256") != identity(
        tuple(asdict(o) for o in extraction.observations)
    ):
        raise ValueError("Observasjoner stemmer ikke med artefaktbinding")
    with _connect(database) as connection:
        observed = dict(
            connection.execute(
                "SELECT observation_id,content_json FROM amount_observations WHERE extraction_id=?",
                (extraction_id,),
            )
        )
    expected = {o.id: encode(asdict(o)) for o in extraction.observations}
    if observed != expected:
        raise ValueError("SQLite-observasjonsrader avviker fra det immutable uttrekket")
    for key, content_key in (
        ("inventory_sha256", "cells"),
        ("candidates_sha256", "candidates"),
        ("rules_sha256", "column_rules"),
        ("metadata_sha256", "metadata"),
    ):
        if binding[key] != identity(data[content_key]):
            raise ValueError("Historisk metadata stemmer ikke med artefaktbinding")
    raw = read_source(database, extraction.artifact.sha256)
    if (
        len(raw) != extraction.artifact.byte_count
        or hashlib.sha256(raw).hexdigest() != extraction.artifact.sha256
    ):
        raise ValueError("Historisk original er skadet")
    return HistoricalSnapshot(
        extraction,
        tuple(data["cells"]),
        tuple(data["candidates"]),
        tuple(data["column_rules"]),
        data["metadata"],
        data["predecessor_id"],
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["import", "stage", "resume", "read", "attempt"])
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--year-evidence", default="uttrykkelig valgt budsjettår fra filinventar")
    parser.add_argument("--predecessor")
    parser.add_argument("--interpretation-note", default="pilotregler-3")
    parser.add_argument("--id")
    arguments = parser.parse_args()
    try:
        if arguments.command in {"import", "stage"}:
            if arguments.source is None:
                raise ValueError("--source kreves")
            attempt_id = stage_historical_workbook(
                arguments.database,
                arguments.source,
                budget_year=arguments.year,
                year_evidence=arguments.year_evidence,
                predecessor_id=arguments.predecessor,
                interpretation_note=arguments.interpretation_note,
            )
            if arguments.command == "import":
                resume_historical_import(arguments.database, attempt_id)
            result = read_historical_attempt(arguments.database, attempt_id)
        elif arguments.id is None:
            raise ValueError("Eksakt --id kreves")
        elif arguments.command == "read":
            snapshot = read_historical_workbook(arguments.database, arguments.id)
            print(
                encode(
                    {
                        "extraction_id": snapshot.extraction.id,
                        "counts": snapshot.metadata["counts"],
                        "professional_approval": False,
                        "year_complete": False,
                    }
                )
            )
            return 0
        elif arguments.command == "resume":
            result = resume_historical_import(arguments.database, arguments.id)
        else:
            result = read_historical_attempt(arguments.database, arguments.id)
        print(encode(asdict(result)))
        return 1 if result.status == "feilet" else 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(encode({"status": "feilet", "error": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
