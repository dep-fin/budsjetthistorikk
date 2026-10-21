"""Godkjente enkeltbeløp og kjedegrunnlag, adskilt fra B3/B4s tekniske avstemming."""

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from openpyxl import Workbook

from innlesning.controls import (
    ContextCache,
    _active,
    _basis,
    _freshness,
    _latest_view,
    _source,
    _target,
    read_decision,
    read_evidence,
)
from innlesning.maintenance_store import now, reading, writing
from innlesning.observations import encode, identity, read_extraction
from innlesning.organization_register import REGISTER_SNAPSHOT
from innlesning.registers import read_register
from innlesning.workfiles import safe_output

from .extraction_excel import add_source_text, write_rows
from .history import HistorySelection, calculate_history


@dataclass(frozen=True)
class ControlledRow:
    observation_id: str
    extraction_id: str
    raw_value: str
    raw_amount_kr: int | None
    effective_amount_kr: int | None
    decision_id: str | None
    status: str
    freshness: str
    approved_fields: str
    approved_use: str
    reason: str
    reviewer: str
    evidence_id: str
    evidence_json: str
    remaining_anomalies: tuple[str, ...]


@dataclass(frozen=True)
class ControlledResult:
    id: str
    created_utc: str
    extraction_ids: tuple[str, ...]
    register_snapshot: str
    control_basis: str
    input_observation_ids: tuple[str, ...]
    applied_decision_ids: tuple[str, ...]
    rows: tuple[ControlledRow, ...]
    activation_basis_json: str
    source_basis_json: str
    context_basis_json: str
    technical_calculation_id: str | None = None
    chain_balance: int | None = None
    complete: bool = False
    freshness: str = "gjeldende"
    coverage: str = (
        "Bare valgte uttrekk; enkeltgodkjenning er ingen faglig kjede- eller årsgodkjenning."
    )

    @property
    def approved_chain_balance(self) -> int | None:
        return self.chain_balance if self.complete and self.freshness == "gjeldende" else None


def reprocess_controlled(
    database: Path,
    extraction_ids: tuple[str, ...],
    register_snapshot: str,
    control_basis: str,
    *,
    selection: HistorySelection | None = None,
) -> ControlledResult:
    """Bruk bare eksplisitt aktivert grunnlag og siste avgjørelse; ingen eldre reservevalg."""
    ids = tuple(sorted(extraction_ids))
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Velg ulike uttrekk")
    extractions = tuple(read_extraction(database, i) for i in ids)
    if len({e.dataset for e in extractions}) != 1:
        raise ValueError("Datasett kan ikke blandes")
    register = (
        read_register(database, register_snapshot)
        if register_snapshot != REGISTER_SNAPSHOT
        else None
    )
    rows: list[ControlledRow] = []
    activation_basis: list[dict[str, Any]] = []
    source_basis: list[dict[str, str]] = []
    context_basis: list[dict[str, str]] = []
    with writing(database) as connection:
        contexts: ContextCache = {}
        for extraction in extractions:
            if extraction.interpretation.register_snapshot != register_snapshot:
                raise ValueError("Nybehandling krever valgt registersnapshot i selve tolkningen")
            active = _active(connection, extraction)
            if not active or any(
                active[k] != v
                for k, v in _basis(extraction, register_snapshot, control_basis).items()
            ):
                raise ValueError("Valgt grunnlag er ikke aktivert")
            activation_basis.append({"scope": extraction.source_unit_id, **active})
            source = _source(connection, database, extraction)
            contexts[extraction.id] = extraction, source, active
            context_basis.append(
                {
                    "extraction_id": extraction.id,
                    "activation_generation": str(active["generation"]),
                    "register_snapshot": register_snapshot,
                    "control_basis": control_basis,
                    "source_generation": str(source["generation"] or ""),
                    "kildekontekst": encode(source),
                }
            )
            for observation in extraction.observations:
                if selection is not None and (
                    observation.budget_year not in (None, selection.budget_year)
                    or observation.chapter not in (None, selection.chapter)
                    or observation.post not in (None, selection.post)
                    or (
                        observation.detail_level in {"post", "underpost"}
                        and observation.detail_level != selection.detail_level
                    )
                    or (
                        observation.detail_level == "underpost"
                        and observation.subpost not in (None, selection.subpost)
                    )
                ):
                    continue
                target = _target(
                    connection,
                    database,
                    extraction,
                    observation,
                    register_snapshot,
                    control_basis,
                    "beregning",
                    contexts,
                    register,
                )
                source_basis.append(target)
                current_freshness = _freshness(connection, database, target, contexts)[0]
                view = _latest_view(connection, database, observation.id, contexts)
                decision = view.decision if view else None
                freshness = view.freshness if view else current_freshness
                effective = None
                approved = bool(
                    decision
                    and decision.status == "godkjent"
                    and freshness == "gjeldende"
                    and "amount_kr" in decision.approved_fields.split(",")
                    and decision.approved_use in {"analysebelop", "kjedegrunnlag"}
                )
                if approved and decision:
                    effective = (
                        decision.corrected_amount_kr
                        if decision.corrected_amount_kr is not None
                        else observation.amount_kr
                    )
                remaining = [a.code for a in observation.anomalies]
                if decision and decision.corrected_amount_kr is not None:
                    remaining.append("representasjonsavvik_bevart")
                if not observation.organization.fdep_nr:
                    remaining.append("mangler_organisasjonsoppslag")
                if register is None or not register.catalogued(
                    observation.chapter, observation.post, observation.budget_year
                ):
                    remaining.append("mangler_kataloggodkjenning")
                if not approved:
                    remaining.append("ikke_godkjent_analysebelop")
                rows.append(
                    ControlledRow(
                        observation.id,
                        extraction.id,
                        observation.raw_value,
                        observation.amount_kr,
                        effective,
                        decision.id if decision else None,
                        decision.status if decision else "til_kontroll",
                        freshness,
                        decision.approved_fields if decision else "",
                        decision.approved_use if decision else "",
                        decision.reason if decision else "Ingen faglig avgjørelse",
                        decision.reviewer if decision else "",
                        decision.evidence_id if decision else "",
                        encode(asdict(read_evidence(database, decision.evidence_id)))
                        if decision and decision.evidence_id
                        else "{}",
                        tuple(dict.fromkeys(remaining)),
                    )
                )
        technical = None
        chain_balance = None
        if selection is not None:
            if set(selection.extraction_ids) != set(ids):
                raise ValueError("Kjedeutvalget må bruke de eksplisitt valgte uttrekkene")
            # Regnekontrollen kjøres utenfor denne skrivelåsen nedenfor.
        applied = tuple(
            sorted(r.decision_id for r in rows if r.decision_id and r.freshness == "gjeldende")
        )
        result = ControlledResult(
            identity(
                "kontrollert-resultat-v1",
                ids,
                register_snapshot,
                control_basis,
                activation_basis,
                [
                    (
                        t["extraction_id"],
                        t["source_generation"],
                        json.loads(t["kildekontekst"])["revision"],
                    )
                    for t in context_basis
                ],
                [(r.observation_id, r.decision_id, r.freshness) for r in rows],
                [(t["extraction_id"], t["source_generation"], t["ferskhet"]) for t in source_basis],
                asdict(selection) if selection else None,
            ),
            now(),
            ids,
            register_snapshot,
            control_basis,
            tuple(sorted(r.observation_id for r in rows)),
            applied,
            tuple(rows),
            encode(activation_basis),
            encode(source_basis),
            encode(context_basis),
            technical,
            chain_balance,
        )
    if selection is not None:
        calculation = calculate_history(database, selection)
        by_id = {r.observation_id: r for r in result.rows}
        eligible = [by_id[i] for i in calculation.input_observation_ids]
        if (
            calculation.approved_balance is not None
            and eligible
            and all(
                r.effective_amount_kr is not None
                and r.approved_use == "kjedegrunnlag"
                and r.effective_amount_kr == r.raw_amount_kr
                and not r.remaining_anomalies
                for r in eligible
            )
        ):
            result = replace(
                result,
                technical_calculation_id=calculation.id,
                chain_balance=calculation.approved_balance,
                complete=True,
            )
        else:
            result = replace(result, technical_calculation_id=calculation.id)
    with writing(database) as connection:
        contexts = {}
        # Hele grunnlaget revalideres mens ingen annen skriver kan endre aktivering/kilde/kontroll.
        for target in context_basis:
            freshness, source = _freshness(connection, database, target, contexts)
            original_source = json.loads(target["kildekontekst"])
            if (
                source["generation"] != original_source["generation"]
                or source["revision"] != original_source["revision"]
            ):
                raise ValueError("Kildegrunnlaget endret seg under nybehandling")
            active = contexts[target["extraction_id"]][2]
            if active is None or active["generation"] != int(target["activation_generation"]):
                raise ValueError("Aktivt grunnlag endret seg under nybehandling")
        for target in source_basis:
            if _freshness(connection, database, target, contexts)[0] != target["ferskhet"]:
                raise ValueError("Grunnlaget endret seg under nybehandling; kjør på nytt")
            view = _latest_view(connection, database, target["observation_id"], contexts)
            if (view.decision.id if view else "") != target["forgjenger"]:
                raise ValueError("Kontrollavgjørelse endret seg under nybehandling")
        connection.execute(
            "INSERT OR IGNORE INTO controlled_results VALUES (?,?)",
            (result.id, encode(asdict(result))),
        )
    return read_controlled(database, result.id)


def read_controlled(database: Path, identifier: str) -> ControlledResult:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT content FROM controlled_results WHERE id=?", (identifier,)
        ).fetchone()
        if not row:
            raise ValueError("Ukjent kontrollert resultat")
        data = json.loads(row[0])
        for key in ("extraction_ids", "input_observation_ids", "applied_decision_ids"):
            data[key] = tuple(data[key])
        data["rows"] = tuple(
            ControlledRow(**{**r, "remaining_anomalies": tuple(r["remaining_anomalies"])})
            for r in data["rows"]
        )
        result = ControlledResult(**data)
        freshness = "gjeldende"
        contexts: ContextCache = {}
        for target in json.loads(result.context_basis_json):
            current = _freshness(connection, database, target, contexts)[0]
            if current == "utdatert" or freshness == "gjeldende":
                freshness = current
        for target in json.loads(result.source_basis_json):
            current = _freshness(connection, database, target, contexts)[0]
            view = _latest_view(connection, database, target["observation_id"], contexts)
            if (view.decision.id if view else "") != target["forgjenger"]:
                current = "utdatert"
            if current == "utdatert" or freshness == "gjeldende":
                freshness = current
    return replace(result, freshness=freshness)


def export_controlled_excel(database: Path, identifier: str, output: Path) -> None:
    import os
    from tempfile import NamedTemporaryFile

    safe_output(database, output)
    result = read_controlled(database, identifier)
    book = Workbook()
    book.remove(book.active)  # type: ignore[arg-type]
    write_rows(
        book,
        "Kontrollert resultat",
        [
            ["Resultat", result.id],
            ["Register", result.register_snapshot],
            ["Kontrollgrunnlag", result.control_basis],
            ["Ferskhet", result.freshness],
            ["Dekningsgrense", result.coverage],
            ["Kilde-/aktiveringsgrunnlag", result.context_basis_json],
            ["Godkjent kjedesaldo", result.approved_chain_balance],
            [
                "Kjedestatus",
                "godkjent avgrenset utvalg"
                if result.approved_chain_balance is not None
                else "ufullstendig",
            ],
        ],
    )
    rows: list[list[str | int | None]] = [
        [
            "Observasjon",
            "Uttrekk",
            "Råverdi",
            "Råbeløp kr",
            "Avklart beløp kr (historisk resultat)",
            "Gjeldende godkjent beløp kr",
            "Avgjørelse",
            "Faglig status",
            "Ferskhet",
            "Godkjente felter",
            "Godkjent bruk",
            "Begrunnelse",
            "Kontrollør",
            "Bevis-ID",
            "Bevis",
            "Gjenstående avvik",
        ]
    ]
    for r in result.rows:
        view = read_decision(database, r.decision_id) if r.decision_id else None
        freshness = view.freshness if view else result.freshness
        rows.append(
            [
                r.observation_id,
                r.extraction_id,
                r.raw_value,
                r.raw_amount_kr,
                r.effective_amount_kr,
                r.effective_amount_kr if freshness == "gjeldende" else None,
                r.decision_id,
                r.status,
                freshness,
                r.approved_fields,
                r.approved_use,
                r.reason,
                r.reviewer,
                r.evidence_id,
                r.evidence_json,
                ", ".join(r.remaining_anomalies),
            ]
        )
    write_rows(book, "Beløp og avgjørelser", rows)
    targets = json.loads(result.source_basis_json)
    if targets:
        keys = tuple(k for k in targets[0] if k != "eksport_id")
        binding_rows: list[list[str | int | None]] = [list(keys)]
        binding_rows.extend([target[k] for k in keys] for target in targets)
        write_rows(book, "Kilde- og kontrollbinding", binding_rows)
    add_source_text(book, database, result.extraction_ids)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".xlsx", delete=False) as handle:
            temporary = Path(handle.name)
        book.save(temporary)
        os.replace(temporary, output)
    finally:
        book.close()
        if temporary:
            temporary.unlink(missing_ok=True)
