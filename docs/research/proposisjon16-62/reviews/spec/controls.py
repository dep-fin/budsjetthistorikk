"""Independent T5 Spec probes; run from a checkout of --candidate."""

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--files", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    sys.path.insert(0, str(root))

    def git(*argv, binary=False):
        return subprocess.check_output(["git", "-C", str(root), *argv], text=not binary)

    candidate = git("rev-parse", args.candidate).strip()
    base = git("rev-parse", args.base).strip()
    tree = git("rev-parse", candidate + "^{tree}").strip()
    assert tree == "df0eed6d6e8a0b2a07962e641ae05d1194a3304d", tree
    assert not git("diff", candidate, "--name-only"), "Tracked checkout differs"
    changed = git("diff", "--name-only", "--diff-filter=DMRTUXB", base, candidate).splitlines()
    assert changed == ["AGENTS.md", "docs/kildefunn.md"], changed
    report = {"candidate": candidate, "tree": tree, "base": base, "changed_base_files": changed}

    manifest = json.loads(
        (root / "docs/research/proposisjon16-62/delivery-manifest.json").read_text("utf8")
    )
    hashes = []
    for entry in manifest["files"]:
        raw = (root / entry["path"]).read_bytes()
        controlled = raw.replace(b"\r\n", b"\n") if entry["representation"] == "UTF-8/LF" else raw
        blob = git("show", candidate + ":" + entry["path"], binary=True)
        blob_sha1 = hashlib.sha1(b"blob " + str(len(blob)).encode() + b"\0" + blob).hexdigest()
        assert len(controlled) == entry["bytes"], entry["path"]
        assert hashlib.sha256(controlled).hexdigest() == entry["sha256"], entry["path"]
        assert blob_sha1 == entry["git_blob_sha1"], entry["path"]
        assert blob == controlled, entry["path"]
        hashes.append(
            {
                "path": entry["path"],
                "raw_bytes": len(raw),
                "controlled_bytes": len(controlled),
                "matches_git": True,
            }
        )
    report["manifest_checks"] = hashes

    from lxml import html

    from analyse import proposisjon16 as t5
    from analyse import visningspilot as t1
    from innlesning.visningspilot_model import PilotSelection

    legacy_raw = gzip.decompress(
        (root / "tests/fixtures/t2/authentic-t1.json.gz").read_bytes()
    ).decode("utf8")
    old = t1.report_from_json(legacy_raw)
    basis = t5.import_basis(legacy_raw, root)
    data = t5.contents(basis)
    assert basis.t1_basis == old.basis
    assert len(basis.observations) == 105
    assert len(data.observations) == len({o.id for o in data.observations}) == 123
    assert all(
        o.round == "uavklart" for o in old.basis.observations if o.figure_type == "stortingsvedtak"
    )
    prop = next(d for d in data.documents if d.key == "prop16")
    assert prop.structured_coverage == "delvis_1429"
    assert basis.coverage[0].document_id == prop.id
    assert basis.coverage[0].table_fields == 111
    whole = t5.build_report(basis, PilotSelection(mode="document", document_id=prop.id))
    assert len(whole.view.observation_ids) == 111
    proposed = [o for o in data.observations if o.figure_type == "regjeringsforslag"]
    assert len(proposed) == 111 and len({o.chapter for o in proposed}) == 15
    assert sum(o.meaning == "endring" and int(o.chapter) < 3000 for o in proposed) == 27
    reference = json.loads(
        (root / "docs/research/to-visninger-37/originals/forgrening/inventory.json").read_text(
            "utf8"
        )
    )
    for entry in reference["account_comparison"]:
        if entry["proposal"] is None:
            continue
        observations = {
            o.meaning: o for o in proposed if (o.chapter + "/" + o.post) == entry["account"]
        }
        for meaning, key in (
            ("for_belop", "before"),
            ("endring", "delta"),
            ("etter_belop", "after"),
        ):
            assert observations[meaning].amount_kr == entry["proposal"][key]
    prop_items = [i for i in data.inventory if i.document_id == prop.id]
    accounts = sorted({(i.chapter, i.post) for i in prop_items})
    assert len(accounts) == 45 and ("1533", "45") in accounts
    table_accounts = {(i.chapter, i.post) for i in prop_items if i.role == "endringstabell"}
    assert len(table_accounts) == 37
    selections = []
    docs = {d.key: d.id for d in data.documents}
    for chapter, post in accounts:
        selection = PilotSelection(years=(2024,), accounts=((chapter, post),))
        selected = t5.build_report(basis, selection)
        expected = (
            (9, 3, 1)
            if chapter == "1429" and post in {"1", "22"}
            else (3, 0, 0)
            if (chapter, post) in table_accounts
            else (0, 0, 0)
        )
        actual = (
            len(selected.view.observation_ids),
            len(selected.view.adopted_observation_ids),
            len(selected.view.adopted_event_ids),
        )
        assert actual == expected, (chapter, post, actual, expected)
        assert t5.go_back(t5.open_document(selected, prop.id)) == selected
        assert t5.go_back(t5.open_accounts(whole, selection)) == whole
        if chapter == "1533":
            assert docs["inns95"] not in selected.view.document_ids
        selections.append(
            {"account": chapter + "/" + post, "counts": actual, "return_both_directions": True}
        )
    zero = next(
        o for o in proposed if (o.chapter, o.post, o.meaning) == ("4400", "2", "etter_belop")
    )
    assert (
        type(zero.amount_kr) is int
        and zero.amount_kr == 0
        and not dict(zero.null_reasons).get("amount_kr")
    )
    report["basis_id"] = basis.id
    report["all_45_selections"] = selections
    report["all_111_fields_match_independent_inventory"] = True
    report["authorizations"] = [
        {
            "roman": a.roman,
            "point": a.point,
            "period": a.period,
            "accounts": a.accounts,
            "frame": a.frame_kr,
            "raw_section_text": a.text,
        }
        for a in basis.authorizations
    ]

    # The formal branch endpoint must remain recoverable from preserved XML, while
    # current per-account selection must not import the untouched historical scope.
    assert len(basis.branches) == 8
    assert len(basis.authorizations) == 9
    assert len([a for a in basis.authorizations if a.roman == "IV"]) == 1
    assert len([b for b in basis.branches if b.point == "V.3" and b.committee_point == "II"]) == 1
    assert all("1533/45" not in b.accounts for b in basis.branches)
    report["branches"] = [asdict(b) for b in basis.branches]
    for a in basis.authorizations:
        nodes = html.fromstring(
            (root / "docs/research/omtale-o1/originals/prop16s-ch4.html")
            .read_bytes()
            .decode("utf8")
        ).xpath(a.locator)
        assert len(nodes) == 1
    if args.files:
        directory = args.files.resolve()
        ledger = json.loads((directory / "kontroll.json").read_text("utf8"))
        assert ledger["binding"]["candidate"] == candidate
        assert ledger["binding"]["base"] == base
        assert ledger["basis_id"] == basis.id
        expected_counts = {
            "utgift": (3, 0, 0),
            "inntekt-null": (3, 0, 0),
            "tekst": (0, 0, 0),
            "flere": (21, 6, 2),
            "tomt": (0, 0, 0),
            "hele-prop": (111, 0, 0),
            "post1": (9, 3, 1),
            "post22": (9, 3, 1),
            "begge": (18, 6, 2),
            "kontekst1533": (0, 0, 0),
            "konto-til-dokument": (111, 0, 0),
            "retur-konto": (21, 6, 2),
            "dokument-til-konto": (21, 6, 2),
            "retur-dokument": (111, 0, 0),
        }
        assert len(ledger["pairs"]) == len(expected_counts) == 14
        for pair in ledger["pairs"]:
            assert (
                pair["fields"],
                pair["adopted_fields"],
                pair["monetary_events"],
            ) == expected_counts[pair["name"]]
            for file in pair["files"]:
                raw = (directory / file["name"]).read_bytes()
                assert len(raw) == file["bytes"]
                assert hashlib.sha256(raw).hexdigest() == file["sha256"]
            parsed = json.loads((directory / (pair["name"] + ".json")).read_text("utf8"))
            assert (
                parsed["report"]["basis"]["t1_basis"] == json.loads(legacy_raw)["report"]["basis"]
            )
            assert len(parsed["report"]["basis"]["observations"]) == 105
            assert len(parsed["report"]["basis"]["sources"]) == 2
        recovery = json.loads(
            (root / "docs/research/proposisjon16-62/original-recovery.json").read_text("utf8")
        )
        for entry in recovery["files"]:
            raw = (directory / "originaler" / entry["path"]).read_bytes()
            assert len(raw) == entry["bytes"]
            assert hashlib.sha256(raw).hexdigest() == entry["sha256"]
        report["actual_files"] = {
            "directory": str(directory),
            "pair_count": len(ledger["pairs"]),
            "originals_exact": len(recovery["files"]),
            "ledger_sha256": hashlib.sha256((directory / "kontroll.json").read_bytes()).hexdigest(),
            "basis_capsule_exact_in_all_json": True,
        }
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(
        json.dumps(
            {
                "candidate": candidate,
                "tree": tree,
                "base": base,
                "manifest_files": len(hashes),
                "accounts_checked": len(accounts),
                "fields_checked": len(proposed),
                "output": str(output),
            }
        )
    )


if __name__ == "__main__":
    main()
