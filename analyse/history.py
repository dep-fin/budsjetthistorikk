"""Eksplisitt valgt historikk. Observerte verdier og avledede saldoer er adskilt."""

import json
import sqlite3
from collections import defaultdict
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from innlesning.observations import (
    AmountObservation,
    Anomaly,
    Extraction,
    encode,
    identity,
    initialize_observations,
    read_extraction,
)
from innlesning.storage import check_schema
from innlesning.sync import read_revision

RULE_VERSION = "vedtatt-kjede-v1"
COVERAGE = (
    "Bare uttrykkelig valgte revisjoner/tolkninger, konto og budsjettår. "
    "Ingen garanti om komplett sesjon eller år. Avstemt utvalg er ikke faglig godkjenning."
)


@dataclass(frozen=True)
class HistorySelection:
    dataset: str
    extraction_ids: tuple[str, ...]
    budget_year: int
    chapter: str
    post: str
    subpost: str | None = None
    detail_level: str = "post"
    # Eksplisitt kildebelagt rekkefølge ved lik/manglende dato. Aldri radrekkefølge.
    step_order: tuple[str, ...] = ()
    order_evidence: str | None = None
    register_basis: str = "Ingen registerkobling brukt"
    control_basis: str = "Automatiske lokale og kronologiske kontroller; ingen manuell godkjenning"

    def __post_init__(self) -> None:
        if (
            not self.extraction_ids
            or any(not isinstance(id, str) or not id for id in self.extraction_ids)
            or len(set(self.extraction_ids)) != len(self.extraction_ids)
        ):
            raise ValueError("Velg ikke-tomme, ulike uttrekks-ID-er")
        if type(self.budget_year) is not int or not 1000 <= self.budget_year <= 9999:
            raise ValueError("Budsjettår må være et firesifret heltall")
        if self.dataset not in {"produksjon", "prove", "historisk"}:
            raise ValueError("Ukjent datasett")
        for code in (self.chapter, self.post, self.subpost):
            if code is not None and (
                not isinstance(code, str)
                or not code.isascii()
                or not code.isdigit()
                or str(int(code)) != code
            ):
                raise ValueError("Utvalget krever normaliserte kontokoder")
        if self.detail_level not in {"post", "underpost"}:
            raise ValueError("Velg post eller underpost eksplisitt")
        if self.detail_level == "underpost" and self.subpost is None:
            raise ValueError("Underpostutvalg krever konkret kode; ukjent er ikke 0")
        if self.detail_level == "post" and self.subpost is not None:
            raise ValueError("Posttotal kan ikke samtidig velge underpost")
        if self.step_order and not self.order_evidence:
            raise ValueError("Eksplisitt rekkefølge krever kildebevis")


@dataclass(frozen=True)
class HistoryStep:
    step_id: str
    source_unit_id: str
    source_revision_id: str
    decision_date: str | None
    round: str
    original: int | None
    delta: int | None
    before: int | None
    after: int | None
    balance: int | None
    observation_ids: tuple[str, ...]
    status: str
    anomalies: tuple[str, ...]


@dataclass(frozen=True)
class SourceContext:
    extraction_id: str
    source_system: str
    revision_id: str
    generation: int | None
    current_revision_id: str | None
    source_sha256: str
    fingerprint: str | None
    fingerprint_version: str | None
    latest_observation_id: str | None
    latest_source_sha256: str | None
    latest_attempt_status: str | None
    observation_status: str | None
    controls_json: str


@dataclass(frozen=True)
class HistoryCalculation:
    id: str
    selection: HistorySelection
    rule_version: str
    created_utc: str
    input_observation_ids: tuple[str, ...]
    steps: tuple[HistoryStep, ...]
    calculated_balance: int | None
    status: str
    anomalies: tuple[Anomaly, ...]
    contexts: tuple[SourceContext, ...]
    coverage: str = COVERAGE
    freshness: str = "samme kildegrunnlag"
    current_contexts: tuple[SourceContext, ...] = ()
    assessed_utc: str | None = None

    @property
    def approved_balance(self) -> int | None:
        """Kun avstemming av det avgrensede utvalget, aldri komplett årsgodkjenning."""
        return (
            self.calculated_balance
            if self.status == "avstemt_utvalg" and self.freshness == "samme kildegrunnlag"
            else None
        )


def _context(database: Path, extraction: Extraction) -> SourceContext:
    if extraction.source_system != "storting":
        return SourceContext(
            extraction.id,
            extraction.source_system,
            extraction.source_revision_id,
            None,
            None,
            extraction.artifact.sha256,
            None,
            None,
            None,
            None,
            None,
            None,
            "[]",
        )
    revision = read_revision(database, extraction.source_revision_id)
    decision = revision.report.decision
    if decision is None:
        raise ValueError("B3-kildegrunnlaget mangler vedtaksmetadata")
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as connection:
        generation = connection.execute(
            "SELECT generation FROM decision_heads WHERE dataset=? AND session=? AND decision_id=?",
            (revision.dataset, decision.session, decision.id),
        ).fetchone()[0]
    return SourceContext(
        extraction.id,
        extraction.source_system,
        extraction.source_revision_id,
        generation,
        revision.current_revision_id,
        extraction.artifact.sha256,
        revision.fingerprint,
        revision.fingerprint_version,
        revision.current_observation_id,
        revision.current_source_sha256,
        revision.latest_attempt_status,
        revision.observation_status,
        encode([asdict(control) for control in revision.controls]),
    )


def _basis(contexts: tuple[SourceContext, ...]) -> tuple[tuple[object, ...], ...]:
    # Volatil konvolutttid og ny henting av samme innhold skaper ingen ny beregning.
    return tuple(
        (
            context.extraction_id,
            context.generation,
            context.current_revision_id,
            context.controls_json,
        )
        for context in contexts
    )


def _value(by_meaning: dict[str, list[AmountObservation]], meaning: str) -> int | None:
    rows = by_meaning.get(meaning, [])
    return rows[0].amount_kr if len(rows) == 1 else None


def calculate_history(database: Path, selection: HistorySelection) -> HistoryCalculation:
    """Beregn og bevar ett reproduserbart utvalg; ingen latest eller automatisk import."""
    extractions = tuple(read_extraction(database, id) for id in sorted(selection.extraction_ids))
    if any(extraction.dataset != selection.dataset for extraction in extractions):
        raise ValueError("Datasett kan ikke blandes i en beregning")
    contexts = tuple(_context(database, extraction) for extraction in extractions)
    selection = replace(selection, extraction_ids=tuple(sorted(selection.extraction_ids)))
    issues: list[Anomaly] = []
    revisions: dict[str, set[tuple[str, str]]] = defaultdict(set)
    observations: list[AmountObservation] = []
    for extraction in extractions:
        revisions[extraction.source_unit_id].add(
            (extraction.source_revision_id, extraction.interpretation.id)
        )
        for anomaly in extraction.anomalies:
            if anomaly.code == "ingen_bevilgningstabell":
                continue
            if (
                anomaly.budget_year in (None, selection.budget_year)
                and anomaly.chapter in (None, selection.chapter)
                and anomaly.post in (None, selection.post)
            ):
                issues.append(anomaly)
        for observation in extraction.observations:
            if observation.budget_year not in (None, selection.budget_year):
                continue
            same_or_unknown_account = observation.chapter in (
                None,
                selection.chapter,
            ) and observation.post in (None, selection.post)
            uncertain_account = observation.chapter is None or observation.post is None
            uncertain_level = observation.detail_level not in {"post", "underpost"}
            uncertain_subpost = (
                selection.detail_level == "underpost"
                and observation.detail_level == "underpost"
                and observation.subpost is None
            )
            if same_or_unknown_account and (
                uncertain_account or uncertain_level or uncertain_subpost
            ):
                issues.append(
                    Anomaly(
                        "uavklart_kontoutvalg",
                        "Valgt kilde har uavklart konto eller nivå",
                        evidence=observation.id,
                    )
                )
                observations.append(observation)
                continue
            if (
                observation.chapter,
                observation.post,
                observation.subpost,
                observation.detail_level,
            ) != (selection.chapter, selection.post, selection.subpost, selection.detail_level):
                continue
            observations.append(observation)
    if any(len(values) != 1 for values in revisions.values()):
        issues.append(
            Anomaly("motstridende_grunnlag", "Velg én revisjon og én tolkning per kildeenhet")
        )
    if not observations:
        issues.append(Anomaly("ingen_observasjoner", "Ingen beløp for valgt konto og budsjettår"))
    groups: dict[str, list[AmountObservation]] = defaultdict(list)
    for observation in observations:
        if observation.information_type not in {
            "bevilgning",
            "fullmaktsramme",
            "sats",
            "overforte_midler",
        }:
            issues.append(
                Anomaly("ukjent_ledd", "Uavklart opplysningstype", evidence=observation.id)
            )
            continue
        if (
            observation.information_type != "bevilgning"
            or observation.figure_type
            in {
                "regjeringsforslag",
                "komiteforslag",
                "regnskap",
            }
            or observation.scope == "aggregat"
        ):
            continue
        if observation.figure_type != "stortingsvedtak" or observation.scope != "enkeltledd":
            issues.append(
                Anomaly("ukjent_ledd", "Uavklart talltype eller omfang", evidence=observation.id)
            )
            continue
        groups[observation.step_id].append(observation)
    dates = {id: {o.decision_date for o in group} for id, group in groups.items()}
    order: list[str]
    if selection.step_order:
        if len(set(selection.step_order)) != len(selection.step_order) or set(
            selection.step_order
        ) != set(groups):
            raise ValueError("Eksplisitt rekkefølge må inneholde hvert valgt ledd nøyaktig én gang")
        order = list(selection.step_order)
        known_dates = [
            str(next(iter(dates[id])))
            for id in order
            if len(dates[id]) == 1 and None not in dates[id]
        ]
        if known_dates != sorted(known_dates):
            issues.append(
                Anomaly("motstrid_rekkefolge", "Valgt rekkefølge strider mot vedtaksdatoene")
            )
    else:
        known = [
            next(iter(values))
            for values in dates.values()
            if len(values) == 1 and None not in values
        ]
        if len(known) != len(groups) or len(set(known)) != len(known):
            issues.append(
                Anomaly(
                    "uavklart_rekkefolge",
                    "Dato mangler, er motstridende eller deles av flere ledd; "
                    "krever kildebelagt valg",
                )
            )
        order = sorted(groups, key=lambda id: (str(next(iter(dates[id]))), id))
    originals = [
        o
        for group in groups.values()
        for o in group
        if o.meaning == "nivaa" and o.round == "opprinnelig"
    ]
    if len(originals) != 1:
        issues.append(
            Anomaly(
                "manglende_start" if not originals else "flere_startniva",
                "Krever nøyaktig ett opprinnelig nivå; førbeløp og (Ny) er ikke nullstart",
            )
        )
    balance: int | None = None
    steps: list[HistoryStep] = []
    broken = bool(issues)
    for index, step_id in enumerate(order):
        group = groups[step_id]
        first = group[0]
        by_meaning: dict[str, list[AmountObservation]] = defaultdict(list)
        step_issues: list[str] = []
        for observation in group:
            by_meaning[observation.meaning].append(observation)
            if (
                observation.structure_status != "strukturert"
                or observation.amount_kr is None
                or observation.budget_year is None
            ):
                step_issues.append("uavklart_observasjon")
            if (
                observation.currency != "NOK"
                or not observation.multiplier
                or not observation.conversion_rule
                or not observation.normalization_evidence
            ):
                step_issues.append("uavklart_normalisering")
            step_issues.extend(anomaly.code for anomaly in observation.anomalies)
            if observation.meaning == "uavklart" or observation.professional_status == "avvist":
                step_issues.append("ukjent_ledd")
        if any(len(values) != 1 for values in by_meaning.values()):
            step_issues.append("gjentatt_belopsrolle")

        original, delta, before, after = (
            _value(by_meaning, meaning)
            for meaning in ("nivaa", "endring", "for_belop", "etter_belop")
        )
        if "nivaa" in by_meaning:
            if index != 0 or first.round != "opprinnelig" or "endring" in by_meaning:
                step_issues.append("ukjent_startledd")
            if original is not None and not broken and not step_issues:
                balance = original
        elif "endring" not in by_meaning:
            step_issues.append("mangler_delta")
        else:
            if (
                before is not None
                and delta is not None
                and after is not None
                and before + delta != after
            ):
                step_issues.append("lokal_konflikt")
            if balance is not None and before is not None and balance != before:
                step_issues.append("kjedekonflikt")
            if (
                balance is not None
                and delta is not None
                and after is not None
                and balance + delta != after
            ):
                step_issues.append("etter_konflikt")
            if balance is None:
                step_issues.append("manglende_inngaende")
            if not broken and not step_issues and balance is not None and delta is not None:
                balance += delta
                if abs(balance) > 9_007_199_254_740_991:
                    step_issues.append("saldo_utenfor_presisjon")
        if step_issues:
            broken = True
            balance = None
            issues.extend(
                Anomaly(code, "Historikkleddet krever kontroll", evidence=step_id)
                for code in dict.fromkeys(step_issues)
            )
        steps.append(
            HistoryStep(
                step_id,
                first.source_unit_id,
                first.source_revision_id,
                first.decision_date,
                first.round,
                original,
                delta,
                before,
                after,
                balance,
                tuple(sorted(o.id for o in group)),
                "til_kontroll" if broken else "avstemt_utvalg",
                tuple(dict.fromkeys(step_issues)),
            )
        )
    input_ids = tuple(sorted(o.id for o in observations))
    calculation_id = identity(RULE_VERSION, asdict(selection), input_ids, _basis(contexts))
    result = HistoryCalculation(
        calculation_id,
        selection,
        RULE_VERSION,
        datetime.now(UTC).isoformat(),
        input_ids,
        tuple(steps),
        balance,
        "ufullstendig" if issues or balance is None else "avstemt_utvalg",
        tuple(issues),
        contexts,
    )
    with sqlite3.connect(database) as connection:
        connection.execute("BEGIN IMMEDIATE")
        initialize_observations(connection)
        connection.execute(
            "INSERT OR IGNORE INTO history_calculations "
            "(calculation_id,content_json,created_utc) VALUES (?,?,?)",
            (result.id, encode(asdict(result)), result.created_utc),
        )
    return read_history(database, result.id)


def _calculation_from_dict(data: dict[str, Any]) -> HistoryCalculation:
    data = dict(data)
    selection = data["selection"]
    selection["extraction_ids"] = tuple(selection["extraction_ids"])
    selection["step_order"] = tuple(selection["step_order"])
    data["selection"] = HistorySelection(**selection)
    data["input_observation_ids"] = tuple(data["input_observation_ids"])
    data["steps"] = tuple(
        HistoryStep(
            **{
                **step,
                "observation_ids": tuple(step["observation_ids"]),
                "anomalies": tuple(step["anomalies"]),
            }
        )
        for step in data["steps"]
    )
    data["anomalies"] = tuple(
        Anomaly(**{**issue, "affected_fields": tuple(issue["affected_fields"])})
        for issue in data["anomalies"]
    )
    for name in ("contexts", "current_contexts"):
        data[name] = tuple(SourceContext(**context) for context in data[name])
    return HistoryCalculation(**data)


def read_history(database: Path, calculation_id: str) -> HistoryCalculation:
    """Bevart beregning med separat nåværende kilde-/kontrollkontekst."""
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as connection:
        check_schema(connection)
        row = connection.execute(
            "SELECT content_json FROM history_calculations WHERE calculation_id=?",
            (calculation_id,),
        ).fetchone()
    if row is None:
        raise ValueError(f"Ukjent beregning: {calculation_id}")
    result = _calculation_from_dict(json.loads(row[0]))
    current = tuple(
        _context(database, read_extraction(database, id)) for id in result.selection.extraction_ids
    )
    freshness = (
        "samme kildegrunnlag"
        if _basis(current) == _basis(result.contexts)
        else "utdatert kilde-/kontrollgrunnlag"
    )
    if freshness == "samme kildegrunnlag" and any(
        context.latest_attempt_status not in (None, "fullfort")
        or context.observation_status == "mangler i siste fulle svar"
        for context in current
    ):
        freshness = "ikke vurderbart kildegrunnlag"
    return replace(
        result,
        freshness=freshness,
        current_contexts=current,
        assessed_utc=datetime.now(UTC).isoformat(),
    )
