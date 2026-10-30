"""T5s opt-in analyseinngang. T1 er én uendret typet kapsel."""

import argparse
import json
from dataclasses import asdict, replace
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning import proposisjon16 as source
from innlesning.observations import encode
from innlesning.omtale import identified
from innlesning.proposisjon16_model import FORMAT, Basis, Report
from innlesning.visningspilot_model import PilotBasis, PilotSelection

from . import visningspilot as t1
from .saksdokumenter import _publish
from .session_serialization import _constant, _decode, _object

MAX_REPORT_BYTES = 64 * 1024 * 1024


def import_basis(t1_json: str, root: Path | None = None) -> Basis:
    old = t1.report_from_json(t1_json)
    return source.import_basis(old.basis, t1.source_input(old.basis.o2b_json), root or Path("."))


@lru_cache(maxsize=2)
def contents(basis: Basis) -> PilotBasis:
    """Kun minneunion, aldri en ekstra serialisert gammel beløps-/payloadkapsel."""
    return replace(
        basis.t1_basis,
        id=basis.id,
        rule=basis.rule,
        observations=basis.t1_basis.observations + basis.observations,
        contexts=basis.t1_basis.contexts + basis.contexts,
        issues=tuple(
            "historisk_T1:" + issue
            if issue.startswith(("prop16_delvis_strukturert:", "inns95_strukturering_ikke_levert:"))
            else issue
            for issue in basis.t1_basis.issues
        )
        + basis.issues,
    )


def validate_basis(basis: Basis) -> None:
    source.validate_basis(basis, t1.source_input(basis.t1_basis.o2b_json))


def build_report(
    basis: Basis, selection: PilotSelection, *, return_selection: PilotSelection | None = None
) -> Report:
    validate_basis(basis)
    data = contents(basis)
    t1.validate_selection(selection, data)
    if return_selection is not None:
        t1.validate_selection(return_selection, data)
    view = t1._view(data, selection)
    if selection.mode == "accounts":
        # T1s historiske dokumentreferanse hadde videre kontekstopplisting.
        # T5s aktive kontoomfang følger bare eksplisitte tabell-/fullmaktsgrener.
        sister_id = next(d.id for d in data.documents if d.key == "inns95")
        active = 2024 in selection.years and any(
            account.split("/")[0] in selection.chapters
            or tuple(account.split("/")) in selection.accounts
            for branch in basis.branches
            if branch.case_id == "100889"
            for account in branch.accounts
        )
        if not active:
            sister_statements = {s.id for s in data.statements if s.document_id == sister_id}
            view = replace(
                view,
                document_ids=tuple(d for d in view.document_ids if d != sister_id),
                statement_ids=tuple(s for s in view.statement_ids if s not in sister_statements),
            )
        elif sister_id not in view.document_ids:
            view = replace(view, document_ids=tuple(sorted((*view.document_ids, sister_id))))
    return identified(FORMAT, Report("", basis, selection, return_selection, view))


def open_document(report: Report, document_id: str) -> Report:
    return build_report(
        report.basis,
        PilotSelection(mode="document", document_id=document_id),
        return_selection=report.selection,
    )


def open_accounts(report: Report, selection: PilotSelection) -> Report:
    if selection.mode != "accounts":
        raise ValueError("Velg konto-/årsinngang")
    return build_report(report.basis, selection, return_selection=report.selection)


def go_back(report: Report) -> Report:
    if report.return_selection is None:
        raise ValueError("Ingen tidligere inngang")
    return build_report(report.basis, report.return_selection)


def report_to_json(report: Report) -> str:
    if report != build_report(
        report.basis, report.selection, return_selection=report.return_selection
    ):
        raise ValueError("T5-rapport avviker fra originaler, utvalg eller global dekning")
    raw = encode({"format": FORMAT, "report": asdict(report)})
    if len(raw.encode()) > MAX_REPORT_BYTES:
        raise ValueError("T5-rapport overstiger 64 MiB")
    return raw


def report_from_json(raw: str) -> Report:
    if len(raw.encode()) > MAX_REPORT_BYTES:
        raise ValueError("T5-rapport overstiger 64 MiB")
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        if (
            not isinstance(data, dict)
            or set(data) != {"format", "report"}
            or data["format"] != FORMAT
        ):
            raise ValueError("Ukjent T5-konvolutt")
        report: Report = _decode(Report, data["report"])
        if encode(asdict(report)) != encode(data["report"]):
            raise ValueError("T5-felt endres ved type-/nullkontroll")
        report_to_json(report)
        return report
    except (TypeError, KeyError, RecursionError) as error:
        raise ValueError("Ugyldig T5-rapport") from error


def read_json(path: Path) -> Report:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("T5-rapport overstiger 64 MiB")
    return report_from_json(raw.decode("utf8"))


def export_json(report: Report, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".json":
        raise ValueError("Velg nytt T5-JSON-filnavn")
    raw = report_to_json(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw.encode("utf8"))
        if read_json(temporary) != report:
            raise ValueError("Skrevet T5-JSON avviker")
        _publish(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    origin = parser.add_mutually_exclusive_group(required=True)
    origin.add_argument("--t1", type=Path)
    origin.add_argument("--frosset", type=Path)
    parser.add_argument("--rot", type=Path, default=Path("."))
    parser.add_argument("--dokument")
    parser.add_argument("--aar", type=int, action="append", default=[])
    parser.add_argument("--kapittel", action="append", default=[])
    parser.add_argument("--konto", action="append", default=[])
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--excel", type=Path, required=True)
    parser.add_argument("--originaler", type=Path)
    args = parser.parse_args()
    try:
        previous = read_json(args.frosset) if args.frosset else None
        if previous:
            basis = previous.basis
        else:
            old = t1.read_json(args.t1)
            basis = source.import_basis(old.basis, t1.source_input(old.basis.o2b_json), args.rot)
        if args.dokument:
            if args.aar or args.kapittel or args.konto:
                raise ValueError("Dokumentvalg har ingen konto-/årsfiltre")
            document_id = next(
                (d.id for d in basis.t1_basis.documents if d.key == args.dokument), args.dokument
            )
            selection = PilotSelection(mode="document", document_id=document_id)
        else:
            accounts = []
            for pair in args.konto:
                pieces = pair.split("/")
                if len(pieces) != 2:
                    raise ValueError("Konto oppgis som kapittel/post")
                accounts.append((pieces[0], pieces[1]))
            selection = PilotSelection(
                years=tuple(args.aar), chapters=tuple(args.kapittel), accounts=tuple(accounts)
            )
        report = (
            previous
            if previous and not (args.dokument or args.aar or args.kapittel or args.konto)
            else build_report(basis, selection)
        )
        from .proposisjon16_excel import export_originals, export_pair

        export_pair(report, args.json, args.excel)
        if args.originaler:
            export_originals(report, args.originaler)
        print(
            encode(
                {
                    "report_id": report.id,
                    "basis_id": basis.id,
                    "fields": len(report.view.observation_ids),
                    "issues": basis.issues,
                }
            )
        )
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
