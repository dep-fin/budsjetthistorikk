"""Reproduser O2b/#35 lokalt fra autentiske originaler, uten HTTP/historisk Excel.

python -m ops.omtale_begge_proeve --output work/omtale-begge-ny
"""

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

from analyse.omtale import build_report, export_pair, read_excel, read_json, report_to_json
from analyse.omtale_begge import build_both_report, propose_relation
from analyse.saksdokumenter import SaksSelection, build_saks_report, export_saks_json
from analyse.session import SessionSelection
from innlesning import extract_revision, read_sync, sync_saved
from innlesning.observations import Interpretation
from innlesning.omtale import O2B_EXTRACTOR, import_omtale
from innlesning.saksdokumenter import enrich_revision, import_case_response


def file_evidence(path: Path) -> dict[str, str | int]:
    return {
        "file": str(path),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--previous", type=Path, help="Valgfri ekte gammel O2a-leveranse; leses uendret"
    )
    args = parser.parse_args()
    output: Path = args.output
    output.mkdir(parents=True, exist_ok=False)
    fixtures = Path("tests/fixtures")
    database = output / "210.sqlite"
    job = sync_saved(
        database,
        (fixtures / "b6/40034048.xml").read_bytes(),
        json.loads((fixtures / "b6/40034048.json").read_text("utf-8")),
        historical_sample=True,
        decision_id="40034048",
    )
    revision = read_sync(database, job).entries[0].revision_id
    extraction = extract_revision(
        database, revision, interpretation=Interpretation(adapter_version="storting-belop-v2")
    )
    case = import_case_response(
        database,
        "100927",
        (fixtures / "b8/sak-100927.xml").read_bytes(),
        json.loads((fixtures / "b8/sak-100927.json").read_text("utf-8")),
        dataset="prove",
        session="2024-2025",
    )
    enrichment = enrich_revision(database, revision, case.id)
    selection = SaksSelection(
        SessionSelection(
            "prove", "2024-2025", (job,), extraction_ids=(extraction.id,), posts=("1", "22")
        ),
        (enrichment.id,),
    )
    basis = import_omtale(Path("docs/research/omtale-o1"), fixtures, extractor=O2B_EXTRACTOR)
    base = build_saks_report(database, selection)
    export_saks_json(base, output / "uendret-b8-begge.json", database=database)
    report = build_report(base, basis)
    assert report == build_report(base, basis)
    sections = {s.key: s for s in basis.sections}
    target = next(r for r in report.relations if r.accounts == ("1429/1",))
    proposed = propose_relation(
        report,
        section_id=sections["K22"].id,
        event_id=target.event_id,
        evidence_ids=(sections["K22"].id,),
        reason=(
            "Syntetisk uavklart relasjonsforslag; "
            "ingen kildeverifisert egen post 1-forklaring i K22."
        ),
    )
    results = []
    for name, posts in (
        ("begge", ("1", "22")),
        ("post1", ("1",)),
        ("post22", ("22",)),
        ("tomt", ("99",)),
    ):
        filtered = build_saks_report(
            database, replace(selection, base=replace(selection.base, posts=posts))
        )
        current = build_both_report(
            filtered,
            basis,
            proposals=tuple(r for r in proposed.relations if r.status == "uavklart")
            if name == "tomt"
            else (),
        )
        frozen, excel = output / (name + ".json"), output / (name + ".xlsx")
        export_pair(current, frozen, excel)
        assert read_json(frozen) == read_excel(excel) == current
        results.append(
            {
                "selection": name,
                "report_id": current.id,
                "observations_selected": len(filtered.base.rows),
                "observations_unfiltered": len(filtered.base.unfiltered_rows),
                "post_events_unfiltered": len(
                    {r.observation.step_id for r in filtered.base.unfiltered_rows}
                ),
                "sections": [s.key for s in current.basis.sections],
                "visible_section_ids": current.visible_section_ids,
                "relations": len(current.relations),
                "issues": current.issues,
                "files": [file_evidence(frozen), file_evidence(excel)],
            }
        )
    export_pair(proposed, output / "syntetisk-forslag.json", output / "syntetisk-forslag.xlsx")
    assert read_json(output / "syntetisk-forslag.json") == read_excel(
        output / "syntetisk-forslag.xlsx"
    )
    database.rename(output / "210.sqlite.unavailable")
    offline = read_json(output / "begge.json")
    export_pair(offline, output / "offline.json", output / "offline.xlsx")
    assert (output / "offline.json").read_bytes() == (output / "begge.json").read_bytes()
    assert read_excel(output / "offline.xlsx") == offline
    previous = []
    if args.previous:
        for name in ("omtale-210-post1", "offline-gjenlest"):
            frozen, excel = args.previous / (name + ".json"), args.previous / (name + ".xlsx")
            before = [file_evidence(frozen), file_evidence(excel)]
            old = read_json(frozen)
            assert old == read_excel(excel)
            assert report_to_json(old) == frozen.read_text("utf-8")
            assert len(old.basis.sections) == 8 and len(old.relations) == 6
            assert before == [file_evidence(frozen), file_evidence(excel)]
            previous.append({"report_id": old.id, "files": before, "byte_preserved": True})
    manifest = {
        "kind": (
            "Autentisk O2b-kildeprøve og særskilt merket syntetisk forslag; "
            "ingen faglig godkjenning/årsdekning"
        ),
        "basis_id": basis.id,
        "extractor": basis.extractor,
        "selections": results,
        "previous_o2a": previous,
        "files": [file_evidence(p) for p in sorted(output.iterdir()) if p.is_file()],
    }
    (output / "kontroll.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "basis_id": basis.id,
                "pairs": 6,
                "genuine_old_pairs": len(previous),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
