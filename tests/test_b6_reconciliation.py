"""Validerte kontrollbegreper og union av kontoer, uten nullpåfylling."""

import json
from dataclasses import replace
from pathlib import Path

import pytest
from openpyxl import load_workbook
from test_b5_controls import FIXTURES, prepared
from test_b5_register import edit_rows

from analyse.controlled import reprocess_controlled
from analyse.session import SessionSelection, build_session_report
from analyse.session_excel import export_session_excel
from analyse.session_reconciliation import AmountScope, Reconciliation, ReferenceValue
from innlesning.controls import export_controls, import_controls, store_evidence
from innlesning.sync import read_revision


def approved_delta(db: Path, directory: Path):
    extraction, register, basis = prepared(db, "40034443")
    target = next(o for o in extraction.observations if o.chapter == "900")
    proof = store_evidence(
        db,
        FIXTURES / "referat-5538.xml",
        version="syntetisk-kontroll",
        locator="/table",
        role="kontrollkilde",
        url="https://example.invalid/test",
    )
    path = directory / "review.csv"
    export_controls(db, (extraction.id,), path, register_snapshot=register.id, control_basis=basis)
    edit_rows(
        path,
        lambda rows: [
            r.update(
                status="godkjent",
                godkjente_felter="amount_kr",
                godkjent_bruk="analysebelop",
                bevis_id=proof.id,
                kontrollor="Test",
                begrunnelse="Syntetisk prøvekontroll",
            )
            for r in rows
        ],
    )
    assert not import_controls(db, path).errors
    result = reprocess_controlled(db, (extraction.id,), register.id, basis)
    job = read_revision(db, extraction.source_revision_id).current_observation_id
    selection = SessionSelection(
        "prove",
        "2024-2025",
        (job,),
        extraction_ids=(extraction.id,),
        controlled_result_ids=(result.id,),
    )
    reference = ReferenceValue(
        "900",
        "32",
        454_000_000,
        False,
        "https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034443&p=102001",
        extraction.artifact.sha256,
        target.pointer.locator,
        "Autentisk kildeverdi",
    )
    scope = AmountScope(2025, "2025-01-01", "2025-12-31", "avgrenset_endring")
    return selection, target, reference, scope


def test_exact_effective_value_matches_reference_and_amount_difference_is_retained(tmp_path):
    db = tmp_path / "match.sqlite"
    selection, target, reference, scope = approved_delta(db, tmp_path)
    check = Reconciliation("Prøve", scope, scope, (target.id,), (reference,))
    report = build_session_report(db, replace(selection, reconciliations=(check,)))
    assert report.reconciliations[0].status == "samsvar"
    assert report.reconciliations[0].rows[0].actual_amount_kr == 454_000_000
    wrong = replace(check, references=(replace(reference, expected_amount_kr=453_999_999),))
    report = build_session_report(db, replace(selection, reconciliations=(wrong,)))
    assert report.reconciliations[0].rows[0].status == "belopsavvik"
    assert report.reconciliations[0].rows[0].difference_kr == 1
    assert all(s.complete_total_kr is None for s in report.sums)  # Ingen inngående bevilgning.


def test_excel_binds_each_full_reconciliation_once_and_rows_keep_only_constant_scope(tmp_path):
    db = tmp_path / "scope-binding.sqlite"
    selection, target, reference, scope = approved_delta(db, tmp_path)
    scope_sizes = []
    for count in (1, 4):
        references = (reference,) + tuple(
            replace(
                reference, chapter=str(901 + n), reference=f"Separat referanse {n}: " + "x" * 100
            )
            for n in range(count - 1)
        )
        check = Reconciliation("Prøve", scope, scope, (target.id,), references)
        output = tmp_path / f"scope-{count}.xlsx"
        export_session_excel(db, replace(selection, reconciliations=(check,)), output)
        book = load_workbook(output)
        try:
            specifications = []
            for sheet in book:
                for row in sheet.values:
                    for value in row:
                        if not isinstance(value, str) or not value.startswith(("{", "[")):
                            continue
                        try:
                            pending = [json.loads(value)]
                        except json.JSONDecodeError:
                            continue
                        while pending:
                            item = pending.pop()
                            if isinstance(item, dict):
                                if {"references", "observation_ids", "actual_scope"} <= item.keys():
                                    specifications.append(item)
                                pending.extend(item.values())
                            elif isinstance(item, list):
                                pending.extend(item)
            assert len(specifications) == 1
            assert specifications[0]["name"] == "Prøve"
            assert len(specifications[0]["references"]) == count
            values = list(book["Avstemming"].values)
            rows = [dict(zip(values[0], row, strict=True)) for row in values[1:]]
            assert len(rows) == count
            for row in rows:
                scopes = json.loads(row["Omfang"])
                assert set(scopes) == {"actual_scope", "reference_scope"}
                assert scopes["actual_scope"]["concept"] == "avgrenset_endring"
                assert row["Kontrollgrunnlag"] == "Sesjonsgrunnlag!B4/reconciliations/0"
            scope_sizes.append(len(rows[0]["Omfang"]))
        finally:
            book.close()
    assert scope_sizes[0] == scope_sizes[1]


@pytest.mark.parametrize(
    "change",
    [
        {"concept": "rekneskap"},
        {"concept": "samla_loyving"},
        {"concept": "saldert"},
        {"budget_year": 2024},
        {"period_start": "2025-07-01"},
        {"currency": "EUR"},
        {"multiplier": "1000"},
        {"detail_level": "underpost"},
    ],
)
def test_wrong_concept_year_period_unit_or_level_cannot_pass_reconciliation(tmp_path, change):
    db = tmp_path / "wrong.sqlite"
    selection, target, reference, scope = approved_delta(db, tmp_path)
    reference_scope = replace(scope, **change)
    if reference_scope.detail_level == "underpost":
        reference = replace(reference, subpost="1")
    check = Reconciliation("Feil omfang", scope, reference_scope, (target.id,), (reference,))
    report = build_session_report(db, replace(selection, reconciliations=(check,)))
    assert all(r.status == "uforenlig_omfang" for r in report.reconciliations[0].rows)
    assert all(r.actual_amount_kr is None for r in report.reconciliations[0].rows)


def test_explicit_reference_absence_is_different_from_observed_zero_and_missing_field(tmp_path):
    db = tmp_path / "absence.sqlite"
    selection, target, reference, scope = approved_delta(db, tmp_path)
    absent = replace(reference, expected_amount_kr=None, absent=True)
    check = Reconciliation("Uttrykkelig fravær", scope, scope, (target.id,), (absent,))
    row = (
        build_session_report(db, replace(selection, reconciliations=(check,)))
        .reconciliations[0]
        .rows[0]
    )
    assert row.status == "mangler_i_kontrollgrunnlag" and row.reference_absent is True
    assert row.expected_amount_kr is None and row.actual_amount_kr == 454_000_000
    with pytest.raises(ValueError, match="uttrykkelig fravær"):
        replace(reference, expected_amount_kr=None)
    with pytest.raises(ValueError, match="uttrykkelig fravær"):
        replace(reference, expected_amount_kr=0, absent=True)
