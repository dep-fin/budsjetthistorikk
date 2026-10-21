"""Egne pilot-CLI-er; eksisterende Storting-valg beholdes."""

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from test_historical_excel import workbook_bytes

from analyse.historical_pilot import run_pilot
from innlesning.historical_excel import (
    import_historical_workbook,
    read_historical_workbook,
    resume_historical_import,
    stage_historical_workbook,
)


def test_public_runner_rejects_source_named_summary_before_any_writes(tmp_path: Path) -> None:
    source = tmp_path / "summary.json"
    raw = workbook_bytes()
    source.write_bytes(raw)
    with pytest.raises(ValueError, match="[Kk]ollisjon"):
        run_pilot(Path(__file__).resolve().parent.parent, source, tmp_path)
    assert source.read_bytes() == raw
    assert not (tmp_path / "pilot.sqlite").exists()


@pytest.mark.parametrize("alias", ["direct", "hardlink"])
def test_public_runner_protects_control_reference_aliases(tmp_path: Path, alias: str) -> None:
    source = tmp_path / "source.xlsx"
    source.write_bytes(workbook_bytes())
    output = tmp_path / "out"
    output.mkdir()
    reference = output / "summary.json"
    reference.write_text("independent input", encoding="utf-8")
    if alias == "hardlink":
        linked = tmp_path / "reference.json"
        try:
            linked.hardlink_to(reference)
        except OSError as error:
            pytest.skip(f"Hardlink er utilgjengelig på verten: {error}")
        reference = linked
    with pytest.raises(ValueError, match="[Kk]ollisjon"):
        run_pilot(Path(__file__).resolve().parent.parent, source, output, proposal_refs=reference)
    assert reference.read_text(encoding="utf-8") == "independent input"
    assert not (output / "pilot.sqlite").exists()


def test_public_runner_preserves_unrelated_existing_summary(tmp_path: Path) -> None:
    source, output = tmp_path / "source.xlsx", tmp_path / "out"
    source.write_bytes(workbook_bytes())
    output.mkdir()
    summary = output / "summary.json"
    summary.write_bytes(b"unrelated document")
    with pytest.raises(ValueError, match="[Ss]ammendrag"):
        run_pilot(Path(__file__).resolve().parent.parent, source, output)
    assert summary.read_bytes() == b"unrelated document"
    assert not (output / "pilot.sqlite").exists()


def test_cli_offline_import_read_export_verify(tmp_path: Path) -> None:
    source, database, package = (
        tmp_path / "input.xlsx",
        tmp_path / "pilot.sqlite",
        tmp_path / "package",
    )
    source.write_bytes(workbook_bytes())
    imported = subprocess.run(
        [
            sys.executable,
            "-m",
            "innlesning.historical_excel",
            "import",
            "--database",
            str(database),
            "--source",
            str(source),
            "--year",
            "2024",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    extraction_id = json.loads(imported.stdout)["extraction_id"]
    source.unlink()
    read = subprocess.run(
        [
            sys.executable,
            "-m",
            "innlesning.historical_excel",
            "read",
            "--database",
            str(database),
            "--id",
            extraction_id,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(read.stdout)["counts"]["observations"] == 17
    for command in ["export", "verify"]:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "analyse.historical_package",
                command,
                "--database",
                str(database),
                "--id",
                extraction_id,
                "--package",
                str(package),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        assert json.loads(result.stdout)["verified"] is True


@pytest.mark.parametrize("table", ["amount_observations", "amount_extractions"])
def test_database_observation_corruption_is_rejected_at_read_boundary(
    tmp_path: Path, table: str
) -> None:
    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    source.write_bytes(workbook_bytes())
    imported = import_historical_workbook(database, source, budget_year=2024)
    # Bevisst lagringsfeil på utsiden av lesegrensen; original bevares.
    with sqlite3.connect(database) as connection:
        rowid, content = connection.execute(
            f"SELECT rowid,content_json FROM {table} LIMIT 1"
        ).fetchone()
        data = json.loads(content)
        if table == "amount_observations":
            data["amount_text"] = "tampered source"
        else:
            data["observations"][0]["amount_text"] = "tampered source"
        connection.execute(
            f"UPDATE {table} SET content_json=? WHERE rowid=?", (json.dumps(data), rowid)
        )
    with pytest.raises(ValueError):
        read_historical_workbook(database, imported.extraction_id)


def test_staged_corrupt_source_and_unknown_future_schema_are_rejected(tmp_path: Path) -> None:
    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    source.write_bytes(workbook_bytes())
    attempt = stage_historical_workbook(database, source, budget_year=2024)
    with sqlite3.connect(database) as connection:
        connection.execute("UPDATE sources SET raw_response=?", (b"tampered",))
    result = resume_historical_import(database, attempt)
    assert result.status == "feilet"
    assert result.extraction_id is None
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA user_version=6")
    with pytest.raises(ValueError, match="Ukjent databaseskjema"):
        stage_historical_workbook(database, source, budget_year=2024)
