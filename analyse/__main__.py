"""Eksport kan kjøres uten ny innlesning eller nettilgang."""

import argparse
import json
import sqlite3
from pathlib import Path

from . import export_excel, export_revision_excel


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--kjoring", help="Eksakt lagret B1/B2-struktureringsresultat")
    selection.add_argument("--revisjon", help="Eksakt lagret B2-innholdsrevisjon")
    parser.add_argument("--excel", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        if arguments.revisjon:
            export_revision_excel(arguments.database, arguments.revisjon, arguments.excel)
        else:
            export_excel(arguments.database, arguments.kjoring, arguments.excel)
    except (OSError, ValueError, sqlite3.Error) as error:
        print(json.dumps({"status": "eksportfeil", "feil": str(error)}))
        return 1
    print(json.dumps({"status": "eksportert", "fil": str(arguments.excel)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
