"""Reproduser den lokale autentiske O2a-prøven; ingen HTTP eller historisk Excel.

Kjør fra reporoten: python -m ops.omtale_proeve --output work/omtale-post1-leveranse
"""

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from analyse.omtale import build_report, export_pair, read_excel, read_json
from analyse.saksdokumenter import (
    SaksSelection,
    build_saks_report,
    export_built_saks_excel,
    export_saks_json,
)
from analyse.session import SessionSelection
from innlesning import extract_revision, read_sync, sync_saved
from innlesning.observations import Interpretation
from innlesning.omtale import import_omtale
from innlesning.saksdokumenter import enrich_revision, import_case_response


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    fixtures = Path("tests/fixtures")
    database = output / "210.sqlite"
    raw = (fixtures / "b6/40034048.xml").read_bytes()
    metadata = json.loads((fixtures / "b6/40034048.json").read_text("utf-8"))
    job = sync_saved(database, raw, metadata, historical_sample=True, decision_id="40034048")
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
            "prove", "2024-2025", (job,), extraction_ids=(extraction.id,), posts=("1",)
        ),
        (enrichment.id,),
    )
    (output / "saksutvalg.json").write_text(
        json.dumps(asdict(selection), ensure_ascii=False, indent=2), "utf-8"
    )
    base = build_saks_report(database, selection)
    export_saks_json(base, output / "uendret-b8.json", database=database)
    export_built_saks_excel(database, base, output / "uendret-b9.xlsx")
    basis = import_omtale(Path("docs/research/omtale-o1"), fixtures)
    report = build_report(base, basis)
    frozen, excel = output / "omtale-210-post1.json", output / "omtale-210-post1.xlsx"
    export_pair(report, frozen, excel)
    first = read_json(frozen)
    assert read_excel(excel) == first
    # Reeksporter fra bare den frosne filen med databasen utilgjengelig.
    database.rename(output / "210.sqlite.unavailable")
    export_pair(first, output / "offline-gjenlest.json", output / "offline-gjenlest.xlsx")
    assert read_json(output / "offline-gjenlest.json") == read_excel(
        output / "offline-gjenlest.xlsx"
    )
    manifest = {
        "kind": "Autentisk lokal O2a-prøve, ikke årsdekning eller faglig godkjenning",
        "report_id": report.id,
        "basis_id": report.basis.id,
        "base_report_id": base.id,
        "observations_unfiltered": len(base.base.unfiltered_rows),
        "post_events_unfiltered": len({r.observation.step_id for r in base.base.unfiltered_rows}),
        "observations_selected": len(base.base.rows),
        "sections": [s.key for s in report.basis.sections],
        "relations": len(report.relations),
        "relation_statuses": sorted({r.status for r in report.relations}),
        "issues": report.issues,
        "files": [
            {
                "file": p.name,
                "bytes": p.stat().st_size,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            }
            for p in sorted(output.iterdir())
            if p.is_file()
        ],
    }
    (output / "kontroll.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
