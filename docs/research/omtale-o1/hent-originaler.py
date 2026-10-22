"""Avgrenset O1-kildeinnhenting; ikke en produksjonsadapter.

Bevarer HTTP-responskropp før teksttolkning. Krever vanlig nettverkstilgang.
"""

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCES = {
    "prop16s.pdf": "https://www.regjeringen.no/contentassets/65a4e1b12ca242b6b7c5958edd9dc5c1/no/pdfs/prp202420250016000dddpdfs.pdf",
    "prop16s-ch2.html": "https://www.regjeringen.no/no/dokumenter/prop.-16-s-20242025/id3075774/?ch=2",
    "prop16s-ch4.html": "https://www.regjeringen.no/no/dokumenter/prop.-16-s-20242025/id3075774/?ch=4",
    "inns81s.pdf": "https://www.stortinget.no/globalassets/pdf/innstillinger/stortinget/2024-2025/inns-202425-081s.pdf",
    "inns81s.html": "https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-081s/?all=true",
    "votering-161224.html": "https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-16/voteringer#161224-25",
}

root = Path(__file__).resolve().parent
out = root / "originals"
out.mkdir(exist_ok=True)
manifest_path = root / "source-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
for name, url in SOURCES.items():
    if any(e.get("status") == 200 and e.get("file") == "originals/" + name for e in manifest):
        continue
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    entry = {"file": "originals/" + name, "requested_url": url, "started_utc": started}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        entry["request_headers"] = {"User-Agent": "Mozilla/5.0"}
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
            (out / name).write_bytes(raw)
            entry.update(
                final_url=response.url,
                status=response.status,
                headers={k: v for k, v in response.headers.items() if k.lower() != "set-cookie"},
                omitted_headers=["Set-Cookie"],
                bytes=len(raw),
                sha256=hashlib.sha256(raw).hexdigest(),
            )
    except Exception as exc:
        entry.update(error=str(exc))
    entry["completed_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    manifest.append(entry)
    (root / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(name, entry.get("status"), entry.get("bytes"), entry.get("error", ""))
