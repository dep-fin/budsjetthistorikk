import json
import subprocess
import sys
from pathlib import Path

from innlesning import read_sync


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


def test_sync_cli_can_stage_resume_report_and_export_an_explicit_revision(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    database = tmp_path / "b2.sqlite"
    source_file = tmp_path / "response.xml"
    metadata_file = tmp_path / "metadata.json"
    source_file.write_bytes((root / "tests/fixtures/40033944.derived.xml").read_bytes())
    metadata_file.write_bytes((root / "tests/fixtures/40033944.metadata.json").read_bytes())

    def command(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", *arguments],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )

    staged = command(
        "innlesning",
        "synkroniser",
        "--database",
        str(database),
        "--sesjon",
        "2024-2025",
        "--historisk-proeve",
        "--vedtak-id",
        "40033944",
        "--forbered",
        "--response",
        str(source_file),
        "--metadata",
        str(metadata_file),
    )
    assert staged.returncode == 0, staged.stderr + staged.stdout
    job_id = json.loads(staged.stdout)["kjoring"]
    assert read_sync(database, job_id).status == "venter"
    source_file.unlink()
    metadata_file.unlink()
    resumed = command("innlesning", "gjenoppta", "--database", str(database), "--kjoring", job_id)
    assert resumed.returncode == 0, resumed.stderr + resumed.stdout
    summary = json.loads(resumed.stdout)
    assert summary["antall"]["ny"] == 1
    assert summary["omfang"] == "valgt"
    report = command("innlesning", "rapport", "--database", str(database), "--kjoring", job_id)
    assert json.loads(report.stdout) == summary
    revision_id = summary["vedtak"][0]["revision_id"]
    output = tmp_path / "b2.xlsx"
    exported = command(
        "analyse", "--database", str(database), "--revisjon", revision_id, "--excel", str(output)
    )
    assert exported.returncode == 0, exported.stderr + exported.stdout
    assert output.is_file()
