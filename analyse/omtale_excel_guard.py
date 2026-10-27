"""Ressurs- og strukturkontroll av O2a-arkiv før openpyxl får laste celler."""

import posixpath
import re
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, BadZipFile, ZipFile

from lxml import etree
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string

from .session_serialization import MAX_REPORT_BYTES

S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
MAX_ARCHIVE_MEMBERS = 256
MAX_SHEETS = 64
MAX_CELLS = 60_000
MAX_ROWS = 20_000
MAX_COLUMNS = 256
MAX_EXPANDED_BYTES = 4 * MAX_REPORT_BYTES
MAX_COMPRESSION_RATIO = 2000  # Også store, repeterende base64-originaler er legitime.
METADATA_BYTES = 2 * 1024 * 1024
BASE_SHEETS = {
    "Historikk",
    "Historikkdetaljer",
    "Beløpsobservasjoner",
    "Kildeinventar",
    "Avvik",
    "Sesjonsgrunnlag",
    "Inventarjobber",
    "Dekning",
    "Summer",
    "Historikkberegninger",
    "Kontrollresultater",
    "Avstemming",
    "Kildeprøvekontroll",
    "Eksportavstemming",
    "Vedtaksfulltekst",
    "Tekstopplysninger",
    "Inventarfulltekst",
    "Saksdokumenter",
    "Dokumentrelasjoner",
    "Dokumentavvik",
    "Stikkordgrunnlag",
    "Saksgrunnlag",
    "Omtale",
    "Relasjoner",
    "Omtalekilder",
    "Omtaleavvik",
    "Omtalegrunnlag",
    "Uavhengig kontroll 2024",
    "Omfangsforskjeller 2024",
}
WORKSHEET_TAGS = {
    S + name
    for name in (
        "worksheet",
        "sheetPr",
        "outlinePr",
        "pageSetUpPr",
        "dimension",
        "sheetViews",
        "sheetView",
        "pane",
        "selection",
        "sheetFormatPr",
        "cols",
        "col",
        "sheetData",
        "row",
        "c",
        "is",
        "t",
        "v",
        "autoFilter",
        "hyperlinks",
        "hyperlink",
        "pageMargins",
        "tabColor",
    )
}
WORKSHEET_ATTRIBUTES = {
    "worksheet": set(),
    "sheetPr": set(),
    "outlinePr": {"summaryBelow", "summaryRight"},
    "pageSetUpPr": set(),
    "tabColor": {"rgb"},
    "dimension": {"ref"},
    "sheetViews": set(),
    "sheetView": {"showGridLines", "workbookViewId"},
    "pane": {"activePane", "state", "topLeftCell", "xSplit", "ySplit"},
    "selection": {"activeCell", "pane", "sqref"},
    "sheetFormatPr": {"baseColWidth", "defaultRowHeight"},
    "cols": set(),
    "col": {"width", "customWidth", "min", "max"},
    "sheetData": set(),
    "row": {"r", "ht", "customHeight"},
    "c": {"r", "s", "t"},
    "is": set(),
    "t": {"{http://www.w3.org/XML/1998/namespace}space"},
    "v": set(),
    "autoFilter": {"ref"},
    "hyperlinks": set(),
    "hyperlink": {"ref", "location", R + "id"},
    "pageMargins": {"left", "right", "top", "bottom", "header", "footer"},
}


@dataclass(frozen=True)
class SheetShape:
    rows: int
    columns: int


def _metadata(archive: ZipFile, name: str) -> etree._Element:
    if archive.getinfo(name).file_size > METADATA_BYTES:
        raise ValueError("Excel-metadata overstiger ressursgrense")
    root = etree.fromstring(
        archive.read(name),
        etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True),
    )
    if root.getroottree().docinfo.doctype:
        raise ValueError("DOCTYPE er ikke tillatt i Excel")
    return root


def _coordinate(value: str) -> tuple[int, int]:
    if not re.fullmatch(r"[A-Z]{1,3}[1-9][0-9]{0,6}", value):
        raise ValueError("Ugyldig Excel-cellepeker")
    letters, number = coordinate_from_string(value)
    column = column_index_from_string(letters)
    if number > MAX_ROWS or column > MAX_COLUMNS:
        raise ValueError("Excel-cellepeker overstiger ressursgrense")
    return number, column


def _index(value: str, maximum: int, *, minimum: int = 0) -> int:
    if not re.fullmatch(r"[0-9]{1,8}", value) or not minimum <= int(value) <= maximum:
        raise ValueError("Excel-indeks overstiger ressursgrense eller er ugyldig")
    return int(value)


def _range(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    parts = value.split(":")
    if not 1 <= len(parts) <= 2:
        raise ValueError("Ugyldig Excel-område")
    first, last = _coordinate(parts[0]), _coordinate(parts[-1])
    if first[0] > last[0] or first[1] > last[1]:
        raise ValueError("Reversert Excel-område")
    return first, last


def _style_count(archive: ZipFile) -> int:
    root = _metadata(archive, "xl/styles.xml")
    if len({child.tag for child in root}) != len(root):
        raise ValueError("Excel har dupliserte stilgrupper")
    groups = {}
    for name in ("fonts", "fills", "borders", "cellStyleXfs", "cellXfs"):
        elements = root.findall(S + name)
        if len(elements) != 1 or not 1 <= len(elements[0]) <= MAX_CELLS:
            raise ValueError("Ugyldig Excel-stiltabell eller ressursgrense")
        groups[name] = elements[0]
    number_formats = root.find(S + "numFmts")
    custom_formats: set[int] = set()
    if number_formats is not None:
        for element in number_formats:
            index = _index(element.get("numFmtId", ""), 164 + len(number_formats) - 1, minimum=164)
            if index in custom_formats:
                raise ValueError("Excel har dupliserte tallformatindekser")
            custom_formats.add(index)
    for metadata_group in root:
        if "count" in metadata_group.attrib and _index(
            metadata_group.attrib["count"], MAX_CELLS
        ) != len(metadata_group):
            raise ValueError("Excel har feil antall stilposter")
    for name in ("cellStyleXfs", "cellXfs", "cellStyles"):
        group = root.find(S + name)
        if group is None:
            continue
        for element in group:
            if "numFmtId" in element.attrib:
                index = _index(element.attrib["numFmtId"], 163 + len(custom_formats))
                if index >= 164 and index not in custom_formats:
                    raise ValueError("Excel har ubundet tallformatindeks")
            for attribute, target in (
                ("fontId", "fonts"),
                ("fillId", "fills"),
                ("borderId", "borders"),
                ("xfId", "cellStyleXfs"),
            ):
                if attribute in element.attrib:
                    _index(element.attrib[attribute], len(groups[target]) - 1)
    return len(groups["cellXfs"])


def _workbook_ranges(archive: ZipFile, paths: dict[str, str]) -> int:
    """Eksportens eneste navngitte områder er de lokale autofilterområdene."""
    root = _metadata(archive, "xl/workbook.xml")
    allowed = {
        "workbook",
        "workbookPr",
        "bookViews",
        "workbookView",
        "sheets",
        "sheet",
        "definedNames",
        "definedName",
        "calcPr",
        "workbookProtection",
    }
    if any(element.tag not in {S + name for name in allowed} for element in root.iter()):
        raise ValueError("Excel-arbeidsbok har uventet XML-innhold")
    parents = {
        "workbookPr": "workbook",
        "workbookProtection": "workbook",
        "bookViews": "workbook",
        "workbookView": "bookViews",
        "sheets": "workbook",
        "sheet": "sheets",
        "definedNames": "workbook",
        "definedName": "definedNames",
        "calcPr": "workbook",
    }
    if len({child.tag for child in root}) != len(root):
        raise ValueError("Excel-arbeidsbok har dupliserte XML-grupper")
    for element in root.iterdescendants():
        parent = element.getparent()
        if parent is None or parent.tag != S + parents.get(etree.QName(element).localname, ""):
            raise ValueError("Excel-arbeidsbok har ugyldig XML-struktur")
    views = root.find(S + "bookViews")
    if views is None or not 1 <= len(views) <= MAX_SHEETS:
        raise ValueError("Excel har ugyldige arbeidsbokvisninger")
    for view in views:
        for attribute in ("activeTab", "firstSheet"):
            if attribute in view.attrib:
                _index(view.attrib[attribute], len(paths) - 1)
    names = list(paths)
    seen = set()
    for element in root.findall(S + "definedNames/" + S + "definedName"):
        if (
            set(element.attrib) != {"name", "localSheetId", "hidden"}
            or element.get("name") != "_xlnm._FilterDatabase"
            or element.get("hidden") != "1"
        ):
            raise ValueError("Excel har uventet navngitt område")
        index = _index(element.get("localSheetId", ""), len(paths) - 1)
        prefix = "'" + names[index].replace("'", "''") + "'!"
        value = element.text or ""
        if index in seen or not value.startswith(prefix):
            raise ValueError("Excel har duplisert eller ubundet filterområde")
        seen.add(index)
        reference = value[len(prefix) :]
        if not re.fullmatch(
            r"\$[A-Z]{1,3}\$[1-9][0-9]{0,6}:\$[A-Z]{1,3}\$[1-9][0-9]{0,6}", reference
        ):
            raise ValueError("Excel har uventet filterområde")
        _range(reference.replace("$", ""))
    return len(views)


def _sheet_reference_attributes(
    element: etree._Element, styles: int, views: int, sheet_names: frozenset[str]
) -> None:
    """Kontroller alle indekser/områder i den smale eksportgrammatikken."""
    name = etree.QName(element).localname
    if set(element.attrib) - WORKSHEET_ATTRIBUTES[name]:
        raise ValueError("Excel-ark har uventede XML-attributter")
    if name in {"dimension", "autoFilter"}:
        _range(element.get("ref", ""))
    elif name == "hyperlink":
        _coordinate(element.get("ref", ""))
        if "location" in element.attrib:
            match = re.fullmatch(
                r"'([^']+)'!([A-Z]{1,3}[1-9][0-9]{0,6})", element.attrib["location"]
            )
            if match is None or match[1] not in sheet_names:
                raise ValueError("Excel har uventet intern lenke")
            _coordinate(match[2])
    elif name == "selection":
        _coordinate(element.get("activeCell", ""))
        _coordinate(element.get("sqref", ""))
    elif name == "pane":
        if element.get("state") != "frozen":
            raise ValueError("Excel har uventet rutefrysing")
        _coordinate(element.get("topLeftCell", ""))
        for attribute, maximum in (("xSplit", MAX_COLUMNS), ("ySplit", MAX_ROWS)):
            if attribute in element.attrib:
                _index(element.attrib[attribute], maximum)
    elif name == "sheetView":
        _index(element.get("workbookViewId", ""), views - 1)
    elif name == "col":
        first = _index(element.get("min", ""), MAX_COLUMNS, minimum=1)
        _index(element.get("max", ""), MAX_COLUMNS, minimum=first)
    elif name == "c":
        _index(element.get("s", "0"), styles - 1)
        if element.get("t", "n") not in {"n", "inlineStr"}:
            raise ValueError("Excel har uventet celletype")


def _sheet_paths(
    archive: ZipFile, sheet_names: frozenset[str], snapshot_name: str
) -> dict[str, str]:
    book = _metadata(archive, "xl/workbook.xml")
    rels = _metadata(archive, "xl/_rels/workbook.xml.rels")
    targets = {}
    for relationship in rels:
        identifier, target = relationship.get("Id"), relationship.get("Target", "")
        if identifier in targets or relationship.get("TargetMode") == "External":
            raise ValueError("Ugyldig Excel-arkrelasjon")
        path = posixpath.normpath(target.lstrip("/") if target.startswith("/") else "xl/" + target)
        targets[identifier] = (path, relationship.get("Type", ""))
    result: dict[str, str] = {}
    sheets = book.find(S + "sheets")
    if sheets is None or not 1 <= len(sheets) <= MAX_SHEETS:
        raise ValueError("Excel har feil antall ark")
    allowed = sheet_names | {f"{name[:18]} fortsettelse" for name in sheet_names}
    for sheet in sheets:
        name = sheet.get("name", "")
        path, kind = targets.get(sheet.get(R + "id"), ("", ""))
        if (
            name not in allowed
            or name in result
            or path in result.values()
            or not kind.endswith("/worksheet")
            or not re.fullmatch(r"xl/worksheets/sheet[1-9][0-9]*\.xml", path)
        ):
            raise ValueError("Uventet eller duplisert Excel-ark")
        _index(sheet.get("sheetId", ""), MAX_SHEETS, minimum=1)
        result[name] = path
    physical = {n for n in archive.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)}
    if set(result.values()) != physical or snapshot_name not in result:
        raise ValueError("Excel har ubundne eller manglende ark")
    return result


def inspect_excel(
    path: Path,
    *,
    sheet_names: frozenset[str] = frozenset(BASE_SHEETS),
    snapshot_name: str = "Omtalegrunnlag",
    max_expanded_bytes: int = MAX_EXPANDED_BYTES,
) -> tuple[str, dict[str, SheetShape]]:
    """Strøm bare avgrenset XML; returner frosset tekst og faktiske arkdimensjoner."""
    if path.stat().st_size > MAX_REPORT_BYTES:
        raise ValueError("Excel-arkiv overstiger 128 MiB")
    try:
        with ZipFile(path) as archive:
            members = archive.infolist()
            if (
                len(members) > MAX_ARCHIVE_MEMBERS
                or len({m.filename for m in members}) != len(members)
                or sum(m.file_size for m in members) > max_expanded_bytes
            ):
                raise ValueError("Excel-arkiv overstiger ressursgrense eller har duplikater")
            for member in members:
                if (
                    member.flag_bits & 1
                    or member.compress_type not in {ZIP_STORED, ZIP_DEFLATED}
                    or member.file_size > 2 * MAX_REPORT_BYTES
                    or member.file_size > max(1, member.compress_size) * MAX_COMPRESSION_RATIO
                    or not re.fullmatch(
                        r"(?:\[Content_Types\]\.xml|_rels/\.rels|docProps/(?:app|core)\.xml|"
                        r"xl/(?:workbook\.xml|_rels/workbook\.xml\.rels|styles\.xml|theme/theme1\.xml|"
                        r"worksheets/(?:sheet[1-9][0-9]*\.xml|_rels/sheet[1-9][0-9]*\.xml\.rels)))",
                        member.filename,
                    )
                ):
                    raise ValueError("Excel-arkiv har uventet innhold eller kompresjonsgrense")
                if not re.fullmatch(r"xl/worksheets/sheet[1-9][0-9]*\.xml", member.filename):
                    _metadata(archive, member.filename)
            paths = _sheet_paths(archive, sheet_names, snapshot_name)
            styles = _style_count(archive)
            views = _workbook_ranges(archive, paths)
            snapshot: list[str] = []
            shapes = {}
            cells = 0
            xml_nodes = 0
            frozen_bytes = 0
            for name, member_path in paths.items():
                last_row = last_column = row_index = column_index = 0
                parts: list[str] = []
                inside_cell = False
                cell_coordinates: set[tuple[int, int]] = set()
                link_coordinates: set[tuple[int, int]] = set()
                column_ranges: set[int] = set()
                declared_ranges: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {}
                with archive.open(member_path) as stream:
                    context = etree.iterparse(
                        stream,
                        events=("start", "end"),
                        resolve_entities=False,
                        load_dtd=False,
                        no_network=True,
                    )
                    for event, element in context:
                        if event == "start":
                            xml_nodes += 1
                            if element.tag not in WORKSHEET_TAGS or xml_nodes > 10 * MAX_CELLS:
                                raise ValueError(
                                    "Excel-ark har ubundet XML-innhold eller ressursgrense"
                                )
                            _sheet_reference_attributes(element, styles, views, sheet_names)
                            if element.tag in {S + "dimension", S + "autoFilter"}:
                                if element.tag in declared_ranges:
                                    raise ValueError("Excel har dupliserte celleområder")
                                declared_ranges[str(element.tag)] = _range(element.get("ref", ""))
                            elif element.tag == S + "hyperlink":
                                coordinate = _coordinate(element.get("ref", ""))
                                if (
                                    coordinate in link_coordinates
                                    or len(link_coordinates) >= MAX_CELLS
                                ):
                                    raise ValueError(
                                        "Excel har dupliserte lenker eller ressursgrense"
                                    )
                                link_coordinates.add(coordinate)
                            elif element.tag == S + "col":
                                columns = set(
                                    range(
                                        int(element.attrib["min"]), int(element.attrib["max"]) + 1
                                    )
                                )
                                if column_ranges & columns:
                                    raise ValueError("Excel har overlappende kolonneområder")
                                column_ranges.update(columns)
                            if element.tag == S + "c":
                                parent = element.getparent()
                                if inside_cell or parent is None or parent.tag != S + "row":
                                    raise ValueError("Excel har ugyldig cellestruktur")
                                inside_cell = True
                            if element.tag == S + "row":
                                current = int(element.get("r", "0"))
                                if current <= row_index or current > MAX_ROWS:
                                    raise ValueError("Duplisert eller for stor Excel-rad")
                                row_index, column_index = current, 0
                                last_row = current
                            continue
                        if len(element.text or "") > 32_767:
                            raise ValueError("Excel-tekstcelle overstiger ressursgrense")
                        if element.tag == S + "c":
                            cells += 1
                            number, column = _coordinate(element.get("r", ""))
                            if (
                                cells > MAX_CELLS
                                or number > MAX_ROWS
                                or column > MAX_COLUMNS
                                or number != row_index
                                or column <= column_index
                            ):
                                raise ValueError(
                                    "Excel-celler overstiger grense eller har feil rekkefølge"
                                )
                            column_index = column
                            cell_coordinates.add((number, column))
                            last_column = max(last_column, column)
                            if name == snapshot_name and number > 1:
                                if element.find(S + "f") is not None:
                                    raise ValueError("Formel i frosset Excel-grunnlag")
                                if column == 1:
                                    value = element.findtext(S + "v")
                                    if element.get("t", "n") != "n" or value != str(number - 1):
                                        raise ValueError("Feil delrekkefølge i omtalegrunnlag")
                                elif column == 2 and element.get("t") == "inlineStr":
                                    value = "".join(t.text or "" for t in element.iter(S + "t"))
                                    frozen_bytes += len(value.encode("utf-8"))
                                    if frozen_bytes > MAX_REPORT_BYTES or len(value) > 30_000:
                                        raise ValueError("Frosset Excel-grunnlag overstiger grense")
                                    parts.append(value)
                                else:
                                    raise ValueError("Ugyldig celle i omtalegrunnlag")
                            element.clear()
                            inside_cell = False
                        elif element.tag == S + "row":
                            # Rader er strengt stigende; ingen skjulte/dupliserte celleområder.
                            number = int(element.get("r", "0"))
                            if number != row_index or number > MAX_ROWS:
                                raise ValueError("Excel har ugyldige arkrader")
                            element.clear()
                            while element.getprevious() is not None:
                                parent = element.getparent()
                                assert parent is not None
                                del parent[0]
                        elif not inside_cell:
                            element.clear()
                    assert context.root is not None
                    if context.root.getroottree().docinfo.doctype:
                        raise ValueError("DOCTYPE er ikke tillatt i Excel")
                shapes[name] = SheetShape(last_row, last_column)
                if (
                    not link_coordinates <= cell_coordinates
                    or any(column > last_column for column in column_ranges)
                    or any(
                        bounds != ((1, 1), (last_row, last_column))
                        for bounds in declared_ranges.values()
                    )
                ):
                    raise ValueError("Excel har ubundne lenker eller celleområder")
                if name == snapshot_name:
                    snapshot = parts
            if not snapshot:
                raise ValueError("Excel mangler innebygd omtalegrunnlag")
            return "".join(snapshot), shapes
    except (BadZipFile, etree.LxmlError, KeyError, TypeError) as error:
        raise ValueError("Ugyldig Excel-arkiv/XML") from error
