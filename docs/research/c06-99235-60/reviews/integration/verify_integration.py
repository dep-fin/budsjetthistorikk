"""Bind historical review evidence and check the narrow post-review integration offline."""

import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REVIEWS = HERE.parent
PACK = REVIEWS.parent
ROOT = PACK.parents[2]
CANDIDATE = "9eb27cebf7ca4a99aeb30fa32245e41314e0d295"
ALLOWED = {
    "README.md",
    "OVERLEVERING.md",
    "reproduksjon.md",
    "cross-reference-journal.json",
    "delivery-manifest.json",
    "verification.json",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main() -> None:
    baseline = json.loads((HERE / "original-review-files.json").read_text("utf-8"))
    assert baseline["research_candidate"] == CANDIDATE
    assert (
        git("rev-parse", CANDIDATE + "^{tree}").decode().strip()
        == baseline["research_candidate_tree"]
    )
    old_helper = None
    for row in baseline["files"]:
        path = REVIEWS / row.get("original_copy", row["path"])
        raw = path.read_bytes()
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"], row["path"]
        if "original_copy" in row:
            old_helper = raw
    assert old_helper is not None and len(baseline["files"]) == 15

    helper = REVIEWS / "standards/check_candidate.py"
    assert ast.dump(ast.parse(old_helper)) == ast.dump(ast.parse(helper.read_bytes()))
    spec = importlib.util.spec_from_file_location("c06_standards_integration", helper)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    captures: list[dict[str, Any]] = []

    def capture_write(path: Path, content: str, **kwargs: object) -> int:
        assert path == helper.with_name("candidate-checks.json")
        captures.append(json.loads(content))
        return len(content)

    output = io.StringIO()
    with patch.object(Path, "write_text", capture_write), contextlib.redirect_stdout(output):
        module.main()
    assert len(captures) == 1
    historic = json.loads(helper.with_name("candidate-checks.json").read_text("utf-8"))
    current = captures[0]
    for row in (historic, current):
        row.pop("checked_utc")
    assert current == historic

    prefix = PACK.relative_to(ROOT).as_posix() + "/"
    journal = PACK / "cross-reference-journal.json"
    original = git("show", CANDIDATE + ":" + prefix + journal.name)
    old = "14 nøkkelsider er lest visuelt".encode()
    new = "18 nøkkelsider er lest visuelt".encode()
    assert original.count(old) == 1 and journal.read_bytes() == original.replace(old, new)
    pages = json.loads((PACK / "appendix-reading-journal.json").read_text("utf-8"))["pages"]
    visual = [row["pdf_page_1based"] for row in pages if row["visual_review"]]
    assert len(visual) == 18

    changed = [
        path
        for path in git("diff", "--name-only", CANDIDATE).decode().splitlines()
        if not path.startswith(prefix + "reviews/")
    ]
    assert set(changed) <= {prefix + name for name in ALLOWED}
    tree_rows = git("ls-tree", "-rz", CANDIDATE).split(b"\0")
    bound_files = 0
    for entry in tree_rows:
        if not entry:
            continue
        metadata, encoded_path = entry.split(b"\t", 1)
        path = encoded_path.decode()
        if path.startswith(prefix) and path[len(prefix) :] in ALLOWED:
            continue
        blob = metadata.split()[2].decode()
        raw = (ROOT / path).read_bytes()
        actual = hashlib.sha1(
            b"blob " + str(len(raw)).encode() + b"\0" + raw, usedforsecurity=False
        ).hexdigest()
        if actual != blob:
            actual = git("hash-object", "--path", path, path).decode().strip()
        assert actual == blob, path
        bound_files += 1

    for name in ("README.md", "OVERLEVERING.md", "reproduksjon.md"):
        before = git("show", CANDIDATE + ":" + prefix + name)
        assert (PACK / name).read_bytes().startswith(before), name

    files = []
    for path in sorted(REVIEWS.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path in (HERE / "result.json", HERE / "checks.json"):
            continue
        raw = path.read_bytes()
        files.append(
            {"path": path.relative_to(REVIEWS).as_posix(), "bytes": len(raw), "sha256": sha(raw)}
        )
    result = {
        "schema": "c06-post-review-integration-1",
        "checked_utc": datetime.now(UTC).isoformat(),
        "research_candidate": CANDIDATE,
        "research_candidate_tree": baseline["research_candidate_tree"],
        "base": baseline["base"],
        "historical_review_files_preserved": len(baseline["files"]),
        "standards_helper_identical_ast": True,
        "standards_fixed_candidate_result_identical_except_timestamp": True,
        "standards_helper_stdout": json.loads(output.getvalue()),
        "J02_only_byte_replacement": {"before": old.decode(), "after": new.decode()},
        "unchanged_visual_pages": visual,
        "unchanged_candidate_files": bound_files,
        "changed_research_candidate_paths": changed,
        "review_evidence_files": files,
        "failures": 0,
        "boundary": (
            "Additive working-file integration after the four fixed-9eb reviews. "
            "No original reviewer result/report rewritten. No new independent review, "
            "candidate commit, HTTP, full suite, Linux CI, PR or merge claimed. "
            "The subsequent committed candidate requires a bounded independent recheck."
        ),
    }
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(serialized, encoding="utf-8", newline="\n")
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
