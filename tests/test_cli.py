import json
import subprocess
import sys
from pathlib import Path


def test_analyst_can_import_a_saved_sample_and_export_it_again(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    database = tmp_path / "budget.sqlite"
    output = tmp_path / "budget.xlsx"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "innlesning",
            "hent",
            "--vedtak-id",
            "40033944",
            "--sesjon",
            "2024-2025",
            "--historisk-proeve",
            "--database",
            str(database),
            "--response",
            str(root / "tests/fixtures/40033944.derived.xml"),
            "--metadata",
            str(root / "tests/fixtures/40033944.metadata.json"),
            "--excel",
            str(output),
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr + completed.stdout
    summary = json.loads(completed.stdout)
    assert summary["status"] == "strukturert"
    assert summary["antall_postlinjer"] == 8
    assert output.is_file()
    second = tmp_path / "second.xlsx"
    export = subprocess.run(
        [
            sys.executable,
            "-m",
            "analyse",
            "--database",
            str(database),
            "--kjoring",
            summary["kjoring"],
            "--excel",
            str(second),
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert export.returncode == 0, export.stderr + export.stdout
    assert second.is_file()


def test_historical_sample_requires_an_explicit_flag(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "innlesning",
            "hent",
            "--vedtak-id",
            "40033944",
            "--sesjon",
            "2024-2025",
            "--database",
            str(tmp_path / "budget.sqlite"),
            "--response",
            str(root / "tests/fixtures/40033944.derived.xml"),
            "--metadata",
            str(root / "tests/fixtures/40033944.metadata.json"),
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 1
    assert "historisk-proeve" in json.loads(completed.stdout)["feil"]
    assert not (tmp_path / "budget.sqlite").exists()
