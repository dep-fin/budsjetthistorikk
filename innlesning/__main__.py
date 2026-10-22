"""Analytikerens CLI: ett vedtak, valgfritt lagret respons, SQLite og Excel."""

import argparse
import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from . import fetch_session, import_saved, read_report, read_sync, resume_sync, stage_sync
from .ingestion import MAX_BYTES, START_SESSION, session_url
from .observations import Interpretation, extract_revision
from .sync import SyncReport


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    documents_command = commands.add_parser(
        "saksdokumenter", help="B8: berik valgt vedtaksrevisjon med saksmetadata"
    )
    documents_command.add_argument("--database", type=Path, required=True)
    documents_command.add_argument("--revisjon", required=True)
    documents_command.add_argument("--response", type=Path)
    documents_command.add_argument("--metadata", type=Path)
    documents_command.add_argument("--timeout", type=int, default=30)
    interpretation_command = commands.add_parser(
        "tolk", help="B3: tolk én valgt B2-revisjon offline"
    )
    interpretation_command.add_argument("--database", type=Path, required=True)
    interpretation_command.add_argument("--revisjon", required=True)
    interpretation_command.add_argument(
        "--tolkning",
        required=True,
        help="Adapterversjon: storting-belop-v1 eller storting-belop-v2",
    )
    interpretation_command.add_argument(
        "--runde", choices=["opprinnelig", "rnb", "nysaldering", "ovrig", "uavklart"]
    )
    interpretation_command.add_argument(
        "--rundegrunnlag", help="Kildebevis for eksplisitt rundevalg"
    )
    for name in ("hent", "synkroniser"):
        command = commands.add_parser(
            name,
            help=(
                "B1-prøveimport av ett vedtak"
                if name == "hent"
                else "B2: sammenlign alle ID-er, eller ett uttrykkelig valgt vedtak"
            ),
        )
        command.add_argument(
            "--vedtak-id",
            required=name == "hent",
            help="Begrenser importomfanget til dette vedtaket",
        )
        command.add_argument("--sesjon", default=START_SESSION)
        command.add_argument("--historisk-proeve", action="store_true")
        command.add_argument("--database", type=Path, required=True)
        command.add_argument(
            "--excel", type=Path, help="Ett valgt vedtak; synkroniser krever --vedtak-id"
        )
        command.add_argument("--response", type=Path, help="Lagret XML-respons, offline")
        command.add_argument(
            "--metadata", type=Path, help="Hentemetadata med URL, tid, hash og byteantall"
        )
        command.add_argument("--timeout", type=int, default=30, help="HTTP-timeout, 1–120 sekunder")
        if name == "synkroniser":
            command.add_argument(
                "--forbered",
                action="store_true",
                help="Bevar råbyte og returner gjenopptaks-ID før publisering",
            )
    for name in ("gjenoppta", "rapport"):
        command = commands.add_parser(name, help="Bruk én lagret B2-jobb, uten nett")
        command.add_argument("--database", type=Path, required=True)
        command.add_argument("--kjoring", required=True)
    arguments = parser.parse_args()
    job_id: str | None = None
    try:
        if arguments.command == "saksdokumenter":
            from .saksdokumenter import enrich_revision, fetch_case_attempt, import_case_response
            from .sync import read_revision

            revision = read_revision(arguments.database, arguments.revisjon)
            decision = revision.report.decision
            if decision is None:
                raise ValueError("Saksberikelse krever bevart vedtak")
            if bool(arguments.response) != bool(arguments.metadata):
                raise ValueError("--response og --metadata må gis sammen")
            paths = [arguments.database, arguments.response, arguments.metadata]
            resolved = [p.resolve() for p in paths if p is not None]
            if len(set(resolved)) != len(resolved):
                raise ValueError("Database og kildefiler må ha forskjellige baner")
            if arguments.response:
                with arguments.response.open("rb") as handle:
                    raw = handle.read(MAX_BYTES + 1)
                if arguments.metadata.stat().st_size > 1024 * 1024:
                    raise ValueError("Hentemetadata overstiger 1 MiB")
                metadata = json.loads(arguments.metadata.read_text(encoding="utf-8-sig"))
                if not isinstance(metadata, dict):
                    raise ValueError("Hentemetadata må være et JSON-objekt")
                attempt = import_case_response(
                    arguments.database,
                    decision.case_id,
                    raw,
                    metadata,
                    dataset=revision.dataset,
                    session=decision.session,
                )
            else:
                attempt = fetch_case_attempt(
                    arguments.database,
                    decision.case_id,
                    dataset=revision.dataset,
                    session=decision.session,
                    timeout=arguments.timeout,
                )
            enrichment = enrich_revision(arguments.database, arguments.revisjon, attempt.id)
            print(
                json.dumps(
                    {
                        "status": attempt.status,
                        "saksforsok": attempt.id,
                        "saksberikelse": enrichment.id,
                        "avvik": enrichment.issues,
                        "feil": attempt.reason,
                    }
                )
            )
            return 0 if attempt.status == "observert" else 2
        if arguments.command == "tolk":
            interpretation = Interpretation(
                adapter_version=arguments.tolkning,
                round=arguments.runde,
                round_evidence=arguments.rundegrunnlag,
            )
            extraction = extract_revision(
                arguments.database, arguments.revisjon, interpretation=interpretation
            )
            print(
                json.dumps(
                    {
                        "status": "tolket",
                        "belopsuttrekk": extraction.id,
                        "tolkning": interpretation.id,
                        "observasjoner": len(extraction.observations),
                        "avvik": [asdict(issue) for issue in extraction.anomalies],
                        "dekningsgrense": "Bare valgt revisjon; ingen sesjonsgaranti",
                    }
                )
            )
            return 0
        if arguments.command in ("gjenoppta", "rapport"):
            job_id = str(arguments.kjoring)
            if arguments.command == "gjenoppta":
                resume_sync(arguments.database, job_id)
            return show_sync(read_sync(arguments.database, job_id))
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
        if arguments.command == "synkroniser":
            if arguments.excel and (not arguments.vedtak_id or arguments.forbered):
                raise ValueError("B2 --excel krever --vedtak-id og fullført publisering")
            job_id = stage_sync(
                arguments.database,
                raw,
                metadata,
                historical_sample=arguments.historisk_proeve,
                decision_id=arguments.vedtak_id,
            )
            if not arguments.forbered:
                resume_sync(arguments.database, job_id)
            sync = read_sync(arguments.database, job_id)
            if arguments.excel and sync.status == "fullfort":
                from analyse import export_revision_excel

                export_revision_excel(
                    arguments.database, sync.entries[0].revision_id, arguments.excel
                )
            return show_sync(sync)
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
        print(json.dumps({"status": "innlesningsfeil", "feil": str(error), "kjoring": job_id}))
        return 1
    except KeyboardInterrupt:
        print(
            json.dumps(
                {
                    "status": "avbrutt",
                    "kjoring": job_id,
                    "feil": "Gjenoppta lagret jobb; publiseringen er atomisk",
                }
            )
        )
        return 130


def show_sync(report: SyncReport) -> int:
    print(
        json.dumps(
            {
                "kjoring": report.job_id,
                "status": report.status,
                "datakontrakt": report.contract_version,
                "datasett": report.dataset,
                "sesjon": report.session,
                "omfang": report.scope,
                "kildeversjon": report.source_sha256,
                "hentemetadata": report.source_metadata,
                "responstid": report.response_time,
                "startet_utc": report.started_utc,
                "fullfort_utc": report.completed_utc,
                "fingeravtrykksmetode": report.fingerprint_version,
                "struktureringsversjon": report.parser_version,
                "antall": report.counts,
                "kontrollbehov": report.control_count,
                "feil": report.errors,
                "vedtak": [asdict(entry) for entry in report.entries],
                "dekningsgrense": (
                    "Kildeinventar; ingen garanti om komplett faglig strukturering "
                    "eller additiv historikk"
                ),
            }
        )
    )
    return 1 if report.status == "feilet" else 2 if report.control_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
