"""Daglig kilde → B2 → eksplisitt v2 → B5-lesing → frosset B6 → varig outbox."""

import hashlib
import re
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Protocol
from urllib.error import HTTPError

from analyse import SessionSelection, build_session_report, export_built_session_excel
from analyse.controlled import reprocess_controlled
from analyse.session import SessionReport
from analyse.session_excel import verify_built_session_excel
from analyse.session_serialization import report_from_json, report_to_json
from innlesning import (
    control_report,
    extract_revision,
    read_extraction,
    read_sync,
    resume_sync,
    stage_sync,
)
from innlesning.controls import read_activation
from innlesning.http import fetch_session
from innlesning.observations import Extraction, Interpretation, encode, identity
from innlesning.source_attempts import (
    begin_source_attempt,
    fail_source_attempt,
    read_source_attempt,
    save_attempt_response,
)
from innlesning.sync import list_sync_jobs

from .artifacts import publish_text
from .config import Config
from .locking import database_lock
from .notifications import GitHubClient, GitHubPort, deliver
from .schedule import due_date
from .sessions import SESSIONS_URL, fetch_sessions, select_sessions
from .store import (
    acknowledge_excel,
    enqueue,
    enqueue_many,
    finish_day,
    freeze_report,
    notification_count,
    pending_notifications,
    read_frozen_report,
    save_state,
    start_day,
    update_delivery,
)


class SourcePort(Protocol):
    def sessions(self, timeout: int) -> tuple[bytes, dict[str, object]]: ...
    def session(self, session: str, timeout: int) -> tuple[bytes, dict[str, object]]: ...


class OfficialSource:
    def sessions(self, timeout: int) -> tuple[bytes, dict[str, object]]:
        return fetch_sessions(timeout=timeout)

    def session(self, session: str, timeout: int) -> tuple[bytes, dict[str, object]]:
        return fetch_session(session, timeout=timeout)


def _error(error: Exception) -> str:
    return (
        "httpfeil"
        if isinstance(error, HTTPError)
        else ("ugyldig_kilde" if isinstance(error, ValueError) else "transportfeil")
    )


def _emit(checkpoint: Callable[[str], None] | None, event: str) -> None:
    if checkpoint:
        checkpoint(event)


def _notification(
    config: Config,
    job: str,
    day: str,
    session: str,
    category: str,
    *,
    decision: str = "",
    locator: str = "",
    field: str = "",
    report_id: str = "",
) -> None:
    key, title, body = _notice(
        config,
        day,
        session,
        category,
        decision=decision,
        locator=locator,
        field=field,
        report_id=report_id,
    )
    enqueue(config.database, job, config.repository, key, title, body)


def _notice(
    config: Config,
    day: str,
    session: str,
    category: str,
    *,
    decision: str = "",
    locator: str = "",
    field: str = "",
    report_id: str = "",
) -> tuple[str, str, str]:
    # Ingen dato, innholdshash, revisjons-/uttrekks-ID eller unntakstekst i nøkkelen.
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,100}", category):
        category = "kildekontekst"
    key = identity(
        "b7-anomaly-1", config.dataset, "storting", session, category, decision, locator, field
    )
    return (
        key,
        f"Budsjetthistorikk: {category} {session} {decision}".strip(),
        f"Siste vurdering: {day}.\nDatasett: {config.dataset}; sesjon: {session}.\n"
        f"Avviksklasse: {category}; vedtak: {decision or 'sesjonsinventar'}.\n"
        f"Lokator: {locator or 'ikke relevant'}; felt: {field or 'ikke relevant'}.\n"
        f"Rapport-ID: {report_id or 'ingen B6-rapport tilgjengelig'}.\n"
        "Kildetall og kontrollgrunnlag finnes i den lokale kjørerapporten/Excel. "
        "Dette er et kontrollbehov, ingen automatisk faglig avgjørelse. "
        "Lukkede issues åpnes ikke automatisk.",
    )


def _extract_and_control(
    config: Config, jobs: dict[str, str]
) -> tuple[list[Extraction], tuple[str, ...]]:
    extractions: list[Extraction] = []
    controlled: list[str] = []
    for job_id in jobs.values():
        report = read_sync(config.database, job_id)
        if report.status != "fullfort":
            continue
        for entry in report.entries:
            if entry.classification == "mangler":
                continue
            extraction = extract_revision(
                config.database,
                entry.revision_id,
                interpretation=Interpretation(
                    adapter_version="storting-belop-v2", register_snapshot=config.register_snapshot
                ),
            )
            extractions.append(extraction)
            # Bruk aldri et annet aktivt grunnlag som reserve for dagens tolkning.
            active = read_activation(config.database, extraction.id)
            if (
                config.control_basis
                and active
                and all(
                    active.get(k) == v
                    for k, v in {
                        "extraction_id": extraction.id,
                        "register_snapshot": config.register_snapshot,
                        "control_basis": config.control_basis,
                    }.items()
                )
            ):
                result = reprocess_controlled(
                    config.database,
                    (extraction.id,),
                    config.register_snapshot,
                    config.control_basis,
                )
                controlled.append(result.id)
    # B5-leseren utføres også uten aktivert grunnlag; dette godkjenner ingenting.
    control_report(config.database, tuple(e.id for e in extractions))
    return extractions, tuple(controlled)


def _report_notifications(config: Config, job: str, day: str, report: SessionReport) -> int:
    keys: set[tuple[str, str, str, str, str]] = set()
    for row in report.inventory:
        if row.context.observation_status != "observert":
            keys.add((row.session, "kildeinventar", row.decision_id, "", ""))
        if not row.extraction_ids:
            keys.add((row.session, "manglende_uttrekk", row.decision_id, "", ""))
        elif row.observation_count == 0:
            keys.add((row.session, "tekst_til_kontroll", row.decision_id, "", ""))
        for identifier in row.extraction_ids:
            extraction = read_extraction(config.database, identifier)
            for anomaly in extraction.anomalies:
                keys.add((row.session, anomaly.code, row.decision_id, "", ""))
    for amount_row in report.unfiltered_rows:
        observation = amount_row.observation
        source_session = next(
            i.session for i in report.inventory if amount_row.extraction_id in i.extraction_ids
        )
        decision = next(
            i.decision_id for i in report.inventory if amount_row.extraction_id in i.extraction_ids
        )
        for code in amount_row.issues:
            keys.add(
                (
                    source_session,
                    code,
                    decision,
                    observation.pointer.locator,
                    observation.pointer.amount_field,
                )
            )
    if not report.coverage.source_complete:
        keys.add((report.selection.session, "ufullstendig_kildeinventar", "", "", ""))
    enqueue_many(
        config.database,
        job,
        config.repository,
        [
            _notice(
                config,
                day,
                session,
                code,
                decision=decision,
                locator=locator,
                field=field,
                report_id=report.id,
            )
            for session, code, decision, locator, field in sorted(keys)
        ],
    )
    return len(keys)


def _publish(
    config: Config, identifiers: list[str], checkpoint: Callable[[str], None] | None
) -> list[dict[str, str]]:
    published: list[dict[str, str]] = []
    for identifier in identifiers:
        raw, path, digest = read_frozen_report(config.database, identifier)
        report = report_from_json(raw)
        if path.exists():
            verify_built_session_excel(path, report)
            if digest is not None and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError("Publisert Excel er endret; bruk et nytt rapportgrunnlag")
        else:
            export_built_session_excel(config.database, report, path)
        _emit(checkpoint, "excel_published")
        acknowledge_excel(config.database, identifier, path)
        published.append({"id": identifier, "excel": str(path)})
    return published


def _delivery(config: Config, github: GitHubPort | None) -> str:
    if not pending_notifications(config.database, limit=1):
        return "ingen_avvik"
    if github is None:
        try:
            github = GitHubClient(config.token_environment, timeout=config.timeout)
        except ValueError:
            return "venter"
    return deliver(config.database, github)


def run_daily(
    config: Config,
    *,
    source: SourcePort | None = None,
    github: GitHubPort | None = None,
    now: datetime | None = None,
    checkpoint: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Kjør én forfalt lokal dato. Avvik er data; prosessavbrudd kan gjenopptas.

    checkpoint er en valgfri livssyklushook for vertens observasjon/avbruddsprøve.
    Bare faste hendelsesnavn sendes, aldri råkilder eller autentisering.
    """
    now = now or datetime.now(UTC)
    day = due_date(now)
    if day is None:
        return {"outcome": "ikke_forfalt", "reports": [], "delivery": "ikke_forsokt"}
    source = source or OfficialSource()
    with database_lock(config.database):
        job, attempt, state, previous = start_day(config, day)
        if attempt is None:
            assert previous is not None
            if pending_notifications(config.database, limit=1):
                previous["delivery"] = _delivery(config, github)
                update_delivery(config.database, job, previous)
            return previous
        # Ingen HTTP før ALLE ventende B2-jobber i dette datasettet er gjenopptatt.
        for pending in list_sync_jobs(config.database, config.dataset, status="venter"):
            resume_sync(config.database, pending.job_id)
        errors: list[str] = []
        if not state.get("sessions"):
            if state.get("catalog_attempt"):
                old = read_source_attempt(config.database, state["catalog_attempt"])
                if old.status == "venter":
                    fail_source_attempt(config.database, old.id, "avbrutt")
            catalog_attempt = begin_source_attempt(config.database, config.dataset, "sesjonsliste")
            state["catalog_attempt"] = catalog_attempt
            save_state(config.database, job, state)
            try:
                raw, metadata = source.sessions(config.timeout)
                if metadata.get("url") != SESSIONS_URL:
                    raise ValueError("Ugyldig sesjonsliste-URL")
                save_attempt_response(config.database, catalog_attempt, raw, metadata)
                state["sessions"] = list(select_sessions(raw, now, config.first_session))
                save_attempt_response(
                    config.database, catalog_attempt, raw, metadata, complete=True
                )
                save_state(config.database, job, state)
            except Exception as error:
                fail_source_attempt(config.database, catalog_attempt, _error(error))
                errors.append("sesjonsliste_feilet")
                _notification(config, job, day, "sesjonsliste", "kildehenting")
        catalog_sessions = set(state.get("sessions", ()))
        known_sessions = {
            j.session
            for j in list_sync_jobs(config.database, config.dataset)
            if j.session >= config.first_session
        }
        sessions = sorted(catalog_sessions | known_sessions)
        if catalog_sessions:
            for session in sorted(known_sessions - catalog_sessions):
                errors.append("sesjon_mangler_i_katalog:" + session)
                _notification(config, job, day, session, "sesjon_mangler_i_katalog")
        sources: dict[str, dict[str, str]] = state.setdefault("sources", {})
        jobs: dict[str, str] = {}
        observed_jobs: list[str] = []
        changed = False
        for session in sessions:
            step = sources.setdefault(session, {})
            job_id = step.get("job_id")
            old_attempt = (
                read_source_attempt(config.database, step["attempt_id"])
                if step.get("attempt_id")
                else None
            )
            if old_attempt and old_attempt.job_id:
                job_id = old_attempt.job_id
            if job_id and read_sync(config.database, job_id).status == "fullfort":
                jobs[session] = job_id
                observed_jobs.append(job_id)
                step["job_id"] = job_id
                continue
            if old_attempt and old_attempt.status == "venter" and old_attempt.job_id is None:
                fail_source_attempt(config.database, old_attempt.id, "avbrutt")
            identifier = begin_source_attempt(config.database, config.dataset, session)
            step["attempt_id"] = identifier
            step.pop("job_id", None)
            state.pop("frozen", None)
            save_state(config.database, job, state)
            changed = True
            try:
                raw, metadata = source.session(session, config.timeout)
                save_attempt_response(config.database, identifier, raw, metadata)
                job_id = stage_sync(
                    config.database,
                    raw,
                    metadata,
                    historical_sample=config.dataset == "prove",
                    source_attempt_id=identifier,
                )
                _emit(checkpoint, "source_staged")
                step["job_id"] = job_id
                save_state(config.database, job, state)
                resume_sync(config.database, job_id)
                report = read_sync(config.database, job_id)
                if report.dataset != config.dataset or report.session != session:
                    raise ValueError("Kildesvar passer ikke driftsomfanget")
                if report.status != "fullfort":
                    errors.append("kildeinventar_feilet:" + session)
                    _notification(config, job, day, session, "kildeinventar")
                    prior = [
                        j
                        for j in list_sync_jobs(config.database, config.dataset, status="fullfort")
                        if j.session == session
                    ]
                    jobs[session] = prior[-1].job_id if prior else job_id
                else:
                    jobs[session] = job_id
                observed_jobs.append(job_id)
            except Exception as error:
                failed = read_source_attempt(config.database, identifier)
                if failed.job_id is None:
                    fail_source_attempt(config.database, identifier, _error(error))
                errors.append("kildehenting_feilet:" + session)
                _notification(config, job, day, session, "kildehenting")
                prior = [
                    j
                    for j in list_sync_jobs(config.database, config.dataset, status="fullfort")
                    if j.session == session
                ]
                if prior:
                    jobs[session] = prior[-1].job_id
        save_state(config.database, job, state)
        counts = {k: 0 for k in ("ny", "rettelse", "uendret", "mangler")}
        for identifier in observed_jobs:
            for key, count in read_sync(config.database, identifier).counts.items():
                counts[key] += count
        control_needs = 0
        reports: list[dict[str, str]] = []
        try:
            if jobs and (changed or not state.get("frozen")):
                extractions, controlled = _extract_and_control(config, jobs)
                state["frozen"] = []
                for session, identifier in jobs.items():
                    other = tuple(j for s, j in jobs.items() if s != session)
                    selection = SessionSelection(
                        config.dataset,
                        session,
                        (identifier,),
                        extraction_ids=tuple(e.id for e in extractions),
                        controlled_result_ids=controlled,
                        supplemental_inventory_job_ids=other,
                    )
                    session_report = build_session_report(config.database, selection)
                    path = config.output_directory / f"{day}_{session}_{session_report.id}.xlsx"
                    freeze_report(
                        config.database,
                        job,
                        session_report.id,
                        report_to_json(session_report),
                        path,
                    )
                    state["frozen"].append(session_report.id)
                    control_needs += _report_notifications(config, job, day, session_report)
                state["control_needs"] = control_needs
                save_state(config.database, job, state)
                _emit(checkpoint, "report_frozen")
            if state.get("frozen"):
                reports = _publish(config, state["frozen"], checkpoint)
                control_needs = state.get("control_needs", 0)
        except Exception:
            errors.append("rapport_feilet")
            _notification(config, job, day, "rapport", "eksportfeil")
        if not sessions:
            errors.append("ingen_kontrollerbare_sesjoner")
        result: dict[str, Any] = {
            "id": job,
            "attempt_id": attempt,
            "local_date": day,
            "assessed_utc": now.astimezone(UTC).isoformat(),
            "outcome": "partial" if errors and jobs else "failed" if errors else "full",
            "source_changes": counts,
            "control_needs": notification_count(config.database, job),
            "errors": errors,
            "delivery": "venter"
            if pending_notifications(config.database, limit=1)
            else "ingen_avvik",
            "reports": reports,
            "jobs": jobs,
            "source_attempt_ids": {
                s: entry["attempt_id"] for s, entry in sources.items() if entry.get("attempt_id")
            },
            "session_list_attempt_id": state.get("catalog_attempt"),
            "professional_complete": False,
        }
        run_path = config.output_directory / f"{day}_run_{attempt}.json"
        result["run_report"] = str(run_path)
        try:
            publish_text(config.database, run_path, encode(result))
        except Exception:
            result.pop("run_report")
            result["errors"].append("kjorerapport_fil_feilet")
            result["outcome"] = "partial" if jobs else "failed"
            _notification(config, job, day, "rapport", "kjorerapport_fil_feilet")
            result["control_needs"] = notification_count(config.database, job)
        _emit(checkpoint, "outbox_saved")
        result["delivery"] = _delivery(config, github)
        finish_day(config.database, job, attempt, result)
        return result
