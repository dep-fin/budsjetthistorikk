"""P2: avgrenset R2-tillegg i begge innganger, også fra frosne filer offline."""

import argparse
import json
from dataclasses import asdict, replace
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning import perioderegister_r2 as source
from innlesning.fleraarspilot_model import Report as MonetaryReport
from innlesning.observations import encode
from innlesning.omtale import identified
from innlesning.perioderegister_model import Report as P1Report
from innlesning.perioderegister_r2_model import FORMAT, Basis, Report, View
from innlesning.visningspilot_model import PilotBasis, PilotSelection

from . import fleraarspilot as t4
from . import perioderegister as p1
from . import visningspilot as t1
from .komitepilot import legacy_payloads, legacy_report
from .saksdokumenter import _publish
from .session_serialization import _constant, _decode, _object

MAX_REPORT_BYTES = 64 * 1024 * 1024


def import_basis(root: Path, *, t1_json: str = "") -> Basis:
    old = legacy_report(t1_json)
    return source.import_basis(
        root,
        p1.import_basis(root, t1_json=t1_json),
        legacy_payloads(t1_json),
        old.basis if old else None,
    )


@lru_cache(maxsize=2)
def contents(basis: Basis) -> PilotBasis:
    old = p1.contents(basis.p1_basis)
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
    p1.validate_basis(basis.p1_basis)
    old = legacy_report(basis.p1_basis.t4_basis.legacy_json)
    source.validate_basis(
        basis, legacy_payloads(basis.p1_basis.t4_basis.legacy_json), old.basis if old else None
    )


def p1_report(basis: Basis, selection: PilotSelection) -> P1Report:
    if selection.mode == "document" and selection.document_id not in {
        d.id for d in p1.contents(basis.p1_basis).documents
    }:
        selection = PilotSelection()
    return p1.build_report(basis.p1_basis, selection)


def monetary_report(basis: Basis, selection: PilotSelection) -> MonetaryReport:
    report = p1_report(basis, selection)
    return p1.monetary_report(basis.p1_basis, report.selection)


def build_report(
    basis: Basis, selection: PilotSelection, *, return_selection: PilotSelection | None = None
) -> Report:
    validate_basis(basis)
    data = contents(basis)
    t1.validate_selection(selection, data)
    if return_selection is not None:
        t1.validate_selection(return_selection, data)
    old = p1_report(basis, selection)
    docs = {d.id: d.key for d in data.documents}
    document_key = docs.get(selection.document_id or "", "")
    extra = {
        "forslag23887": {"PROP-I", "PROP-II", "KOMITE", "BEHANDLING"},
        "votering23887": {"BEHANDLING", "D230", "D231"},
        "inns90": {"FULLMAKT429"},
        "forslag23945": {"FULLMAKT429"},
        "votering23945": {"FULLMAKT429"},
    }.get(document_key, set())
    post1 = 2024 in selection.years and (
        "1429" in selection.chapters or ("1429", "1") in selection.accounts
    )
    post22 = 2024 in selection.years and (
        "1429" in selection.chapters or ("1429", "22") in selection.accounts
    )
    finding_ids = tuple(
        f.id
        for f in basis.findings
        if (
            f.document_id == selection.document_id or f.key in extra
            if selection.mode == "document"
            else post1 and f.key != "INDEX" or (post1 or post22) and f.key == "O1-OMDISPONERING"
        )
    )
    documents = tuple(
        dict.fromkeys(
            old.view.document_ids
            + (
                (selection.document_id,)
                if selection.mode == "document" and selection.document_id
                else ()
            )
            + tuple(f.document_id for f in basis.findings if f.id in finding_ids)
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
                old.view,
                finding_ids,
                documents,
                tuple(s.id for s in basis.status_updates),
                tuple(c.id for c in basis.cross_references),
            ),
            old.calculations,
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
        raise ValueError("P2-rapporten avviker fra kilder/utvalg/global dekning")
    raw = encode({"format": FORMAT, "report": asdict(report)})
    if len(raw.encode()) > MAX_REPORT_BYTES:
        raise ValueError("P2-rapport overstiger 64 MiB")
    return raw


def report_from_json(raw: str) -> Report:
    if len(raw.encode()) > MAX_REPORT_BYTES:
        raise ValueError("P2-rapport overstiger 64 MiB")
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        if (
            not isinstance(data, dict)
            or set(data) != {"format", "report"}
            or data["format"] != FORMAT
        ):
            raise ValueError("Ukjent P2-konvolutt")
        report: Report = _decode(Report, data["report"])
        if encode(asdict(report)) != encode(data["report"]):
            raise ValueError("P2-felt endres ved type-/nullkontroll")
        report_to_json(report)
        return report
    except (TypeError, KeyError, RecursionError) as error:
        raise ValueError("Ugyldig P2-rapport") from error


def read_json(path: Path) -> Report:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("P2-rapport overstiger 64 MiB")
    return report_from_json(raw.decode())


def export_json(report: Report, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".json":
        raise ValueError("Velg nytt P2-JSON-filnavn")
    raw = report_to_json(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw.encode())
        if read_json(temporary) != report:
            raise ValueError("Skrevet P2-JSON avviker")
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
            raise ValueError("Frosset P2 har allerede sitt tidligere grunnlag")
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
        from .perioderegister_r2_excel import export_originals, export_pair

        export_pair(report, args.json, args.excel)
        if args.originaler:
            export_originals(report, args.originaler)
        print(
            encode(
                {
                    "report_id": report.id,
                    "basis_id": basis.id,
                    "monetary_events": len(report.view.p1.monetary.adopted_event_ids),
                    "issues": basis.issues,
                }
            )
        )
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
