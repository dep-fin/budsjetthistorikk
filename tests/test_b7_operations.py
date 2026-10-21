"""Offentlig drift: feil, prosesslås, schema-kompatibilitet og Windows-oppsett."""

import json
import sqlite3
import subprocess
import sys
from dataclasses import asdict
from datetime import UTC, date, datetime
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest
from test_b2 import RAW, metadata, synchronize
from test_b7 import FakeGitHub, FakeSource

from drift import Config, read_daily, run_daily
from drift.__main__ import main
from drift.store import pending_notifications, read_frozen_report
from drift.windows import task_xml
from innlesning import extract_revision, import_saved, read_report, read_sync
from innlesning.organization_register import REGISTER_SNAPSHOT
from innlesning.registers import seed_register


def configuration(tmp_path: Path, **kw: object) -> Config:
    return Config(
        "ops",
        tmp_path / "ops.sqlite",
        tmp_path / "reports",
        REGISTER_SNAPSHOT,
        dataset="prove",
        first_session="2024-2025",
        **kw,
    )


def test_before_six_does_not_fetch_or_create_a_database(tmp_path: Path) -> None:
    config = configuration(tmp_path)
    source = FakeSource()
    assert (
        run_daily(config, source=source, now=datetime(2026, 10, 21, 3, 59, tzinfo=UTC))["outcome"]
        == "ikke_forfalt"
    )
    assert not config.database.exists() and not source.calls


@pytest.mark.parametrize("fault", ["timeout", "http", "invalid_xml", "empty"])
def test_failures_are_distinct_from_no_new_decisions_and_empty_has_no_coverage(
    tmp_path: Path, fault: str
) -> None:
    from urllib.error import HTTPError

    from lxml import etree

    from analyse.session_serialization import report_from_json

    class BadSource(FakeSource):
        def session(self, session: str, timeout: int) -> tuple[bytes, dict[str, object]]:
            if fault == "timeout":
                raise TimeoutError("secret")
            if fault == "http":
                raise HTTPError("https://fixed.invalid", 503, "secret", {}, None)
            raw = b"<broken>"
            if fault == "empty":
                root = etree.fromstring(RAW)
                root.find("{http://data.stortinget.no}stortingsvedtak_liste").clear()
                raw = etree.tostring(root)
            return raw, metadata(raw)

    config = configuration(tmp_path)
    result = run_daily(
        config, source=BadSource(), github=FakeGitHub(), now=datetime(2026, 10, 21, 6, tzinfo=UTC)
    )
    assert result["source_changes"]["ny"] == 0
    assert result["control_needs"] > 0
    if fault != "empty":
        assert result["outcome"] in {"partial", "failed"}
    else:
        report = report_from_json(
            read_frozen_report(config.database, result["reports"][0]["id"])[0]
        )
        assert not report.coverage.source_complete and not report.coverage.professional_complete


def test_failed_session_list_is_a_fault_even_when_known_sessions_can_be_refreshed(
    tmp_path: Path,
) -> None:
    class NoCatalog(FakeSource):
        def sessions(self, timeout: int) -> tuple[bytes, dict[str, object]]:
            raise TimeoutError()

    config = configuration(tmp_path)
    synchronize(config.database)
    source = NoCatalog()
    result = run_daily(
        config, source=source, github=FakeGitHub(), now=datetime(2026, 10, 21, 6, tzinfo=UTC)
    )
    assert source.calls == ["2024-2025"]
    assert result["outcome"] == "partial" and "sesjonsliste_feilet" in result["errors"]


def test_github_failure_keeps_ingest_and_outbox_and_repeat_retries_only_delivery(
    tmp_path: Path,
) -> None:
    config = configuration(tmp_path)
    source, github = FakeSource(), FakeGitHub()
    github.fail = True
    failed_delivery = run_daily(
        config, source=source, github=github, now=datetime(2026, 10, 21, 6, tzinfo=UTC)
    )
    assert failed_delivery["outcome"] == "full" and failed_delivery["delivery"] == "venter"
    assert pending_notifications(config.database)
    github.fail = False
    recovered = run_daily(
        config, source=source, github=github, now=datetime(2026, 10, 21, 7, tzinfo=UTC)
    )
    assert recovered["delivery"] == "levert" and len(source.calls) == 1
    assert read_daily(config.database, config.pipeline_id)[0]["result"]["delivery"] == "levert"


@pytest.mark.parametrize("version", [0, 2, 3, 4])
def test_schema_five_is_additive_and_old_writers_do_not_downgrade(
    tmp_path: Path, version: int
) -> None:
    config = configuration(tmp_path)
    b1 = import_saved(config.database, RAW, metadata(RAW), "40033944", historical_sample=True)
    if version >= 2:
        job = synchronize(config.database)
        if version >= 3:
            extract_revision(
                config.database, read_sync(config.database, job).entries[0].revision_id
            )
        if version >= 4:
            seed_register(config.database)
    before = asdict(read_report(config.database, b1))
    with sqlite3.connect(config.database) as db:
        assert db.execute("PRAGMA user_version").fetchone()[0] == version
    result = run_daily(
        config, source=FakeSource(), github=FakeGitHub(), now=datetime(2026, 10, 21, 6, tzinfo=UTC)
    )
    assert result["outcome"] == "full"
    synchronize(config.database)
    seed_register(config.database)
    import_saved(config.database, RAW, metadata(RAW), "40033944", historical_sample=True)
    with sqlite3.connect(config.database) as db:
        assert db.execute("PRAGMA user_version").fetchone()[0] == 5
    assert asdict(read_report(config.database, b1)) == before


def test_future_schema_is_rejected_before_fetch(tmp_path: Path) -> None:
    config = configuration(tmp_path)
    with sqlite3.connect(config.database) as db:
        db.execute("PRAGMA user_version=6")
    source = FakeSource()
    with pytest.raises(ValueError, match="Ukjent databaseskjema"):
        run_daily(config, source=source, now=datetime(2026, 10, 21, 6, tzinfo=UTC))
    assert not source.calls


def test_symbolic_database_path_uses_same_os_lock_as_canonical_file(tmp_path: Path) -> None:
    from drift.locking import AlreadyRunning, database_lock

    canonical = tmp_path / "canonical.sqlite"
    canonical.touch()
    alias = tmp_path / "alias.sqlite"
    try:
        alias.symlink_to(canonical)
    except OSError:
        pytest.skip("Windows-kontoen har ikke rett til å opprette symbolske lenker")
    with database_lock(canonical), pytest.raises(AlreadyRunning), database_lock(alias):
        pass


def test_os_process_lock_rejects_overlap_and_process_termination_releases_it(
    tmp_path: Path,
) -> None:
    config = configuration(tmp_path)
    script = (
        "from drift.locking import database_lock\nfrom pathlib import Path\n"
        "import sys,time\nwith database_lock(Path(sys.argv[1])):\n"
        " print('locked',flush=True)\n time.sleep(60)\n"
    )
    child = subprocess.Popen(
        [sys.executable, "-c", script, str(config.database)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        assert child.stdout.readline().strip() == "locked"
        from drift.locking import AlreadyRunning

        with pytest.raises(AlreadyRunning):
            run_daily(config, source=FakeSource(), now=datetime(2026, 10, 21, 6, tzinfo=UTC))
    finally:
        child.terminate()
        child.communicate(timeout=10)
    assert (
        run_daily(
            config,
            source=FakeSource(),
            github=FakeGitHub(),
            now=datetime(2026, 10, 21, 6, tzinfo=UTC),
        )["outcome"]
        == "full"
    )


def test_windows_adapter_has_local_six_recovery_and_account_without_registration(
    tmp_path: Path,
) -> None:
    raw = task_xml(
        tmp_path / "config.json",
        tmp_path / "python.exe",
        tmp_path,
        "DOMAIN\\existing-account",
        date(2026, 10, 21),
    )
    root = ET.fromstring(raw)
    ns = {"t": "http://schemas.microsoft.com/windows/2004/02/mit/task"}
    assert (
        root.findtext("t:Triggers/t:CalendarTrigger/t:StartBoundary", namespaces=ns)
        == "2026-10-21T06:00:00"
    )
    assert root.findtext("t:Settings/t:StartWhenAvailable", namespaces=ns) == "true"
    assert root.findtext("t:Settings/t:MultipleInstancesPolicy", namespaces=ns) == "IgnoreNew"
    assert (
        root.findtext("t:Principals/t:Principal/t:UserId", namespaces=ns)
        == "DOMAIN\\existing-account"
    )
    assert "Password" in raw and "registered" not in raw


def test_cli_status_next_due_config_guard_and_task_xml_are_read_only(
    tmp_path: Path, capsys
) -> None:
    config = configuration(tmp_path)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(asdict(config), default=str), encoding="utf-8")
    assert main(["--config", str(path), "--next-due"]) == 0
    assert "next_due" in capsys.readouterr().out
    assert not config.database.exists()
    assert (
        main(
            [
                "--config",
                str(path),
                "--task-xml",
                str(tmp_path / "task.xml"),
                "--python",
                sys.executable,
                "--working-directory",
                str(tmp_path),
                "--account",
                "DOMAIN\\existing-account",
                "--start-date",
                "2026-10-21",
            ]
        )
        == 0
    )
    assert not config.database.exists() and (tmp_path / "task.xml").exists()
    assert not (tmp_path / "task.xml").read_text().count("token")
    with pytest.raises(ValueError):
        Config(
            "bad",
            config.database,
            config.output_directory,
            REGISTER_SNAPSHOT,
            repository="someone/else",
        )
