"""P1: samme delvise register i dokument- og konto-/årsinngangen, også offline."""

import argparse
import json
from dataclasses import asdict, replace
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning import perioderegister as source
from innlesning.fleraarspilot_model import Report as MonetaryReport
from innlesning.observations import encode
from innlesning.omtale import identified
from innlesning.perioderegister_model import FORMAT, Basis, Report, View
from innlesning.visningspilot_model import PilotBasis, PilotSelection

from . import fleraarspilot as t4
from . import visningspilot as t1
from .komitepilot import legacy_payloads, legacy_report
from .saksdokumenter import _publish
from .session_serialization import _constant, _decode, _object

MAX_REPORT_BYTES = 64 * 1024 * 1024


def import_basis(root: Path, *, t1_json: str = "") -> Basis:
    old = legacy_report(t1_json)
    return source.import_basis(
        root,
        t4.import_basis(root, t1_json=t1_json),
        legacy_payloads(t1_json),
        old.basis if old else None,
    )


@lru_cache(maxsize=2)
def contents(basis: Basis) -> PilotBasis:
    old = t4.contents(basis.t4_basis)
    # Unionen lever bare i minnet. Ingen ekstra gamle objekter serialiseres.
    return replace(
        old,
        id=basis.id,
        rule=basis.rule,
        documents=old.documents + basis.documents,
        inventory=old.inventory + basis.inventory,
        statements=old.statements + basis.statements,
        relations=old.relations + basis.relations,
        issues=old.issues + basis.issues,
    )


def validate_basis(basis: Basis) -> None:
    t4.validate_basis(basis.t4_basis)
    old = legacy_report(basis.t4_basis.legacy_json)
    source.validate_basis(
        basis, legacy_payloads(basis.t4_basis.legacy_json), old.basis if old else None
    )


def monetary_report(basis: Basis, selection: PilotSelection) -> MonetaryReport:
    old = t4.contents(basis.t4_basis)
    if selection.mode == "document":
        if selection.document_id in {d.id for d in old.documents}:
            result = t4.build_report(basis.t4_basis, selection)
            # Hele dokumentinventaret består, mens P1s beløpsomfang er 2024.
            ids = {
                o.id
                for o in old.observations
                if o.budget_year == 2024 and o.chapter == "1429" and o.post in {"1", "22"}
            }
            view = result.view
            kept = tuple(i for i in view.observation_ids if i in ids)
            adopted = tuple(i for i in view.adopted_observation_ids if i in ids)
            events = tuple(dict.fromkeys(o.step_id for o in old.observations if o.id in adopted))
            return replace(
                result,
                view=replace(
                    view,
                    observation_ids=kept,
                    adopted_observation_ids=adopted,
                    adopted_event_ids=events,
                ),
            )
        return t4.build_report(basis.t4_basis, PilotSelection())
    years = (2024,) if 2024 in selection.years else ()
    accounts = tuple(a for a in selection.accounts if a in {("1429", "1"), ("1429", "22")})
    if "1429" in selection.chapters:
        accounts = tuple(dict.fromkeys(accounts + (("1429", "1"), ("1429", "22"))))
    return t4.build_report(basis.t4_basis, PilotSelection(years=years, accounts=accounts))


def build_report(
    basis: Basis, selection: PilotSelection, *, return_selection: PilotSelection | None = None
) -> Report:
    validate_basis(basis)
    data = contents(basis)
    t1.validate_selection(selection, data)
    if return_selection is not None:
        t1.validate_selection(return_selection, data)
    monetary = monetary_report(basis, selection)
    entries = tuple(
        e.id
        for e in basis.entries
        if (
            e.document_id == selection.document_id
            if selection.mode == "document"
            else e.post_link == "proven_selected"
            and e.budget_year in selection.years
            and any(
                account.split("/")[0] in selection.chapters
                or tuple(account.split("/")) in selection.accounts
                for account in e.accounts
            )
        )
    )
    documents = tuple(
        dict.fromkeys(
            (
                (selection.document_id,)
                if selection.mode == "document" and selection.document_id
                else ()
            )
            + tuple(e.document_id for e in basis.entries if e.id in entries)
            + monetary.view.document_ids
        )
    )
    return identified(
        FORMAT,
        Report(
            "",
            basis,
            selection,
            return_selection,
            View(
                monetary.view,
                entries,
                documents,
                tuple(c.id for c in basis.case_candidates),
                tuple(c.id for c in basis.decision_candidates),
                tuple(g.id for g in basis.gaps),
            ),
            monetary.calculations,
        ),
    )


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
        raise ValueError("P1-rapporten avviker fra kilder/utvalg/global dekning")
    raw = encode({"format": FORMAT, "report": asdict(report)})
    if len(raw.encode()) > MAX_REPORT_BYTES:
        raise ValueError("P1-rapport overstiger 64 MiB")
    return raw


def report_from_json(raw: str) -> Report:
    if len(raw.encode()) > MAX_REPORT_BYTES:
        raise ValueError("P1-rapport overstiger 64 MiB")
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        if (
            not isinstance(data, dict)
            or set(data) != {"format", "report"}
            or data["format"] != FORMAT
        ):
            raise ValueError("Ukjent P1-konvolutt")
        report: Report = _decode(Report, data["report"])
        if encode(asdict(report)) != encode(data["report"]):
            raise ValueError("P1-felt endres ved type-/nullkontroll")
        report_to_json(report)
        return report
    except (TypeError, KeyError, RecursionError) as error:
        raise ValueError("Ugyldig P1-rapport") from error


def read_json(path: Path) -> Report:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("P1-rapport overstiger 64 MiB")
    return report_from_json(raw.decode())


def export_json(report: Report, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".json":
        raise ValueError("Velg nytt P1-JSON-filnavn")
    raw = report_to_json(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw.encode())
        if read_json(temporary) != report:
            raise ValueError("Skrevet P1-JSON avviker")
        _publish(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rot", type=Path, default=Path("."))
    parser.add_argument("--t1", type=Path, help="Én uendret validert T1-kapsel")
    parser.add_argument("--frosset", type=Path)
    parser.add_argument("--dokument")
    parser.add_argument("--aar", type=int, action="append", default=[])
    parser.add_argument("--konto", action="append", default=[])
    parser.add_argument("--kapittel", action="append", default=[])
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--excel", type=Path, required=True)
    parser.add_argument("--originaler", type=Path)
    args = parser.parse_args()
    try:
        if args.t1 and args.frosset:
            raise ValueError("Frosset P1 har allerede sitt tidligere grunnlag")
        previous = read_json(args.frosset) if args.frosset else None
        basis = (
            previous.basis
            if previous
            else import_basis(args.rot, t1_json=t4._read_legacy(args.t1) if args.t1 else "")
        )
        if args.dokument:
            if args.aar or args.konto or args.kapittel:
                raise ValueError("Dokumentvalg krever tomme kontofiltre")
            doc_id = next(
                (d.id for d in contents(basis).documents if d.key == args.dokument), args.dokument
            )
            selection = PilotSelection(mode="document", document_id=doc_id)
        else:
            pairs = tuple(tuple(x.split("/")) for x in args.konto)
            if any(len(x) != 2 for x in pairs):
                raise ValueError("Konto oppgis som kapittel/post")
            selection = PilotSelection(
                years=tuple(args.aar),
                chapters=tuple(args.kapittel),
                accounts=tuple((x[0], x[1]) for x in pairs),
            )
        report = (
            previous
            if previous and not (args.dokument or args.aar or args.konto or args.kapittel)
            else build_report(basis, selection)
        )
        from .perioderegister_excel import export_originals, export_pair

        export_pair(report, args.json, args.excel)
        if args.originaler:
            export_originals(report, args.originaler)
        print(
            encode(
                {
                    "report_id": report.id,
                    "basis_id": basis.id,
                    "monetary_events": len(report.view.monetary.adopted_event_ids),
                    "issues": basis.issues,
                }
            )
        )
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
