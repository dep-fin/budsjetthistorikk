"""Fast Prop. 16 S-adapter over typet T1. Ingen analyseavhengighet eller nett."""

import base64
import gzip
import hashlib
import io
import json
import re
from functools import lru_cache
from pathlib import Path

from lxml import html

from .legacy_html import parse_legacy_html
from .observations import AmountObservation, Interpretation, SourcePointer, encode, identity
from .omtale import compact, identified, source_bytes
from .proposisjon16_model import RULE, Authorization, Basis, Branch, DocumentCoverage, FieldBinding
from .visningspilot import MAX_PARENT_BYTES, MAX_SOURCE_BYTES, _xml, raw_source
from .visningspilot import validate_basis as validate_t1
from .visningspilot_model import PilotBasis, PilotInput, PilotSource, TreatmentContext

PROP_SOURCE = "docs/research/omtale-o1/originals/prop16s-ch4.html"
HISTORICAL = "prop16_delvis_strukturert:35_av_37_tabellgrupper_uten_belopsimport"
RESEARCH = "docs/research/to-visninger-37/originals/forgrening/"
SOURCE_CATALOG = {
    RESEARCH + "inns95s-20261022-reused.html": (
        "text/html",
        "1f159a3ca1df3e0bc35617644d0b36f7c92fd5684947f6eca5510595af533a03",
    ),
    RESEARCH + "reused-inns95-manifest.json": (
        "application/json",
        "8fc18d92f651e3d075bb4bf86498aff90eee3033297db920b32da83a4019bc4d",
    ),
}


def _source(name: str, raw: bytes | None, metadata: str) -> PilotSource:
    properties = json.loads(metadata)
    expected = {"repository_path"} if raw is not None else {"repository_path", "error_type"}
    if (
        not isinstance(properties, dict)
        or set(properties) != expected
        or properties.get("repository_path") != name
        or (
            raw is None
            and (not isinstance(properties["error_type"], str) or not properties["error_type"])
        )
    ):
        raise ValueError("T5-kildens lokale innlesningsmetadata avviker")
    mime, pin = SOURCE_CATALOG[name]
    digest = hashlib.sha256(raw).hexdigest() if raw is not None else None
    return identified(
        "proposisjonskilde16-1",
        PilotSource(
            "",
            name,
            "inns95_representasjon22",
            mime,
            pin,
            base64.b64encode(raw).decode("ascii") if raw is not None else None,
            digest,
            len(raw) if raw is not None else None,
            "mangler" if raw is None else "kildeverifisert" if digest == pin else "motstrid",
            metadata,
        ),
    )


def _authorizations(t1_basis: PilotBasis, prepared: PilotInput) -> tuple[Authorization, ...]:
    original = next(s for s in prepared.basis.sources if s.name == "originals/prop16s-ch4.html")
    raw = source_bytes(original)
    assert raw is not None
    root = parse_legacy_html(raw)
    document = next(d for d in t1_basis.documents if d.key == "prop16")
    specs = (
        ("57", "II", "1", "bestillingsramme", ("1420/21",), 8_000_000, "./p"),
        ("58", "III", "1", "tilsagnsramme", ("1420/61",), 601_000_000, ".//tbody/tr[2]"),
        ("58", "III", "2", "tilsagnsramme", ("1420/62",), 266_300_000, ".//tbody/tr[3]"),
        (
            "59",
            "IV",
            "1",
            "felles_forpliktelsesramme",
            ("1420/39", "1420/69", "1420/79"),
            16_300_000,
            "./p",
        ),
        ("60", "V", "1", "stikkord", ("1420/66",), None, "./ol/li[1]"),
        ("60", "V", "2", "stikkord", ("1420/87",), None, "./ol/li[2]"),
        ("60", "V", "3", "stikkord", ("1429/60",), None, "./ol/li[3]"),
        ("61", "VI", "1", "forskutteringsramme", ("1471/1", "4471/3"), 25_000_000, "./ol/li[1]"),
        ("61", "VI", "2", "regnskapsregel", (), None, "./ol/li[2]"),
    )
    result = []
    for anchor, roman, point, role, accounts, frame, selector in specs:
        section = root.get_element_by_id("kap2-p" + anchor).getparent()
        assert section is not None
        node = section.xpath(selector)[0]
        # Punktets atomiske lokator suppleres med hele seksjonens vilkår/innledning.
        result.append(
            identified(
                "proposisjonsfullmakt16-1",
                Authorization(
                    "",
                    document.id,
                    original.id,
                    node.getroottree().getpath(node),
                    roman,
                    point,
                    role,
                    "2024; fremtidige år; nye forpliktelser og gammelt ansvar"
                    if roman in {"II", "III", "IV"}
                    else "2024",
                    accounts,
                    frame,
                    section.text_content(),
                    html.tostring(section, encoding="unicode", with_tail=False),
                    "kildebundet_inventar_ikke_bevilgningsdelta",
                ),
            )
        )
    return tuple(result)


def _branches(
    t1_basis: PilotBasis, authorizations: tuple[Authorization, ...]
) -> tuple[Branch, ...]:
    documents = {d.key: d for d in t1_basis.documents}
    prop = documents["prop16"]
    table_accounts = tuple(
        item.chapter + "/" + item.post
        for item in t1_basis.inventory
        if item.document_id == prop.id and item.role == "endringstabell"
    )
    parent_source = next(
        s
        for s in t1_basis.sources
        if s.document_key == "forelder2024" and s.media_type == "application/gzip"
    )
    parent_raw = raw_source(parent_source)
    decisions: dict[str, str] = {}
    if parent_raw is not None and parent_source.status == "kildeverifisert":
        with gzip.GzipFile(fileobj=io.BytesIO(parent_raw)) as archive:
            expanded = archive.read(MAX_PARENT_BYTES + 1)
        if len(expanded) > MAX_PARENT_BYTES:
            raise ValueError("T5: for stor bevart vedtaksforelder")
        parent = _xml(expanded)
        ns = "{http://data.stortinget.no}"
        for node in parent.findall(".//" + ns + "stortingsvedtak"):
            identifier = node.findtext(ns + "id") or ""
            if identifier not in {
                "40034220",
                "40034221",
                "40034222",
                "40034223",
                "40034224",
                "40034225",
            }:
                continue
            if node.findtext(ns + "sak_id") != "100889":
                raise ValueError("T5: vedtaksgrenens saksidentitet avviker")
            decisions[identifier] = parent_source.id + ":" + node.getroottree().getpath(node)
    specs = (
        (
            "I",
            "I",
            "inns81",
            "100927",
            tuple(a for a in table_accounts if a.startswith("1429/")),
            ("40034048",),
        ),
        (
            "I",
            "I",
            "inns95",
            "100889",
            tuple(a for a in table_accounts if not a.startswith("1429/")),
            ("40034220",),
        ),
        ("II", "II", "inns95", "100889", ("1420/21",), ("40034221",)),
        ("III", "III", "inns95", "100889", ("1420/61", "1420/62"), ("40034222",)),
        ("IV", "IV", "inns95", "100889", ("1420/39", "1420/69", "1420/79"), ("40034223",)),
        ("V.1-2", "V", "inns95", "100889", ("1420/66", "1420/87"), ("40034224",)),
        ("V.3", "II", "inns81", "100927", ("1429/60",), ("40034049",)),
        ("VI", "VI", "inns95", "100889", ("1471/1", "4471/3"), ("40034225",)),
    )
    result = []
    for point, committee, target, case, accounts, decision_ids in specs:
        evidence = tuple(
            s.id
            for s in t1_basis.sources
            if s.document_key == target and s.status == "kildeverifisert"
        )
        evidence += tuple(
            a.id
            for a in authorizations
            if a.roman == point.split(".")[0] and set(a.accounts) & set(accounts)
        )
        evidence += tuple(decisions[d] for d in decision_ids if d in decisions)
        valid = all(
            s.status == "kildeverifisert" for s in t1_basis.sources if s.document_key == target
        )
        valid = valid and (target != "inns95" or all(d in decisions for d in decision_ids))
        result.append(
            identified(
                "proposisjonsgren16-1",
                Branch(
                    "",
                    prop.id,
                    documents[target].id,
                    case,
                    accounts,
                    point,
                    committee,
                    decision_ids,
                    evidence,
                    "kildeverifisert" if valid else "uavklart",
                    "ikke_strukturert_T6" if target == "inns95" else "T1_bevart",
                ),
            )
        )
    return tuple(result)


def import_basis(t1_basis: PilotBasis, prepared: PilotInput, root: Path = Path(".")) -> Basis:
    """Importer T5 fra de samme bevarte originalene, uten duplisert råpayload."""
    sources = []
    for name in SOURCE_CATALOG:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("T5-kilde utenfor valgt rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(MAX_SOURCE_BYTES + 1)
            if len(raw) > MAX_SOURCE_BYTES:
                raise ValueError("T5-kilde overstiger 16 MiB")
            metadata = encode({"repository_path": name})
        except (OSError, ValueError) as error:
            raw = None
            metadata = encode({"repository_path": name, "error_type": type(error).__name__})
        sources.append(_source(name, raw, metadata))
    return structure_basis(t1_basis, prepared, tuple(sources))


@lru_cache(maxsize=2)
def structure_basis(
    t1_basis: PilotBasis, prepared: PilotInput, sources: tuple[PilotSource, ...]
) -> Basis:
    validate_t1(t1_basis, prepared)
    if tuple(s.name for s in sources) != tuple(SOURCE_CATALOG):
        raise ValueError("T5: ukjent, duplisert eller manglende kildekatalog")
    for item in sources:
        if item != _source(item.name, raw_source(item), item.metadata_json):
            raise ValueError("T5: kildekatalogens rolle/hash/status avviker")
    document = next(d for d in t1_basis.documents if d.key == "prop16")
    source = next(s for s in t1_basis.sources if s.name == PROP_SOURCE)
    observations: list[AmountObservation] = []
    contexts: list[TreatmentContext] = []
    interpretation = Interpretation(
        adapter_version=RULE,
        round="nysaldering",
        round_evidence="Prop. 16 S kapittel 4 I: Endringer i statsbudsjettet 2024",
        reason="T5: 35 øvrige eksakte forslagstrioer; ingen nye vedtak",
    )
    if source.status == "kildeverifisert":
        raw = raw_source(source)
        assert raw is not None
        root = parse_legacy_html(raw)
        for table in root.xpath("//table")[:2]:
            chapter, chapter_name = "", ""
            rows = table.xpath("./tbody/tr")
            for index, row in enumerate(rows):
                cells = row.xpath("./td")
                values = [compact(c.text_content()) for c in cells]
                if len(values) != 4:
                    continue
                if values[0].isdigit():
                    chapter, chapter_name = str(int(values[0])), values[2]
                if not values[1].isdigit() or not (
                    "økes med" in values[2] or "reduseres med" in values[2]
                ):
                    continue
                post = str(int(values[1]))
                if chapter == "1429":
                    continue
                levels = rows[index + 1]
                level_text = compact(levels.xpath("./td")[2].text_content())
                match = re.fullmatch(r"fra kr ([\d ]+) til kr ([\d ]+)", level_text)
                if not chapter or match is None:
                    raise ValueError("T5: ufullstendig fast tabellgruppe")
                raw_values = (match[1].strip(), values[3], match[2].strip())
                before, delta, after = (int(v.replace(" ", "")) for v in raw_values)
                if "reduseres med" in values[2]:
                    delta = -delta
                if before + delta != after:
                    raise ValueError("T5: originalens før/endring/etter avviker")
                for meaning, raw_value, value, node, column in zip(
                    ("for_belop", "endring", "etter_belop"),
                    raw_values,
                    (before, delta, after),
                    (levels, row, levels),
                    (3, 4, 3),
                    strict=True,
                ):
                    observation = AmountObservation(
                        dataset="prove",
                        source_system="proposisjon16",
                        source_unit_id="prop16",
                        source_revision_id=source.sha256 or "",
                        interpretation_id=interpretation.id,
                        pointer=SourcePointer(
                            source.sha256 or "",
                            node.getroottree().getpath(node) + f"/td[{column}]",
                            meaning,
                            raw_record=html.tostring(node, encoding="unicode", with_tail=False),
                        ),
                        step_id=identity(RULE, document.id, chapter, post),
                        raw_value=raw_value,
                        amount_text=raw_value,
                        amount_kr=value,
                        chapter_raw=chapter,
                        post_raw=values[1],
                        chapter=chapter,
                        post=post,
                        chapter_name=chapter_name,
                        purpose=values[2],
                        detail_level="post",
                        budget_year=2024,
                        year_evidence=interpretation.round_evidence,
                        unit_raw="Kroner",
                        currency="NOK",
                        multiplier="1",
                        precision="hele kroner",
                        conversion_rule=interpretation.normalization_rule,
                        normalization_evidence=source.id,
                        figure_type="regjeringsforslag",
                        proposal_identity=document.id,
                        proposal_author="regjeringen",
                        round="nysaldering",
                        round_evidence=interpretation.round_evidence,
                        stage_raw=document.title,
                        meaning=meaning,
                        scope="enkeltledd",
                        classification_evidence=source.id,
                        structure_status="strukturert",
                    )
                    observations.append(observation)
                    contexts.append(
                        identified(
                            "proposisjonskontekst16-1",
                            TreatmentContext(
                                "",
                                observation.id,
                                document.id,
                                "nysaldering",
                                "regjering",
                                "regjeringen",
                                "kildeverifisert",
                                (source.id,),
                            ),
                        )
                    )
        if len(observations) != 105:
            raise ValueError("T5: det faste originalinventaret er ikke 35 trioer")
    all_observations = t1_basis.observations + tuple(observations)
    bindings = tuple(
        identified(
            "proposisjonsbinding16-1",
            FieldBinding(
                "",
                item.id,
                tuple(
                    o.id
                    for o in all_observations
                    if o.source_unit_id == "prop16"
                    and (o.chapter, o.post) == (item.chapter, item.post)
                ),
            ),
        )
        for item in t1_basis.inventory
        if item.document_id == document.id and item.role == "endringstabell"
    )
    fields = sum(len(b.observation_ids) for b in bindings)
    coverage = identified(
        "proposisjonsdekning16-1",
        DocumentCoverage(
            "",
            document.id,
            37,
            fields,
            45,
            "111_strukturerte_endringstabellfelt" if fields == 111 else "tabellstadium_mangler",
            "bare_endringstabell; omtale_og_fullmaktsvilkar_ikke_fulltolket",
            HISTORICAL,
        ),
    )
    authorizations = _authorizations(t1_basis, prepared)
    branches = _branches(t1_basis, authorizations)
    issues = [
        "inns95_belopsstadium_ustrukturert:T6",
        "aarsdekning_delvis",
        "historisk_T1_avvik:" + HISTORICAL,
    ]
    issues.extend(s.status + ":" + s.name for s in sources if s.status != "kildeverifisert")
    reused = sources[0]
    current = next(
        s for s in t1_basis.sources if s.document_key == "inns95" and s.media_type == "text/html"
    )
    if reused.status == current.status == "kildeverifisert":
        old_raw, new_raw = raw_source(reused), raw_source(current)
        assert old_raw is not None and new_raw is not None
        old_html, new_html = parse_legacy_html(old_raw), parse_legacy_html(new_raw)
        if not all(
            compact(old_html.get_element_by_id(key).text_content())
            == compact(new_html.get_element_by_id(key).text_content())
            for key in ("m1", "m2", "m3", "m4")
        ):
            raise ValueError("T5: de bevarte 95-representasjonenes hovedtekst avviker")
        issues.append("inns95_to_beriktigede_html:lik_hovedtekst_ukjent_rettelseshistorikk")
    else:
        issues.append("inns95_representasjonssammenligning_mangler:ukjent_rettelseshistorikk")
    return identified(
        "proposisjonsgrunnlag16-1",
        Basis(
            "",
            RULE,
            t1_basis,
            sources,
            tuple(observations),
            tuple(contexts),
            bindings,
            (coverage,),
            authorizations,
            branches,
            tuple(issues),
        ),
    )


def validate_basis(basis: Basis, prepared: PilotInput) -> None:
    if basis != structure_basis(basis.t1_basis, prepared, basis.sources):
        raise ValueError("T5: basis avviker fra originaler, gammel identitet eller dekning")
