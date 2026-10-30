"""Verify audit exports, historical byte bindings and explicit resource edges.

Run as a module from the repo root, with --audit pointing at audit_checks output.
"""

import argparse
import base64
import hashlib
import json
import subprocess
from dataclasses import replace
from pathlib import Path

from analyse import innstilling95 as t6
from analyse.omtale import report_from_json as omtale
from analyse.visningspilot import source_input


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    report = t6.read_json(Path(".local/full-acceptance/t6-files0/tomt.json"))
    old = omtale(report.basis.t5_basis.t1_basis.o2b_json)
    entries = [("t1/" + s.name, s) for s in report.basis.t5_basis.t1_basis.sources]
    entries += [("o2b/" + s.name, s) for s in old.basis.sources]
    entries += [(s.name, s) for s in report.basis.sources]
    entries += [("t5/" + s.name, s) for s in report.basis.t5_basis.sources]
    rows = []
    for name, source in entries:
        if source.content_base64 is None:
            continue
        data = base64.b64decode(source.content_base64, validate=True)
        assert (args.audit / "originals" / name).read_bytes() == data
        assert sha(data) == source.sha256
        rows.append({"path": name, "bytes": len(data), "sha256": source.sha256})
    assert len(rows) == 35
    local = json.loads(
        Path("docs/research/innstilling95-64/local-candidate.json").read_text("utf8")
    )
    checks = []
    for row in local["files"]:
        path = Path(row["path"])
        raw = path.read_bytes()
        blob = (
            subprocess.check_output(["git", "hash-object", "--path=" + row["path"], row["path"]])
            .decode()
            .strip()
        )
        assert len(raw) == row["bytes"]
        assert sha(raw) == row["sha256_raw"]
        # The fixture is binary. Its manifest intentionally has no LF hash.
        if row["sha256_lf"] is not None:
            assert sha(raw.replace(b"\r\n", b"\n")) == row["sha256_lf"]
        assert blob == row["git_filtered_blob"]
        checks.append(
            {
                "path": row["path"],
                "bytes": len(raw),
                "sha256_raw": row["sha256_raw"],
                "sha256_lf": row["sha256_lf"],
                "git_filtered_blob": blob,
            }
        )
    prepared = source_input(report.basis.t5_basis.t1_basis.o2b_json)
    boundary_results = []
    old = report.basis.t5_basis.t1_basis
    for field, limit in (
        ("sources", 64),
        ("documents", 16),
        ("inventory", 4096),
        ("statements", 1024),
        ("observations", 512),
        ("relations", 4096),
    ):
        old_count = len(getattr(old, field))
        if field in {"sources", "observations"}:
            old_count += len(getattr(report.basis.t5_basis, field))
        if field == "sources":
            old_count += len(prepared.basis.sources)
        values = getattr(report.basis, field)
        for extra, expect_resource in ((0, False), (1, True)):
            candidate = replace(report.basis, **{field: (values[0],) * (limit + extra - old_count)})
            try:
                t6.validate_basis(candidate)
            except ValueError as error:
                assert ("ressursprofil" in str(error)) == expect_resource
                boundary_results.append(
                    {
                        "field": field,
                        "union_count": limit + extra,
                        "resource_gate_rejected": expect_resource,
                        "message": str(error),
                    }
                )
            else:
                raise AssertionError("Synthetic repeated objects must fail reconstruction")
    product_files = (
        "analyse/innstilling95.py",
        "analyse/innstilling95_excel.py",
        "innlesning/innstilling95.py",
        "innlesning/innstilling95_model.py",
        "ops/innstilling95_proeve.py",
        "tests/test_innstilling95.py",
    )
    bindings = []
    for name in product_files:
        data = Path(name).read_bytes()
        bindings.append(
            {
                "path": name,
                "bytes": len(data),
                "sha256_raw": sha(data),
                "sha256_lf": sha(data.replace(b"\r\n", b"\n")),
                "git_blob": subprocess.check_output(["git", "rev-parse", "HEAD:" + name])
                .decode()
                .strip(),
            }
        )
    result = {
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
        "tree": subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"]).decode().strip(),
        "raw_originals": rows,
        "local_candidate_bindings": checks,
        "resource_edges": boundary_results,
        "product_bindings": bindings,
        "count_raw_originals": len(rows),
        "count_manifest_bindings": len(checks),
    }
    with (args.audit / "supplement.json").open("x", encoding="utf8", newline="\n") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "raw_originals": len(rows),
                "candidate_bindings": len(checks),
                "resource_edges": len(boundary_results),
                "status": "passed",
            }
        )
    )


if __name__ == "__main__":
    main()
