"""T1s strengere kildegrense for seks overførte 210-felt. Gamle lesere endres ikke."""

import json
import re

from lxml import etree, html

from .ingestion import NS, structure_node, text
from .model import Report
from .observations import (
    AmountObservation,
    Artifact,
    DocumentReference,
    Interpretation,
    SourcePointer,
    encode,
    identity,
)
from .omtale import source_bytes
from .organization_register import lookup
from .visningspilot_model import PilotInput


def validate_adopted(prepared: PilotInput) -> None:
    """Gjenskap hele observasjonsobjekter fra pinnet original og kjent gammel tolkning."""
    sources = {s.name: s for s in prepared.basis.sources}
    raw, metadata_raw = (source_bytes(sources[n]) for n in ("b6/40034048.xml", "b6/40034048.json"))
    assert raw is not None and metadata_raw is not None
    metadata = json.loads(metadata_raw)
    parsed = Report("", sources["b6/40034048.xml"].sha256 or "", metadata, True)
    root = etree.fromstring(
        raw, etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    )
    nodes = root.findall(NS + "stortingsvedtak_liste/" + NS + "stortingsvedtak")
    if len(nodes) != 1:
        raise ValueError("Tvetydig vedtaksoriginal")
    structure_node(parsed, nodes[0], "2024-2025")
    decision = parsed.decision
    assert decision is not None
    extraction = prepared.extraction
    interpretation = Interpretation(adapter_version="storting-belop-v2")
    artifact = Artifact(
        parsed.source_sha256,
        "stortingsvedtak-2024-2025.xml",
        str(metadata.get("fixture_kind", "http_original")),
        "text/xml",
        len(raw),
        encode(metadata),
    )
    unit = f"storting:{decision.session}:{decision.id}"
    if (
        extraction.interpretation != interpretation
        or extraction.artifact != artifact
        or extraction.dataset != "prove"
        or extraction.source_system != "storting"
        or extraction.source_unit_id != unit
    ):
        raise ValueError("T1s gamle vedtaksuttrekk/tolkning avviker fra original")
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
    document = html.fromstring(decision.html, parser=html.HTMLParser(no_network=True))
    tables = document.findall(".//table")
    if len(tables) != 1:
        raise ValueError("Tvetydig vedtakstabell")
    rows = tables[0].findall(".//tr")
    if len(rows) != 6 or [text(c) for c in rows[0]] != ["Kap.", "Post", "Formål", "Kroner"]:
        raise ValueError("T1s vedtaksinventar avviker")
    chapter, chapter_name = text(rows[1][0]), text(rows[1][2])
    years = set(re.findall(r"statsbudsjettet (20\d{2})", decision.title, re.I))
    if chapter != "1429" or years != {"2024"}:
        raise ValueError("T1s vedtakskonto/år avviker")
    expected = []
    for index, post in ((2, "1"), (4, "22")):
        delta, levels = rows[index], rows[index + 1]
        purpose, raw_delta = text(delta[2]), text(delta[3])
        level_match = re.fullmatch(r"fra kr ([\d ]+) til kr ([\d ]+)", text(levels[2]))
        if text(delta[1]) != post or level_match is None:
            raise ValueError("T1s vedtaksgruppe avviker")
        values = (level_match[1].strip(), raw_delta, level_match[2].strip())
        delta_locator = f"table[1]/tr[{index + 1}]"
        step = identity(unit, extraction.source_revision_id, delta_locator)
        for meaning, value in zip(("for_belop", "endring", "etter_belop"), values, strict=True):
            is_delta = meaning == "endring"
            row = delta if is_delta else levels
            locator = delta_locator + "/td[4]" if is_delta else f"table[1]/tr[{index + 2}]/td[3]"
            amount = int(value.replace(" ", ""))
            if is_delta and "reduseres med" in purpose:
                amount = -amount
            expected.append(
                AmountObservation(
                    dataset=extraction.dataset,
                    source_system="storting",
                    source_unit_id=unit,
                    source_revision_id=extraction.source_revision_id,
                    interpretation_id=interpretation.id,
                    pointer=SourcePointer(
                        artifact.sha256,
                        locator,
                        meaning,
                        raw_record=etree.tostring(row, encoding="unicode", method="html"),
                    ),
                    step_id=step,
                    raw_value=value,
                    amount_text=value,
                    amount_kr=amount,
                    chapter_raw=chapter,
                    post_raw=post,
                    chapter=chapter,
                    post=post,
                    chapter_name=chapter_name,
                    purpose=purpose,
                    detail_level="post",
                    budget_year=2024,
                    year_evidence="Uttrykkelig budsjettår i vedtakstittelen: " + decision.title,
                    decision_date=decision.date,
                    decision_session=decision.session,
                    api_id=decision.id,
                    unit_raw="Kroner",
                    currency="NOK",
                    multiplier="1",
                    precision="Hele kroner",
                    conversion_rule=interpretation.normalization_rule,
                    normalization_evidence=(
                        "Kroner i tabellhodet; beløpscelle og eventuelle retningsord"
                    ),
                    figure_type="stortingsvedtak",
                    round="uavklart",
                    stage_raw=decision.title,
                    meaning=meaning,
                    scope="enkeltledd",
                    information_type="bevilgning",
                    classification_evidence=(
                        "Kapittelregel R-101/2024 side 2–3: utgift; eksplisitt vedtaksobjekt"
                    ),
                    organization=lookup(chapter, 2024),
                    documents=(reference,),
                    structure_status="strukturert",
                )
            )
    by_id = {o.id: o for o in expected}
    for actual in (extraction.observations, prepared.adopted):
        if (
            len(actual) != 6
            or len({o.id for o in actual}) != 6
            or {o.id: o for o in actual} != by_id
        ):
            raise ValueError("T1s overførte vedtaksfelt avviker fra original/tolkning/identitet")
