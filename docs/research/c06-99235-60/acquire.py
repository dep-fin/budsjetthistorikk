"""Bounded one-attempt research capture with validation before every HTTP hop."""

import argparse
import datetime as dt
import gzip
import hashlib
import http.client
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HOSTS = frozenset(("data.stortinget.no", "www.stortinget.no", "www.regjeringen.no"))
REPRESENTATION = (
    "HTTP response entity bytes as read by urllib; transfer framing/TLS excluded; "
    "Accept-Encoding identity; no decompression or text/line-ending normalization. "
    "Each HTTP hop has its own capture. Local gzip is an archive, not HTTP Content-Encoding."
)


def now():
    return dt.datetime.now(dt.UTC).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate_url(url):
    if any(ord(char) <= 32 for char in url) or "\\" in url:
        raise ValueError("control/whitespace/backslash in source URL")
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname not in HOSTS
        or parsed.port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
    ):
        raise ValueError("source URL outside exact HTTPS host/port/credential contract")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_once(req):
    opener = urllib.request.build_opener(NoRedirect())
    try:
        return opener.open(req, timeout=55)
    except urllib.error.HTTPError as exc:
        return exc


def capture(identifier, url, dest, opener=request_once):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]*", identifier):
        raise ValueError("invalid capture identifier")
    validate_url(url)  # Before any network, including a first request.
    dest.mkdir(parents=True, exist_ok=True)
    meta_path = dest / (identifier + ".meta.json")
    if meta_path.exists() or list(dest.glob(identifier + ".hop*.gz")):
        raise FileExistsError(identifier)
    meta = {
        "id": identifier,
        "requested_url": url,
        "started_utc": now(),
        "request_headers": {
            "User-Agent": "budsjetthistorikk-research/60",
            "Accept-Encoding": "identity",
        },
        "representation": REPRESENTATION,
        "state": "started",
        "hops": [],
    }

    def save():
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    # Do not overwrite a prior attempt, even if another process created it.
    with meta_path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    try:
        for hop_number in range(9):
            validate_url(url)
            hop = {"url": url, "started_utc": now(), "state": "requesting"}
            meta["hops"].append(hop)
            save()
            response, body = None, bytearray()
            try:
                response = opener(urllib.request.Request(url, headers=meta["request_headers"]))
                hop.update(status=response.status, response_headers=list(response.headers.items()))
                save()
                while True:
                    try:
                        chunk = response.read(65536)
                    except http.client.IncompleteRead as exc:
                        body.extend(exc.partial)
                        raise
                    if not chunk:
                        break
                    body.extend(chunk)
                    if len(body) > 80 * 1024 * 1024:
                        raise ValueError("research response exceeds 80 MiB capture limit")
                length = response.headers.get("Content-Length")
                if length is not None and int(length) != len(body):
                    raise ValueError("incomplete HTTP Content-Length")
                hop.update(state="complete", body_complete=True)
            except BaseException as exc:
                hop.update(state="transport_failed", body_complete=False, error=repr(exc))
                raise
            finally:
                if response is not None:
                    archive = dest / f"{identifier}.hop{hop_number}.gz"
                    archive.write_bytes(gzip.compress(bytes(body), mtime=0))
                    hop.update(
                        archive=archive.name,
                        bytes=len(body),
                        sha256=sha(body),
                        archive_bytes=archive.stat().st_size,
                        archive_sha256=sha(archive.read_bytes()),
                    )
                hop["completed_utc"] = now()
                save()
                if response is not None:
                    response.close()
            status = hop["status"]
            if status in (301, 302, 303, 307, 308):
                location = response.headers.get("Location")
                if not location:
                    raise ValueError("redirect without Location")
                target = urllib.parse.urljoin(url, location)
                hop["redirect_target"] = target
                try:
                    validate_url(target)  # Before the next network call, for every hop.
                except ValueError as exc:
                    meta.update(state="redirect_rejected", error=repr(exc))
                    break
                url = target
                if hop_number == 8:
                    meta.update(state="redirect_limit", error="more than eight redirects")
                continue
            meta.update(
                state="complete" if 200 <= status < 300 else "http_error",
                final_url=url,
                status=status,
            )
            break
    except BaseException as exc:
        meta.update(state="transport_failed", error=repr(exc))
        if isinstance(exc, KeyboardInterrupt | SystemExit):
            raise
    finally:
        meta["completed_utc"] = now()
        save()
    return meta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("identifier")
    parser.add_argument("url")
    args = parser.parse_args()
    meta = capture(args.identifier, args.url, Path(__file__).parent / "originals")
    print(json.dumps({key: meta.get(key) for key in ("id", "state", "status", "error")}))


if __name__ == "__main__":
    main()
