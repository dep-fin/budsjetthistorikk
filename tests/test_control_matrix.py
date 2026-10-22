"""Den frosne P2-matrisen er en separat kontroll, uten aktivering i innlesningen."""

import hashlib
import json
import shutil
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from analyse.control_matrix import main, proposed_h2024_integer, read_control_matrix

MATRIX = (
    Path(__file__).parents[1] / "docs/research/historisk-excel/p13-p2/control-matrix-2024-v1.json"
)


def _write_matrix(tmp_path: Path, matrix: dict[str, Any]) -> Path:
    path = tmp_path / MATRIX.name
    for evidence in read_control_matrix(MATRIX)["evidence_files"]:
        shutil.copyfile(MATRIX.parent / evidence["path"], tmp_path / evidence["path"])
    path.write_text(json.dumps(matrix), encoding="utf-8")
    return path


def test_original_proposal_requires_typed_reference_without_expected_hash(tmp_path: Path) -> None:
    matrix = read_control_matrix(MATRIX)
    matrix["prior_controls"][0]["references"] = "removed original proposal proof"
    path = _write_matrix(tmp_path, matrix)
    with pytest.raises(ValueError):
        read_control_matrix(path)
    result = subprocess.run(
        [sys.executable, "-m", "analyse.control_matrix", str(path)],
        cwd=MATRIX.parents[4],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "invalid"


@pytest.mark.parametrize("column_index", [0, 1])
@pytest.mark.parametrize(
    "field,value",
    [
        ("budget_year", 2025),
        ("budget_year", "2024"),
        ("budget_year", 2024.0),
        ("unit", "USD"),
        ("candidate_multiplier", "1000000"),
        ("candidate_multiplier", 1),
        ("figure_type", "stortingsvedtak"),
        ("meaning", "uavklart"),
        ("stage", "nysaldering"),
        ("period", "regnskapsåret"),
        ("detail_level", "underpost"),
        ("budget_side", "ukjent"),
        ("reference_basis", "avledet_komponentdifferanse"),
        ("unknown", "unsupported claim"),
    ],
)
def test_original_proposal_requires_compatible_closed_scope_without_expected_hash(
    tmp_path: Path, column_index: int, field: str, value: Any
) -> None:
    matrix = read_control_matrix(MATRIX)
    matrix["prior_controls"][column_index]["references"][0]["scope"][field] = value
    with pytest.raises(ValueError):
        read_control_matrix(_write_matrix(tmp_path, matrix))


@pytest.mark.parametrize(
    "field,value",
    [
        ("cells", ["G3"]),
        ("meaning", "endring"),
        ("unknown", "unsupported claim"),
        ("references", []),
        ("references", ["removed proof"]),
        ("references.0.unknown", "unsupported claim"),
        ("references.0.key", ["151", "70"]),
        ("references.0.key", "1/1"),
        ("references.0.amount_kr", "NaN"),
        ("references.0.amount_kr", 14768000),
        ("references.0.source_budget_year", 2025),
        ("references.0.source_budget_year", "2024"),
        ("references.0.pointers", []),
        ("references.0.pointers", "removed locator"),
        ("references.0.pointers.0", "removed locator"),
        ("references.0.pointers.0.unknown", "unsupported claim"),
        ("references.0.pointers.0.xpath", ""),
        ("references.0.pointers.0.xpath", "   "),
        ("references.0.pointers.0.xpath", "not an absolute source locator"),
        ("references.0.pointers.0.short_evidence", ""),
        ("references.0.pointers.0.source_sha256", "0" * 64),
        ("sources.0.unknown", "unsupported metadata"),
        ("sources.0.bytes", "998471"),
        ("sources.0.bytes", True),
        ("sources.0.bytes", 0),
        ("sources.0.retrieved_date", "not a date"),
        ("sources.0.kind", ""),
        ("sources.0.url", "https://example.org/unrelated"),
    ],
)
def test_original_proposal_rejects_unbound_or_untyped_reference_without_expected_hash(
    tmp_path: Path, field: str, value: Any
) -> None:
    matrix = read_control_matrix(MATRIX)
    target: Any = matrix["prior_controls"][0]
    tokens = field.split(".")
    for token in tokens[:-1]:
        target = target[int(token)] if isinstance(target, list) else target[token]
    if isinstance(target, list):
        target[int(tokens[-1])] = value
    else:
        target[tokens[-1]] = value
    with pytest.raises(ValueError):
        read_control_matrix(_write_matrix(tmp_path, matrix))


@pytest.mark.parametrize("field", ["references", "sources"])
@pytest.mark.parametrize("duplicate", [False, True])
def test_original_proposal_rejects_missing_or_duplicate_proof(
    tmp_path: Path, field: str, duplicate: bool
) -> None:
    matrix = read_control_matrix(MATRIX)
    control = matrix["prior_controls"][0]
    if duplicate:
        control[field].append(control[field][0])
    else:
        del control[field]
    with pytest.raises(ValueError):
        read_control_matrix(_write_matrix(tmp_path, matrix))


@pytest.mark.parametrize("column_index,row_index", [(0, 0), (1, 2)])
@pytest.mark.parametrize("subscope", [False, True])
def test_internal_proposal_evidence_must_resolve_the_matching_reference(
    tmp_path: Path, column_index: int, row_index: int, subscope: bool
) -> None:
    matrix = read_control_matrix(MATRIX)
    row = matrix["rows"][row_index]
    refs = row["subscopes"][0]["evidence"] if subscope else row["source_evidence"]
    refs[0]["matrix_pointer"] = f"/prior_controls/{1 - column_index}"
    with pytest.raises(ValueError):
        read_control_matrix(_write_matrix(tmp_path, matrix))


@pytest.mark.parametrize("row_index", [0, 2])
@pytest.mark.parametrize("subscope", [False, True])
def test_proposal_row_cannot_substitute_unrelated_valid_evidence(
    tmp_path: Path, row_index: int, subscope: bool
) -> None:
    matrix = read_control_matrix(MATRIX)
    row = matrix["rows"][row_index]
    refs = [{"file": "precision-summary.json", "pointer": "/baseline"}]
    if subscope:
        row["subscopes"][0]["evidence"] = refs
    else:
        row["source_evidence"] = refs
    with pytest.raises(ValueError):
        read_control_matrix(_write_matrix(tmp_path, matrix))


@pytest.mark.parametrize("field", ["budget_year", "figure_type"])
def test_cli_rejects_incompatible_original_proposal_without_expected_hash(
    tmp_path: Path, field: str
) -> None:
    matrix = read_control_matrix(MATRIX)
    matrix["prior_controls"][1]["references"][0]["scope"][field] = (
        2025 if field == "budget_year" else "stortingsvedtak"
    )
    path = _write_matrix(tmp_path, matrix)
    result = subprocess.run(
        [sys.executable, "-m", "analyse.control_matrix", str(path)],
        cwd=MATRIX.parents[4],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "invalid"


@pytest.mark.parametrize(
    "invalid_manifest",
    [
        "too_few",
        "too_many",
        "duplicate",
        "unknown_name",
        "entry_shape",
        "hash",
        "size",
        "zero_size",
        "negative_size",
        "oversized",
        "total_budget",
        "kind",
        "unknown_metadata",
    ],
)
def test_invalid_evidence_manifest_opens_no_evidence_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, invalid_manifest: str
) -> None:
    matrix = read_control_matrix(MATRIX)
    entries = matrix["evidence_files"]
    if invalid_manifest == "too_few":
        entries.pop()
    elif invalid_manifest == "too_many":
        entries.append(entries[0])
    elif invalid_manifest == "duplicate":
        entries[-1] = entries[0]
    elif invalid_manifest == "unknown_name":
        entries[-1]["path"] = "unrelated.json"
        (tmp_path / "unrelated.json").write_bytes(b"{}")
    elif invalid_manifest == "entry_shape":
        entries[-1] = "removed metadata"
    elif invalid_manifest == "hash":
        entries[-1]["sha256"] = "not a hash"
    elif invalid_manifest == "size":
        entries[-1]["bytes"] = True
    elif invalid_manifest == "zero_size":
        entries[-1]["bytes"] = 0
    elif invalid_manifest == "negative_size":
        entries[-1]["bytes"] = -1
    elif invalid_manifest == "oversized":
        entries[-1]["bytes"] = 2 * 1024 * 1024
    elif invalid_manifest == "total_budget":
        for entry in entries:
            entry["bytes"] = 600_000
    elif invalid_manifest == "kind":
        entries[-1]["kind"] = "unrelated"
    else:
        entries[-1]["unknown"] = "unsupported metadata"
    path = _write_matrix(tmp_path, matrix)
    opened: list[str] = []
    original_open = Path.open

    def recording_open(file: Path, *args: Any, **kwargs: Any) -> Any:
        if file.parent == tmp_path and file != path:
            opened.append(file.name)
        return original_open(file, *args, **kwargs)

    monkeypatch.setattr(Path, "open", recording_open)
    with pytest.raises(ValueError):
        read_control_matrix(path)
    assert opened == []


def test_normal_evidence_reads_have_fixed_per_file_and_total_budgets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    matrix = read_control_matrix(MATRIX)
    path = _write_matrix(tmp_path, matrix)
    reads: list[tuple[str, int]] = []
    original_open = Path.open

    def recording_open(file: Path, *args: Any, **kwargs: Any) -> Any:
        stream = original_open(file, *args, **kwargs)
        if file.parent == tmp_path and file != path:
            original_read = stream.read

            def recording_read(size: int = -1) -> Any:
                reads.append((file.name, size))
                return original_read(size)

            stream.read = recording_read
        return stream

    monkeypatch.setattr(Path, "open", recording_open)
    assert read_control_matrix(path) == matrix
    assert len(reads) == 4
    assert dict(reads) == {entry["path"]: entry["bytes"] + 1 for entry in matrix["evidence_files"]}
    assert all(0 < size <= 2 * 1024 * 1024 for _, size in reads)
    assert sum(size for _, size in reads) <= 2 * 1024 * 1024


def test_evidence_read_stops_at_declared_size_even_if_file_grows(tmp_path: Path) -> None:
    matrix = read_control_matrix(MATRIX)
    path = _write_matrix(tmp_path, matrix)
    changed = tmp_path / "precision-summary.json"
    changed.write_bytes(changed.read_bytes() + b" ")
    with pytest.raises(ValueError, match="bytegrense"):
        read_control_matrix(path)


def test_frozen_matrix_covers_all_nine_columns_without_approval() -> None:
    matrix = read_control_matrix(MATRIX)
    assert [row["column"] for row in matrix["rows"]] == list("GHIJKLMN") + ["docD"]
    assert matrix["professional_approval"] == {"status": "OPEN", "actor": None}
    assert matrix["activation"] == "NONE"


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("170591.75599999999", 170_591_756_000),
        ("336484.23200000002", 336_484_232_000),
        ("-15", -15_000_000),
        ("0", 0),
        ("1.0000005", None),
        ("NaN", None),
        ("Infinity", None),
        ("10000000000000000", None),
    ],
)
def test_proposal_reproduces_integer_candidates_without_approving_normalization(
    raw: str, expected: int | None
) -> None:
    assert proposed_h2024_integer(raw) == expected


@pytest.mark.parametrize(
    "field,value",
    [
        ("version", 2),
        ("budget_year", 2025),
        ("activation", "CURRENT"),
        ("normalized_values_changed", True),
        ("year_coverage", "COMPLETE"),
        ("professional_approval", {"status": "APPROVED", "actor": "invented"}),
        ("rows.0.economic_meaning", "endring"),
        ("rows.0.figure_type", "stortingsvedtak"),
        ("rows.0.stage", "rnb"),
        ("rows.0.unit.currency", "USD"),
        ("rows.0.unit.universal_column_year_approval", True),
        ("rows.0.source_factor", "1"),
        ("rows.0.source_correspondence_status", "APPROVED"),
        ("rows.0.subscopes.0.status", "APPROVED"),
        ("rows.0.source_evidence", []),
        ("rows.0.source_evidence.0.matrix_pointer", "/rows/0"),
        ("rows.1.precision.proposal.conditions", []),
        ("rows.1.precision.proposal_applied", True),
        ("rows.1.subscopes.0.evidence.0.pointer", "/nonexistent"),
        ("rows.0.precision", {}),
        ("rows", []),
        ("evidence_files.0.path", "../precision-summary.json"),
    ],
)
def test_reader_rejects_unsupported_or_incomplete_claims(
    tmp_path: Path, field: str, value: Any
) -> None:
    matrix = read_control_matrix(MATRIX)
    target: Any = matrix
    tokens = field.split(".")
    for token in tokens[:-1]:
        target = target[int(token)] if isinstance(target, list) else target[token]
    target[tokens[-1]] = value
    path = tmp_path / MATRIX.name
    for evidence in matrix["evidence_files"]:
        name = evidence["path"]
        if "/" not in name:
            shutil.copyfile(MATRIX.parent / name, tmp_path / name)
    path.write_text(json.dumps(matrix), encoding="utf-8")
    with pytest.raises(ValueError):
        read_control_matrix(path)


def test_reader_binds_exact_evidence_bytes_and_optional_matrix_hash(tmp_path: Path) -> None:
    matrix = read_control_matrix(MATRIX)
    expected = hashlib.sha256(MATRIX.read_bytes()).hexdigest()
    assert read_control_matrix(MATRIX, expected_sha256=expected) == matrix
    with pytest.raises(ValueError, match="Matrisehash"):
        read_control_matrix(MATRIX, expected_sha256="0" * 64)
    path = tmp_path / MATRIX.name
    shutil.copyfile(MATRIX, path)
    for evidence in matrix["evidence_files"]:
        shutil.copyfile(MATRIX.parent / evidence["path"], tmp_path / evidence["path"])
    changed = tmp_path / "precision-summary.json"
    changed.write_bytes(changed.read_bytes().replace(b"2024", b"2025", 1))
    with pytest.raises(ValueError, match="Bevishash"):
        read_control_matrix(path)


def test_cli_validates_without_workbook_database_or_network(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "analyse.control_matrix", str(MATRIX)],
        cwd=MATRIX.parents[4],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["activation"] == "NONE"
    missing = subprocess.run(
        [sys.executable, "-m", "analyse.control_matrix", str(tmp_path / "missing.json")],
        cwd=MATRIX.parents[4],
        capture_output=True,
        text=True,
        check=False,
    )
    assert missing.returncode == 1
    assert json.loads(missing.stdout)["status"] == "invalid"


@pytest.mark.parametrize("change", ["replace", "remove"])
@pytest.mark.parametrize("bind_hash", [False, True])
def test_cli_reports_hash_of_bounded_validated_bytes_when_matrix_path_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    change: str,
    bind_hash: bool,
) -> None:
    path = _write_matrix(tmp_path, read_control_matrix(MATRIX))
    shutil.copyfile(MATRIX, path)
    expected_sha256 = "8bf8f9395881593d222884744c974ce2c7023099cdca65b92cc6886ebedacdc5"
    arguments = ["control-matrix", str(path)]
    if bind_hash:
        arguments.extend(["--sha256", expected_sha256])
    monkeypatch.setattr(sys, "argv", arguments)
    reads: list[int] = []
    original_open = Path.open

    def recording_open(file: Path, *args: Any, **kwargs: Any) -> Any:
        stream = original_open(file, *args, **kwargs)
        mode = args[0] if args else kwargs.get("mode", "r")
        if file == path and mode == "rb":
            original_read = stream.read

            def recording_read(size: int = -1) -> Any:
                reads.append(size)
                return original_read(size)

            stream.read = recording_read
        elif file == tmp_path / "stage-residuals.json":
            # The matrix stream has closed; validation continues from its received bytes.
            if change == "replace":
                path.write_bytes(b'{"unvalidated": true}')
            else:
                path.unlink()
        return stream

    monkeypatch.setattr(Path, "open", recording_open)
    assert main() == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "valid"
    assert result["sha256"] == expected_sha256
    assert reads == [2 * 1024 * 1024 + 1]


def test_cli_reports_matrix_read_failure_without_valid_result_or_exception(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["control-matrix", str(MATRIX)])
    original_open = Path.open

    def failing_open(file: Path, *args: Any, **kwargs: Any) -> Any:
        stream = original_open(file, *args, **kwargs)
        if file == MATRIX:

            def failing_read(size: int = -1) -> Any:
                raise OSError("matrix read failed")

            stream.read = failing_read
        return stream

    monkeypatch.setattr(Path, "open", failing_open)
    assert main() == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {"status": "invalid", "error": "matrix read failed"}
    assert captured.err == ""


def _evidence(name: str) -> Any:
    return json.loads((MATRIX.parent / name).read_text(encoding="utf-8"))


def test_all_precision_strata_and_representative_raw_residuals_are_preserved() -> None:
    h = _evidence("precision-summary.json")
    assert sum(h["baseline"].values()) == 1694
    assert h["baseline"] == {
        "exact": 847,
        "fractional": 726,
        "excel_only": 120,
        "reference_only": 1,
    }
    assert sum(h["fractional"]["abs_histogram"].values()) == 726
    assert sum(h["fractional"]["signs"].values()) == 726
    assert h["individual"]["noninteger_cells"] == 787
    assert h["cancellation"]["noninteger_cells_in_exact_keys"] == 4
    assert sum(h["classification"]["categories"].values()) == 120
    assert sorted(h["classification"]["categories"].values()) == [1, 16, 39, 64]
    assert h["rounding_experiment"]["common_aggregate_matches"] == 1573
    # Literal original lexemes and independent Blå bok amounts from PDF p. 74/72.
    assert Decimal("336484.23200000002") * 1_000_000 - 336_484_232_000 == Decimal(".00002")
    assert Decimal("170591.75599999999") * 1_000_000 - 170_591_756_000 == Decimal("-.00001")


def test_salary_and_stage_diagnostics_do_not_turn_zero_sum_into_proof() -> None:
    e = _evidence("stages-evidence.json")
    salary = e["salary_source"]
    assert (salary["positive_account_rows"], salary["negative_key"]) == (165, ["2309", "1"])
    assert Decimal(salary["positive_sum_nok"]) == 2_620_361_000
    assert Decimal(salary["positive_sum_nok"]) + Decimal(salary["negative_amount_nok"]) == 0
    assert e["column_distributions"]["M"]["zero"] == 1871
    assert e["identities"]["J_minus_H_minus_K"]["exact"] == 1654
    assert e["identities"]["J_minus_H_minus_K"]["nonzero_residuals"] == 217
    assert e["identities"]["K_minus_I"]["residual_count"] == 71
    n = e["comparisons"]["N_nysald_candidate"]
    assert n["excel_nonzero_keys"] == 737
    assert n["statuses"]["exact"] + n["statuses"]["nonzero_residual"] == 738
    assert n["statuses"]["nonzero_residual"] == 229
    assert e["comparisons"]["L_other"]["statuses"]["exact"] == 4


def test_six_material_residuals_have_distinct_proposal_and_adopted_source_fields() -> None:
    e = _evidence("stage-residuals.json")
    dispositions = e["dispositions"]
    assert {"/".join(x["key"]) for x in dispositions} == {
        "118/70",
        "1420/32",
        "150/70",
        "315/78",
        "5800/50",
        "732/70",
    }
    for rest in dispositions:
        account = "/".join(rest["key"])
        fields = [f for f in e["fields"] if f.get("account") == account]
        assert any(f["role"] == "adopted_decision" for f in fields)
        addition = Decimal(rest["committee_addition_nok"])
        raw_sum = sum(sum(Decimal(row[c]) for c in "KLN") for row in rest["raw_inputs"]) * 1_000_000
        assert raw_sum - Decimal(rest["doc"]) == Decimal(rest["residual_nok"])
        expected_precision = Decimal("-0.0000005") if account == "5800/50" else Decimal(0)
        assert Decimal(rest["residual_nok"]) + addition == expected_precision
        assert rest["classification"] == "proposal_vs_adopted_committee_addition"
    expenses = [r for r in dispositions if r["key"] != ["5800", "50"]]
    assert sum(Decimal(r["committee_addition_nok"]) for r in expenses) == 600_000_000
    assert len([f for f in e["fields"] if f["role"] == "adopted_decision"]) == 6


def test_public_fixture_replay_keeps_v2_boundaries_and_all_2894_observations(
    tmp_path: Path,
) -> None:
    from innlesning import extract_revision, read_extraction, read_sync, sync_saved
    from innlesning.observations import Interpretation

    evidence = _evidence("decisions-evidence.json")
    repo = MATRIX.parents[4]
    controls = json.loads(
        (MATRIX.parent.parent / "pilotkontroll/kontrollgrunnlag.json").read_text(encoding="utf-8")
    )
    database = tmp_path / "bounded.sqlite"
    observed = []
    for source in controls["sources"]:
        fixture = repo / source["fixture"]
        raw = fixture.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source["sha256"]
        metadata = json.loads(fixture.with_suffix(".json").read_text(encoding="utf-8"))
        job = sync_saved(database, raw, metadata, historical_sample=True, decision_id=source["id"])
        revision = read_sync(database, job).entries[0].revision_id
        interpretation = Interpretation(adapter_version="storting-belop-v2")
        assert interpretation.id == controls["adapter_interpretation_id"]
        out = extract_revision(database, revision, interpretation=interpretation)
        assert out == read_extraction(database, out.id)
        assert out == extract_revision(database, revision, interpretation=interpretation)
        assert len(out.observations) == source["count"]
        observed.extend(out.observations)
    assert len(observed) == 2894
    for future in evidence["future_adapter_expectations"]:
        current = [
            o
            for o in observed
            if o.api_id == future["api_id"] and [o.chapter, o.post] == future["account"]
        ]
        assert len(current) == future["v2_expected_count_for_account"]
        if current:
            assert current[0].meaning == "uavklart"
            assert current[0].amount_kr == 30_000_000
            assert current[0].pointer.locator == "table[1]/tr[143]/td[5]"
        assert future["implemented"] is False
        assert future["before_observation"] is None and future["after_observation"] is None

    # Six internally consistent source transitions retain three cross-event conflicts.
    def amount(api: str, chapter: str, meaning: str) -> int:
        return next(
            o.amount_kr
            for o in observed
            if o.api_id == api and o.chapter == chapter and o.meaning == meaning
        )

    for chapter, first, second in [
        ("1860", "40034064", "40034226"),
        ("4860", "40034064", "40034226"),
        ("5999", "40033719", "40034287"),
    ]:
        for api in (first, second):
            assert amount(api, chapter, "for_belop") + amount(api, chapter, "endring") == amount(
                api, chapter, "etter_belop"
            )
        assert amount(first, chapter, "etter_belop") != amount(second, chapter, "for_belop")
    assert len(evidence["rest_classification"]) == 5
