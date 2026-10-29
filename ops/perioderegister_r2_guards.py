"""Konkrete syntetiske ZIP/XML-/ressursprøver mot en faktisk P2-bok."""

import argparse
import hashlib
import json
import warnings
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

from analyse.perioderegister_r2 import read_json, report_from_json
from analyse.perioderegister_r2_excel import read_excel


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    results = []
    for attack in (
        "duplicate-member",
        "traversal",
        "formula",
        "external-relationship",
        "root-relationship",
        "content-type",
        "raw-style",
        "huge-dimension",
        "member-limit",
        "doctype",
        "expanded-limit",
    ):
        target = output / (attack + ".xlsx")
        with ZipFile(args.source) as before, ZipFile(target, "w", ZIP_DEFLATED) as after:
            for entry in before.infolist():
                raw = before.read(entry.filename)
                if entry.filename == "xl/worksheets/sheet1.xml" and attack in {
                    "formula",
                    "huge-dimension",
                    "doctype",
                }:
                    tree = etree.fromstring(raw)
                    if attack == "formula":
                        cell = tree.find(".//" + ns + 'c[@r="G2"]')
                        etree.SubElement(cell, ns + "f").text = "1+1"
                    elif attack == "huge-dimension":
                        tree.find(ns + "dimension").set("ref", "A1:XFD1048576")
                    raw = etree.tostring(tree)
                    if attack == "doctype":
                        raw = b'<!DOCTYPE worksheet [<!ENTITY bomb "synthetic">]>' + raw
                if (
                    entry.filename == "xl/_rels/workbook.xml.rels"
                    and attack == "external-relationship"
                ):
                    tree = etree.fromstring(raw)
                    etree.SubElement(
                        tree,
                        "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship",
                        Id="synthetic-external",
                        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/externalLink",
                        Target="https://example.invalid/synthetic",
                        TargetMode="External",
                    )
                    raw = etree.tostring(tree)
                if entry.filename == "_rels/.rels" and attack == "root-relationship":
                    tree = etree.fromstring(raw)
                    tree[0].set("Target", "https://example.invalid/synthetic")
                    tree[0].set("TargetMode", "External")
                    raw = etree.tostring(tree)
                if entry.filename == "[Content_Types].xml" and attack == "content-type":
                    tree = etree.fromstring(raw)
                    tree[0].set("ContentType", "application/synthetic")
                    raw = etree.tostring(tree)
                if entry.filename == "xl/styles.xml" and attack == "raw-style":
                    tree = etree.fromstring(raw)
                    tree.find("{*}cellXfs")[0].set("applyAlignment", "0")
                    raw = etree.tostring(tree)
                after.writestr(entry, raw)
            if attack == "duplicate-member":
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    after.writestr(before.infolist()[0], before.read(before.infolist()[0].filename))
            elif attack == "traversal":
                after.writestr("../outside.txt", "synthetic")
            elif attack == "member-limit":
                for n in range(257):
                    after.writestr("synthetic/" + str(n), b"x")
            elif attack == "expanded-limit":
                after.writestr("synthetic-expanded.xml", b"x" * (129 * 1024 * 1024))
        try:
            read_excel(target)
        except ValueError as error:
            message = str(error)
        else:
            raise AssertionError(attack)
        results.append(
            {
                "synthetic": True,
                "attack": attack,
                "rejection": message,
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
        )
    for name, raw in (
        (
            "duplicate-json",
            '{"format":"perioderegister-r2-1","format":"perioderegister-r2-1","report":{}}',
        ),
        ("nan", '{"format":"perioderegister-r2-1","report":NaN}'),
    ):
        (output / (name + ".json")).write_text(raw, encoding="utf8")
        try:
            report_from_json(raw)
        except ValueError as error:
            results.append({"synthetic": True, "attack": name, "rejection": str(error)})
        else:
            raise AssertionError(name)
    large = output / "report-limit.json"
    with large.open("wb") as handle:
        handle.write(b"x" * (64 * 1024 * 1024 + 1))
    try:
        read_json(large)
    except ValueError as error:
        results.append({"synthetic": True, "attack": "report-limit", "rejection": str(error)})
    else:
        raise AssertionError("report-limit")
    (output / "guards.json").write_text(
        json.dumps(
            {"tests": results, "rejected": len(results), "errors": 0}, ensure_ascii=False, indent=2
        ),
        encoding="utf8",
    )
    print(json.dumps({"rejected": len(results), "errors": 0}))


if __name__ == "__main__":
    main()
