"""T4: separate konto-/årsforløp og dokumenter fra ett frosset grunnlag."""

import argparse
import json
from dataclasses import asdict, replace
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning.fleraarspilot import import_basis as import_sources
from innlesning.fleraarspilot import validate_basis as validate_sources
from innlesning.fleraarspilot_model import FORMAT, Basis, Report
from innlesning.observations import encode
from innlesning.omtale import identified
from innlesning.visningspilot_model import PilotBasis, PilotSelection

from . import visningspilot as t1
from .forlopspilot import calculate_path
from .komitepilot import legacy_payloads, legacy_report
from .saksdokumenter import _publish
from .session_serialization import _constant, _decode, _object

MAX_REPORT_BYTES = 64 * 1024 * 1024


def import_basis(root: Path, *, t1_json: str = "") -> Basis:
    old = legacy_report(t1_json)
    return import_sources(
        root,
        legacy_json=t1_json,
        legacy=legacy_payloads(t1_json),
        previous=old.basis if old else None,
    )


@lru_cache(maxsize=3)
def contents(basis: Basis) -> PilotBasis:
    """ID-union bare i minnet; gamle objekter skrives aldri inn i ny basis."""
    old = legacy_report(basis.legacy_json)
    previous = old.basis if old else None
    return PilotBasis(
        basis.id,
        basis.rule,
        "",
        (),
        basis.documents + (previous.documents if previous else ()),
        basis.inventory + (previous.inventory if previous else ()),
        basis.statements + (previous.statements if previous else ()),
        basis.observations + (previous.observations if previous else ()),
        basis.relations + (previous.relations if previous else ()),
        basis.contexts + (previous.contexts if previous else ()),
        basis.issues + tuple("T1-kapsel: " + issue for issue in previous.issues)
        if previous
        else basis.issues,
    )


def validate_basis(basis: Basis) -> None:
    old = legacy_report(basis.legacy_json)
    validate_sources(basis, legacy_payloads(basis.legacy_json), old.basis if old else None)


def build_report(
    basis: Basis, selection: PilotSelection, *, return_selection: PilotSelection | None = None
) -> Report:
    validate_basis(basis)
    data = contents(basis)
    t1.validate_selection(selection, data)
    if return_selection is not None:
        t1.validate_selection(return_selection, data)
    view = t1._view(data, selection)
    # T1s stadiesammenligning gjelder bare 2024. Inventar fra 2025 må aldri
    # hente inn 2024-sammenligninger gjennom like kontokoder.
    if selection.mode == "document":
        compare_data = replace(
            data,
            inventory=tuple(
                i
                for i in data.inventory
                if i.document_id == selection.document_id and i.budget_year == 2024
            ),
        )
        compare_selection = selection
    else:
        compare_data = data
        compare_selection = replace(selection, years=tuple(y for y in selection.years if y == 2024))
    contexts = {c.observation_id: c for c in data.contexts}
    documents = {d.id: d for d in data.documents}
    ordered = sorted(
        (o for o in data.observations if o.id in view.observation_ids),
        key=lambda o: (
            o.budget_year or 0,
            int(o.chapter or "0"),
            int(o.post or "0"),
            documents[contexts[o.id].document_id].date,
            {"regjering": 0, "tilraading": 1, "vedtak": 2}.get(contexts[o.id].stage, 3),
            {"nivaa": 0, "for_belop": 1, "endring": 2, "etter_belop": 3}.get(o.meaning, 4),
        ),
    )
    adopted = [o for o in ordered if o.figure_type == "stortingsvedtak"]
    view = replace(
        view,
        observation_ids=tuple(o.id for o in ordered),
        adopted_observation_ids=tuple(o.id for o in adopted),
        adopted_event_ids=tuple(dict.fromkeys(o.step_id for o in adopted)),
        comparisons=t1._view(compare_data, compare_selection).comparisons,
    )
    # Stadiesammenligning gjelder nysaldering; nye runder er ikke nye forslagstadier.
    calculations = []
    for post in ("1", "22"):
        account = "1429/" + post
        if any(
            o.id in view.adopted_observation_ids and o.post == post and o.budget_year == 2024
            for o in data.observations
        ):
            absence = tuple(
                s.id
                for s in basis.statements
                if s.role == "857_1429_22_fravaer_kun_tr822_830_for_1432"
            )
            calculations.append(
                calculate_path(
                    tuple(o for o in data.observations if o.budget_year == 2024),
                    tuple(
                        c
                        for c in data.contexts
                        if c.observation_id
                        in {o.id for o in data.observations if o.budget_year == 2024}
                    ),
                    account=account,
                    absence_ids=absence if post == "22" else (),
                )
            )
    return identified(
        FORMAT, Report("", basis, selection, return_selection, view, tuple(calculations))
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
        raise ValueError("T4-rapporten avviker fra kilder/utvalgs-/regneregler")
    raw = encode({"format": FORMAT, "report": asdict(report)})
    if len(raw.encode("utf8")) > MAX_REPORT_BYTES:
        raise ValueError("T4-rapport overstiger 64 MiB")
    return raw


def report_from_json(raw: str) -> Report:
    if len(raw.encode("utf8")) > MAX_REPORT_BYTES:
        raise ValueError("T4-rapport overstiger 64 MiB")
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        if (
            not isinstance(data, dict)
            or set(data) != {"format", "report"}
            or data["format"] != FORMAT
        ):
            raise ValueError("Ukjent T4-konvolutt")
        report: Report = _decode(Report, data["report"])
        if encode(asdict(report)) != encode(data["report"]):
            raise ValueError("T4-felter endres ved type-/nullgrunnskontroll")
        report_to_json(report)
        return report
    except (TypeError, KeyError, RecursionError) as error:
        raise ValueError("Ugyldig T4-rapport") from error


def read_json(path: Path) -> Report:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("T4-rapport overstiger 64 MiB")
    return report_from_json(raw.decode("utf8"))


def export_json(report: Report, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".json":
        raise ValueError("Velg nytt T4-JSON-filnavn")
    raw = report_to_json(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw.encode("utf8"))
        if read_json(temporary) != report:
            raise ValueError("Skrevet T4-JSON avviker")
        _publish(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _read_legacy(path: Path) -> str:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("T1-visningsinput overstiger 64 MiB")
    return raw.decode("utf8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rot", type=Path, default=Path("."))
    parser.add_argument("--t1", type=Path, help="Én uendret validert T1-JSON-kapsel")
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
            raise ValueError("Frosset T4 har allerede sitt tidligere grunnlag")
        previous = read_json(args.frosset) if args.frosset else None
        basis = (
            previous.basis
            if previous
            else import_basis(args.rot, t1_json=_read_legacy(args.t1) if args.t1 else "")
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
        from .fleraarspilot_excel import export_originals, export_pair

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
