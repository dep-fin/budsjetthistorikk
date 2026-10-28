"""Lesekontroller for Standards-review; skriver bare i egen reviewkatalog."""

from __future__ import annotations

import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RESEARCH = HERE.parents[1]
BASE = "6b2441ee5e859d103ab44d78f12d33c374a89171"
CANDIDATE = "7af3153bda95726ac93d0780b918ae95440bae2d"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_text("utf-8"))


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, key
        result[key] = value
    return result


def main() -> None:
    assert git("rev-parse", "HEAD").decode().strip() == CANDIDATE
    assert git("merge-base", BASE, CANDIDATE).decode().strip() == BASE
    names = git("diff", "--name-only", BASE + "..." + CANDIDATE).decode().splitlines()
    assert len(names) == 64
    inventory = []
    for name in names:
        blob = git("show", CANDIDATE + ":" + name)
        actual = (ROOT / name).read_bytes()
        equal = actual == blob
        if name in {"AGENTS.md", "docs/kildefunn.md"}:
            assert actual.replace(b"\r\n", b"\n") == blob
        else:
            assert equal, name
        entry = {
            "path": name,
            "git_blob_sha256": digest(blob),
            "git_blob_bytes": len(blob),
            "checkout_byteidentical": equal,
        }
        if name.endswith(".json"):
            parsed = json.loads(blob, object_pairs_hook=unique_pairs)
            entry["json_top_level"] = list(parsed) if isinstance(parsed, dict) else "list"
        if name.endswith(".gz"):
            raw = gzip.decompress(blob)
            entry["body_bytes"] = len(raw)
            entry["body_sha256"] = digest(raw)
        inventory.append(entry)

    # Kjør publisert kontrollkode uten å endre kildekontrollørens filer.
    source_script = RESEARCH / "reviews/source-control/verify_sources.py"
    spec = importlib.util.spec_from_file_location("r2_source_review", source_script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source_out = HERE / "source-recheck"
    source_out.mkdir(exist_ok=True)
    module.HERE = source_out
    previous_argv = sys.argv
    sys.argv = [str(source_script), "--raw-root", str(RESEARCH / "originals")]
    try:
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            module.main()
    finally:
        sys.argv = previous_argv
    source_result = load(source_out / "results.json")
    published_result = load(RESEARCH / "reviews/source-control/results.json")
    stable_keys = [
        "base",
        "source_bindings",
        "passages",
        "checks",
        "script_sha256",
        "context_source_bindings",
        "unchanged_pins",
        "pdf_pages",
        "summary",
        "annex4_structure",
        "june_date_conflict",
    ]
    for key in stable_keys:
        assert source_result[key] == published_result[key], key

    # Kjør den dokumenterte kommandoen direkte fra den publiserte Markdown-blokken.
    text = (RESEARCH / "reproduksjon.md").read_text("utf-8")
    code = text.split("```python\n", 1)[1].split("\n```", 1)[0]
    previous_argv = sys.argv
    sys.argv = ["published-reproduction", CANDIDATE]
    try:
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            exec(compile(code, "reproduksjon.md:python", "exec"), {})
    finally:
        sys.argv = previous_argv
    reproduction = json.loads(captured.getvalue())
    (HERE / "reproduction-results.json").write_text(
        json.dumps(reproduction, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    tooling = []
    for command in [
        [sys.executable, "-m", "ruff", "check", "--no-cache", str(source_script)],
        [sys.executable, "-m", "ruff", "format", "--check", "--no-cache", str(source_script)],
        ["git", "diff", "--check", BASE + "..." + CANDIDATE],
    ]:
        run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        tooling.append(
            {
                "command": command,
                "exit_code": run.returncode,
                "stdout": run.stdout,
                "stderr": run.stderr,
            }
        )
        assert run.returncode == 0, tooling[-1]

    result = {
        "schema": "r2-standards-review-checks-1",
        "checked_utc": datetime.now(UTC).isoformat(),
        "base_commit": BASE,
        "candidate_commit": CANDIDATE,
        "commits": git("log", BASE + ".." + CANDIDATE, "--oneline").decode().splitlines(),
        "changed_files": inventory,
        "source_control_recheck": source_result["summary"],
        "source_control_published_stable_fields_match": stable_keys,
        "reproduction": reproduction,
        "tooling": tooling,
        "review_script_sha256": digest(Path(__file__).read_bytes()),
        "boundary": (
            "Offline dokument-, kilde- og standardkontroll. "
            "Ingen ny HTTP, produktadopsjon, full CI eller merge."
        ),
    }
    (HERE / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "files": len(inventory),
                "source_checks": source_result["summary"],
                "reproduction_checks": reproduction["total_checks"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
