"""Rebuild the small exact-history bundle from locally available fixed Git objects."""

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CANDIDATE = "9efa1f7b67e4ad5b2722b6a6604591af281e4e9c"
PUBLISHED = "92b43c2ce7ec350e10639bd0c75540da0d83ee72"
BASE = "49cc6e44851cf74e0aaea4eb333419e5598bfd95"
REF = "refs/c06-history/candidates"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main() -> None:
    expected = {
        "9eb27cebf7ca4a99aeb30fa32245e41314e0d295": (
            "60dfabaec4e7c022e30c6a6389a622790fad11f5",
            BASE,
        ),
        "d241ad8f36f70718dbc54d3093c151d301d04f30": (
            "afd35a9f4bf98c8b2e69bd3373464a9661811b7b",
            "9eb27cebf7ca4a99aeb30fa32245e41314e0d295",
        ),
        CANDIDATE: (
            "4664149a1cbf6c288b741fa502e162746b032e07",
            "d241ad8f36f70718dbc54d3093c151d301d04f30",
        ),
        PUBLISHED: ("4664149a1cbf6c288b741fa502e162746b032e07", BASE),
    }
    for commit, (tree, parent) in expected.items():
        assert git("show", "-s", "--format=%T %P", commit).decode().strip() == tree + " " + parent
    existing = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", REF], cwd=ROOT, check=False
    )
    assert existing.returncode in (0, 1)
    created = existing.returncode == 1
    if created:
        git("update-ref", REF, CANDIDATE, "0" * 40)
    else:
        assert git("rev-parse", REF).decode().strip() == CANDIDATE
    bundle = HERE / "candidates.bundle"
    relative_bundle = bundle.relative_to(ROOT).as_posix()
    try:
        git(
            "bundle",
            "create",
            relative_bundle,
            REF,
            "^" + PUBLISHED,
            "^" + PUBLISHED + "^{tree}",
        )
    finally:
        if created:
            git("update-ref", "-d", REF, CANDIDATE)
    header, pack = bundle.read_bytes().split(b"\n\n", 1)
    lines = header.splitlines()
    assert lines[0] == b"# v2 git bundle"
    assert lines[1].startswith(("-" + BASE + " ").encode())
    assert lines[2] == (CANDIDATE + " " + REF).encode()
    # Native Git records the ancestry boundary, BASE. The explicit excluded
    # published tree also supplies shared objects, so declare its commit too.
    lines.insert(2, ("-" + PUBLISHED + " Published C06 tree prerequisite").encode())
    data = b"\n".join(lines) + b"\n\n" + pack
    assert len(data) < 100_000
    bundle.write_bytes(data)
    verification = git("bundle", "verify", relative_bundle).decode()
    print(
        json.dumps(
            {
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "pack_sha256": hashlib.sha256(pack).hexdigest(),
                "native_pack_bytes_preserved": True,
                "prerequisites": [BASE, PUBLISHED],
                "head": {REF: CANDIDATE},
                "verification": verification,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
