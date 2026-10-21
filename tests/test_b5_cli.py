"""En saksbehandler kan fullføre B5 uten å endre Python-kode."""

import json
from dataclasses import asdict
from pathlib import Path

import pytest
from test_b4 import ingest
from test_b5_controls import prepared
from test_b5_register import edit_rows

from analyse import HistorySelection
from analyse.controlled import export_controlled_excel, read_controlled, reprocess_controlled
from innlesning.maintenance import main


def test_cli_complete_register_and_control_roundtrip(tmp_path: Path, capsys) -> None:
    database = tmp_path / "cli.sqlite"
    original = ingest(database, "40036289")

    def run(*arguments: str):
        result = main(["--database", str(database), *arguments])
        output = capsys.readouterr()
        assert result == 0, output.err or output.out
        return json.loads(output.out)

    seed = run("register-seed")["snapshot_id"]
    register_file = tmp_path / "register.csv"
    run("register-export", "--snapshot", seed, "--output", str(register_file))
    imported = run("register-import", "--input", str(register_file))
    assert imported["reused_ids"] == [seed]
    assert run("import-read", "--id", imported["id"])["snapshot_id"] == seed
    assert len(run("register-read", "--snapshot", seed)["departments"]) == 17
    extraction_id = run(
        "reinterpret", "--revision", original.source_revision_id, "--register", seed
    )["extraction_id"]
    basis = run("basis-define", "--description", "Avgrenset kontroll")["control_basis"]
    common = ("--extraction", extraction_id, "--register", seed, "--control", basis)
    assert run("basis-activate", *common)["activation_generations"] == [1]
    path = tmp_path / "kontroll.xlsx"
    run("control-export", *common, "--output", str(path))

    def reject(rows):
        for row in rows:
            row.update(
                status="avvist",
                begrunnelse="Skal ikke brukes i analyse",
                kontrollor="Testkontrollør",
            )

    edit_rows(path, reject)
    imported_control = run("control-import", "--input", str(path))
    assert imported_control["new_ids"]
    assert run("control-read", "--id", imported_control["new_ids"][0])["freshness"] == "gjeldende"
    report = run("control-report", "--extraction", extraction_id)
    assert all(row["decision"]["decision"]["status"] == "avvist" for row in report)
    excel = tmp_path / "result.xlsx"
    result = run("reprocess", *common, "--output", str(excel))
    assert excel.is_file() and all(r["effective_amount_kr"] is None for r in result["rows"])
    assert run("controlled-read", "--id", result["id"])["id"] == result["id"]
    run("controlled-export", "--id", result["id"], "--output", str(tmp_path / "again.xlsx"))


def test_cli_invalid_import_has_nonzero_exit_and_durable_diagnostics(
    tmp_path: Path, capsys
) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("wrong;header\n", encoding="utf-8")
    database = tmp_path / "bad.sqlite"
    assert main(["--database", str(database), "register-import", "--input", str(path)]) == 1
    failure = json.loads(capsys.readouterr().out)
    assert failure["id"] and failure["errors"][0]["field"] == "fil"
    assert main(["--database", str(database), "import-read", "--id", failure["id"]]) == 1


def test_cli_reprocess_protects_normalized_selection_path_and_previous_result(
    tmp_path: Path, capsys
) -> None:
    database = tmp_path / "selection.sqlite"
    extraction, register, basis = prepared(database)
    selection = HistorySelection("prove", (extraction.id,), 2026, "5538", "70")
    previous = reprocess_controlled(
        database, (extraction.id,), register.id, basis, selection=selection
    )
    previous_path = tmp_path / "previous.xlsx"
    export_controlled_excel(database, previous.id, previous_path)
    previous_bytes = previous_path.read_bytes()
    selection_path = tmp_path / "selection.json"
    selection_path.write_text(json.dumps(asdict(selection)), encoding="utf-8")
    raw_selection = selection_path.read_bytes()
    common = [
        "--database",
        str(database),
        "reprocess",
        "--extraction",
        extraction.id,
        "--register",
        register.id,
        "--control",
        basis,
        "--selection",
        str(selection_path),
    ]
    alias = tmp_path / "unused" / ".." / selection_path.name
    assert main([*common, "--output", str(alias)]) == 2
    assert "forskjellige baner" in capsys.readouterr().err
    assert selection_path.read_bytes() == raw_selection
    assert previous_path.read_bytes() == previous_bytes
    assert read_controlled(database, previous.id) == previous

    distinct = tmp_path / "distinct.xlsx"
    assert main([*common, "--output", str(distinct)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["id"] == previous.id and distinct.read_bytes().startswith(b"PK")
    assert selection_path.read_bytes() == raw_selection


@pytest.mark.parametrize("command", ["reprocess", "controlled-export"])
def test_cli_controlled_excel_rejects_other_output_formats_before_replacing(
    tmp_path: Path, capsys, command: str
) -> None:
    database = tmp_path / "format.sqlite"
    extraction, register, basis = prepared(database)
    previous = reprocess_controlled(database, (extraction.id,), register.id, basis)
    path = tmp_path / "previous.json"
    path.write_bytes(b"previous result")
    arguments = (
        ["--id", previous.id]
        if command == "controlled-export"
        else ["--extraction", extraction.id, "--register", register.id, "--control", basis]
    )
    assert main(["--database", str(database), command, *arguments, "--output", str(path)]) == 2
    assert ".xlsx" in capsys.readouterr().err
    assert path.read_bytes() == b"previous result"
    assert read_controlled(database, previous.id) == previous
