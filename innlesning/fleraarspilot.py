"""Separate årsgrunnlag: T3-objekter og to 201-nivåer, uten analyseimport."""

import gzip
import hashlib
import io
import json
from functools import lru_cache
from pathlib import Path

from lxml import html

from . import forlopspilot as t3
from .fleraarspilot_model import RULE, Basis
from .komitepilot import LegacyPayloads, _payload, payload_bytes
from .komitepilot_model import Payload, Source
from .observations import AmountObservation, Interpretation, SourcePointer, encode, identity
from .omtale import compact, identified
from .visningspilot import _doc, _xml
from .visningspilot_model import (
    InventoryItem,
    PilotBasis,
    PilotDocument,
    Statement,
    TreatmentContext,
)

PARENT = t3.ROOT + "session-2024-2025.xml.gz"
META = t3.ROOT + "session-2024-2025.meta.json"
CATALOG = {
    PARENT: (
        "application/gzip",
        "1ea276a5730a5196f4def7471e0bf6ae51a7878a4eac86922cc87a9a71200a6b",
    ),
    META: ("application/json", "4ccc151e0ddd84c11b9c5e973c67762a6470a7bb5f2cd59a542d2847e6c5cd28"),
}
PARENT_SHA = "c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42"
ENVELOPE_SHA = "bd2d50e044e7bbfe1284a8b0dffb5a42ed12412e5b462c61c72614c2d000ee50"
GAPS = (
    "1429/1:kontinuitet_2024_2025_og_oppgaveomfang_ukjent:separate_aarsforlop",
    "1429/22:kontinuitet_2024_2025_og_oppgaveomfang_ukjent:separate_aarsforlop",
    "2025:opprinnelig_forslag_og_tilleggsforslag_mangler",
    "2025:Innst14_og_postvist_vedtakelsesbevis_mangler",
    "2025:rnb_nysaldering_og_ovrige_endringer_ukjent_omfang",
    "2025:vedtak_uten_proposisjon_ikke_undersokt",
    "2025:uttommende_periodeinventar_og_aarsavslutningsavstemming_mangler",
    "2025:1149_ovrige_poster_beviser_ikke_helaarsfravaer_paa_1429_1_22",
    "2025:bare_observerte_opprinnelige_nivaaer:ingen_videreforing_eller_tverraarssum",
)


def parent_bytes(raw: bytes) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as handle:
        expanded = handle.read(t3.MAX_PARENT + 1)
    if len(expanded) != 7479943 or hashlib.sha256(expanded).hexdigest() != PARENT_SHA:
        raise ValueError("T4s dekomprimerte c5f3-forelder avviker")
    return expanded


def derived_xml(parent: bytes) -> bytes:
    if len(parent) != 7479943 or hashlib.sha256(parent).hexdigest() != PARENT_SHA:
        raise ValueError("T4s 201-forelder avviker")
    raw = parent[:317] + parent[5662496:5779401] + b"\n" + parent[7479888:]
    if len(raw) != 117278 or hashlib.sha256(raw).hexdigest() != ENVELOPE_SHA:
        raise ValueError("T4s 201-oppskrift avviker")
    return raw


def _source(name: str, payload: Payload | None, error: str | None = None) -> Source:
    mime, pin = CATALOG[name]
    metadata = {"repository_path": name, "transport_reference": CATALOG[META][1] + "#/"}
    if error:
        metadata["error_type"] = error
    return identified(
        "fleraarskilde-1",
        Source(
            "",
            name,
            "forelder2024",
            mime,
            pin,
            payload.id if payload else None,
            "mangler"
            if payload is None
            else "kildeverifisert"
            if payload.sha256 == pin
            else "motstrid",
            encode(metadata),
        ),
    )


def _derived_source(parent: Source) -> Source:
    return identified(
        "fleraarskilde-1",
        Source(
            "",
            "derived:40034038",
            "vedtak201",
            "application/xml",
            ENVELOPE_SHA,
            parent.payload_id,
            "avledet_kildeverifisert" if parent.status == "kildeverifisert" else "mangler",
            encode(
                {
                    "kind": "avledet_ikke_http",
                    "parent_source_id": parent.id,
                    "parent_sha256": PARENT_SHA,
                    "parent_bytes": 7479943,
                    "prefix_bytes": 317,
                    "object_start_byte_0": 5662496,
                    "object_end_byte_0_exclusive": 5779401,
                    "separator_hex": "0a",
                    "suffix_start_byte_0": 7479888,
                    "research_manifest_sha256": t3.CATALOG[t3.MANIFEST][2],
                }
            ),
        ),
    )


def import_basis(
    root: Path,
    *,
    legacy_json: str = "",
    legacy: LegacyPayloads = (),
    previous: PilotBasis | None = None,
) -> Basis:
    old = t3.import_basis(root, legacy_json=legacy_json, legacy=legacy, previous=previous)
    payloads = {p.id: p for p in old.payloads}
    sources = list(old.sources)
    for name in CATALOG:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("T4-kilde utenfor valgt rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(t3.MAX_SOURCE + 1)
            if len(raw) > t3.MAX_SOURCE:
                raise ValueError("T4-payload overstiger 16 MiB")
            payload = _payload(raw, legacy)
            payloads.setdefault(payload.id, payload)
            source = _source(name, payload)
        except (OSError, ValueError) as error:
            source = _source(name, None, type(error).__name__)
        sources.append(source)
    return structure_basis(tuple(payloads.values()), tuple(sources), legacy_json, legacy, previous)


@lru_cache(maxsize=3)
def structure_basis(
    payloads: tuple[Payload, ...],
    sources: tuple[Source, ...],
    legacy_json: str = "",
    legacy: LegacyPayloads = (),
    previous: PilotBasis | None = None,
) -> Basis:
    count = len(t3.CATALOG) + len(t3.RECIPES)
    if len(payloads) > 64 or len(sources) not in {count + 2, count + 3}:
        raise ValueError("T4-kildeinventar avviker/overstiger kontrakt")
    by_payload = {p.id: p for p in payloads}
    if len(by_payload) != len(payloads):
        raise ValueError("Duplisert T4-payload")
    old_ids = {s.payload_id for s in sources[:count] if s.payload_id}
    old = t3.structure_basis(
        tuple(p for p in payloads if p.id in old_ids),
        sources[:count],
        legacy_json,
        legacy,
        previous,
    )
    extra = sources[count : count + 2]
    if tuple(s.name for s in extra) != tuple(CATALOG):
        raise ValueError("T4-kildekatalog avviker")
    if {s.payload_id for s in sources[: count + 2] if s.payload_id} != set(by_payload):
        raise ValueError("Ubrukt/ukjent T4-payload")
    raws = {p.id: payload_bytes(p, legacy) for p in payloads}
    if any(p != _payload(raws[p.id], legacy) for p in payloads):
        raise ValueError("T4-payload kopierer tidligere original")
    for s in extra:
        metadata = json.loads(s.metadata_json)
        allowed = {"repository_path", "transport_reference"}
        if s.payload_id is None:
            allowed.add("error_type")
        if not isinstance(metadata, dict) or set(metadata) != allowed:
            raise ValueError("T4-metadata avviker")
        error = metadata.get("error_type")
        if s.payload_id is None and (not isinstance(error, str) or not error):
            raise ValueError("T4-kildefravær krever feilkategori")
        if s != _source(s.name, by_payload.get(s.payload_id or ""), error):
            raise ValueError("T4-kildestatus/proveniens/ID avviker")
    derived = _derived_source(extra[0])
    if len(sources) == count + 3 and sources[-1] != derived:
        raise ValueError("T4s 201-forelder/oppskrift avviker")
    sources = sources[: count + 2] + (derived,)
    issues = ["2024:" + issue for issue in old.issues] + list(GAPS)
    issues.extend(s.status + ":" + s.name for s in extra if s.status != "kildeverifisert")
    ready = all(s.status == "kildeverifisert" for s in extra)
    observations, inventory, statements, contexts = [], [], [], []
    doc = identified(
        "fleraarsdokument-1",
        PilotDocument(
            "",
            "vedtak201",
            "Vedtak 201 – statsbudsjettet 2025",
            "stortingsvedtak",
            "2024-2025",
            "2024-12-16",
            "komplett vedtaksobjekt; delvis sesjon; avledet_ikke_http"
            if ready
            else "mangler kilde/transport for komplett vedtaksobjekt",
            "delvis: bare 1429/1 og /22 strukturert; øvrige rader ustrukturert"
            if ready
            else "ustrukturert: kilde/transport mangler",
            "ikke_faglig_godkjent",
            (derived.id,),
            (),
        ),
    )
    if ready:
        parent = parent_bytes(raws[extra[0].payload_id or ""])
        root = _xml(derived_xml(parent))
        nodes = root.xpath('//*[local-name()="stortingsvedtak"]')
        if len(nodes) != 1:
            raise ValueError("T4 krever ett komplett 201-objekt")
        node = nodes[0]
        if (
            t3._field(node, "id") != "40034038"
            or t3._field(node, "sak_id") != "100184"
            or t3._field(root, "sesjon_id") != "2024-2025"
            or t3._field(node, "stortingsvedtak_nummer") != "201"
            or t3._field(node, "stortingsvedtak_dato_tid")[:10] != "2024-12-16"
            or "2025" not in t3._field(node, "stortingsvedtak_tittel")
        ):
            raise ValueError("T4s autoritative 201-identitet/dato/år avviker")
        tree = _doc(t3._field(node, "stortingsvedtak_tekst").encode("utf8"))
        tables = tree.xpath(".//table")
        if len(tables) != 1 or len(tables[0].xpath(".//tr")) != 153:
            raise ValueError("T4s komplette 201-inventar avviker")
        rows = tables[0].xpath(".//tr")
        row_inventory = t3._inventory_rows(rows)
        doc = identified(
            "fleraarsdokument-1",
            PilotDocument(
                "",
                doc.key,
                "Vedtak 201: " + t3._field(node, "stortingsvedtak_tittel"),
                doc.kind,
                doc.session,
                doc.date,
                doc.raw_coverage,
                doc.structured_coverage,
                doc.professional_status,
                doc.source_ids,
                tuple(
                    dict.fromkeys(
                        chapter + "/" + post
                        for _, _, chapter, post, _ in row_inventory
                        if chapter and post
                    )
                ),
            ),
        )
        if "På statsbudsjettet for 2025 bevilges under:" not in compact(tree.text_content()):
            raise ValueError("T4s uttrykkelige 2025-bevilgning mangler")
        full = identified(
            "fleraarsutsagn-1",
            Statement(
                "",
                doc.id,
                derived.id,
                "stortingsvedtak_tekst",
                tree.text_content(),
                html.tostring(tree, encoding="unicode", with_tail=False),
                "fulltekst_delvis_strukturert",
                "stortinget",
                "2025",
                "kildeverifisert",
                (),
                (doc.title, "fulltekst_delvis_strukturert", "stortingsvedtak_tekst"),
            ),
        )
        statements.append(full)
        if compact(rows[99][0].text_content()) != "1429":
            raise ValueError("T4s 201-kapittelgrense avviker")
        for n, post in ((101, "1"), (103, "22")):
            row = rows[n - 1]
            if compact(row[1].text_content()) != post:
                raise ValueError("T4s 201-postlokator avviker")
            value = compact(row[3].text_content())
            interpretation = Interpretation(
                adapter_version=RULE,
                round="opprinnelig",
                round_evidence=doc.title + "; tekst sier budsjett 2025",
                reason="T4: valgt komplett 201-objekt; to eksakte nivåfelt",
            )
            observation = AmountObservation(
                dataset="prove",
                source_system="fleraarspilot",
                source_unit_id=doc.key,
                source_revision_id=derived.expected_sha256,
                interpretation_id=interpretation.id,
                pointer=SourcePointer(
                    derived.expected_sha256,
                    f"table[1]/tr[{n}]/td[4]",
                    "nivaa",
                    raw_record=html.tostring(row, encoding="unicode", with_tail=False),
                ),
                step_id=identity(RULE, doc.id, "1429", post, n),
                raw_value=value,
                amount_text=value,
                amount_kr=int(value.replace(" ", "")),
                chapter_raw="1429",
                post_raw=post,
                chapter="1429",
                post=post,
                chapter_name="Riksantikvaren",
                purpose=compact(row[2].text_content()),
                detail_level="post",
                budget_year=2025,
                year_evidence="Uttrykkelig statsbudsjett 2025 i tittel/vedtakstekst",
                decision_date=doc.date,
                decision_session=doc.session,
                api_id="40034038",
                event_id="201",
                unit_raw="Kroner",
                currency="NOK",
                multiplier="1",
                precision="hele kroner",
                conversion_rule=interpretation.normalization_rule,
                normalization_evidence=derived.id,
                figure_type="stortingsvedtak",
                proposal_identity=doc.id,
                proposal_author="stortinget",
                round="opprinnelig",
                round_evidence=interpretation.round_evidence,
                stage_raw=doc.title,
                meaning="nivaa",
                scope="enkeltledd",
                classification_evidence=derived.id,
                structure_status="strukturert",
                professional_status="ikke_faglig_godkjent",
            )
            observations.append(observation)
            contexts.append(
                identified(
                    "fleraarskontekst-1",
                    TreatmentContext(
                        "",
                        observation.id,
                        doc.id,
                        "opprinnelig",
                        "vedtak",
                        "stortinget",
                        "kildeverifisert",
                        (full.id,),
                    ),
                )
            )
        for n, row, chapter, post, role in row_inventory:
            ids = tuple(
                o.id for o in observations if o.pointer.locator.startswith(f"table[1]/tr[{n}]/")
            )
            inventory.append(
                identified(
                    "fleraarsinventar-1",
                    InventoryItem(
                        "",
                        doc.id,
                        derived.id,
                        f"table[1]/tr[{n}]",
                        chapter,
                        post,
                        "belopsrad" if ids else role,
                        "strukturert" if ids else "ustrukturert",
                        row.text_content(),
                        2025,
                        ids,
                    ),
                )
            )
    else:
        issues.append("2025:201_forelder_eller_transport_mangler:ingen_nye_belop")
    return identified(
        "fleraarsgrunnlag-1",
        Basis(
            "",
            RULE,
            payloads,
            sources,
            old.documents + (doc,),
            old.inventory + tuple(inventory),
            old.statements + tuple(statements),
            old.observations + tuple(observations),
            old.contexts + tuple(contexts),
            old.relations,
            tuple(dict.fromkeys(issues)),
            legacy_json,
        ),
    )


def validate_basis(
    basis: Basis, legacy: LegacyPayloads = (), previous: PilotBasis | None = None
) -> None:
    if any(
        len(items) > cap
        for items, cap in (
            (basis.documents, 16),
            (basis.inventory, t3.MAX_INVENTORY),
            (basis.statements, 512),
            (basis.observations, 256),
            (basis.relations, 1024),
        )
    ):
        raise ValueError("T4-objekter overstiger kontraktens ressursgrense")
    if basis != structure_basis(basis.payloads, basis.sources, basis.legacy_json, legacy, previous):
        raise ValueError("T4-grunnlaget avviker fra kildebyte/år/roller/bevis/ID-er")
