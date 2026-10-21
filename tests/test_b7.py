"""B7 prøves gjennom klokke, offentlig runner og lagret rapport/Excel."""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from drift import due_date, next_due


@pytest.mark.parametrize(
    ("instant", "due", "next_instant"),
    [
        ("2026-01-15T04:59:00+00:00", None, "2026-01-15T05:00:00+00:00"),
        ("2026-01-15T05:00:00+00:00", "2026-01-15", "2026-01-16T05:00:00+00:00"),
        ("2026-07-15T04:00:00+00:00", "2026-07-15", "2026-07-16T04:00:00+00:00"),
        ("2026-03-28T05:00:00+00:00", "2026-03-28", "2026-03-29T04:00:00+00:00"),
        ("2026-10-24T04:00:00+00:00", "2026-10-24", "2026-10-25T05:00:00+00:00"),
    ],
)
def test_oslo_calendar_schedules_six_through_both_dst_transitions(
    instant: str, due: str | None, next_instant: str
) -> None:
    now = datetime.fromisoformat(instant)
    assert due_date(now) == due
    assert next_due(now).astimezone(UTC).isoformat() == next_instant


def test_clock_requires_timezone() -> None:
    with pytest.raises(ValueError, match="tidssone"):
        due_date(datetime(2026, 1, 1))


def test_pre_http_attempt_blocks_old_control_and_stage_binding_survives_lost_ack(
    tmp_path: Path,
) -> None:
    from test_b2 import RAW, metadata, synchronize

    from innlesning import read_inventory, read_revision, read_sync, stage_sync
    from innlesning.source_attempts import (
        begin_source_attempt,
        fail_source_attempt,
        read_source_attempt,
    )

    db = tmp_path / "attempts.sqlite"
    job = synchronize(db)
    revision = read_sync(db, job).entries[0].revision_id
    attempt = begin_source_attempt(db, "prove", "2024-2025")
    assert read_revision(db, revision).observation_status == "siste forsøk ikke fullført"
    assert read_inventory(db, (job,)).contexts[0].latest_attempt_id == attempt
    fail_source_attempt(db, attempt, "transportfeil")
    failed_revision = read_revision(db, revision)
    failed_inventory = read_inventory(db, (job,)).contexts[0]
    assert failed_revision.latest_attempt_id == failed_inventory.latest_attempt_id == attempt
    assert (
        failed_revision.latest_attempt_status == failed_inventory.latest_attempt_status == "feilet"
    )
    assert failed_revision.latest_attempt_source_sha256 == ""
    assert failed_inventory.latest_attempt_source_sha256 == ""
    assert failed_revision.latest_attempt_errors == ["transportfeil"]
    assert failed_inventory.latest_attempt_errors == ("transportfeil",)
    assert failed_revision.observation_status == failed_inventory.observation_status
    assert read_source_attempt(db, attempt).source_sha256 is None
    second = begin_source_attempt(db, "prove", "2024-2025")
    staged = stage_sync(db, RAW, metadata(RAW), historical_sample=True, source_attempt_id=second)
    assert read_source_attempt(db, second).job_id == staged


def test_attempt_cannot_replace_an_already_preserved_http_response(tmp_path: Path) -> None:
    from test_b2 import RAW, metadata

    from innlesning import stage_sync
    from innlesning.source_attempts import (
        begin_source_attempt,
        read_source_attempt,
        save_attempt_response,
    )

    db = tmp_path / "response-identity.sqlite"
    attempt = begin_source_attempt(db, "prove", "2024-2025")
    save_attempt_response(db, attempt, RAW, metadata(RAW))
    changed = RAW.replace(b"10 478 000", b"10 479 000")
    with pytest.raises(ValueError, match="bevart"):
        stage_sync(
            db, changed, metadata(changed), historical_sample=True, source_attempt_id=attempt
        )
    assert read_source_attempt(db, attempt).job_id is None
    assert read_source_attempt(db, attempt).source_sha256 == metadata(RAW)["sha256"]


def test_frozen_report_survives_new_failed_http_and_exports_original_assessment(
    tmp_path: Path,
) -> None:
    from test_b2 import synchronize

    from analyse import SessionSelection, build_session_report, export_built_session_excel
    from analyse.session_serialization import report_from_json, report_to_json
    from innlesning.source_attempts import begin_source_attempt

    db = tmp_path / "freeze.sqlite"
    job = synchronize(db)
    report = build_session_report(db, SessionSelection("prove", "2024-2025", (job,)))
    raw = report_to_json(report)
    begin_source_attempt(db, "prove", "2024-2025")
    restored = report_from_json(raw)
    assert restored == report
    output = tmp_path / "frozen.xlsx"
    export_built_session_excel(db, restored, output)
    assert output.is_file()
    with pytest.raises(ValueError, match="eksisterende"):
        export_built_session_excel(db, restored, output)


def session_list(current: str = "2026-2027", future: bool = True) -> bytes:
    years = [2026, 2027] if future else [int(current[:4])]

    def node(name: str, year: int) -> str:
        return (
            f"<{name}><fra>{year}-10-01T00:00:00</fra><id>{year}-{year + 1}</id>"
            f"<til>{year + 1}-09-30T23:59:59</til></{name}>"
        )

    return (
        "<sesjoner_oversikt xmlns='http://data.stortinget.no'>"
        + node("innevaerende_sesjon", int(current[:4]))
        + "<sesjoner_liste>"
        + "".join(node("sesjon", y) for y in years)
        + "</sesjoner_liste></sesjoner_oversikt>"
    ).encode()


def test_official_session_list_ignores_future_id_and_keeps_started_old_sessions() -> None:
    from drift.sessions import select_sessions

    now = datetime(2027, 10, 21, 6, tzinfo=UTC)
    assert select_sessions(session_list(), now, "2026-2027") == ("2026-2027", "2027-2028")
    assert select_sessions(session_list(), datetime(2026, 10, 21, 6, tzinfo=UTC), "2026-2027") == (
        "2026-2027",
    )
    with pytest.raises(ValueError):
        select_sessions(b"<!DOCTYPE x><x/>", now, "2026-2027")


class FakeGitHub:
    def __init__(self) -> None:
        self.issues: dict[int, dict[str, object]] = {}
        self.lose_post_ack = False
        self.fail = False
        self.creates = 0

    def find(self, repository: str, marker: str) -> int | None:
        if self.fail:
            raise TimeoutError()
        return next((i for i, issue in self.issues.items() if marker in str(issue["body"])), None)

    def read_body(self, repository: str, number: int) -> str:
        return str(self.issues[number]["body"])

    def create(self, repository: str, title: str, body: str) -> int:
        self.creates += 1
        self.issues[self.creates] = {"title": title, "body": body, "state": "open"}
        if self.lose_post_ack:
            raise TimeoutError()
        return self.creates

    def update_body(self, repository: str, number: int, body: str) -> None:
        self.issues[number]["body"] = body


def test_github_ambiguous_post_reconciles_closed_issue_and_preserves_human_content(
    tmp_path: Path,
) -> None:
    from drift.config import Config
    from drift.notifications import deliver, marker
    from drift.store import enqueue, pending_notifications, start_day
    from innlesning.organization_register import REGISTER_SNAPSHOT

    db = tmp_path / "github.sqlite"
    config = Config("test", db, tmp_path / "reports", REGISTER_SNAPSHOT)
    job, _, _, _ = start_day(config, "2026-10-21")
    enqueue(db, job, config.repository, "same-key", "Kontroll", "første status")
    github = FakeGitHub()
    github.lose_post_ack = True
    assert deliver(db, github) == "venter"
    assert github.creates == 1
    github.issues[1]["body"] = "Menneskets tekst\n" + str(github.issues[1]["body"])
    github.issues[1]["state"] = "closed"
    github.lose_post_ack = False
    assert deliver(db, github) == "levert"
    assert github.creates == 1
    assert github.issues[1]["state"] == "closed"
    assert "Menneskets tekst" in str(github.issues[1]["body"])
    assert marker("same-key") in str(github.issues[1]["body"])
    assert not pending_notifications(db)


class FakeSource:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.fail = False

    def sessions(self, timeout: int) -> tuple[bytes, dict[str, object]]:
        import hashlib

        raw = session_list("2024-2025", False)
        return raw, {
            "url": "https://data.stortinget.no/eksport/sesjoner",
            "retrieved_utc": "2026-10-21T04:10:00+00:00",
            "status": 200,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        }

    def session(self, session: str, timeout: int) -> tuple[bytes, dict[str, object]]:
        from test_b2 import RAW, metadata

        self.calls.append(session)
        if self.fail:
            raise TimeoutError("token=must-never-be-recorded")
        return RAW, metadata(RAW)


def test_public_daily_pipeline_saved_source_v2_controls_frozen_excel_and_fake_github(
    tmp_path: Path,
) -> None:
    from drift import Config, read_daily, run_daily
    from innlesning.organization_register import REGISTER_SNAPSHOT

    config = Config(
        "daily",
        tmp_path / "daily.sqlite",
        tmp_path / "reports",
        REGISTER_SNAPSHOT,
        dataset="prove",
        first_session="2024-2025",
    )
    source, github = FakeSource(), FakeGitHub()
    first = run_daily(
        config, source=source, github=github, now=datetime(2026, 10, 21, 6, tzinfo=UTC)
    )
    assert first["outcome"] == "full"
    assert first["source_changes"] == {"ny": 1, "rettelse": 0, "uendret": 0, "mangler": 0}
    import json

    snapshot = json.loads(Path(first["run_report"]).read_text(encoding="utf-8"))
    assert snapshot["delivery"] == "venter" and first["delivery"] == "levert"
    assert read_daily(config.database, config.pipeline_id)[0]["result"] == first
    assert len(first["reports"]) == 1
    original_issue_count = github.creates
    assert Path(first["reports"][0]["excel"]).is_file()
    again = run_daily(
        config, source=source, github=github, now=datetime(2026, 10, 21, 20, tzinfo=UTC)
    )
    assert again == first and source.calls == ["2024-2025"]
    tomorrow = run_daily(
        config, source=source, github=github, now=datetime(2026, 10, 23, 6, tzinfo=UTC)
    )
    assert tomorrow["source_changes"]["uendret"] == 1
    assert github.creates == original_issue_count
    assert [day["status"] for day in read_daily(config.database, config.pipeline_id)] == [
        "fullfort",
        "uteblitt",
        "fullfort",
    ]


class SimulatedStop(BaseException):
    pass


@pytest.mark.parametrize(
    "event", ["source_staged", "report_frozen", "excel_published", "outbox_saved"]
)
def test_process_stop_replays_saved_job_report_and_publish_without_another_http(
    tmp_path: Path, event: str
) -> None:
    from drift import Config, run_daily
    from innlesning.organization_register import REGISTER_SNAPSHOT
    from innlesning.sync import list_sync_jobs

    config = Config(
        "crash",
        tmp_path / "crash.sqlite",
        tmp_path / "reports",
        REGISTER_SNAPSHOT,
        dataset="prove",
        first_session="2024-2025",
    )
    source = FakeSource()

    def stop(point: str) -> None:
        if point == event:
            raise SimulatedStop()

    with pytest.raises(SimulatedStop):
        run_daily(
            config,
            source=source,
            github=FakeGitHub(),
            checkpoint=stop,
            now=datetime(2026, 10, 21, 6, tzinfo=UTC),
        )
    replay = run_daily(
        config, source=source, github=FakeGitHub(), now=datetime(2026, 10, 21, 7, tzinfo=UTC)
    )
    assert replay["outcome"] == "full"
    assert source.calls == ["2024-2025"]
    assert len(list_sync_jobs(config.database, "prove")) == 1
    assert len(list(config.output_directory.glob("*.xlsx"))) == 1


def test_transport_failure_preserves_prior_report_but_blocks_current_coverage_without_secret(
    tmp_path: Path,
) -> None:
    import json

    from analyse.session_serialization import report_from_json
    from drift import Config, run_daily
    from drift.store import read_frozen_report
    from innlesning.organization_register import REGISTER_SNAPSHOT

    config = Config(
        "timeout",
        tmp_path / "timeout.sqlite",
        tmp_path / "reports",
        REGISTER_SNAPSHOT,
        dataset="prove",
        first_session="2024-2025",
    )
    source, github = FakeSource(), FakeGitHub()
    run_daily(config, source=source, github=github, now=datetime(2026, 10, 21, 6, tzinfo=UTC))
    source.fail = True
    failed = run_daily(
        config, source=source, github=github, now=datetime(2026, 10, 22, 6, tzinfo=UTC)
    )
    assert failed["outcome"] == "partial"
    assert failed["source_changes"] == {"ny": 0, "rettelse": 0, "uendret": 0, "mangler": 0}
    assert "must-never-be-recorded" not in json.dumps(failed) + json.dumps(github.issues)
    frozen = report_from_json(read_frozen_report(config.database, failed["reports"][0]["id"])[0])
    assert not frozen.coverage.source_complete
    assert all(r.approved_amount_kr is None for r in frozen.rows)


def test_ambiguous_post_is_never_recreated_on_a_later_day_without_marker(tmp_path: Path) -> None:
    from drift import Config
    from drift.notifications import deliver
    from drift.store import enqueue, start_day
    from innlesning.organization_register import REGISTER_SNAPSHOT

    config = Config("dedup", tmp_path / "dedup.sqlite", tmp_path / "reports", REGISTER_SNAPSHOT)
    first, _, _, _ = start_day(config, "2026-10-21")
    enqueue(config.database, first, config.repository, "key", "Avvik", "første")
    github = FakeGitHub()
    github.lose_post_ack = True
    assert deliver(config.database, github) == "venter"
    github.issues.clear()  # En utilgjengelig/ennå usynlig marker gir ingen ny POST.
    second, _, _, _ = start_day(config, "2026-10-22")
    enqueue(config.database, second, config.repository, "key", "Avvik", "andre")
    github.lose_post_ack = False
    assert deliver(config.database, github) == "venter"
    assert github.creates == 1
