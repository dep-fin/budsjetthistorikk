"""Separat R2-adapter: faste kildebyte, eksakte belegg og avgrensede forskningsroller."""

import gzip
import hashlib
import io
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

from lxml import etree, html

from . import perioderegister as p1
from .komitepilot import LegacyPayloads, _payload, payload_bytes
from .komitepilot_model import Payload, Source
from .observations import encode
from .omtale import identified
from .perioderegister_model import Basis as P1Basis
from .perioderegister_r2_catalog import CATALOG, ROOT
from .perioderegister_r2_model import RULE, Basis, CrossReference, Evidence, Finding, StatusUpdate
from .visningspilot import _xml
from .visningspilot_model import InventoryItem, PilotBasis, PilotDocument, PilotRelation, Statement

MAX_SOURCE = 16 * 1024 * 1024
MAX_ORIGINAL = 32 * 1024 * 1024
NS = {"s": "http://data.stortinget.no"}


def shared_sources(
    old: P1Basis, legacy: LegacyPayloads, previous: PilotBasis | None
) -> dict[str, tuple[str, bytes, str]]:
    result = p1.shared_sources(old.t4_basis, legacy, previous)
    payloads = {p.id: payload_bytes(p, legacy) for p in old.payloads + old.t4_basis.payloads}
    for source in old.sources:
        if source.payload_id in payloads:
            result[source.name] = (source.id, payloads[source.payload_id], source.status)
    return result


def representation(raw: bytes, name: str) -> bytes:
    pin, count, expanded_pin, expanded_count, _ = CATALOG[name]
    if len(raw) != count or hashlib.sha256(raw).hexdigest() != pin:
        raise ValueError("P2-kildebyte avviker fra fast katalog")
    if not name.endswith(".gz"):
        return raw
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as handle:
        body = handle.read(MAX_ORIGINAL + 1)
    if len(body) > MAX_ORIGINAL or len(body) != expanded_count:
        raise ValueError("P2-original overstiger 32 MiB/har feil størrelse")
    if hashlib.sha256(body).hexdigest() != expanded_pin:
        raise ValueError("P2-representasjon avviker")
    return body


def _source(name: str, digest: str | None, raw: bytes | None) -> Source:
    pin, count, expanded, expanded_count, record = CATALOG[name]
    status = (
        "mangler"
        if raw is None
        else "kildeverifisert"
        if len(raw) == count and hashlib.sha256(raw).hexdigest() == pin
        else "motstrid"
    )
    transport = json.loads(record) if record not in {"register", "gjenbrukt"} else record
    if status == "kildeverifisert" and isinstance(transport, dict):
        if transport["http_complete"] is False:
            status = "bevart_ufullstendig"
    mime = (
        "application/gzip"
        if name.endswith(".gz")
        else "application/json"
        if name.endswith(".json")
        else "text/html"
    )
    return identified(
        "periodekilde-r2-1",
        Source(
            "",
            name,
            "r2-54",
            mime,
            pin,
            digest,
            status,
            encode(
                {
                    "repository_path": name,
                    "byte_count": count,
                    "representation_sha256": expanded or pin,
                    "decompressed_byte_count": expanded_count if name.endswith(".gz") else None,
                    "source_record": transport,
                }
            ),
        ),
    )


def import_basis(
    root: Path, old: P1Basis, legacy: LegacyPayloads = (), previous: PilotBasis | None = None
) -> Basis:
    shared = shared_sources(old, legacy, previous)
    old_digests = {hashlib.sha256(raw).hexdigest() for _, raw, _ in shared.values()}
    payloads: dict[str, Payload] = {}
    sources = []
    for name, (pin, *_rest) in CATALOG.items():
        if name in shared and hashlib.sha256(shared[name][1]).hexdigest() == pin:
            continue
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("P2-kilde utenfor valgt rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(MAX_SOURCE + 1)
            if len(raw) > MAX_SOURCE:
                raise ValueError("P2-payload overstiger 16 MiB")
            payload = _payload(raw, legacy)
            if payload.id not in old_digests:
                payloads.setdefault(payload.id, payload)
            sources.append(_source(name, payload.id, raw))
        except (OSError, ValueError):
            sources.append(_source(name, None, None))
    return structure_basis(old, tuple(payloads.values()), tuple(sources), legacy, previous)


def _norm(node: etree._Element) -> str:
    return " ".join("".join(node.itertext()).split())


def _html(raw: bytes | str) -> html.HtmlElement:
    return html.fromstring(
        raw.decode("utf8") if isinstance(raw, bytes) else raw,
        parser=html.HTMLParser(no_network=True),
    )


def _evidence(row: dict[str, Any], sid: str, raw: bytes) -> Evidence:
    if hashlib.sha256(raw).hexdigest() != row["body_sha256"]:
        raise ValueError("P2-belegg har feil originalrepresentasjon")
    doc = _xml(raw) if row["kind"] == "xml" else _html(raw)
    nodes = doc.xpath(row["xpath"], namespaces=NS)
    if len(nodes) != 1:
        raise ValueError("P2-lokator er ikke entydig")
    node = nodes[0]
    nested = row.get("nested_html_field_xpath")
    if nested:
        fields = node.xpath(nested, namespaces=NS)
        if len(fields) != 1 or not fields[0].text:
            raise ValueError("P2s indre HTML-felt mangler")
        node = _html(fields[0].text)
    text = _norm(node)
    if text != row["text"]:
        raise ValueError("P2-belegg avviker fra originalens tekst")
    rows = None
    if "rows" in row:
        rows = [[_norm(c) for c in r.xpath("./td|./th")] for r in node.xpath(".//tr")]
        if rows != row["rows"]:
            raise ValueError("P2-beleggets råceller avviker")
    return identified(
        "periodebevis-r2-1",
        Evidence(
            "",
            row["id"],
            sid,
            row["xpath"],
            nested,
            row["body_sha256"],
            row["kind"],
            row.get("role"),
            text,
            encode(rows) if rows is not None else None,
        ),
    )


@lru_cache(maxsize=2)
def structure_basis(
    old: P1Basis,
    payloads: tuple[Payload, ...],
    sources: tuple[Source, ...],
    legacy: LegacyPayloads = (),
    previous: PilotBasis | None = None,
) -> Basis:
    shared = shared_sources(old, legacy, previous)
    by_digest = {hashlib.sha256(raw).hexdigest(): raw for _, raw, _ in shared.values()}
    if len(sources) > 128 or len(payloads) > 128:
        raise ValueError("P2-kilder/payloads overstiger ressursgrense 128")
    if len({p.id for p in payloads}) != len(payloads):
        raise ValueError("Duplisert P2-payload")
    for payload in payloads:
        raw = payload_bytes(payload, legacy)
        if payload != _payload(raw, legacy) or payload.id in by_digest:
            raise ValueError("P2-payload dupliserer gammel kilde/har feil identitet")
        by_digest[payload.id] = raw
    names = tuple(
        n
        for n in CATALOG
        if n not in shared or hashlib.sha256(shared[n][1]).hexdigest() != CATALOG[n][0]
    )
    if tuple(s.name for s in sources) != names:
        raise ValueError("P2s faste kildeinventar avviker")
    raw_map = dict(shared)
    issues = []
    for source in sources:
        source_raw = by_digest.get(source.payload_id or "")
        if source != _source(source.name, source.payload_id, source_raw):
            raise ValueError("P2-kilde/metadata/status/identitet avviker fra fast katalog")
        if source.status in {"mangler", "motstrid"}:
            issues.append(source.name + ":" + source.status)
        elif source_raw is not None:
            raw_map[source.name] = (source.id, source_raw, source.status)
    if {s.payload_id for s in sources if s.payload_id} - {
        hashlib.sha256(raw).hexdigest() for _, raw, _ in shared.values()
    } != {p.id for p in payloads}:
        raise ValueError("Ubrukt/ukjent P2-payload")
    bodies = {
        n: (sid, representation(raw, n))
        for n, (sid, raw, _) in raw_map.items()
        if n in CATALOG and hashlib.sha256(raw).hexdigest() == CATALOG[n][0]
    }

    def register(name: str) -> Any:
        item = bodies.get(ROOT + name)
        return json.loads(item[1]) if item else None

    research, ledger, cross, comparison = (
        register(n)
        for n in (
            "evidence.json",
            "treatment-ledger.json",
            "cross-reference-journal.json",
            "source-comparison.json",
        )
    )
    evidence = []
    if research:
        for row in research["evidence"]:
            name = research["sources"][row["source"]]
            if name in bodies:
                sid, raw = bodies[name]
                evidence.append(_evidence(row, sid, raw))
            else:
                issues.append(row["id"] + ":original_mangler")
    proofs = {e.key: e for e in evidence}
    # Samme objekt i to uavhengige HTTP-representasjoner; de rå konvoluttene beholdes.
    if comparison and all(n in bodies for n in comparison["parents"]):
        trees = [_xml(bodies[n][1]) for n in comparison["parents"]]
        for decision in comparison["decisions"]:
            chunks = [
                etree.tostring(
                    t.xpath(
                        "//s:stortingsvedtak[s:id='" + decision["decision_api_id"] + "']",
                        namespaces=NS,
                    )[0],
                    method="c14n",
                )
                for t in trees
            ]
            if (
                chunks[0] != chunks[1]
                or len(chunks[0]) != decision["canonical_bytes"]
                or hashlib.sha256(chunks[0]).hexdigest() != decision["canonical_sha256"]
            ):
                raise ValueError("P2s vedtaksrepresentasjoner avviker")

    old_docs = old.documents + old.t4_basis.documents + (previous.documents if previous else ())
    docs = {d.key: d for d in old_docs}
    documents: list[PilotDocument] = []
    inventory: list[InventoryItem] = []
    statements: list[Statement] = []
    relations: list[PilotRelation] = []
    findings: list[Finding] = []

    def document(
        key: str,
        title: str,
        kind: str,
        date: str,
        accounts: tuple[str, ...],
        names: tuple[str, ...],
        coverage: str,
    ) -> PilotDocument:
        if key not in docs:
            item = identified(
                "periodedokument-r2-1",
                PilotDocument(
                    "",
                    key,
                    title,
                    kind,
                    "2024-2025",
                    date,
                    coverage,
                    "uttrykkelig_R2_delstruktur_ingen_nye_belopshendelser",
                    "ikke_faglig_godkjent",
                    tuple(bodies[n][0] for n in names if n in bodies),
                    accounts,
                ),
            )
            documents.append(item)
            docs[key] = item
        return docs[key]

    def source_names(*names: str) -> tuple[str, ...]:
        return tuple(ROOT + "originals/" + n + ".gz" for n in names)

    prop = document(
        "prop34",
        "Prop. 34 S (2024–2025)",
        "regjeringsforslag",
        "2024-11-29",
        ("1560/71",),
        source_names(
            "prop34-root.html", *(f"prop34-ch{n}.html" for n in range(1, 6)), "prop34.pdf"
        ),
        "komplett_hovedsak_5_HTML_kapitler_og_PDF_hvis_kilder_tilgjengelige",
    )
    committee = document(
        "inns91",
        "Innst. 91 S (2024–2025)",
        "komiteinnstilling",
        "2024-12-10",
        ("1560/71",),
        source_names("inns91.html", "inns91-all.html"),
        "komplett_hovedsak_I_II_og_ulike_merknader_hvis_kilder_tilgjengelige",
    )
    for key, api in (
        ("vedtak230", "40034098"),
        ("vedtak231", "40034099"),
        ("vedtak429", "40034289"),
    ):
        document(
            key,
            "Vedtak " + key.removeprefix("vedtak") + " / " + api,
            "stortingsvedtak",
            "2024-12-19" if key == "vedtak429" else "2024-12-17",
            ("1560/71",) if key == "vedtak230" else (),
            ("docs/research/k3-arsinventar-50/originals/ind-vedtak-2024-2025.xml.gz",),
            "komplett_vedtaksobjekt_hvis_original_tilgjengelig",
        )
    vote = document(
        "votering23887",
        "Sak 101000: debatt og votering 23887",
        "behandling",
        "2024-12-17",
        (),
        source_names(
            "sak101000-retry.xml",
            "voteringer101000.xml",
            "ref171224-debatt6.html",
            "ref171224-votering.html",
            "voteringsvedtak23887.xml",
        ),
        "komplett_avgrenset_sak6_og_voteringsblokk_hvis_kilder_tilgjengelige",
    )
    document(
        "forslag23887",
        "Forslag 40077003/I og 40077004/II",
        "voteringsforslag",
        "2024-12-17",
        ("1560/71",),
        source_names("voteringsforslag23887.xml"),
        "komplett_forslagsrespons_hvis_kilde_tilgjengelig",
    )
    document(
        "inns90",
        "Innst. 90 S (2024–2025): bare fullmaktsgren II",
        "komiteinnstilling",
        "2024-12-13",
        (),
        source_names("inns90-all.html"),
        "hel_innstilling_raabevart_bare_fullmaktII_strukturert",
    )
    document(
        "forslag23945",
        "Forslag 40078386: fullmakt II",
        "voteringsforslag",
        "2024-12-19",
        (),
        source_names("voteringsforslag23945.xml"),
        "komplett_respons_bare_forslag40078386_strukturert",
    )
    document(
        "votering23945",
        "Votering 23945: særskilt fullmakt II",
        "behandling",
        "2024-12-19",
        (),
        source_names("voteringer100289.xml", "voteringsvedtak23945.xml"),
        "komplett_respons_bare_fullmakt429_strukturert",
    )
    index = next(
        (
            c
            for c in old.case_candidates
            if c.case_id == "101000" and c.index_session == "2024-2025" and c.ordinal_1based == 624
        ),
        None,
    )
    key_docs = {
        "INDEX": next((d for d in old_docs if index and d.id == index.document_id), None),
        "PROP-I": prop,
        "PROP-II": prop,
        "KOMITE": committee,
        "BEHANDLING": vote,
        "D230": docs["vedtak230"],
        "D231": docs["vedtak231"],
        "FIN-METODE": docs.get("prop36"),
        "FIN-1429-1": docs.get("prop36"),
        "O1-OMDISPONERING": docs.get("prop16"),
        "FULLMAKT429": docs["vedtak429"],
    }
    actors = {
        "INDEX": "ukjent",
        "PROP-I": "regjeringen",
        "PROP-II": "regjeringen",
        "KOMITE": "samlet komité",
        "BEHANDLING": "stortinget",
        "D230": "stortinget",
        "D231": "stortinget",
        "FIN-METODE": "regjeringen",
        "FIN-1429-1": "regjeringen",
        "O1-OMDISPONERING": "regjeringen",
        "FULLMAKT429": "stortinget",
    }
    for row in ledger["rows"] if ledger else []:
        doc = key_docs[row["id"]]
        if not doc or any(key not in proofs for key in row["evidence_ids"]):
            issues.append(row["id"] + ":funnsgrunnlag_mangler")
            continue
        key = row["id"]
        finding = identified(
            "periodefunn-r2-1",
            Finding(
                "",
                key,
                doc.id,
                row["case_id"],
                row.get("decision_api_id"),
                row["budget_year"],
                tuple(row["accounts"]),
                tuple(row.get("conditional_accounts", [])),
                row.get("transfer_target_year"),
                row["post_link"],
                row["role"],
                actors[key],
                row["status"],
                row["finding"],
                tuple(proofs[k].id for k in row["evidence_ids"]),
                encode(row.get("amounts")),
                ("40077003",)
                if key == "D230"
                else ("40077004",)
                if key == "D231"
                else ("40077003", "40077004")
                if key == "BEHANDLING"
                else ("40078386",)
                if key == "FULLMAKT429"
                else (),
                "23887"
                if key in {"BEHANDLING", "D230", "D231"}
                else "23945"
                if key == "FULLMAKT429"
                else None,
            ),
        )
        findings.append(finding)

    def statement(
        doc: PilotDocument,
        sid: str,
        locator: str,
        text: str,
        role: str,
        actor: str,
        accounts: tuple[str, ...] = (),
        period: str = "2024",
    ) -> None:
        statements.append(
            identified(
                "periodeutsagn-r2-1",
                Statement(
                    "",
                    doc.id,
                    sid,
                    locator,
                    text,
                    "",
                    role,
                    actor,
                    period,
                    "kildebundet_delstruktur_ingen_ny_vedtaksvirkning",
                    accounts,
                    (doc.title, role),
                ),
            )
        )

    for finding in findings:
        doc = next(d for d in docs.values() if d.id == finding.document_id)
        proof = next(e for e in evidence if e.id == finding.evidence_ids[0])
        statement(
            doc,
            proof.source_id,
            proof.locator,
            finding.reason,
            finding.role,
            finding.actor,
            finding.accounts,
            str(finding.budget_year) if finding.budget_year else "",
        )
    # Full hovedsak bevares i tillegg til de eksakte 74 forskningsbeleggene.
    for n in range(1, 6):
        name = source_names(f"prop34-ch{n}.html")[0]
        if name in bodies:
            sid, raw = bodies[name]
            nodes = _html(raw).xpath("//main")
            if len(nodes) != 1:
                raise ValueError("P2s proposisjon mangler hovedinnhold")
            statement(prop, sid, "//main", _norm(nodes[0]), "komplett_HTML_kapittel", "regjeringen")
    for key, doc_key, actor in (
        ("S-inn91-m1", "inns91", "komiteens gjengivelse"),
        ("S-inn91-m2_1", "inns91", "ulike navngitte merknadsavsendere"),
        ("S-inn91-m2_2", "inns91", "ulike navngitte merknadsavsendere"),
        ("S-inn91-m2_3_1_1", "inns91", "komiteen"),
        ("S-inn91-m3", "inns91", "samlet komité"),
        ("S-debatt6", "votering23887", "ulike navngitte talere"),
        ("R33", "forslag23887", "samlet komité"),
        ("R31", "votering23887", "stortinget"),
        ("R24", "prop36", "regjeringen"),
        ("R25", "inns90", "samlet komité"),
        ("R38", "forslag23945", "samlet komité"),
        ("S-vot23945", "votering23945", "stortinget"),
        ("D40034098", "vedtak230", "stortinget"),
        ("D40034099", "vedtak231", "stortinget"),
        ("S-D429", "vedtak429", "stortinget"),
    ):
        if key in proofs and doc_key in docs:
            e = proofs[key]
            statement(docs[doc_key], e.source_id, e.locator, e.text, e.role or "kildebelegg", actor)
    # Eksakte råtabeller og generelle regler har eget inventar, uten AmountObservation.
    for key, doc_key, account, role in (
        ("R36", "prop34", "1560/71", "regjeringsforslag_I_annen_konto"),
        ("R16", "prop34", "", "regjeringsforslag_II_generell_regel"),
        ("R37", "inns91", "1560/71", "samlet_tilråding_I_annen_konto"),
        ("R20", "inns91", "", "samlet_tilråding_II_generell_regel"),
        ("D40034098", "vedtak230", "1560/71", "endelig_vedtak_annen_konto"),
        ("D40034099", "vedtak231", "", "endelig_generell_lønnsregel"),
        ("R28", "prop36", "1429/1", "foreslått_kompensasjonsanslag"),
        ("R24", "prop36", "", "forslag_II_overføringsfullmakt"),
        ("R25", "inns90", "", "tilråding_II_overføringsfullmakt"),
        ("R38", "forslag23945", "", "forslag40078386_fullmaktII"),
        ("S-D429", "vedtak429", "", "overføringsfullmakt_ikke_faktisk_bruk"),
    ):
        if key not in proofs or doc_key not in docs:
            continue
        e = proofs[key]
        chapter, post = account.split("/") if account else ("", "")
        inventory.append(
            identified(
                "periodeinventar-r2-1",
                InventoryItem(
                    "",
                    docs[doc_key].id,
                    e.source_id,
                    e.locator,
                    chapter,
                    post,
                    role,
                    "uttrykkelig_delstruktur_ingen_ny_belopsobservasjon",
                    e.rows_json or e.text,
                    2024,
                    (),
                ),
            )
        )
    if "R28" in proofs:
        e = proofs["R28"]
        name = research["sources"]["prop36-ch11.html"]
        table_doc = _html(bodies[name][1])
        cell = e.locator + "/td[4]"
        raw_amount = _norm(table_doc.xpath(cell)[0])
        chapter = _norm(table_doc.xpath(proofs["R27"].locator + "/td[1]")[0])
        post = _norm(table_doc.xpath(e.locator + "/td[2]")[0])
        units = table_doc.xpath("//table//th")
        if (
            chapter != "1429"
            or post != "1"
            or raw_amount.replace(" ", "") != "2796000"
            or not any(_norm(n) == "Kroner" for n in units)
        ):
            raise ValueError("P2s direkte kompensasjonsanslag har feil post/enhet/verdi")
        statement(
            docs["prop36"],
            e.source_id,
            cell,
            raw_amount,
            "foreslått_kompensasjonsanslag_kroner",
            "regjeringen",
            ("1429/1",),
        )

    def relation(
        left: str, right: str, role: str, keys: tuple[str, ...], accounts: tuple[str, ...] = ()
    ) -> None:
        if left not in docs or right not in docs or any(k not in proofs for k in keys):
            return
        relations.append(
            identified(
                "perioderelasjon-r2-1",
                PilotRelation(
                    "",
                    docs[left].id,
                    docs[right].id,
                    role,
                    "2024; uttrykkelig gren; generell regel/fullmakt har "
                    "ukjent faktisk postvirkning",
                    "kildebundet_ingen_ny_monetær_hendelse",
                    accounts,
                    tuple(proofs[k].id for k in keys),
                    2024,
                ),
            )
        )

    relation(
        "prop34",
        "inns91",
        "forslag_I_og_II_til_tilråding",
        ("R36", "R37", "S-inn91-m3"),
        ("1560/71",),
    )
    relation(
        "inns91",
        "forslag23887",
        "tilråding_I_II_til_forslag40077003_40077004",
        ("R33", "S-inn91-m3"),
        ("1560/71",),
    )
    relation("forslag23887", "votering23887", "I_II_votering23887_sentinel_minus1", ("R31", "R33"))
    relation("votering23887", "vedtak230", "I_40077003_til_230", ("R32", "D40034098"), ("1560/71",))
    relation(
        "votering23887", "vedtak231", "II_40077004_til_231_generell_regel", ("R32", "D40034099")
    )
    relation("prop36", "inns90", "fullmaktsforslag_II_til_tilråding_II", ("R24", "R25"))
    relation("inns90", "forslag23945", "tilråding_II_til_forslag40078386", ("R25", "R38"))
    relation("forslag23945", "votering23945", "fullmaktII_i_votering23945", ("R38", "S-vot23945"))
    relation("votering23945", "vedtak429", "II_til_429_overføringsmål2025", ("R35", "S-D429"))
    relation(
        "prop34",
        "prop36",
        "uttrykkelig_kildehenvisning_ikke_postvis_vedtak",
        ("R11", "FIN-kap5-p4"),
    )
    relation(
        "prop16",
        "prop36",
        "lønnshenvisning_separate_bevisroller",
        ("O1-kap2-p24", "R28"),
        ("1429/1",),
    )
    relation(
        "prop16",
        "vedtak210",
        "eksisterende_omdisponering_ikke_ny_hendelse",
        ("O1-kap2-p24", "O1-kap2-p25"),
        ("1429/1", "1429/22"),
    )
    cross_references = (
        tuple(
            identified(
                "periodekryssreferanse-r2-1",
                CrossReference(
                    "",
                    r["id"],
                    r["from"],
                    r["target"],
                    r["status"],
                    r["result"],
                    tuple(proofs[k].id for k in r["evidence_ids"]),
                ),
            )
            for r in cross["references"]
            if all(k in proofs for k in r["evidence_ids"])
        )
        if cross
        else ()
    )
    status: tuple[StatusUpdate, ...] = ()
    if index and all(k in {f.key for f in findings} for k in ("D230", "D231", "FULLMAKT429")):
        status = (
            identified(
                "periodestatus-r2-1",
                StatusUpdate(
                    "",
                    index.id,
                    index.case_id,
                    index.index_session,
                    index.ordinal_1based,
                    "hovedsak_undersokt_faktisk_postvirkning_uavklart",
                    "Hovedsak 101000 undersøkt separat: 230 gjelder 1560/71; "
                    "231 og 429 har uavklart faktisk anvendelse. "
                    "Historisk kandidatstatus, 67/66/60/25 og R1–R7 beholdes.",
                    tuple(proofs[k].id for k in ("IDX624", "D40034098", "D40034099", "S-D429")),
                ),
            ),
        )
    return identified(
        "periodegrunnlag-r2-1",
        Basis(
            "",
            RULE,
            old,
            payloads,
            sources,
            tuple(evidence),
            tuple(documents),
            tuple(inventory),
            tuple(statements),
            tuple(relations),
            tuple(findings),
            status,
            cross_references,
            tuple(issues),
        ),
    )


def validate_basis(
    basis: Basis, legacy: LegacyPayloads = (), previous: PilotBasis | None = None
) -> None:
    if any(
        len(items) > cap
        for items, cap in (
            (basis.sources, 128),
            (basis.payloads, 128),
            (basis.evidence, 128),
            (basis.findings, 32),
            (basis.status_updates, 1),
            (basis.cross_references, 12),
        )
    ) or any(n > 4096 for n in Counter(i.document_id for i in basis.inventory).values()):
        raise ValueError("P2-samling overstiger kontraktens ressursgrense")
    expected = structure_basis(basis.p1_basis, basis.payloads, basis.sources, legacy, previous)
    if basis != expected:
        raise ValueError("P2-grunnlaget avviker fra kilder/år/post/roller/status/lokator/ID-er")
