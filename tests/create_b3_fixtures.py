"""Reproduser avledede enkeltobjekter fra hashkontrollerte originalbyte (#2)."""

import hashlib
import json
import re
import sys
from pathlib import Path

PARENTS = {
    "2023-2024": (
        "554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf",
        6816165,
        "11:35:51",
        ("40032850", "40033719", "40033025"),
    ),
    "2024-2025": (
        "9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680",
        7479943,
        "11:36:10",
        (
            "40033805",
            "40034064",
            "40034226",
            "40034287",
            "40034443",
            "40035422",
            "40034385",
            "40035429",
        ),
    ),
}
PARENTS["2025-2026"] = (
    "795afc4202c51a13c4360f1374f3a603aa5d8e803c57195ec48effb60c6aebf6",
    7387302,
    "12:21:14.180591",
    ("40036289",),
)


def main() -> None:
    directory = Path(__file__).parent / "fixtures" / "b3"
    directory.mkdir(exist_ok=True)
    for session, (digest, size, time, identifiers) in PARENTS.items():
        source = Path(sys.argv[1]) / f"vedtak-{session}.xml"
        if session == "2025-2026":
            source = Path(sys.argv[2])
        raw = source.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest and len(raw) == size
        marker = b"  <stortingsvedtak_liste>\r\n"
        prefix = raw[: raw.index(marker) + len(marker)]
        suffix = raw[raw.rindex(b"  </stortingsvedtak_liste>") :]
        for identifier in identifiers:
            match = re.search(
                rb"    <stortingsvedtak>\r\n      <id>"
                + identifier.encode()
                + rb"</id>.*?</stortingsvedtak>\r\n",
                raw,
                re.DOTALL,
            )
            if match is None:
                continue
            derived = prefix + match.group() + suffix
            (directory / f"{identifier}.xml").write_bytes(derived)
            metadata = {
                "url": f"https://data.stortinget.no/eksport/stortingsvedtak?sesjonid={session}",
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
                "extraction": "Original byteprefix + én komplett uendret objektblokk + suffix",
                "provenance": (
                    "docs/research/issue-2/vedtak599/fetch-manifest.json"
                    if session == "2025-2026"
                    else "docs/research/issue-2/kontrollkilder.md; aar/input_manifest.json"
                ),
            }
            (directory / f"{identifier}.json").write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )


if __name__ == "__main__":
    main()
