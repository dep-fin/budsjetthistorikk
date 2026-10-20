"""Offline brukerflyt med uttrykkelig revisjon/tolkning og beregningsutvalg."""

import json
import os
import subprocess
import sys
from pathlib import Path

from innlesning import read_sync, sync_saved

FIXTURES = Path(__file__).parent / "fixtures" / "b3"


def cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
    )


def test_offline_cli_can_select_interpretation_calculate_and_reexport(tmp_path: Path) -> None:
    database = tmp_path / "cli.sqlite"
    raw = (FIXTURES / "40032850.xml").read_bytes()
    metadata = json.loads((FIXTURES / "40032850.json").read_text(encoding="utf-8"))
    job = sync_saved(database, raw, metadata, historical_sample=True, decision_id="40032850")
    revision = read_sync(database, job).entries[0].revision_id
    result = cli(
        "innlesning",
        "tolk",
        "--database",
        str(database),
        "--revisjon",
        revision,
        "--tolkning",
        "storting-belop-v1",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    extraction_id = json.loads(result.stdout)["belopsuttrekk"]
    selection = tmp_path / "utvalg.json"
    selection.write_text(
        json.dumps(
            {
                "dataset": "prove",
                "extraction_ids": [extraction_id],
                "budget_year": 2024,
                "chapter": "2541",
                "post": "70",
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "historikk.xlsx"
    result = cli(
        "analyse", "--database", str(database), "--utvalg", str(selection), "--excel", str(output)
    )
    assert result.returncode == 0, result.stdout + result.stderr
    calculation_id = json.loads(result.stdout)["beregning"]
    result = cli(
        "analyse",
        "--database",
        str(database),
        "--beregning",
        calculation_id,
        "--excel",
        str(tmp_path / "igjen.xlsx"),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert output.is_file()
    before = selection.read_bytes()
    unsafe = cli(
        "analyse",
        "--database",
        str(database),
        "--utvalg",
        str(selection),
        "--excel",
        str(selection),
    )
    assert unsafe.returncode == 1
    assert selection.read_bytes() == before
