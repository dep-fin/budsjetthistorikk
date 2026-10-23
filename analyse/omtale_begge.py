"""Eksplisitt O2b-algoritme; A-rekonstruksjon og gamle identiteter består."""

from collections.abc import Sequence
from dataclasses import replace

from lxml import etree, html

from innlesning.omtale import (
    OmtaleBasis,
    Section,
    compact,
    identified,
    is_o2b,
    source_bytes,
    validate_basis,
)

from .omtale import (
    _chain_issues,
    _rows_bound_to_extraction,
)
from .omtale_model import FORMAT, OmtaleReport, Relation
from .saksdokumenter import SaksReport
from .saksdokumenter import report_from_json as read_base
from .saksdokumenter import report_to_json as base_json


def post22_groups(rows: Sequence[etree._Element]) -> list[int]:
    """Returindeks er raden foran deltaet, som i A sin lokatorregel."""
    matches: list[int] = []
    chapter: list[str] = []
    chapter_index = -1
    for n, row in enumerate(rows[:-1]):
        cells = [compact("".join(c.itertext())) for c in row.findall("td")]
        if len(cells) != 4:
            chapter, chapter_index = [], -1
            continue
        if cells[0]:
            chapter, chapter_index = cells, n
        levels = [compact("".join(c.itertext())) for c in rows[n + 1].findall("td")]
        if (
            chapter_index == n - 3
            and len(chapter) == 4
            and chapter[0] == "1429"
            and chapter[1] == chapter[3] == ""
            and bool(chapter[2])
            and cells
            == [
                "",
                "22",
                "Flerårige prosjekter kulturminneforvaltning, kan overføres, reduseres med",
                "3 000 000",
            ]
            and levels == ["", "", "fra kr 32 185 000 til kr 29 185 000", ""]
        ):
            matches.append(n - 1)
    return matches


def _table_proves_post22(section: Section, basis: OmtaleBasis) -> bool:
    if section.key == "PT22":
        source = next(s for s in basis.sources if s.id == section.source_id)
        raw = source_bytes(source)
        assert raw is not None
        doc = html.fromstring(raw.decode("utf-8"), parser=html.HTMLParser(no_network=True))
        nodes = doc.xpath(section.locator)
        if len(nodes) != 1:
            return False
        node = nodes[0]
        parents = node.xpath("ancestor::table[1]")
        if len(parents) != 1:
            return False
        rows = parents[0].findall(".//tr")
        return [rows[n + 1] for n in post22_groups(rows)] == [node]
    doc = html.fromstring(section.html)
    matches = [n for t in doc.findall(".//table") for n in post22_groups(t.findall(".//tr"))]
    return len(matches) == 1


def _post22_issues(basis: OmtaleBasis) -> list[str]:
    sections = {s.key: s for s in basis.sections}
    issues = ["belegg_mangler:" + key for key in ("P22", "K22", "PT22") if key not in sections]
    for key in ("PT22", "KT", "V"):
        if key in sections and not _table_proves_post22(sections[key], basis):
            issues.append("konto_eller_forslagsbelop_motstrid_post22:" + key)
    for key in ("P22", "K22"):
        section = sections.get(key)
        if section is None:
            continue
        headings = [compact(h.text) for h in section.hierarchy]
        content = compact(section.text)
        if not any(h.startswith("Kap. 1429 ") for h in headings) or not any(
            h.startswith("Post 22 Flerårige prosjekter kulturmiljøforvaltning") for h in headings
        ):
            issues.append("konto_hierarki_motstrid:" + key)
        # De to originalene har litt ulik ordlyd. Ingen generell konto-/beløpsjoin.
        expected = (
            "Bevilgningen på posten foreslås redusert med 3 mill. kroner som foreslås "
            "omdisponert til kap. 1429, post 01."
            if key == "P22"
            else "Bevilgningen på posten foreslås redusert med 3 mill. kroner som foreslås "
            "omdisponert til kap. 1429 post 1."
        )
        if expected not in content:
            issues.append("forklaring_omfang_motstrid:" + key)
    p1 = sections.get("P1")
    if p1 and (
        "Som en følge av dette foreslås det å omdisponere 3 mill. kroner fra kap. 1429, post 22."
    ) not in compact(p1.text):
        issues.append("omdisponeringsbelegg_motstrid:P1")
    return issues


def build_both_report(
    base: SaksReport, basis: OmtaleBasis, *, proposals: tuple[Relation, ...] = ()
) -> OmtaleReport:
    if not is_o2b(basis.extractor):
        raise ValueError("Begge poster krever eksplisitt O2b-uttrekksversjon")
    validate_basis(basis)
    chain_issues = (*_chain_issues(base, basis), *_post22_issues(basis))
    issues = [*basis.issues, *chain_issues]
    sections = {s.key: s for s in basis.sections}
    relations: list[Relation] = []
    values_by_post = {
        "1": {"endring": 5_796_000, "for_belop": 160_243_000, "etter_belop": 166_039_000},
        "22": {"endring": -3_000_000, "for_belop": 32_185_000, "etter_belop": 29_185_000},
    }
    for post, expected in values_by_post.items():
        rows = [
            r
            for r in base.base.unfiltered_rows
            if (
                r.observation.api_id,
                r.observation.chapter,
                r.observation.post,
                r.observation.budget_year,
            )
            == ("40034048", "1429", post, 2024)
        ]
        if (
            len(rows) != 3
            or {r.observation.meaning: r.observation.amount_kr for r in rows} != expected
            or len({r.observation.step_id for r in rows}) != 1
            or rows[0].observation.step_id is None
            or len({r.observation.source_revision_id for r in rows}) != 1
            or not _rows_bound_to_extraction(base, basis, rows, post)
        ):
            issues.append("210_post" + post + "_grunnlag_mangler_eller_motstrid")
            continue
        keys = (
            ("P1", "PT", "K1", "KS", "KT", "V")
            if post == "1"
            else ("P1", "P22", "PT22", "K22", "KS", "KT", "V")
        )
        evidence = tuple(s.id for s in basis.sections if s.key in keys)
        evidence += tuple(s.id for s in basis.sources if s.media_type == "application/xml")
        valid = not chain_issues and all(s.status == "kildeverifisert" for s in basis.sources)
        for key in keys:
            section = sections.get(key)
            if section is None:
                continue
            reason = (
                "P1 → PT → K1 + KS + KT → V → 210/1429/1. Omdisponering og avrundet "
                "lønnsforklaring; ingen eksakt lønnskomponent."
                if post == "1"
                else "P1 (bare omdisponeringsutsagnet) + P22 → PT22 → K22 + KS + KT → V → "
                "210/1429/22. Reduksjon finansierer post 1; lønnsforklaringen gjelder bare post 1."
            )
            relations.append(
                identified(
                    "omtale-relasjon-1",
                    Relation(
                        "",
                        section.id,
                        rows[0].observation.step_id,
                        rows[0].observation.source_revision_id,
                        tuple(r.observation.id for r in rows),
                        ("1429/" + post,),
                        section.role,
                        section.actor,
                        evidence,
                        "kildeverifisert" if valid else "uavklart",
                        "ikke_faglig_godkjent",
                        reason
                        if valid
                        else reason + " Belegg/rolle/kilde er uavklart; se globale Omtaleavvik.",
                    ),
                )
            )
    for proposal in proposals:
        _validate_proposal(proposal, basis, relations)
        if proposal.id in {r.id for r in relations}:
            raise ValueError("Duplisert relasjonsforslag")
        relations.append(proposal)
        issues.append("uavklart_relasjonsforslag:" + proposal.id + ":" + proposal.reason)
    # Bare eksplisitte relasjoner til faktisk viste observasjoner velger omtalen.
    selected = {r.observation.id for r in base.base.rows}
    visible = {r.section_id for r in relations if selected.intersection(r.observation_ids)}
    if sections.get("P1") and sections["P1"].id in visible:
        visible.update(s.id for s in basis.sections if s.key == "P1_PDF")
    return identified(
        FORMAT,
        OmtaleReport(
            "",
            base_json(base),
            basis,
            tuple(relations),
            tuple(s.id for s in basis.sections if s.id in visible),
            tuple(dict.fromkeys(issues)),
        ),
    )


def _validate_proposal(proposal: Relation, basis: OmtaleBasis, relations: list[Relation]) -> None:
    known = {s.id for s in basis.sources} | {s.id for s in basis.sections}
    targets = {
        (r.event_id, r.decision_revision_id, r.observation_ids, r.accounts)
        for r in relations
        if r.role != "uavklart_relasjonsforslag"
    }
    if (
        proposal.id != identified("omtale-relasjon-1", proposal).id
        or proposal.section_id not in {s.id for s in basis.sections if s.key != "PN"}
        or proposal.role != "uavklart_relasjonsforslag"
        or proposal.actor != "forslagsstiller_ukjent"
        or proposal.status != "uavklart"
        or proposal.professional_status != "ikke_faglig_godkjent"
        or not proposal.reason.strip()
        or len(proposal.reason) > 100_000
        or not proposal.evidence_ids
        or len(set(proposal.evidence_ids)) != len(proposal.evidence_ids)
        or not set(proposal.evidence_ids) <= known
        or (
            proposal.event_id,
            proposal.decision_revision_id,
            proposal.observation_ids,
            proposal.accounts,
        )
        not in targets
    ):
        raise ValueError("Ugyldig uavklart relasjonsforslag")


def propose_relation(
    report: OmtaleReport,
    *,
    section_id: str,
    event_id: str,
    evidence_ids: tuple[str, ...],
    reason: str,
) -> OmtaleReport:
    """Bevar et uttrykkelig forslag separat; det er aldri dokumentert kildekobling."""
    base = read_base(report.base_json)
    canonical = build_both_report(
        base,
        report.basis,
        proposals=tuple(r for r in report.relations if r.role == "uavklart_relasjonsforslag"),
    )
    if report != canonical:
        raise ValueError("Forslag krever et gyldig O2b-grunnlag")
    target = next(
        (
            r
            for r in report.relations
            if r.event_id == event_id and r.role != "uavklart_relasjonsforslag"
        ),
        None,
    )
    if target is None:
        raise ValueError("Ukjent uttrykkelig hendelse")
    proposal = identified(
        "omtale-relasjon-1",
        replace(
            target,
            id="",
            section_id=section_id,
            role="uavklart_relasjonsforslag",
            actor="forslagsstiller_ukjent",
            evidence_ids=evidence_ids,
            status="uavklart",
            reason=reason,
        ),
    )
    return build_both_report(
        base,
        report.basis,
        proposals=tuple(r for r in report.relations if r.role == "uavklart_relasjonsforslag")
        + (proposal,),
    )
