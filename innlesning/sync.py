"""Varig sesjonssynkronisering. Kildeinventar er ikke en additiv budsjettkjede."""

import hashlib
import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field as datafield
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from lxml import etree

from .ingestion import NS, START_SESSION, field, structure_node, validate_source
from .model import Report
from .storage import SCHEMA_VERSION, check_schema, initialize, read_report, save_report_in

FINGERPRINT_VERSION = "xml-object-v1"
PARSER_VERSION = "b1-original-v1"
MAX_CONTROL_TEXT = 32_767

SCHEMA = """
CREATE TABLE IF NOT EXISTS sync_jobs (
  sequence INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL UNIQUE,
  dataset TEXT NOT NULL, session TEXT NOT NULL,
  scope TEXT NOT NULL, selected_id TEXT, source_sha256 TEXT NOT NULL REFERENCES sources(sha256),
  metadata_json TEXT NOT NULL, historical_sample INTEGER NOT NULL,
  fingerprint_version TEXT NOT NULL, parser_version TEXT NOT NULL,
  started_utc TEXT NOT NULL, completed_utc TEXT, status TEXT NOT NULL,
  response_time TEXT, result_json TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS one_pending_sync
  ON sync_jobs(dataset, session) WHERE status = 'venter';
CREATE TABLE IF NOT EXISTS decision_revisions (
  revision_id TEXT PRIMARY KEY, dataset TEXT NOT NULL, session TEXT NOT NULL,
  decision_id TEXT NOT NULL, fingerprint_version TEXT NOT NULL, fingerprint TEXT NOT NULL,
  object_xml TEXT NOT NULL, run_id TEXT NOT NULL UNIQUE REFERENCES runs(run_id),
  parser_version TEXT NOT NULL,
  UNIQUE(dataset, session, decision_id, fingerprint_version, fingerprint)
);
CREATE TABLE IF NOT EXISTS decision_heads (
  dataset TEXT NOT NULL, session TEXT NOT NULL, decision_id TEXT NOT NULL,
  revision_id TEXT NOT NULL REFERENCES decision_revisions(revision_id),
  job_id TEXT NOT NULL REFERENCES sync_jobs(job_id), generation INTEGER NOT NULL,
  PRIMARY KEY(dataset, session, decision_id)
);
CREATE TABLE IF NOT EXISTS sync_entries (
  job_id TEXT NOT NULL REFERENCES sync_jobs(job_id), decision_id TEXT NOT NULL,
  revision_id TEXT NOT NULL REFERENCES decision_revisions(revision_id),
  previous_revision_id TEXT, classification TEXT NOT NULL, extraction_status TEXT NOT NULL,
  controls_json TEXT NOT NULL,
  PRIMARY KEY(job_id, decision_id)
);
CREATE TABLE IF NOT EXISTS control_references (
  control_id TEXT PRIMARY KEY, revision_id TEXT NOT NULL REFERENCES decision_revisions(revision_id),
  generation INTEGER NOT NULL, observation_id TEXT NOT NULL REFERENCES sync_jobs(job_id),
  locator TEXT, reference TEXT NOT NULL, reason TEXT NOT NULL, registered_utc TEXT NOT NULL
);
"""


@dataclass
class SyncEntry:
    decision_id: str
    revision_id: str
    previous_revision_id: str | None
    classification: str
    extraction_status: str
    control_reasons: list[str] = datafield(default_factory=list)


@dataclass
class SyncReport:
    job_id: str
    dataset: str
    session: str
    scope: str
    source_sha256: str
    source_metadata: dict[str, object]
    status: str
    started_utc: str
    completed_utc: str | None
    response_time: str | None
    entries: list[SyncEntry] = datafield(default_factory=list)
    errors: list[str] = datafield(default_factory=list)
    contract_version: str = "2"
    fingerprint_version: str = FINGERPRINT_VERSION
    parser_version: str = PARSER_VERSION

    @property
    def counts(self) -> dict[str, int]:
        return {
            kind: sum(entry.classification == kind for entry in self.entries)
            for kind in ("ny", "uendret", "rettelse", "mangler")
        }

    @property
    def control_count(self) -> int:
        return sum(
            entry.extraction_status != "strukturert" or entry.classification == "mangler"
            for entry in self.entries
        )


@dataclass
class ControlReference:
    control_id: str
    revision_id: str
    observation_id: str
    locator: str | None
    reference: str
    reason: str
    registered_utc: str
    status: str


@dataclass
class RevisionReport:
    revision_id: str
    fingerprint: str
    fingerprint_version: str
    parser_version: str
    dataset: str
    object_xml: str
    report: Report
    current_revision_id: str
    current_observation_id: str
    freshness: str
    assessed_utc: str
    current_source_sha256: str
    latest_attempt_id: str
    latest_attempt_status: str
    observation_status: str
    latest_attempt_source_sha256: str
    latest_attempt_errors: list[str]
    controls: list[ControlReference] = datafield(default_factory=list)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _time(value: object) -> datetime:
    result = datetime.fromisoformat(str(value))
    if result.tzinfo is None:
        raise ValueError("Kildetid krever tidssone")
    try:
        return result.astimezone(UTC)
    except OverflowError as error:
        raise ValueError("Kildetid utenfor støttet UTC-område") from error


@contextmanager
def _connect(database: Path, *, readonly: bool = False) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(
        f"{database.resolve().as_uri()}?mode=ro" if readonly else str(database), uri=readonly
    )
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        check_schema(connection)
        with connection:
            yield connection
    finally:
        connection.close()


def _initialize(connection: sqlite3.Connection) -> None:
    initialize(connection)
    for statement in SCHEMA.split(";"):
        if statement.strip():
            connection.execute(statement)
    version = max(SCHEMA_VERSION, connection.execute("PRAGMA user_version").fetchone()[0])
    connection.execute(f"PRAGMA user_version = {version}")


def stage_sync(
    database: Path,
    raw_response: bytes,
    metadata: dict[str, object],
    *,
    historical_sample: bool = False,
    decision_id: str | None = None,
) -> str:
    """Bevar en ventende jobb. Gjenopptaks-ID finnes før publiseringen begynner."""
    session = validate_source(raw_response, metadata)
    if session < START_SESSION and not historical_sample:
        raise ValueError("Eldre sesjon krever eksplisitt historisk prøve")
    kind = metadata.get("fixture_kind", "http_original")
    if kind not in ("http_original", "derived_excerpt", "synthetic_test"):
        raise ValueError("Ukjent kildeslag")
    if kind == "derived_excerpt" and decision_id is None:
        raise ValueError("Avledet utdrag krever uttrykkelig valgt vedtaks-ID")
    if decision_id is None and metadata.get("session_coverage") == "partial":
        raise ValueError("Delvis kilde kan ikke brukes som full sesjon")
    if kind == "synthetic_test" and decision_id is None:
        if metadata.get("session_coverage") != "complete":
            raise ValueError("Syntetisk fullsesjonsprøve krever session_coverage=complete")
    if decision_id is not None and (not decision_id or decision_id.strip() != decision_id):
        raise ValueError("Valgt vedtaks-ID må være ikke-tom")
    dataset = "prove" if historical_sample or kind != "http_original" else "produksjon"
    database.parent.mkdir(parents=True, exist_ok=True)
    job_id = str(uuid4())
    with _connect(database) as connection:
        connection.execute("BEGIN IMMEDIATE")
        _initialize(connection)
        pending = connection.execute(
            "SELECT job_id FROM sync_jobs WHERE dataset=? AND session=? AND status='venter'",
            (dataset, session),
        ).fetchone()
        if pending:
            raise ValueError(f"Ventende jobb må gjenopptas først: {pending['job_id']}")
        connection.execute(
            "INSERT OR IGNORE INTO sources (sha256, raw_response) VALUES (?, ?)",
            (metadata["sha256"], raw_response),
        )
        connection.execute(
            "INSERT INTO sync_jobs (job_id, dataset, session, scope, selected_id, "
            "source_sha256, metadata_json, historical_sample, fingerprint_version, "
            "parser_version, started_utc, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                job_id,
                dataset,
                session,
                "valgt" if decision_id else "full",
                decision_id,
                metadata["sha256"],
                json.dumps(metadata),
                historical_sample,
                FINGERPRINT_VERSION,
                PARSER_VERSION,
                _now(),
                "venter",
            ),
        )
    return job_id


def sync_saved(
    database: Path,
    raw_response: bytes,
    metadata: dict[str, object],
    *,
    historical_sample: bool = False,
    decision_id: str | None = None,
) -> str:
    """Synkroniser hele inventaret eller ett uttrykkelig valgt vedtak."""
    job_id = stage_sync(
        database,
        raw_response,
        metadata,
        historical_sample=historical_sample,
        decision_id=decision_id,
    )
    try:
        return resume_sync(database, job_id)
    except BaseException as error:
        error.add_note(f"Lagret gjenopptaks-ID: {job_id}")
        raise


def _object_value(node: etree._Element, *, preserve: bool | None = None) -> list[Any]:
    # Utvidede navn gjør prefiksendring irrelevant. Kun innrykk mellom
    # XML-barn fjernes; HTML og alle løvverdier bevares nøyaktig.
    if preserve is None:
        preserve = False
        for ancestor in node.iterancestors():
            space = ancestor.get("{http://www.w3.org/XML/1998/namespace}space")
            if space is not None:
                preserve = space == "preserve"
                break
    value = node.text
    children: list[tuple[etree._Element, str | None]] = []
    for child in node:
        if isinstance(child.tag, str):
            children.append((child, child.tail))
        elif child.tail is not None:
            # Kommentar/PI er ikke innhold, men halen er vanlig tegninnhold.
            # Slå den sammen med forrige tekstsegment før blandet tekst vurderes.
            if children:
                previous, tail = children[-1]
                children[-1] = (previous, (tail or "") + child.tail)
            else:
                value = (value or "") + child.tail
    mixed = any(part and part.strip() for part in [value, *(tail for _, tail in children)])
    space = node.get("{http://www.w3.org/XML/1998/namespace}space")
    if space is not None:
        preserve = space == "preserve"
    if children and not mixed and not preserve and value is not None and not value.strip():
        value = None
    return [
        node.tag,
        sorted(node.attrib.items()),
        value,
        [
            [
                _object_value(child, preserve=preserve),
                tail if mixed or preserve or (tail and tail.strip()) else None,
            ]
            for child, tail in children
        ],
    ]


def _inventory(raw: bytes, job: sqlite3.Row) -> tuple[list[etree._Element], str]:
    root = etree.fromstring(
        raw, parser=etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    )
    if root.getroottree().docinfo.doctype:
        raise ValueError("DOCTYPE er ikke tillatt i kildedata")
    if root.tag != NS + "stortingsvedtak_oversikt":
        raise ValueError("Ukjent XML-rot eller navnerom")
    for name in ("sesjon_id", "versjon", "respons_dato_tid"):
        if len(root.findall(NS + name)) != 1:
            raise ValueError(f"Krever ett entydig konvoluttfelt: {name}")
    if field(root, "sesjon_id") != job["session"]:
        raise ValueError("Kilde-URL stemmer ikke med XML-sesjonen")
    if field(root, "versjon") != "1.6":
        raise ValueError("Ukjent kildeformatversjon; krever kompatibilitetskontroll")
    response_time = _time(field(root, "respons_dato_tid")).isoformat()
    lists = root.findall(NS + "stortingsvedtak_liste")
    if len(lists) != 1 or lists[0].get("{http://www.w3.org/2001/XMLSchema-instance}nil") in (
        "true",
        "1",
    ):
        raise ValueError("Krever én uttrykkelig, ikke-nil vedtaksliste")
    nodes = list(lists[0])
    if (lists[0].text and lists[0].text.strip()) or any(
        node.tail and node.tail.strip() for node in nodes
    ):
        raise ValueError("Uklassifisert tekst i vedtakslisten")
    seen: set[str] = set()
    for node in nodes:
        if node.tag != NS + "stortingsvedtak":
            raise ValueError("Ukjent objekt i vedtakslisten")
        ids = node.findall(NS + "id")
        if len(ids) != 1:
            raise ValueError("Vedtaksobjekt krever én ID")
        decision_id = field(node, "id")
        if decision_id != decision_id.strip() or decision_id in seen:
            raise ValueError("Tom, tvetydig eller duplisert vedtaks-ID")
        seen.add(decision_id)
        for name in (
            "sak_id",
            "stortingsvedtak_lenke_url",
            "stortingsvedtak_nummer",
            "stortingsvedtak_dato_tid",
            "stortingsvedtak_tittel",
            "stortingsvedtak_type",
            "stortingsvedtak_tekst",
        ):
            elements = node.findall(NS + name)
            if len(elements) != 1:
                raise ValueError(f"Manglende eller tvetydig objektfelt: {name}")
            if elements[0].get("{http://www.w3.org/2001/XMLSchema-instance}nil") in (
                "true",
                "1",
            ):
                raise ValueError(f"Nil i påkrevd objektfelt: {name}")
        case_id = field(node, "sak_id")
        types = node.findall(NS + "stortingsvedtak_type/" + NS + "id")
        if len(types) != 1:
            raise ValueError("Krever én entydig vedtakstype-ID")
        raw_url = field(node, "stortingsvedtak_lenke_url")
        url = "https:" + raw_url if raw_url.startswith("//") else raw_url
        expected = (
            "https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/"
            f"?did={decision_id}&p={case_id}"
        )
        if not decision_id.isdigit() or not case_id.isdigit() or url != expected:
            raise ValueError("Vedtaks-ID, sak-ID og kildelenke stemmer ikke")
    if job["scope"] == "valgt":
        nodes = [node for node in nodes if field(node, "id") == job["selected_id"]]
        if len(nodes) != 1:
            raise ValueError("Valgt vedtaks-ID mangler")
    return nodes, response_time


def resume_sync(database: Path, job_id: str) -> str:
    """Publiser atomisk fra lagrede byte. Fullført gjenopptak gjør ingen skriving."""
    with _connect(database) as connection:
        connection.execute("BEGIN IMMEDIATE")
        job = connection.execute("SELECT * FROM sync_jobs WHERE job_id=?", (job_id,)).fetchone()
        if job is None:
            raise ValueError(f"Ukjent synkroniseringsjobb: {job_id}")
        if job["status"] != "venter":
            return job_id
        if (
            job["fingerprint_version"] != FINGERPRINT_VERSION
            or job["parser_version"] != PARSER_VERSION
        ):
            raise ValueError("Jobbens normalisering/parser kan ikke gjenopptas med denne versjonen")
        metadata: dict[str, object] = json.loads(job["metadata_json"])
        raw = bytes(
            connection.execute(
                "SELECT raw_response FROM sources WHERE sha256=?", (job["source_sha256"],)
            ).fetchone()[0]
        )
        response_time: str | None = None
        try:
            validate_source(raw, metadata)
            retrieved_time = _time(metadata["retrieved_utc"])
            nodes, response_time = _inventory(raw, job)
            previous = connection.execute(
                "SELECT * FROM sync_jobs WHERE dataset=? AND session=? AND status='fullfort' "
                "ORDER BY sequence DESC LIMIT 1",
                (job["dataset"], job["session"]),
            ).fetchone()
            if previous and (
                previous["sequence"] > job["sequence"]
                or _time(response_time) < _time(previous["response_time"])
                or retrieved_time < _time(json.loads(previous["metadata_json"])["retrieved_utc"])
            ):
                raise ValueError("Eldre kildeobservasjon kan ikke overstyre nyere publisert kilde")
            reports: list[tuple[etree._Element, Report]] = []
            for node in nodes:
                report = Report(
                    str(uuid4()), job["source_sha256"], metadata, bool(job["historical_sample"])
                )
                structure_node(report, node, job["session"])
                reports.append((node, report))
        except (ValueError, etree.XMLSyntaxError) as error:
            connection.execute(
                "UPDATE sync_jobs SET status='feilet', completed_utc=?, response_time=?, "
                "result_json=? WHERE job_id=?",
                (_now(), response_time, json.dumps([str(error)]), job_id),
            )
            return job_id
        heads = {
            row["decision_id"]: row
            for row in connection.execute(
                "SELECT * FROM decision_heads WHERE dataset=? AND session=?",
                (job["dataset"], job["session"]),
            )
        }
        observed: set[str] = set()
        for node, report in reports:
            decision_id = field(node, "id")
            observed.add(decision_id)
            fingerprint = hashlib.sha256(
                json.dumps(_object_value(node), ensure_ascii=False, separators=(",", ":")).encode(
                    "utf-8"
                )
            ).hexdigest()
            revision = connection.execute(
                "SELECT revision_id, run_id FROM decision_revisions WHERE dataset=? AND "
                "session=? AND decision_id=? AND fingerprint_version=? AND fingerprint=?",
                (job["dataset"], job["session"], decision_id, FINGERPRINT_VERSION, fingerprint),
            ).fetchone()
            if revision:
                revision_id = revision["revision_id"]
            else:
                revision_id = str(uuid4())
                save_report_in(connection, raw, report)
                connection.execute(
                    "INSERT INTO decision_revisions (revision_id, dataset, session, decision_id, "
                    "fingerprint_version, fingerprint, object_xml, run_id, parser_version) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        revision_id,
                        job["dataset"],
                        job["session"],
                        decision_id,
                        FINGERPRINT_VERSION,
                        fingerprint,
                        etree.tostring(node, encoding="unicode", with_tail=False),
                        report.run_id,
                        PARSER_VERSION,
                    ),
                )
            head = heads.get(decision_id)
            previous_id = head["revision_id"] if head else None
            classification = (
                "ny" if head is None else "uendret" if previous_id == revision_id else "rettelse"
            )
            generation = (head["generation"] + (previous_id != revision_id)) if head else 1
            connection.execute(
                "INSERT INTO decision_heads (dataset, session, decision_id, revision_id, job_id, "
                "generation) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(dataset, session, decision_id) "
                "DO UPDATE SET revision_id=excluded.revision_id, job_id=excluded.job_id, "
                "generation=excluded.generation",
                (job["dataset"], job["session"], decision_id, revision_id, job_id, generation),
            )
            connection.execute(
                "INSERT INTO sync_entries (job_id, decision_id, revision_id, previous_revision_id, "
                "classification, extraction_status, controls_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    job_id,
                    decision_id,
                    revision_id,
                    previous_id,
                    classification,
                    report.status,
                    json.dumps(report.controls),
                ),
            )
        if job["scope"] == "full":
            for decision_id in sorted(heads.keys() - observed):
                revision_id = heads[decision_id]["revision_id"]
                connection.execute(
                    "INSERT INTO sync_entries (job_id, decision_id, revision_id, "
                    "previous_revision_id, classification, extraction_status, controls_json) "
                    "VALUES (?, ?, ?, ?, 'mangler', 'til kontroll', ?)",
                    (
                        job_id,
                        decision_id,
                        revision_id,
                        revision_id,
                        json.dumps(["Tidligere kjent ID mangler i fullstendig svar; ikke slettet"]),
                    ),
                )
        connection.execute(
            "UPDATE sync_jobs SET status='fullfort', completed_utc=?, response_time=?, "
            "result_json='[]' "
            "WHERE job_id=?",
            (_now(), response_time, job_id),
        )
    return job_id


def read_sync(database: Path, job_id: str) -> SyncReport:
    with _connect(database, readonly=True) as connection:
        connection.execute("BEGIN")
        job = connection.execute("SELECT * FROM sync_jobs WHERE job_id=?", (job_id,)).fetchone()
        if job is None:
            raise ValueError(f"Ukjent synkroniseringsjobb: {job_id}")
        entries = [
            SyncEntry(
                row["decision_id"],
                row["revision_id"],
                row["previous_revision_id"],
                row["classification"],
                row["extraction_status"],
                json.loads(row["controls_json"]),
            )
            for row in connection.execute(
                "SELECT decision_id, revision_id, previous_revision_id, classification, "
                "extraction_status, controls_json "
                "FROM sync_entries WHERE job_id=? ORDER BY decision_id",
                (job_id,),
            )
        ]
    return SyncReport(
        job_id,
        job["dataset"],
        job["session"],
        job["scope"],
        job["source_sha256"],
        json.loads(job["metadata_json"]),
        job["status"],
        job["started_utc"],
        job["completed_utc"],
        job["response_time"],
        entries,
        json.loads(job["result_json"] or "[]"),
        fingerprint_version=job["fingerprint_version"],
        parser_version=job["parser_version"],
    )


def read_revision(database: Path, revision_id: str) -> RevisionReport:
    with _connect(database, readonly=True) as connection:
        connection.execute("BEGIN")
        revision = connection.execute(
            "SELECT * FROM decision_revisions WHERE revision_id=?",
            (revision_id,),
        ).fetchone()
        if revision is None:
            raise ValueError(f"Ukjent vedtaksrevisjon: {revision_id}")
        head = connection.execute(
            "SELECT * FROM decision_heads WHERE dataset=? AND session=? AND decision_id=?",
            (revision["dataset"], revision["session"], revision["decision_id"]),
        ).fetchone()
        freshness = (
            "gjeldende observert innhold"
            if head["revision_id"] == revision_id
            else "historisk innhold"
        )
        latest = connection.execute(
            "SELECT * FROM sync_jobs WHERE dataset=? AND session=? ORDER BY sequence DESC LIMIT 1",
            (revision["dataset"], revision["session"]),
        ).fetchone()
        head_source = connection.execute(
            "SELECT source_sha256 FROM sync_jobs WHERE job_id=?",
            (head["job_id"],),
        ).fetchone()[0]
        latest_entry = connection.execute(
            "SELECT classification FROM sync_entries WHERE job_id=? AND decision_id=?",
            (latest["job_id"], revision["decision_id"]),
        ).fetchone()
        observation_status = (
            "siste forsøk ikke fullført"
            if latest["status"] != "fullfort"
            else "mangler i siste fulle svar"
            if latest_entry and latest_entry[0] == "mangler"
            else "ikke omfattet av siste valgte observasjon"
            if latest_entry is None
            else "observert"
        )
        choices: list[ControlReference] = []
        for row in connection.execute(
            "SELECT c.* FROM control_references c JOIN decision_revisions r "
            "ON c.revision_id=r.revision_id WHERE r.dataset=? AND r.session=? AND r.decision_id=? "
            "ORDER BY c.registered_utc, c.control_id",
            (revision["dataset"], revision["session"], revision["decision_id"]),
        ):
            status = (
                "utdatert"
                if row["revision_id"] != head["revision_id"]
                or row["generation"] != head["generation"]
                else "ikke vurderbar"
                if observation_status != "observert"
                else "gjeldende henvisning"
            )
            choices.append(
                ControlReference(
                    row["control_id"],
                    row["revision_id"],
                    row["observation_id"],
                    row["locator"],
                    row["reference"],
                    row["reason"],
                    row["registered_utc"],
                    status,
                )
            )
    return RevisionReport(
        revision_id,
        revision["fingerprint"],
        revision["fingerprint_version"],
        revision["parser_version"],
        revision["dataset"],
        revision["object_xml"],
        read_report(database, revision["run_id"]),
        head["revision_id"],
        head["job_id"],
        freshness,
        _now(),
        head_source,
        latest["job_id"],
        latest["status"],
        observation_status,
        latest["source_sha256"],
        json.loads(latest["result_json"] or "[]"),
        choices,
    )


def read_revision_for_run(database: Path, run_id: str) -> RevisionReport | None:
    """B1-resultater er prøvearkiv; bare eksplisitt registrerte B2-resultater kobles."""
    with _connect(database, readonly=True) as connection:
        if not connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='decision_revisions'"
        ).fetchone():
            return None
        row = connection.execute(
            "SELECT revision_id FROM decision_revisions WHERE run_id=?", (run_id,)
        ).fetchone()
    return read_revision(database, row[0]) if row else None


def record_control_reference(
    database: Path,
    revision_id: str,
    reference: str,
    reason: str,
    *,
    locator: str | None = None,
) -> str:
    """Bevar en revisjonsbundet henvisning; endrer eller godkjenner ingen beløp."""
    for name, value in (
        ("valg/referanse", reference),
        ("begrunnelse", reason),
        ("kilderad", locator),
    ):
        if value is not None and len(value) > MAX_CONTROL_TEXT:
            raise ValueError(f"Kontrollhenvisningens {name} overskrider {MAX_CONTROL_TEXT} tegn")
    if not reference.strip() or not reason.strip():
        raise ValueError("Kontrollhenvisning krever valg/referanse og begrunnelse")
    selected = read_revision(database, revision_id)
    if locator is not None and locator not in {line.locator for line in selected.report.lines}:
        raise ValueError("Kilderad finnes ikke i valgt revisjon")
    control_id = str(uuid4())
    with _connect(database) as connection:
        connection.execute("BEGIN IMMEDIATE")
        head = connection.execute(
            "SELECT h.* FROM decision_heads h JOIN decision_revisions r ON "
            "h.dataset=r.dataset AND h.session=r.session AND h.decision_id=r.decision_id "
            "WHERE r.revision_id=?",
            (revision_id,),
        ).fetchone()
        if head["revision_id"] != revision_id:
            raise ValueError("Ny kontrollhenvisning krever gjeldende observert revisjon")
        connection.execute(
            "INSERT INTO control_references (control_id, revision_id, generation, observation_id, "
            "locator, reference, reason, registered_utc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                control_id,
                revision_id,
                head["generation"],
                head["job_id"],
                locator,
                reference,
                reason,
                _now(),
            ),
        )
    return control_id
