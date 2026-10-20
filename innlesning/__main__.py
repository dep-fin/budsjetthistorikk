"""Analytikerens CLI: ett vedtak, valgfritt lagret respons, SQLite og Excel."""

import argparse
import json
import sqlite3
from pathlib import Path

from . import fetch_session, import_saved, read_report
from .ingestion import MAX_BYTES, START_SESSION, session_url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("hent", help="Hent eller les én kilde og velg ett vedtak")
    command.add_argument("--vedtak-id", required=True)
    command.add_argument("--sesjon", default=START_SESSION)
    command.add_argument("--historisk-proeve", action="store_true")
    command.add_argument("--database", type=Path, required=True)
    command.add_argument("--excel", type=Path)
    command.add_argument("--response", type=Path, help="Lagret XML-respons, offline")
    command.add_argument(
        "--metadata", type=Path, help="Hentemetadata med URL, tid, hash og byteantall"
    )
    command.add_argument("--timeout", type=int, default=30, help="HTTP-timeout, 1–120 sekunder")
    arguments = parser.parse_args()
    try:
        url = session_url(arguments.sesjon)
        if arguments.sesjon < START_SESSION and not arguments.historisk_proeve:
            raise ValueError("Eldre sesjon krever --historisk-proeve")
        if bool(arguments.response) != bool(arguments.metadata):
            raise ValueError("--response og --metadata må gis sammen")
        paths = [arguments.database, arguments.excel, arguments.response, arguments.metadata]
        resolved = [path.resolve() for path in paths if path is not None]
        if len(set(resolved)) != len(resolved):
            raise ValueError("Database, Excel og kildefiler må ha forskjellige baner")
        if arguments.response:
            with arguments.response.open("rb") as handle:
                raw = handle.read(MAX_BYTES + 1)
            metadata = json.loads(arguments.metadata.read_text(encoding="utf-8"))
            if not isinstance(metadata, dict) or metadata.get("url") != url:
                raise ValueError("Hentemetadata må være et objekt med valgt sesjons URL")
        else:
            raw, metadata = fetch_session(arguments.sesjon, timeout=arguments.timeout)
        run_id = import_saved(
            arguments.database,
            raw,
            metadata,
            arguments.vedtak_id,
            historical_sample=arguments.historisk_proeve,
        )
        report = read_report(arguments.database, run_id)
        if arguments.excel:
            from analyse import export_excel

            export_excel(arguments.database, run_id, arguments.excel)
        print(
            json.dumps(
                {
                    "kjoring": run_id,
                    "status": report.status,
                    "antall_postlinjer": len(report.lines),
                    "kildeversjon": report.source_sha256,
                    "kontrollbehov": report.controls,
                    "omfang": "Bare valgt vedtak; ingen komplett sesjons- eller historikkdekning",
                    "departement": "uavklart; register inngår ikke i B1",
                    "historisk_proeve": report.historical_sample,
                }
            )
        )
        return {"strukturert": 0, "til kontroll": 2, "innlesningsfeil": 1}[report.status]
    except (OSError, ValueError, sqlite3.Error) as error:
        print(json.dumps({"status": "innlesningsfeil", "feil": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
