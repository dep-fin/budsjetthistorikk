"""Gammel, uendret T1/O2b må gjenleses med begge libxml2-linjeskiftregler."""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("newlines", ["preserved", "normalized"])
def test_authentic_archived_t1_keeps_all_fields_ids_and_originals(newlines):
    # Egen prosess per parserregel: ingen tidligere validert basis i lru-cachene.
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            r"""
import gzip, hashlib, json, sys
from pathlib import Path
from lxml import etree, html

original_fromstring = html.fromstring
def parser_input(value, *args, **kwargs):
    if sys.argv[1] == "normalized" and isinstance(value, str):
        value = value.replace("\r\n", "\n").replace("\r", "\n")
    return original_fromstring(value, *args, **kwargs)
html.fromstring = parser_input

from analyse.visningspilot import report_from_json, report_to_json

archive = Path("tests/fixtures/t2/authentic-t1.json.gz").read_bytes()
assert hashlib.sha256(archive).hexdigest() == (
    "629c3561cca6f0ab2a5644958c7ae6590dd70775d688f40e134bda449e8982a6"
)
raw = gzip.decompress(archive)
assert hashlib.sha256(raw).hexdigest() == (
    "99e871e0ab780cbb548e15699f3093621d0f25229e3fa06c29cfdb5552803f53"
)
saved = json.loads(raw)
read = report_from_json(raw.decode("utf8"))
assert json.loads(report_to_json(read)) == saved
assert len(read.basis.observations) == 18
assert read.basis.o2b_json == saved["report"]["basis"]["o2b_json"]
print(sys.argv[1], etree.LXML_VERSION, etree.LIBXML_VERSION, read.id)
""",
            newlines,
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_synthetic_marker_like_whitespace_keeps_source_text_in_saved_files(tmp_path):
    from test_b9 import source_report
    from test_omtale import synthetic_sources

    from analyse.omtale import build_report, export_pair, read_excel, read_json
    from innlesning.omtale import import_omtale

    # Syntetisk ny kildeversjon. Både rå og tegnreferert markørlik tekst bevares.
    whitespace = "\t" + " " * 4096 + "&#9;" + " " * 8 + "\r\n"
    root = synthetic_sources(
        tmp_path, "prop16s-ch2.html", "For å redusere", "For å redusere" + whitespace
    )
    _, base = source_report(tmp_path)
    report = build_report(base, import_omtale(root, Path("tests/fixtures")))
    frozen, excel = tmp_path / "synthetic-marker.json", tmp_path / "synthetic-marker.xlsx"
    export_pair(report, frozen, excel)
    assert read_json(frozen) == read_excel(excel) == report
    section = next(s for s in report.basis.sections if s.key == "P1")
    assert "For å redusere" + "\t" + " " * 4096 + "\t" + " " * 8 + "\r\n" in section.text
