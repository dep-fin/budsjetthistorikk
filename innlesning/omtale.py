"""Separat, selvforsynt O2-kildegrunnlag. Ingen database- eller nettavhengighet."""

import base64
import binascii
import hashlib
import io
import json
import re
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, cast

from lxml import etree, html
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from .observations import encode, identity

VERSION = "omtale-grunnlag-1"
EXTRACTOR = "o2a-html-pdf-1"
O2B_EXTRACTOR = "o2b-html-pdf-1"
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_METADATA_BYTES = 1024 * 1024
SOURCE_CATALOG = {
    "originals/prop16s.pdf": ("prop-16-s-2024-2025", "application/pdf"),
    "originals/prop16s-ch2.html": ("prop-16-s-2024-2025", "text/html"),
    "originals/prop16s-ch4.html": ("prop-16-s-2024-2025", "text/html"),
    "originals/inns81s.pdf": ("inns-81-s-2024-2025", "application/pdf"),
    "originals/inns81s.html": ("inns-81-s-2024-2025", "text/html"),
    "originals/votering-161224.html": ("votering-2024-12-16-sak25", "text/html"),
    "b6/40034048.xml": ("vedtak-210", "application/xml"),
    "b6/40034048.json": ("vedtak-210", "application/json"),
    "b8/sak-100927.xml": ("sak-100927", "application/xml"),
    "b8/sak-100927.json": ("sak-100927", "application/json"),
}
# Den navngitte samlede avsenderen i den avgrensede Innst. 81 S-prøven.
KS_ACTOR = (
    "Komiteen, medlemmene fra Arbeiderpartiet, Åse Kristin Ask Bakke, Mona Nilsen og Torstein "
    "Tvedt Solberg, fra Høyre, Turid Kristensen og Tage Pettersen, fra Senterpartiet, "
    "Margrethe Haarr og Åslaug Sem-Jacobsen, fra Fremskrittspartiet, Silje Hjemdal, "
    "fra Sosialistisk Venstreparti, Audun Hammer Hovda, og fra Venstre, lederen Grunde Almeland"
)


def is_o2b(extractor: str) -> bool:
    """Revisjonssuffiks identifiserer et nytt uttak med samme eksplisitte B-algoritme."""
    return extractor == O2B_EXTRACTOR or extractor.startswith(O2B_EXTRACTOR + "-")


@dataclass(frozen=True)
class OmtaleSource:
    id: str
    name: str
    document_id: str
    media_type: str
    expected_sha256: str | None
    sha256: str | None
    byte_count: int | None
    content_base64: str | None
    metadata_json: str
    status: str


@dataclass(frozen=True)
class Heading:
    locator: str
    text: str


@dataclass(frozen=True)
class Section:
    id: str
    key: str
    source_id: str
    document_id: str
    extractor: str
    locator: str
    text: str
    html: str
    hierarchy: tuple[Heading, ...]
    actor: str
    role: str
    accounts: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class RepresentationLink:
    id: str
    html_section_id: str
    pdf_section_id: str
    status: str
    reason: str


@dataclass(frozen=True)
class OmtaleBasis:
    id: str
    extractor: str
    sources: tuple[OmtaleSource, ...]
    sections: tuple[Section, ...]
    representation_links: tuple[RepresentationLink, ...]
    issues: tuple[str, ...]
    version: str = VERSION


def identified[T](namespace: str, value: T) -> T:
    """Bare nye omtaleobjekter; gamle identiteter røres ikke."""
    data = asdict(cast(Any, value))
    data["id"] = ""
    return cast(T, replace(cast(Any, value), id=identity(namespace, data)))


def source_bytes(source: OmtaleSource) -> bytes | None:
    if source.content_base64 is None:
        if source.sha256 is not None or source.byte_count is not None:
            raise ValueError("Omtalekilde uten byte kan ikke ha hash/størrelse")
        return None
    try:
        raw = base64.b64decode(source.content_base64, validate=True)
    except (ValueError, binascii.Error) as error:
        raise ValueError("Ugyldig base64 i omtaleoriginal") from error
    if (
        len(raw) > MAX_SOURCE_BYTES
        or source.byte_count != len(raw)
        or source.sha256 != hashlib.sha256(raw).hexdigest()
    ):
        raise ValueError("Omtaleoriginalens byte/hash er endret")
    return raw


def _status(raw: bytes | None, expected: str | None, metadata_json: str) -> str:
    if raw is None:
        return "mangler"
    metadata = json.loads(metadata_json)
    return (
        "kildeverifisert"
        if isinstance(metadata, dict)
        and metadata.get("sha256") == expected == hashlib.sha256(raw).hexdigest()
        and type(metadata.get("bytes")) is int
        and metadata["bytes"] == len(raw)
        else "motstrid"
    )


def _path(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Kildepeker utenfor valgt katalog")
    return path


def _read_metadata(path: Path) -> Any:
    with path.open("rb") as source:
        raw = source.read(MAX_METADATA_BYTES + 1)
    if len(raw) > MAX_METADATA_BYTES:
        raise ValueError("Omtalemetadata overstiger 1 MiB")
    return json.loads(raw.decode("utf-8"))


def _read_manifest(path: Path) -> list[dict[str, Any]]:
    manifest = _read_metadata(path)
    if not isinstance(manifest, list) or any(not isinstance(m, dict) for m in manifest):
        raise ValueError("Omtalemanifest må være en liste av objekter")
    return manifest


def import_omtale(root: Path, supporting_root: Path, *, extractor: str = EXTRACTOR) -> OmtaleBasis:
    """Åpne originalene på nytt og bevar faktiske byte ved uttrykkelig A-/B-valg."""
    if not extractor or len(extractor) > 80:
        raise ValueError("Velg en eksplisitt uttrekksversjon på høyst 80 tegn")
    try:
        manifest = _read_manifest(root / "source-manifest.json")
    except (OSError, ValueError):
        manifest = []
    try:
        supporting = _read_manifest(root / "supporting-manifest.json")
    except (OSError, ValueError):
        supporting = []
    sources: list[OmtaleSource] = []
    for name, (document, mime) in SOURCE_CATALOG.items():
        if not name.startswith("originals/"):
            continue
        matches = [m for m in manifest if m.get("file") == name and m.get("status") == 200]
        metadata = matches[0] if len(matches) == 1 else {"error": "manifest_mangler_eller_tvetydig"}
        sources.append(_read_source(root, name, document, mime, metadata))
    for prefix, document in (("b6/40034048", "vedtak-210"), ("b8/sak-100927", "sak-100927")):
        try:
            meta_path = _path(supporting_root, prefix + ".json")
            metadata = _read_metadata(meta_path)
            if not isinstance(metadata, dict):
                raise ValueError("Støttemetadata må være et objekt")
        except (OSError, ValueError):
            metadata = {"error": "stottemetadata_mangler_eller_korrupt"}
        sources.append(
            _read_source(supporting_root, prefix + ".xml", document, "application/xml", metadata)
        )
        # Sidevognens eksakte byte bevares også, med O1s uavhengige hash.
        matches = [
            m
            for m in supporting
            if m.get("repository_path") == "tests/fixtures/" + prefix + ".json"
        ]
        sidecar = matches[0] if len(matches) == 1 else {}
        sources.append(
            _read_source(supporting_root, prefix + ".json", document, "application/json", sidecar)
        )
    return structure(tuple(sources), extractor)


def _read_source(
    root: Path, name: str, document: str, mime: str, metadata: dict[str, Any]
) -> OmtaleSource:
    raw = None
    try:
        path = _path(root, name)
        if path.stat().st_size > MAX_SOURCE_BYTES:
            raise ValueError("Omtaleoriginal overstiger 16 MiB")
        raw = path.read_bytes()
    except OSError:
        pass
    expected = metadata.get("sha256")
    if not isinstance(expected, str) or not re.fullmatch("[0-9a-f]{64}", expected):
        expected = None
    source = OmtaleSource(
        "",
        name,
        document,
        mime,
        expected,
        hashlib.sha256(raw).hexdigest() if raw is not None else None,
        len(raw) if raw is not None else None,
        base64.b64encode(raw).decode("ascii") if raw is not None else None,
        encode(metadata),
        _status(raw, expected, encode(metadata)),
    )
    return identified("omtale-kilde-1", source)


def _node(document: Any, selector: str) -> Any:
    nodes = document.xpath(selector)
    if len(nodes) != 1:
        raise ValueError("manglende_eller_tvetydig_lokator:" + selector)
    return nodes[0]


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _pdf_comparable(value: str) -> str:
    return re.sub(r"[-\s]+", "", value)


def _section(
    source: OmtaleSource,
    document: Any,
    key: str,
    selector: str,
    heading_selectors: tuple[str, ...],
    extractor: str,
    actor: str,
    role: str,
    accounts: tuple[str, ...],
) -> Section:
    node = _node(document, selector)
    hierarchy = tuple(
        Heading(n.getroottree().getpath(n), n.text_content())
        for s in heading_selectors
        for n in [_node(document, s)]
    )
    return identified(
        "omtale-seksjon-1",
        Section(
            "",
            key,
            source.id,
            source.document_id,
            extractor,
            node.getroottree().getpath(node),
            node.text_content(),
            html.tostring(node, encoding="unicode", with_tail=False),
            hierarchy,
            actor,
            role,
            accounts,
            "kildeverifisert",
        ),
    )


def structure(sources: tuple[OmtaleSource, ...], extractor: str) -> OmtaleBasis:
    """Samme strukturering brukes ved import og gjenlesing av innebygde originalbyte."""
    sections: list[Section] = []
    issues: list[str] = []
    for source in sources:
        raw = source_bytes(source)
        if source.status != _status(raw, source.expected_sha256, source.metadata_json):
            raise ValueError("Omtalekilden har feil status")
        if source.id != identified("omtale-kilde-1", replace(source, id="")).id:
            raise ValueError("Omtalekilden har feil identitet")
        if source.status != "kildeverifisert":
            issues.append(source.status + ":" + source.name)
            continue
        assert raw is not None
        try:
            if source.name == "originals/prop16s.pdf":
                page = PdfReader(io.BytesIO(raw)).pages[2].extract_text()
                sections.append(
                    identified(
                        "omtale-seksjon-1",
                        Section(
                            "",
                            "P1_PDF",
                            source.id,
                            source.document_id,
                            extractor,
                            "pdf:page=3",
                            page,
                            "",
                            (),
                            "regjeringen",
                            "representasjonsbelegg",
                            (),
                            "kildeverifisert",
                        ),
                    )
                )
            if source.media_type != "text/html":
                continue
            doc = html.fromstring(raw.decode("utf-8"), parser=html.HTMLParser(no_network=True))
            title = compact(_node(doc, "//title").text_content()).replace("–", "-")
            expected_title = {
                "prop-16-s-2024-2025": "Prop. 16 S (2024-2025)",
                "inns-81-s-2024-2025": "Innst. 81 S (2024-2025)",
            }
            if (
                source.document_id in expected_title
                and expected_title[source.document_id] not in title
            ):
                issues.append("dokumentidentitet_motstrid:" + source.name)
            if source.name == "originals/prop16s-ch2.html":
                sections.append(
                    _section(
                        source,
                        doc,
                        "P1",
                        "//*[@id='kap2_ch7_ch1']",
                        (
                            "//*[@id='kap2']/h1",
                            "//*[@id='kap2_ch7']/h2",
                            "//*[@id='kap2_ch7_ch1']/h3",
                        ),
                        extractor,
                        "regjeringen",
                        "regjeringsforklaring",
                        ("1429/1", "1429/22"),
                    )
                )
                sections.append(
                    _section(
                        source,
                        doc,
                        "PN",
                        "//*[@id='kap2_ch7_ch3']",
                        ("//*[@id='kap2']/h1", "//*[@id='kap2_ch7']/h2"),
                        extractor,
                        "regjeringen",
                        "nabokontekst_fullmakt",
                        ("1429/60",),
                    )
                )
            elif source.name == "originals/prop16s-ch4.html":
                chapter = "//tr[td[normalize-space()='1429']]"
                sections.append(
                    _section(
                        source,
                        doc,
                        "PT",
                        chapter + "/following-sibling::tr[1]",
                        (chapter, chapter + "/following-sibling::tr[2]"),
                        extractor,
                        "regjeringen",
                        "eksakt_forslag",
                        ("1429/1",),
                    )
                )
            elif source.name == "originals/inns81s.html":
                for key, identifier, role, actor, headings in (
                    (
                        "K1",
                        "m1_1_1",
                        "gjengivelse_av_regjeringen",
                        "komiteen_gjengir_regjeringen",
                        ("//*[@id='m1']//h2", "//*[@id='m1_1']//h3", "//*[@id='m1_1_1']//h4"),
                    ),
                    ("KS", "m2", "samlet_stotte", "samlet_komite", ()),
                    ("KT", "m3", "tilrading", "samlet_komite", ()),
                ):
                    # Innstillingens overskriftsnivåer kontrolleres fra egne overskriftsnoder.
                    if key == "K1":
                        headings = (
                            "//*[@id='m1']//*[self::h1 or self::h2 or self::h3][1]",
                            "//*[@id='m1_1']//*[self::h2 or self::h3 or self::h4][1]",
                            "//*[@id='m1_1_1']//*[self::h3 or self::h4 or self::h5][1]",
                        )
                    section = _section(
                        source,
                        doc,
                        key,
                        f"//*[@id='{identifier}']",
                        headings,
                        extractor,
                        actor,
                        role,
                        ("1429/1", "1429/22") if key == "K1" else ("1429/1", "1429/22", "1429/60"),
                    )
                    known_role = (
                        (
                            key == "KS"
                            and [compact(p.text_content()) for p in doc.xpath("//*[@id='m2']//p")]
                            == [KS_ACTOR + ", støtter regjeringens forslag i proposisjonen."]
                        )
                        or (key == "KT" and "en samlet komité" in compact(section.text))
                        or (key == "K1" and compact(section.hierarchy[0].text) == "Sammendrag")
                    )
                    if not known_role:
                        section = identified(
                            "omtale-seksjon-1",
                            replace(
                                section,
                                id="",
                                actor="ukjent",
                                role="ukjent_rolle",
                                status="ukjent_rolle",
                            ),
                        )
                    sections.append(section)
                # Ingen rollearv fra den felles plenumsdebatten. Hele Innst. 81 S kontrolleres.
                content = compact(_node(doc, "//*[@id='m3']").text_content())
                if "en samlet komité" in content and not re.search(
                    r"mindretall|flertall", doc.text_content(), re.I
                ):
                    issues.append("mindretall_kontrollert_fravaerende:Innst.81S")
                else:
                    issues.append("komiterolle_uavklart:Innst.81S")
            elif source.name == "originals/votering-161224.html":
                sections.append(
                    _section(
                        source,
                        doc,
                        "V",
                        "//*[@id='2024-12-16-25']",
                        (),
                        extractor,
                        "stortinget",
                        "vedtakelse",
                        ("1429/1", "1429/22", "1429/60"),
                    )
                )
        except (ValueError, IndexError, KeyError, etree.LxmlError, PdfReadError) as error:
            issues.append("strukturfeil:" + source.name + ":" + str(error))
    # En ny etikett velger B. Tidligere etiketter rekonstruerer fortsatt bare A.
    if is_o2b(extractor):
        for source in sources:
            if source.status != "kildeverifisert":
                continue
            specs = {
                "originals/prop16s-ch2.html": (
                    "P22",
                    "//*[@id='kap2_ch7_ch2']",
                    ("//*[@id='kap2']/h1", "//*[@id='kap2_ch7']/h2", "//*[@id='kap2_ch7_ch2']/h3"),
                    "regjeringen",
                    "regjeringsforklaring",
                ),
                "originals/prop16s-ch4.html": (
                    "PT22",
                    "//tr[td[normalize-space()='1429']]/following-sibling::tr[3]",
                    (
                        "//tr[td[normalize-space()='1429']]",
                        "//tr[td[normalize-space()='1429']]/following-sibling::tr[4]",
                    ),
                    "regjeringen",
                    "eksakt_forslag",
                ),
                "originals/inns81s.html": (
                    "K22",
                    "//*[@id='m1_1_2']",
                    (
                        "//*[@id='m1']//*[self::h1 or self::h2 or self::h3][1]",
                        "//*[@id='m1_1']//*[self::h2 or self::h3 or self::h4][1]",
                        "//*[@id='m1_1_2']//*[self::h3 or self::h4 or self::h5][1]",
                    ),
                    "komiteen_gjengir_regjeringen",
                    "gjengivelse_av_regjeringen",
                ),
            }
            if source.name not in specs:
                continue
            try:
                raw = source_bytes(source)
                assert raw is not None
                doc = html.fromstring(raw.decode("utf-8"), parser=html.HTMLParser(no_network=True))
                key, selector, b_headings, actor, role = specs[source.name]
                section = _section(
                    source,
                    doc,
                    key,
                    selector,
                    b_headings,
                    extractor,
                    actor,
                    role,
                    ("1429/22", "1429/1") if key != "PT22" else ("1429/22",),
                )
                if key == "K22" and compact(section.hierarchy[0].text) != "Sammendrag":
                    section = identified(
                        "omtale-seksjon-1",
                        replace(
                            section,
                            id="",
                            actor="ukjent",
                            role="ukjent_rolle",
                            status="ukjent_rolle",
                        ),
                    )
                sections.append(section)
            except (ValueError, IndexError, KeyError, etree.LxmlError) as error:
                issues.append("strukturfeil:" + source.name + ":" + str(error))
    links: list[RepresentationLink] = []
    by_key = {s.key: s for s in sections}
    if "P1" in by_key and "P1_PDF" in by_key:
        p1, pdf = by_key["P1"], by_key["P1_PDF"]
        # PDF-leserekkefølge og orddeling er forskjellig fra HTML; ingen byteekvivalens hevdes.
        body = html.fromstring(p1.html).xpath(".//p")
        matches = len(body) == 1 and _pdf_comparable(body[0].text_content()) in _pdf_comparable(
            pdf.text
        )
        status = "kildeverifisert" if matches else "motstrid"
        links.append(
            identified(
                "omtale-representasjon-1",
                RepresentationLink(
                    "",
                    p1.id,
                    pdf.id,
                    status,
                    "Samme Prop. 16 S (2024-2025); P1 på trykt/PDF-side 3. "
                    "Hele P1-avsnittet samsvarer etter fjerning av PDF-mellomrom/orddeling; "
                    "ingen full dokumentekvivalens eller byteekvivalens.",
                ),
            )
        )
        if status != "kildeverifisert":
            issues.append("motstrid:PDF_HTML_P1")
    for section in sections:
        if section.status != "kildeverifisert":
            issues.append(section.status + ":" + section.key)
    return identified(
        VERSION, OmtaleBasis("", extractor, sources, tuple(sections), tuple(links), tuple(issues))
    )


def validate_basis(basis: OmtaleBasis) -> None:
    if (
        basis.version != VERSION
        or len(basis.sources) != len(SOURCE_CATALOG)
        or len({s.name for s in basis.sources}) != len(SOURCE_CATALOG)
        or {s.name: (s.document_id, s.media_type) for s in basis.sources} != SOURCE_CATALOG
        or not basis.extractor
        or len(basis.extractor) > 80
    ):
        raise ValueError("Ukjent eller ufullstendig omtalegrunnlag")
    expected = structure(basis.sources, basis.extractor)
    if basis != expected:
        raise ValueError("Omtalegrunnlaget avviker fra gjenleste originaler/lokatorer/roller")
