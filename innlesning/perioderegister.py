"""K3s separate, kildebundne registeradapter. Ingen analyse, nett eller database."""

import gzip
import hashlib
import io
import json
import re
from dataclasses import replace
from functools import lru_cache
from pathlib import Path
from typing import Any

from lxml import etree

from .fleraarspilot_model import Basis as T4Basis
from .komitepilot import LegacyPayloads, _payload, payload_bytes
from .komitepilot_model import Payload, Source
from .observations import encode
from .omtale import compact, identified
from .perioderegister_catalog import CATALOG, GAPS, ROOT
from .perioderegister_model import (
    RULE,
    Basis,
    CaseCandidate,
    CoverageGap,
    DecisionCandidate,
    Evidence,
    PeriodEntry,
)
from .visningspilot import _doc, _xml, raw_source
from .visningspilot_model import (
    InventoryItem,
    PilotBasis,
    PilotDocument,
    PilotRelation,
    Statement,
)

MAX_SOURCE = 16 * 1024 * 1024
MAX_ORIGINAL = 32 * 1024 * 1024
MAX_SOURCES = 512
MAX_INVENTORY = 4096  # Per dokument. Ingen gammel grense endres.


def shared_sources(
    t4: T4Basis, legacy: LegacyPayloads, previous: PilotBasis | None
) -> dict[str, tuple[str, bytes, str]]:
    payloads = {p.id: payload_bytes(p, legacy) for p in t4.payloads}
    result = {
        s.name: (s.id, payloads[s.payload_id], s.status)
        for s in t4.sources
        if s.payload_id in payloads and not s.name.startswith("derived:")
    }
    if previous:
        for source in previous.sources:
            raw = raw_source(source)
            if raw is not None:
                result.setdefault(source.name, (source.id, raw, source.status))
    return result


def _source(name: str, payload_id: str | None, raw: bytes | None) -> Source:
    pin, count, expanded, expanded_count, record = CATALOG[name]
    metadata = encode(
        {
            "repository_path": name,
            "byte_count": count,
            "representation_sha256": expanded or pin,
            "decompressed_byte_count": expanded_count or None,
            "source_record": json.loads(record) if record != "register" else "K3-register",
        }
    )
    mime = (
        "application/gzip"
        if name.endswith(".gz")
        else "application/json"
        if name.endswith(".json")
        else "application/xml"
        if name.endswith(".xml")
        else "text/html"
        if name.endswith(".html")
        else "text/plain"
    )
    status = (
        "mangler"
        if raw is None
        else "kildeverifisert"
        if (len(raw) == count and hashlib.sha256(raw).hexdigest() == pin)
        else "motstrid"
    )
    if status == "kildeverifisert" and record != "register":
        transport = json.loads(record)
        if transport.get("http_complete") is False:
            status = "bevart_ufullstendig"
        elif transport.get("status", 200) != 200:
            status = "bevart_feilsvar"
    return identified(
        "periodekilde-1",
        Source("", name, "k3-register", mime, pin, payload_id, status, metadata),
    )


def import_basis(
    root: Path, t4: T4Basis, legacy: LegacyPayloads = (), previous: PilotBasis | None = None
) -> Basis:
    shared = shared_sources(t4, legacy, previous)
    old_payload_ids = {p.id for p in t4.payloads}
    payloads: dict[str, Payload] = {}
    sources = []
    for name in CATALOG:
        if name in shared and hashlib.sha256(shared[name][1]).hexdigest() == CATALOG[name][0]:
            continue
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("P1-kilde utenfor valgt rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(MAX_SOURCE + 1)
            if len(raw) > MAX_SOURCE:
                raise ValueError("P1-payload overstiger 16 MiB")
            payload = _payload(raw, legacy)
            if payload.id not in old_payload_ids:
                payloads.setdefault(payload.id, payload)
            sources.append(_source(name, payload.id, raw))
        except (OSError, ValueError):
            sources.append(_source(name, None, None))
    return structure_basis(t4, tuple(payloads.values()), tuple(sources), legacy, previous)


def representation(raw: bytes, name: str) -> bytes:
    """Arkivhash og dekomprimert representasjon er to ulike bindinger."""
    pin, count, expanded_pin, expanded_count, _ = CATALOG[name]
    if len(raw) != count or hashlib.sha256(raw).hexdigest() != pin:
        raise ValueError("P1-kildebyte avviker fra fast katalog")
    if not name.endswith(".gz"):
        return raw
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as handle:
        result = handle.read(MAX_ORIGINAL + 1)
    if len(result) > MAX_ORIGINAL or (expanded_count and len(result) != expanded_count):
        raise ValueError("P1-original overstiger 32 MiB/har feil størrelse")
    if expanded_pin and hashlib.sha256(result).hexdigest() != expanded_pin:
        raise ValueError("P1-dekomprimert original avviker")
    return result


@lru_cache(maxsize=2)
def structure_basis(
    t4: T4Basis,
    payloads: tuple[Payload, ...],
    sources: tuple[Source, ...],
    legacy: LegacyPayloads = (),
    previous: PilotBasis | None = None,
) -> Basis:
    shared = shared_sources(t4, legacy, previous)
    by_digest = {hashlib.sha256(raw).hexdigest(): raw for _, raw, _ in shared.values()}
    by_digest.update((hashlib.sha256(raw).hexdigest(), raw) for _, raw in legacy)
    old_payload_ids = {p.id for p in t4.payloads}
    if len(sources) > MAX_SOURCES or len(payloads) > MAX_SOURCES:
        raise ValueError("P1-kilder overstiger 512")
    if len({p.id for p in payloads}) != len(payloads):
        raise ValueError("Duplisert P1-payload")
    for payload in payloads:
        payload_raw = payload_bytes(payload, legacy)
        if payload != _payload(payload_raw, legacy) or payload.id in old_payload_ids:
            raise ValueError("P1-payload dupliserer gammel kilde")
        by_digest[payload.id] = payload_raw
    names = tuple(
        n
        for n in CATALOG
        if n not in shared or hashlib.sha256(shared[n][1]).hexdigest() != CATALOG[n][0]
    )
    if tuple(s.name for s in sources) != names:
        raise ValueError("P1s faste kildeinventar avviker")
    expected_payloads = {s.payload_id for s in sources if s.payload_id} - old_payload_ids
    if expected_payloads != {p.id for p in payloads}:
        raise ValueError("Ubrukt/ukjent P1-payload")
    raw_map = dict(shared)
    issues = []
    for source in sources:
        raw = by_digest.get(source.payload_id or "")
        if source != _source(source.name, source.payload_id, raw):
            raise ValueError("P1-kilde/forelder/status/identitet avviker fra fast katalog")
        if source.status in {"mangler", "motstrid"}:
            issues.append(source.name + ":" + source.status)
        elif raw is not None:
            raw_map[source.name] = (source.id, raw, source.status)
    # Egen port for store gzip-originaler; gammel 16 MiB-HTML-port brukes aldri.
    representations = {
        n: (sid, representation(raw, n))
        for n, (sid, raw, _) in raw_map.items()
        if n in CATALOG and hashlib.sha256(raw).hexdigest() == CATALOG[n][0]
    }
    evidence: dict[str, Evidence] = {}

    def proof(name: str, locator: str, role: str) -> tuple[str, ...]:
        if name not in representations:
            issues.append(name + ":bevis_mangler:" + role)
            return ()
        sid, raw = representations[name]
        item = identified(
            "periodebevis-1", Evidence("", sid, locator, hashlib.sha256(raw).hexdigest(), role)
        )
        evidence.setdefault(item.id, item)
        return (item.id,)

    def register(name: str) -> Any:
        source_name = ROOT + name
        if source_name not in representations:
            return None
        return json.loads(representations[source_name][1])

    gaps = tuple(
        identified(
            "periodehull-1",
            CoverageGap(
                "",
                key,
                title,
                "open",
                reason,
                proof(ROOT + "m21.md", "table:" + key, "global_rest"),
            ),
        )
        for key, title, reason in GAPS
    )
    old_docs = t4.documents + (previous.documents if previous else ())
    old_observations = t4.observations + (previous.observations if previous else ())
    docs_by_key = {d.key: d for d in old_docs}
    new_documents: dict[str, PilotDocument] = {}
    inventory: list[InventoryItem] = []
    statements: list[Statement] = []
    relations: list[PilotRelation] = []

    def document(
        key: str,
        title: str,
        kind: str,
        session: str,
        date: str,
        accounts: tuple[str, ...],
        refs: tuple[str, ...],
    ) -> PilotDocument:
        if key in docs_by_key:
            return docs_by_key[key]
        if key not in new_documents:
            new_documents[key] = identified(
                "periodedokument-1",
                PilotDocument(
                    "",
                    key,
                    title,
                    kind,
                    session,
                    date,
                    "komplett_indeksobjekt_fulltekst_mangler"
                    if kind == "indekskandidat"
                    else "registerpassasjer_og_originalreferanser_delvis",
                    "delvis_registerstrukturert",
                    "ikke_faglig_godkjent",
                    refs,
                    accounts,
                ),
            )
        return new_documents[key]

    def statement(
        doc: PilotDocument,
        sid: str,
        locator: str,
        text: str,
        role: str,
        actor: str = "ukjent",
        accounts: tuple[str, ...] = (),
        period: str = "",
    ) -> None:
        statements.append(
            identified(
                "periodeutsagn-1",
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
                    "kildebundet_delvis_strukturert",
                    accounts,
                    (doc.title, role, locator),
                ),
            )
        )

    ledger = register("known-period-ledger.json")
    decisions = register("decision-register.json")
    journal = register("coverage-journal.json")
    candidates = register("case-candidates.json")
    decision_evidence = register("decision-evidence.json")
    tables = register("table-locators.json")
    voting = register("voting-evidence.json")
    if any(value is None for value in (ledger, decisions, journal, candidates, decision_evidence)):
        issues.append("registergrunnlag_mangler:ingen_konstruerte_kandidater_eller_postkoblinger")
        ledger, decisions, journal, candidates, decision_evidence = None, [], None, [], []
    entries: list[PeriodEntry] = []
    decision_candidates: list[DecisionCandidate] = []
    case_candidates: list[CaseCandidate] = []
    by_api = {row["id"]: row for row in decisions or []}
    by_decision_evidence = {row["id"]: row for row in decision_evidence or []}
    entry_docs: dict[str, PilotDocument] = {}
    mapping = {
        "original-proposal": "prop1",
        "original-recommendation": "inns14",
        "original-H": "inns14",
        "original-FrP": "inns14",
        "original-341": "vedtak341",
        "original-346": "vedtak346",
        "rnb-proposal": "prop104",
        "rnb-recommendation": "inns447",
        "rnb-857": "vedtak857",
        "nysald-proposal": "prop16",
        "nysald-recommendation": "inns81",
        "nysald-210": "vedtak210",
        "nysald-211": "vedtak211",
        "annual-control": "prop36",
    }
    source_names = {
        "prop1": "prop1-kld-ch6.html",
        "inns14": "inns14-202324.html",
        "prop104": "prop104-ch5.html",
        "inns447": "ind-inns447.html",
        "prop36": "prop36-ch13.html",
    }
    for n, row in enumerate(ledger["rows"] if ledger else []):
        key, role = row["id"], row["role"]
        doc_key = mapping.get(key, "inns447")
        api = row["document"].split("/")[-1] if "/400" in row["document"] else None
        reg = by_api.get(api or "", {})
        accounts = tuple("1429/" + str(p) for p in row["posts"])
        ids = proof(ROOT + "known-period-ledger.json", f"/rows/{n}", role)
        raw_name = source_names.get(doc_key)
        if raw_name:
            ids += proof(ROOT + "originals/" + raw_name + ".gz", "/", "originalreferanse")
        if api in by_decision_evidence:
            d = by_decision_evidence[api]
            ids += proof(d["source_path"], d["xml_locator"], "vedtaksoriginal")
        for table_index, table in enumerate(tables or []):
            if table["source"] == raw_name or (
                doc_key == "prop36" and table["source"] == "prop36-ch10.html"
            ):
                ids += proof(ROOT + "table-locators.json", f"/{table_index}", "tabellbevis")
                ids += proof(
                    ROOT + "originals/" + table["source"] + ".gz",
                    table["table_xpath"],
                    "hashbundet_tabellokator",
                )
        if row.get("vote") and voting:
            for vote_index, vote in enumerate(voting["votes"]):
                if vote["fields"]["votering_id"] == row["vote"]:
                    ids += proof(ROOT + "voting-evidence.json", f"/votes/{vote_index}", "votering")
                    ids += proof(
                        ROOT + "originals/" + vote["source"] + ".gz",
                        vote["xpath"],
                        "voteringsoriginal",
                    )
            for link_index, link in enumerate(voting["decision_links"]):
                if api and link["fields"]["vedtak_nummer"] == reg["number"]:
                    ids += proof(
                        ROOT + "voting-evidence.json",
                        f"/decision_links/{link_index}",
                        "saerskilt_vedtakskobling",
                    )
                    ids += proof(
                        ROOT + "originals/" + link["source"] + ".gz",
                        link["xpath"],
                        "saerskilt_vedtaksoriginal",
                    )
            for proposal_index, proposal in enumerate(voting["proposals"]):
                if row.get("proposal") == proposal["proposal_id"]:
                    ids += proof(
                        ROOT + "voting-evidence.json",
                        f"/proposals/{proposal_index}",
                        "saerskilt_forslagskobling",
                    )
                    ids += proof(
                        ROOT + "originals/" + proposal["source"] + ".gz",
                        proposal["xml_xpath"],
                        "saerskilt_forslagsoriginal",
                    )
        doc = document(
            doc_key,
            row["document"],
            "registerdokument",
            reg.get("session", ""),
            reg.get("date", "")[:10],
            accounts,
            tuple(dict.fromkeys(evidence[i].source_id for i in ids)),
        )
        entry_docs[key] = doc
        actor = str(
            row.get("party")
            or (
                "H"
                if key == "original-H"
                else "FrP"
                if key == "original-FrP"
                else "regjeringen"
                if role == "government_proposal"
                else "stortinget"
                if role.startswith("adopted")
                else "komiteen"
                if role == "committee_recommendation"
                else "ukjent"
            )
        )
        round_name = (
            "opprinnelig"
            if key.startswith("original")
            else "rnb"
            if key.startswith("rnb")
            else "nysaldering"
            if key.startswith("nysald")
            else "kontroll"
        )
        status = (
            "forkastet"
            if role == "rejected_alternative_proposal"
            else "primaervotering_ukjent"
            if key in {"original-H", "original-FrP"}
            else "vedtatt_fullmakt_uten_belop"
            if key == "original-346"
            else "kildebundet_delvis_strukturert"
        )
        observations = tuple(
            o.id
            for o in old_observations
            if api in {"40032928", "40033719", "40034048"} and o.api_id == api
        )
        events = tuple(dict.fromkeys(o.step_id for o in old_observations if o.id in observations))
        entry = identified(
            "periodeledd-1",
            PeriodEntry(
                "",
                key,
                doc.id,
                api,
                reg.get("case"),
                row["budget_year"],
                accounts,
                "proven_selected"
                if any(a in {"1429/1", "1429/22"} for a in accounts)
                else "proven_other_scope",
                role,
                round_name,
                actor,
                status,
                encode(row),
                tuple(dict.fromkeys(ids)),
                observations,
                events,
                "ikke_faglig_godkjent",
            ),
        )
        entries.append(entry)
        if doc.id not in {d.id for d in old_docs}:
            statement(
                doc,
                evidence[ids[0]].source_id,
                f"/rows/{n}",
                encode(row),
                role,
                actor,
                accounts,
                str(row["budget_year"]),
            )
            # Vis de komplette K3-bevispassasjene, også originale råtall, uten
            # å strukturere dem til nye AmountObservation-objekter.
            for table in tables or []:
                if table["source"] != raw_name and not (
                    doc_key == "prop36" and table["source"] == "prop36-ch10.html"
                ):
                    continue
                original_name = ROOT + "originals/" + table["source"] + ".gz"
                if original_name not in representations:
                    continue
                sid, _ = representations[original_name]
                statement(
                    doc,
                    sid,
                    table["table_xpath"],
                    encode(table),
                    "kildebevispassasje_delvis_strukturert",
                    "ukjent",
                    (),
                    "2024",
                )
                for raw_row in table["rows"]:
                    inventory.append(
                        identified(
                            "periodeinventar-1",
                            InventoryItem(
                                "",
                                doc.id,
                                sid,
                                raw_row["xpath"],
                                "",
                                "",
                                "kildebevisrad",
                                "raaceller_ikke_normalisert",
                                encode(raw_row),
                                2024,
                                (),
                            ),
                        )
                    )
        if key == "original-346" and api in by_decision_evidence:
            d = by_decision_evidence[api]
            if d["source_path"] in representations:
                sid, raw = representations[d["source_path"]]
                node = _xml(raw).xpath(
                    "//*[local-name()='stortingsvedtak'][*[local-name()='id']='40032933']"
                )
                if len(node) != 1:
                    raise ValueError("P1s komplette 346-objekt mangler")
                texts = node[0].xpath("./*[local-name()='stortingsvedtak_tekst']/text()")
                full = str(texts[0]) if len(texts) == 1 else ""
                if hashlib.sha256(full.encode()).hexdigest() != d["text_sha256_utf8"]:
                    raise ValueError("346-fullmaktsteksten avviker")
                statement(
                    doc,
                    sid,
                    d["xml_locator"],
                    etree.tostring(node[0]).decode(),
                    "komplett_vedtaksobjekt_fullmakt",
                    "stortinget",
                    accounts,
                    "2024",
                )
                tree = _doc(full.encode())
                inventory.append(
                    identified(
                        "periodeinventar-1",
                        InventoryItem(
                            "",
                            doc.id,
                            sid,
                            d["xml_locator"],
                            "",
                            "",
                            "fullmakt_fulltekst",
                            "strukturert_fullmakt_ingen_belopsobservasjon",
                            compact(tree.text_content()),
                            2024,
                            (),
                        ),
                    )
                )
                for account in ("1429/1", "4429/2", "4429/9", "1633/1"):
                    chapter, post = account.split("/")
                    inventory.append(
                        identified(
                            "periodeinventar-1",
                            InventoryItem(
                                "",
                                doc.id,
                                sid,
                                d["xml_locator"],
                                chapter,
                                post,
                                "fullmakt_kontohenvisning",
                                "strukturert_tekst_ikke_belop",
                                compact(tree.text_content()),
                                2024,
                                (),
                            ),
                        )
                    )
                new_documents[doc.key] = identified(
                    "periodedokument-1",
                    replace(
                        doc,
                        id="",
                        raw_coverage="komplett_vedtaksobjekt",
                        accounts=("1429/1", "4429/2", "4429/9", "1633/1"),
                    ),
                )
                updated = new_documents[doc.key]
                entries[-1] = identified(
                    "periodeledd-1", replace(entry, id="", document_id=updated.id)
                )
                statements[:] = [
                    identified("periodeutsagn-1", replace(s, id="", document_id=updated.id))
                    if s.document_id == doc.id
                    else s
                    for s in statements
                ]
                inventory[:] = [
                    identified("periodeinventar-1", replace(i, id="", document_id=updated.id))
                    if i.document_id == doc.id
                    else i
                    for i in inventory
                ]
                entry_docs[key] = updated
    for n, row in enumerate(journal["decisions"] if journal else []):
        api, session = row["id"], row["session"]
        reg = by_api[api]
        d = by_decision_evidence[api]
        ids = proof(ROOT + "coverage-journal.json", f"/decisions/{n}", "inkludering_ekskludering")
        ids += proof(ROOT + "decision-register.json", "/" + str(decisions.index(reg)), "autoritet")
        ids += proof(d["source_path"], d["xml_locator"], "vedtaksoriginal")
        # Bare dokumentert innledning/omfang kan gi år og kontopar.
        text = d.get("full_text", d["opening_text"])
        years = re.findall(
            r"(?:statsbudsjett(?:et)?(?:\s*for)?|[Ss]valbardbudsjett(?:et)?(?:\s*for)?|"
            r"budsjettåret|\bi)\s*(202[345])\b",
            text,
        )
        year = (
            int(years[0])
            if years
            else (
                2024
                if row["status"]
                in {"include_monetary", "include_authorization", "include_authorization_other_post"}
                else None
            )
        )
        found = next((e for e in entries if e.decision_api_id == api), None)
        accounts = found.accounts if found else ()
        if not accounts:
            pairs = []
            for block in d["chapter_blocks"]:
                chapter = ""
                for cell_row in block["rows"]:
                    cells = cell_row["cells"]
                    if len(cells) >= 2:
                        if cells[0].isdigit() and 3 <= len(cells[0]) <= 4:
                            chapter = cells[0]
                        if chapter and cells[1].isdigit() and 1 <= len(cells[1]) <= 2:
                            pairs.append(chapter + "/" + str(int(cells[1])))
            pairs.extend(
                chapter + "/" + str(int(post))
                for chapter, post in re.findall(r"kap\.\s*(\d{3,4})\s+post\s+(\d{1,2})\b", text)
            )
            accounts = tuple(dict.fromkeys(pairs))
        if found:
            year = found.budget_year
        doc = document(
            "vedtak" + reg["number"],
            "Vedtak " + reg["number"] + ": " + reg["title"],
            "vedtaksregister",
            session,
            reg["date"][:10],
            accounts,
            tuple(dict.fromkeys(evidence[i].source_id for i in ids)),
        )
        link = (
            "proven_selected"
            if row["post_link"] == "proven_selected"
            else ("proven_other_scope" if row["status"].startswith("exclude_") else "unknown")
        )
        decision_candidates.append(
            identified(
                "periodevedtakskandidat-1",
                DecisionCandidate(
                    "",
                    session,
                    api,
                    reg["number"],
                    doc.id,
                    year,
                    accounts,
                    link,
                    row["status"],
                    row["reason"],
                    row["raw_preservation"],
                    row["product_structuring"],
                    row["professional_approval"],
                    row["monetary_effect"],
                    ids,
                ),
            )
        )
        if doc.id not in {d.id for d in old_docs}:
            statement(
                doc,
                evidence[ids[0]].source_id,
                f"/decisions/{n}",
                encode({"journal": row, "identity": reg, "evidence": d}),
                "vedtaksregister",
            )
    for n, row in enumerate(candidates or []):
        session, ordinal, metadata = row["session"], row["ordinal_1based"], row["metadata"]
        name = ROOT + "originals/saker-" + session + ".xml.gz"
        ids = proof(ROOT + "case-candidates.json", "/" + str(n), "sakskandidat")
        ids += proof(name, f"/*/*[3]/*[{ordinal}]", "komplett_indeksobjekt")
        doc = document(
            f"indeks-{session}-{ordinal}",
            (metadata["henvisning"] or "Ukjent henvisning") + ": " + metadata["tittel"],
            "indekskandidat",
            session,
            "",
            (),
            tuple(dict.fromkeys(evidence[i].source_id for i in ids)),
        )
        case_candidates.append(
            identified(
                "periodesakskandidat-1",
                CaseCandidate(
                    "",
                    session,
                    ordinal,
                    metadata["id"],
                    doc.id,
                    encode(metadata),
                    None,
                    (),
                    "unknown",
                    row["status"],
                    row["reason"],
                    ids,
                ),
            )
        )
        # CaseCandidate ER det komplette indeksinventaret. Ingen InventoryItem med
        # oppdiktet år 0/2024 lages; indeksåret er en egen, kildebegrunnet sesjon.
        if name in representations:
            sid, raw = representations[name]
            nodes = _xml(raw).xpath(f"/*/*[3]/*[{ordinal}]")
            if len(nodes) != 1:
                raise ValueError("P1s indeksordinal mangler i originalen")
            fields = {etree.QName(child).localname: child.text for child in nodes[0]}
            if any(fields.get(key) != value for key, value in metadata.items()):
                raise ValueError("P1s komplette indeksmetadata avviker fra originalen")
            statement(
                doc,
                sid,
                f"/*/*[3]/*[{ordinal}]",
                etree.tostring(nodes[0]).decode(),
                "komplett_indeksobjekt_fulltekst_mangler",
            )
        else:
            statement(
                doc,
                evidence[ids[0]].source_id,
                "/" + str(n),
                encode(metadata),
                "indeksmetadata_original_mangler_fulltekst_mangler",
            )
    # Dokumenterte ledd bindes gjennom registerbevis; ingen ny monetær virkning.
    for left_key, right_key in (
        ("original-proposal", "original-recommendation"),
        ("original-recommendation", "original-341"),
        ("original-recommendation", "original-346"),
        ("rnb-proposal", "rnb-recommendation"),
        ("rnb-recommendation", "rnb-857"),
    ):
        left = next((e for e in entries if e.key == left_key), None)
        right = next((e for e in entries if e.key == right_key), None)
        if left and right:
            relations.append(
                identified(
                    "perioderelasjon-1",
                    PilotRelation(
                        "",
                        left.document_id,
                        right.document_id,
                        "kildebundet_registerrelasjon",
                        "uttrykkelig_delvis_postomfang",
                        "kildebundet",
                        tuple(a for a in left.accounts if a in right.accounts),
                        tuple(dict.fromkeys(left.evidence_ids + right.evidence_ids)),
                        2024,
                    ),
                )
            )
    return identified(
        "periodegrunnlag-1",
        Basis(
            "",
            RULE,
            t4,
            payloads,
            sources,
            tuple(evidence.values()),
            tuple(new_documents.values()),
            tuple(dict.fromkeys(inventory)),
            tuple(dict.fromkeys(statements)),
            tuple(relations),
            tuple(entries),
            tuple(case_candidates),
            tuple(decision_candidates),
            gaps,
            tuple(dict.fromkeys(issues)),
        ),
    )


def validate_basis(
    basis: Basis, legacy: LegacyPayloads = (), previous: PilotBasis | None = None
) -> None:
    from collections import Counter

    if any(
        len(items) > cap
        for items, cap in (
            (basis.entries, 256),
            (basis.case_candidates, 67),
            (basis.decision_candidates, 25),
            (basis.gaps, 7),
            (basis.evidence, 4096),
            (basis.sources, MAX_SOURCES),
        )
    ) or any(
        count > MAX_INVENTORY for count in Counter(i.document_id for i in basis.inventory).values()
    ):
        raise ValueError("P1-samling overstiger kontraktens ressursgrense")
    expected = structure_basis(basis.t4_basis, basis.payloads, basis.sources, legacy, previous)
    if basis != expected:
        raise ValueError("P1-grunnlaget avviker fra kilder/år/post/roller/status/lokator/ID-er")
