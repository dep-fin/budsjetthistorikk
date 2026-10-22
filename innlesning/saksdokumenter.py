"""B8: selvstendige kildeforsøk og immutable metadata om vedtakets sak.

Dokumentene er knyttet til saken. Ingen forslagstekst eller forslagssum hentes.
Tidligere vedtaks-/beløpsobservasjoner og faglige avgjørelser endres aldri.
"""

import hashlib
import json
import re
import sqlite3
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from http.client import HTTPException, IncompleteRead
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, build_opener
from uuid import uuid4

from lxml import etree, html

from .http import NoRedirect
from .ingestion import MAX_BYTES, NS, session_url, text
from .observations import encode, identity
from .storage import check_schema
from .sync import initialize_sync_storage, read_revision

VERSION = "saksdokumenter-1"
KEYWORD_VERSION = "stikkord-1"
_NIL = "{http://www.w3.org/2001/XMLSchema-instance}nil"
_CASE_FIELDS = ("id", "sak_sesjon", "sak_nummer", "henvisning", "type", "status", "ferdigbehandlet")
_SCHEMA = """
CREATE TABLE IF NOT EXISTS b8_meta (version TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS b8_sources (sha256 TEXT PRIMARY KEY, raw_response BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS b8_attempts (
 sequence INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT UNIQUE NOT NULL,
 dataset TEXT NOT NULL, session TEXT NOT NULL, case_id TEXT NOT NULL,
 started_utc TEXT NOT NULL, observed_utc TEXT NOT NULL,
 status TEXT NOT NULL, sha256 TEXT, metadata_json TEXT, reason TEXT NOT NULL,
 source_utc TEXT, revision_id TEXT, content_json TEXT, generation INTEGER
);
CREATE TABLE IF NOT EXISTS b8_case_revisions (
 id TEXT PRIMARY KEY, fingerprint_version TEXT NOT NULL, canonical_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS b8_heads (
 dataset TEXT NOT NULL, session TEXT NOT NULL, case_id TEXT NOT NULL,
 attempt_id TEXT NOT NULL, revision_id TEXT NOT NULL, generation INTEGER NOT NULL,
 observed_utc TEXT NOT NULL, source_utc TEXT NOT NULL,
 PRIMARY KEY(dataset,session,case_id)
);
CREATE TABLE IF NOT EXISTS b8_enrichments (id TEXT PRIMARY KEY, payload TEXT NOT NULL);
"""


@dataclass(frozen=True)
class RawField:
    text: str | None
    nil: str | None = None
    present: bool = True


@dataclass(frozen=True)
class Publication:
    id: str
    source_sha256: str
    locator: str
    fields: dict[str, RawField]
    kind: str
    number: str | None
    series: str | None
    session: str | None
    url: str | None
    identity_status: str
    link_status: str
    issues: tuple[str, ...]


@dataclass(frozen=True)
class CaseRelation:
    source_sha256: str
    locator: str
    fields: dict[str, RawField]


@dataclass(frozen=True)
class CaseContent:
    revision_id: str
    source_utc: str
    source_sha256: str
    fields: dict[str, RawField]
    publications: tuple[Publication, ...]
    relations: tuple[CaseRelation, ...]
    issues: tuple[str, ...]


@dataclass(frozen=True)
class CaseAttempt:
    id: str
    dataset: str
    session: str
    case_id: str
    started_utc: str
    observed_utc: str
    status: str
    source_sha256: str | None
    metadata_json: str | None
    reason: str
    content: CaseContent | None
    generation: int | None


@dataclass(frozen=True)
class CaseContext:
    current_attempt_id: str | None
    current_revision_id: str | None
    generation: int
    latest_attempt_id: str | None
    latest_status: str
    latest_reason: str
    latest_source_sha256: str | None


@dataclass(frozen=True)
class KeywordView:
    chapter: str
    post: str
    locator: str
    source_sha256: str
    raw_text: str
    raw_html: str
    words: tuple[str, ...]
    status: str
    reason: str
    version: str = KEYWORD_VERSION


@dataclass(frozen=True)
class CaseEnrichment:
    id: str
    decision_revision_id: str
    dataset: str
    session: str
    api_id: str
    formal_number: str
    case_id: str
    attempt_id: str
    case_generation: int | None
    content: CaseContent | None
    keywords: tuple[KeywordView, ...]
    issues: tuple[str, ...]
    version: str = VERSION


def case_url(case_id: str) -> str:
    if not isinstance(case_id, str) or not re.fullmatch(r"[1-9][0-9]{0,11}", case_id):
        raise ValueError("Saks-ID krever positive ASCII-sifre")
    return f"https://data.stortinget.no/eksport/sak?sakid={case_id}"


def safe_document_url(raw: str | None) -> str | None:
    """Bare eksplisitte offentlige HTTPS-verter; dette er metadata, ingen nettprøve."""
    if not raw or any(ord(c) < 33 or ord(c) == 127 for c in raw) or "\\" in raw:
        return None
    try:
        parsed = urlsplit("https:" + raw if raw.startswith("//") else raw)
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.hostname
            not in {"www.stortinget.no", "stortinget.no", "www.regjeringen.no", "regjeringen.no"}
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port not in {None, 80, 443}
        ):
            return None
        return urlunsplit(("https", parsed.hostname, parsed.path, parsed.query, parsed.fragment))
    except ValueError:
        return None


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _time(value: object) -> str:
    result = datetime.fromisoformat(str(value))
    if result.tzinfo is None:
        raise ValueError("Sakens kilde-/hentetid krever tidssone")
    return result.astimezone(UTC).isoformat()


@contextmanager
def _connection(database: Path, *, write: bool = False) -> Iterator[sqlite3.Connection]:
    if write:
        database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(
        str(database) if write else f"{database.resolve().as_uri()}?mode=ro", uri=not write
    )
    connection.row_factory = sqlite3.Row
    try:
        check_schema(connection)
        if write:
            connection.execute("BEGIN IMMEDIATE")
            initialize_sync_storage(connection)
            existing = connection.execute(
                "SELECT name FROM sqlite_master WHERE name='b8_meta'"
            ).fetchone()
            if existing and [r[0] for r in connection.execute("SELECT version FROM b8_meta")] != [
                VERSION
            ]:
                raise ValueError("Ukjent B8-modulversjon")
            for statement in _SCHEMA.split(";"):
                if statement.strip():
                    connection.execute(statement)
            connection.execute("INSERT OR IGNORE INTO b8_meta VALUES (?)", (VERSION,))
            connection.execute("PRAGMA user_version = 5")
        else:
            existing = connection.execute(
                "SELECT name FROM sqlite_master WHERE name='b8_meta'"
            ).fetchone()
            if existing and [r[0] for r in connection.execute("SELECT version FROM b8_meta")] != [
                VERSION
            ]:
                raise ValueError("Ukjent B8-modulversjon")
        with connection:
            yield connection
    finally:
        connection.close()


def _fields(node: etree._Element) -> dict[str, RawField]:
    result: dict[str, RawField] = {}
    for child in node:
        if not isinstance(child.tag, str) or not child.tag.startswith(NS):
            raise ValueError("Ukjent XML-navnerom i saksmetadata")
        name = child.tag.removeprefix(NS)
        if name in result or len(child):
            raise ValueError("Duplisert eller sammensatt saksmetadatafelt")
        result[name] = RawField(child.text, child.get(_NIL))
    return result


def _value(fields: dict[str, RawField], name: str) -> str | None:
    value = fields.get(name)
    return value.text if value and value.nil not in {"true", "1"} else None


def _canonical(fields: dict[str, RawField]) -> dict[str, Any]:
    return {k: asdict(v) for k, v in fields.items() if k != "respons_dato_tid"}


def _document_identity(identifier: str) -> tuple[str, int, str, str] | None:
    """Bare gjenkjennelige dokumentkoder, ikke vilkårlige URL-/ID-gjetninger."""
    try:
        code = urlsplit(identifier).path.rstrip("/").rsplit("/", 1)[-1]
    except ValueError:
        return None
    reference = re.fullmatch(r"inns-(20\d{2})(\d{2})-(\d+)(ls|s|l)", code, re.I)
    if reference:
        return (
            "innstilling",
            int(reference[3]),
            reference[4].upper(),
            reference[1] + "-20" + reference[2],
        )
    reference = re.fullmatch(r"PRP(20\d{2})(20\d{2})(\d{4})000DDDEPI(LS|S|L)", code, re.I)
    if reference:
        return (
            "proposisjon",
            int(reference[3]),
            reference[4].upper(),
            reference[1] + "-" + reference[2],
        )
    return None


def _publication(
    fields: dict[str, RawField], sha: str, locator: str, revision: str, case_session: str
) -> Publication:
    label = _value(fields, "lenke_tekst")
    raw_type, subtype = _value(fields, "type"), _value(fields, "undertype")
    match = re.fullmatch(
        r"(Prop\.|Innst\.)\s+(\d+)\s+(LS|S|L)\s+\((20\d{2})-(20\d{2})\)", label or ""
    )
    kind, status = "uavklart", "uavklart"
    number = series = session = None
    issues: list[str] = []
    if match:
        number, series = match[2], match[3]
        session = match[4] + "-" + match[5]
        kind = "proposisjon" if match[1] == "Prop." else "innstilling"
        compatible = (raw_type, subtype) == (
            ("regjering", "proposisjon") if kind == "proposisjon" else ("innstilling", "storting")
        )
        if int(match[5]) != int(match[4]) + 1 or int(number) < 1:
            status = "uavklart"
            issues.append("ugyldig_dokumentnummer_eller_sesjon")
        elif not compatible:
            status = "motstrid"
            issues.append("motstrid_mellom_etikett_og_type")
        else:
            status = "identifisert"
        for field, unresolved in (
            ("eksport_id", "uavklart_eksportidentitet"),
            ("lenke_url", "uavklart_lenkeidentitet"),
        ):
            identifier = _value(fields, field)
            # Nil eksport-ID er legitimt; en ukjent lenke beviser ikke identiteten.
            if field == "eksport_id" and not identifier:
                continue
            reference = _document_identity(identifier or "")
            if reference is None:
                if status == "identifisert":
                    status = "uavklart"
                issues.append(unresolved)
            elif reference != (kind, int(number), series, session):
                status = "motstrid"
                issues.append("motstrid_dokumentidentiteter")
        if session != case_session:
            status = "motstrid"
            issues.append("dokumentets_sesjon_avviker_fra_saken")
    elif raw_type == "referat":
        kind, status = "referat", "råreferanse"
    else:
        issues.append("uavklart_dokumentidentitet")
    if not label:
        issues.append("mangler_dokumentetikett")
    url = safe_document_url(_value(fields, "lenke_url"))
    if url is None:
        issues.append("mangler_eller_utrygg_dokumentlenke")
    return Publication(
        identity(VERSION, revision, locator, _canonical(fields)),
        sha,
        locator,
        fields,
        kind,
        number,
        series,
        session,
        url,
        status,
        "metadata_ikke_hentet" if url else "utilgjengelig",
        tuple(issues),
    )


def _parse(raw: bytes, sha: str, case_id: str, session: str) -> tuple[CaseContent, str]:
    if not raw or len(raw) > MAX_BYTES:
        raise ValueError("Tom eller for stor saksrespons (maks 32 MiB)")
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
    root = etree.fromstring(raw, parser)
    if root.getroottree().docinfo.doctype or root.tag != NS + "detaljert_sak":
        raise ValueError("Saksrespons krever detaljert_sak uten DTD")
    fields: dict[str, RawField] = {}
    for name in _CASE_FIELDS:
        nodes = root.findall(NS + name)
        if len(nodes) > 1:
            raise ValueError("Duplisert saksfelt: " + name)
        fields[name] = (
            RawField(nodes[0].text, nodes[0].get(_NIL)) if nodes else RawField(None, present=False)
        )
    if _value(fields, "id") != case_id or _value(fields, "sak_sesjon") != session:
        raise ValueError("Saks-ID/sesjon stemmer ikke med valgt vedtaksgrunnlag")
    source_utc = _time(root.findtext(NS + "respons_dato_tid"))
    pubs: list[tuple[str, dict[str, RawField]]] = []
    relations: list[CaseRelation] = []
    issues: list[str] = []
    for container, item in (
        ("publikasjon_referanse_liste", "publikasjon_referanse"),
        ("sak_relasjon_liste", "sak_relasjon"),
    ):
        nodes = root.findall(NS + container)
        if len(nodes) > 1:
            raise ValueError("Duplisert saksliste: " + container)
        if not nodes or nodes[0].get(_NIL) in {"true", "1"}:
            issues.append("mangler_" + container)
            continue
        for n, node in enumerate(nodes[0], 1):
            if node.tag != NS + item or n > 1000:
                raise ValueError("Ukjent eller for stor saksliste")
            locator = f"/detaljert_sak/{container}/{item}[{n}]"
            values = _fields(node)
            if item == "publikasjon_referanse":
                pubs.append((locator, values))
            else:
                relations.append(CaseRelation(sha, locator, values))
        if item == "publikasjon_referanse" and not pubs:
            issues.append("ingen_publikasjonsreferanser")
    canonical = encode(
        [
            _canonical(fields),
            [[loc, _canonical(f)] for loc, f in pubs],
            [[r.locator, _canonical(r.fields)] for r in relations],
        ]
    )
    revision = identity(VERSION, canonical)
    publications = tuple(_publication(f, sha, loc, revision, session) for loc, f in pubs)
    for kind in ("innstilling", "proposisjon"):
        matching = [p for p in publications if p.kind == kind]
        if not matching:
            issues.append("mangler_" + kind)
        if len(matching) > 1:
            issues.append("flere_" + kind + "er")
    return CaseContent(
        revision, source_utc, sha, fields, publications, tuple(relations), tuple(issues)
    ), canonical


def begin_case_attempt(
    database: Path, case_id: str, *, dataset: str, session: str, observed_utc: str | None = None
) -> str:
    case_url(case_id)
    session_url(session)
    if dataset not in {"produksjon", "prove"}:
        raise ValueError("Saksmetadata krever produksjon eller prove")
    now = _now()
    observed = _time(observed_utc or now)
    identifier = str(uuid4())
    with _connection(database, write=True) as connection:
        connection.execute(
            "INSERT INTO b8_attempts "
            "(id,dataset,session,case_id,started_utc,observed_utc,status,reason) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (
                identifier,
                dataset,
                session,
                case_id,
                now,
                observed,
                "venter",
                "HTTP/lagret respons er ikke ferdigbehandlet",
            ),
        )
    return identifier


def fail_case_attempt(
    database: Path, attempt_id: str, reason: str, *, metadata: dict[str, object] | None = None
) -> CaseAttempt:
    metadata_json = encode(metadata) if metadata is not None else None
    with _connection(database, write=True) as connection:
        row = connection.execute(
            "SELECT status,metadata_json FROM b8_attempts WHERE id=?", (attempt_id,)
        ).fetchone()
        if row is None or row[0] != "venter":
            raise ValueError("Bare et ventende saksforsøk kan feile")
        if metadata_json is not None and row["metadata_json"] not in {None, metadata_json}:
            raise ValueError("Saksforsøket er bundet til andre metadata")
        connection.execute(
            "UPDATE b8_attempts SET status='feilet',reason=?,"
            "metadata_json=COALESCE(metadata_json,?) WHERE id=?",
            (reason, metadata_json, attempt_id),
        )
    return read_case_attempt(database, attempt_id)


def save_case_response(
    database: Path, attempt_id: str, raw: bytes, metadata: dict[str, object]
) -> CaseAttempt:
    """Mottatte byte lagres før proveniens-/XML-kontroll. Publisering er atomisk."""
    raw = bytes(raw)
    metadata_json = encode(metadata)
    metadata = json.loads(metadata_json)  # Tolk den samme frosne sidevognen som lagres.
    sha = hashlib.sha256(raw).hexdigest()
    with _connection(database, write=True) as connection:
        row = connection.execute("SELECT * FROM b8_attempts WHERE id=?", (attempt_id,)).fetchone()
        if row is None or row["status"] != "venter":
            raise ValueError("Saksforsøket er ukjent eller allerede avsluttet")
        if (row["sha256"] is not None or row["metadata_json"] is not None) and (
            row["sha256"],
            row["metadata_json"],
        ) != (sha, metadata_json):
            raise ValueError("Saksforsøket er bundet til andre råbyte eller metadata")
        if len(raw) > MAX_BYTES:
            connection.execute(
                "UPDATE b8_attempts SET status='feilet',reason=? WHERE id=?",
                ("Saksrespons overstiger 32 MiB; ikke lagret", attempt_id),
            )
        else:
            connection.execute("INSERT OR IGNORE INTO b8_sources VALUES (?,?)", (sha, raw))
            connection.execute(
                "UPDATE b8_attempts SET sha256=?,metadata_json=? WHERE id=?",
                (sha, metadata_json, attempt_id),
            )
    if len(raw) > MAX_BYTES:
        return read_case_attempt(database, attempt_id)
    # Råbyte overlever også feil eller avbrudd før/under tolkning.
    try:
        if metadata.get("body_read_error"):
            raise ValueError("Feil ved lesing av HTTP-respons: " + str(metadata["body_read_error"]))
        if (
            metadata.get("url") != case_url(row["case_id"])
            or type(metadata.get("status")) is not int
            or metadata["status"] != 200
        ):
            raise ValueError("Saksmetadata krever valgt offisiell URL og HTTP 200")
        if (
            metadata.get("sha256") != sha
            or type(metadata.get("bytes")) is not int
            or metadata["bytes"] != len(raw)
        ):
            raise ValueError("Saksmetadata har feil byteantall/SHA-256")
        observed = _time(metadata.get("retrieved_utc"))
        content, canonical = _parse(raw, sha, row["case_id"], row["session"])
    except (ValueError, etree.LxmlError) as error:
        return fail_case_attempt(database, attempt_id, str(error))
    with _connection(database, write=True) as connection:
        current = connection.execute(
            "SELECT * FROM b8_attempts WHERE id=?", (attempt_id,)
        ).fetchone()
        if current is None or current["status"] != "venter":
            raise ValueError("Saksforsøket ble allerede avsluttet")
        if (current["sha256"], current["metadata_json"]) != (sha, metadata_json) or any(
            current[field] != row[field] for field in ("dataset", "session", "case_id")
        ):
            raise ValueError("Saksforsøkets råbyte-/metadatabinding er endret")
        head = connection.execute(
            "SELECT * FROM b8_heads WHERE dataset=? AND session=? AND case_id=?",
            (row["dataset"], row["session"], row["case_id"]),
        ).fetchone()
        stale = head is not None and (
            observed < head["observed_utc"] or content.source_utc < head["source_utc"]
        )
        status, reason = (
            ("eldre_kilde", "Eldre kilde-/hentetid kan ikke overta gjeldende kilde")
            if stale
            else ("observert", "")
        )
        generation = (
            None
            if stale
            else 1
            if head is None
            else head["generation"] + (head["revision_id"] != content.revision_id)
        )
        connection.execute(
            "INSERT OR IGNORE INTO b8_case_revisions VALUES (?,?,?)",
            (content.revision_id, VERSION, canonical),
        )
        connection.execute(
            "UPDATE b8_attempts SET status=?,reason=?,observed_utc=?,source_utc=?,"
            "revision_id=?,content_json=?,generation=? WHERE id=?",
            (
                status,
                reason,
                observed,
                content.source_utc,
                content.revision_id,
                encode(asdict(content)),
                generation,
                attempt_id,
            ),
        )
        if not stale:
            connection.execute(
                "INSERT INTO b8_heads VALUES (?,?,?,?,?,?,?,?) "
                "ON CONFLICT(dataset,session,case_id) DO UPDATE SET "
                "attempt_id=excluded.attempt_id,revision_id=excluded.revision_id,"
                "generation=excluded.generation,observed_utc=excluded.observed_utc,"
                "source_utc=excluded.source_utc",
                (
                    row["dataset"],
                    row["session"],
                    row["case_id"],
                    attempt_id,
                    content.revision_id,
                    generation,
                    observed,
                    content.source_utc,
                ),
            )
    return read_case_attempt(database, attempt_id)


def import_case_response(
    database: Path,
    case_id: str,
    raw: bytes,
    metadata: dict[str, object],
    *,
    dataset: str,
    session: str,
) -> CaseAttempt:
    # Feil i metadata gir også et varig forsøk og råbevis.
    try:
        observed = _time(metadata.get("retrieved_utc"))
    except ValueError:
        observed = _now()
    attempt = begin_case_attempt(
        database, case_id, dataset=dataset, session=session, observed_utc=observed
    )
    return save_case_response(database, attempt, raw, metadata)


def _content(data: dict[str, Any] | None) -> CaseContent | None:
    if data is None:
        return None
    values = dict(data)
    values["fields"] = {k: RawField(**v) for k, v in values["fields"].items()}
    values["publications"] = tuple(
        Publication(
            **{
                **p,
                "fields": {k: RawField(**v) for k, v in p["fields"].items()},
                "issues": tuple(p["issues"]),
            }
        )
        for p in values["publications"]
    )
    values["relations"] = tuple(
        CaseRelation(**{**r, "fields": {k: RawField(**v) for k, v in r["fields"].items()}})
        for r in values["relations"]
    )
    values["issues"] = tuple(values["issues"])
    return CaseContent(**values)


def read_case_attempt(database: Path, attempt_id: str) -> CaseAttempt:
    with _connection(database) as connection:
        row = connection.execute("SELECT * FROM b8_attempts WHERE id=?", (attempt_id,)).fetchone()
        if row is None:
            raise ValueError("Ukjent saksforsøk: " + attempt_id)
        return CaseAttempt(
            row["id"],
            row["dataset"],
            row["session"],
            row["case_id"],
            row["started_utc"],
            row["observed_utc"],
            row["status"],
            row["sha256"],
            row["metadata_json"],
            row["reason"],
            _content(json.loads(row["content_json"]) if row["content_json"] else None),
            row["generation"],
        )


def read_case_source(database: Path, attempt_id: str) -> bytes:
    attempt = read_case_attempt(database, attempt_id)
    if not attempt.source_sha256:
        raise ValueError("Saksforsøket har ingen mottatt rårespons")
    with _connection(database) as connection:
        row = connection.execute(
            "SELECT raw_response FROM b8_sources WHERE sha256=?", (attempt.source_sha256,)
        ).fetchone()
    if row is None or hashlib.sha256(row[0]).hexdigest() != attempt.source_sha256:
        raise ValueError("Sakens råbevis mangler eller er korrupt")
    return bytes(row[0])


def read_case_context(database: Path, *, dataset: str, session: str, case_id: str) -> CaseContext:
    with _connection(database) as connection:
        connection.execute("BEGIN")
        if not connection.execute("SELECT name FROM sqlite_master WHERE name='b8_meta'").fetchone():
            return CaseContext(None, None, 0, None, "ikke_hentet", "Ingen saksforsøk", None)
        head = connection.execute(
            "SELECT * FROM b8_heads WHERE dataset=? AND session=? AND case_id=?",
            (dataset, session, case_id),
        ).fetchone()
        latest = connection.execute(
            "SELECT * FROM b8_attempts WHERE dataset=? AND session=? AND case_id=? "
            "AND status!='eldre_kilde' ORDER BY observed_utc DESC,sequence DESC LIMIT 1",
            (dataset, session, case_id),
        ).fetchone()
    return CaseContext(
        head["attempt_id"] if head else None,
        head["revision_id"] if head else None,
        head["generation"] if head else 0,
        latest["id"] if latest else None,
        latest["status"] if latest else "ikke_hentet",
        latest["reason"] if latest else "Ingen saksforsøk",
        latest["sha256"] if latest else None,
    )


def fetch_case(case_id: str, *, timeout: int = 30) -> tuple[bytes, dict[str, object]]:
    url = case_url(case_id)
    if type(timeout) is not int or not 1 <= timeout <= 120:
        raise ValueError("Timeout må være mellom 1 og 120 sekunder")
    request = Request(url, headers={"User-Agent": "budsjetthistorikk-B8/1", "Accept": "text/xml"})
    with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Saksrespons overstiger 32 MiB")
        return raw, {
            "url": url,
            "retrieved_utc": _now(),
            "status": response.status,
            "headers": dict(response.headers.items()),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "fixture_kind": "http_original",
        }


def fetch_case_attempt(
    database: Path,
    case_id: str,
    *,
    dataset: str,
    session: str,
    timeout: int = 30,
    fetch: Callable[..., tuple[bytes, dict[str, object]]] = fetch_case,
) -> CaseAttempt:
    attempt_id = begin_case_attempt(database, case_id, dataset=dataset, session=session)
    try:
        raw, metadata = fetch(case_id, timeout=timeout)
    except HTTPError as error:
        metadata = {
            "url": case_url(case_id),
            "retrieved_utc": _now(),
            "status": error.code,
            "headers": dict(error.headers.items()) if error.headers else {},
        }
        try:
            raw = error.read(MAX_BYTES + 1)
            metadata["body_status"] = "complete" if raw else "empty"
        except (OSError, HTTPException) as read_error:
            # Bare eksplisitt mottatte delbyte kan få råhash. En lesefeil alene
            # sier ikke om null eller flere byte kom frem inne i HTTP-biblioteket.
            raw = read_error.partial if isinstance(read_error, IncompleteRead) else b""
            metadata["body_status"] = "partial" if raw else "unavailable_or_incomplete"
            metadata["body_read_error"] = type(read_error).__name__ + ": " + str(read_error)
        finally:
            error.close()
        if raw:
            metadata.update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
            return save_case_response(database, attempt_id, raw, metadata)
        reason = f"HTTP {error.code}: {error.reason}"
        if metadata.get("body_read_error"):
            reason += "; Feil ved lesing av respons: " + str(metadata["body_read_error"])
        return fail_case_attempt(database, attempt_id, reason, metadata=metadata)
    except (OSError, ValueError, HTTPException) as error:
        return fail_case_attempt(database, attempt_id, str(error))
    return save_case_response(database, attempt_id, raw, metadata)


_KNOWN_WORDS = (
    "kan overføres",
    "overslagsbevilgning",
    "kan nyttes under",
    "kan nyttast under",
    "kan overførast",
    "overslagsløyving",
)


def _keywords(source_html: str, sha: str) -> tuple[KeywordView, ...]:
    """Separat visning av merkede postformål. Ingen beløps-/observasjonsparser."""
    parser = html.HTMLParser(no_network=True, recover=False)
    try:
        document = html.fromstring(source_html, parser=parser)
    except etree.LxmlError:
        return ()
    if any(e.level_name in {"ERROR", "FATAL"} for e in parser.error_log):
        return ()
    result: list[KeywordView] = []
    for table_no, table in enumerate(document.xpath(".//table"), 1):
        rows = table.xpath(".//tr")
        if not rows or [text(c) for c in rows[0]][:3] != ["Kap.", "Post", "Formål"]:
            continue
        chapter = ""
        for row_no, row in enumerate(rows[1:], 2):
            cells = list(row)
            if len(cells) < 3 or any(
                c.get("rowspan") or c.get("colspan", "1") != "1" for c in cells
            ):
                chapter = ""
                continue
            cap, post, purpose = (text(c) for c in cells[:3])
            if cap.isascii() and cap.isdigit() and not post:
                chapter = str(int(cap))
                continue
            if cap:
                chapter = ""
            if not chapter or not post.isascii() or not post.isdigit():
                continue
            marker_xpath = (
                ".//span[contains(concat(' ', normalize-space(@class), ' '), ' type_kursiv ')]"
                " | .//i | .//em"
            )
            markers = cells[2].xpath(marker_xpath)
            words: list[str] = []
            unknown: list[str] = []
            for marker in markers:
                value = text(marker)
                pieces = [v.strip() for v in value.split(",") if v.strip()]
                for piece in pieces:
                    if piece.lower() in _KNOWN_WORDS or re.fullmatch(
                        r"kan (?:nyttes|nyttast) under (?:kap\. \d+(?:,? post \d+)?|post \d+)",
                        piece,
                        re.I,
                    ):
                        words.append(piece)
                    else:
                        unknown.append(piece)
            # Undersøk også resten når en annen (eventuelt tom) markering finnes.
            unmarked_cell = deepcopy(cells[2])
            for marker in unmarked_cell.xpath(marker_xpath):
                marker.drop_tree()  # Beholder halen uten å endre det bevarte råfeltet.
            purpose_without_action = re.sub(
                r",\s*(?:økes|aukes|auka|reduseres|reduserast|minka|bevilges)\s+med.*$",
                "",
                text(unmarked_cell),
                flags=re.I,
            ).rstrip(" ,;")
            unmarked = any(w in purpose_without_action.lower() for w in _KNOWN_WORDS) or (
                "," in purpose_without_action
            )
            status = (
                "uavklart"
                if unknown or unmarked
                else "funnet"
                if words
                else "ingen_stikkord_funnet"
            )
            reason = (
                "Ukjent/umerket stikkord: " + ("; ".join(unknown) or purpose)
                if unknown or unmarked
                else "Eksakte kjente uttrykk i kursiv kildemarkering"
                if words
                else "Ingen stikkord i støttet formålsrad"
            )
            result.append(
                KeywordView(
                    chapter,
                    str(int(post)),
                    f"table[{table_no}]/tr[{row_no}]/td[3]",
                    sha,
                    purpose,
                    etree.tostring(cells[2], encoding="unicode", method="html"),
                    tuple(words),
                    status,
                    reason,
                )
            )
    return tuple(result)


def enrich_revision(database: Path, revision_id: str, attempt_id: str) -> CaseEnrichment:
    revision = read_revision(database, revision_id)
    decision = revision.report.decision
    if decision is None:
        raise ValueError("Berikelse krever bevart vedtak")
    attempt = read_case_attempt(database, attempt_id)
    if (attempt.dataset, attempt.session, attempt.case_id) != (
        revision.dataset,
        decision.session,
        decision.case_id,
    ):
        raise ValueError("Saksforsøket hører ikke til vedtaksrevisjonen")
    issues: tuple[str, ...] = (
        ()
        if attempt.status == "observert"
        else ("saksforsok_" + attempt.status + ":" + attempt.reason,)
    )
    keywords = _keywords(decision.html, revision.report.source_sha256)
    if not keywords:
        issues += ("stikkordtolkning_ukjent_eller_ingen_postrader",)
    result = CaseEnrichment(
        "",
        revision_id,
        revision.dataset,
        decision.session,
        decision.id,
        decision.number,
        decision.case_id,
        attempt_id,
        attempt.generation,
        attempt.content,
        keywords,
        issues,
    )
    result = replace(result, id=identity(VERSION, asdict(result)))
    with _connection(database, write=True) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO b8_enrichments VALUES (?,?)", (result.id, encode(asdict(result)))
        )
    return read_enrichment(database, result.id)


def read_enrichment(database: Path, enrichment_id: str) -> CaseEnrichment:
    with _connection(database) as connection:
        if not connection.execute("SELECT name FROM sqlite_master WHERE name='b8_meta'").fetchone():
            raise ValueError("Ukjent saksberikelse: " + enrichment_id)
        row = connection.execute(
            "SELECT payload FROM b8_enrichments WHERE id=?", (enrichment_id,)
        ).fetchone()
    if row is None:
        raise ValueError("Ukjent saksberikelse: " + enrichment_id)
    data = json.loads(row[0])
    data["content"] = _content(data["content"])
    data["keywords"] = tuple(
        KeywordView(**{**k, "words": tuple(k["words"])}) for k in data["keywords"]
    )
    data["issues"] = tuple(data["issues"])
    result = CaseEnrichment(**data)
    if (
        result.version != VERSION
        or result.id != enrichment_id
        or result.id != identity(VERSION, asdict(replace(result, id="")))
    ):
        raise ValueError("Korrupt eller ukjent saksberikelse")
    return result
