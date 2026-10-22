"""Avled fullmaktsvedtak 211 byteidentisk fra en eksplisitt lokal HTTP-original."""

import argparse
import hashlib
import json
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("metadata", type=Path)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    meta = json.loads(args.metadata.read_text("utf-8"))
    assert hashlib.sha256(raw).hexdigest() == meta["sha256"]
    assert len(raw) == meta["bytes"]
    nodes = list(re.finditer(rb"    <stortingsvedtak>.*?</stortingsvedtak>", raw, re.S))
    selected = next(n for n in nodes if b"<id>40034049</id>" in n.group())
    source = raw[: nodes[0].start()] + selected.group() + raw[nodes[-1].end() :]
    output = Path(__file__).parent / "fixtures/b8/40034049.xml"
    output.write_bytes(source)
    metadata = {
        "url": meta["url"],
        "retrieved_utc": meta["fetched_utc"],
        "status": meta["status"],
        "fixture_kind": "derived_excerpt",
        "session_coverage": "partial",
        "source_response_sha256": meta["sha256"],
        "source_response_bytes": meta["bytes"],
        "sha256": hashlib.sha256(source).hexdigest(),
        "bytes": len(source),
        "decision_id": "40034049",
        "object_start_byte_0": selected.start(),
        "object_bytes": len(selected.group()),
        "extraction": "Original byteprefix + ett komplett byteidentisk vedtaksobjekt + suffix",
        "provenance": "tests/create_b8_fixtures.py; kildekontroll for B8/#28",
    }
    output.with_suffix(".json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()
