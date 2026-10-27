"""Avgrenset T2-kildeadapter. Kjøres uten analyse, database, HTTP eller T1-data."""

import base64
import binascii
import gzip
import hashlib
import io
import json
import re
from functools import lru_cache
from pathlib import Path

from lxml import etree, html
from pypdf import PdfReader

from .komitepilot_model import RULE, Basis, Payload, Source
from .observations import AmountObservation, Interpretation, SourcePointer, encode, identity
from .omtale import compact, identified
from .visningspilot import _doc, _hierarchy, _table_groups, _xml
from .visningspilot_model import (
    InventoryItem,
    PilotDocument,
    PilotRelation,
    Statement,
    TreatmentContext,
)

ROOT = "docs/research/to-visninger-37/originals/"
K = ROOT + "komite/"
PARENT = ROOT + "aar/session-2024-2025.xml.gz"
MANIFEST = K + "manifest.json"
PLENUM = "docs/research/omtale-o1/originals/votering-161224.html"
MAX_SOURCE = 16 * 1024 * 1024
MAX_PARENT = 32 * 1024 * 1024
# Uavhengige ankere fra #37; ingen hasher beregnes fra innkommende eksportfelter.
CATALOG = {
    K + "prop25s-ch4.html": (
        "prop25",
        "text/html",
        "17922400028d80971540293ace9d6904d3be86b8d97d880a5b6a18bdd2bb5ecf",
    ),
    K + "prop25s-ch2.html": (
        "prop25",
        "text/html",
        "87205b4e91472cdef72f73abe482d01b1981a8cd4c0f4863951bb8a2d4d20c7b",
    ),
    K + "prop25s.pdf": (
        "prop25",
        "application/pdf",
        "aeb725790fa208766fc15d24082346ce8c5295c26208a04f7b266b2bce37dd1a",
    ),
    K + "inns85s.html": (
        "inns85",
        "text/html",
        "0adeb21331ef20b44186ae6fae539bd304d4e9fe2a22aa64698469c90804c657",
    ),
    K + "inns85s.pdf": (
        "inns85",
        "application/pdf",
        "961591a7f80608e9b15002de1b06f8e51162879b0f0137d0ef38eb3254404288",
    ),
    K + "vedtak40034045-sak100887.html": (
        "vedtak208",
        "text/html",
        "232e06bc5ed62185a856016fea4ed609429d8c654dc3070d8698b3085102c1ab",
    ),
    K + "vedtak40034045.html": (
        "feilet208",
        "text/html",
        "5c7743ddfe2cc62db9db7a993d95d3abb31f55b884dbb7ca2cb1a08c774654ec",
    ),
    K + "sak100887.xml": (
        "sak100887",
        "application/xml",
        "cfaf7b451df64c4a4cad5f437f04a06da0f1e2377159a6cde6cee6ee2f76fb2e",
    ),
    MANIFEST: (
        "transport",
        "application/json",
        "6a9c4b1ca1d8be43cf63e4a66d67d69eb382d375a7248a65cd36a78fc2d19145",
    ),
    PLENUM: (
        "plenum24",
        "text/html",
        "22170a60f769e89642b2e52525899903020de25938aa2b566ea28d11f85fb2e5",
    ),
    PARENT: (
        "forelder2024",
        "application/gzip",
        "1ea276a5730a5196f4def7471e0bf6ae51a7878a4eac86922cc87a9a71200a6b",
    ),
    ROOT + "aar/session-2024-2025.meta.json": (
        "forelder2024",
        "application/json",
        "4ccc151e0ddd84c11b9c5e973c67762a6470a7bb5f2cd59a542d2847e6c5cd28",
    ),
}
PARENT_SHA = "c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42"
# Ingen avledede bytekopier lagres: prefix[0:321]+objekt[start:end]+suffix[-57:].
RECIPES = {
    "40034045": (
        1191752,
        1248367,
        "5f399fc5c9603ea2be74659b40307d31aa7a4b2ce1fa17d053166043f6d33df1",
        "9cc1a9b2406f78cfd3e9ec0c0e57b1145813a53c0a2f409d71d6f6069049b8a1",
    ),
    "40034047": (
        1248373,
        1249810,
        "12850ccf53c91c197562c12e0bdf56f2438621d55aabb0cd47b1eca4711868e4",
        "b0294d5e20b8ef0d5bd83d33efe0fdd700f831701111261935205824423aa84d",
    ),
}
LegacyPayloads = tuple[tuple[str, bytes], ...]


def payload_bytes(payload: Payload, legacy: LegacyPayloads = ()) -> bytes:
    if payload.content_base64 is None:
        if payload.legacy_source_id is None:
            raise ValueError("Payload mangler innhold og legacy-referanse")
        matches = [raw for sid, raw in legacy if sid == payload.legacy_source_id]
        if len(matches) != 1:
            raise ValueError("Ukjent eller tvetydig legacy-payloadreferanse")
        raw = matches[0]
    else:
        if payload.legacy_source_id is not None or len(payload.content_base64) > 4 * (
            (MAX_SOURCE + 2) // 3
        ):
            raise ValueError("Duplisert eller for stor payload")
        try:
            raw = base64.b64decode(payload.content_base64, validate=True)
        except (ValueError, binascii.Error) as error:
            raise ValueError("Ugyldig T2-base64") from error
    if (
        len(raw) > MAX_SOURCE
        or len(raw) != payload.byte_count
        or hashlib.sha256(raw).hexdigest() != payload.sha256
        or payload.id != payload.sha256
    ):
        raise ValueError("T2-payloadens byte/hash/identitet avviker")
    return raw


def _payload(raw: bytes, legacy: LegacyPayloads) -> Payload:
    digest = hashlib.sha256(raw).hexdigest()
    shared = next((sid for sid, old in legacy if hashlib.sha256(old).hexdigest() == digest), None)
    return Payload(
        digest, digest, len(raw), None if shared else base64.b64encode(raw).decode("ascii"), shared
    )


def _source(name: str, payload: Payload | None, error: str | None = None) -> Source:
    key, mime, pin = CATALOG[name]
    transport_indices = {
        "prop25s-ch4.html": 4,
        "prop25s-ch2.html": 5,
        "inns85s.html": 6,
        "vedtak40034045.html": 7,
        "prop25s.pdf": 8,
        "inns85s.pdf": 9,
        "vedtak40034045-sak100887.html": 10,
        "sak100887.xml": 11,
    }
    filename = name.rsplit("/", 1)[-1]
    transport = (
        CATALOG[MANIFEST][2] + "#/sources/" + str(transport_indices[filename])
        if filename in transport_indices
        else CATALOG[MANIFEST][2] + "#/reused_sources/0/original_fetch_metadata"
        if name == PLENUM
        else CATALOG[ROOT + "aar/session-2024-2025.meta.json"][2] + "#/"
        if key == "forelder2024"
        else "repository:publisert_kildearkiv_37"
    )
    metadata: dict[str, object] = {"repository_path": name, "transport_reference": transport}
    if error:
        metadata["error_type"] = error
    return identified(
        "komitekilde-1",
        Source(
            "",
            name,
            key,
            mime,
            pin,
            payload.id if payload else None,
            "mangler"
            if payload is None
            else "motstrid"
            if payload.sha256 != pin
            else "http_500"
            if key == "feilet208"
            else "kildeverifisert",
            encode(metadata),
        ),
    )


def import_basis(root: Path, *, legacy_json: str = "", legacy: LegacyPayloads = ()) -> Basis:
    payloads: dict[str, Payload] = {}
    sources = []
    for name in CATALOG:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("T2-kilde utenfor valgt rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(MAX_SOURCE + 1)
            if len(raw) > MAX_SOURCE:
                raise ValueError("T2-kilde overstiger 16 MiB")
            payload = _payload(raw, legacy)
            payloads.setdefault(payload.id, payload)
            source = _source(name, payload)
        except (OSError, ValueError) as error:
            source = _source(name, None, type(error).__name__)
        sources.append(source)
    return structure_basis(tuple(payloads.values()), tuple(sources), legacy_json, legacy)


def _parent(raw: bytes) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as handle:
        expanded = handle.read(MAX_PARENT + 1)
    if len(expanded) != 7479943 or hashlib.sha256(expanded).hexdigest() != PARENT_SHA:
        raise ValueError("T2s fullsesjonsforelder avviker")
    return expanded


def derived_xml(parent: bytes, api_id: str) -> bytes:
    """Eksakt, versjonert avledning fra bevart HTTP-respons. Ingen ny HTTP."""
    start, end, object_pin, envelope_pin = RECIPES[api_id]
    if (
        hashlib.sha256(parent).hexdigest() != PARENT_SHA
        or hashlib.sha256(parent[start:end]).hexdigest() != object_pin
    ):
        raise ValueError("Feil forelder eller bytegrenser for API-utdrag")
    raw = parent[:321] + parent[start:end] + parent[-57:]
    if hashlib.sha256(raw).hexdigest() != envelope_pin:
        raise ValueError("API-utdragets konvolutt avviker")
    return raw


def _derived_source(api_id: str, parent: Source) -> Source:
    start, end, pin, envelope = RECIPES[api_id]
    return identified(
        "komitekilde-1",
        Source(
            "",
            "derived:" + api_id,
            "vedtak208" if api_id == "40034045" else "vedtak209",
            "application/xml",
            envelope,
            parent.payload_id,
            "avledet_kildeverifisert" if parent.status == "kildeverifisert" else "mangler",
            encode(
                {
                    "kind": "avledet_ikke_http",
                    "parent_source_id": parent.id,
                    "parent_sha256": PARENT_SHA,
                    "parent_bytes": 7479943,
                    "prefix_bytes": 321,
                    "object_start_byte_0": start,
                    "object_end_byte_0_exclusive": end,
                    "object_sha256": pin,
                    "suffix_bytes": 57,
                }
            ),
        ),
    )


def _statement(
    document: PilotDocument,
    source: Source,
    node: html.HtmlElement,
    role: str,
    actor: str,
    accounts: tuple[str, ...] = (),
    period: str = "2024",
    locator: str | None = None,
) -> Statement:
    hierarchy = (
        ("Plenum 16.12.2024", "Sak 24", "I 315/78", "Votering 19.49.48")
        if role == "postvis_votering_63_35_194948"
        else _hierarchy(node)
    )
    if role == "regjeringens_begrunnelse":
        # Proposisjonens kapitler og poster er DOM-søsken, ikke forfedre.
        headings = node.xpath(
            "preceding::h1[@class='K-DEL-KAPITTEL'][1] | "
            "preceding::h2[@class='K-DEL-BUDKAP'][1] | ./h3[@class='K-DEL-POST']"
        )
        hierarchy = tuple(compact(h.text_content()) for h in headings)
    return identified(
        "komiteutsagn-1",
        Statement(
            "",
            document.id,
            source.id,
            locator or node.getroottree().getpath(node),
            node.text_content(),
            html.tostring(node, encoding="unicode", with_tail=False),
            role,
            actor,
            period,
            "kildeverifisert",
            accounts,
            hierarchy,
        ),
    )


def _amounts(
    document: PilotDocument,
    source: Source,
    groups: list[tuple[str, str, html.HtmlElement, html.HtmlElement, str]],
) -> list[AmountObservation]:
    interpretation = Interpretation(
        adapter_version=RULE,
        round="nysaldering",
        round_evidence=(
            "Prop.25 S/85 S/208: statsbudsjettet 2024; sak 100887, særskilt I 315/78-votering"
        ),
        reason="T2: én valgt HTML-representasjon per stadium; eksakte 315/78-felt",
    )
    role, actor, figure = {
        "prop25": (None, "regjeringen", "regjeringsforslag"),
        "inns85": ("tilraading", "Ap_Sp_SV", "komiteforslag"),
        "vedtak208": (None, "stortinget", "stortingsvedtak"),
    }[document.key]
    observations = []
    for chapter, post, row, levels, purpose in groups:
        if (chapter, post) != ("315", "78"):
            continue
        delta = compact(row.xpath("./td")[3].text_content())
        level = compact(levels.xpath("./td")[2].text_content())
        match = re.fullmatch(r"fra kr ([\d ]+) til kr ([\d ]+)", level)
        if match is None:
            raise ValueError("T2 fra/til-lokator avviker")
        raws = (match[1].strip(), delta, match[2].strip())
        values = [int(x.replace(" ", "")) for x in raws]
        if "reduseres med" in purpose:
            values[1] = -values[1]
        if values[0] + values[1] != values[2]:
            raise ValueError("T2s lokale trio stemmer ikke")
        for meaning, raw, value, node, column in zip(
            ("for_belop", "endring", "etter_belop"),
            raws,
            values,
            (levels, row, levels),
            (3, 4, 3),
            strict=True,
        ):
            observations.append(
                AmountObservation(
                    dataset="prove",
                    source_system="komitepilot",
                    source_unit_id=document.key,
                    source_revision_id=source.expected_sha256,
                    interpretation_id=interpretation.id,
                    pointer=SourcePointer(
                        source.expected_sha256,
                        node.getroottree().getpath(node) + f"/td[{column}]",
                        meaning,
                        raw_record=html.tostring(node, encoding="unicode", with_tail=False),
                    ),
                    step_id=identity(RULE, document.id, chapter, post),
                    raw_value=raw,
                    amount_text=raw,
                    amount_kr=value,
                    chapter_raw=chapter,
                    post_raw=compact(row.xpath("./td")[1].text_content()),
                    chapter=chapter,
                    post=post,
                    chapter_name="Frivillighetsformål",
                    purpose=purpose,
                    detail_level="post",
                    budget_year=2024,
                    year_evidence="I statsbudsjettet for 2024; tabelloverskrift",
                    decision_date=document.date if figure == "stortingsvedtak" else None,
                    decision_session="2024-2025" if figure == "stortingsvedtak" else None,
                    api_id="40034045" if figure == "stortingsvedtak" else None,
                    event_id="208" if figure == "stortingsvedtak" else None,
                    unit_raw="Kroner",
                    currency="NOK",
                    multiplier="1",
                    precision="hele kroner",
                    conversion_rule=interpretation.normalization_rule,
                    normalization_evidence=source.id,
                    figure_type=figure,
                    proposal_role=role,
                    proposal_identity=document.id,
                    proposal_author=actor,
                    round="nysaldering",
                    round_evidence=interpretation.round_evidence,
                    stage_raw=document.title,
                    meaning=meaning,
                    scope="enkeltledd",
                    classification_evidence=source.id,
                    structure_status="strukturert",
                    professional_status="ikke_faglig_godkjent",
                )
            )
    return observations


@lru_cache(maxsize=3)
def structure_basis(
    payloads: tuple[Payload, ...],
    sources: tuple[Source, ...],
    legacy_json: str = "",
    legacy: LegacyPayloads = (),
) -> Basis:
    """Rekonstruer alle objekter fra byte; brukes igjen ved offline-lesing."""
    if len(payloads) > 64 or len(sources) not in (len(CATALOG), len(CATALOG) + 2):
        raise ValueError("T2-kildeinventaret overstiger eller avviker fra kontrakten")
    by_payload = {p.id: p for p in payloads}
    if len(by_payload) != len(payloads):
        raise ValueError("Duplisert T2-payload")
    raw_payloads = {p.id: payload_bytes(p, legacy) for p in payloads}
    for payload in payloads:
        if payload != _payload(raw_payloads[payload.id], legacy):
            raise ValueError("T2-payload kopierer en allerede bevart legacy-original")
    raw_sources = sources[: len(CATALOG)]
    if tuple(s.name for s in raw_sources) != tuple(CATALOG):
        raise ValueError("Ukjent eller duplisert T2-kilde")
    used = {s.payload_id for s in raw_sources if s.payload_id is not None}
    if used != set(by_payload):
        raise ValueError("Ubrukt eller ukjent payloadreferanse")
    for source in raw_sources:
        metadata = json.loads(source.metadata_json)
        if not isinstance(metadata, dict) or set(metadata) != (
            {"repository_path", "transport_reference", "error_type"}
            if source.payload_id is None
            else {"repository_path", "transport_reference"}
        ):
            raise ValueError("Ugyldig lokal T2-kildemetadata")
        error = metadata.get("error_type")
        if source.payload_id is None and (not isinstance(error, str) or not error):
            raise ValueError("Manglende kilde krever faktisk feilkategori")
        if source != _source(source.name, by_payload.get(source.payload_id or ""), error):
            raise ValueError("Kildestatus/proveniens/identitet avviker")
    by_name = {s.name: s for s in raw_sources}

    def raw(name: str) -> bytes | None:
        source = by_name[name]
        return (
            raw_payloads[source.payload_id]
            if source.status == "kildeverifisert" and source.payload_id
            else None
        )

    issues = [
        "aarsdekning_delvis:opprinnelig_rnb_ovrige_og_andre_aar_ikke_importert",
        "kontokontinuitet_ikke_dokumentert",
        "strukturdekning_delvis:bare_315_78",
        "faglig_godkjenning_ikke_utført",
        "K1_positivt_parallellforslag_ikke_levert",
        "fullmakt_209_uten_postkobling:ingen_315_belopshendelse",
        "driftsaksept_ikke_utført:#10_aapen",
    ]
    issues.extend(s.status + ":" + s.name for s in raw_sources if s.status != "kildeverifisert")
    derived = tuple(_derived_source(api_id, by_name[PARENT]) for api_id in RECIPES)
    if len(sources) > len(CATALOG) and sources[len(CATALOG) :] != derived:
        raise ValueError("Avledet API-proveniens avviker")
    sources = raw_sources + derived
    # Transportbevis beholdes som ett råmanifest; hver HTTP-observasjon har egen lokator der.
    if raw(MANIFEST):
        manifest = json.loads(raw(MANIFEST) or b"")
        for entry in manifest["sources"]:
            if "sha256" in entry:
                source = by_name[K + entry["file"]]
                if source.expected_sha256 != entry["sha256"]:
                    raise ValueError("Transportmanifest og uavhengig kildeanker avviker")
    api_nodes: dict[str, etree._Element] = {}
    if raw(PARENT):
        parent = _parent(raw(PARENT) or b"")
        for api_id in RECIPES:
            api_tree = _xml(derived_xml(parent, api_id))
            api_node = api_tree.find(
                "{http://data.stortinget.no}stortingsvedtak_liste/{http://data.stortinget.no}stortingsvedtak"
            )
            if (
                api_node is None
                or api_node.findtext("{http://data.stortinget.no}sak_id") != "100887"
            ):
                raise ValueError("API-objektet tilhører feil sak")
            api_nodes[api_id] = api_node
    else:
        issues.append("API208_209_forelderbinding_mangler")
    html_specs = (
        ("prop25", K + "prop25s-ch4.html", "//table"),
        (
            "inns85",
            K + "inns85s.html",
            "//*[@id='m3']//*[@data-strtngt-romertallseksjon-romertall='i']//table",
        ),
        ("vedtak208", K + "vedtak40034045-sak100887.html", "//table"),
    )
    trees = {}
    groups_by_key = {}
    for key, name, selector in html_specs:
        content = raw(name)
        if content:
            tree = _doc(content)
            groups = _table_groups(tree, tree.xpath(selector))
            if len(groups) != 30 or len({(c, p) for c, p, *_ in groups}) != 30:
                raise ValueError("T2s helinventar avviker fra 30 postgrupper")
            trees[key] = tree
            groups_by_key[key] = groups
    specs = (
        ("prop25", "Prop. 25 S (2024–2025)", "proposisjon", "2024-11-22"),
        ("inns85", "Innst. 85 S (2024–2025)", "innstilling", "2024-12-09"),
        ("vedtak208", "Vedtak 208/40034045", "vedtak", "2024-12-16"),
        ("vedtak209", "Vedtak 209/40034047 – fullmakt II", "fullmakt", "2024-12-16"),
        ("plenum24", "Plenum 16.12.2024 – sak 24", "referat", "2024-12-16"),
        ("sak100887", "Sak 100887", "sak", "2024-12-16"),
    )
    documents = tuple(
        identified(
            "komitedokument-1",
            PilotDocument(
                "",
                key,
                title,
                kind,
                "2024-2025",
                date,
                "bevarte_representasjoner_se_kildestatus",
                ("delvis_315_78" if key in groups_by_key else "mangler_adaptergrunnlag")
                if key in {"prop25", "inns85", "vedtak208"}
                else "tekst_ingen_belopsimport",
                "ikke_faglig_godkjent",
                tuple(s.id for s in sources if s.document_key == key),
                tuple(c + "/" + p for c, p, *_ in groups_by_key.get(key, [])),
            ),
        )
        for key, title, kind, date in specs
    )
    docs = {d.key: d for d in documents}
    statements: list[Statement] = []
    observations: list[AmountObservation] = []
    inventory: list[InventoryItem] = []
    for key, name, _ in html_specs:
        groups = groups_by_key.get(key, [])
        obs = _amounts(docs[key], by_name[name], groups)
        observations.extend(obs)
        for chapter, post, row, levels, _ in groups:
            ids = tuple(o.id for o in obs if (o.chapter, o.post) == (chapter, post))
            inventory.append(
                identified(
                    "komiteinventar-1",
                    InventoryItem(
                        "",
                        docs[key].id,
                        by_name[name].id,
                        row.getroottree().getpath(row),
                        chapter,
                        post,
                        "endringstabell",
                        "strukturert" if ids else "ikke_strukturert",
                        row.text_content() + levels.text_content(),
                        2024,
                        ids,
                    ),
                )
            )
    # Full PDF som separat representasjon; ingen nye beløp trekkes ut herfra.
    for key, filename in (("prop25", "prop25s.pdf"), ("inns85", "inns85s.pdf")):
        content = raw(K + filename)
        if content:
            for page, pdf_page in enumerate(PdfReader(io.BytesIO(content)).pages, 1):
                statements.append(
                    identified(
                        "komiteutsagn-1",
                        Statement(
                            "",
                            docs[key].id,
                            by_name[K + filename].id,
                            f"pdf:page={page}",
                            pdf_page.extract_text(),
                            "",
                            "fulltekstrepresentasjon",
                            "regjeringen" if key == "prop25" else "komiteen",
                            "2024; historisk og fremtidig kontekst",
                            "kildeverifisert",
                            (),
                            (f"PDF side {page}",),
                        ),
                    )
                )
    # Fullt HTML-inventar med logisk hierarki; en kilde/ett sted struktureres én gang.
    accounts: tuple[str, ...]
    inns = trees.get("inns85")
    if inns is not None:
        for section in inns.xpath("//*[@data-bigdoc-section]"):
            identifier = section.get("id")
            if identifier == "m2_1":
                for number, node in enumerate(
                    section.xpath("./div[contains(@class,'krnl_chapter')]/p"), 1
                ):
                    statements.append(
                        _statement(
                            docs["inns85"],
                            by_name[K + "inns85s.html"],
                            node,
                            "generell_stotte" if number == 1 else "generell_merknad",
                            "samlet_komite" if number == 1 else "H_V",
                        )
                    )
                continue
            if identifier == "m3":
                for paragraph in section.xpath("./div/p"):
                    statements.append(
                        _statement(
                            docs["inns85"],
                            by_name[K + "inns85s.html"],
                            paragraph,
                            "tilraading_med_postunntak",
                            "samlet_komite_unntatt_315_78_Ap_Sp_SV",
                            ("315/78",),
                        )
                    )
                for roman in section.xpath(".//*[@data-strtngt-romertallseksjon-romertall]"):
                    is_ii = roman.get("data-strtngt-romertallseksjon-romertall") == "ii"
                    statements.append(
                        _statement(
                            docs["inns85"],
                            by_name[K + "inns85s.html"],
                            roman,
                            "fullmakt_II_tilraading" if is_ii else "tilraading_I_fulltekst",
                            "samlet_komite" if is_ii else "samlet_komite_unntatt_315_78_Ap_Sp_SV",
                            (),
                            "2025–2028; Alpin-VM 2029" if is_ii else "2024",
                        )
                    )
                continue
            role, actor, accounts = (
                "gjengivelse_av_regjeringen" if identifier.startswith("m1") else "komiteoverskrift",
                "komiteen_gjengir_regjeringen" if identifier.startswith("m1") else "komiteen",
                (),
            )
            if identifier == "m2_2_1":
                role, actor, accounts = "flertallsbegrunnelse_LNU_tillegg", "Ap_Sp_SV", ("315/78",)
            statements.append(
                _statement(
                    docs["inns85"], by_name[K + "inns85s.html"], section, role, actor, accounts
                )
            )
    prop_text = raw(K + "prop25s-ch2.html")
    if prop_text:
        tree = _doc(prop_text)
        for node in tree.xpath("//div[h3[contains(@class,'K-DEL-POST')]]"):
            accounts = ("315/78",) if any(x.get("id") == "kap2-p11" for x in node.iter()) else ()
            statements.append(
                _statement(
                    docs["prop25"],
                    by_name[K + "prop25s-ch2.html"],
                    node,
                    "regjeringens_begrunnelse",
                    "regjeringen",
                    accounts,
                )
            )
        # Hele HTML-delens innhold er bevart i originalen og PDF-teksten ovenfor.
    if "prop25" in trees:
        tree = trees["prop25"]
        for node in tree.xpath("//div[h2[contains(@class,'K-TIT-VEDTAKDEL')]]"):
            statements.append(
                _statement(
                    docs["prop25"],
                    by_name[K + "prop25s-ch4.html"],
                    node,
                    "forslag_inkludert_fullmakt",
                    "regjeringen",
                    (),
                    "2024; fullmakt 2025–2029",
                )
            )
    for api_id, key in (("40034045", "vedtak208"), ("40034047", "vedtak209")):
        if api_id in api_nodes:
            api_object = api_nodes[api_id]
            markup = api_object.findtext("{http://data.stortinget.no}stortingsvedtak_tekst") or ""
            api_html = html.fromstring(markup)
            source = next(s for s in derived if s.name == "derived:" + api_id)
            statements.append(
                _statement(
                    docs[key],
                    source,
                    api_html,
                    "vedtatt_I_kontrollrepresentasjon"
                    if key == "vedtak208"
                    else "vedtatt_fullmakt_II",
                    "stortinget",
                    (),
                    "2024" if key == "vedtak208" else "2025–2028; Alpin-VM 2029; samlet ramme",
                    "/stortingsvedtak_liste/stortingsvedtak/stortingsvedtak_tekst",
                )
            )
    plenum = raw(PLENUM)
    if plenum:
        node = _doc(plenum).get_element_by_id("2024-12-16-24")
        statements.append(
            _statement(
                docs["plenum24"],
                by_name[PLENUM],
                node,
                "postvis_votering_63_35_194948",
                "stortinget;motstand_H_FrP_V",
                (),
            )
        )
    case = raw(K + "sak100887.xml")
    if case:
        case_node = _xml(case)
        statements.append(
            identified(
                "komiteutsagn-1",
                Statement(
                    "",
                    docs["sak100887"].id,
                    by_name[K + "sak100887.xml"].id,
                    "/detaljert_sak",
                    "".join(case_node.itertext()),
                    etree.tostring(case_node, encoding="unicode"),
                    "saksrelasjon_ikke_postbevis",
                    "Stortingets_saksmetadata",
                    "2024",
                    "kildeverifisert",
                    (),
                    ("Sak 100887",),
                ),
            )
        )

    # Eksakte roller og postunntak er bundet til uavhengig hashfestede HTML-blokker.
    def evidence(role: str) -> tuple[str, ...]:
        return tuple(s.id for s in statements if s.role == role)

    flertall = evidence("flertallsbegrunnelse_LNU_tillegg")
    unntak = evidence("tilraading_med_postunntak")
    vote = evidence("postvis_votering_63_35_194948")
    case_ids = evidence("saksrelasjon_ikke_postbevis")
    fullmakt_ii = evidence("fullmakt_II_tilraading")
    contexts = []
    for o in observations:
        stage, actor, ev = {
            "prop25": ("regjering", "regjeringen", case_ids),
            "inns85": ("tilraading", "Ap_Sp_SV", flertall + unntak + case_ids),
            "vedtak208": ("vedtak", "stortinget", vote + case_ids),
        }[o.source_unit_id]
        verified = bool(
            case_ids
            and (
                stage == "regjering"
                or stage == "tilraading"
                and flertall
                and unntak
                or stage == "vedtak"
                and vote
                and "40034045" in api_nodes
            )
        )
        contexts.append(
            identified(
                "komitekontekst-1",
                TreatmentContext(
                    "",
                    o.id,
                    docs[o.source_unit_id].id,
                    "nysaldering",
                    stage,
                    actor,
                    "kildeverifisert" if verified else "uavklart",
                    ev,
                ),
            )
        )
    relations = []
    for left, right, role, ev, accounts, scope in (
        (
            "prop25",
            "inns85",
            "forslag_til_flertallstilraading",
            case_ids + flertall + unntak,
            ("315/78",),
            "I_315_78",
        ),
        (
            "inns85",
            "vedtak208",
            "saerskilt_vedtakelse_63_35",
            case_ids + unntak + vote,
            ("315/78",),
            "I_315_78",
        ),
        (
            "inns85",
            "vedtak209",
            "fullmakt_II_til_separat_209",
            case_ids + fullmakt_ii + vote + evidence("vedtatt_fullmakt_II"),
            (),
            "II_Narvik_uten_postkobling",
        ),
        (
            "plenum24",
            "vedtak208",
            "varslet_motstand_H_FrP_V",
            case_ids + vote,
            ("315/78",),
            "I_315_78",
        ),
    ):
        verified = (
            bool(case_ids and vote and "40034045" in api_nodes)
            if role == "varslet_motstand_H_FrP_V"
            else bool(
                case_ids
                and ev
                and (
                    flertall and unntak
                    if left == "prop25"
                    else fullmakt_ii and vote
                    if right == "vedtak209"
                    else unntak and vote
                )
                and (right != "vedtak209" or "40034047" in api_nodes)
            )
        )
        relations.append(
            identified(
                "komiterelasjon-1",
                PilotRelation(
                    "",
                    docs[left].id,
                    docs[right].id,
                    role,
                    scope,
                    "kildeverifisert" if verified else "uavklart",
                    accounts,
                    ev,
                    2024,
                ),
            )
        )
    issues.extend(
        "behandlingsbevis_mangler:" + c.stage for c in contexts if c.status != "kildeverifisert"
    )
    return identified(
        "komitegrunnlag-1",
        Basis(
            "",
            RULE,
            payloads,
            sources,
            documents,
            tuple(inventory),
            tuple(statements),
            tuple(observations),
            tuple(contexts),
            tuple(relations),
            tuple(dict.fromkeys(issues)),
            legacy_json,
        ),
    )


def validate_basis(basis: Basis, legacy: LegacyPayloads = ()) -> None:
    if any(
        len(items) > maximum
        for items, maximum in (
            (basis.documents, 16),
            (basis.inventory, 512),
            (basis.statements, 512),
            (basis.observations, 256),
            (basis.relations, 1024),
        )
    ):
        raise ValueError("T2-objekter overstiger kontraktens ressursgrense")
    if basis != structure_basis(basis.payloads, basis.sources, basis.legacy_json, legacy):
        raise ValueError("T2-grunnlaget avviker fra kildebyte/roller/bevis/ID-er")
