"""Lag en syntetisk kompatibilitetsfixture med den uendrede B8-skriveren."""

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict, replace
from pathlib import Path
from types import ModuleType

from analyse.saksdokumenter import report_from_json, report_to_json
from innlesning.observations import identity

BASE = "a7fc7d9996733dcaa73589c2fa8a3906059b4413"


def fingerprint(raw: bytes) -> dict[str, str | int]:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frozen_json", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    original = args.frozen_json.read_bytes()
    if args.frozen_json.suffix == ".gz":
        original = gzip.decompress(original)
    report = report_from_json(original.decode("utf-8"))
    rows = tuple(
        replace(
            row,
            observation=replace(
                row.observation,
                pointer=replace(row.observation.pointer, raw_record="syntetisk raatekst " * 2500),
            ),
        )
        for row in report.base.rows
        if row.observation.post == "1"
    )
    if not rows:
        raise ValueError("Prøven krever det eksisterende 210-snapshotets post 1")
    report = replace(
        report, base=replace(report.base, rows=rows, unfiltered_rows=rows, issues=()), id=""
    )
    report = replace(report, id=identity("b6-frozen-2", asdict(report)))
    frozen = report_to_json(report).encode("utf-8")
    source = subprocess.run(
        ["git", "show", f"{BASE}:analyse/saksdokumenter.py"],
        check=True,
        capture_output=True,
    ).stdout
    # Hele originalmodulen kjøres uendret; ingen omdøping av en ny B9-arbeidsbok.
    legacy = ModuleType("analyse._b8_fixture_original")
    legacy.__package__ = "analyse"
    sys.modules[legacy.__name__] = legacy
    exec(compile(source, f"{BASE}:analyse/saksdokumenter.py", "exec"), legacy.__dict__)
    old_report = legacy.report_from_json(frozen.decode("utf-8"))
    args.output_directory.mkdir(parents=True, exist_ok=False)
    output = args.output_directory / "legacy-b8.xlsx"
    absent_database = args.output_directory / "unavailable.sqlite"
    legacy.export_built_saks_excel(absent_database, old_report, output)
    legacy.verify_saks_excel(output, old_report)
    assert not absent_database.exists()
    compressed = gzip.compress(frozen, mtime=0)
    (args.output_directory / "legacy-b8.json.gz").write_bytes(compressed)
    metadata = {
        "fixture_kind": "synthetic_original_b8_writer",
        "base_commit": BASE,
        "writer_source": "analyse/saksdokumenter.py",
        "writer_source_sha256": hashlib.sha256(source).hexdigest(),
        "original_writer_and_verifier_passed": True,
        "source_snapshot": fingerprint(original),
        "format": "b6-frozen-2",
        "report_id": report.id,
        "synthetic_raw_record": {"text": "syntetisk raatekst ", "repeat": 2500},
        "xlsx": fingerprint(output.read_bytes()),
        "compressed_json": fingerprint(compressed),
        "uncompressed_json": fingerprint(frozen),
    }
    (args.output_directory / "legacy-b8.manifest.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()
