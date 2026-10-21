"""Uttrykkelig sammenstilling av lagrede inventarer, uttrekk og kontrollresultater.

Lesing oppdager, tolker, aktiverer og godkjenner ingenting. Teknisk saldo fra B3
er fortsatt en annen opplysning enn et faglig godkjent analysetall.
"""

import re
import sqlite3
from collections import defaultdict
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from innlesning.controls import read_decisions
from innlesning.observations import AmountObservation, Extraction, identity, read_extraction
from innlesning.sync import InventoryContext, InventorySnapshot, read_inventory, read_revision

from .controlled import ControlledResult, ControlledRow, read_controlled
from .history import HistoryCalculation, read_history
from .preserved_controls import PreservedControl, audit_preserved_2024
from .session_reconciliation import (
    Reconciliation,
    ReconciliationResult,
    SourceCheck,
    SourceExpectation,
    check_source,
    reconcile,
)


def _ids(values: tuple[str, ...], name: str) -> None:
    if (
        not isinstance(values, tuple)
        or any(not isinstance(v, str) or not v.strip() or v.strip() != v for v in values)
        or len(set(values)) != len(values)
    ):
        raise ValueError(f"{name} må være ulike, ikke-tomme tekstverdier")


@dataclass(frozen=True)
class SessionSelection:
    dataset: str
    session: str
    inventory_job_ids: tuple[str, ...]
    extraction_ids: tuple[str, ...] = ()
    controlled_result_ids: tuple[str, ...] = ()
    history_calculation_ids: tuple[str, ...] = ()
    supplemental_inventory_job_ids: tuple[str, ...] = ()
    budget_years: tuple[int, ...] = ()
    fdep_nrs: tuple[str, ...] = ()
    chapters: tuple[str, ...] = ()
    posts: tuple[str, ...] = ()
    reconciliations: tuple[Reconciliation, ...] = ()
    source_expectations: tuple[SourceExpectation, ...] = ()
    preserved_2024_controls: str | None = None

    def __post_init__(self) -> None:
        if self.dataset not in {"produksjon", "prove"}:
            raise ValueError("Sesjonsuttrekk krever produksjon eller prove")
        if not isinstance(self.session, str) or not re.fullmatch(r"20\d{2}-20\d{2}", self.session):
            raise ValueError("Sesjon krever ÅÅÅÅ-ÅÅÅÅ")
        a, b = map(int, self.session.split("-"))
        if b != a + 1:
            raise ValueError("Sesjonens år må følge hverandre")
        for field in (
            "inventory_job_ids",
            "extraction_ids",
            "controlled_result_ids",
            "history_calculation_ids",
            "supplemental_inventory_job_ids",
            "fdep_nrs",
            "chapters",
            "posts",
        ):
            _ids(getattr(self, field), field)
        if not self.inventory_job_ids:
            raise ValueError("Velg hovedsesjonens inventar uttrykkelig")
        if set(self.inventory_job_ids) & set(self.supplemental_inventory_job_ids):
            raise ValueError("Hovedinventar og supplerende inventar må være forskjellige")
        if (
            not isinstance(self.budget_years, tuple)
            or any(type(v) is not int or not 1000 <= v <= 9999 for v in self.budget_years)
            or len(set(self.budget_years)) != len(self.budget_years)
        ):
            raise ValueError("Budsjettår må være ulike firesifrede heltall")
        for codes in (self.chapters, self.posts):
            if any(not c.isascii() or not c.isdigit() or str(int(c)) != c for c in codes):
                raise ValueError("Kapittel og post krever normaliserte kontokoder")
        if not isinstance(self.reconciliations, tuple) or any(
            not isinstance(r, Reconciliation) for r in self.reconciliations
        ):
            raise ValueError("Avstemminger må følge den validerte modellen")
        if not isinstance(self.source_expectations, tuple) or any(
            not isinstance(r, SourceExpectation) for r in self.source_expectations
        ):
            raise ValueError("Kildeprøver må følge den validerte modellen")
        if len({r.name for r in self.reconciliations}) != len(self.reconciliations) or len(
            {r.observation_id for r in self.source_expectations}
        ) != len(self.source_expectations):
            raise ValueError("Avstemmingsnavn og kildeprøve-ID-er må være ulike")
        if self.preserved_2024_controls is not None and (
            not isinstance(self.preserved_2024_controls, str) or not self.preserved_2024_controls
        ):
            raise ValueError("Kontrollmappe må være en ikke-tom bane")


def selection_from_dict(data: dict[str, Any]) -> SessionSelection:
    """Strengt JSON-format; ukjente felter og skalarer avvises."""
    values = dict(data)
    for name in (
        "inventory_job_ids",
        "extraction_ids",
        "controlled_result_ids",
        "history_calculation_ids",
        "supplemental_inventory_job_ids",
        "budget_years",
        "fdep_nrs",
        "chapters",
        "posts",
        "reconciliations",
        "source_expectations",
    ):
        if name in values:
            if not isinstance(values[name], list):
                raise ValueError(f"{name} må være en JSON-liste")
            values[name] = tuple(values[name])
    values["reconciliations"] = tuple(
        Reconciliation.from_dict(r) for r in values.get("reconciliations", ())
    )
    values["source_expectations"] = tuple(
        SourceExpectation(**r) for r in values.get("source_expectations", ())
    )
    return SessionSelection(**values)


@dataclass(frozen=True)
class SessionRow:
    observation: AmountObservation
    extraction_id: str
    selection_status: str
    supplemental: bool
    controlled_result_ids: tuple[str, ...]
    controlled: ControlledRow | None
    historical_effective_amount_kr: int | None
    corrected_amount_kr: int | None
    approved_amount_kr: int | None
    freshness: str
    issues: tuple[str, ...]


@dataclass(frozen=True)
class InventoryRow:
    session: str
    decision_id: str
    revision_id: str
    job_ids: tuple[str, ...]
    supplemental: bool
    api_type: str
    date: str | None
    title: str
    url: str
    source_sha256: str
    extraction_ids: tuple[str, ...]
    content_status: str
    structure_status: str
    observation_count: int
    selected_count: int
    unresolved_count: int
    excluded_count: int
    approved_count: int
    context: InventoryContext
    issues: tuple[str, ...]


@dataclass(frozen=True)
class Coverage:
    session: str
    supplemental: bool
    inventory_count: int
    source_count: int
    structured_count: int
    observation_count: int
    approved_count: int
    source_complete: bool
    structure_complete: bool
    professional_complete: bool = False
    boundary: str = (
        "Kildeinnhold, struktur og faglig godkjente enkeltverdier er ulike nivåer. "
        "Ingen erklæring om uttømmende sesjon eller budsjettår."
    )


@dataclass(frozen=True)
class SessionSum:
    budget_year: int | None
    meaning: str
    detail_level: str
    budget_side: str
    currency: str | None
    multiplier: str | None
    approved_subtotal_kr: int | None
    complete_total_kr: int | None
    included_observation_ids: tuple[str, ...]
    excluded_observation_ids: tuple[str, ...]
    issues: tuple[str, ...]


@dataclass(frozen=True)
class SessionReport:
    id: str
    selection: SessionSelection
    assessed_utc: str
    snapshot: InventorySnapshot
    inventory: tuple[InventoryRow, ...]
    rows: tuple[SessionRow, ...]
    coverage: Coverage
    supplemental_coverage: tuple[Coverage, ...]
    sums: tuple[SessionSum, ...]
    histories: tuple[HistoryCalculation, ...]
    controlled_results: tuple[ControlledResult, ...]
    issues: tuple[str, ...]
    unfiltered_rows: tuple[SessionRow, ...]
    reconciliations: tuple[ReconciliationResult, ...] = ()
    source_checks: tuple[SourceCheck, ...] = ()
    independent_control: PreservedControl | None = None


def _match(observation: AmountObservation, selection: SessionSelection) -> str:
    unknown = False
    for values, value in (
        (selection.budget_years, observation.budget_year),
        (selection.fdep_nrs, observation.organization.fdep_nr),
        (selection.chapters, observation.chapter),
        (selection.posts, observation.post),
    ):
        if values:
            if value is None:
                unknown = True
            elif value not in values:
                return "utenfor"
    return "uavklart_treff" if unknown else "treff"


def _account(o: AmountObservation) -> tuple[Any, ...]:
    return o.budget_year, o.chapter, o.post, o.subpost, o.detail_level


def _chain_issues(rows: list[SessionRow]) -> dict[tuple[Any, ...], tuple[str, ...]]:
    """Konservative sperrer for summer, uten ny B3-beregning eller godkjenning."""
    accounts: dict[tuple[Any, ...], list[AmountObservation]] = defaultdict(list)
    for row in rows:
        o = row.observation
        if o.information_type == "bevilgning" and o.figure_type == "stortingsvedtak":
            accounts[_account(o)].append(o)
    result: dict[tuple[Any, ...], tuple[str, ...]] = {}
    for account, observations in accounts.items():
        issues: list[str] = []
        groups: dict[str, list[AmountObservation]] = defaultdict(list)
        for o in observations:
            groups[o.step_id].append(o)
        starts = [o for o in observations if o.meaning == "nivaa" and o.round == "opprinnelig"]
        if len(starts) != 1:
            issues.append("manglende_start" if not starts else "flere_startniva")
        dates = {step: {o.decision_date for o in group} for step, group in groups.items()}
        if any(len(d) != 1 or None in d for d in dates.values()):
            issues.append("uavklart_rekkefolge")
        date_values = [str(next(iter(d))) for d in dates.values()]
        if len(set(date_values)) != len(date_values):
            issues.append("uavklart_rekkefolge")
        balance: int | None = None
        for index, step in enumerate(
            sorted(groups, key=lambda s: (min(str(d) for d in dates[s]), s))
        ):
            group = groups[step]
            by_meaning: dict[str, list[AmountObservation]] = defaultdict(list)
            for o in group:
                by_meaning[o.meaning].append(o)
            if any(len(v) != 1 for v in by_meaning.values()):
                issues.append("gjentatt_belopsrolle")
            values = {k: v[0].amount_kr if len(v) == 1 else None for k, v in by_meaning.items()}
            if "nivaa" in values and index == 0 and group[0].round == "opprinnelig":
                balance = values["nivaa"]
            elif "endring" not in values:
                issues.append("mangler_delta")
                balance = None
            else:
                before, delta, after = (
                    values.get(k) for k in ("for_belop", "endring", "etter_belop")
                )
                if before is not None and balance is not None and before != balance:
                    issues.append("kjedekonflikt")
                if (
                    before is not None
                    and delta is not None
                    and after is not None
                    and before + delta != after
                ):
                    issues.append("lokal_konflikt")
                balance = balance + delta if balance is not None and delta is not None else None
                if after is not None and balance is not None and after != balance:
                    issues.append("etter_konflikt")
        result[account] = tuple(dict.fromkeys(issues))
    return result


def _sums(
    rows: list[SessionRow], global_issues: list[str], *, filtered: bool
) -> tuple[SessionSum, ...]:
    groups: dict[tuple[Any, ...], list[SessionRow]] = defaultdict(list)
    for row in rows:
        o = row.observation
        if o.information_type == "bevilgning":
            groups[
                (o.budget_year, o.meaning, o.detail_level, o.budget_side, o.currency, o.multiplier)
            ].append(row)
    result: list[SessionSum] = []
    for key, values in sorted(groups.items(), key=lambda item: str(item[0])):
        issues = list(global_issues)
        if filtered:
            issues.append("filtrert_delsum")
        included: list[SessionRow] = []
        for row in values:
            o = row.observation
            problems = list(row.issues)
            if row.selection_status != "treff":
                problems.append("uavklart_treff")
            if (
                o.budget_year is None
                or o.chapter is None
                or o.post is None
                or o.detail_level not in {"post", "underpost"}
            ):
                problems.append("uavklart_konto_eller_ar")
            if (
                o.budget_side not in {"utgift", "inntekt"}
                or o.currency != "NOK"
                or not o.multiplier
            ):
                problems.append("uforenlig_enhet_eller_side")
            if row.approved_amount_kr is None:
                problems.append("ikke_godkjent_analysebelop")
            if problems:
                issues.extend(problems)
            else:
                included.append(row)
        # Flere kildeobservasjoner av samme nivå er alternativer, aldri en additiv sum.
        if key[1] != "endring" and len({_account(r.observation) for r in values}) != len(values):
            issues.append("flere_nivaa_per_konto")
            included = []
        subtotal = (
            sum(r.approved_amount_kr for r in included if r.approved_amount_kr is not None)
            if included
            else None
        )
        result.append(
            SessionSum(
                key[0],
                key[1],
                key[2],
                key[3],
                key[4],
                key[5],
                subtotal,
                subtotal if not issues else None,
                tuple(r.observation.id for r in included),
                tuple(r.observation.id for r in values if r not in included),
                tuple(dict.fromkeys(issues)),
            )
        )
    return tuple(result)


def build_session_report(database: Path, selection: SessionSelection) -> SessionReport:
    """Les bare valgte lagrede resultater; avvis et grunnlag som endres under lesing."""
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as guard:
        version = guard.execute("PRAGMA data_version").fetchone()[0]
        result = _build(database, selection)
        if guard.execute("PRAGMA data_version").fetchone()[0] != version:
            raise ValueError("Grunnlaget endret seg under sammenstilling; kjør eksport på nytt")
    return result


def _build(database: Path, selection: SessionSelection) -> SessionReport:
    snapshot = read_inventory(
        database, selection.inventory_job_ids + selection.supplemental_inventory_job_ids
    )
    main = set(selection.inventory_job_ids)
    for job in snapshot.jobs:
        if job.dataset != selection.dataset:
            raise ValueError("Datasett kan ikke blandes")
        if (job.job_id in main) != (job.session == selection.session):
            raise ValueError(
                "Hovedinventar må gjelde valgt sesjon; supplement må gjelde en annen sesjon"
            )
    chosen_revisions = {r for c in snapshot.contexts for r in c.selected_revision_ids}
    extractions = tuple(read_extraction(database, i) for i in selection.extraction_ids)
    by_revision: dict[str, Extraction] = {}
    for extraction in extractions:
        if (
            extraction.dataset != selection.dataset
            or extraction.source_system != "storting"
            or extraction.source_revision_id not in chosen_revisions
        ):
            raise ValueError("Uttrekket må høre til uttrykkelig valgt sesjonsinventar og datasett")
        if extraction.source_revision_id in by_revision:
            raise ValueError("Velg én tolkning per vedtaksrevisjon")
        by_revision[extraction.source_revision_id] = extraction
    controlled = tuple(read_controlled(database, i) for i in selection.controlled_result_ids)
    decisions = {
        view.decision.id: view
        for view in read_decisions(
            database,
            tuple(
                sorted(
                    {r.decision_id for result in controlled for r in result.rows if r.decision_id}
                )
            ),
        )
    }
    controls: dict[str, list[tuple[ControlledResult, ControlledRow]]] = defaultdict(list)
    selected_observations = {o.id for e in extractions for o in e.observations}
    for controlled_result in controlled:
        if not set(controlled_result.extraction_ids) <= set(selection.extraction_ids):
            raise ValueError("Kontrollresultatet inneholder uttrekk utenfor sesjonsutvalget")
        if set(controlled_result.input_observation_ids) != {
            r.observation_id for r in controlled_result.rows
        } or len(controlled_result.rows) != len(set(controlled_result.input_observation_ids)):
            raise ValueError("Kontrollresultatets observasjonsdekning stemmer ikke")
        if not set(controlled_result.input_observation_ids) <= selected_observations:
            raise ValueError("Kontrollresultatet har observasjoner utenfor valgte uttrekk")
        for row in controlled_result.rows:
            controls[row.observation_id].append((controlled_result, row))
    histories = tuple(read_history(database, i) for i in selection.history_calculation_ids)
    if any(
        h.selection.dataset != selection.dataset
        or not set(h.selection.extraction_ids) <= set(selection.extraction_ids)
        for h in histories
    ):
        raise ValueError("Historikkberegningen må bruke valgte uttrekk og datasett")
    inventory: list[InventoryRow] = []
    rows: list[SessionRow] = []
    global_issues: list[str] = []
    global_issues.extend(
        f"kontrollresultat_{r.freshness}:{r.id}" for r in controlled if r.freshness != "gjeldende"
    )
    for c in snapshot.contexts:
        revisions = c.selected_revision_ids or (c.current_revision_id,)
        for revision_id in revisions:
            revision = read_revision(database, revision_id)
            d = revision.report.decision
            if d is None:
                raise ValueError("Inventarets vedtak mangler bevart identitet")
            e = by_revision.get(revision_id)
            problems: list[str] = []
            if not c.selected_job_ids:
                problems.append("kjent_id_utenfor_valgt_inventar")
            if c.missing_job_ids:
                problems.append("mangler_i_valgt_inventar")
            if len(c.selected_revision_ids) > 1:
                problems.append("flere_valgte_revisjoner")
            if revision_id != c.current_revision_id:
                problems.append("historisk_kilderevisjon")
            if c.observation_status != "observert":
                problems.append(c.observation_status)
            if c.latest_attempt_id not in {j.job_id for j in snapshot.jobs}:
                problems.append("nyere_kildeforsok")
            problems.extend(c.latest_attempt_errors)
            local_rows: list[SessionRow] = []
            if e:
                for o in e.observations:
                    selected_controls = controls.get(o.id, [])
                    controlled_row = (
                        selected_controls[0][1] if len(selected_controls) == 1 else None
                    )
                    result = selected_controls[0][0] if len(selected_controls) == 1 else None
                    view = (
                        decisions[controlled_row.decision_id]
                        if controlled_row and controlled_row.decision_id
                        else None
                    )
                    freshness = result.freshness if result else "ikke_vurderbar"
                    if view and view.freshness != "gjeldende":
                        freshness = view.freshness
                    approved = bool(
                        controlled_row
                        and view
                        and result
                        and freshness == "gjeldende"
                        and controlled_row.status == "godkjent"
                        and "amount_kr" in controlled_row.approved_fields.split(",")
                        and controlled_row.approved_use in {"analysebelop", "kjedegrunnlag"}
                    )
                    row_issues = list(problems)
                    row_issues.extend(a.code for a in o.anomalies)
                    row_issues.extend(
                        a.code
                        for a in e.anomalies
                        if a.budget_year in (None, o.budget_year)
                        and a.chapter in (None, o.chapter)
                        and a.post in (None, o.post)
                    )
                    if not o.organization.fdep_nr:
                        row_issues.append("mangler_organisasjonsoppslag")
                    if not selected_controls:
                        row_issues.append("mangler_valgt_kontrollresultat")
                    elif len(selected_controls) > 1:
                        row_issues.append("flere_valgte_kontrollresultater")
                    if controlled_row:
                        if (
                            controlled_row.raw_value != o.raw_value
                            or controlled_row.raw_amount_kr != o.amount_kr
                            or controlled_row.extraction_id != e.id
                        ):
                            raise ValueError(
                                "Kontrollresultatets råbinding stemmer ikke med uttrekket"
                            )
                        if view and (
                            controlled_row.status != view.decision.status
                            or controlled_row.approved_fields != view.decision.approved_fields
                            or controlled_row.approved_use != view.decision.approved_use
                        ):
                            raise ValueError("Kontrollresultatets avgjørelse stemmer ikke")
                        expected_effective = (
                            view.decision.corrected_amount_kr
                            if view and view.decision.corrected_amount_kr is not None
                            else o.amount_kr
                        )
                        if approved and controlled_row.effective_amount_kr != expected_effective:
                            raise ValueError(
                                "Kontrollresultatets effektive verdi stemmer ikke med avgjørelsen"
                            )
                        row_issues.extend(controlled_row.remaining_anomalies)
                    if not approved:
                        row_issues.append("ikke_godkjent_analysebelop")
                    local_rows.append(
                        SessionRow(
                            o,
                            e.id,
                            _match(o, selection),
                            c.session != selection.session,
                            tuple(r.id for r, _ in selected_controls),
                            controlled_row,
                            controlled_row.effective_amount_kr if controlled_row else None,
                            view.decision.corrected_amount_kr if view else None,
                            controlled_row.effective_amount_kr
                            if controlled_row and approved and not problems
                            else None,
                            freshness,
                            tuple(dict.fromkeys(row_issues)),
                        )
                    )
                problems.extend(a.code for a in e.anomalies)
            else:
                problems.append("mangler_belopsuttrekk")
            if e and not e.observations:
                problems.append("ingen_belopsobservasjoner_tekst_til_kontroll")
            content = "bevart" if d.html else "mangler_tekst"
            structure = (
                "ikke_uttrukket"
                if e is None
                else "tekst_uten_belop"
                if not e.observations
                else "strukturert"
                if all(o.structure_status == "strukturert" for o in e.observations)
                and not any(a.code != "mangler_organisasjonsoppslag" for a in e.anomalies)
                else "til_kontroll"
            )
            inventory.append(
                InventoryRow(
                    c.session,
                    c.decision_id,
                    revision_id,
                    c.selected_job_ids,
                    c.session != selection.session,
                    d.api_type,
                    d.date,
                    d.title,
                    d.url,
                    revision.report.source_sha256,
                    (e.id,) if e else (),
                    content,
                    structure,
                    len(local_rows),
                    sum(r.selection_status == "treff" for r in local_rows),
                    sum(r.selection_status == "uavklart_treff" for r in local_rows),
                    sum(r.selection_status == "utenfor" for r in local_rows),
                    sum(r.approved_amount_kr is not None for r in local_rows),
                    c,
                    tuple(dict.fromkeys(problems)),
                )
            )
            rows.extend(local_rows)
    for j in snapshot.jobs:
        if j.status != "fullfort":
            global_issues.append(f"inventar_{j.status}:{j.job_id}")
        if j.scope != "full":
            global_issues.append(f"valgt_delinventar:{j.job_id}")
        if not j.entries:
            global_issues.append(f"tomt_inventar:{j.job_id}")
        global_issues.extend(j.errors)
    global_issues.extend(issue for r in inventory for issue in r.issues)

    def coverage(session: str) -> Coverage:
        items = [r for r in inventory if r.session == session]
        jobs = [j for j in snapshot.jobs if j.session == session]
        full = bool(items) and any(
            j.scope == "full" and j.status == "fullfort" and j.entries for j in jobs
        )
        full = full and all(
            r.context.latest_attempt_id
            in {j.job_id for j in jobs if j.scope == "full" and j.status == "fullfort"}
            and r.context.observation_status == "observert"
            and r.context.selected_job_ids
            and len(r.context.selected_revision_ids) == 1
            and not r.context.missing_job_ids
            for r in items
        )
        return Coverage(
            session,
            session != selection.session,
            len({r.decision_id for r in items}),
            len({r.decision_id for r in items if r.content_status == "bevart"}),
            len({r.decision_id for r in items if r.structure_status == "strukturert"}),
            sum(r.observation_count for r in items),
            sum(r.approved_count for r in items),
            bool(full and all(r.content_status == "bevart" for r in items)),
            bool(full and all(r.structure_status == "strukturert" for r in items)),
        )

    chain_issues = _chain_issues(rows)
    rows = [
        replace(
            r,
            issues=tuple(
                dict.fromkeys((*r.issues, *chain_issues.get(_account(r.observation), ())))
            ),
        )
        for r in rows
    ]
    rows.sort(
        key=lambda r: (
            r.observation.decision_date or "9999",
            r.observation.api_id or "",
            r.observation.pointer.locator,
            r.observation.meaning,
        )
    )
    # Alle rå-, kontroll- og kjedeavvik vurderes før et beløpsfilter kan skjule rader.
    unfiltered_rows = tuple(rows)
    global_issues.extend(issue for row in unfiltered_rows for issue in row.issues)
    rows = [r for r in unfiltered_rows if r.selection_status != "utenfor"]
    report = SessionReport(
        identity(
            "sesjonsrapport-v1",
            asdict(selection),
            asdict(snapshot),
            [(r.observation.id, r.approved_amount_kr, r.freshness) for r in rows],
        ),
        selection,
        snapshot.assessed_utc,
        snapshot,
        tuple(inventory),
        tuple(rows),
        coverage(selection.session),
        tuple(
            coverage(s) for s in sorted({j.session for j in snapshot.jobs} - {selection.session})
        ),
        _sums(
            rows,
            global_issues,
            filtered=any(
                (selection.budget_years, selection.fdep_nrs, selection.chapters, selection.posts)
            ),
        ),
        histories,
        controlled,
        tuple(dict.fromkeys(global_issues)),
        unfiltered_rows,
    )
    return replace(
        report,
        reconciliations=tuple(reconcile(report, check) for check in selection.reconciliations),
        source_checks=tuple(check_source(report, check) for check in selection.source_expectations),
        independent_control=audit_preserved_2024(Path(selection.preserved_2024_controls))
        if selection.preserved_2024_controls
        else None,
    )
