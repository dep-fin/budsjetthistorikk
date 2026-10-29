"""Uavhengige filidentiteter: ny P2 mot autentiske P1/T4/T1 og uendret produktbase."""

import argparse
import gzip
import hashlib
import json
import subprocess
from pathlib import Path

from analyse import fleraarspilot as t4
from analyse import perioderegister as p1
from analyse import perioderegister_r2 as p2
from analyse.komitepilot import legacy_payloads, legacy_report
from innlesning.perioderegister_r2 import shared_sources


def binding(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {
        "path": str(path.resolve()),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--previous-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    previous = args.previous_root
    files = [
        args.new,
        previous / "outputs/p1-52-973db1f/p1-1429-2024.json",
        previous / "outputs/t4-48-3f856d8/2024-both.json",
        previous / "outputs/t1-41-608895f/begge.json",
    ]
    before = [binding(p) for p in files]
    new, old, earlier = p2.read_json(files[0]), p1.read_json(files[1]), t4.read_json(files[2])
    assert new.basis.p1_basis == old.basis
    assert new.basis.p1_basis.t4_basis == earlier.basis
    assert new.basis.p1_basis.t4_basis.legacy_json == files[3].read_text("utf8")
    fixture = Path("tests/fixtures/t2/authentic-t1.json.gz")
    assert gzip.decompress(fixture.read_bytes()).decode() == new.basis.p1_basis.t4_basis.legacy_json
    assert p2.contents(new.basis).observations == p1.contents(old.basis).observations
    for selection in (new.selection,):
        expected = p1.build_report(old.basis, selection)
        assert new.view.p1 == expected.view and new.calculations == expected.calculations
    legacy = legacy_payloads(old.basis.t4_basis.legacy_json)
    prior = legacy_report(old.basis.t4_basis.legacy_json)
    shared = shared_sources(old.basis, legacy, prior.basis if prior else None)
    old_digests = {hashlib.sha256(raw).hexdigest() for _, raw, _ in shared.values()}
    assert not old_digests.intersection(p.id for p in new.basis.payloads)
    protected = subprocess.check_output(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            "c041ad8",
            "innlesning",
            "analyse",
            "drift",
            "tests",
            "docs/research/k3-arsinventar-50",
            "docs/research/perioderegister-52",
            "docs/research/r2-101000-54",
            ".github",
            "requirements.txt",
            "requirements-dev.txt",
            "pyproject.toml",
        ],
        text=True,
    ).splitlines()
    unchanged = subprocess.run(
        ["git", "diff", "--exit-code", "c041ad8", "--", *protected],
        capture_output=True,
        text=True,
        check=False,
    )
    assert unchanged.returncode == 0, unchanged.stdout + unchanged.stderr
    after = [binding(p) for p in files]
    assert before == after
    result = {
        "files": before,
        "p1_basis_byte_semantics_equal": old.basis.id,
        "t4_basis_equal": earlier.basis.id,
        "literal_t1_bytes_sha256": hashlib.sha256(
            new.basis.p1_basis.t4_basis.legacy_json.encode()
        ).hexdigest(),
        "old_observations_equal": len(p1.contents(old.basis).observations),
        "old_document_ids": [d.id for d in p1.contents(old.basis).documents],
        "protected_old_files_unchanged": len(protected),
        "old_unique_raw_digests": len(old_digests),
        "new_payloads": len(new.basis.payloads),
        "new_unique_payload_digests": len({p.id for p in new.basis.payloads}),
        "new_physical_raw_payloads": sum(p.content_base64 is not None for p in new.basis.payloads),
        "new_old_raw_digest_overlap": 0,
        "inherited_immutable_duplication": "bevart uendret i de eksakte gamle kapslene",
        "errors": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps({"protected_old_files": len(protected), "old_basis_equal": True, "errors": 0}))


if __name__ == "__main__":
    main()
