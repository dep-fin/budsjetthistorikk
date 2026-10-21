"""Fast offisiell sesjonsliste; fremtidig maksimal ID er ikke dagens sesjon."""

import hashlib
import re
from datetime import UTC, datetime
from urllib.request import Request, build_opener

from lxml import etree

from innlesning.http import NoRedirect
from innlesning.ingestion import MAX_BYTES, session_url

from .schedule import OSLO

SESSIONS_URL = "https://data.stortinget.no/eksport/sesjoner"


def fetch_sessions(*, timeout: int = 30) -> tuple[bytes, dict[str, object]]:
    if not 1 <= timeout <= 120:
        raise ValueError("Timeout må være mellom 1 og 120 sekunder")
    request = Request(SESSIONS_URL, headers={"User-Agent": "budsjetthistorikk-B7/1"})
    with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError("Uventet HTTP-status ved sesjonsliste")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Sesjonsliste overskrider 32 MiB")
        return raw, {
            "url": SESSIONS_URL,
            "retrieved_utc": datetime.now(UTC).isoformat(),
            "status": 200,
            "headers": dict(response.headers.items()),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        }


def select_sessions(raw: bytes, now: datetime, floor: str) -> tuple[str, ...]:
    session_url(floor)
    if now.tzinfo is None:
        raise ValueError("Sesjonsvalg krever tidssone")
    if len(raw) > MAX_BYTES:
        raise ValueError("Sesjonsliste overskrider 32 MiB")
    root = etree.fromstring(
        raw, etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    )
    if root.getroottree().docinfo.doctype:
        raise ValueError("DOCTYPE er ikke tillatt")
    namespace = etree.QName(root).namespace
    if namespace not in {"http://data.stortinget.no", "https://data.stortinget.no"}:
        raise ValueError("Ukjent navnerom i sesjonsliste")
    ns = "{" + namespace + "}"
    if root.tag != ns + "sesjoner_oversikt":
        raise ValueError("Ukjent rot i sesjonsliste")

    def one(node: etree._Element, name: str) -> etree._Element:
        nodes = node.findall(ns + name)
        if len(nodes) != 1 or nodes[0].get("{http://www.w3.org/2001/XMLSchema-instance}nil") in (
            "1",
            "true",
        ):
            raise ValueError("Manglende/tvetydig/nil felt i sesjonsliste: " + name)
        return nodes[0]

    def session(node: etree._Element) -> tuple[str, datetime, datetime]:
        identifier = one(node, "id").text or ""
        if not re.fullmatch(r"\d{4}-\d{2,4}", identifier):
            raise ValueError("Ugyldig sesjons-ID")
        start = datetime.fromisoformat(one(node, "fra").text or "")
        end = datetime.fromisoformat(one(node, "til").text or "")
        if start.tzinfo is not None or end.tzinfo is not None or start > end:
            raise ValueError("Sesjonsperiode krever ordnet lokal dato/tid")
        if identifier >= floor:
            session_url(identifier)
            if start.year != int(identifier[:4]) or end.year != int(identifier[-4:]):
                raise ValueError("Sesjons-ID og periode stemmer ikke")
        return identifier, start.replace(tzinfo=OSLO), end.replace(tzinfo=OSLO)

    current = session(one(root, "innevaerende_sesjon"))
    listing = one(root, "sesjoner_liste")
    if (listing.text or "").strip() or any((n.tail or "").strip() for n in listing):
        raise ValueError("Uklassifisert tekst i sesjonsliste")
    known: dict[str, tuple[str, datetime, datetime]] = {}
    for node in listing:
        if node.tag != ns + "sesjon":
            raise ValueError("Ukjent objekt i sesjonsliste")
        item = session(node)
        if item[0] in known:
            raise ValueError("Duplisert sesjons-ID")
        known[item[0]] = item
    if known.get(current[0]) != current:
        raise ValueError("Inneværende sesjon mangler eller avviker fra listen")
    result = tuple(sorted(i for i, start, _ in known.values() if i >= floor and start <= now))
    if not result:
        raise ValueError("Sesjonslisten gir ingen startet produksjonssesjon")
    return result
