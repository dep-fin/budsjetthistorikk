"""T5s selvforsynte produkteksport med de etablerte defensive Excel-profilene."""

import base64
from copy import copy
from dataclasses import asdict
from pathlib import Path
from tempfile import NamedTemporaryFile

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

from innlesning.observations import encode
from innlesning.proposisjon16_model import Report
from innlesning.visningspilot_model import PilotReport

from . import visningspilot_excel as old_excel
from .extraction_excel import Value, write_rows
from .omtale import report_from_json as read_omtale
from .omtale_excel_guard import SheetShape, inspect_excel
from .perioderegister_excel import _package_profile, _style_profile
from .proposisjon16 import contents, export_json, report_from_json, report_to_json
from .saksdokumenter import _publish

SHEET_NAMES = old_excel.SHEET_NAMES | {"Fullmakter", "Grenbevis", "T5-dekning"}


def _selected(report: Report, accounts: tuple[str, ...], document_ids: tuple[str, ...]) -> str:
    selection = report.selection
    match = (
        selection.document_id in document_ids
        if selection.mode == "document"
        else 2024 in selection.years
        and any(
            account.split("/")[0] in selection.chapters
            or tuple(account.split("/")) in selection.accounts
            for account in accounts
        )
    )
    return "ja" if match else "nei"


def _book(report: Report, frozen: str) -> Workbook:
    data = contents(report.basis)
    projection = PilotReport(
        report.id, data, report.selection, report.return_selection, report.view, report.version
    )
    book = old_excel._book(projection, frozen)
    book["Visningsgrunnlag"]["B1"] = "Frosset proposisjon16-1 med originalbyte"
    book["Dokumenter"]["G1"] = "Historisk T1-strukturdekning"
    bindings = {b.inventory_id: b.observation_ids for b in report.basis.bindings}
    inventory = book["Inventar"]
    inventory["G1"] = "Historisk T1-strukturstatus"
    inventory["M1"], inventory["N1"] = "T5-feltbinding", "Gjeldende tabellstatus"
    for column_number in (13, 14):
        inventory.cell(1, column_number).font = copy(inventory["G1"].font)
        inventory.cell(1, column_number).fill = copy(inventory["G1"].fill)
    for row_number, item in enumerate(data.inventory, 2):
        inventory.cell(row_number, 13, encode(bindings.get(item.id, ())))
        inventory.cell(row_number, 14, "strukturert_T5" if bindings.get(item.id) else "T1_bevart")
    inventory.auto_filter.ref = inventory.dimensions
    accounts = book["Kontoer"]
    accounts["G1"] = "Historisk T1-strukturstatus"
    accounts["H1"] = "Gjeldende T5-tabellstatus"
    accounts["H1"].font = copy(accounts["G1"].font)
    accounts["H1"].fill = copy(accounts["G1"].fill)
    for account_row in accounts.iter_rows(min_row=2):
        identifier = str(account_row[5].value)
        accounts.cell(
            int(account_row[0].row or 0),
            8,
            "strukturert_T5" if bindings.get(identifier) else "T1_bevart",
        )
    accounts.auto_filter.ref = accounts.dimensions
    book["Relasjoner"]["D1"] = "Historisk T1-rolle"
    book["Relasjoner"]["E1"] = "Historisk T1-omfang; gjeldende gren i Grenbevis"
    book["Relasjoner"].column_dimensions["E"].width = 52
    coverage_sheet = book["Dekning"]
    for row in coverage_sheet.iter_rows(min_row=2):
        if str(row[0].value).startswith(
            ("prop16_delvis_strukturert:", "inns95_strukturering_ikke_levert:")
        ):
            row[0].value = "Historisk T1: " + str(row[0].value)
    # Råpayload ligger bare i den selvforsynte kapselen. Synlig originalark peker dit.
    originals: list[list[Value]] = [
        [
            "Kilde-ID",
            "Originalnavn",
            "Dokumentnøkkel",
            "Format",
            "SHA-256",
            "Byte",
            "Forventet SHA-256",
            "Status",
            "Metadata",
            "Payloadreferanse",
        ]
    ]
    old = read_omtale(data.o2b_json)
    for source in (*data.sources, *report.basis.sources):
        originals.append(
            [
                source.id,
                source.name,
                source.document_key,
                source.media_type,
                source.sha256,
                source.byte_count,
                source.expected_sha256,
                source.status,
                source.metadata_json,
                "Visningsgrunnlag: " + source.id,
            ]
        )
    originals.extend(
        [
            s.id,
            s.name,
            s.document_id,
            s.media_type,
            s.sha256,
            s.byte_count,
            s.expected_sha256,
            s.status,
            s.metadata_json,
            "Visningsgrunnlag: " + s.id,
        ]
        for s in old.basis.sources
    )
    original_index = book.sheetnames.index("Originaler")
    book.remove(book["Originaler"])
    write_rows(book, "Originaler", originals)
    book.move_sheet(book["Originaler"], offset=original_index - (len(book.sheetnames) - 1))
    tables: dict[str, list[list[Value]]] = {
        "Fullmakter": [
            [
                "Romertall",
                "Punkt",
                "Kontoer",
                "Felles ramme kr",
                "Rolle",
                "Periode",
                "Status",
                "Kilde-ID",
                "Lokator",
                "Inventar-ID",
                "Råtekst med vilkår",
                "Valgt",
            ]
        ],
        "Grenbevis": [
            [
                "Prop.-punkt",
                "Kontoer",
                "Sak",
                "Innst.-punkt",
                "Vedtaks-ID-er",
                "Beløpsstadium",
                "Status",
                "Fra dokument-ID",
                "Til dokument-ID",
                "Kildebevis",
                "Gren-ID",
                "Valgt",
            ]
        ],
        "T5-dekning": [
            [
                "Dokument-ID",
                "Tabellgrupper",
                "Forslagfelt",
                "Ulike kontoangivelser",
                "Gjeldende status",
                "Omfang",
                "Historisk T1-avvik",
                "Overlay-ID",
            ]
        ],
    }
    for a in report.basis.authorizations:
        tables["Fullmakter"].append(
            [
                a.roman,
                a.point,
                ", ".join(a.accounts),
                a.frame_kr,
                a.role,
                a.period,
                a.status,
                a.source_id,
                a.locator,
                a.id,
                a.text,
                _selected(report, a.accounts, (a.document_id,)),
            ]
        )
    for b in report.basis.branches:
        tables["Grenbevis"].append(
            [
                b.point,
                ", ".join(b.accounts),
                b.case_id,
                b.committee_point,
                ", ".join(b.decision_ids),
                b.amount_stage,
                b.status,
                b.from_document_id,
                b.to_document_id,
                encode(b.evidence_ids),
                b.id,
                _selected(report, b.accounts, (b.from_document_id, b.to_document_id)),
            ]
        )
    for c in report.basis.coverage:
        tables["T5-dekning"].append(
            [
                c.document_id,
                c.table_groups,
                c.table_fields,
                c.account_count,
                c.status,
                c.scope,
                c.historical_issue,
                c.id,
            ]
        )
    for name, rows in tables.items():
        write_rows(book, name, rows)
    for name in (*tables, "Originaler"):
        sheet = book[name]
        for row in sheet:
            sheet.row_dimensions[int(row[0].row or 0)].height = 48 if row[0].row == 1 else 36
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
                if type(cell.value) is int:
                    cell.number_format = "#,##0"
        for column_number in range(1, sheet.max_column + 1):
            sheet.column_dimensions[get_column_letter(column_number)].width = 32
    for name, widths in {
        "Fullmakter": {"A": 12, "B": 10, "C": 36, "D": 23, "E": 32, "F": 54, "K": 110},
        "Grenbevis": {"A": 16, "B": 105, "C": 15, "D": 16, "E": 32, "F": 30, "G": 26},
        "T5-dekning": {"A": 24, "B": 18, "C": 18, "D": 22, "E": 52, "F": 80, "G": 80},
        "Forløp": {"B": 44, "G": 24, "H": 22, "I": 28, "J": 24, "K": 22},
        "Inventar": {"G": 36, "H": 80, "M": 42, "N": 32},
        "Kontoer": {"D": 42, "G": 36, "H": 36},
    }.items():
        for column, width in widths.items():
            book[name].column_dimensions[column].width = width
    book["Grenbevis"].row_dimensions[3].height = 66
    for sheet in (book["Forløp"], book["Inventar"], book["Kontoer"]):
        for row in sheet:
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
            sheet.row_dimensions[int(row[0].row or 0)].height = (
                48 if row[0].row == 1 or sheet.title == "Inventar" else 36
            )
    # Overlegg og fullmakter har klikkbar dokumentreferanse, i begge retninger.
    document_rows = {d.id: row for row, d in enumerate(data.documents, 2)}
    for number, c in enumerate(report.basis.coverage, 2):
        old_excel._link(
            book, "T5-dekning", f"A{number}", "Dokumenter", f"B{document_rows[c.document_id]}"
        )
        old_excel._link(
            book, "Dokumenter", f"G{document_rows[c.document_id]}", "T5-dekning", f"E{number}"
        )
    for number, branch in enumerate(report.basis.branches, 2):
        old_excel._link(
            book,
            "Grenbevis",
            f"I{number}",
            "Dokumenter",
            f"B{document_rows[branch.to_document_id]}",
        )
    return book


def read_excel(path: Path) -> Report:
    raw, shapes = inspect_excel(
        path,
        sheet_names=SHEET_NAMES,
        snapshot_name="Visningsgrunnlag",
        max_expanded_bytes=128 * 1024 * 1024,
    )
    _package_profile(path, len(shapes))
    report = report_from_json(raw)
    expected = _book(report, raw)
    try:
        if shapes != {s.title: SheetShape(s.max_row, s.max_column) for s in expected}:
            raise ValueError("T5-Excel har uventede ark/celleområder")
        _style_profile(path, expected)
        saved = load_workbook(path, data_only=False, keep_links=False)
        try:
            if saved.sheetnames != expected.sheetnames or saved.views != expected.views:
                raise ValueError("T5-Excel har endret arkrekkefølge/arbeidsbokvisning")
            for wanted_sheet, actual_sheet in zip(expected, saved, strict=True):
                for dimension in wanted_sheet.column_dimensions.values():
                    dimension.reindex()
                if (
                    actual_sheet.sheet_state != wanted_sheet.sheet_state
                    or actual_sheet.sheet_view != wanted_sheet.sheet_view
                    or actual_sheet.sheet_format != wanted_sheet.sheet_format
                    or actual_sheet.auto_filter != wanted_sheet.auto_filter
                    or actual_sheet.merged_cells != wanted_sheet.merged_cells
                    or set(actual_sheet.row_dimensions) != set(wanted_sheet.row_dimensions)
                    or set(actual_sheet.column_dimensions) != set(wanted_sheet.column_dimensions)
                    or any(
                        dict(actual_sheet.row_dimensions[k]) != dict(d)
                        for k, d in wanted_sheet.row_dimensions.items()
                    )
                    or any(
                        dict(actual_sheet.column_dimensions[k]) != dict(d)
                        for k, d in wanted_sheet.column_dimensions.items()
                    )
                ):
                    raise ValueError("T5-Excel har endret synlighet/oppsett: " + actual_sheet.title)
                for wanted_row, actual_row in zip(wanted_sheet, actual_sheet, strict=True):
                    for wanted, actual in zip(wanted_row, actual_row, strict=True):
                        value = None if wanted.value == "" else wanted.value
                        if (
                            actual.value != value
                            or type(actual.value) is not type(value)
                            or isinstance(value, str)
                            and actual.data_type != "s"
                            or actual.data_type == "f"
                            or actual.number_format != wanted.number_format
                            or copy(actual.font) != copy(wanted.font)
                            or copy(actual.fill) != copy(wanted.fill)
                            or copy(actual.border) != copy(wanted.border)
                            or copy(actual.alignment) != copy(wanted.alignment)
                            or copy(actual.protection) != copy(wanted.protection)
                            or (actual.hyperlink.location if actual.hyperlink else None)
                            != (wanted.hyperlink.location if wanted.hyperlink else None)
                            or (actual.hyperlink.target if actual.hyperlink else None)
                            != (wanted.hyperlink.target if wanted.hyperlink else None)
                        ):
                            raise ValueError(
                                "T5-Excel avviker i celle/stil/lenke: "
                                + actual_sheet.title
                                + "!"
                                + actual.coordinate
                            )
        finally:
            saved.close()
    finally:
        expected.close()
    return report


def export_excel(report: Report, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".xlsx":
        raise ValueError("Velg nytt T5-Excel-filnavn")
    raw = report_to_json(report)
    book = _book(report, raw)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".xlsx", delete=False) as handle:
            temporary = Path(handle.name)
        book.save(temporary)
        if read_excel(temporary) != report:
            raise ValueError("Skrevet T5-Excel avviker")
        _publish(temporary, output)
    finally:
        book.close()
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def export_pair(report: Report, frozen: Path, excel: Path) -> None:
    if frozen.resolve() == excel.resolve() or frozen.exists() or excel.exists():
        raise ValueError("Velg to forskjellige nye filnavn")
    export_json(report, frozen)
    export_excel(report, excel)


def export_originals(report: Report, directory: Path) -> None:
    report_to_json(report)
    directory.mkdir(parents=True, exist_ok=False)
    old = read_omtale(report.basis.t1_basis.o2b_json)
    entries = [("t1/" + s.name, s.content_base64) for s in report.basis.t1_basis.sources]
    entries += [("o2b/" + s.name, s.content_base64) for s in old.basis.sources]
    entries += [(s.name, s.content_base64) for s in report.basis.sources]
    for name, content in entries:
        if content is None:
            continue
        path = (directory / name).resolve()
        if not path.is_relative_to(directory.resolve()):
            raise ValueError("T5-originalsti utenfor eksportkatalog")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(base64.b64decode(content, validate=True))
    (directory / "index.json").write_text(
        encode(
            {
                "basis_id": report.basis.id,
                "coverage": [asdict(c) for c in report.basis.coverage],
                "sources": [s.id for s in report.basis.sources],
            }
        ),
        encoding="utf8",
    )
