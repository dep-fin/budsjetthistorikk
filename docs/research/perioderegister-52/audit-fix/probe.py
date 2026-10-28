"""Reproduce the two exact audit files without altering their original evidence."""

import argparse
import hashlib
import json
import socket
import sqlite3
from pathlib import Path
from unittest.mock import patch

from analyse.perioderegister import read_json
from analyse.perioderegister_excel import read_excel


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("before", "after"))
    args = parser.parse_args()
    output = Path(__file__).parent / (args.phase + ".json")
    if output.exists():
        raise FileExistsError(output)
    audit = Path(".local/p1-file-audit")
    reference = read_json(audit / "inputs/p1-complete/both.json")
    results = []
    positive_checks = []
    calls = []

    def forbidden(*values, **kwargs):
        calls.append(repr(values))
        raise AssertionError("Network/SQLite forbidden")

    with (
        patch.object(socket, "create_connection", forbidden),
        patch.object(socket.socket, "connect", forbidden),
        patch.object(socket.socket, "connect_ex", forbidden),
        patch.object(sqlite3, "connect", forbidden),
    ):
        for name, expected_digest in (
            (
                "root-external-office-document",
                "929615ec56df384b1113fe57351d26948d8ae52b242fa4bc429537756a981a68",
            ),
            (
                "apply-alignment-zero",
                "c10c3fa0f85ee0d501785d0ccfb5ec990c1aaff76d989baf258e8692dc7140a7",
            ),
        ):
            path = audit / "synthetic" / ("container-" + name + ".xlsx")
            assert digest(path) == expected_digest
            try:
                actual = read_excel(path)
            except ValueError as error:
                result = dict(status="REJECTED", error=str(error))
                assert args.phase == "after", result
            else:
                assert args.phase == "before" and actual == reference
                result = dict(status="ACCEPTED", report_equal_reference=True)
            results.append(dict(name=name, sha256=expected_digest, **result))
        if args.phase == "after":
            for path in sorted((audit / "inputs/p1-complete").glob("*.xlsx")):
                frozen = path.with_suffix(".json")
                report = read_json(frozen)
                assert read_excel(path) == report
                counts = (
                    len(report.view.monetary.adopted_observation_ids),
                    len(report.view.monetary.adopted_event_ids),
                )
                assert counts == ((11, 5) if path.stem == "both" else (0, 0))
                globals_ = (
                    len(report.basis.case_candidates),
                    len(report.basis.decision_candidates),
                    len(report.basis.gaps),
                )
                assert globals_ == (67, 25, 7)
                assert report.basis.year_coverage == "partial"
                assert report.basis.professional_annual_balance_approval is False
                positive_checks.append(
                    dict(
                        file=path.as_posix(),
                        sha256=digest(path),
                        frozen_sha256=digest(frozen),
                        monetary_counts=counts,
                        global_counts=globals_,
                        report_id=report.id,
                    )
                )
    assert not calls
    research = Path("docs/research/perioderegister-52")
    preservation = {
        p.as_posix(): digest(p)
        for p in research.rglob("*")
        if p.is_file() and "audit-fix" not in p.parts
    }
    preservation.update(
        {
            p.as_posix(): digest(p)
            for p in (
                audit / "artifact-manifest.json",
                audit / "confirmed-findings.json",
                Path("analyse/omtale_excel_guard.py"),
            )
        }
    )
    if args.phase == "after":
        baseline = json.loads((output.parent / "before.json").read_text("utf8"))
        assert preservation == baseline["preserved_sha256"]
    payload = dict(
        phase=args.phase,
        candidate_commit="4413a5f21be71ccd2ad5c885560da6bae2e8b885",
        results=results,
        positive_checks=positive_checks,
        forbidden_calls=calls,
        preserved_sha256=preservation,
    )
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps(dict(phase=args.phase, results=results, preserved_files=len(preservation))))


if __name__ == "__main__":
    main()
