"""Frosne uavhengige kontroller og ny offisiell kilde uten historisk start."""

import json
from copy import deepcopy
from pathlib import Path

import pytest
from test_historical_excel import formula_range_workbook, mutate_member, workbook_bytes

from analyse.extraction_excel import export_extraction_excel
from analyse.historical_comparison import (
    VERSION,
    compare_historical_controls,
    freeze_historical_controls,
    historical_control_scope,
    read_historical_comparison,
)
from analyse.history import HistorySelection, calculate_history
from innlesning import read_sync, sync_saved
from innlesning.historical_excel import import_historical_workbook, read_historical_workbook
from innlesning.observations import Interpretation, extract_revision, read_extraction


def test_union_preserves_missing_zero_precision_and_hierarchy(tmp_path: Path) -> None:
    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    source.write_bytes(workbook_bytes())
    result = import_historical_workbook(database, source, budget_year=2024)
    assert result.extraction_id is not None
    specification = {
        "version": VERSION,
        "controls": [
            {
                "id": "independent_synthetic_reference",
                "tolerance": "0",
                "scope": {
                    "budget_year": 2024,
                    "figure_type": "stortingsvedtak",
                    "meaning": "nivaa",
                    "detail_level": "post",
                    "unit": "NOK",
                    "candidate_multiplier": "1000000",
                    "stage": "opprinnelig",
                    "period": "budsjettåret",
                    "budget_side": "begge",
                    "reference_basis": "observert_kildefelt",
                    "aggregation": "rå underpostceller prøves som separat kontrollaggregat",
                },
                "selector": {"sheet": "Rådata", "column": "H", "key_fields": ["chapter", "post"]},
                "sources": [{"sha256": "synthetic-reference", "kind": "synthetic_test"}],
                "references": [
                    {
                        "key": ["1", "1"],
                        "amount_kr": "14768000",
                        "pointers": ["synthetic-reference/1"],
                        "scope": {**historical_control_scope("H"), "candidate_multiplier": "1"},
                        "source_budget_year": 2024,
                    },
                    {
                        "key": ["99", "90"],
                        "amount_kr": "0",
                        "pointers": ["synthetic-reference/2"],
                        "scope": {**historical_control_scope("H"), "candidate_multiplier": "1"},
                        "source_budget_year": 2024,
                    },
                ],
            }
        ],
    }
    spec_id = freeze_historical_controls(database, result.extraction_id, specification)
    report = compare_historical_controls(database, spec_id)
    assert report["summary"] == {
        "independent_synthetic_reference": {
            "fractional_kr": 1,
            "missing_reference": 1,
            "missing_excel": 1,
        }
    }
    assert read_historical_comparison(database, report["id"]) == report
    assert compare_historical_controls(database, spec_id) == report
    missing = next(row for row in report["rows"] if row["key"] == ["99", "90"])
    assert missing["candidate_kr"] is None and missing["reference_kr"] == "0"
    specification["controls"][0]["selector"]["column"] = "N"
    with pytest.raises(ValueError):
        freeze_historical_controls(database, result.extraction_id, specification)


@pytest.mark.parametrize(
    "field,value",
    [
        ("budget_year", 2025),
        ("unit", "USD"),
        ("meaning", "endring"),
        ("figure_type", "regnskap"),
        ("stage", "rnb"),
        ("period", "regnskapsåret"),
        ("detail_level", "uavklart"),
        ("candidate_multiplier", "1"),
        ("budget_side", "ukjent"),
        ("unknown", "anything"),
    ],
)
def test_equal_numbers_cannot_match_an_incompatible_control_scope(
    tmp_path: Path, field: str, value: object
) -> None:
    from analyse.historical_pilot import _control

    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    source.write_bytes(workbook_bytes(amount="0"))
    result = import_historical_workbook(database, source, budget_year=2024)
    assert result.extraction_id is not None
    control = _control(
        "same_numeric_zero",
        "H",
        [{"key": ["1", "1"], "amount_kr": "0", "pointers": ["independent synthetic reference"]}],
        [{"kind": "synthetic"}],
    )
    control["selector"]["cells"] = ["H2"]
    good = {"version": VERSION, "controls": [control]}
    report = compare_historical_controls(
        database, freeze_historical_controls(database, result.extraction_id, good)
    )
    assert report["summary"]["same_numeric_zero"] == {"match": 1}
    bad = deepcopy(good)
    bad["controls"][0]["scope"][field] = value
    with pytest.raises(ValueError):
        freeze_historical_controls(database, result.extraction_id, bad)


def test_reference_source_year_is_checked_even_with_compatible_declared_scope(
    tmp_path: Path,
) -> None:
    from analyse.historical_pilot import _control

    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    source.write_bytes(workbook_bytes(amount="0"))
    result = import_historical_workbook(database, source, budget_year=2024)
    assert result.extraction_id is not None
    control = _control(
        "wrong_reference_year",
        "H",
        [
            {
                "key": ["1", "1"],
                "amount_kr": "0",
                "pointers": ["independent synthetic 2025 source"],
                "source_budget_year": 2025,
            }
        ],
        [{"kind": "synthetic"}],
    )
    with pytest.raises(ValueError, match="kildeår"):
        freeze_historical_controls(
            database, result.extraction_id, {"version": VERSION, "controls": [control]}
        )


def test_empty_shared_formula_never_matches_its_cached_value(tmp_path: Path) -> None:
    from analyse.historical_pilot import _control

    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    source.write_bytes(
        mutate_member(
            workbook_bytes(), "xl/worksheets/other.xml", b"<f>1+1</f>", b'<f t="shared" si="0"/>'
        )
    )
    result = import_historical_workbook(database, source, budget_year=2024)
    assert result.extraction_id is not None
    control = _control(
        "formula_cache",
        "H",
        [
            {
                "key": ["2", "1"],
                "amount_kr": "2000000",
                "pointers": ["independent synthetic reference"],
            }
        ],
        [{"kind": "synthetic"}],
    )
    control["selector"]["cells"] = ["H3"]
    report = compare_historical_controls(
        database,
        freeze_historical_controls(
            database, result.extraction_id, {"version": VERSION, "controls": [control]}
        ),
    )
    assert report["summary"]["formula_cache"] == {"unresolved": 1}


@pytest.mark.parametrize("formula_type", ["array", "shared", "dataTable"])
def test_covered_formula_cache_cannot_match_without_its_own_formula(
    tmp_path: Path, formula_type: str
) -> None:
    from analyse.historical_pilot import _control

    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    source.write_bytes(formula_range_workbook(formula_type))
    result = import_historical_workbook(database, source, budget_year=2024)
    assert result.extraction_id is not None
    control = _control(
        "covered_formula_cache",
        "H",
        [{"key": ["2", "1"], "amount_kr": "2000000", "pointers": ["synthetic reference"]}],
        [{"kind": "synthetic"}],
    )
    control["selector"]["cells"] = ["H3"]
    report = compare_historical_controls(
        database,
        freeze_historical_controls(
            database, result.extraction_id, {"version": VERSION, "controls": [control]}
        ),
    )
    assert report["summary"]["covered_formula_cache"] == {"unresolved": 1}


def test_component_difference_and_document_delta_keep_separate_bases(tmp_path: Path) -> None:
    from analyse.historical_pilot import _control

    source, database = tmp_path / "input.xlsx", tmp_path / "pilot.sqlite"
    raw = mutate_member(
        workbook_bytes(),
        "xl/worksheets/docs.xml",
        b'<c r="C2"><v>0</v></c>',
        b'<c r="C2"><v>1</v></c>',
    )
    source.write_bytes(raw)
    result = import_historical_workbook(database, source, budget_year=2024)
    assert result.extraction_id is not None
    control = _control(
        "separate_component",
        "D",
        [
            {
                "key": ["i2/23-24", "1", "1", "1"],
                "amount_kr": "-7",
                "pointers": ["synthetic before", "synthetic after"],
                "derived": True,
            }
        ],
        [{"kind": "synthetic"}],
        groups=["i2/23-24"],
        component=True,
    )
    spec = {"version": VERSION, "controls": [control]}
    report = compare_historical_controls(
        database, freeze_historical_controls(database, result.extraction_id, spec)
    )
    assert report["summary"]["separate_component"] == {"match": 1}
    bad = deepcopy(spec)
    bad["controls"][0]["references"][0]["scope"]["reference_basis"] = "observert_kildefelt"
    with pytest.raises(ValueError):
        freeze_historical_controls(database, result.extraction_id, bad)


@pytest.mark.parametrize("legacy", ["absent", "corrupt", "conflicting"])
def test_authentic_new_official_source_needs_no_legacy_start_or_register(
    tmp_path: Path,
    legacy: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    if legacy != "absent":
        (tmp_path / "legacy.xlsx").write_bytes(
            b"corrupt" if legacy == "corrupt" else workbook_bytes(amount="999999")
        )
    fixtures = Path(__file__).parent / "fixtures" / "b3"
    identifier = "40034443"
    database = tmp_path / "official.sqlite"
    raw = (fixtures / f"{identifier}.xml").read_bytes()
    metadata = json.loads((fixtures / f"{identifier}.json").read_text(encoding="utf-8"))
    job = sync_saved(database, raw, metadata, historical_sample=True, decision_id=identifier)
    revision = read_sync(database, job).entries[0].revision_id
    extraction = extract_revision(
        database, revision, interpretation=Interpretation(adapter_version="storting-belop-v2")
    )
    assert read_extraction(database, extraction.id) == extraction
    observed = next(
        o
        for o in extraction.observations
        if o.chapter == "1760" and o.post == "45" and o.meaning == "endring"
    )
    assert observed.amount_kr == -227_000_000
    assert observed.pointer.artifact_id == metadata["sha256"]
    assert observed.organization.mapped_department_code is None
    output = tmp_path / "official.xlsx"
    export_extraction_excel(database, extraction.id, output)
    calculation = calculate_history(
        database, HistorySelection("prove", (extraction.id,), 2025, "1760", "45")
    )
    assert calculation.approved_balance is None
    assert "manglende_start" in {a.code for a in calculation.anomalies}
    assert calculation.steps[0].delta == -227_000_000


def test_old_official_writer_preserves_pilot_tables_and_ids(tmp_path: Path) -> None:
    source, database = tmp_path / "input.xlsx", tmp_path / "combined.sqlite"
    source.write_bytes(workbook_bytes())
    imported = import_historical_workbook(database, source, budget_year=2024)
    original = read_historical_workbook(database, imported.extraction_id)
    fixture = Path(__file__).parent / "fixtures/b3/40033805.xml"
    metadata = json.loads(fixture.with_suffix(".json").read_text(encoding="utf-8"))
    job = sync_saved(
        database, fixture.read_bytes(), metadata, historical_sample=True, decision_id="40033805"
    )
    revision = read_sync(database, job).entries[0].revision_id
    extraction = extract_revision(database, revision)
    assert extraction.interpretation.adapter_version == "storting-belop-v1"
    assert read_historical_workbook(database, imported.extraction_id) == original
    assert read_extraction(database, extraction.id) == extraction
