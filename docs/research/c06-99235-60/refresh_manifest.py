"""Bind the reviewed local delivery files; excludes itself only as a manifest target."""

import hashlib
import json
from pathlib import Path

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[2]


def main():
    paths = {
        path
        for path in PACK.rglob("*")
        if path.is_file()
        and path.name != "delivery-manifest.json"
        and not {"reviews", "__pycache__"}.intersection(path.relative_to(PACK).parts)
    }
    paths.update((ROOT / "AGENTS.md", ROOT / "docs/kildefunn.md"))
    rows = []
    for path in sorted(paths):
        data = path.read_bytes()
        representation = "exact_file_bytes"
        if not path.is_relative_to(PACK):
            data = data.replace(b"\r\n", b"\n")
            representation = "utf-8-lf"
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "representation": representation,
            }
        )
    manifest = {
        "schema": "c06-delivery-manifest-1",
        "base_commit": "49cc6e44851cf74e0aaea4eb333419e5598bfd95",
        "rule": (
            "All builder files and administrative issue assessment, plus two additive pointers. "
            "Manifest itself, Python caches and later independent reviews/** are excluded. "
            "No claim of commit, publication, independent review, CI or merge."
        ),
        "files": rows,
        "file_count": len(rows),
        "total_bytes": sum(row["bytes"] for row in rows),
    }
    (PACK / "delivery-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"files": len(rows), "bytes": manifest["total_bytes"]}))


if __name__ == "__main__":
    main()
