"""Reproduserbar T5-kontroll mot bevarte originaler og en eksplisitt kandidatrot."""

import argparse
import gzip
import hashlib
import json
import os
import subprocess
from dataclasses import asdict
from pathlib import Path

from lxml import etree, html

from analyse import proposisjon16 as t5
from analyse.proposisjon16_excel import export_originals, export_pair, read_excel
from analyse.visningspilot import report_from_json as read_t1
from analyse.visningspilot import report_to_json as freeze_t1
from innlesning.visningspilot_model import PilotSelection


def source_controls(basis, root: Path) -> dict:
    """Separat råkilde-/locatorfasit; ingen gjenkjøring av produktets parser."""
    original = html.fromstring(
        (root / "docs/research/omtale-o1/originals/prop16s-ch4.html").read_text("utf8")
    )
    frames = {
        ("II", "1"): (8_000_000, "8 mill."),
        ("III", "1"): (601_000_000, "601,0 mill."),
        ("III", "2"): (266_300_000, "266,3 mill."),
        ("IV", "1"): (16_300_000, "16,3 mill."),
        ("VI", "1"): (25_000_000, "25 mill."),
    }
    authorizations = []
    for auth in basis.authorizations:
        nodes = original.xpath(auth.locator)
        assert len(nodes) == 1
        section = nodes[0].xpath("ancestor-or-self::div[@class='K-DEL-VEDTAKDEL'][1]")[0]
        assert " ".join(section.text_content().split()) == " ".join(auth.text.split())
        assert section.xpath("./h2[@class='K-TIT-VEDTAKDEL']/text()") == [auth.roman]
        frame = frames.get((auth.roman, auth.point))
        if frame:
            assert auth.frame_kr == frame[0]
            assert frame[1] in " ".join(section.text_content().split())
        else:
            assert auth.frame_kr is None
        authorizations.append(
            {
                "id": auth.id,
                "locator": auth.locator,
                "frame_kr": auth.frame_kr,
                "accounts": auth.accounts,
            }
        )
    from innlesning.visningspilot import raw_source

    parent_source = next(
        s
        for s in basis.t1_basis.sources
        if s.document_key == "forelder2024" and s.media_type == "application/gzip"
    )
    raw = raw_source(parent_source)
    assert raw is not None
    parent = etree.fromstring(gzip.decompress(raw))
    ns = {"s": "http://data.stortinget.no"}
    branches = []
    for branch in basis.branches:
        for identifier in branch.decision_ids:
            nodes = parent.xpath(
                "//s:stortingsvedtak[s:id=$identifier]", namespaces=ns, identifier=identifier
            )
            assert len(nodes) == 1
            node = nodes[0]
            assert node.findtext("s:sak_id", namespaces=ns) == branch.case_id
            text = node.findtext("s:stortingsvedtak_tekst", namespaces=ns)
            inner = html.fromstring(text)
            assert inner.xpath(
                "//*[@data-strtngt-romertallseksjon-romertall]/@data-strtngt-romertallseksjon-romertall"
            ) == [branch.committee_point.lower()]
            branches.append(
                {
                    "branch_id": branch.id,
                    "api_id": identifier,
                    "case_id": branch.case_id,
                    "committee_point": branch.committee_point,
                    "source_sha256": parent_source.sha256,
                    "locator": node.getroottree().getpath(node),
                }
            )
    return {"authorizations": authorizations, "formal_branch_locators": branches}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base", help="Publisert sammenligningsref, tilgjengelig i valgt klon")
    parser.add_argument("--candidate", help="Valgfri publisert kandidatref til rapportbinding")
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    os.chdir(root)
    old_file = root / "tests/fixtures/t2/authentic-t1.json.gz"
    old_hash = hashlib.sha256(old_file.read_bytes()).hexdigest()
    old = read_t1(gzip.decompress(old_file.read_bytes()).decode("utf8"))
    basis = t5.import_basis(freeze_t1(old), root)
    data = t5.contents(basis)
    source_evidence = source_controls(basis, root)
    prop = next(d for d in data.documents if d.key == "prop16")
    proposed = {
        (o.chapter + "/" + o.post, o.meaning): o
        for o in data.observations
        if o.figure_type == "regjeringsforslag" and o.chapter and o.post
    }
    reference_path = root / "docs/research/to-visninger-37/originals/forgrening/inventory.json"
    reference = json.loads(reference_path.read_text("utf8"))
    original_path = root / "docs/research/omtale-o1/originals/prop16s-ch4.html"
    original = html.fromstring(original_path.read_bytes().decode("utf8"))
    fields = []
    # Eldre kontrolluttrekk gir uavhengige forventede felt og lokatorer.
    # Originalens faktiske celle kontrolleres i tillegg uten produktparseren.
    for entry in reference["account_comparison"]:
        row = entry["proposal"]
        if row is None:
            continue
        for meaning, value_key, locator, column in (
            ("for_belop", "before", row["next_xpath"], 3),
            ("endring", "delta", row["xpath"], 4),
            ("etter_belop", "after", row["next_xpath"], 3),
        ):
            observation = proposed[(entry["account"], meaning)]
            source_locator = locator + f"/td[{column}]"
            assert observation.amount_kr == row[value_key]
            assert observation.pointer.locator == source_locator
            nodes = original.xpath(source_locator)
            assert len(nodes) == 1
            text = " ".join(nodes[0].text_content().split())
            assert observation.raw_value in text
            fields.append(
                {
                    "account": entry["account"],
                    "meaning": meaning,
                    "amount_kr": row[value_key],
                    "locator": source_locator,
                    "observation_id": observation.id,
                    "original_cell": text,
                }
            )
    assert len(fields) == 111
    assert basis.t1_basis == old.basis and len(basis.observations) == 105
    assert len(data.observations) == len({o.id for o in data.observations}) == 123
    prop_items = [i for i in data.inventory if i.document_id == prop.id]
    assert len({(i.chapter, i.post) for i in prop_items}) == 45
    assert len(basis.authorizations) == 9
    assert [a.frame_kr for a in basis.authorizations if a.roman == "IV"] == [16_300_000]
    assert all("1533/45" not in b.accounts for b in basis.branches)
    accounts = PilotSelection(
        years=(2024,), chapters=("1429",), accounts=(("4400", "2"), ("1420", "22"))
    )
    selections = {
        "utgift": PilotSelection(years=(2024,), accounts=(("1400", "1"),)),
        "inntekt-null": PilotSelection(years=(2024,), accounts=(("4400", "2"),)),
        "tekst": PilotSelection(years=(2024,), accounts=(("1420", "66"),)),
        "flere": accounts,
        "tomt": PilotSelection(years=(2024,)),
        "hele-prop": PilotSelection(mode="document", document_id=prop.id),
        "post1": PilotSelection(years=(2024,), accounts=(("1429", "1"),)),
        "post22": PilotSelection(years=(2024,), accounts=(("1429", "22"),)),
        "begge": PilotSelection(years=(2024,), chapters=("1429",)),
        "kontekst1533": PilotSelection(years=(2024,), accounts=(("1533", "45"),)),
    }
    reports = {name: t5.build_report(basis, selection) for name, selection in selections.items()}
    reports["konto-til-dokument"] = t5.open_document(reports["flere"], prop.id)
    reports["retur-konto"] = t5.go_back(reports["konto-til-dokument"])
    reports["dokument-til-konto"] = t5.open_accounts(reports["hele-prop"], accounts)
    reports["retur-dokument"] = t5.go_back(reports["dokument-til-konto"])
    results = []
    for name, report in reports.items():
        frozen, excel = output / (name + ".json"), output / (name + ".xlsx")
        export_pair(report, frozen, excel)
        assert t5.read_json(frozen) == read_excel(excel) == report
        results.append(
            {
                "name": name,
                "report_id": report.id,
                "basis_id": basis.id,
                "selection": asdict(report.selection),
                "return_selection": asdict(report.return_selection)
                if report.return_selection
                else None,
                "fields": len(report.view.observation_ids),
                "adopted_fields": len(report.view.adopted_observation_ids),
                "monetary_events": len(report.view.adopted_event_ids),
                "files": [
                    {
                        "name": path.name,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "bytes": path.stat().st_size,
                    }
                    for path in (frozen, excel)
                ],
            }
        )
    assert reports["retur-konto"] == reports["flere"]
    assert reports["retur-dokument"] == reports["hele-prop"]
    export_originals(reports["hele-prop"], output / "originaler")
    assert old_hash == hashlib.sha256(old_file.read_bytes()).hexdigest()
    binding = {}
    for key in ("base", "candidate"):
        ref = getattr(args, key)
        if ref:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", ref + "^{commit}"],
                capture_output=True,
                check=True,
                text=True,
            )
            binding[key] = result.stdout.strip()
    if args.base:
        changes = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=DMRTUXB", args.base],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.splitlines()
        assert set(changes) <= {"AGENTS.md", "docs/kildefunn.md"}
        binding["changed_base_files"] = changes
    if args.candidate:
        subprocess.run(["git", "diff", "--quiet", "--exit-code", args.candidate], check=True)
    sources = []
    from analyse.omtale import report_from_json as read_o2

    o2 = read_o2(old.basis.o2b_json)
    for source in (*old.basis.sources, *basis.sources, *o2.basis.sources):
        sources.append(
            {
                "id": source.id,
                "name": source.name,
                "sha256": source.sha256,
                "bytes": source.byte_count,
                "status": source.status,
                "metadata_json": source.metadata_json,
            }
        )
    ledger = {
        "schema": "t5-control-1",
        "binding": binding,
        "basis_id": basis.id,
        "legacy_fixture_sha256": old_hash,
        "source_control_sha256": hashlib.sha256(reference_path.read_bytes()).hexdigest(),
        "proposal_html_sha256": hashlib.sha256(original_path.read_bytes()).hexdigest(),
        "fields": fields,
        "sources": sources,
        "independent_source_controls": source_evidence,
        "coverage": [asdict(c) for c in basis.coverage],
        "authorizations": [asdict(a) for a in basis.authorizations],
        "branches": [asdict(b) for b in basis.branches],
        "pairs": results,
        "limits": [
            "ikke full semantikk",
            "ikke årsdekning",
            "95-beløp venter T6",
            "native Excel uprøvd",
            "uavhengige porter/CI eies av orkestrator",
        ],
    }
    (output / "kontroll.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2), "utf8")
    print(
        json.dumps(
            {
                "basis_id": basis.id,
                "fields_checked": len(fields),
                "saved_pairs": len(results),
                "output": str(output),
            }
        )
    )


if __name__ == "__main__":
    main()
