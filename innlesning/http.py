"""Offentlig Stortings-API. Ingen URL-parameter, omdirigering eller automatisk retry."""

import hashlib
from datetime import UTC, datetime
from email.message import Message
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .ingestion import MAX_BYTES, session_url


class NoRedirect(HTTPRedirectHandler):
    def http_error_302(
        self, req: Request, fp: object, code: int, msg: str, headers: object
    ) -> None:
        raise HTTPError(req.full_url, code, "Omdirigering avvist", Message(), None)

    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    http_error_308 = http_error_302


def fetch_session(session: str, *, timeout: int = 30) -> tuple[bytes, dict[str, object]]:
    url = session_url(session)
    if not 1 <= timeout <= 120:
        raise ValueError("Timeout må være mellom 1 og 120 sekunder")
    request = Request(url, headers={"User-Agent": "budsjetthistorikk-B1/1", "Accept": "text/xml"})
    with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError(f"Uventet HTTP-status: {response.status}")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Kilderespons overskrider 32 MiB")
        return raw, {
            "url": url,
            "retrieved_utc": datetime.now(UTC).isoformat(),
            "status": response.status,
            "headers": dict(response.headers.items()),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "fixture_kind": "http_original",
        }
