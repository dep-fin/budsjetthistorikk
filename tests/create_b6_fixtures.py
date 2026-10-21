"""Avled komplette B6-objekter byteidentisk fra bevart 2024–2025-respons."""

import hashlib
import json
import re
import sys
from pathlib import Path

from create_b3_fixtures import PARENTS


def main() -> None:
    raw = Path(sys.argv[1]).read_bytes()
    digest, size, time, _ = PARENTS["2024-2025"]
    if hashlib.sha256(raw).hexdigest() != digest or len(raw) != size:
        raise ValueError("Foreldrekildens hash/byteantall stemmer ikke")
    marker = b"  <stortingsvedtak_liste>\r\n"
    prefix = raw[: raw.index(marker) + len(marker)]
    suffix = raw[raw.rindex(b"  </stortingsvedtak_liste>") :]
    directory = Path(__file__).parent / "fixtures/b6"
    directory.mkdir(exist_ok=True)
    for identifier in ("40034048", "40034229"):
        match = re.search(
            rb"    <stortingsvedtak>\r\n      <id>"
            + identifier.encode()
            + rb"</id>.*?</stortingsvedtak>\r\n",
            raw,
            re.DOTALL,
        )
        if match is None:
            raise ValueError("Påkrevd vedtaks-ID mangler")
        derived = prefix + match.group() + suffix
        (directory / f"{identifier}.xml").write_bytes(derived)
        metadata = {
            "url": "https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025",
            "retrieved_utc": f"2026-10-20T{time}+00:00",
            "status": 200,
            "headers": {"Content-Type": "text/xml; charset=utf-8"},
            "fixture_kind": "derived_excerpt",
            "session_coverage": "partial",
            "source_response_sha256": digest,
            "source_response_bytes": size,
            "sha256": hashlib.sha256(derived).hexdigest(),
            "bytes": len(derived),
            "decision_id": identifier,
            "object_start_byte_0": match.start(),
            "object_bytes": len(match.group()),
            "extraction": "Original byteprefix + ett komplett byteidentisk vedtaksobjekt + suffix",
            "provenance": (
                "docs/research/issue-2/aar/input_manifest.json; tests/create_b6_fixtures.py"
            ),
        }
        (directory / f"{identifier}.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
