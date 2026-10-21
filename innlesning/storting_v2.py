"""Eksplisitt B4-tolkning. Ingen endring av B1/B2 eller storting-belop-v1."""

import re
from dataclasses import replace
from pathlib import Path

from lxml import etree, html

from .ingestion import amount, text
from .observations import (
    AmountObservation,
    Anomaly,
    Artifact,
    DocumentReference,
    Extraction,
    Interpretation,
    SourcePointer,
    component_anomalies,
    encode,
    identity,
    read_extraction,
    save_extraction,
    validate_component_relations,
)
from .organization_register import REGISTER_SNAPSHOT, classify_chapter, lookup
from .storage import read_source
from .sync import read_revision


def numbering_anomalies(observations: tuple[AmountObservation, ...]) -> tuple[Anomaly, ...]:
    """Nummereringskontroll for Storting-v2s dokumenterte post-24-mønster."""
    by_id = {o.id: o for o in observations}
    groups = validate_component_relations(observations)
    issues: list[Anomaly] = []
    for parent_id, children in groups.items():
        parent = by_id[parent_id]
        codes = [child.subpost for child in children]
        code = None
        if None in codes:
            code = "ukjent_komponent"
        elif len(set(codes)) != len(codes):
            code = "duplisert_komponent"
        elif sorted(int(c) for c in codes if c is not None and c != "0") != list(
            range(1, len([c for c in codes if c != "0"]) + 1)
        ):
            code = "manglende_komponent"
        if code:
            issues.append(
                Anomaly(
                    code,
                    "Nummereringen er ikke entydig og sammenhengende",
                    evidence=parent.id,
                    chapter=parent.chapter,
                    post=parent.post,
                    budget_year=parent.budget_year,
                )
            )
    return tuple(issues)


def extract_v2(database: Path, revision_id: str, interpretation: Interpretation) -> Extraction:
    register = None
    if interpretation.register_snapshot != REGISTER_SNAPSHOT:
        from .registers import read_register

        register = read_register(database, interpretation.register_snapshot)
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
    raw = read_source(database, report.source_sha256)
    artifact = Artifact(
        report.source_sha256,
        f"stortingsvedtak-{decision.session}.xml",
        str(report.source_metadata.get("fixture_kind", "http_original")),
        "text/xml",
        len(raw),
        encode(report.source_metadata),
    )
    parser = html.HTMLParser(no_network=True, recover=False)
    errors: list[str] = []
    try:
        document = html.fromstring(decision.html, parser=parser)
    except etree.LxmlError as error:
        document = None
        errors.append(str(error))
    errors.extend(str(e) for e in parser.error_log if e.level_name in {"ERROR", "FATAL"})
    if errors:
        document = None
    all_text = text(document) if document is not None else ""
    years = set(re.findall(r"statsbudsjettet for (20\d{2})", all_text, re.I))
    year_evidence = "Uttrykkelig budsjettår i vedtaksteksten"
    if not years:
        years = set(re.findall(r"statsbudsjettet (20\d{2})", decision.title, re.I))
        year_evidence = "Uttrykkelig budsjettår i vedtakstittelen: " + decision.title
    year = int(next(iter(years))) if len(years) == 1 else None
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
    observations: list[AmountObservation] = []
    anomalies: list[Anomaly] = []
    if errors:
        anomalies.append(
            Anomaly(
                "ugyldig_html",
                "Ingen delresultater etter HTML-feil",
                evidence="\n".join(errors),
                budget_year=year,
            )
        )
    chapter, chapter_name = "", ""

    def issue(code: str, reason: str, locator: str, post: str | None = None) -> None:
        anomalies.append(
            Anomaly(
                code,
                reason,
                evidence=locator,
                chapter=str(int(chapter)) if chapter else None,
                post=post,
                budget_year=year,
            )
        )

    def observe(
        locator: str,
        field: str,
        raw_amount: str,
        meaning: str,
        step: str,
        post: str,
        purpose: str,
        raw_row: str,
        *,
        sign: int = 1,
        subpost_raw: str | None = None,
        detail: str = "post",
        reasons: tuple[Anomaly, ...] = (),
    ) -> AmountObservation:
        value = amount(raw_amount)
        if value is None:
            reasons += (
                Anomaly("ugyldig_belop", "Ikke entydige hele kroner", (field,), raw_amount),
            )
        if year is None:
            reasons += (Anomaly("uavklart_ar", "Krever ett uttrykkelig budsjettår"),)
        normalized_chapter = str(int(chapter)) if chapter else None
        side = classify_chapter(normalized_chapter)
        if side in {"uavklart", "kapitalregnskap"} or not post or not 1 <= int(post) <= 99:
            reasons += (
                Anomaly(
                    "utenfor_bevilgningskonti" if side == "kapitalregnskap" else "uavklart_konto",
                    "Kapittel 1–5999 og post 1–99 kreves for bevilgning",
                ),
            )
        organization = (
            register.lookup(normalized_chapter, year)
            if register is not None
            else lookup(normalized_chapter, year)
        )
        if organization.fdep_nr is None:
            issue("mangler_organisasjonsoppslag", organization.null_reason, locator, post)
        item = AmountObservation(
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
            chapter=normalized_chapter,
            post=str(int(post)) if post else None,
            subpost_raw=subpost_raw,
            subpost=(
                str(int(subpost_raw))
                if subpost_raw is not None and subpost_raw.isascii() and subpost_raw.isdigit()
                else None
            ),
            chapter_name=chapter_name or None,
            purpose=purpose or None,
            detail_level=detail,
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
            normalization_evidence="Kroner i tabellhodet; beløpscelle og eventuelle retningsord",
            figure_type="stortingsvedtak",
            round=round_,
            round_evidence=round_evidence,
            stage_raw=decision.title,
            meaning=meaning,
            scope="enkeltledd",
            information_type="kapitalregnskap" if side == "kapitalregnskap" else "bevilgning",
            classification_evidence=(
                f"Kapittelregel R-101/2024 side 2–3: {side}; eksplisitt vedtaksobjekt"
            ),
            organization=organization,
            documents=(reference,),
            structure_status="til_kontroll" if reasons else "strukturert",
            anomalies=reasons,
        )
        observations.append(item)
        return item

    tables = document.findall(".//table") if document is not None else []
    if len(tables) > 1:
        issue("flere_tabeller", "Flere tabeller krever særskilt tolkning", "")
        tables = []
    for table_number, table in enumerate(tables, 1):
        rows = table.findall(".//tr")
        headers = [text(cell) for cell in rows[0]] if rows else []
        if (
            not rows
            or any(
                cell.tag not in {"td", "th"}
                or cell.get("rowspan", "1") != "1"
                or cell.get("colspan", "1") != "1"
                for cell in rows[0]
            )
            or headers
            not in (
                ["Kap.", "Post", "Formål", "Kroner"],
                ["Kap.", "Post", "Formål", "Kroner", "Kroner"],
                ["Kap.", "Post", "Formål", "", "Kroner"],
                ["Kap.", "Post", "Formål", "", "Kroner", "Kroner"],
            )
        ):
            issue("ukjent_tabell", "Ukjent tabellhode/enhet", f"table[{table_number}]")
            continue
        chapter, chapter_name = "", ""
        last: tuple[str, str, str] | None = None
        block: tuple[str, str, str] | None = None
        child_indices: list[int] = []

        def finish(parent: AmountObservation | None = None) -> None:
            nonlocal block, child_indices
            if block:
                if parent is None:
                    issue(
                        "mangler_posttotal",
                        "Komponentblokk uten fysisk observert posttotal",
                        block[0],
                        block[1],
                    )
                else:
                    parent_id = parent.id
                    for index in child_indices:
                        observations[index] = replace(
                            observations[index],
                            component_of=parent_id,
                            relations=(("komponent_av", parent_id, block[0]),),
                        )
                    if not child_indices:
                        issue(
                            "manglende_komponent",
                            "Posttotal uten komponenter i spesifikasjonen",
                            block[0],
                            block[1],
                        )
            block, child_indices = None, []

        for number, row in enumerate(rows[1:], 2):
            values = [text(cell) for cell in row]
            locator = f"table[{table_number}]/tr[{number}]"
            raw_row = etree.tostring(row, encoding="unicode", method="html")
            if len(values) == 1 and values[0] in {"Utgifter", "Inntekter"}:
                finish()
                chapter, chapter_name, last = "", "", None
                continue
            if len(values) != len(headers) or any(
                cell.get("rowspan") or cell.get("colspan", "1") != "1" for cell in row
            ):
                finish()
                chapter, chapter_name, last = "", "", None
                issue("ukjent_rad", "Ukjent celleoppsett; kontokontekst opphevet", locator)
                continue
            cap, post, purpose, *amount_cells = values
            populated = [(index, value) for index, value in enumerate(amount_cells, 4) if value]
            if cap.isascii() and cap.isdigit() and not post and purpose and not populated:
                finish()
                chapter, chapter_name, last = cap, purpose, None
                continue
            if cap:
                finish()
                chapter, chapter_name, last = "", "", None
                issue("uavklart_konto", "Uavklart kapittelrad", locator)
                continue
            if post.isascii() and post.isdigit() and purpose:
                finish()
                step = identity(unit_id, revision_id, locator)
                if post == "24" and not populated:
                    block = (locator, post, purpose)
                    last = (step, post, purpose)
                    continue
                increase = bool(re.search(r"(?:økes|auka|aukes)\s+med", purpose))
                decrease = bool(
                    re.search(r"(?:reduseres|redusert|reduserast|minka)\s+med", purpose)
                )
                new = bool(re.search(r"bevilges\s+med", purpose))
                reasons: tuple[Anomaly, ...] = ()
                if original and not (increase or decrease or new):
                    meaning, sign = "nivaa", 1
                elif increase + decrease + new == 1:
                    meaning, sign = "endring", -1 if decrease else 1
                else:
                    meaning, sign = "uavklart", 1
                    reasons = (
                        Anomaly(
                            "ukjent_ledd", "Ingen entydig nivå-/endringstolkning", evidence=purpose
                        ),
                    )
                if len(populated) != 1:
                    reasons += (
                        Anomaly(
                            "tvetydig_belopsfelt", "Krever nøyaktig ett postbeløp", evidence=locator
                        ),
                    )
                for column, raw_amount in populated or [(4, "")]:
                    local = reasons
                    if meaning == "endring" and (amount(raw_amount) or 0) < 0:
                        local += (Anomaly("motstrid_fortegn", "Retningsord med negativt råbeløp"),)
                    observe(
                        f"{locator}/td[{column}]",
                        meaning,
                        raw_amount,
                        meaning,
                        step,
                        post,
                        purpose,
                        raw_row,
                        sign=sign,
                        reasons=local,
                    )
                last = (step, post, purpose)
                continue
            if block and last and not post:
                step, block_post, block_purpose = last
                code = re.fullmatch(r"([0-9]+)\.?\s+(\S.*)", purpose, re.S)
                meaning = "nivaa" if original else "etter_belop"
                if code and populated:
                    column, raw_amount = populated[0]
                    observe(
                        f"{locator}/td[{column}]",
                        meaning,
                        raw_amount,
                        meaning,
                        step,
                        block_post,
                        purpose,
                        raw_row,
                        subpost_raw=code[1],
                        detail="underpost",
                    )
                    child_indices.append(len(observations) - 1)
                    if len(populated) == 2 and populated[0][0] == 4 and populated[1][0] == 5:
                        column, raw_amount = populated[1]
                        parent = observe(
                            f"{locator}/td[{column}]",
                            meaning,
                            raw_amount,
                            meaning,
                            step,
                            block_post,
                            block_purpose,
                            raw_row,
                        )
                        finish(parent)
                        last = None
                    elif len(populated) > 1:
                        issue(
                            "tvetydig_belopsfelt",
                            "Ukjent komponent-/totalplassering",
                            locator,
                            block_post,
                        )
                    continue
                if purpose in {"", "Sum:", "Sum"} and len(populated) == 1:
                    column, raw_amount = populated[0]
                    parent = observe(
                        f"{locator}/td[{column}]",
                        meaning,
                        raw_amount,
                        meaning,
                        step,
                        block_post,
                        block_purpose,
                        raw_row,
                    )
                    finish(parent)
                    last = None
                    continue
                issue(
                    "ukjent_komponent",
                    "Ukjent rad i nummerert post-24-spesifikasjon",
                    locator,
                    block_post,
                )
                for column, raw_amount in populated:
                    observe(
                        f"{locator}/td[{column}]",
                        meaning,
                        raw_amount,
                        meaning,
                        step,
                        block_post,
                        purpose,
                        raw_row,
                        subpost_raw=purpose.split(maxsplit=1)[0] if purpose else None,
                        detail="underpost",
                        reasons=(
                            Anomaly("ukjent_komponent", "Komponentkode mangler eller er uavklart"),
                        ),
                    )
                    child_indices.append(len(observations) - 1)
                continue
            if not post and last:
                match = re.fullmatch(r"(?:fra|frå) kr (.*?) til kr (.*)", purpose)
                if match and not populated:
                    step, last_post, last_purpose = last
                    for field, raw_amount in zip(
                        ("for_belop", "etter_belop"), match.groups(), strict=True
                    ):
                        observe(
                            f"{locator}/td[3]",
                            field,
                            raw_amount,
                            field,
                            step,
                            last_post,
                            last_purpose,
                            raw_row,
                        )
                    last = None
                    continue
            if purpose in {"Utgifter", "Inntekter", "Totale utgifter", "Totale inntekter"}:
                last = None
                continue
            issue("uklassifisert_rad", "Kilderad er ikke sikker bevilgningsobservasjon", locator)
            last = None
        finish()
    if not tables:
        anomalies.append(
            Anomaly(
                "mangler_bevilgningstabell" if years else "ingen_bevilgningstabell",
                "Fulltekst bevart i B2; ingen bevilgningslinjer tolket",
                budget_year=year,
            )
        )
    anomalies.extend(component_anomalies(tuple(observations)))
    anomalies.extend(numbering_anomalies(tuple(observations)))
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
