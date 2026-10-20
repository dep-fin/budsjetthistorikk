"""Observasjon-1: uforanderlige kildebeløp; B1/B2-resultater røres ikke.

Den generiske lagringsgrensen krever ingen API-identitet. Storting-adapteren
tolker bare eksplisitt valgte B2-revisjoner og leser aldri fra nettet.
"""

import hashlib
import json
import re
import sqlite3
from dataclasses import asdict, dataclass, fields
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from lxml import etree, html

from .ingestion import amount, text
from .storage import check_schema, initialize
from .sync import read_revision

FORMAT_VERSION = "observasjon-1"
ADAPTER_VERSION = "storting-belop-v1"


def encode(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def identity(*parts: object) -> str:
    return hashlib.sha256(encode(parts).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Anomaly:
    code: str
    reason: str
    affected_fields: tuple[str, ...] = ()
    evidence: str | None = None
    resolution: str | None = None
    chapter: str | None = None
    post: str | None = None
    budget_year: int | None = None


@dataclass(frozen=True)
class Artifact:
    sha256: str
    name: str
    source_kind: str
    mime_type: str
    byte_count: int
    metadata_json: str = "{}"


@dataclass(frozen=True)
class SourcePointer:
    artifact_id: str
    locator: str
    amount_field: str
    sheet: str | None = None
    row: int | None = None
    column: str | None = None
    cell: str | None = None
    raw_record: str | None = None
    null_reason: str = "ikke relevant"

    def __post_init__(self) -> None:
        if self.row is not None and (type(self.row) is not int or self.row < 1):
            raise ValueError("Kildepekerens rad er 1-basert")


@dataclass(frozen=True)
class DocumentReference:
    raw_code: str
    source_column: str
    role: str
    document_type: str | None = None
    number: str | None = None
    session: str | None = None
    external_id: str | None = None
    verified_url: str | None = None
    status: str = "uavklart"
    null_reason: str = "ikke oppgitt"


@dataclass(frozen=True)
class Organization:
    dep: str | None = None
    fdep_nr: str | None = None
    gdep_nr: str | None = None
    gdep_name: str | None = None
    omr_nr: str | None = None
    kat_nr: str | None = None
    mapped_department_code: str | None = None
    mapped_department_name: str | None = None
    register_source: str | None = None
    register_version: str | None = None
    valid_from: str | None = None
    valid_to: str | None = None
    validity_precision: str | None = None
    null_reason: str = "ikke oppgitt"


@dataclass(frozen=True)
class Interpretation:
    adapter_version: str = ADAPTER_VERSION
    normalization_rule: str = "Eksplisitte kroner; heltall; ingen reparasjon av råtekst"
    round: str | None = None
    round_evidence: str | None = None
    reason: str = "Avgrenset tabellmønster for opprinnelig vedtak og enkeltendringer"

    def __post_init__(self) -> None:
        if self.round is not None and (
            self.round not in {"opprinnelig", "rnb", "nysaldering", "ovrig", "uavklart"}
            or not self.round_evidence
        ):
            raise ValueError("Eksplisitt runde krever kjent kode og kildegrunnlag")

    @property
    def id(self) -> str:
        return identity(FORMAT_VERSION, asdict(self))


@dataclass(frozen=True, kw_only=True)
class AmountObservation:
    dataset: str
    source_system: str
    source_unit_id: str
    source_revision_id: str
    interpretation_id: str
    pointer: SourcePointer
    step_id: str
    raw_value: str
    amount_text: str
    amount_kr: int | None
    chapter_raw: str | None = None
    post_raw: str | None = None
    subpost_raw: str | None = None
    chapter: str | None = None
    post: str | None = None
    subpost: str | None = None
    chapter_name: str | None = None
    purpose: str | None = None
    detail_level: str = "uavklart"
    component_of: str | None = None
    budget_year: int | None = None
    year_evidence: str | None = None
    decision_date: str | None = None
    decision_session: str | None = None
    api_id: str | None = None
    event_id: str | None = None
    raw_type: str = "tekst"
    formula: str | None = None
    cached_value: str | None = None
    unit_raw: str | None = None
    currency: str | None = None
    multiplier: str | None = None
    precision: str | None = None
    conversion_rule: str | None = None
    normalization_evidence: str | None = None
    figure_type: str = "uavklart"
    proposal_role: str | None = None
    proposal_identity: str | None = None
    proposal_author: str | None = None
    round: str = "uavklart"
    round_evidence: str | None = None
    stage_raw: str | None = None
    meaning: str = "uavklart"
    scope: str = "uavklart"
    aggregate_coverage: str | None = None
    information_type: str = "bevilgning"
    classification_evidence: str | None = None
    organization: Organization = Organization()
    documents: tuple[DocumentReference, ...] = ()
    relations: tuple[tuple[str, str, str], ...] = ()
    structure_status: str = "til_kontroll"
    professional_status: str = "til_kontroll"
    anomalies: tuple[Anomaly, ...] = ()
    null_reasons: tuple[tuple[str, str], ...] = ()
    format_version: str = FORMAT_VERSION

    def __post_init__(self) -> None:
        if self.dataset not in {"produksjon", "historisk", "prove"}:
            raise ValueError("Ukjent datasett")
        if self.budget_year is not None and (
            type(self.budget_year) is not int or not 1000 <= self.budget_year <= 9999
        ):
            raise ValueError("Budsjettår må være et firesifret heltall")
        reasons = dict(self.null_reasons)
        for field in fields(self):
            if getattr(self, field.name) is None:
                reasons.setdefault(field.name, "ikke oppgitt")
            else:
                reasons.pop(field.name, None)
        object.__setattr__(self, "null_reasons", tuple(sorted(reasons.items())))
        for code in (self.chapter, self.post, self.subpost):
            if code is not None and (
                not isinstance(code, str)
                or not code.isascii()
                or not code.isdigit()
                or str(int(code)) != code
            ):
                raise ValueError("Normalisert kontokode må være desimal tekst uten ledende nuller")
        if self.amount_kr is not None and (
            type(self.amount_kr) is not int or abs(self.amount_kr) > 9_007_199_254_740_991
        ):
            raise ValueError("Kronebeløp må være et Excel-eksakt heltall")
        if (
            self.decision_date is not None
            and date.fromisoformat(self.decision_date).isoformat() != self.decision_date
        ):
            raise ValueError("Vedtaksdato må være ISO-dato")

    @property
    def id(self) -> str:
        return identity(
            self.dataset,
            self.source_system,
            self.source_revision_id,
            self.pointer.locator,
            self.pointer.amount_field,
            self.interpretation_id,
            self.format_version,
        )


@dataclass(frozen=True)
class Extraction:
    dataset: str
    source_system: str
    source_unit_id: str
    source_revision_id: str
    interpretation: Interpretation
    artifact: Artifact
    observations: tuple[AmountObservation, ...]
    anomalies: tuple[Anomaly, ...] = ()
    import_id: str | None = None
    imported_utc: str | None = None

    @property
    def id(self) -> str:
        return identity(
            self.dataset, self.source_system, self.source_revision_id, self.interpretation.id
        )


SCHEMA = """
CREATE TABLE IF NOT EXISTS amount_extractions (
  extraction_id TEXT PRIMARY KEY, dataset TEXT NOT NULL, source_revision_id TEXT NOT NULL,
  interpretation_id TEXT NOT NULL, content_json TEXT NOT NULL, created_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS amount_observations (
  observation_id TEXT PRIMARY KEY,
  extraction_id TEXT NOT NULL REFERENCES amount_extractions(extraction_id),
  content_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS history_calculations (
  calculation_id TEXT PRIMARY KEY, content_json TEXT NOT NULL, created_utc TEXT NOT NULL
);
"""


def initialize_observations(connection: sqlite3.Connection) -> None:
    initialize(connection)
    for statement in SCHEMA.split(";"):
        if statement.strip():
            connection.execute(statement)
    connection.execute("PRAGMA user_version = 3")


def observation_from_dict(data: dict[str, Any]) -> AmountObservation:
    data = dict(data)
    data["pointer"] = SourcePointer(**data["pointer"])
    data["organization"] = Organization(**data["organization"])
    data["documents"] = tuple(DocumentReference(**item) for item in data["documents"])
    data["anomalies"] = tuple(
        Anomaly(**{**item, "affected_fields": tuple(item["affected_fields"])})
        for item in data["anomalies"]
    )
    data["null_reasons"] = tuple(tuple(item) for item in data["null_reasons"])
    data["relations"] = tuple(tuple(item) for item in data["relations"])
    return AmountObservation(**data)


def _extraction_from_dict(data: dict[str, Any]) -> Extraction:
    data = dict(data)
    data["artifact"] = Artifact(**data["artifact"])
    data["interpretation"] = Interpretation(**data["interpretation"])
    data["observations"] = tuple(observation_from_dict(item) for item in data["observations"])
    data["anomalies"] = tuple(
        Anomaly(**{**item, "affected_fields": tuple(item["affected_fields"])})
        for item in data["anomalies"]
    )
    return Extraction(**data)


def save_extraction(database: Path, extraction: Extraction, raw: bytes) -> str:
    """Generisk, atomisk grense. Identisk kilde/tolkning gjenbrukes; ingen overskriving."""
    if (
        hashlib.sha256(raw).hexdigest() != extraction.artifact.sha256
        or len(raw) != extraction.artifact.byte_count
    ):
        raise ValueError("Artefaktens hash/byteantall stemmer ikke")
    seen: set[str] = set()
    for item in extraction.observations:
        if (
            item.dataset,
            item.source_system,
            item.source_unit_id,
            item.source_revision_id,
            item.interpretation_id,
            item.pointer.artifact_id,
        ) != (
            extraction.dataset,
            extraction.source_system,
            extraction.source_unit_id,
            extraction.source_revision_id,
            extraction.interpretation.id,
            extraction.artifact.sha256,
        ) or item.id in seen:
            raise ValueError("Observasjonen har feil grunnlag eller duplisert identitet")
        seen.add(item.id)
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")
        initialize_observations(connection)
        existing = connection.execute(
            "SELECT content_json FROM amount_extractions WHERE extraction_id=?",
            (extraction.id,),
        ).fetchone()
        content = encode(asdict(extraction))
        if existing:
            if existing[0] != content:
                raise ValueError("Uforanderlig tolkning er allerede lagret med annet resultat")
            return extraction.id
        connection.execute(
            "INSERT OR IGNORE INTO sources (sha256, raw_response) VALUES (?, ?)",
            (extraction.artifact.sha256, raw),
        )
        connection.execute(
            "INSERT INTO amount_extractions "
            "(extraction_id,dataset,source_revision_id,interpretation_id,content_json,created_utc) "
            "VALUES (?,?,?,?,?,?)",
            (
                extraction.id,
                extraction.dataset,
                extraction.source_revision_id,
                extraction.interpretation.id,
                content,
                datetime.now(UTC).isoformat(),
            ),
        )
        for item in extraction.observations:
            connection.execute(
                "INSERT INTO amount_observations "
                "(observation_id,extraction_id,content_json) VALUES (?,?,?)",
                (item.id, extraction.id, encode(asdict(item))),
            )
    return extraction.id


def read_extraction(database: Path, extraction_id: str) -> Extraction:
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as connection:
        check_schema(connection)
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE name='amount_extractions'",
        ).fetchone()
        row = (
            connection.execute(
                "SELECT content_json FROM amount_extractions WHERE extraction_id=?",
                (extraction_id,),
            ).fetchone()
            if exists
            else None
        )
    if row is None:
        raise ValueError(f"Ukjent beløpsuttrekk: {extraction_id}")
    return _extraction_from_dict(json.loads(row[0]))


def extract_revision(
    database: Path,
    revision_id: str,
    *,
    interpretation: Interpretation | None = None,
) -> Extraction:
    """Ny adapter over valgt B2-revisjon. B1s parser/resultat/versjon beholdes."""
    interpretation = interpretation or Interpretation()
    if interpretation.adapter_version != ADAPTER_VERSION:
        raise ValueError("Ukjent Storting-adapterversjon")
    revision = read_revision(database, revision_id)
    extraction_id = identity(revision.dataset, "storting", revision_id, interpretation.id)
    try:
        return read_extraction(database, extraction_id)
    except ValueError as error:
        if not str(error).startswith("Ukjent beløpsuttrekk"):
            raise
    report = revision.report
    decision = report.decision
    if decision is None:
        raise ValueError("Valgt B2-revisjon mangler vedtaksmetadata")
    from .storage import read_source

    raw = read_source(database, report.source_sha256)
    artifact = Artifact(
        report.source_sha256,
        f"stortingsvedtak-{decision.session}.xml",
        str(report.source_metadata.get("fixture_kind", "http_original")),
        "text/xml",
        len(raw),
        encode(report.source_metadata),
    )
    document = html.fromstring(decision.html, parser=html.HTMLParser(no_network=True))
    all_text = text(document)
    year_matches = set(re.findall(r"statsbudsjettet for (20\d{2})", all_text, re.I))
    year_evidence = "Uttrykkelig budsjettår i vedtaksteksten"
    if not year_matches:
        year_matches = set(re.findall(r"statsbudsjettet (20\d{2})", decision.title, re.I))
        year_evidence = "Uttrykkelig budsjettår i vedtakstittelen: " + decision.title
    year = int(next(iter(year_matches))) if len(year_matches) == 1 else None
    original = bool(re.search(r"På statsbudsjettet for 20\d{2} bevilges under:", all_text))
    if interpretation.round is not None:
        round_, round_evidence = interpretation.round, interpretation.round_evidence
    elif original:
        round_, round_evidence = "opprinnelig", "Vedtakstekst: bevilges under"
    elif re.search(r"Revidert nasjonalbudsjett", decision.title, re.I):
        round_, round_evidence = "rnb", "Vedtakstittel: " + decision.title
    elif re.search(r"Ny saldering|nysaldering", decision.title, re.I):
        round_, round_evidence = "nysaldering", "Vedtakstittel: " + decision.title
    else:
        round_, round_evidence = "uavklart", None
    observations: list[AmountObservation] = []
    anomalies: list[Anomaly] = []
    unit_id = f"storting:{decision.session}:{decision.id}"
    reference = DocumentReference(
        decision.number,
        "stortingsvedtak_nummer",
        "vedtak",
        "stortingsvedtak",
        decision.number,
        decision.session,
        decision.id,
        decision.url,
        "identifisert",
    )

    def observe(
        locator: str,
        field: str,
        raw_amount: str,
        meaning: str,
        step: str,
        chapter: str,
        post: str,
        chapter_name: str,
        purpose: str,
        raw_row: str,
        *,
        sign: int = 1,
        reasons: tuple[Anomaly, ...] = (),
    ) -> None:
        value = amount(raw_amount)
        if value is None:
            reasons += (
                Anomaly(
                    "ugyldig_belop", "Beløpet er ikke entydige hele kroner", (field,), raw_amount
                ),
            )
        if year is None:
            reasons += (
                Anomaly("uavklart_ar", "Krever ett uttrykkelig budsjettår", ("budget_year",)),
            )
        if not chapter or not 1 <= int(chapter) <= 5999 or not post or not 1 <= int(post) <= 99:
            reasons += (
                Anomaly("uavklart_konto", "Kontoen er utenfor avgrenset bevilgningsmønster"),
            )
        observations.append(
            AmountObservation(
                dataset=revision.dataset,
                source_system="storting",
                source_unit_id=unit_id,
                source_revision_id=revision_id,
                interpretation_id=interpretation.id,
                pointer=SourcePointer(artifact.sha256, locator, field, raw_record=raw_row),
                step_id=step,
                raw_value=raw_amount,
                amount_text=raw_amount,
                amount_kr=None if value is None else sign * value,
                chapter_raw=chapter or None,
                post_raw=post or None,
                chapter=str(int(chapter)) if chapter else None,
                post=str(int(post)) if post else None,
                chapter_name=chapter_name or None,
                purpose=purpose or None,
                detail_level="post",
                budget_year=year,
                year_evidence=year_evidence if year is not None else None,
                decision_date=decision.date,
                decision_session=decision.session,
                api_id=decision.id,
                unit_raw="Kroner",
                currency="NOK",
                multiplier="1",
                precision="Hele kroner",
                conversion_rule=interpretation.normalization_rule,
                normalization_evidence="Kroner i tabellhodet; retningsord i kilderaden",
                figure_type="stortingsvedtak",
                round=round_,
                round_evidence=round_evidence,
                stage_raw=decision.title,
                meaning=meaning,
                scope="enkeltledd",
                classification_evidence="Endelig vedtaksobjekt og avgrenset bevilgningstabell",
                documents=(reference,),
                structure_status="til_kontroll" if reasons else "strukturert",
                professional_status="til_kontroll",
                anomalies=reasons,
                null_reasons=(("subpost", "ikke relevant"), ("proposal_role", "ikke relevant")),
            )
        )

    tables = document.findall(".//table")
    if len(tables) > 1:
        anomalies.append(
            Anomaly("flere_tabeller", "Flere tabeller krever særskilt tolkning", budget_year=year)
        )
        tables = []
    for table_number, table in enumerate(tables, 1):
        rows = table.findall(".//tr")
        headers = [text(cell) for cell in rows[0]] if rows else []
        supported = headers in (
            ["Kap.", "Post", "Formål", "Kroner"],
            ["Kap.", "Post", "Formål", "Kroner", "Kroner"],
            ["Kap.", "Post", "Formål", "", "Kroner"],
            ["Kap.", "Post", "Formål", "", "Kroner", "Kroner"],
        )
        if not supported:
            anomalies.append(
                Anomaly(
                    "ukjent_tabell",
                    "Ukjent tabellhode/enhet",
                    evidence=f"table[{table_number}]",
                    budget_year=year,
                )
            )
            continue
        chapter, chapter_name = "", ""
        last: tuple[str, str, str, str] | None = None
        for number, row in enumerate(rows[1:], 2):
            values = [text(cell) for cell in row]
            locator = f"table[{table_number}]/tr[{number}]"
            raw_row = etree.tostring(row, encoding="unicode", method="html")
            if len(values) == 1 and values[0] in {"Utgifter", "Inntekter"}:
                chapter, chapter_name, last = "", "", None
                continue
            if len(values) != len(headers) or any(
                cell.get("rowspan") or cell.get("colspan", "1") != "1" for cell in row
            ):
                anomalies.append(
                    Anomaly(
                        "ukjent_rad",
                        "Ukjent celleoppsett",
                        evidence=locator,
                        chapter=str(int(chapter)) if chapter else None,
                        post=str(int(last[2])) if last else None,
                        budget_year=year,
                    )
                )
                last = None
                continue
            cap, post, purpose, *amount_cells = values
            if cap.isascii() and cap.isdigit() and not post and purpose and not any(amount_cells):
                chapter, chapter_name, last = cap, purpose, None
                continue
            if not cap and post.isascii() and post.isdigit() and purpose:
                step = identity(unit_id, revision_id, locator)
                populated = [value for value in amount_cells if value]
                reasons: tuple[Anomaly, ...] = ()
                if len(populated) != 1:
                    reasons = (
                        Anomaly(
                            "tvetydig_belopsfelt", "Krever nøyaktig ett postbeløp", evidence=locator
                        ),
                    )
                raw_amount = populated[0] if len(populated) == 1 else " | ".join(populated)
                raw_value = amount(raw_amount)
                increase = bool(re.search(r"(?:økes|auka|aukes)\s+med", purpose))
                decrease = bool(
                    re.search(r"(?:reduseres|redusert|reduserast|minka)\s+med", purpose)
                )
                new = bool(re.search(r"bevilges\s+med", purpose))
                if original and not (increase or decrease or new):
                    meaning, sign = "nivaa", 1
                elif (increase + decrease + new) == 1:
                    meaning, sign = "endring", -1 if decrease else 1
                    if raw_value is not None and raw_value < 0:
                        reasons += (
                            Anomaly("motstrid_fortegn", "Retningsord med negativt råbeløp"),
                        )
                else:
                    meaning, sign = "uavklart", 1
                    reasons += (
                        Anomaly(
                            "ukjent_ledd", "Ingen entydig nivå-/endringstolkning", evidence=purpose
                        ),
                    )
                observe(
                    locator,
                    meaning,
                    raw_amount,
                    meaning,
                    step,
                    chapter,
                    post,
                    chapter_name,
                    purpose,
                    raw_row,
                    sign=sign,
                    reasons=reasons,
                )
                last = (step, chapter, post, purpose)
                continue
            if (
                not cap
                and not post
                and re.match(r"fr[ aå]+kr\b|fra kr\b|frå kr\b", purpose)
                and last
            ):
                match = re.fullmatch(r"(?:fra|frå) kr (.*?) til kr (.*)", purpose)
                if match and not any(amount_cells):
                    step, last_chapter, last_post, last_purpose = last
                    for field, raw_amount in zip(
                        ("for_belop", "etter_belop"), match.groups(), strict=True
                    ):
                        observe(
                            locator,
                            field,
                            raw_amount,
                            field,
                            step,
                            last_chapter,
                            last_post,
                            chapter_name,
                            last_purpose,
                            raw_row,
                        )
                    last = None
                    continue
            if purpose in {"Utgifter", "Inntekter", "Totale utgifter", "Totale inntekter"}:
                last = None
                continue
            if last:
                step, last_chapter, last_post, last_purpose = last
                observe(
                    locator,
                    "uavklart",
                    purpose,
                    "uavklart",
                    step,
                    last_chapter,
                    last_post,
                    chapter_name,
                    last_purpose,
                    raw_row,
                    reasons=(
                        Anomaly(
                            "ukjent_ledd",
                            "Utolket etterfølgende rad i samme ledd",
                            evidence=locator,
                        ),
                    ),
                )
            anomalies.append(
                Anomaly(
                    "uklassifisert_rad",
                    "Kilderad er ikke en sikker bevilgningsobservasjon",
                    evidence=locator,
                    chapter=str(int(chapter)) if chapter else None,
                    post=str(int(last[2])) if last else None,
                    budget_year=year,
                )
            )
            last = None
    if not tables:
        code = "mangler_bevilgningstabell" if year_matches else "ingen_bevilgningstabell"
        anomalies.append(
            Anomaly(code, "Fulltekst bevart i B2; ingen bevilgningslinjer tolket", budget_year=year)
        )
    extraction = Extraction(
        revision.dataset,
        "storting",
        unit_id,
        revision_id,
        interpretation,
        artifact,
        tuple(observations),
        tuple(anomalies),
        report.run_id,
        str(report.source_metadata["retrieved_utc"]),
    )
    save_extraction(database, extraction, raw)
    return extraction
