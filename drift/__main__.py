"""python -m drift --config eksplisitt.json. Ingen innebygd installasjon/credentials."""

import argparse
import json
import sqlite3
import sys
from datetime import UTC, date, datetime
from pathlib import Path

from .artifacts import publish_text
from .config import Config
from .locking import AlreadyRunning
from .runner import run_daily
from .schedule import next_due
from .store import read_daily
from .windows import task_xml


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Daglig kildeinnlesning kl. 06 Europe/Oslo")
    parser.add_argument("--config", required=True, type=Path)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--status", action="store_true")
    actions.add_argument("--next-due", action="store_true")
    actions.add_argument("--task-xml", type=Path)
    parser.add_argument("--python", type=Path)
    parser.add_argument("--working-directory", type=Path)
    parser.add_argument("--account")
    parser.add_argument("--start-date", type=date.fromisoformat)
    args = parser.parse_args(argv)
    try:
        if args.config.stat().st_size > 64 * 1024:
            raise ValueError("Konfigurasjon overstiger 64 KiB")
        data = json.loads(args.config.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("Konfigurasjon krever JSON-objekt")
        config = Config.from_dict(data)
        if args.next_due:
            print(json.dumps({"next_due": next_due(datetime.now(UTC)).isoformat()}))
            return 0
        if args.status:
            print(json.dumps(read_daily(config.database, config.pipeline_id), ensure_ascii=False))
            return 0
        if args.task_xml:
            if not all((args.python, args.working_directory, args.account, args.start_date)):
                raise ValueError(
                    "Task XML krever --python, --working-directory, --account, --start-date"
                )
            xml = task_xml(
                args.config.resolve(),
                args.python,
                args.working_directory,
                args.account,
                args.start_date,
            )
            if args.task_xml.resolve() == args.config.resolve():
                raise ValueError("Task XML kan ikke erstatte konfigurasjonen")
            publish_text(config.database, args.task_xml, xml)
            print(json.dumps({"task_xml": str(args.task_xml.resolve()), "registered": False}))
            return 0
        result = run_daily(config)
        print(json.dumps(result, ensure_ascii=False))
        return (
            0
            if result["outcome"] in ("full", "ikke_forfalt") and result["delivery"] != "venter"
            else 1
        )
    except AlreadyRunning:
        print(json.dumps({"outcome": "overlap_avvist"}))
        return 2
    except (OSError, ValueError, TypeError, KeyError, sqlite3.Error):
        # Feilmeldinger kan inneholde URL/token/kildeverdier: ingen råunntak i stdout.
        print(
            json.dumps(
                {
                    "outcome": "driftsfeil",
                    "detail": "Kontroller lokal konfigurasjon og driftsregister",
                }
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
