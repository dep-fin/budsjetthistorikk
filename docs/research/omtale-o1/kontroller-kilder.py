"""Reproduser O1-belegg fra bevarte originaler. Ingen produktadapter."""

import hashlib
import importlib.metadata
import json
from pathlib import Path

from lxml import html
from pypdf import PdfReader

root = Path(__file__).resolve().parent
manifest = json.loads((root / "source-manifest.json").read_text(encoding="utf-8"))
for entry in manifest:
    if entry.get("status") == 200:
        raw = (root / entry["file"]).read_bytes()
        assert len(raw) == entry["bytes"]
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"]

selections = {
    "prop16s-ch2.html": ["kap2", "kap2_ch7", "kap2_ch7_ch1", "kap2_ch7_ch2", "kap2_ch7_ch3"],
    "prop16s-ch4.html": [],
    "inns81s.html": ["m1", "m1_1", "m1_1_1", "m1_1_2", "m1_1_3", "m2", "m3"],
    "votering-161224.html": ["2024-12-16-25"],
}
evidence = {
    "kind": "O1 research evidence, not a product schema or export",
    "extractor": "o1-lxml-text-content-1",
    "libraries": {n: importlib.metadata.version(n) for n in ["lxml", "pypdf"]},
    "sections": [],
}
for name, ids in selections.items():
    raw = (root / "originals" / name).read_bytes()
    doc = html.fromstring(raw.decode("utf-8"))
    nodes = [doc.get_element_by_id(i) for i in ids]
    if name == "prop16s-ch4.html":
        rows = doc.xpath('//tr[td[contains(., "1429")]]')
        assert len(rows) == 1
        row = rows[0]
        nodes = [row, *list(row.itersiblings())[:4]]
    for node in nodes:
        # kap2 is heading only; neighbouring chapter/post blocks are siblings,
        # not XML ancestors. Keep all selected blocks separately.
        path = node.getroottree().getpath(node)
        evidence["sections"].append(
            {
                "file": "originals/" + name,
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "encoding": "utf-8",
                "html_id": node.get("id"),
                "xpath": path,
                "text": node.text_content(),
                "html": html.tostring(node, encoding="unicode", with_tail=False),
            }
        )
for name in ["prop16s", "inns81s"]:
    reader = PdfReader(root / "originals" / (name + ".pdf"))
    (root / (name + ".txt")).write_text(
        "\n".join(
            "=== PDF page " + str(i + 1) + " ===\n" + p.extract_text()
            for i, p in enumerate(reader.pages)
        ),
        encoding="utf-8",
    )
(root / "passages.json").write_text(
    json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("Verified source hashes; extracted", len(evidence["sections"]), "HTML blocks")
