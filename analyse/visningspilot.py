"""Avledede T1-utvalg, navigasjon og sammenligning. Streng offline JSON-grense."""

import argparse
import json
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning.observations import AmountObservation, encode
from innlesning.omtale import identified
from innlesning.visningspilot import import_basis as import_sources
from innlesning.visningspilot import validate_basis as validate_sources
from innlesning.visningspilot_model import (
    FORMAT,
    PilotBasis,
    PilotInput,
    PilotReport,
    PilotSelection,
    PilotView,
    StageComparison,
    TreatmentContext,
)

from .saksdokumenter import _publish
from .session_serialization import _constant, _decode, _object

MAX_REPORT_BYTES = 64 * 1024 * 1024


@lru_cache(maxsize=2)
def source_input(o2b_json: str) -> PilotInput:
    """Analyse eier lesing av sine gamle konvolutter; adapteren mottar kildeobjekter."""
    from .omtale import _source_binding
    from .omtale import report_from_json as read_old
    from .saksdokumenter import report_from_json as read_base

    old = read_old(o2b_json)
    base = read_base(old.base_json)
    _source_binding(base, old.basis)
    rows = base.base.unfiltered_rows
    extractions = base.source_text.extractions
    if len(extractions) != 1 or any(r.extraction_id != extractions[0].id for r in rows):
        raise ValueError("T1 krever ett entydig opprinnelig vedtaksuttrekk")
    return PilotInput(
        o2b_json, old.basis, old.issues, extractions[0], tuple(r.observation for r in rows)
    )


def import_basis(o2b_json: str, root: Path) -> PilotBasis:
    return import_sources(source_input(o2b_json), root)


def validate_basis(basis: PilotBasis) -> None:
    validate_sources(basis, source_input(basis.o2b_json))


def validate_selection(selection: PilotSelection, basis: PilotBasis) -> None:
    if selection.mode not in {"document", "accounts"}:
        raise ValueError("Ukjent visningsinngang")
    if selection.mode == "document":
        if (
            selection.document_id not in {d.id for d in basis.documents}
            or selection.years
            or selection.chapters
            or selection.accounts
        ):
            raise ValueError("Dokumentvalg krever eksakt versjon uten kontofiltre")
    elif selection.document_id is not None:
        raise ValueError("Konto-/årsvalg kan ikke ha dokumentfilter")
    if any(type(y) is not int or not 1000 <= y <= 9999 for y in selection.years):
        raise ValueError("År må være firesifrede heltall")
    for code in (*selection.chapters, *(c for pair in selection.accounts for c in pair)):
        if not code.isascii() or not code.isdigit() or str(int(code)) != code:
            raise ValueError("Kontokoder må være kanonisk desimal tekst")
    if (
        len(selection.years) > 100
        or len(selection.chapters) > 100
        or len(selection.accounts) > 512
        or len(set(selection.years)) != len(selection.years)
        or len(set(selection.chapters)) != len(selection.chapters)
        or len(set(selection.accounts)) != len(selection.accounts)
    ):
        raise ValueError("Duplisert eller for stort utvalg")
    if any(len(pair) != 2 for pair in selection.accounts):
        raise ValueError("Kontoutvalg krever eksakte kapittel/post-par")


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
    """Offentlig sammenligningsport; også kildeuavhengige negative prøver bruker den."""
    reason = ""
    if left is None or right is None:
        reason = "manglende stadium"
    elif (
        left_context is None
        or right_context is None
        or not relation_bound
        or left_context.observation_id != left.id
        or right_context.observation_id != right.id
        or left_context.status != "kildeverifisert"
        or right_context.status != "kildeverifisert"
        or not left_context.evidence_ids
        or not right_context.evidence_ids
    ):
        reason = "manglende dokumentert behandlingsgrunnlag"
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
            reason = "manglende verdi eller motstridende forventet konto/betydning"
        allowed = {
            ("regjering", "tilraading", "regjeringsforslag", "komiteforslag", None, "tilraading"),
            ("tilraading", "vedtak", "komiteforslag", "stortingsvedtak", "tilraading", None),
        }
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
            or left_context.round != right_context.round
            or left_context.round == "uavklart"
            or left.round not in {"uavklart", left_context.round}
            or right.round not in {"uavklart", right_context.round}
            or left.scope != "enkeltledd"
            or left.detail_level != "post"
            or left.information_type != "bevilgning"
            or left_context.actor
            != {"regjering": "regjeringen", "tilraading": "samlet_komite"}.get(left_context.stage)
            or right_context.actor
            != {"tilraading": "samlet_komite", "vedtak": "stortinget"}.get(right_context.stage)
        ):
            reason = "uforenlig runde, stadium, rolle eller omfang"
    difference = None
    if not reason:
        assert left is not None and right is not None
        assert left.amount_kr is not None and right.amount_kr is not None
        difference = right.amount_kr - left.amount_kr
        if abs(difference) > 9_007_199_254_740_991:
            reason = "forskjell utenfor Excel-eksakt heltall"
            difference = None
    return identified(
        "visningssammenligning-1",
        StageComparison(
            "",
            meaning,
            account,
            "beregnet" if not reason else "hull" if left is None or right is None else "sperret",
            reason or "To kildebelagte felt med samme konto, år, betydning og omfang",
            "stadieforskjell-1",
            left.id if left else None,
            right.id if right else None,
            reason or None,
            difference,
        ),
    )


def _matches(selection: PilotSelection, chapter: str, post: str, year: int) -> bool:
    return year in selection.years and (
        chapter in selection.chapters or (chapter, post) in selection.accounts
    )


def _view(basis: PilotBasis, selection: PilotSelection) -> PilotView:
    inventory = (
        tuple(
            item
            for item in basis.inventory
            if item.document_id == selection.document_id
            if selection.mode == "document"
        )
        if selection.mode == "document"
        else tuple(
            item
            for item in basis.inventory
            if _matches(selection, item.chapter, item.post, item.budget_year)
        )
    )
    contexts = {c.observation_id: c for c in basis.contexts}
    observations = tuple(
        o
        for o in basis.observations
        if (
            contexts[o.id].document_id == selection.document_id
            if selection.mode == "document"
            else _matches(selection, o.chapter or "", o.post or "", o.budget_year or 0)
        )
    )
    statements = (
        tuple(
            statement
            for statement in basis.statements
            if statement.document_id == selection.document_id
        )
        if selection.mode == "document"
        else tuple(
            statement
            for statement in basis.statements
            if any(
                _matches(selection, account.split("/")[0], account.split("/")[1], year)
                for account in statement.accounts
                for year in selection.years
                if str(year) in statement.period
            )
        )
    )
    documents = {r.document_id for r in inventory} | {s.document_id for s in statements}
    documents.update(contexts[o.id].document_id for o in observations)
    if selection.mode == "document":
        documents.add(selection.document_id or "")
    compared_accounts = {(i.chapter, i.post) for i in inventory}
    comparisons = []
    for chapter, post in sorted(compared_accounts):
        if chapter != "1429" or post not in {"1", "22"}:
            continue
        for meaning in ("for_belop", "endring", "etter_belop"):
            stages = {}
            for observation in basis.observations:
                if (
                    observation.chapter,
                    observation.post,
                    observation.budget_year,
                    observation.meaning,
                ) == (chapter, post, 2024, meaning):
                    stages[contexts[observation.id].stage] = observation
            for left_stage, right_stage in (("regjering", "tilraading"), ("tilraading", "vedtak")):
                left, right = stages.get(left_stage), stages.get(right_stage)
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
                        and chapter + "/" + post in r.accounts
                        for r in basis.relations
                    )
                )
                comparisons.append(
                    compare_observations(
                        left,
                        right,
                        lc,
                        rc,
                        account=chapter + "/" + post,
                        meaning=meaning,
                        relation_bound=bound,
                    )
                )
    adopted = tuple(o for o in observations if o.figure_type == "stortingsvedtak")
    return PilotView(
        tuple(d.id for d in basis.documents if d.id in documents),
        tuple(i.id for i in inventory),
        tuple(s.id for s in statements),
        tuple(o.id for o in observations),
        tuple(o.id for o in adopted),
        tuple(sorted({o.step_id for o in adopted})),
        tuple(comparisons),
    )


def build_report(
    basis: PilotBasis,
    selection: PilotSelection,
    *,
    return_selection: PilotSelection | None = None,
) -> PilotReport:
    validate_basis(basis)
    validate_selection(selection, basis)
    if return_selection is not None:
        validate_selection(return_selection, basis)
    return identified(
        FORMAT, PilotReport("", basis, selection, return_selection, _view(basis, selection))
    )


def open_document(report: PilotReport, document_id: str) -> PilotReport:
    return build_report(
        report.basis,
        PilotSelection(mode="document", document_id=document_id),
        return_selection=report.selection,
    )


def open_accounts(report: PilotReport, selection: PilotSelection) -> PilotReport:
    if selection.mode != "accounts":
        raise ValueError("Velg konto-/årsinngang")
    return build_report(report.basis, selection, return_selection=report.selection)


def go_back(report: PilotReport) -> PilotReport:
    if report.return_selection is None:
        raise ValueError("Ingen tidligere inngang")
    # Første retur til et startutvalg rekonstruerer også den opprinnelige rapport-ID-en.
    return build_report(report.basis, report.return_selection)


def _validate(report: PilotReport) -> None:
    if report.version != FORMAT or report != build_report(
        report.basis, report.selection, return_selection=report.return_selection
    ):
        raise ValueError("Visningsrapport avviker fra originaler/utvalgsregler")


def report_to_json(report: PilotReport) -> str:
    _validate(report)
    raw = encode({"format": FORMAT, "report": asdict(report)})
    if len(raw.encode("utf-8")) > MAX_REPORT_BYTES:
        raise ValueError("Visningsrapport overstiger 64 MiB")
    return raw


def report_from_json(raw: str) -> PilotReport:
    if len(raw.encode("utf-8")) > MAX_REPORT_BYTES:
        raise ValueError("Visningsrapport overstiger 64 MiB")
    try:
        data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        if (
            not isinstance(data, dict)
            or set(data) != {"format", "report"}
            or data["format"] != FORMAT
        ):
            raise ValueError("Ukjent visningskonvolutt")
        report: PilotReport = _decode(PilotReport, data["report"])
        _validate(report)
        return report
    except (RecursionError, TypeError, KeyError) as error:
        raise ValueError("Ugyldig visningsrapport") from error


def read_json(path: Path) -> PilotReport:
    with path.open("rb") as handle:
        raw = handle.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("Visningsrapport overstiger 64 MiB")
    return report_from_json(raw.decode("utf-8"))


def export_json(report: PilotReport, output: Path) -> None:
    if output.exists() or output.suffix.lower() != ".json":
        raise ValueError("Velg nytt JSON-filnavn")
    frozen = report_to_json(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(frozen.encode("utf-8"))
        if read_json(temporary) != report:
            raise ValueError("Skrevet JSON avviker")
        _publish(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--o2b", type=Path)
    source.add_argument("--frosset", type=Path)
    parser.add_argument("--rot", type=Path, default=Path("."))
    parser.add_argument(
        "--dokument", help="Eksakt dokumentversjons-ID, eller pilotnøkkel ved førstegangsvalg"
    )
    parser.add_argument("--aar", type=int, action="append", default=[])
    parser.add_argument("--kapittel", action="append", default=[])
    parser.add_argument("--konto", action="append", default=[])
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--excel", type=Path, required=True)
    parser.add_argument(
        "--originaler", type=Path, help="Ny katalog med gjenfunne originalbyte offline"
    )
    args = parser.parse_args()
    try:
        previous = read_json(args.frosset) if args.frosset else None
        basis = previous.basis if previous else import_basis(args.o2b.read_text("utf-8"), args.rot)
        if args.dokument:
            if args.aar or args.kapittel or args.konto:
                raise ValueError("Dokumentvalg har ingen konto-/årsfiltre")
            document_id = next(
                (d.id for d in basis.documents if d.key == args.dokument), args.dokument
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
        from .visningspilot_excel import export_originals, export_pair

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
