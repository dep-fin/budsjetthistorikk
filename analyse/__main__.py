"""Eksport kan kjøres uten ny innlesning eller nettilgang."""

import argparse
import json
import sqlite3
from pathlib import Path

from . import export_excel, export_extraction_excel, export_revision_excel
from .history import HistorySelection, calculate_history, read_history
from .history_excel import export_history_excel


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--kjoring", help="Eksakt lagret B1/B2-struktureringsresultat")
    selection.add_argument("--revisjon", help="Eksakt lagret B2-innholdsrevisjon")
    selection.add_argument("--utvalg", type=Path, help="JSON med eksplisitt B3-utvalg")
    selection.add_argument("--beregning", help="Eksakt lagret B3-beregning")
    selection.add_argument("--belopsuttrekk", help="Hele valgte beløpsuttrekk, også uten beløp")
    selection.add_argument(
        "--sesjonsutvalg", type=Path, help="JSON med eksplisitt samlet sesjonsutvalg"
    )
    parser.add_argument("--excel", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        calculation_id: str | None = None
        session_result = None
        if arguments.sesjonsutvalg:
            from .session import selection_from_dict
            from .session_excel import export_session_excel

            path = arguments.sesjonsutvalg
            if path.stat().st_size > 8 * 1024 * 1024:
                raise ValueError("Sesjonsutvalget overstiger 8 MiB")
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(data, dict):
                raise ValueError("Sesjonsutvalget må være et JSON-objekt")
            controls = data.get("preserved_2024_controls")
            if isinstance(controls, str) and not Path(controls).is_absolute():
                data["preserved_2024_controls"] = str((path.parent / controls).resolve())
            session_result = export_session_excel(
                arguments.database, selection_from_dict(data), arguments.excel, input_path=path
            )
        elif arguments.utvalg:
            paths = [
                arguments.database.resolve(),
                arguments.excel.resolve(),
                arguments.utvalg.resolve(),
            ]
            if len(set(paths)) != len(paths):
                raise ValueError("Database, Excel og utvalgsfil må ha forskjellige baner")
            data = json.loads(arguments.utvalg.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Utvalgsfilen må inneholde et JSON-objekt")
            data["extraction_ids"] = tuple(data.get("extraction_ids", []))
            data["step_order"] = tuple(data.get("step_order", []))
            calculation = calculate_history(arguments.database, HistorySelection(**data))
            calculation_id = calculation.id
            export_history_excel(arguments.database, calculation.id, arguments.excel)
        elif arguments.beregning:
            calculation_id = str(arguments.beregning)
            export_history_excel(arguments.database, calculation_id, arguments.excel)
        elif arguments.revisjon:
            export_revision_excel(arguments.database, arguments.revisjon, arguments.excel)
        elif arguments.belopsuttrekk:
            export_extraction_excel(arguments.database, arguments.belopsuttrekk, arguments.excel)
        else:
            export_excel(arguments.database, arguments.kjoring, arguments.excel)
    except (OSError, ValueError, TypeError, sqlite3.Error) as error:
        print(json.dumps({"status": "eksportfeil", "feil": str(error)}))
        return 1
    result = {"status": "eksportert", "fil": str(arguments.excel)}
    if session_result is not None:
        result.update(
            sesjonsrapport=session_result.id,
            inventar=str(len(session_result.inventory)),
            observasjoner=str(len(session_result.rows)),
            avstemming="utført" if session_result.reconciliations else "ikke utført",
            dekningsgrense=session_result.coverage.boundary,
        )
    if calculation_id is not None:
        calculation = read_history(arguments.database, calculation_id)
        result.update(
            beregning=calculation_id,
            kjedestatus=calculation.status,
            ferskhet=calculation.freshness,
            dekningsgrense=calculation.coverage,
        )
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
