"""Readonly kontroll av gammel fullrespons og begge autentiske B6-utdrag."""

import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
original = Path(__file__).parent / "originals/session-2024-2025-9cfe.xml.gz"
raw = gzip.decompress(original.read_bytes())
assert len(raw) == 7_479_943
assert hashlib.sha256(raw).hexdigest() == (
    "9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680"
)
prefix = raw[:317]
suffix = raw[-55:]
rows = []
for identifier, start, count in (
    ("40034048", 1_249_812, 5_686),
    ("40034229", 2_298_491, 132_911),
):
    expected = (ROOT / f"tests/fixtures/b6/{identifier}.xml").read_bytes()
    sidecar = json.loads((ROOT / f"tests/fixtures/b6/{identifier}.json").read_bytes())
    reconstructed = prefix + raw[start : start + count] + suffix
    assert reconstructed == expected
    assert sidecar["object_start_byte_0"] == start
    assert sidecar["object_bytes"] == count
    assert sidecar["source_response_sha256"] == hashlib.sha256(raw).hexdigest()
    rows.append(
        {
            "decision_id": identifier,
            "object_start_byte_0": start,
            "object_bytes": count,
            "prefix_bytes": len(prefix),
            "suffix_bytes": len(suffix),
            "excerpt_sha256": hashlib.sha256(expected).hexdigest(),
            "byteidentical": True,
        }
    )
print(json.dumps(rows, ensure_ascii=False, indent=2))
