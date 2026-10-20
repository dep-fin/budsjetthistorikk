"""Eksport kan kjøres uten ny innlesning eller nettilgang."""

import argparse
import json
import sqlite3
from pathlib import Path

from . import export_excel, export_revision_excel
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
    parser.add_argument("--excel", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        calculation_id: str | None = None
        if arguments.utvalg:
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
        else:
            export_excel(arguments.database, arguments.kjoring, arguments.excel)
    except (OSError, ValueError, TypeError, sqlite3.Error) as error:
        print(json.dumps({"status": "eksportfeil", "feil": str(error)}))
        return 1
    result = {"status": "eksportert", "fil": str(arguments.excel)}
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
