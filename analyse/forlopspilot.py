"""T3: konto/2024 og dokumenter fra samme frosne kildegrunnlag. Ingen database."""

import argparse
import json
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning.forlopspilot import import_basis as import_sources
from innlesning.forlopspilot import validate_basis as validate_sources
from innlesning.forlopspilot_model import FORMAT, Basis, Calculation, Report
from innlesning.observations import AmountObservation, encode
from innlesning.omtale import identified
from innlesning.visningspilot_model import PilotBasis, PilotSelection, TreatmentContext

from . import visningspilot as t1
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


def calculate_path(
    observations: tuple[AmountObservation, ...],
    contexts: tuple[TreatmentContext, ...],
    *,
    account: str,
    absence_ids: tuple[str, ...] = (),
) -> Calculation:
    """Offentlig avgrenset regneport; kildeverifisert rapport rekonstrurerer inngangene."""
    ctx = {c.observation_id: c for c in contexts}
    chosen = tuple(
        o
        for o in observations
        if f"{o.chapter}/{o.post}" == account and o.figure_type == "stortingsvedtak"
    )
    reason = ""
    values: dict[tuple[str, str], AmountObservation] = {}
    for o in chosen:
        c = ctx.get(o.id)
        if not c or c.status != "kildeverifisert" or not c.evidence_ids:
            reason = "manglende kildebelagt behandlingsgrunnlag"
            break
        if (
            c.stage != "vedtak"
            or c.actor != "stortinget"
            or o.proposal_role is not None
            or (
                o.round != c.round
                and not (
                    o.round == "uavklart"
                    and o.source_system == "storting"
                    and c.round == "nysaldering"
                )
            )
            or c.round == "uavklart"
        ):
            reason = "uforenlig rolle eller behandlingsrunde"
            break
        if (
            o.budget_year != 2024
            or o.currency != "NOK"
            or o.multiplier != "1"
            or o.detail_level != "post"
            or o.scope != "enkeltledd"
            or o.subpost is not None
            or o.information_type != "bevilgning"
            or o.amount_kr is None
        ):
            reason = "uforenlig år/enhet/konto/betydning/omfang eller manglende verdi"
            break
        key = (c.round, o.meaning)
        if key in values:
            reason = "tvetydig kildefelt i behandlingsrunde"
            break
        values[key] = o
    rounds = ("rnb", "nysaldering") if account == "1429/1" else ("nysaldering",)
    required = (("opprinnelig", "nivaa"),) + tuple(
        (r, meaning) for r in rounds for meaning in ("for_belop", "endring", "etter_belop")
    )
    if not reason and (account not in {"1429/1", "1429/22"} or set(values) != set(required)):
        reason = "manglende eller uventet start/delta/kontrollfelt"
    if not reason and account == "1429/22" and not absence_ids:
        reason = "manglende avgrenset 857-/22-fraværsbevis"
    inputs, checks = [], list(absence_ids)
    amount = observed = None
    if not reason:
        initial = values[("opprinnelig", "nivaa")]
        amount = initial.amount_kr
        inputs.append(initial.id)
        date = initial.decision_date or ""
        for round in rounds:
            before, delta, after = (
                values[(round, m)] for m in ("for_belop", "endring", "etter_belop")
            )
            inputs.append(delta.id)
            checks.extend((before.id, after.id))
            observed = after.amount_kr
            assert amount is not None and before.amount_kr is not None
            assert delta.amount_kr is not None and observed is not None
            if (
                not date
                or not delta.decision_date
                or date >= delta.decision_date
                or before.decision_date != delta.decision_date
                or after.decision_date != delta.decision_date
                or len({before.step_id, delta.step_id, after.step_id}) != 1
            ):
                reason = "motstridende hendelse eller kronologisk rekkefølge"
                break
            if amount != before.amount_kr or before.amount_kr + delta.amount_kr != observed:
                reason = "motstridende før/etter-kontroll i " + round
                break
            amount += delta.amount_kr
            date = delta.decision_date
        if amount is not None and abs(amount) > 9_007_199_254_740_991:
            reason = "resultat utenfor Excel-eksakt heltall"
    if reason:
        amount = None
    return identified(
        "forlopskontroll-1",
        Calculation(
            "",
            account,
            2024,
            "startnivaa-pluss-vedtatte-deltaer-1",
            "sperret" if reason else "avgrenset kontroll",
            reason or "Valgt lokal regning; ingen godkjent årsbalanse eller helårsdekning",
            tuple(inputs),
            tuple(checks),
            amount,
            observed,
        ),
    )


def build_report(
    basis: Basis, selection: PilotSelection, *, return_selection: PilotSelection | None = None
) -> Report:
    validate_basis(basis)
    data = contents(basis)
    t1.validate_selection(selection, data)
    if return_selection is not None:
        t1.validate_selection(return_selection, data)
    view = t1._view(data, selection)
    # Stadiesammenligning gjelder nysaldering; nye runder er ikke nye forslagstadier.
    calculations = []
    for post in ("1", "22"):
        account = "1429/" + post
        if any(o.id in view.adopted_observation_ids and o.post == post for o in data.observations):
            absence = tuple(
                s.id
                for s in basis.statements
                if s.role == "857_1429_22_fravaer_kun_tr822_830_for_1432"
            )
            calculations.append(
                calculate_path(
                    data.observations,
                    data.contexts,
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
        raise ValueError("T3-rapporten avviker fra kilder/utvalgs-/regneregler")
    raw = encode({"format": FORMAT, "report": asdict(report)})
    if len(raw.encode("utf8")) > MAX_REPORT_BYTES:
        raise ValueError("T3-rapport overstiger 64 MiB")
    return raw


def report_from_json(raw: str) -> Report:
    if len(raw.encode("utf8")) > MAX_REPORT_BYTES:
        raise ValueError("T3-rapport overstiger 64 MiB")
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        if (
            not isinstance(data, dict)
            or set(data) != {"format", "report"}
            or data["format"] != FORMAT
        ):
            raise ValueError("Ukjent T3-konvolutt")
        report: Report = _decode(Report, data["report"])
        if encode(asdict(report)) != encode(data["report"]):
            raise ValueError("T3-felter endres ved type-/nullgrunnskontroll")
        report_to_json(report)
        return report
    except (TypeError, KeyError, RecursionError) as error:
        raise ValueError("Ugyldig T3-rapport") from error


def read_json(path: Path) -> Report:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("T3-rapport overstiger 64 MiB")
    return report_from_json(raw.decode("utf8"))


def export_json(report: Report, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".json":
        raise ValueError("Velg nytt T3-JSON-filnavn")
    raw = report_to_json(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw.encode("utf8"))
        if read_json(temporary) != report:
            raise ValueError("Skrevet T3-JSON avviker")
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
            raise ValueError("Frosset T3 har allerede sitt tidligere grunnlag")
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
        from .forlopspilot_excel import export_originals, export_pair

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
