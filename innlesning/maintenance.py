"""Offentlig B5-CLI: python -m innlesning.maintenance --help."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .controls import (
    activate_basis,
    control_report,
    define_control_basis,
    export_controls,
    import_controls,
    read_decision,
    read_evidence,
    store_evidence,
)
from .maintenance_store import read_import
from .observations import Interpretation, extract_revision
from .registers import (
    export_register,
    import_register,
    read_current_register,
    read_register,
    seed_register,
)
from .workfiles import safe_output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="B5 registervedlikehold og faglig kontroll")
    parser.add_argument("--database", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("register-seed", help="Lagre dokumentert startgrunnlag; ingen godkjenning")
    commands.add_parser(
        "register-head", help="Les gjeldende publisert register; aktiverer ikke kontrollgrunnlag"
    )
    export = commands.add_parser("register-export")
    export.add_argument("--snapshot", required=True)
    export.add_argument("--output", type=Path, required=True)
    for name in ("register-import", "control-import"):
        commands.add_parser(name).add_argument("--input", type=Path, required=True)
    commands.add_parser("register-read").add_argument("--snapshot", required=True)
    commands.add_parser("import-read").add_argument("--id", required=True)
    commands.add_parser("control-read").add_argument("--id", required=True)
    commands.add_parser("evidence-read").add_argument("--id", required=True)
    proof = commands.add_parser("evidence-add")
    proof.add_argument("--input", type=Path, required=True)
    for field in ("version", "locator", "url"):
        proof.add_argument(f"--{field}", required=True)
    proof.add_argument("--parent-sha256")
    commands.add_parser("basis-define").add_argument("--description", required=True)
    activate = commands.add_parser("basis-activate")
    control_export = commands.add_parser("control-export")
    process = commands.add_parser("reprocess")
    for command in (activate, control_export, process):
        command.add_argument("--extraction", action="append", required=True)
        command.add_argument("--register", required=True)
        command.add_argument("--control", required=True)
    control_export.add_argument("--output", type=Path, required=True)
    control_export.add_argument("--observation", action="append")
    process.add_argument("--selection", type=Path, help="JSON for eksplisitt HistorySelection")
    process.add_argument("--output", type=Path, help="Eksporter kontrollert resultat til Excel")
    report = commands.add_parser("control-report")
    report.add_argument("--extraction", action="append", required=True)
    reinterpret = commands.add_parser(
        "reinterpret", help="Ny immutable v2-tolkning; aktiverer ikke"
    )
    reinterpret.add_argument("--revision", required=True)
    reinterpret.add_argument("--register", required=True)
    commands.add_parser("controlled-read").add_argument("--id", required=True)
    controlled_export = commands.add_parser("controlled-export")
    controlled_export.add_argument("--id", required=True)
    controlled_export.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    database = args.database
    result: Any
    try:
        if args.command in {"reprocess", "controlled-export"}:
            paths = [database.resolve()]
            if args.command == "reprocess" and args.selection:
                paths.append(args.selection.resolve())
            if args.output:
                paths.append(args.output.resolve())
            if len(set(paths)) != len(paths):
                raise ValueError("Database, Excel og utvalgsfil må ha forskjellige baner")
            if args.output:
                if args.output.suffix.lower() != ".xlsx":
                    raise ValueError("Kontrollert resultat krever .xlsx som utformat")
                safe_output(database, args.output)
        match args.command:
            case "register-seed":
                snapshot = seed_register(database)
                result = {"snapshot_id": snapshot.id, **asdict(snapshot)}
            case "register-export":
                result = {"export_id": export_register(database, args.snapshot, args.output)}
            case "register-import":
                result = asdict(import_register(database, args.input))
            case "register-read":
                snapshot = read_register(database, args.snapshot)
                result = {"snapshot_id": snapshot.id, **asdict(snapshot)}
            case "register-head":
                snapshot = read_current_register(database)
                result = {"snapshot_id": snapshot.id, **asdict(snapshot)}
            case "import-read":
                result = asdict(read_import(database, args.id))
            case "control-read":
                result = asdict(read_decision(database, args.id))
            case "evidence-read":
                result = asdict(read_evidence(database, args.id))
            case "evidence-add":
                result = asdict(
                    store_evidence(
                        database,
                        args.input,
                        version=args.version,
                        locator=args.locator,
                        role="kontrollkilde",
                        url=args.url,
                        parent_sha256=args.parent_sha256,
                    )
                )
            case "basis-define":
                result = {"control_basis": define_control_basis(database, args.description)}
            case "basis-activate":
                result = {
                    "activation_generations": activate_basis(
                        database, tuple(args.extraction), args.register, args.control
                    )
                }
            case "control-export":
                result = {
                    "export_id": export_controls(
                        database,
                        tuple(args.extraction),
                        args.output,
                        register_snapshot=args.register,
                        control_basis=args.control,
                        observation_ids=tuple(args.observation) if args.observation else None,
                    )
                }
            case "control-import":
                result = asdict(import_controls(database, args.input))
            case "control-report":
                result = control_report(database, tuple(args.extraction))
            case "reinterpret":
                extraction = extract_revision(
                    database,
                    args.revision,
                    interpretation=Interpretation(
                        adapter_version="storting-belop-v2", register_snapshot=args.register
                    ),
                )
                result = {
                    "extraction_id": extraction.id,
                    "interpretation_id": extraction.interpretation.id,
                }
            case "reprocess":
                from analyse.controlled import export_controlled_excel, reprocess_controlled
                from analyse.history import HistorySelection

                selection = None
                if args.selection:
                    data = json.loads(args.selection.read_text(encoding="utf-8"))
                    data["extraction_ids"] = tuple(data["extraction_ids"])
                    data["step_order"] = tuple(data.get("step_order", ()))
                    selection = HistorySelection(**data)
                processed = reprocess_controlled(
                    database,
                    tuple(args.extraction),
                    args.register,
                    args.control,
                    selection=selection,
                )
                if args.output:
                    export_controlled_excel(database, processed.id, args.output)
                result = asdict(processed)
            case "controlled-read":
                from analyse.controlled import read_controlled

                result = asdict(read_controlled(database, args.id))
            case "controlled-export":
                from analyse.controlled import export_controlled_excel

                export_controlled_excel(database, args.id, args.output)
                result = {"result_id": args.id, "output": str(args.output)}
            case _:
                raise ValueError("Ukjent kommando")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if isinstance(result, dict) and result.get("errors") else 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
