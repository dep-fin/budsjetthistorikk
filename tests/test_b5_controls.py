"""Faglig kontroll gjennom fil, varig import, gjenåpning og separat analyse."""

import hashlib
from pathlib import Path

import pytest
from openpyxl import load_workbook
from test_b4 import ingest
from test_b5_register import edit_rows

from analyse.controlled import export_controlled_excel, reprocess_controlled
from innlesning import extract_revision, read_extraction
from innlesning.controls import (
    activate_basis,
    define_control_basis,
    export_controls,
    import_controls,
    read_decision,
    store_evidence,
)
from innlesning.observations import Interpretation
from innlesning.registers import seed_register

FIXTURES = Path(__file__).parent / "fixtures" / "b5"


def prepared(db: Path, identifier: str = "40036289"):
    old = ingest(db, identifier)
    register = seed_register(db)
    extraction = extract_revision(
        db,
        old.source_revision_id,
        interpretation=Interpretation(
            adapter_version="storting-belop-v2", register_snapshot=register.id
        ),
    )
    basis = define_control_basis(db, "Manuell kontroll mot uttrykkelig bevis; ingen årsdekning")
    activate_basis(db, (extraction.id,), register.id, basis)
    return extraction, register, basis


@pytest.mark.parametrize("suffix", [".xlsx", ".csv"])
def test_referat_bound_correction_only_changes_effective_after_amount(
    tmp_path: Path, suffix: str
) -> None:
    db = tmp_path / "control.sqlite"
    extraction, register, basis = prepared(db)
    target = next(
        o for o in extraction.observations if o.post == "70" and o.meaning == "etter_belop"
    )
    before = next(o for o in extraction.observations if o.post == "70" and o.meaning == "for_belop")
    assert target.raw_value == "I 615 833" and target.amount_kr is None
    assert before.pointer.locator == target.pointer.locator  # Beløpsfeltet er nødvendig.
    raw = (FIXTURES / "referat-5538.xml").read_bytes()
    from lxml import etree

    assert (
        hashlib.sha256(raw).hexdigest()
        == "7fa34518b05f948e7ff834995e97513a492262790be8445609bc453c9a09ff51"
    )
    node = etree.fromstring(
        raw, parser=etree.XMLParser(resolve_entities=False, no_network=True)
    ).xpath("/table/tgroup/tbody/row[3]/entry[3]/A")
    assert len(node) == 1
    compact_cell = "".join("".join(node[0].itertext()).split())
    assert compact_cell == "frakr2770000000tilkr1615833000"
    assert compact_cell.split("tilkr")[1] == "1615833000"
    evidence = store_evidence(
        db,
        FIXTURES / "referat-5538.xml",
        version="refs-202526-03-26",
        locator="/table/tgroup/tbody/row[3]/entry[3]/A",
        role="kontrollkilde",
        url="https://data.stortinget.no/eksport/publikasjon?publikasjonid=refs-202526-03-26",
        parent_sha256="4eed3a96b705a6bc80f9f7776efbde1c3dab07f36b898ed4722617ff59ea5b56",
    )
    assert evidence.sha256 == hashlib.sha256(raw).hexdigest()
    path = tmp_path / ("kontroll" + suffix)
    export_controls(
        db,
        (extraction.id,),
        path,
        register_snapshot=register.id,
        control_basis=basis,
        observation_ids=(target.id,),
    )

    def approve(rows: list[dict[str, str]]) -> None:
        rows[0].update(
            status="godkjent",
            godkjente_felter="amount_kr",
            godkjent_bruk="analysebelop",
            korrigert_belop_kr="1615833000",
            begrunnelse="Referatets fulle tall, representasjonsavvik bevart",
            kontrollor="Saksbehandler",
            bevis_id=evidence.id,
        )

    edit_rows(path, approve)
    imported = import_controls(db, path)
    assert not imported.errors and len(imported.new_ids) == 1
    view = read_decision(db, imported.new_ids[0])
    assert view.freshness == "gjeldende" and view.decision.corrected_amount_kr == 1_615_833_000
    assert import_controls(db, path) == imported
    result = reprocess_controlled(db, (extraction.id,), register.id, basis)
    row = next(r for r in result.rows if r.observation_id == target.id)
    assert row.raw_amount_kr is None and row.effective_amount_kr == 1_615_833_000
    assert row.decision_id == view.decision.id and row.raw_value == "I 615 833"
    assert next(r for r in result.rows if r.observation_id == before.id).effective_amount_kr is None
    assert result.approved_chain_balance is None and not result.complete
    assert read_extraction(db, extraction.id) == extraction
    output = tmp_path / "result.xlsx"
    export_controlled_excel(db, result.id, output)
    book = load_workbook(output)
    values = [c.value for s in book for row in s for c in row]
    assert "I 615 833" in values and 1_615_833_000 in values and evidence.id in values
    assert not any(c.data_type == "f" for s in book for row in s for c in row)
    book.close()


@pytest.mark.parametrize("status", ["avvist", "til_kontroll"])
def test_new_decision_excludes_previous_approval_and_stale_file_cannot_overwrite(
    tmp_path: Path, status: str
) -> None:
    db = tmp_path / "later.sqlite"
    extraction, register, basis = prepared(db)
    target = extraction.observations[0]
    proof = store_evidence(
        db,
        FIXTURES / "referat-5538.xml",
        version="referat",
        locator="/table",
        role="kontrollkilde",
        url="https://data.stortinget.no/",
    )
    first = tmp_path / "first.csv"
    export_controls(
        db,
        (extraction.id,),
        first,
        register_snapshot=register.id,
        control_basis=basis,
        observation_ids=(target.id,),
    )

    def approve(rows):
        rows[0].update(
            status="godkjent",
            godkjente_felter="amount_kr",
            godkjent_bruk="analysebelop",
            begrunnelse="Sjekket",
            kontrollor="Kontrollør",
            bevis_id=proof.id,
        )

    edit_rows(first, approve)
    approved = import_controls(db, first)
    assert not approved.errors
    stale = tmp_path / "stale.csv"
    second = tmp_path / "second.xlsx"
    for path in (stale, second):
        export_controls(
            db,
            (extraction.id,),
            path,
            register_snapshot=register.id,
            control_basis=basis,
            observation_ids=(target.id,),
        )
    edit_rows(
        second,
        lambda rows: rows[0].update(
            status=status, begrunnelse="Ny vurdering", kontrollor="Kontrollør 2"
        ),
    )
    newer = import_controls(db, second)
    assert not newer.errors
    assert read_decision(db, approved.new_ids[0]).freshness == "utdatert"
    edit_rows(stale, approve)
    rejected = import_controls(db, stale)
    assert any(e.field == "forgjenger" for e in rejected.errors)
    assert import_controls(db, first) == approved  # Replay endrer ingen gjeldende peker.
    result = reprocess_controlled(db, (extraction.id,), register.id, basis)
    row = next(r for r in result.rows if r.observation_id == target.id)
    assert row.status == status and row.effective_amount_kr is None


@pytest.mark.parametrize(
    "field",
    [
        "dataset",
        "revision_id",
        "interpretation_id",
        "locator",
        "amount_field",
        "register_snapshot",
        "control_basis",
        "raw_value",
        "observation_id",
        "eksport_id",
    ],
)
def test_control_binding_tamper_persists_error_without_any_decision(
    tmp_path: Path, field: str
) -> None:
    from innlesning.controls import latest_decision
    from innlesning.maintenance_store import read_import

    db = tmp_path / "tamper.sqlite"
    extraction, register, basis = prepared(db)
    target = extraction.observations[0]
    path = tmp_path / "tamper.csv"
    export_controls(
        db,
        (extraction.id,),
        path,
        register_snapshot=register.id,
        control_basis=basis,
        observation_ids=(target.id,),
    )
    edit_rows(
        path,
        lambda rows: rows[0].update(
            {field: "tampered", "status": "avvist", "kontrollor": "Test", "begrunnelse": "Test"}
        ),
    )
    result = import_controls(db, path)
    assert result.errors and not result.new_ids and latest_decision(db, target.id) is None
    assert read_import(db, result.id) == result


def review_one(db, extraction, register, basis, path, status="avvist"):
    export_controls(
        db,
        (extraction.id,),
        path,
        register_snapshot=register.id,
        control_basis=basis,
        observation_ids=(extraction.observations[0].id,),
    )
    edit_rows(
        path,
        lambda rows: rows[0].update(status=status, begrunnelse="Vurdert", kontrollor="Kontrollør"),
    )
    imported = import_controls(db, path)
    assert not imported.errors
    return imported.new_ids[0]


@pytest.mark.parametrize("change", ["control", "interpretation", "register"])
def test_active_basis_a_b_a_never_reactivates_old_decision(tmp_path: Path, change: str) -> None:
    from dataclasses import replace

    from innlesning.registers import export_register, import_register

    db = tmp_path / "basis.sqlite"
    extraction, register, basis = prepared(db)
    decision_id = review_one(db, extraction, register, basis, tmp_path / "a.csv")
    if change == "control":
        other_basis = define_control_basis(db, "Et annet kontrollgrunnlag")
        activate_basis(db, (extraction.id,), register.id, other_basis)
    elif change == "interpretation":
        other = extract_revision(
            db,
            extraction.source_revision_id,
            interpretation=replace(extraction.interpretation, reason="Annen eksplisitt tolkning"),
        )
        # Historisk/alternativ lesing i seg selv skal ikke aktivere.
        assert read_decision(db, decision_id).freshness == "gjeldende"
        activate_basis(db, (other.id,), register.id, basis)
    else:
        file = tmp_path / "register.csv"
        export_register(db, register.id, file)
        edit_rows(file, lambda rows: rows[1].update(begrunnelse="Endret registergrunnlag"))
        other_register = import_register(db, file).snapshot_id
        other = extract_revision(
            db,
            extraction.source_revision_id,
            interpretation=replace(extraction.interpretation, register_snapshot=other_register),
        )
        assert read_decision(db, decision_id).freshness == "gjeldende"
        activate_basis(db, (other.id,), other_register, basis)
    assert read_decision(db, decision_id).freshness == "utdatert"
    activate_basis(db, (extraction.id,), register.id, basis)
    assert read_decision(db, decision_id).freshness == "utdatert"
    new_id = review_one(db, extraction, register, basis, tmp_path / "fresh.csv")
    assert read_decision(db, new_id).freshness == "gjeldende"


def test_source_a_b_a_and_pending_attempt_are_separate_from_professional_status(
    tmp_path: Path,
) -> None:
    import json

    from innlesning import read_sync, resume_sync, stage_sync, sync_saved

    db = tmp_path / "source.sqlite"
    extraction, register, basis = prepared(db)
    decision_id = review_one(db, extraction, register, basis, tmp_path / "a.csv")
    directory = FIXTURES.parent / "b3"
    original = (directory / "40036289.xml").read_bytes()
    changed = original.replace(b"2 770 000 000", b"2 771 000 000")
    assert changed != original

    def metadata(raw, minute):
        data = json.loads((directory / "40036289.json").read_text(encoding="utf-8"))
        data.update(
            sha256=hashlib.sha256(raw).hexdigest(),
            bytes=len(raw),
            retrieved_utc=f"2026-10-21T08:{minute:02d}:00+00:00",
        )
        return data

    pending = stage_sync(
        db, changed, metadata(changed, 1), historical_sample=True, decision_id="40036289"
    )
    view = read_decision(db, decision_id)
    assert view.freshness == "ikke_vurderbar" and view.decision.status == "avvist"
    resume_sync(db, pending)
    assert read_decision(db, decision_id).freshness == "utdatert"
    back = sync_saved(
        db, original, metadata(original, 2), historical_sample=True, decision_id="40036289"
    )
    assert read_sync(db, back).entries[0].revision_id == extraction.source_revision_id
    assert read_decision(db, decision_id).freshness == "utdatert"
    newer = review_one(db, extraction, register, basis, tmp_path / "fresh.csv")
    assert read_decision(db, newer).freshness == "gjeldende"


def test_latest_selected_source_attempt_does_not_reassess_other_decision(tmp_path: Path) -> None:
    import json

    from innlesning import sync_saved

    db = tmp_path / "scope.sqlite"
    extraction, register, basis = prepared(db)
    decision_id = review_one(db, extraction, register, basis, tmp_path / "review.csv")
    directory = FIXTURES.parent / "b3"
    raw = (directory / "40036289.xml").read_bytes().replace(b"40036289", b"40036290")
    metadata = json.loads((directory / "40036289.json").read_text(encoding="utf-8"))
    metadata.update(
        fixture_kind="synthetic_test",
        sha256=hashlib.sha256(raw).hexdigest(),
        bytes=len(raw),
        retrieved_utc="2026-10-21T09:00:00+00:00",
    )
    sync_saved(db, raw, metadata, historical_sample=True, decision_id="40036290")
    view = read_decision(db, decision_id)
    assert view.freshness == "ikke_vurderbar" and view.decision.status == "avvist"
    assert "ikke omfattet av siste valgte observasjon" in view.source_context_json


def test_formula_and_invalid_row_abort_whole_control_file(tmp_path: Path) -> None:
    from innlesning.controls import latest_decision

    db = tmp_path / "formula.sqlite"
    extraction, register, basis = prepared(db)
    path = tmp_path / "formula.xlsx"
    export_controls(
        db,
        (extraction.id,),
        path,
        register_snapshot=register.id,
        control_basis=basis,
        observation_ids=tuple(o.id for o in extraction.observations[:2]),
    )

    def edits(rows):
        for row in rows:
            row.update(status="avvist", kontrollor="Kontrollør", begrunnelse="Kontroll")
        rows[1]["begrunnelse"] = "=1+1"

    edit_rows(path, edits)
    result = import_controls(db, path)
    assert result.errors and not result.new_ids
    assert latest_decision(db, extraction.observations[0].id) is None


def test_explicit_approved_chain_is_separate_from_technical_balance(tmp_path: Path) -> None:
    from test_b4 import synthetic

    from analyse import HistorySelection, calculate_history
    from analyse.controlled import read_controlled
    from innlesning.registers import PostEntry, export_register, import_register

    db = tmp_path / "approved.sqlite"
    original = synthetic(
        db,
        "<table><tr><td>Kap.</td><td>Post</td><td>Formål</td><td>Kroner</td></tr>"
        "<tr><td>41</td><td></td><td>Stortinget</td><td></td></tr>"
        "<tr><td></td><td>1</td><td>Drift</td><td>10</td></tr></table>",
        year=2027,
    )
    seed = seed_register(db)
    register_file = tmp_path / "register.csv"
    export_register(db, seed.id, register_file)

    def add_post(rows):
        rows.append(
            {
                "radtype": "post",
                **{
                    k: str(v)
                    for k, v in PostEntry(
                        "41", "1", 2027, 2027, "Syntetisk kilde", "table[1]/tr[3]", "Kun test"
                    )
                    .to_row()
                    .items()
                },
            }
        )

    edit_rows(register_file, add_post)
    snapshot_id = import_register(db, register_file).snapshot_id
    extraction = extract_revision(
        db,
        original.source_revision_id,
        interpretation=Interpretation(
            adapter_version="storting-belop-v2", register_snapshot=snapshot_id
        ),
    )
    selection = HistorySelection("prove", (extraction.id,), 2027, "41", "1")
    assert calculate_history(db, selection).approved_balance == 10
    basis = define_control_basis(db, "Uttrykkelig avgrenset kontroll av syntetisk kjede")
    activate_basis(db, (extraction.id,), snapshot_id, basis)
    unreviewed = reprocess_controlled(db, (extraction.id,), snapshot_id, basis, selection=selection)
    assert unreviewed.approved_chain_balance is None
    proof = store_evidence(
        db,
        FIXTURES / "referat-5538.xml",
        version="syntetisk-testreferanse",
        locator="/table",
        role="kontrollkilde",
        url="https://example.invalid/test",
    )
    path = tmp_path / "review.csv"
    export_controls(db, (extraction.id,), path, register_snapshot=snapshot_id, control_basis=basis)
    edit_rows(
        path,
        lambda rows: rows[0].update(
            status="godkjent",
            godkjente_felter="amount_kr,organization,catalogue",
            godkjent_bruk="kjedegrunnlag",
            bevis_id=proof.id,
            begrunnelse="Kun syntetisk prøvegodkjenning",
            kontrollor="Testkontrollør",
        ),
    )
    approved = import_controls(db, path)
    assert not approved.errors
    result = reprocess_controlled(db, (extraction.id,), snapshot_id, basis, selection=selection)
    assert result.approved_chain_balance == 10 and result.id != unreviewed.id
    assert read_controlled(db, unreviewed.id).freshness == "utdatert"
    assert "ingen faglig kjede- eller årsgodkjenning" in result.coverage


@pytest.mark.parametrize("chapter,post", [("1860", "1"), ("4860", "1"), ("5999", "90")])
def test_single_amount_approvals_do_not_remove_authentic_chain_conflicts(
    tmp_path: Path, chapter: str, post: str
) -> None:
    from analyse import HistorySelection, read_history

    db = tmp_path / "conflict.sqlite"
    source_ids = (
        ("40033025", "40033719", "40034287")
        if chapter == "5999"
        else ("40032850", "40033719", "40034064", "40034226")
    )
    seed = seed_register(db)
    basis = define_control_basis(db, "Enkeltbeløp opphever ikke dokumentert kjedekonflikt")
    proof = store_evidence(
        db,
        FIXTURES / "referat-5538.xml",
        version="syntetisk-testreferanse",
        locator="/table",
        role="kontrollkilde",
        url="https://example.invalid/test",
    )
    ids = []
    for identifier in source_ids:
        original = ingest(db, identifier)
        extraction = extract_revision(
            db,
            original.source_revision_id,
            interpretation=Interpretation(
                adapter_version="storting-belop-v2", register_snapshot=seed.id
            ),
        )
        ids.append(extraction.id)
        activate_basis(db, (extraction.id,), seed.id, basis)
        obs = tuple(o.id for o in extraction.observations if (o.chapter, o.post) == (chapter, post))
        if not obs:
            continue
        path = tmp_path / f"{identifier}.csv"
        export_controls(
            db,
            (extraction.id,),
            path,
            register_snapshot=seed.id,
            control_basis=basis,
            observation_ids=obs,
        )

        def approve(rows):
            for row in rows:
                row.update(
                    status="godkjent",
                    godkjente_felter="amount_kr",
                    godkjent_bruk="kjedegrunnlag",
                    bevis_id=proof.id,
                    begrunnelse="Test av kjedesperre",
                    kontrollor="Test",
                )

        edit_rows(path, approve)
        assert not import_controls(db, path).errors
    result = reprocess_controlled(
        db,
        tuple(ids),
        seed.id,
        basis,
        selection=HistorySelection("prove", tuple(ids), 2024, chapter, post),
    )
    assert result.approved_chain_balance is None
    assert "kjedekonflikt" in {
        a.code for a in read_history(db, result.technical_calculation_id).anomalies
    }
