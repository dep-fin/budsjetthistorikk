"""T2: selvstendige 315/78-innganger og valgfri, validert T1-union. Ingen database."""

import argparse
import json
from dataclasses import asdict, replace
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning.komitepilot import LegacyPayloads
from innlesning.komitepilot import import_basis as import_sources
from innlesning.komitepilot import validate_basis as validate_sources
from innlesning.komitepilot_model import FORMAT, Basis, Report
from innlesning.observations import AmountObservation, encode
from innlesning.omtale import identified, source_bytes
from innlesning.visningspilot import raw_source
from innlesning.visningspilot_model import (
    PilotBasis,
    PilotReport,
    PilotSelection,
    PilotView,
    StageComparison,
    TreatmentContext,
)

from . import visningspilot as t1
from .saksdokumenter import _publish
from .session_serialization import _constant, _decode, _object

MAX_REPORT_BYTES = 64 * 1024 * 1024


@lru_cache(maxsize=2)
def legacy_report(raw: str) -> PilotReport | None:
    return t1.report_from_json(raw) if raw else None


@lru_cache(maxsize=2)
def legacy_payloads(raw: str) -> LegacyPayloads:
    old = legacy_report(raw)
    if old is None:
        return ()
    prepared = t1.source_input(old.basis.o2b_json)
    values = [(s.id, raw_source(s)) for s in old.basis.sources]
    values.extend((s.id, source_bytes(s)) for s in prepared.basis.sources)
    return tuple((sid, content) for sid, content in values if content is not None)


def import_basis(root: Path, *, t1_json: str = "") -> Basis:
    return import_sources(root, legacy_json=t1_json, legacy=legacy_payloads(t1_json))


@lru_cache(maxsize=3)
def contents(basis: Basis) -> PilotBasis:
    """Vue i minnet med gamle ID-referanser; serialiseres aldri som ny T2-basis."""
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
        basis.issues + (previous.issues if previous else ()),
    )


def validate_basis(basis: Basis) -> None:
    validate_sources(basis, legacy_payloads(basis.legacy_json))


def compare_observations(
    left: AmountObservation | None,
    right: AmountObservation | None,
    left_context: TreatmentContext | None,
    right_context: TreatmentContext | None,
    *,
    account: str,
    meaning: str,
    relation_bound: bool,
) -> StageComparison:
    """T2s egen rolleport. T1s samlet-komité-port beholdes uendret."""
    reason = ""
    if left is None or right is None:
        reason = "manglende stadium"
    elif (
        not left_context
        or not right_context
        or not relation_bound
        or left_context.observation_id != left.id
        or right_context.observation_id != right.id
        or left_context.status != "kildeverifisert"
        or right_context.status != "kildeverifisert"
        or not left_context.evidence_ids
        or not right_context.evidence_ids
    ):
        reason = "manglende dokumentert flertalls-/voteringsgrunnlag"
    else:
        for field in (
            "budget_year",
            "chapter",
            "post",
            "subpost",
            "currency",
            "multiplier",
            "meaning",
            "detail_level",
            "scope",
            "information_type",
        ):
            a, b = getattr(left, field), getattr(right, field)
            if a != b or (a is None and field != "subpost") or a == "uavklart":
                reason = "uforenlig eller uavklart " + field
                break
        if not reason and (
            left.meaning != meaning
            or (left.chapter or "") + "/" + (left.post or "") != account
            or left.amount_kr is None
            or right.amount_kr is None
        ):
            reason = "manglende verdi eller motstridende konto/betydning"
        allowed = {
            ("regjering", "tilraading", "regjeringsforslag", "komiteforslag", None, "tilraading"),
            ("tilraading", "vedtak", "komiteforslag", "stortingsvedtak", "tilraading", None),
        }
        actors = {"regjering": "regjeringen", "tilraading": "Ap_Sp_SV", "vedtak": "stortinget"}
        if not reason and (
            (
                left_context.stage,
                right_context.stage,
                left.figure_type,
                right.figure_type,
                left.proposal_role,
                right.proposal_role,
            )
            not in allowed
            or left_context.actor != actors.get(left_context.stage)
            or right_context.actor != actors.get(right_context.stage)
            or left.proposal_author != left_context.actor
            or right.proposal_author != right_context.actor
            or left_context.round != "nysaldering"
            or right_context.round != "nysaldering"
            or left.round != "nysaldering"
            or right.round != "nysaldering"
            or left.scope != "enkeltledd"
            or left.detail_level != "post"
            or left.information_type != "bevilgning"
        ):
            reason = "uforenlig runde, stadium, rolle, aktør eller omfang"
    difference = None
    if not reason:
        assert left and right and left.amount_kr is not None and right.amount_kr is not None
        difference = right.amount_kr - left.amount_kr
        if abs(difference) > 9_007_199_254_740_991:
            reason, difference = "forskjell utenfor Excel-eksakt heltall", None
    return identified(
        "komitesammenligning-1",
        StageComparison(
            "",
            meaning,
            account,
            "beregnet" if not reason else "hull" if left is None or right is None else "sperret",
            reason or "To kildebelagte felt; postvis flertall og vedtakelse er kontrollert",
            "stadieforskjell-komite315-1",
            left.id if left else None,
            right.id if right else None,
            reason or None,
            difference,
        ),
    )


def _view(basis: Basis, selection: PilotSelection) -> PilotView:
    all_data = contents(basis)
    view = t1._view(all_data, selection)
    comparisons = list(view.comparisons)
    selected_inventory = {i.id for i in basis.inventory if (i.chapter, i.post) == ("315", "78")}
    if selected_inventory.intersection(view.inventory_ids):
        contexts = {c.observation_id: c for c in basis.contexts}
        for meaning in ("for_belop", "endring", "etter_belop"):
            stages = {contexts[o.id].stage: o for o in basis.observations if o.meaning == meaning}
            for a, b in (("regjering", "tilraading"), ("tilraading", "vedtak")):
                left, right = stages.get(a), stages.get(b)
                lc, rc = (
                    contexts.get(left.id) if left else None,
                    contexts.get(right.id) if right else None,
                )
                bound = bool(
                    lc
                    and rc
                    and any(
                        r.from_id == lc.document_id
                        and r.to_id == rc.document_id
                        and r.status == "kildeverifisert"
                        and "315/78" in r.accounts
                        and r.evidence_ids
                        for r in basis.relations
                    )
                )
                comparisons.append(
                    compare_observations(
                        left, right, lc, rc, account="315/78", meaning=meaning, relation_bound=bound
                    )
                )
    evidence_ids = {
        sid
        for context in basis.contexts
        if context.observation_id in view.observation_ids
        for sid in context.evidence_ids
    }
    statement_ids = set(view.statement_ids) | evidence_ids
    document_ids = set(view.document_ids) | {
        s.document_id for s in basis.statements if s.id in statement_ids
    }
    return replace(
        view,
        comparisons=tuple(comparisons),
        statement_ids=tuple(s.id for s in all_data.statements if s.id in statement_ids),
        document_ids=tuple(d.id for d in all_data.documents if d.id in document_ids),
    )


def build_report(
    basis: Basis, selection: PilotSelection, *, return_selection: PilotSelection | None = None
) -> Report:
    validate_basis(basis)
    t1.validate_selection(selection, contents(basis))
    if return_selection is not None:
        t1.validate_selection(return_selection, contents(basis))
    return identified(
        FORMAT, Report("", basis, selection, return_selection, _view(basis, selection))
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
        raise ValueError("T2-rapporten avviker fra kilder/utvalgsregler")
    raw = encode({"format": FORMAT, "report": asdict(report)})
    if len(raw.encode("utf8")) > MAX_REPORT_BYTES:
        raise ValueError("T2-rapport overstiger 64 MiB")
    return raw


def report_from_json(raw: str) -> Report:
    if len(raw.encode("utf8")) > MAX_REPORT_BYTES:
        raise ValueError("T2-rapport overstiger 64 MiB")
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        if (
            not isinstance(data, dict)
            or set(data) != {"format", "report"}
            or data["format"] != FORMAT
        ):
            raise ValueError("Ukjent T2-konvolutt")
        report: Report = _decode(Report, data["report"])
        if encode(asdict(report)) != encode(data["report"]):
            raise ValueError("T2-felter endres ved type-/nullgrunnskontroll")
        report_to_json(report)
        return report
    except (TypeError, KeyError, RecursionError) as error:
        raise ValueError("Ugyldig T2-rapport") from error


def read_json(path: Path) -> Report:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("T2-rapport overstiger 64 MiB")
    return report_from_json(raw.decode("utf8"))


def export_json(report: Report, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".json":
        raise ValueError("Velg nytt T2-JSON-filnavn")
    raw = report_to_json(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw.encode("utf8"))
        if read_json(temporary) != report:
            raise ValueError("Skrevet T2-JSON avviker")
        _publish(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rot", type=Path, default=Path("."))
    parser.add_argument("--t1", type=Path, help="Én valgfri gammel T1-kapsel for union")
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
            raise ValueError("Frosset T2 har allerede sitt eventuelle T1-grunnlag")
        previous = read_json(args.frosset) if args.frosset else None
        basis = (
            previous.basis
            if previous
            else import_basis(args.rot, t1_json=args.t1.read_text("utf8") if args.t1 else "")
        )
        if args.dokument:
            if args.aar or args.kapittel or args.konto:
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
            if previous and not (args.dokument or args.aar or args.kapittel or args.konto)
            else build_report(basis, selection)
        )
        from .komitepilot_excel import export_originals, export_pair

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
