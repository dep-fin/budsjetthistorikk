"""Autentiske ANNET-, netto-, 90- og konfliktprøver i samlet sesjonseksport."""

import hashlib
import json
from pathlib import Path

import pytest
from test_b4 import ingest
from test_b6 import session_for

from analyse.session import SessionSelection, build_session_report
from innlesning import extract_revision, read_sync, sync_saved
from innlesning.observations import Interpretation


def test_annet_without_introductory_phrase_keeps_all_76_events_and_partial_provenance(
    tmp_path: Path,
):
    db = tmp_path / "missing-phrase.sqlite"
    directory = Path(__file__).parent / "fixtures/b6"
    jobs, ids = [], []
    for identifier, count in (("40034048", 2), ("40034229", 74)):
        raw = (directory / f"{identifier}.xml").read_bytes()
        meta = json.loads((directory / f"{identifier}.json").read_text(encoding="utf-8"))
        assert hashlib.sha256(raw).hexdigest() == meta["sha256"]
        job = sync_saved(db, raw, meta, historical_sample=True, decision_id=identifier)
        jobs.append(job)
        extraction = extract_revision(
            db,
            read_sync(db, job).entries[0].revision_id,
            interpretation=Interpretation(adapter_version="storting-belop-v2"),
        )
        ids.append(extraction.id)
        assert len({o.step_id for o in extraction.observations}) == count
    report = build_session_report(
        db, SessionSelection("prove", "2024-2025", tuple(jobs), extraction_ids=tuple(ids))
    )
    assert {r.api_type for r in report.inventory} == {"ANNET"}
    assert len({r.observation.step_id for r in report.rows}) == 76
    assert not report.coverage.source_complete


@pytest.mark.parametrize(
    "chapter,post,identifiers,final",
    [
        ("1860", "1", ("40032850", "40033719", "40034064", "40034226"), 360_312_000),
        ("4860", "1", ("40032850", "40033719", "40034064", "40034226"), 83_400_000),
        ("5999", "90", ("40033025", "40033719", "40034287"), 120_371_709_000),
    ],
)
def test_authentic_chain_conflicts_remain_visible_in_aggregate(
    tmp_path, chapter, post, identifiers, final
):
    db = tmp_path / "conflict.sqlite"
    extractions = tuple(ingest(db, i) for i in identifiers)
    report = build_session_report(
        db, session_for(db, extractions, chapters=(chapter,), posts=(post,))
    )
    assert any("kjedekonflikt" in r.issues for r in report.rows)
    afters = [r.observation for r in report.rows if r.observation.meaning == "etter_belop"]
    assert afters[-1].amount_kr == final
    assert all(s.complete_total_kr is None for s in report.sums)
    if chapter == "5999":
        assert any(o.amount_kr == 0 for o in afters)
    else:
        assert len({o.api_id for o in afters[-2:]}) == 2
    excluded = build_session_report(db, session_for(db, extractions, posts=("99",)))
    assert "kjedekonflikt" in excluded.issues
    assert all(
        r.selection_status == "utenfor"
        for r in excluded.unfiltered_rows
        if r.observation.chapter == chapter and r.observation.post == post
    )


def test_post24_total_and_components_remain_separate_and_later_level_is_not_delta(tmp_path):
    db = tmp_path / "net.sqlite"
    original, later = (ingest(db, i) for i in ("40032850", "40034064"))
    report = build_session_report(
        db, session_for(db, (original, later), chapters=("2470",), posts=("24",))
    )
    assert {s.detail_level for s in report.sums} == {"post", "underpost"}
    assert any("mangler_delta" in r.issues for r in report.rows)
    assert not any(r.observation.meaning == "endring" for r in report.rows)
    assert [
        r.observation.amount_kr for r in report.rows if r.observation.detail_level == "post"
    ] == [-15_000_000, -15_000_000]
