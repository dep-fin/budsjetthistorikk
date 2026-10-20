"""Engangsoppskrift: kopier ett autentisk vedtaksobjekt, uten serialisering."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = Path(sys.argv[1])
raw = ORIGINAL.read_bytes()
assert hashlib.sha256(raw).hexdigest() == (
    "6d7859369de69105c957cb8dbc520a077355b4c9d4452f1605f7954deccea2ac"
)
marker = b"  <stortingsvedtak_liste>\r\n"
prefix = raw[: raw.index(marker) + len(marker)]
block = re.search(
    rb"    <stortingsvedtak>\r\n      <id>40033944</id>.*?</stortingsvedtak>\r\n",
    raw,
    re.DOTALL,
)
assert block is not None
suffix = raw[raw.rindex(b"  </stortingsvedtak_liste>") :]
fixture = prefix + block.group() + suffix
assert len(fixture) == 15214
assert hashlib.sha256(fixture).hexdigest() == (
    "043012d31683fb98d53f3c94b649af6d05ef738bdf4cd6bce7e6558103600512"
)
directory = ROOT / "tests/fixtures"
directory.mkdir(parents=True, exist_ok=True)
(directory / "40033944.derived.xml").write_bytes(fixture)
metadata = json.loads(ORIGINAL.with_suffix(".meta.json").read_text(encoding="utf-8"))
metadata.update(
    fixture_kind="derived_excerpt",
    source_response_sha256=metadata["sha256"],
    source_response_bytes=metadata["bytes"],
    sha256=hashlib.sha256(fixture).hexdigest(),
    bytes=len(fixture),
    decision_id="40033944",
    session_coverage="partial",
    extraction="Original byteprefix (317), komplett objektblokk (14842), suffix (55)",
)
(directory / "40033944.metadata.json").write_text(
    json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
