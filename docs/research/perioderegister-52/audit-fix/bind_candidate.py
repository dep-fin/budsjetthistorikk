"""Bind this additive correction to final code, checks and actual test files."""

import hashlib
import json
import subprocess
from pathlib import Path
from xml.etree import ElementTree


def record(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return dict(path=path.as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main() -> None:
    root = Path(__file__).parent
    output = root / "candidate.json"
    if output.exists():
        raise FileExistsError(output)
    previous = json.loads((root.parent / "candidate-code.json").read_text("utf8"))
    code = []
    replaced = []
    for old in previous["files"]:
        current = record(Path(old["file"]))
        code.append(current)
        if current["sha256"] != old["sha256"]:
            replaced.append(
                dict(
                    path=old["file"],
                    original_sha256=old["sha256"],
                    replacement_sha256=current["sha256"],
                )
            )
    assert {row["path"] for row in replaced} == {
        "analyse/perioderegister_excel.py",
        "tests/test_perioderegister.py",
    }
    before = json.loads((root / "before.json").read_text("utf8"))
    after = json.loads((root / "after.json").read_text("utf8"))
    assert before["preserved_sha256"] == after["preserved_sha256"]
    for name, sha256 in after["preserved_sha256"].items():
        assert record(Path(name))["sha256"] == sha256, name
    summaries = {}
    for path in root.glob("*.xml"):
        suite = ElementTree.parse(path).getroot()[0]
        summaries[path.stem] = {
            key: suite.get(key) for key in ("tests", "errors", "failures", "skipped", "time")
        }
    assert summaries["targeted"]["tests"] == "31"
    assert summaries["targeted"]["errors"] == summaries["targeted"]["failures"] == "0"
    assert all(row["status"] == "REJECTED" for row in after["results"])
    assert len(after["positive_checks"]) == 5 and not after["forbidden_calls"]
    files = sorted(p for p in root.rglob("*") if p.is_file() and p != output)
    test_files = sorted(
        p
        for p in Path(".local/p1-audit-fix-targeted").rglob("*")
        if p.is_file() and p.suffix in {".xlsx", ".json"}
    )
    payload = dict(
        base=previous["base"],
        original_candidate="4413a5f21be71ccd2ad5c885560da6bae2e8b885",
        original_tree="afc1eacfa74cec19e35a5cb49ee5907be5bfc877",
        head=subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        stage="uncommitted additive audit correction; no Git/GitHub mutations",
        replacement_code=replaced,
        complete_executable_binding=code,
        control_summary=summaries,
        original_evidence_preserved=len(after["preserved_sha256"]),
        files=[record(p) for p in files],
        actual_targeted_test_files=[record(p) for p in test_files],
        attributes=record(Path(".gitattributes")),
        full_suite_rerun=False,
        linux_ci_run=False,
        native_excel_run=False,
    )
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(
        json.dumps(
            dict(
                replacements=len(replaced),
                preserved_files=payload["original_evidence_preserved"],
                tests=summaries["targeted"],
                evidence_files=len(files),
                actual_test_files=len(test_files),
            )
        )
    )


if __name__ == "__main__":
    main()
