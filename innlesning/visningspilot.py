"""T1-kildeadapter. Fast kildeutvalg, ingen database, HTTP eller gamle formatendringer."""

import base64
import binascii
import gzip
import hashlib
import io
import json
import re
from dataclasses import replace
from functools import lru_cache
from pathlib import Path

from lxml import etree, html
from pypdf import PdfReader

from .legacy_html import parse_legacy_html
from .observations import AmountObservation, Interpretation, SourcePointer, encode, identity
from .omtale import OmtaleSource, compact, identified, source_bytes
from .omtale import validate_basis as validate_omtale
from .visningspilot_model import (
    RULE,
    InventoryItem,
    PilotBasis,
    PilotDocument,
    PilotInput,
    PilotRelation,
    PilotSource,
    Statement,
    TreatmentContext,
)
from .visningspilot_vedtak import validate_adopted

MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_PARENT_BYTES = 32 * 1024 * 1024
RESEARCH = "docs/research/to-visninger-37/"
# Uavhengige ankere fra de bevarte originalene, ikke fra eksportens egne felt.
O2_PINS = {
    "originals/prop16s.pdf": "677716056269c07b8ec81bcae91d814b975123791635548281038d9beb3aa5db",
    "originals/prop16s-ch2.html": (
        "258d26e6d324bde709bf3d1cb660d7eb6f4248f537d4b0c77e095f17697cf8df"
    ),
    "originals/prop16s-ch4.html": (
        "ff1c53688a155c2cb9d8d37a8d40550e56b5c5c1d2d171c30519ef49227eca5e"
    ),
    "originals/inns81s.pdf": "5a29d0553991759d8ddc234899647e9e6b5e1f2885bf13edccfb26105a6be496",
    "originals/inns81s.html": "e7069d74e911fb868812bb34f68b41d210b4e33035c1317cbedd296ac1101e95",
    "originals/votering-161224.html": (
        "22170a60f769e89642b2e52525899903020de25938aa2b566ea28d11f85fb2e5"
    ),
    "b6/40034048.xml": "2a540261f110b761a0213516c8ad72844d0285744ca0f1cdd4cb1afce06f0850",
    "b6/40034048.json": "1b43cc3e77fb8b216d3d0bd2d51739c4200b38aabcdac907afcdf47d0218a79b",
    "b8/sak-100927.xml": "2ee25b327b78772523d56317c752e35f5134eef60db9536f6dea3c94ad8fed27",
    "b8/sak-100927.json": "07b85b79438fa1cfcc8774c36291fc28d0cfdc7d429ca82e1e5810bca89ac895",
}
# navn -> (dokumentnøkkel, MIME-type, pin). Metadataoriginaler følger også filen.
SOURCE_CATALOG = {
    "docs/research/omtale-o1/originals/prop16s-ch4.html": (
        "prop16",
        "text/html",
        O2_PINS["originals/prop16s-ch4.html"],
    ),
    "docs/research/omtale-o1/originals/inns81s.html": (
        "inns81",
        "text/html",
        O2_PINS["originals/inns81s.html"],
    ),
    "docs/research/visningspilot-41/originals/session-2024-2025-9cfe.xml.gz": (
        "eldreforelder2024",
        "application/gzip",
        "7502f2f565048f1b0954cb4cb132183d0bc5ec362ba74e14de877df36003a7d4",
    ),
    "docs/research/visningspilot-41/originals/session-2024-2025-9cfe.meta.json": (
        "eldreforelder2024",
        "application/json",
        "cf9397ad44be04796cf3ed95765cddb165b0193fe071b4e1a6b629566aa82363",
    ),
    "tests/fixtures/b8/40034049.xml": (
        "vedtak211",
        "application/xml",
        "5f253a556d2ac512570899252b396bc38f068de5f4bd6820178e7de8ce41f3eb",
    ),
    "tests/fixtures/b8/40034049.json": (
        "vedtak211",
        "application/json",
        "6e0e37551b00da15c262e8ba2e40e8b21abba96d3b47acc57e41b908024d9def",
    ),
    "tests/fixtures/b8/sak-100889.xml": (
        "sak100889",
        "application/xml",
        "3a8f0918a3fcce90bf2c93f3ce972c3de7277c76e27e5ef563d6c43384cf2af2",
    ),
    "tests/fixtures/b8/sak-100889.json": (
        "sak100889",
        "application/json",
        "67033cce596b33ccb7f2cd459a6df7af98d44836292f0675d308797a888ba04c",
    ),
    RESEARCH + "originals/aar/session-2024-2025.xml.gz": (
        "forelder2024",
        "application/gzip",
        "1ea276a5730a5196f4def7471e0bf6ae51a7878a4eac86922cc87a9a71200a6b",
    ),
    RESEARCH + "originals/aar/session-2024-2025.meta.json": (
        "forelder2024",
        "application/json",
        "4ccc151e0ddd84c11b9c5e973c67762a6470a7bb5f2cd59a542d2847e6c5cd28",
    ),
    RESEARCH + "originals/forgrening/inns95s.html": (
        "inns95",
        "text/html",
        "ae61227fa83adf04fb45956b1bd714a75592bbc1d6c70da300e554afef806aa6",
    ),
    RESEARCH + "originals/forgrening/inns95s.pdf": (
        "inns95",
        "application/pdf",
        "7a78167c7eafc500938e4ac39d8ed9febec1f6e7e6ce337acc4b7a58d0d14635",
    ),
    RESEARCH + "originals/forgrening/manifest.json": (
        "inns95",
        "application/json",
        "6b2dd282d4c1bffff15063907bc6c3d5948279c7898f7caf7291d7a140de6816",
    ),
}


def raw_source(source: PilotSource) -> bytes | None:
    if source.content_base64 is None:
        if source.sha256 is not None or source.byte_count is not None:
            raise ValueError("Manglende pilotkilde med oppfunnet hash/størrelse")
        return None
    if len(source.content_base64) > 4 * ((MAX_SOURCE_BYTES + 2) // 3):
        raise ValueError("Pilotbase64 overstiger bytegrensen")
    try:
        raw = base64.b64decode(source.content_base64, validate=True)
    except (ValueError, binascii.Error) as error:
        raise ValueError("Ugyldig pilotbase64") from error
    if (
        len(raw) > MAX_SOURCE_BYTES
        or hashlib.sha256(raw).hexdigest() != source.sha256
        or len(raw) != source.byte_count
    ):
        raise ValueError("Pilotkildens faktiske byte/hash avviker")
    return raw


def _source(name: str, raw: bytes | None, metadata: str) -> PilotSource:
    properties = json.loads(metadata)
    allowed = {"repository_path", "error_type"} if raw is None else {"repository_path"}
    if (
        not isinstance(properties, dict)
        or set(properties) != allowed
        or properties.get("repository_path") != name
        or (
            raw is None
            and (not isinstance(properties.get("error_type"), str) or not properties["error_type"])
        )
    ):
        raise ValueError("Pilotkildens lokale innlesningsmetadata avviker")
    key, mime, pin = SOURCE_CATALOG[name]
    digest = hashlib.sha256(raw).hexdigest() if raw is not None else None
    status = "mangler" if raw is None else "kildeverifisert" if digest == pin else "motstrid"
    return identified(
        "visningskilde-1",
        PilotSource(
            "",
            name,
            key,
            mime,
            pin,
            base64.b64encode(raw).decode("ascii") if raw is not None else None,
            digest,
            len(raw) if raw is not None else None,
            status,
            metadata,
        ),
    )


def import_basis(prepared: PilotInput, root: Path) -> PilotBasis:
    """Les bare det eksplisitte T1-katalogutvalget; mangler beholdes som avvik."""
    sources = []
    for name in SOURCE_CATALOG:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("Pilotkilde utenfor valgt rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(MAX_SOURCE_BYTES + 1)
            if len(raw) > MAX_SOURCE_BYTES:
                raise ValueError("Pilotkilde overstiger 16 MiB")
            metadata = encode({"repository_path": name})
        except (OSError, ValueError) as error:
            raw = None
            metadata = encode({"repository_path": name, "error_type": type(error).__name__})
        sources.append(_source(name, raw, metadata))
    return structure_basis(prepared, tuple(sources))


def _doc(raw: bytes) -> html.HtmlElement:
    return parse_legacy_html(raw)


def _xml(raw: bytes) -> etree._Element:
    root = etree.fromstring(
        raw, etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    )
    if root.getroottree().docinfo.doctype:
        raise ValueError("DOCTYPE i pilotkilde")
    return root


def _statement(
    document: PilotDocument,
    source_id: str,
    node: html.HtmlElement,
    role: str,
    actor: str,
    accounts: tuple[str, ...],
    period: str = "2024",
) -> Statement:
    hierarchy = _hierarchy(node)
    return identified(
        "visningsutsagn-1",
        Statement(
            "",
            document.id,
            source_id,
            node.getroottree().getpath(node),
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


def _hierarchy(node: html.HtmlElement) -> tuple[str, ...]:
    """Kildenes logiske seksjoner, også når Stortingets delseksjoner er søsken."""
    chain = [*reversed(list(node.iterancestors())), node]
    headings: list[str] = []
    sections = [n for n in chain if "data-bigdoc-section" in n.attrib]
    if sections:
        section = sections[-1]
        parts = section.get("id", "").split("_")
        document = node.getroottree()
        for length in range(1, len(parts) + 1):
            identifier = "_".join(parts[:length]) + "-title"
            titles = document.xpath("//*[@id=$identifier]", identifier=identifier)
            if len(titles) != 1:
                raise ValueError("Logisk Storting-seksjon mangler entydig overskrift")
            headings.append(compact(titles[0].text_content()))
        for container in chain:
            if "strtngt_romertallseksjon" in container.get("class", "").split():
                titles = container.xpath("./div[@class='strtngt_tittel']")
                if len(titles) != 1:
                    raise ValueError("Romertallsseksjon mangler entydig overskrift")
                headings.append(compact(titles[0].text_content()))
        return tuple(headings)
    # Regjeringen bruker nestede K-DEL-seksjoner. På delte nivåer gjelder siste
    # foregående overskrift av hver semantiske klasse, aldri senere søsken.
    for index, container in enumerate(chain):
        prop_titles: dict[str, html.HtmlElement] = {}
        branch = chain[index + 1] if index + 1 < len(chain) else None
        for child in container:
            if child is branch:
                break
            if isinstance(child.tag, str) and re.fullmatch(r"h[1-6]", child.tag):
                category = child.get("class", "")
                if category.startswith("K-"):
                    prop_titles[category] = child
            elif branch is None:
                break
        headings.extend(
            compact(child.text_content()) for child in container if child in prop_titles.values()
        )
    return tuple(headings)


def _table_groups(
    doc: html.HtmlElement, tables: list[html.HtmlElement]
) -> list[tuple[str, str, html.HtmlElement, html.HtmlElement, str]]:
    groups = []
    for table in tables:
        chapter = ""
        rows = table.xpath("./tbody/tr")
        for index, row in enumerate(rows):
            cells = [compact(c.text_content()) for c in row.xpath("./td")]
            if len(cells) != 4:
                continue
            if cells[0].isdigit():
                chapter = str(int(cells[0]))
            if cells[1].isdigit() and ("økes med" in cells[2] or "reduseres med" in cells[2]):
                if not chapter or index + 1 >= len(rows):
                    raise ValueError("Ufullstendig tabellgruppe")
                groups.append((chapter, str(int(cells[1])), row, rows[index + 1], cells[2]))
    return groups


def _amounts(
    document: PilotDocument,
    source: OmtaleSource | PilotSource,
    groups: list[tuple[str, str, html.HtmlElement, html.HtmlElement, str]],
) -> list[AmountObservation]:
    interpretation = Interpretation(
        adapter_version=RULE,
        round="nysaldering",
        round_evidence="Prop.16 S: endringer i statsbudsjettet 2024; dokumentert 81/210-behandling",
        reason="T1: bare eksakte 1429-tabellfelt; forslag/tilråding er separate observasjoner",
    )
    result = []
    for chapter, post, row, levels, purpose in groups:
        if chapter != "1429":
            continue
        delta_text = compact(row.xpath("./td")[3].text_content())
        level_text = compact(levels.xpath("./td")[2].text_content())
        match = re.fullmatch(r"fra kr ([\d ]+) til kr ([\d ]+)", level_text)
        if match is None:
            raise ValueError("Fra/til-mønster avviker")
        raw_values = (match[1].strip(), delta_text, match[2].strip())
        values = tuple(int(v.replace(" ", "")) for v in raw_values)
        signed_delta = -values[1] if "reduseres med" in purpose else values[1]
        if values[0] + signed_delta != values[2]:
            raise ValueError("Kildens lokale trio avviker")
        for meaning, raw, value, node, column in zip(
            ("for_belop", "endring", "etter_belop"),
            raw_values,
            (values[0], signed_delta, values[2]),
            (levels, row, levels),
            (3, 4, 3),
            strict=True,
        ):
            result.append(
                AmountObservation(
                    dataset="prove",
                    source_system="visningspilot",
                    source_unit_id=document.key,
                    source_revision_id=source.sha256 or "",
                    interpretation_id=interpretation.id,
                    pointer=SourcePointer(
                        source.sha256 or "",
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
                    chapter_name="Riksantikvaren",
                    purpose=purpose,
                    detail_level="post",
                    budget_year=2024,
                    year_evidence="Endringer i statsbudsjettet 2024; kildeoverskrift",
                    unit_raw="Kroner",
                    currency="NOK",
                    multiplier="1",
                    precision="hele kroner",
                    conversion_rule=interpretation.normalization_rule,
                    normalization_evidence=source.id,
                    figure_type="regjeringsforslag"
                    if document.key == "prop16"
                    else "komiteforslag",
                    proposal_role=None if document.key == "prop16" else "tilraading",
                    proposal_identity=document.id,
                    proposal_author="regjeringen" if document.key == "prop16" else "samlet_komite",
                    round="nysaldering",
                    round_evidence=interpretation.round_evidence,
                    stage_raw=document.title,
                    meaning=meaning,
                    scope="enkeltledd",
                    classification_evidence=source.id,
                    structure_status="strukturert",
                )
            )
    return result


def _check_211_parent(sources: tuple[PilotSource, ...], issues: list[str]) -> None:
    by_name = {s.name: s for s in sources}
    names = (
        RESEARCH + "originals/aar/session-2024-2025.xml.gz",
        RESEARCH + "originals/aar/session-2024-2025.meta.json",
        "tests/fixtures/b8/40034049.xml",
        "tests/fixtures/b8/40034049.json",
    )
    if any(by_name[n].status != "kildeverifisert" for n in names):
        issues.append("211_forelderbinding_ikke_kontrollert")
        return
    raws = [raw_source(by_name[n]) for n in names]
    assert all(r is not None for r in raws)
    compressed, meta_raw, excerpt, sidecar_raw = raws
    assert compressed is not None and meta_raw is not None and sidecar_raw is not None
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as handle:
        parent = handle.read(MAX_PARENT_BYTES + 1)
    meta, sidecar = json.loads(meta_raw), json.loads(sidecar_raw)
    if len(parent) > MAX_PARENT_BYTES or hashlib.sha256(parent).hexdigest() != meta["sha256"]:
        raise ValueError("Ugyldig dekomprimert forelder")
    start, count = sidecar["object_start_byte_0"], sidecar["object_bytes"]
    objects = list(re.finditer(rb"    <stortingsvedtak>.*?</stortingsvedtak>", parent, re.S))
    first, end = objects[0].start(), objects[-1].end()
    reconstructed = parent[:first] + parent[start : start + count] + parent[end:]
    if (
        reconstructed != excerpt
        or sidecar["source_response_sha256"] != meta["sha256"]
        or sidecar["source_response_bytes"] != len(parent)
    ):
        raise ValueError("211 kan ikke rekonstrueres fra sin dokumenterte forelder")
    issues.append("211_byteeksakt_rekonstruert_fra_c5f3b900")


def _check_210_parent(
    sources: tuple[PilotSource, ...], old_sources: dict[str, OmtaleSource], issues: list[str]
) -> None:
    archive, meta = (s for s in sources if s.document_key == "eldreforelder2024")
    if archive.status != "kildeverifisert" or meta.status != "kildeverifisert":
        issues.append("eldre_forelder_ikke_kontrollert:210:9cfeaef5")
        return
    compressed, meta_raw = raw_source(archive), raw_source(meta)
    assert compressed is not None and meta_raw is not None
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as handle:
        parent = handle.read(MAX_PARENT_BYTES + 1)
    transport = json.loads(meta_raw)["source_response"]
    sidecar_raw = source_bytes(old_sources["b6/40034048.json"])
    assert sidecar_raw is not None
    sidecar = json.loads(sidecar_raw)
    if (
        len(parent) > MAX_PARENT_BYTES
        or len(parent) != transport["bytes"]
        or hashlib.sha256(parent).hexdigest() != transport["sha256"]
        or transport["sha256"] != sidecar["source_response_sha256"]
    ):
        raise ValueError("210s eldre forelder avviker fra gammel proveniens")
    marker = b"  <stortingsvedtak_liste>\r\n"
    prefix = parent[: parent.index(marker) + len(marker)]
    suffix = parent[parent.rindex(b"  </stortingsvedtak_liste>") :]
    start, count = sidecar["object_start_byte_0"], sidecar["object_bytes"]
    if prefix + parent[start : start + count] + suffix != source_bytes(
        old_sources["b6/40034048.xml"]
    ):
        raise ValueError("210 kan ikke rekonstrueres byteeksakt fra gammel forelder")
    issues.append("210_byteeksakt_rekonstruert_fra_9cfeaef5")


@lru_cache(maxsize=2)
def structure_basis(old: PilotInput, sources: tuple[PilotSource, ...]) -> PilotBasis:
    """Kanonisk rekonstruksjon også ved offline-gjenlesing; aldri stol på eksportfelter."""
    validate_omtale(old.basis)
    if old.basis.extractor != "o2b-html-pdf-1":
        raise ValueError("T1 krever eksplisitt uendret O2b-grunnlag")
    old_sources = {s.name: s for s in old.basis.sources}
    if set(old_sources) != set(O2_PINS):
        raise ValueError("T1 krever det komplette O2b-kildeinventaret")
    for name, pin in O2_PINS.items():
        if old_sources[name].sha256 != pin or old_sources[name].status != "kildeverifisert":
            raise ValueError("O2b-original avviker fra T1-kildeankeret: " + name)
    validate_adopted(old)
    if tuple(s.name for s in sources) != tuple(SOURCE_CATALOG):
        raise ValueError("Ukjent, duplisert eller manglende pilotkildeinventar")
    for source in sources:
        if source != _source(source.name, raw_source(source), source.metadata_json):
            raise ValueError("Pilotkildens status/rolle/identitet avviker fra katalogen")
    issues = [
        *old.issues,
        "aarsdekning_delvis:opprinnelig_rnb_ovrige_ikke_importert",
        "kontokontinuitet_ikke_dokumentert:2024_2025",
        "prop16_delvis_strukturert:35_av_37_tabellgrupper_uten_belopsimport",
        "inns95_strukturering_ikke_levert:T5_T6",
    ]
    issues.extend(s.status + ":" + s.name for s in sources if s.status != "kildeverifisert")
    _check_211_parent(sources, issues)
    _check_210_parent(sources, old_sources, issues)
    new_by_name = {s.name: s for s in sources}
    all_old_ids = {
        s.document_id: tuple(t.id for t in old.basis.sources if t.document_id == s.document_id)
        for s in old.basis.sources
    }
    prop_raw = source_bytes(old_sources["originals/prop16s-ch4.html"])
    inns_raw = source_bytes(old_sources["originals/inns81s.html"])
    assert prop_raw is not None and inns_raw is not None
    prop_html, inns_html = _doc(prop_raw), _doc(inns_raw)
    prop_groups = _table_groups(prop_html, prop_html.xpath("//table")[:2])
    inns_groups = _table_groups(inns_html, inns_html.xpath("//*[@id='m3']//table"))
    if len(prop_groups) != 37 or {(c, p) for c, p, *_ in inns_groups} != {
        ("1429", "1"),
        ("1429", "22"),
    }:
        raise ValueError("T1-originalinventaret avviker")
    prop_accounts = {c + "/" + p for c, p, *_ in prop_groups}
    prop_accounts.update(
        ("1420/39", "1420/79", "1420/66", "1420/87", "1429/60", "1533/45", "1474/50", "1474/70")
    )
    accounts1429 = ("1429/1", "1429/22", "1429/60")
    document_specs = (
        (
            "prop16",
            "Prop. 16 S (2024–2025)",
            "proposisjon",
            "2024-11-22",
            "full_pdf_delvis_html",
            "delvis_1429",
            all_old_ids["prop-16-s-2024-2025"]
            + tuple(s.id for s in sources if s.document_key == "prop16"),
            tuple(sorted(prop_accounts)),
        ),
        (
            "inns81",
            "Innst. 81 S (2024–2025)",
            "innstilling",
            "2024-12-09",
            "full_html_pdf",
            "helt_inventert",
            all_old_ids["inns-81-s-2024-2025"]
            + tuple(s.id for s in sources if s.document_key == "inns81"),
            accounts1429,
        ),
        (
            "vedtak210",
            "Vedtak 210 (2024–2025)",
            "vedtak",
            "2024-12-16",
            "helt_objekt_eldre_forelder_separat",
            "helt_inventert",
            all_old_ids["vedtak-210"],
            ("1429/1", "1429/22"),
        ),
        (
            "vedtak211",
            "Vedtak 211 (2024–2025)",
            "vedtak",
            "2024-12-16",
            "helt_objekt",
            "helt_inventert",
            tuple(s.id for s in sources if s.document_key == "vedtak211"),
            ("1429/60",),
        ),
        (
            "inns95",
            "Innst. 95 S (2024–2025), Beriktiget",
            "innstilling",
            "2024-12-10",
            "full_html_pdf",
            "ikke_strukturert",
            tuple(s.id for s in sources if s.document_key == "inns95"),
            tuple(sorted(a for a in prop_accounts if not a.startswith("1429/"))) + ("1420/32",),
        ),
    )
    documents = tuple(
        identified(
            "visningsdokument-1",
            PilotDocument(
                "",
                key,
                title,
                kind,
                "2024-2025",
                day,
                raw_cov
                if all(s.status == "kildeverifisert" for s in sources if s.id in ids)
                else "mangler_eller_motstrid_i_rakilde",
                structured,
                "ikke_faglig_godkjent",
                ids,
                accounts,
            ),
        )
        for key, title, kind, day, raw_cov, structured, ids, accounts in document_specs
    )
    docs = {d.key: d for d in documents}
    adopted = old.adopted
    if len(adopted) != 6 or {o.figure_type for o in adopted} != {"stortingsvedtak"}:
        raise ValueError("T1 krever seks opprinnelige vedtaksfelt")
    stage_observations = []
    for key, name in (
        ("prop16", "docs/research/omtale-o1/originals/prop16s-ch4.html"),
        ("inns81", "docs/research/omtale-o1/originals/inns81s.html"),
    ):
        stage_source = new_by_name[name]
        if stage_source.status != "kildeverifisert":
            issues.append("numerisk_stadium_mangler:" + key)
            continue
        stage_raw = raw_source(stage_source)
        assert stage_raw is not None
        stage_doc = _doc(stage_raw)
        stage_groups = _table_groups(
            stage_doc,
            stage_doc.xpath("//table")[:2]
            if key == "prop16"
            else stage_doc.xpath("//*[@id='m3']//table"),
        )
        stage_observations.extend(_amounts(docs[key], stage_source, stage_groups))
    observations = tuple(stage_observations) + adopted
    inventory: list[InventoryItem] = []
    statements: list[Statement] = []

    def item(
        key: str, source_id: str, node: html.HtmlElement, chapter: str, post: str, role: str
    ) -> None:
        obs = tuple(
            o.id
            for o in observations
            if o.source_unit_id == key and o.chapter == chapter and o.post == post
        )
        if key == "vedtak210":
            obs = tuple(o.id for o in adopted if o.chapter == chapter and o.post == post)
        inventory.append(
            identified(
                "visningsinventar-1",
                InventoryItem(
                    "",
                    docs[key].id,
                    source_id,
                    node.getroottree().getpath(node),
                    chapter,
                    post,
                    role,
                    "strukturert" if obs or role != "endringstabell" else "ikke_strukturert",
                    node.text_content(),
                    2024,
                    obs,
                ),
            )
        )

    for key, source_name, groups in (
        ("prop16", "originals/prop16s-ch4.html", prop_groups),
        ("inns81", "originals/inns81s.html", inns_groups),
    ):
        for chapter, post, row, _, _ in groups:
            item(key, old_sources[source_name].id, row, chapter, post, "endringstabell")
            # Inventaret viser hele gruppens ordlyd; de øvrige feltene importeres ikke som beløp.
            following = row.getnext()
            assert following is not None
            last = inventory.pop()
            inventory.append(
                identified(
                    "visningsinventar-1",
                    replace(last, text=row.text_content() + following.text_content()),
                )
            )
    # Hele PDF-en er dokumentets fulltekstgrunnlag. HTML-delene merkes som delrepresentasjoner.
    for key, source_name in (
        ("prop16", "originals/prop16s.pdf"),
        ("inns81", "originals/inns81s.pdf"),
    ):
        original = old_sources[source_name]
        pdf_raw = source_bytes(original)
        assert pdf_raw is not None
        for number, page in enumerate(PdfReader(io.BytesIO(pdf_raw)).pages, 1):
            statements.append(
                identified(
                    "visningsutsagn-1",
                    Statement(
                        "",
                        docs[key].id,
                        original.id,
                        "pdf:page=" + str(number),
                        page.extract_text(),
                        "",
                        "fulltekstrepresentasjon",
                        "regjeringen" if key == "prop16" else "komiteen",
                        "2024; historisk og fremtidig kontekst i originalen",
                        "kildeverifisert",
                        (),
                        (),
                    ),
                )
            )
    for source_name, selector in (
        ("originals/prop16s-ch2.html", "//*[@id='kap2']"),
        ("originals/prop16s-ch4.html", "/html/body/main/div/div[3]/div[3]/div/div"),
    ):
        original = old_sources[source_name]
        raw = source_bytes(original)
        assert raw is not None
        nodes = _doc(raw).xpath(selector)
        if len(nodes) != 1:
            raise ValueError("Delrepresentasjonens fulltekstlokator avviker")
        statements.append(
            _statement(
                docs["prop16"],
                original.id,
                nodes[0],
                "delvis_html_representasjon",
                "regjeringen",
                (),
            )
        )
    accounts: tuple[str, ...]
    evidence: tuple[str, ...]
    for identifier, accounts, role, period in (
        ("m1", accounts1429, "sammendrag_innledning", "2024"),
        ("m1_1", accounts1429, "kapitteloverskrift", "2024"),
        (
            "m1_1_1",
            ("1429/1", "1429/22"),
            "gjengivelse_av_regjeringen",
            "2024; avrundet lønnsanslag",
        ),
        ("m1_1_2", ("1429/22", "1429/1"), "gjengivelse_av_regjeringen", "2024"),
        (
            "m1_1_3",
            ("1429/60",),
            "gjengivelse_av_regjeringen",
            "historisk RNB 2024; fond 10 mill. aggregat; 5 mill. i 2024 og 2025; "
            "fremtidig usikker utbetaling",
        ),
        ("m2", accounts1429, "samlet_stotte", "2024"),
        ("m3", accounts1429, "tilraading", "2024"),
    ):
        node = inns_html.get_element_by_id(identifier)
        statements.append(
            _statement(
                docs["inns81"],
                old_sources["originals/inns81s.html"].id,
                node,
                role,
                "samlet_komite" if identifier in {"m2", "m3"} else "komiteen_gjengir_regjeringen",
                accounts,
                period,
            )
        )
    # Hele HTML-innholdet. PDF-representasjonen bevarer i tillegg sluttunderskriften.
    complete = inns_html.get_element_by_id("m1").getparent()
    assert complete is not None
    statements.append(
        _statement(
            docs["inns81"],
            old_sources["originals/inns81s.html"].id,
            complete,
            "full_dokumenttekst",
            "komiteen",
            accounts1429,
        )
    )
    inns_ii = inns_html.xpath("//*[@id='m3']//*[@data-strtngt-romertallseksjon-romertall='ii']")[0]
    statements.append(
        _statement(
            docs["inns81"],
            old_sources["originals/inns81s.html"].id,
            inns_ii,
            "stikkordsfullmakt_tilraading",
            "samlet_komite",
            ("1429/60",),
        )
    )
    item(
        "inns81",
        old_sources["originals/inns81s.html"].id,
        inns_ii,
        "1429",
        "60",
        "stikkordsfullmakt",
    )
    # Postvist fullmaktsinventar; en delt ramme beholder samme seksjonslokator.
    authorizations = (
        ("kap2-p57", ("1420/21",)),
        ("kap2-p58", ("1420/61", "1420/62")),
        ("kap2-p59", ("1420/39", "1420/69", "1420/79")),
        ("kap2-p60", ("1420/66", "1420/87", "1429/60")),
        ("kap2-p61", ("1471/1", "4471/3")),
    )
    for identifier, accounts in authorizations:
        authorization_node = prop_html.get_element_by_id(identifier).getparent()
        assert authorization_node is not None
        statements.append(
            _statement(
                docs["prop16"],
                old_sources["originals/prop16s-ch4.html"].id,
                authorization_node,
                "fullmaktsforslag",
                "regjeringen",
                accounts,
                "2024; fremtidige år; samlet ramme, ikke bevilgningsdelta",
            )
        )
        for account in accounts:
            chapter, post = account.split("/")
            item(
                "prop16",
                old_sources["originals/prop16s-ch4.html"].id,
                authorization_node,
                chapter,
                post,
                "fullmaktsreferanse",
            )
    v3 = prop_html.get_element_by_id("kap2-p60").getparent()
    assert v3 is not None
    v3_node = v3.xpath("./ol/li[3]")[0]
    statements.append(
        _statement(
            docs["prop16"],
            old_sources["originals/prop16s-ch4.html"].id,
            v3_node,
            "stikkordsfullmakt_forslag",
            "regjeringen",
            ("1429/60",),
        )
    )
    prop_ch2_raw = source_bytes(old_sources["originals/prop16s-ch2.html"])
    assert prop_ch2_raw is not None
    prop_ch2 = _doc(prop_ch2_raw)
    for account, selector in (
        ("1533/45", "//*[@id='kap2_ch1_ch2']"),
        ("1474/50", "//*[@id='kap2_ch9']"),
        ("1474/70", "//*[@id='kap2_ch9']"),
    ):
        nodes = prop_ch2.xpath(selector)
        if len(nodes) != 1:
            raise ValueError("Kontekstlokator mangler: " + selector)
        chapter, post = account.split("/")
        item(
            "prop16",
            old_sources["originals/prop16s-ch2.html"].id,
            nodes[0],
            chapter,
            post,
            "kontekstreferanse",
        )
    for section in old.basis.sections:
        if section.key == "P1_PDF":
            continue
        key = (
            "prop16"
            if section.document_id.startswith("prop-")
            else "inns81"
            if section.document_id.startswith("inns-")
            else "vedtak210"
        )
        statements.append(
            identified(
                "visningsutsagn-1",
                Statement(
                    "",
                    docs[key].id,
                    section.source_id,
                    section.locator,
                    section.text,
                    section.html,
                    section.role,
                    section.actor,
                    "2024; 2025-kontekst" if section.key == "PN" else "2024",
                    section.status,
                    section.accounts,
                    tuple(h.text for h in section.hierarchy),
                ),
            )
        )
    raw210 = source_bytes(old_sources["b6/40034048.xml"])
    assert raw210 is not None
    text210 = _xml(raw210).findtext(".//{http://data.stortinget.no}stortingsvedtak_tekst")
    if text210 is None:
        raise ValueError("210-fulltekst mangler")
    original210_html = _doc(text210.encode("utf-8"))
    statements.append(
        _statement(
            docs["vedtak210"],
            old_sources["b6/40034048.xml"].id,
            original210_html,
            "endelig_vedtak",
            "stortinget",
            ("1429/1", "1429/22"),
        )
    )
    for post in ("1", "22"):
        node = original210_html.xpath("//tr[td[normalize-space()='" + post + "']]")
        # API bruker 1 (ikke 01); lokatoren er originalens egen tabell.
        item(
            "vedtak210",
            old_sources["b6/40034048.xml"].id,
            node[0] if node else original210_html,
            "1429",
            post,
            "endringstabell",
        )
    source211 = new_by_name["tests/fixtures/b8/40034049.xml"]
    if source211.status == "kildeverifisert":
        raw211 = raw_source(source211)
        assert raw211 is not None
        root211 = _xml(raw211)
        text211 = root211.findtext(".//{http://data.stortinget.no}stortingsvedtak_tekst")
        if text211 is None:
            raise ValueError("211-fulltekst mangler")
        node211 = _doc(text211.encode("utf-8"))
        statements.append(
            _statement(
                docs["vedtak211"],
                source211.id,
                node211,
                "stikkordsfullmakt_vedtatt",
                "stortinget",
                ("1429/60",),
            )
        )
        item("vedtak211", source211.id, node211, "1429", "60", "stikkordsfullmakt")
    source95 = new_by_name[RESEARCH + "originals/forgrening/inns95s.html"]
    if source95.status == "kildeverifisert":
        raw95 = raw_source(source95)
        assert raw95 is not None
        doc95 = _doc(raw95)
        body95 = doc95.get_element_by_id("m1").getparent()
        assert body95 is not None
        statements.append(
            _statement(
                docs["inns95"],
                source95.id,
                body95,
                "fulltekst_ikke_strukturert",
                "komiteen_egne_roller_ikke_tolket",
                docs["inns95"].accounts,
            )
        )
    relations: list[PilotRelation] = []
    for left, right, evidence, scope, accounts in (
        ("prop16", "inns81", (old_sources["b8/sak-100927.xml"].id,), "kapittel_1429", accounts1429),
        (
            "inns81",
            "vedtak210",
            (old_sources["originals/votering-161224.html"].id, old_sources["b6/40034048.xml"].id),
            "kapittel_1429",
            ("1429/1", "1429/22"),
        ),
        (
            "inns81",
            "vedtak211",
            (old_sources["originals/votering-161224.html"].id, source211.id),
            "kapittel_1429",
            ("1429/60",),
        ),
        (
            "prop16",
            "inns95",
            (new_by_name["tests/fixtures/b8/sak-100889.xml"].id,),
            "unntatt_1429",
            docs["inns95"].accounts,
        ),
    ):
        valid = all(s.status == "kildeverifisert" for s in sources if s.id in evidence)
        relations.append(
            identified(
                "visningsrelasjon-1",
                PilotRelation(
                    "",
                    docs[left].id,
                    docs[right].id,
                    "dokumentert_behandling",
                    scope,
                    "kildeverifisert" if valid else "uavklart",
                    accounts,
                    evidence,
                    2024,
                ),
            )
        )
    # Kildens alle publikasjonshenvisninger bevares, også like eksport-ID-er.
    for case_source, key, scoped in (
        (old_sources["b8/sak-100927.xml"], "inns81", "kapittel_1429"),
        (new_by_name["tests/fixtures/b8/sak-100889.xml"], "inns95", "unntatt_1429"),
    ):
        raw_case = (
            source_bytes(case_source)
            if isinstance(case_source, OmtaleSource)
            else raw_source(case_source)
        )
        if raw_case is None or case_source.status != "kildeverifisert":
            continue
        case = _xml(raw_case)
        for ref in case.findall(".//{http://data.stortinget.no}publikasjon_referanse"):
            # Et referansebevis har egen identitet, originalt XML og presis lokator.
            statements.append(
                identified(
                    "visningsutsagn-1",
                    Statement(
                        "",
                        docs[key].id,
                        case_source.id,
                        ref.getroottree().getpath(ref),
                        "".join(ref.itertext()),
                        etree.tostring(ref, encoding="unicode"),
                        "saksreferanse_" + scoped,
                        "stortingets_saksregister",
                        "2024",
                        "kildeverifisert",
                        docs[key].accounts,
                        (),
                    ),
                )
            )
    contexts = []
    for observation in observations:
        key = (
            observation.source_unit_id
            if observation.source_system == "visningspilot"
            else "vedtak210"
        )
        evidence = tuple(
            s.id
            for s in statements
            if s.document_id == docs[key].id
            and s.role in {"tilraading", "endelig_vedtak", "eksakt_forslag"}
        )
        contexts.append(
            identified(
                "visningskontekst-1",
                TreatmentContext(
                    "",
                    observation.id,
                    docs[key].id,
                    "nysaldering",
                    "regjering"
                    if key == "prop16"
                    else "tilraading"
                    if key == "inns81"
                    else "vedtak",
                    "regjeringen"
                    if key == "prop16"
                    else "samlet_komite"
                    if key == "inns81"
                    else "stortinget",
                    "kildeverifisert",
                    evidence,
                ),
            )
        )
    # Bare pilotens uttrykkelig kildebeviste tabellkjede; aldri konto-/beløpsjoin til søstergrenen.
    for post in ("1", "22"):
        for meaning in ("for_belop", "endring", "etter_belop"):
            chain = tuple(
                o
                for key in ("prop16", "inns81", "vedtak210")
                for o in observations
                if o.post == post
                and o.meaning == meaning
                and (
                    (o.source_unit_id == key)
                    if key != "vedtak210"
                    else o.figure_type == "stortingsvedtak"
                )
            )
            # Manglende nytt adapterstadium er et synlig hull, aldri en nullverdi.
            # Bare nabostadier med faktiske kildefelt får en feltrelasjon.
            for left_observation, right_observation in zip(chain[:-1], chain[1:], strict=True):
                left_stage = next(
                    c.stage for c in contexts if c.observation_id == left_observation.id
                )
                right_stage = next(
                    c.stage for c in contexts if c.observation_id == right_observation.id
                )
                if (left_stage, right_stage) not in {
                    ("regjering", "tilraading"),
                    ("tilraading", "vedtak"),
                }:
                    continue
                relations.append(
                    identified(
                        "visningsrelasjon-1",
                        PilotRelation(
                            "",
                            left_observation.id,
                            right_observation.id,
                            "dokumentert_tabellfelt",
                            "kapittel_1429",
                            "kildeverifisert",
                            ("1429/" + post,),
                            (
                                left_observation.pointer.artifact_id,
                                right_observation.pointer.artifact_id,
                                old_sources["originals/votering-161224.html"].id,
                            ),
                            2024,
                        ),
                    )
                )
    fullmakt_chain = tuple(
        next((s for s in statements if s.role == role), None)
        for role in (
            "stikkordsfullmakt_forslag",
            "stikkordsfullmakt_tilraading",
            "stikkordsfullmakt_vedtatt",
        )
    )
    for left_statement, right_statement in zip(
        fullmakt_chain[:-1], fullmakt_chain[1:], strict=True
    ):
        if left_statement is None or right_statement is None:
            issues.append("stikkordsfullmaktkjede_innlegg_mangler")
            continue
        relations.append(
            identified(
                "visningsrelasjon-1",
                PilotRelation(
                    "",
                    left_statement.id,
                    right_statement.id,
                    "dokumentert_stikkordsfullmakt",
                    "kapittel_1429",
                    "kildeverifisert",
                    ("1429/60",),
                    (
                        left_statement.source_id,
                        right_statement.source_id,
                        old_sources["originals/votering-161224.html"].id,
                    ),
                    2024,
                ),
            )
        )
    return identified(
        "visningsgrunnlag-1",
        PilotBasis(
            "",
            RULE,
            old.o2b_json,
            sources,
            documents,
            tuple(inventory),
            tuple(statements),
            observations,
            tuple(relations),
            tuple(contexts),
            tuple(dict.fromkeys(issues)),
        ),
    )


def validate_basis(basis: PilotBasis, prepared: PilotInput) -> None:
    if (
        len(basis.sources) > 64
        or len(basis.documents) > 16
        or len(basis.inventory) > 512
        or len(basis.statements) > 512
        or len(basis.observations) > 256
        or len(basis.relations) > 1024
        or basis.o2b_json != prepared.o2b_json
        or basis != structure_basis(prepared, basis.sources)
    ):
        raise ValueError("Visningsgrunnlaget avviker fra sine originaler/regler")
