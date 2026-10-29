"""Målrettet temareproduksjon; offentlige lesere og faktiske eksportfiler."""

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--exports", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expect", choices=("accepted", "rejected"), required=True)
    args = parser.parse_args()
    root, exports, output = args.root.resolve(), args.exports.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    os.chdir(root)
    sys.path.insert(0, str(root))

    def git(*values):
        return subprocess.check_output(["git", "-C", str(root), *values], text=True).strip()

    candidate = git("rev-parse", "--verify", args.candidate + "^{commit}")
    base = git("rev-parse", "--verify", args.base + "^{commit}")
    from lxml import etree
    from openpyxl import load_workbook

    from analyse import proposisjon16 as t5
    from analyse.omtale_excel_guard import inspect_excel
    from analyse.proposisjon16_excel import SHEET_NAMES, export_excel, read_excel
    from analyse.visningspilot import report_from_json

    assert Path(t5.__file__).resolve().is_relative_to(root)

    def digest(path):
        raw = path.read_bytes()
        return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

    old = report_from_json(
        gzip.decompress((root / "tests/fixtures/t2/authentic-t1.json.gz").read_bytes()).decode()
    )
    positive = []
    for frozen in sorted(exports.glob("*.json")):
        excel = frozen.with_suffix(".xlsx")
        if not excel.is_file():
            continue
        report = t5.read_json(frozen)
        assert read_excel(excel) == report
        assert report.basis.t1_basis == old.basis
        positive.append({"name": excel.name, **digest(excel), "report_id": report.id})
    assert positive
    source = exports / "inntekt-null.xlsx"
    report = t5.read_json(source.with_suffix(".json"))
    # Ny eksport bruker uendret skriver og skal også bestå samme offentlige leser.
    fresh = output / "new-valid.xlsx"
    export_excel(report, fresh)
    assert read_excel(fresh) == report
    book = load_workbook(fresh)
    try:
        assert book["Forløp"]["G4"].value == 0
        assert book["Forløp"]["G4"].data_type == "n"
        affected = []
        for title, coordinate in (("Inventar", "M2"), ("Inventar", "N2"), ("Kontoer", "H2")):
            cell = book[title][coordinate]
            assert cell.font.color.type == "theme" and cell.font.color.theme == 1
            assert cell.fill.patternType is None
            affected.append({"sheet": title, "cell": coordinate, "value": cell.value})
    finally:
        book.close()

    with ZipFile(source) as archive:
        original = {name: archive.read(name) for name in archive.namelist()}
    with ZipFile(fresh) as archive:
        assert archive.read("xl/theme/theme1.xml") == original["xl/theme/theme1.xml"]
    raw = source.with_suffix(".json").read_text("utf8")
    drawing = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    negatives = []
    for mutation in ("srgb-white", "system-white", "minor-font"):
        parts = dict(original)
        theme = etree.fromstring(parts["xl/theme/theme1.xml"])
        if mutation == "minor-font":
            latin = theme.find(".//" + drawing + "minorFont/" + drawing + "latin")
            assert latin is not None
            latin.set("typeface", "Wingdings")
        else:
            dark = theme.find(".//" + drawing + "clrScheme/" + drawing + "dk1")
            assert dark is not None
            for child in list(dark):
                dark.remove(child)
            if mutation == "srgb-white":
                etree.SubElement(dark, drawing + "srgbClr", val="FFFFFF")
            else:
                etree.SubElement(dark, drawing + "sysClr", val="window", lastClr="FFFFFF")
        parts["xl/theme/theme1.xml"] = etree.tostring(theme)
        changed = [name for name in parts if parts[name] != original[name]]
        assert changed == ["xl/theme/theme1.xml"]
        damaged = output / (mutation + ".xlsx")
        with ZipFile(damaged, "w", ZIP_DEFLATED) as archive:
            for name, content in parts.items():
                archive.writestr(name, content)
        extracted, _ = inspect_excel(
            damaged,
            sheet_names=SHEET_NAMES,
            snapshot_name="Visningsgrunnlag",
            max_expanded_bytes=128 * 1024 * 1024,
        )
        assert extracted == raw and t5.report_from_json(extracted) == report
        try:
            assert read_excel(damaged) == report
        except ValueError as error:
            outcome, detail = "rejected", str(error)
            assert "T5-Excel" in detail and "tema" in detail
        else:
            outcome, detail = "accepted", "equal report"
        assert outcome == args.expect, (mutation, outcome, detail)
        negatives.append(
            {
                "mutation": mutation,
                "changed_parts": changed,
                "container_valid_capsule_unchanged": True,
                "outcome": outcome,
                "detail": detail,
                **digest(damaged),
            }
        )

    preservation = []
    baseline = root / "docs/research/proposisjon16-62/security-fix/preserved-before.json"
    if baseline.is_file():
        for entry in json.loads(baseline.read_text("utf8")):
            assert digest(root / entry["path"]) == {k: entry[k] for k in ("bytes", "sha256")}, (
                entry["path"]
            )
            preservation.append(entry["path"])
    bound = ["analyse/proposisjon16_excel.py", "tests/test_proposisjon16.py"]
    result = {
        "candidate": candidate,
        "candidate_tree": git("rev-parse", candidate + "^{tree}"),
        "base": base,
        "working_changes_from_candidate": git("diff", "--name-only", candidate).splitlines(),
        "reader_inputs": [{"path": name, **digest(root / name)} for name in bound],
        "existing_valid_exports": positive,
        "new_valid_export": digest(fresh),
        "numeric_zero_preserved": True,
        "new_export_theme_unchanged": True,
        "affected_cells": affected,
        "theme_probes": negatives,
        "preserved_paths": preservation,
    }
    (output / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", "utf8", newline="\n"
    )
    print(json.dumps({"positive": len(positive), "new_export": 1, "themes": negatives}))


if __name__ == "__main__":
    main()
