"""Frosset rapport er versjonert JSON med felt-/typevern, ikke vilkårlig objektkode."""

import json
from pathlib import Path

import pytest
from test_b2 import synchronize

from analyse import SessionSelection, build_session_report
from analyse.session_serialization import report_from_json, report_to_json


@pytest.mark.parametrize("fault", ["version", "field", "type", "complete", "duplicate", "nan"])
def test_frozen_report_rejects_unknown_versions_fields_types_and_false_complete(
    tmp_path: Path, fault: str
) -> None:
    db = tmp_path / "frozen.sqlite"
    job = synchronize(db)
    raw = report_to_json(build_session_report(db, SessionSelection("prove", "2024-2025", (job,))))
    data = json.loads(raw)
    if fault == "version":
        data["format"] = "future"
    elif fault == "field":
        data["report"]["unexpected"] = "not allowed"
    elif fault == "type":
        data["report"]["coverage"]["source_count"] = True
    elif fault == "complete":
        data["report"]["coverage"]["professional_complete"] = True
    raw = json.dumps(data)
    if fault == "duplicate":
        raw = raw.replace(
            '"format": "b6-frozen-1"', '"format": "b6-frozen-1", "format": "b6-frozen-1"'
        )
    elif fault == "nan":
        raw = raw.replace('"source_count": 1', '"source_count": NaN')
    with pytest.raises(ValueError):
        report_from_json(raw)
