"""Et avgrenset originalbudsjettmønster. Ustøttet innhold bevares til kontroll."""

import hashlib
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from lxml import etree, html

from .model import Allocation, Decision, Report
from .storage import save_report

NS = "{http://data.stortinget.no}"
START_SESSION = "2026-2027"
MAX_BYTES = 32 * 1024 * 1024


def session_url(session: str) -> str:
    if not re.fullmatch(r"20\d{2}-20\d{2}", session):
        raise ValueError("Sesjon må ha format ÅÅÅÅ-ÅÅÅÅ")
    first, last = map(int, session.split("-"))
    if last != first + 1:
        raise ValueError("Sesjon må bestå av to påfølgende år")
    return f"https://data.stortinget.no/eksport/stortingsvedtak?sesjonid={session}"


def text(element: etree._Element) -> str:
    return " ".join(" ".join(element.itertext()).split())


def field(element: etree._Element, name: str) -> str:
    value = element.findtext(NS + name)
    if value is None or not value.strip():
        raise ValueError(f"Manglende XML-felt: {name}")
    return value


def amount(raw: str) -> int | None:
    if not re.fullmatch(r"-?(?:0|[1-9]\d*|[1-9]\d{0,2}(?: \d{3})+)", raw):
        return None
    value = int(raw.replace(" ", ""))
    return value if abs(value) <= 9_007_199_254_740_991 else None


def extract(report: Report) -> None:
    decision = report.decision
    assert decision is not None
    document = html.fromstring(decision.html, parser=html.HTMLParser(no_network=True))
    years = re.findall(r"På statsbudsjettet for (20\d{2}) bevilges under:", text(document))
    tables = document.findall(".//table")
    if len(years) != 1 or len(tables) != 1:
        raise ValueError("Ustøttet mønster: krever ett uttrykkelig budsjettår og én tabell")
    decision.budget_year = int(years[0])
    outside = deepcopy(document)
    for table in outside.findall(".//table"):
        table.clear(keep_tail=True)
    if text(outside) != f"På statsbudsjettet for {decision.budget_year} bevilges under:":
        report.controls.append("Uklassifisert innhold utenfor tabellen")
    rows = tables[0].findall(".//tr")
    if (
        not rows
        or [text(cell) for cell in rows[0]] != ["Kap.", "Post", "Formål", "Kroner", "Kroner"]
        or any(cell.get("colspan", "1") != "1" or cell.get("rowspan") for cell in rows[0])
    ):
        raise ValueError("Ukjent tabellhode eller beløpsenhet; krever kroner")
    if text(tables[0]) != " ".join(text(row) for row in rows):
        report.controls.append("Uklassifisert innhold i tabellen utenfor kilderadene")
    chapter, chapter_name, section = "", "", ""
    for row_number, row in enumerate(rows[1:], start=2):
        locator = f"table[1]/tr[{row_number}]"
        cells = list(row)
        values = [text(cell) for cell in cells]
        if (
            len(cells) == 1
            and cells[0].get("colspan") == "5"
            and values[0] in ("Utgifter", "Inntekter")
        ):
            section = "utgift" if values[0] == "Utgifter" else "inntekt"
            chapter, chapter_name = "", ""
            continue
        if len(values) != 5 or any(
            cell.get("rowspan") or cell.get("colspan", "1") != "1" for cell in cells
        ):
            report.controls.append(f"{locator}: ukjent celleoppsett")
            continue
        cap, post, purpose, raw_amount, total = values
        if cap.isdigit() and not post and purpose and not raw_amount and not total:
            chapter, chapter_name = cap, purpose
        elif not cap and post.isdigit() and purpose:
            direction = (
                "utgift"
                if chapter.isdigit() and 1 <= int(chapter) <= 2999
                else "inntekt"
                if chapter.isdigit() and 3000 <= int(chapter) <= 5999
                else "uavklart"
            )
            value = amount(raw_amount) if not total else None
            reason = ""
            if value is None:
                reason = "Manglende eller tvetydig postbeløp"
            if direction != section or not chapter or not 1 <= int(post) <= 99:
                reason = "Uavklart kapittel, post eller inntekts-/utgiftsdel"
            line = Allocation(
                locator,
                chapter,
                chapter_name,
                post,
                purpose,
                raw_amount,
                value,
                direction,
                etree.tostring(row, encoding="unicode", method="html"),
                status="til kontroll" if reason else "strukturert",
                control_reason=reason,
            )
            report.lines.append(line)
            if reason:
                report.controls.append(f"{locator}: {reason}")
        elif (
            not cap
            and not post
            and purpose in ("Totale utgifter", "Totale inntekter")
            and not raw_amount
        ):
            direction = "utgift" if purpose == "Totale utgifter" else "inntekt"
            if direction in report.source_totals:
                report.controls.append(f"{locator}: gjentatt kilde-total")
            report.source_totals[direction] = amount(total)
        else:
            report.controls.append(f"{locator}: uklassifisert kilderad: {' | '.join(values)}")
    if not report.lines:
        report.controls.append("Ingen sikre postrader i valgt vedtak")
    for direction in ("utgift", "inntekt"):
        subtotal = sum(
            line.amount_kr
            for line in report.lines
            if line.direction == direction and line.amount_kr is not None
        )
        if (
            report.source_totals.get(direction) is None
            or subtotal != report.source_totals[direction]
        ):
            report.controls.append(f"{direction}: manglende eller avvikende kilde-total")


def import_saved(
    database: Path,
    raw_response: bytes,
    metadata: dict[str, object],
    decision_id: str,
    *,
    historical_sample: bool = False,
) -> str:
    """Valider proveniens, bevar faktisk input, og strukturer ett valgt vedtak."""
    if len(raw_response) > MAX_BYTES:
        raise ValueError("Kilderespons overskrider 32 MiB")
    digest = hashlib.sha256(raw_response).hexdigest()
    if metadata.get("sha256") != digest or metadata.get("bytes") != len(raw_response):
        raise ValueError("Råbyte stemmer ikke med metadataenes SHA-256 og byteantall")
    retrieved = datetime.fromisoformat(str(metadata.get("retrieved_utc", "")))
    if retrieved.tzinfo is None or metadata.get("status") != 200:
        raise ValueError("Krever hentetid med tidssone og vellykket HTTP-status")
    report = Report(str(uuid4()), digest, dict(metadata), historical_sample)
    try:
        root = etree.fromstring(
            raw_response,
            parser=etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False),
        )
        if root.getroottree().docinfo.doctype:
            raise ValueError("DOCTYPE er ikke tillatt i kildedata")
        if root.tag != NS + "stortingsvedtak_oversikt":
            raise ValueError("Ukjent XML-rot eller navnerom")
        session = field(root, "sesjon_id")
        if metadata.get("url") != session_url(session):
            raise ValueError("Kilde-URL stemmer ikke med XML-sesjonen")
        if session < START_SESSION and not historical_sample:
            raise ValueError("Eldre sesjon krever eksplisitt historisk prøve")
        matches = [
            node
            for node in root.findall(f"{NS}stortingsvedtak_liste/{NS}stortingsvedtak")
            if node.findtext(NS + "id") == decision_id
        ]
        if len(matches) != 1:
            raise ValueError("Valgt vedtaks-ID mangler eller forekommer flere ganger")
        node = matches[0]
        source_date = field(node, "stortingsvedtak_dato_tid")
        date = datetime.fromisoformat(source_date).date().isoformat()
        raw_url = field(node, "stortingsvedtak_lenke_url")
        report.decision = Decision(
            decision_id,
            field(node, "stortingsvedtak_nummer"),
            session,
            date,
            source_date,
            field(node, "sak_id"),
            field(node, "stortingsvedtak_type/" + NS + "id"),
            field(node, "stortingsvedtak_tittel"),
            "https:" + raw_url if raw_url.startswith("//") else raw_url,
            raw_url,
            field(node, "stortingsvedtak_tekst"),
        )
    except (ValueError, etree.XMLSyntaxError) as error:
        report.status = "innlesningsfeil"
        report.controls.append(str(error))
    if report.decision is not None:
        try:
            extract(report)
        except (ValueError, etree.ParserError) as error:
            report.controls.append(str(error))
        if report.controls:
            report.status = "til kontroll"
    save_report(database, raw_response, report)
    return report.run_id
