"""Avgrenset OOXML-inventar. Ingen Excel-evaluering eller float-konvertering."""

import posixpath
import re
from bisect import bisect_right
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, localcontext
from io import BytesIO
from typing import Any
from zipfile import BadZipFile, ZipFile

from lxml import etree

from .observations import identity

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CELL = re.compile(r"([A-Z]{1,3})([1-9][0-9]{0,6})\Z")
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE]([+-]?[0-9]+))?\Z")


@dataclass(frozen=True)
class Limits:
    max_bytes: int = 32 * 1024 * 1024
    members: int = 128
    member_bytes: int = 32 * 1024 * 1024
    inflated_bytes: int = 128 * 1024 * 1024
    xml_nodes: int = 1_000_000
    text_chars: int = 1_000_000
    cells: int = 250_000
    positions: int = 300_000
    number_chars: int = 128
    exponent: int = 100
    resolved_chars: int = 16 * 1024 * 1024
    serialized_chars: int = 256 * 1024 * 1024

    def __post_init__(self) -> None:
        ceilings = (
            32 * 1024 * 1024,
            128,
            32 * 1024 * 1024,
            128 * 1024 * 1024,
            1_000_000,
            1_000_000,
            250_000,
            300_000,
            128,
            100,
            16 * 1024 * 1024,
            256 * 1024 * 1024,
        )
        if any(
            type(value) is not int or not 0 < value <= cap
            for value, cap in zip(asdict(self).values(), ceilings, strict=True)
        ):
            raise ValueError("Ressursgrenser må være positive og høyst adapterens faste maksimum")


DEFAULT_LIMITS = Limits()


class MaterializationBudget:
    """Conservative JSON-size bound, checked without allocating serialized copies."""

    def __init__(self, maximum: int) -> None:
        self.remaining = maximum

    def charge(self, value: Any) -> None:
        if isinstance(value, str):
            size = 2 + len(value) + value.count('"') + value.count("\\")
            size += sum(value.count(chr(code)) * 5 for code in range(32))
        elif isinstance(value, dict):
            self.charge(tuple(value.keys()))
            self.charge(tuple(value.values()))
            size = 2 + len(value)
        elif isinstance(value, tuple | list):
            for item in value:
                self.charge(item)
            size = 2 + len(value)
        else:
            size = 32
        if size > self.remaining:
            raise ValueError("Samlet serialisert/materialisert innhold overskrider grensen")
        self.remaining -= size


@dataclass(frozen=True)
class Inventory:
    cells: tuple[dict[str, Any], ...]
    metadata: dict[str, Any]


def column_number(label: str) -> int:
    number = 0
    for letter in label:
        number = number * 26 + ord(letter) - 64
    return number


def column_label(number: int) -> str:
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def address(value: str) -> tuple[int, int]:
    match = CELL.fullmatch(value)
    if match is None:
        raise ValueError("Ugyldig celleadresse")
    column, row = column_number(match[1]), int(match[2])
    if column > 16384 or row > 1048576:
        raise ValueError("Celleadresse utenfor Excel-grensen")
    return column, row


def decimal_value(value: str | None, limits: Limits = DEFAULT_LIMITS) -> Decimal | None:
    if value is None or len(value) > limits.number_chars:
        return None
    match = NUMBER.fullmatch(value)
    if match is None or (match[1] is not None and abs(int(match[1])) > limits.exponent):
        return None
    try:
        result = Decimal(value)
    except InvalidOperation:
        return None
    return result if result.is_finite() else None


def multiply(value: Decimal, factor: str) -> Decimal:
    with localcontext() as context:
        context.prec = 256
        return value * Decimal(factor)


def safe_xml(raw: bytes, limits: Limits) -> etree._Element:
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("DOCTYPE/ENTITY er ikke tillatt")
    parser = etree.XMLPullParser(
        events=("start", "end"), resolve_entities=False, no_network=True, load_dtd=False
    )
    count = 0
    try:
        for start in range(0, len(raw), 8192):
            parser.feed(raw[start : start + 8192])
            for event, element in parser.read_events():
                if event == "start":
                    count += 1
                    if count > limits.xml_nodes:
                        raise ValueError("XML-nodegrense overskredet")
                    if any(len(v) > limits.text_chars for v in element.attrib.values()):
                        raise ValueError("XML-attributtgrense overskredet")
                elif (
                    len(element.text or "") > limits.text_chars
                    or len(element.tail or "") > limits.text_chars
                ):
                    raise ValueError("XML-tekstgrense overskredet")
        root = parser.close()
    except etree.XMLSyntaxError as error:
        raise ValueError("Ugyldig OOXML") from error
    if root.getroottree().docinfo.doctype:
        raise ValueError("DOCTYPE er ikke tillatt")
    return root


def _target(member: str, target: str) -> str:
    if "\\" in target or ":" in target or "?" in target or "#" in target or "%" in target:
        raise ValueError("Usikkert relasjonsmål")
    result = posixpath.normpath(
        target.lstrip("/")
        if target.startswith("/")
        else posixpath.join(posixpath.dirname(member), target)
    )
    if result.startswith("../") or result in {".", ".."}:
        raise ValueError("Relasjonsmål utenfor pakken")
    return result


def _mark_formula_regions(
    found: dict[str, dict[str, Any]], remaining: int, budget: MaterializationBudget
) -> int:
    # Index bounded column intervals, never expand the referenced cell rectangle.
    columns: dict[int, list[tuple[int, int, dict[str, str]]]] = {}
    positions = 0
    for cell in found.values():
        attributes = cell["formula_attributes"]
        if attributes is None:
            continue
        kind = attributes.get("t", "normal")
        ref = attributes.get("ref")
        if kind not in {"normal", "array", "shared", "dataTable"} or (
            kind in {"array", "dataTable"} and ref is None
        ):
            raise ValueError("Ustøttet formelområde/type")
        if ref is None:
            continue
        if kind == "normal":
            raise ValueError("Ustøttet formelområde/type")
        bounds = ref.split(":")
        if len(bounds) > 2:
            raise ValueError("Ugyldig formelområde")
        first, last = address(bounds[0]), address(bounds[-1])
        anchor = address(cell["cell"])
        if not (first[0] <= anchor[0] <= last[0] and first[1] <= anchor[1] <= last[1]):
            raise ValueError("Omvendt formelområde eller anker utenfor området")
        positions += (last[0] - first[0] + 1) * (last[1] - first[1] + 1)
        if positions > remaining:
            raise ValueError("Samlet formelområde overskrider posisjonsgrensen")
        region = {"anchor": cell["cell"], "ref": ref, "type": kind}
        for column in range(first[0], last[0] + 1):
            budget.charge((first[1], last[1], region))
            columns.setdefault(column, []).append((first[1], last[1], region))
    starts: dict[int, list[int]] = {}
    for column, intervals in columns.items():
        intervals.sort(key=lambda interval: interval[0])
        for previous, current in zip(intervals, intervals[1:], strict=False):
            if previous[1] >= current[0]:
                raise ValueError("Overlappende formelområder")
        starts[column] = [interval[0] for interval in intervals]
    # All physical cells and dimension positions now exist, regardless of XML order.
    for cell in found.values():
        column, row = column_number(cell["column"]), cell["row"]
        matching_intervals = columns.get(column)
        if matching_intervals is None:
            continue
        index = bisect_right(starts[column], row) - 1
        if index >= 0 and row <= matching_intervals[index][1]:
            region = matching_intervals[index][2]
            budget.charge({"formula_region": region, "cached_value": cell["raw_v"]})
            cell["formula_result"] = True
            cell["formula_region"] = region
            cell["cached_value"] = cell["raw_v"]
    return positions


def inventory_workbook(raw: bytes, *, limits: Limits = DEFAULT_LIMITS) -> Inventory:
    if len(raw) > limits.max_bytes:
        raise ValueError("Arbeidsboken overskrider bytegrensen")
    try:
        archive = ZipFile(BytesIO(raw))
    except BadZipFile as error:
        raise ValueError("Ugyldig ZIP-arbeidsbok") from error
    with archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(infos) > limits.members or len(set(names)) != len(names):
            raise ValueError("For mange eller dupliserte ZIP-medlemmer")
        for info in infos:
            if (
                info.filename.startswith("/")
                or "\\" in info.filename
                or ":" in info.filename
                or ".." in info.filename.split("/")
                or info.flag_bits & 1
                or info.file_size > limits.member_bytes
            ):
                raise ValueError("Usikkert eller for stort ZIP-medlem")
        if sum(info.file_size for info in infos) > limits.inflated_bytes:
            raise ValueError("Utpakket størrelsesgrense overskredet")
        members: dict[str, bytes] = {}
        inflated = 0
        for info in infos:
            with archive.open(info) as stream:
                content = stream.read(limits.member_bytes + 1)
            inflated += len(content)
            if len(content) > limits.member_bytes or inflated > limits.inflated_bytes:
                raise ValueError("Faktisk utpakket størrelsesgrense overskredet")
            members[info.filename] = content
    roots = {
        name: safe_xml(content, limits)
        for name, content in members.items()
        if name.endswith((".xml", ".rels"))
    }
    if "xl/workbook.xml" not in roots or "xl/_rels/workbook.xml.rels" not in roots:
        raise ValueError("Arbeidsbok eller relasjoner mangler")
    # Kontroller alle relasjoner, også dem adapteren ikke fortolker.
    for name, root in roots.items():
        if not name.endswith(".rels"):
            continue
        if root.tag != f"{{{PACKAGE_REL}}}Relationships":
            raise ValueError("Ukjent relasjonsformat")
        origin = "" if name == "_rels/.rels" else name.replace("/_rels/", "/").removesuffix(".rels")
        seen: set[str] = set()
        for relation in root:
            rid = relation.get("Id", "")
            if not rid or rid in seen:
                raise ValueError("Duplisert eller tom relasjons-ID")
            seen.add(rid)
            if relation.get("TargetMode") == "External":
                # Bevares som metadata; hentes aldri. Eksterne ark tillates ikke nedenfor.
                continue
            if _target(origin, relation.get("Target", "")) not in members:
                raise ValueError("Relasjonsmål mangler")
    relationships = {item.get("Id"): item for item in roots["xl/_rels/workbook.xml.rels"]}
    strings: list[str] = []
    string_chars = 0
    if "xl/sharedStrings.xml" in roots:
        if roots["xl/sharedStrings.xml"].tag != f"{{{MAIN}}}sst":
            raise ValueError("Ukjent shared-string-format")
        for item in roots["xl/sharedStrings.xml"]:
            parts = (
                item.xpath("./m:t/text() | ./m:r/m:t/text()", namespaces={"m": MAIN})
                if item.tag == f"{{{MAIN}}}si"
                else []
            )
            size = sum(len(part) for part in parts)
            string_chars += size
            if size > limits.text_chars or string_chars > limits.resolved_chars:
                raise ValueError("Samlet shared-string-tekst overskrider grensen")
            strings.append("".join(parts))
    cells: list[dict[str, Any]] = []
    sheets: list[dict[str, Any]] = []
    physical_total = 0
    resolved_chars = 0
    formula_positions = 0
    materialized = MaterializationBudget(limits.serialized_chars)
    workbook = roots["xl/workbook.xml"]
    if workbook.tag != f"{{{MAIN}}}workbook":
        raise ValueError("Ukjent arbeidsbokformat")
    seen_names: set[str] = set()
    used_members: set[str] = set()
    for sheet in workbook.findall(f"{{{MAIN}}}sheets/{{{MAIN}}}sheet"):
        name = sheet.get("name", "")
        relationship = relationships.get(sheet.get(f"{{{REL}}}id"))
        if (
            not name
            or name in seen_names
            or relationship is None
            or relationship.get("TargetMode") == "External"
            or not relationship.get("Type", "").endswith("/worksheet")
        ):
            raise ValueError("Ugyldig eller duplisert arkrelasjon")
        seen_names.add(name)
        member = _target("xl/workbook.xml", relationship.get("Target", ""))
        if member in used_members or member not in roots:
            raise ValueError("Duplisert eller manglende arkinnhold")
        used_members.add(member)
        root = roots[member]
        if root.tag != f"{{{MAIN}}}worksheet":
            raise ValueError("Ukjent arkformat")
        found: dict[str, dict[str, Any]] = {}
        row_metadata: list[dict[str, str]] = []
        seen_rows: set[str | None] = set()
        for row in root.findall(f"{{{MAIN}}}sheetData/{{{MAIN}}}row"):
            if row.get("r") is None or row.get("r") in seen_rows:
                raise ValueError("Duplisert eller manglende radidentitet")
            seen_rows.add(row.get("r"))
            row_metadata.append(dict(row.attrib))
            for item in row.findall(f"{{{MAIN}}}c"):
                ref = item.get("r", "")
                col, row_num = address(ref)
                if ref in found or row.get("r") != str(row_num):
                    raise ValueError("Duplisert celle eller motstridende rad")
                physical_total += 1
                if physical_total > limits.cells:
                    raise ValueError("Fysisk cellegrense overskredet")
                values = item.findall(f"{{{MAIN}}}v")
                formulas = item.findall(f"{{{MAIN}}}f")
                inline = item.findall(f"{{{MAIN}}}is")
                if len(values) > 1 or len(formulas) > 1 or len(inline) > 1:
                    raise ValueError("Tvetydig celleverdi/formel")
                lexical = values[0].text if values else None
                kind = item.get("t", "n")
                resolved = lexical
                if kind == "inlineStr":
                    parts = (
                        inline[0].xpath("./m:t/text() | ./m:r/m:t/text()", namespaces={"m": MAIN})
                        if inline
                        else []
                    )
                    if sum(len(part) for part in parts) > min(
                        limits.text_chars, limits.resolved_chars - resolved_chars
                    ):
                        raise ValueError("Samlet løst celleinnhold overskrider grensen")
                    resolved = "".join(parts) if inline else None
                elif kind == "s":
                    if (
                        lexical is None
                        or not lexical.isascii()
                        or not lexical.isdigit()
                        or len(lexical) > 9
                    ):
                        raise ValueError("Ugyldig shared-string-indeks")
                    index = int(lexical)
                    if index >= len(strings):
                        raise ValueError("Shared-string-indeks utenfor inventar")
                    resolved = strings[index]
                if resolved is not None and len(resolved) > limits.text_chars:
                    raise ValueError("Celle-tekstgrense overskredet")
                resolved_chars += len(resolved or "")
                if resolved_chars > limits.resolved_chars:
                    raise ValueError("Samlet løst celleinnhold overskrider grensen")
                found[ref] = {
                    "id": identity("historisk-celle-1", name, ref),
                    "sheet": name,
                    "cell": ref,
                    "row": row_num,
                    "column": column_label(col),
                    "physical": True,
                    "state": "value" if lexical is not None or inline or formulas else "blank",
                    "raw_type": kind,
                    "raw_v": lexical,
                    "resolved_text": resolved,
                    "formula_present": bool(formulas),
                    "formula_result": bool(formulas),
                    "formula_region": None,
                    "formula": formulas[0].text if formulas else None,
                    "formula_attributes": dict(formulas[0].attrib) if formulas else None,
                    "cached_value": lexical if formulas else None,
                    "attributes": dict(item.attrib),
                    "row_attributes": dict(row.attrib),
                    "raw_xml": etree.tostring(item, encoding="unicode"),
                }
                materialized.charge(found[ref])
        dimension = root.find(f"{{{MAIN}}}dimension")
        dimension_ref = dimension.get("ref") if dimension is not None else None
        min_col, min_row, max_col, max_row = (1, 1, 0, 0)
        if dimension_ref:
            bounds = dimension_ref.split(":")
            if len(bounds) > 2:
                raise ValueError("Ugyldig arkdimensjon")
            first, last = address(bounds[0]), address(bounds[-1])
            if first[0] > last[0] or first[1] > last[1]:
                raise ValueError("Omvendt arkdimensjon")
            max_col, max_row = last
            min_col, min_row = first
        if (max_col - min_col + 1) * (max_row - min_row + 1) + len(cells) > limits.positions:
            raise ValueError("Dokumentert rutenett overskrider posisjonsgrensen")
        for row_num in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                ref = f"{column_label(col)}{row_num}"
                if ref not in found:
                    found[ref] = {
                        "id": identity("historisk-celle-1", name, ref),
                        "sheet": name,
                        "cell": ref,
                        "row": row_num,
                        "column": column_label(col),
                        "physical": False,
                        "state": "absent",
                        "raw_type": None,
                        "raw_v": None,
                        "resolved_text": None,
                        "formula_present": False,
                        "formula_result": False,
                        "formula_region": None,
                        "formula": None,
                        "formula_attributes": None,
                        "cached_value": None,
                        "attributes": {},
                        "row_attributes": {},
                        "raw_xml": None,
                    }
                    materialized.charge(found[ref])
        if len(cells) + len(found) > limits.positions:
            raise ValueError("Samlet celleunion overskrider posisjonsgrensen")
        formula_positions += _mark_formula_regions(
            found, limits.positions - formula_positions, materialized
        )
        cells.extend(sorted(found.values(), key=lambda c: (c["row"], column_number(c["column"]))))
        sheets.append(
            {
                "name": name,
                "member": member,
                "attributes": dict(sheet.attrib),
                "dimension": dimension_ref,
                "rows": row_metadata,
                "metadata_xml": [
                    etree.tostring(item, encoding="unicode")
                    for item in root
                    if item.tag != f"{{{MAIN}}}sheetData"
                ],
                "physical_cells": sum(c["physical"] for c in found.values()),
                "positions": len(found),
            }
        )
    if not sheets:
        raise ValueError("Arbeidsboken har ingen ark")
    return Inventory(
        tuple(cells),
        {
            "inventory_version": "historisk-celler-3",
            "limits": asdict(limits),
            "sheets": sheets,
            "physical_cells": physical_total,
            "positions": len(cells),
            "workbook_xml": members["xl/workbook.xml"].decode("utf-8-sig"),
            "members": [{"name": info.filename, "bytes": info.file_size} for info in infos],
            "other_xml": {
                name: content.decode("utf-8-sig")
                for name, content in members.items()
                if name.endswith((".xml", ".rels")) and name not in used_members
            },
            "formula_evaluation": "ikke utført",
            "column_style_expansion": False,
        },
    )
