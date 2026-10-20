"""Eksport kan kjøres uten ny innlesning eller nettilgang."""

import argparse
import json
import sqlite3
from pathlib import Path

from . import export_excel


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--kjoring", required=True)
    parser.add_argument("--excel", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        export_excel(arguments.database, arguments.kjoring, arguments.excel)
    except (OSError, ValueError, sqlite3.Error) as error:
        print(json.dumps({"status": "eksportfeil", "feil": str(error)}))
        return 1
    print(json.dumps({"status": "eksportert", "fil": str(arguments.excel)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
