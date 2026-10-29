"""Explicit one-response research capture; never imports into product storage."""

import argparse
import datetime as dt
import gzip
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("identifier")
    parser.add_argument("url")
    args = parser.parse_args()
    if not args.identifier.replace("-", "").replace(".", "").isalnum():
        raise ValueError("invalid identifier")
    if not args.url.startswith(
        ("https://data.stortinget.no/", "https://www.stortinget.no/", "https://www.regjeringen.no/")
    ):
        raise ValueError("source host outside contract")
    dest = Path(__file__).parent / "originals"
    dest.mkdir(exist_ok=True)
    meta_path = dest / (args.identifier + ".meta.json")
    archive = dest / (args.identifier + ".gz")
    if meta_path.exists() or archive.exists():
        raise FileExistsError(args.identifier)
    meta = {
        "id": args.identifier,
        "requested_url": args.url,
        "started_utc": dt.datetime.now(dt.UTC).isoformat(),
        "request_headers": {
            "User-Agent": "budsjetthistorikk-research/58",
            "Accept-Encoding": "identity",
        },
        "representation": (
            "HTTP response entity bytes read by Python urllib; transfer framing and TLS excluded; "
            "no text normalization; Accept-Encoding identity"
        ),
        "state": "started",
    }

    def save():
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
        )

    save()
    body = None
    try:
        req = urllib.request.Request(args.url, headers=meta["request_headers"])
        with urllib.request.urlopen(req, timeout=50) as resp:
            meta.update(
                status=resp.status, final_url=resp.url, response_headers=list(resp.headers.items())
            )
            body = resp.read()
        meta["state"] = "complete"
    except urllib.error.HTTPError as exc:
        meta.update(
            state="http_error",
            status=exc.code,
            final_url=exc.url,
            response_headers=list(exc.headers.items()),
            error=str(exc),
        )
        body = exc.read()
    except Exception as exc:
        meta.update(state="transport_failed", error=repr(exc))
    if body is not None:
        archive.write_bytes(gzip.compress(body, mtime=0))
        meta.update(
            bytes=len(body),
            sha256=hashlib.sha256(body).hexdigest(),
            archive=archive.name,
            archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
            archive_bytes=archive.stat().st_size,
        )
    meta["completed_utc"] = dt.datetime.now(dt.UTC).isoformat()
    save()
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
