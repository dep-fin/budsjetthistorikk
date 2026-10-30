"""Independent public-boundary security probes for the frozen T6 candidate.

Run with python -m docs.research.innstilling95-64.reviews.security.audit_checks
from the repo root, with --output NEW_DIRECTORY. Product files are read only.
Large generated hostile artifacts stay in that explicitly chosen local directory.
"""

import argparse
import base64
import gzip
import hashlib
import json
import struct
import subprocess
import time
from dataclasses import asdict, fields, is_dataclass, replace
from pathlib import Path
from unittest.mock import patch
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.writer.theme import theme_xml

from analyse import innstilling95 as t6
from analyse import innstilling95_excel as excel
from analyse import proposisjon16 as t5
from analyse import visningspilot as t1
from analyse.omtale_excel_guard import inspect_excel
from innlesning import innstilling95 as adapter
from innlesning.observations import encode
from innlesning.omtale import identified
from innlesning.visningspilot import MAX_PARENT_BYTES, MAX_SOURCE_BYTES, raw_source

BASE = "9616fbe6a8ab15eec696f34de76888565a784f8f"
HEAD = "fc9b676ce6e2f361433f2562bcdf91930302c21e"
TREE = "93fee86f5b117c076136dd95d8d48b32fe1d1316"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SOURCE = Path(".local/full-acceptance/t6-files0")
NAMESPACES = {
    "sources": "source",
    "recipes": "recipe",
    "documents": "document",
    "inventory": "inventory",
    "statements": "statement",
    "contexts": "context",
    "relations": "relation",
    "bindings": "binding",
    "coverage": "coverage",
    "authorizations": "authorization",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args, binary=False):
    result = subprocess.check_output(["git", *args])
    return result if binary else result.decode("utf8").strip()


def remap(value, mapping):
    if isinstance(value, str):
        return mapping.get(value, value)
    if isinstance(value, tuple):
        return tuple(remap(v, mapping) for v in value)
    if is_dataclass(value):
        return replace(
            value, **{f.name: remap(getattr(value, f.name), mapping) for f in fields(value)}
        )
    return value


def rehash(basis):
    """Rebind all new object hashes/references until the acyclic graph is stable."""
    for _ in range(8):
        changes, mapping = {}, {}
        for field, namespace in NAMESPACES.items():
            rewritten = tuple(
                identified("innstilling95-" + namespace, o) for o in getattr(basis, field)
            )
            changes[field] = rewritten
            mapping.update(
                (old.id, new.id)
                for old, new in zip(getattr(basis, field), rewritten, strict=True)
                if old.id != new.id
            )
        basis = replace(basis, **changes)
        if not mapping:
            return identified("innstilling95-basis", basis)
        basis = replace(
            basis,
            **{
                field: remap(getattr(basis, field), mapping)
                for field in (*NAMESPACES, "observations")
            },
        )
    raise AssertionError("Unexpected identity cycle in probe")


def poison(basis, name):
    if name in {
        "amount",
        "arithmetic",
        "role",
        "author",
        "year",
        "account",
        "meaning",
        "currency",
        "multiplier",
        "round",
        "scope",
        "sourceunit",
        "raw",
        "pointer",
        "monetary",
    }:
        target = next(
            o
            for o in basis.observations
            if (o.source_unit_id, o.chapter, o.post, o.meaning)
            == ("inns95", "4400", "2", "etter_belop")
        )
        changes = {
            "amount": {"amount_kr": 1},
            "arithmetic": {"amount_kr": 1},
            "role": {"proposal_role": "alternativ"},
            "author": {"proposal_author": "stortinget"},
            "year": {"budget_year": 2025},
            "account": {"chapter": "1429", "post": "22"},
            "meaning": {"meaning": "endring"},
            "currency": {"currency": "EUR"},
            "multiplier": {"multiplier": "1000"},
            "round": {"round": "opprinnelig"},
            "scope": {"scope": "helaar"},
            "sourceunit": {"source_unit_id": "vedtak359"},
            "raw": {"raw_value": "1", "amount_text": "1"},
            "pointer": {"pointer": replace(target.pointer, amount_field="endring")},
            "monetary": {"information_type": "fullmakt", "figure_type": "stortingsvedtak"},
        }[name]
        new = replace(target, **changes)
        obs = tuple(new if o == target else o for o in basis.observations)
        if name == "arithmetic":
            obs = tuple(
                replace(o, amount_kr=o.amount_kr + 1)
                if o.source_unit_id == "inns95"
                and o.chapter == "4400"
                and o.post == "2"
                and o.meaning == "for_belop"
                else o
                for o in obs
            )
        basis = replace(basis, observations=obs)
        if new.id != target.id:
            basis = replace(
                basis,
                **{
                    field: remap(getattr(basis, field), {target.id: new.id}) for field in NAMESPACES
                },
            )
    elif name == "null32":
        prop = next(o for o in basis.t5_basis.observations if o.meaning == "endring")
        fake = replace(prop, chapter="1420", post="32", amount_kr=0)
        basis = replace(basis, observations=basis.observations + (fake,))
    elif name in {"frame", "roman", "authorization_role"}:
        auth = next(a for a in basis.authorizations if a.roman == "IV")
        if name == "frame":
            replacement = tuple(replace(auth, accounts=(account,)) for account in auth.accounts)
            basis = replace(
                basis,
                authorizations=tuple(a for a in basis.authorizations if a != auth) + replacement,
            )
        else:
            changed = replace(
                auth, **({"roman": "V"} if name == "roman" else {"role": "vedtak:bevilgningsdelta"})
            )
            basis = replace(
                basis,
                authorizations=tuple(changed if a == auth else a for a in basis.authorizations),
            )
    elif name == "branch":
        r = basis.relations[0]
        basis = replace(
            basis,
            relations=(
                replace(r, accounts=r.accounts + ("1429/1", "1533/45")),
                *basis.relations[1:],
            ),
        )
    elif name == "coverage":
        c = basis.coverage[0]
        basis = replace(
            basis, coverage=(replace(c, status="full_faglig_aarsdekning"), *basis.coverage[1:])
        )
    elif name == "hidden":
        basis = replace(basis, issues=())
    elif name == "correction":
        basis = replace(basis, issues=("uberiktiget95_rekonstruert",))
    elif name == "old":
        old = basis.t5_basis.t1_basis
        old = identified("visningsgrunnlag-1", replace(old, issues=()))
        prior = identified("proposisjonsgrunnlag16-1", replace(basis.t5_basis, t1_basis=old))
        basis = replace(basis, t5_basis=prior)
    elif name == "recipe":
        r = basis.recipes[0]
        basis = replace(
            basis, recipes=(replace(r, object_start=r.object_start + 1), *basis.recipes[1:])
        )
    elif name == "traversal":
        s = basis.sources[0]
        basis = replace(basis, sources=(replace(s, name="../../outside.json"), *basis.sources[1:]))
    else:
        raise AssertionError(name)
    return rehash(basis)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    results = []

    def run(name, fn, expect="pass"):
        started = time.monotonic()
        try:
            detail = fn()
            if is_dataclass(detail):
                detail = {"report_id": detail.id}
            result = "accepted" if expect == "reject" else "pass"
        except (ValueError, OSError, etree.LxmlError, StopIteration) as error:
            detail = {"error": type(error).__name__, "message": str(error)}
            result = "rejected" if expect == "reject" else "error"
        except Exception as error:
            detail = {"error": type(error).__name__, "message": str(error)}
            result = "error"
        row = {
            "name": name,
            "expected": expect,
            "result": result,
            "detail": detail,
            "seconds": round(time.monotonic() - started, 3),
        }
        results.append(row)
        print(json.dumps({"name": name, "result": result}, ensure_ascii=False), flush=True)
        (args.output / "results.json").write_text(
            json.dumps(
                {"base": BASE, "head": HEAD, "tree": TREE, "results": results},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf8",
            newline="\n",
        )

    assert git("rev-parse", "HEAD") == HEAD
    assert git("rev-parse", "HEAD^{tree}") == TREE
    baseline_status = git("diff", "--name-only", "HEAD")
    input_json, input_excel = SOURCE / "tomt.json", SOURCE / "tomt.xlsx"
    report = t6.read_json(input_json)
    raw = input_json.read_text("utf8")
    source_hashes = {str(p): digest(p.read_bytes()) for p in (input_json, input_excel)}
    files = {}
    with ZipFile(input_excel) as archive:
        files = {n: archive.read(n) for n in archive.namelist()}

    def baseline():
        assert excel.read_excel(input_excel) == report
        old = t5.report_from_json(
            gzip.decompress(Path("tests/fixtures/t6/authentic-t5.json.gz").read_bytes()).decode()
        )
        original = t1.report_from_json(
            gzip.decompress(Path("tests/fixtures/t2/authentic-t1.json.gz").read_bytes()).decode()
        )
        assert old.basis == report.basis.t5_basis
        assert old.basis.t1_basis == original.basis
        data = t6.contents(report.basis)
        assert len(data.observations) == 339
        assert sum(o.figure_type == "stortingsvedtak" for o in data.observations) == 114
        assert (
            len({o.step_id for o in data.observations if o.figure_type == "stortingsvedtak"}) == 38
        )
        return {"fields": 339, "adopted_fields": 114, "events": 38, "typed_legacy_equal": True}

    run("valid_public_read_and_authentic_legacy", baseline)

    def preservation():
        before = {
            line.split("\t", 1)[1]: line.split()[2]
            for line in git("ls-tree", "-r", BASE).splitlines()
        }
        current = {
            line.split("\t", 1)[1]: line.split()[2]
            for line in git("ls-tree", "-r", HEAD).splitlines()
        }
        changed = [p for p, blob in before.items() if current.get(p) != blob]
        assert changed == ["AGENTS.md"]
        assert git("diff", BASE, HEAD, "--", "AGENTS.md").count("\n+") == 3
        return {"base_files": len(before), "unchanged": len(before) - 1, "only_changed": changed}

    run("all_base_blobs_preserved_except_additive_agents", preservation)

    def original_check():
        target = args.output / "originals"
        excel.export_originals(report, target)
        for recipe in report.basis.recipes:
            original = Path(adapter.ROOT) / (
                str(40034220 + int(recipe.document_key[6:]) - 359) + ".xml"
            )
            assert (
                adapter.reconstruct(report.basis.t5_basis, report.basis.sources, recipe)
                == original.read_bytes()
            )
            assert (target / "vedtak" / original.name).read_bytes() == original.read_bytes()
        assert len(list(p for p in target.rglob("*") if p.is_file())) == 42
        return {"actual_export_files": 42, "reconstructed_xml": 6, "byte_exact": True}

    run("offline_originals_and_six_recipes", original_check)
    run(
        "original_directory_no_clobber",
        lambda: excel.export_originals(report, args.output / "originals"),
        "reject",
    )

    semantic = (
        "amount",
        "arithmetic",
        "role",
        "author",
        "year",
        "account",
        "meaning",
        "currency",
        "multiplier",
        "round",
        "scope",
        "sourceunit",
        "raw",
        "pointer",
        "monetary",
        "null32",
        "frame",
        "roman",
        "authorization_role",
        "branch",
        "coverage",
        "hidden",
        "correction",
        "old",
        "recipe",
    )
    for name in semantic:
        basis = poison(report.basis, name)
        poisoned = identified("innstilling95-1", replace(report, basis=basis))
        frozen = encode({"format": "innstilling95-1", "report": asdict(poisoned)})
        json_path = args.output / ("semantic-" + name + ".json")
        json_path.write_text(frozen, encoding="utf8")
        run("semantic_json_" + name, lambda p=json_path: t6.read_json(p), "reject")
        book = excel._book(poisoned, frozen)
        xlsx_path = args.output / ("semantic-" + name + ".xlsx")
        book.save(xlsx_path)
        book.close()
        extracted = inspect_excel(
            xlsx_path,
            sheet_names=excel.SHEET_NAMES,
            snapshot_name="Visningsgrunnlag",
            max_expanded_bytes=128 * 1024 * 1024,
        )[0]
        assert extracted == frozen
        run("semantic_xlsx_" + name, lambda p=xlsx_path: excel.read_excel(p), "reject")

    def zip_probe(name, mutator, expect="reject"):
        changed = dict(files)
        mutator(changed)
        path = args.output / ("package-" + name + ".xlsx")
        with ZipFile(path, "w", ZIP_DEFLATED) as archive:
            for n, content in changed.items():
                archive.writestr(n, content)
        run("xlsx_" + name, lambda: excel.read_excel(path), expect)

    def mutate_xml(container, name, fn):
        tree = etree.fromstring(container[name])
        fn(tree)
        container[name] = etree.tostring(tree)

    zip_probe(
        "theme_white",
        lambda f: f.__setitem__(
            "xl/theme/theme1.xml",
            theme_xml.encode().replace(b'lastClr="000000"', b'lastClr="FFFFFF"'),
        ),
    )
    zip_probe(
        "theme_wingdings",
        lambda f: f.__setitem__(
            "xl/theme/theme1.xml",
            theme_xml.encode().replace(b'typeface="Calibri"', b'typeface="Wingdings"'),
        ),
    )
    zip_probe(
        "theme_bom",
        lambda f: f.__setitem__("xl/theme/theme1.xml", b"\xef\xbb\xbf" + f["xl/theme/theme1.xml"]),
    )
    zip_probe("path_traversal", lambda f: f.__setitem__("../outside.xml", b"x"))
    zip_probe("unknown_member", lambda f: f.__setitem__("xl/vbaProject.bin", b"x"))
    zip_probe(
        "doctype",
        lambda f: f.__setitem__(
            "xl/workbook.xml",
            b'<!DOCTYPE workbook [<!ENTITY x SYSTEM "file:///C:/Windows/win.ini">]>'
            + f["xl/workbook.xml"],
        ),
    )
    zip_probe(
        "worksheet_doctype",
        lambda f: f.__setitem__(
            "xl/worksheets/sheet1.xml",
            b'<!DOCTYPE worksheet [<!ENTITY x "unsafe">]>' + f["xl/worksheets/sheet1.xml"],
        ),
    )
    zip_probe(
        "external_theme",
        lambda f: f.__setitem__(
            "xl/_rels/workbook.xml.rels",
            f["xl/_rels/workbook.xml.rels"].replace(
                b'Target="theme/theme1.xml"',
                b'Target="https://example.invalid/theme.xml" TargetMode="External"',
            ),
        ),
    )
    zip_probe(
        "numeric_as_string",
        lambda f: mutate_xml(
            f,
            "xl/worksheets/sheet3.xml",
            lambda tree: next(n for n in tree.iter(S + "c") if n.get("t") == "n").set("t", "str"),
        ),
    )
    zip_probe(
        "formula",
        lambda f: mutate_xml(
            f,
            "xl/worksheets/sheet1.xml",
            lambda tree: next(tree.iter(S + "c")).append(etree.Element(S + "f")),
        ),
    )
    zip_probe(
        "hidden_sheet",
        lambda f: mutate_xml(
            f, "xl/workbook.xml", lambda tree: tree.find(S + "sheets")[0].set("state", "veryHidden")
        ),
    )
    zip_probe(
        "hidden_row",
        lambda f: mutate_xml(
            f,
            "xl/worksheets/sheet1.xml",
            lambda tree: next(tree.iter(S + "row")).set("hidden", "1"),
        ),
    )
    zip_probe(
        "style_applyfont",
        lambda f: mutate_xml(
            f, "xl/styles.xml", lambda tree: tree.find(S + "cellXfs")[0].set("applyFont", "0")
        ),
    )
    zip_probe(
        "oversized_coordinate",
        lambda f: mutate_xml(
            f, "xl/worksheets/sheet1.xml", lambda tree: next(tree.iter(S + "c")).set("r", "A20001")
        ),
    )
    zip_probe(
        "extra_cell_attribute",
        lambda f: mutate_xml(
            f, "xl/worksheets/sheet1.xml", lambda tree: next(tree.iter(S + "c")).set("hidden", "1")
        ),
    )

    # Deliberate ancillary print/outline mutations: record actual acceptance,
    # without treating an unchanged on-screen cell grid as a semantic forgery.
    zip_probe(
        "changed_print_margins",
        lambda f: mutate_xml(
            f,
            "xl/worksheets/sheet1.xml",
            lambda tree: tree.find(S + "pageMargins").set("left", "1000"),
        ),
        "observe",
    )
    zip_probe(
        "changed_outline_direction",
        lambda f: mutate_xml(
            f,
            "xl/worksheets/sheet1.xml",
            lambda tree: tree.find(S + "sheetPr/" + S + "outlinePr").set("summaryBelow", "0"),
        ),
        "observe",
    )

    for name, change in {
        "internal_hyperlink": lambda b: setattr(
            b["Forløp"]["B2"].hyperlink, "location", "'Dokumenter'!B3"
        ),
        "external_hyperlink": lambda b: setattr(
            b["Forløp"]["B2"], "hyperlink", "https://example.invalid/unsafe"
        ),
        "number_format_hide": lambda b: setattr(b["Forløp"]["G2"], "number_format", ";;;"),
        "white_font": lambda b: setattr(b["T6-dekning"]["E2"], "font", Font(color="FFFFFF")),
        "zero_row_height": lambda b: setattr(b["T6-dekning"].row_dimensions[2], "height", 0),
        "chunk_index": lambda b: setattr(b["Visningsgrunnlag"]["A2"], "value", 2),
    }.items():
        book = load_workbook(SOURCE / "null.xlsx")
        change(book)
        target = args.output / ("presentation-" + name + ".xlsx")
        book.save(target)
        book.close()
        run("xlsx_" + name, lambda p=target: excel.read_excel(p), "reject")

    for name, text in {
        "duplicate_key": '{"format":"innstilling95-1","format":"innstilling95-1","report":{}}',
        "nan": '{"format":"innstilling95-1","report":NaN}',
        "infinity": '{"format":"innstilling95-1","report":Infinity}',
        "extra_key": raw[:-1] + ',"extra":true}',
        "deep": "[" * 1100 + "0" + "]" * 1100,
        "boundary64": " " * t6.MAX_REPORT_BYTES,
        "over64": " " * (t6.MAX_REPORT_BYTES + 1),
    }.items():
        run("json_" + name, lambda text=text: t6.report_from_json(text), "reject")
    typed = json.loads(raw)
    typed["report"]["basis"]["coverage"][0]["table_fields"] = True
    run("json_bool_as_int", lambda: t6.report_from_json(encode(typed)), "reject")

    source = report.basis.sources[0]
    for name, content in (
        ("exact16", b"x" * MAX_SOURCE_BYTES),
        ("over16", b"x" * (MAX_SOURCE_BYTES + 1)),
    ):
        candidate = replace(
            source,
            content_base64=base64.b64encode(content).decode(),
            sha256=digest(content),
            byte_count=len(content),
        )
        run(
            "payload_" + name,
            lambda s=candidate: {"length": len(raw_source(s))},
            "pass" if name == "exact16" else "reject",
        )
    run(
        "payload_invalid_base64",
        lambda: raw_source(replace(source, content_base64="!!!!")),
        "reject",
    )

    # Exercise the actual bounded gzip reader directly with a synthetic parent.
    # Full public validation additionally pins the historical gzip before this.
    parent = next(
        s
        for s in report.basis.t5_basis.t1_basis.sources
        if s.document_key == "forelder2024" and s.media_type == "application/gzip"
    )
    bomb = gzip.compress(b"x" * (MAX_PARENT_BYTES + 1), mtime=0)
    fake = replace(
        parent,
        content_base64=base64.b64encode(bomb).decode(),
        sha256=digest(bomb),
        byte_count=len(bomb),
    )
    old = report.basis.t5_basis.t1_basis
    fake_t5 = replace(
        report.basis.t5_basis,
        t1_basis=replace(old, sources=tuple(fake if s == parent else s for s in old.sources)),
    )
    run("gzip_over32_bounded_parent", lambda: adapter._parent(fake_t5), "reject")

    total = sum(len(v) for v in files.values())
    run(
        "zip_exact_expansion_gate",
        lambda: {
            "snapshot_bytes": len(
                inspect_excel(
                    input_excel,
                    sheet_names=excel.SHEET_NAMES,
                    snapshot_name="Visningsgrunnlag",
                    max_expanded_bytes=total,
                )[0].encode()
            ),
            "expanded_bytes": total,
        },
    )
    run(
        "zip_over_expansion_gate",
        lambda: inspect_excel(
            input_excel,
            sheet_names=excel.SHEET_NAMES,
            snapshot_name="Visningsgrunnlag",
            max_expanded_bytes=total - 1,
        ),
        "reject",
    )
    duplicate = args.output / "duplicate-member.xlsx"
    with ZipFile(duplicate, "w", ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
        archive.writestr("xl/workbook.xml", files["xl/workbook.xml"])
    run("zip_duplicate_member", lambda: excel.read_excel(duplicate), "reject")

    # Forge only the central-directory expanded size. The guard must reject it
    # before any XML member is read or decompressed.
    declared = bytearray(input_excel.read_bytes())
    offset = declared.index(b"PK\x01\x02")
    struct.pack_into("<I", declared, offset + 24, 128 * 1024 * 1024 + 1)
    declared_path = args.output / "declared-over128.xlsx"
    declared_path.write_bytes(declared)
    run("zip_declared_over128", lambda: excel.read_excel(declared_path), "reject")

    def no_clobber(kind, race=False):
        target = args.output / (
            "no-clobber-"
            + kind
            + ("-race" if race else "")
            + (".json" if kind == "json" else ".xlsx")
        )
        sentinel = b"existing-user-data"
        writer, module = (t6.export_json, t6) if kind == "json" else (excel.export_excel, excel)
        publish = module._publish
        if race:

            def collision(temporary, output):
                output.write_bytes(sentinel)
                publish(temporary, output)

            with patch.object(module, "_publish", collision):
                try:
                    writer(report, target)
                except FileExistsError:
                    pass
                else:
                    raise AssertionError("Publication overwrote concurrent existing file")
        else:
            target.write_bytes(sentinel)
            try:
                writer(report, target)
            except ValueError:
                pass
            else:
                raise AssertionError("Writer accepted existing output")
        assert target.read_bytes() == sentinel
        return {"unchanged_existing_bytes": True, "simulated_publish_collision": race}

    for kind in ("json", "excel"):
        run(kind + "_existing_no_clobber", lambda kind=kind: no_clobber(kind))
        run(kind + "_publish_race_no_clobber", lambda kind=kind: no_clobber(kind, True))

    traversal = identified(
        "innstilling95-1", replace(report, basis=poison(report.basis, "traversal"))
    )
    run(
        "original_traversal_rejected_before_write",
        lambda: excel.export_originals(traversal, args.output / "bad-originals"),
        "reject",
    )
    assert not (args.output / "bad-originals").exists()

    def cold_offline():
        def forbidden(*_args, **_kwargs):
            raise AssertionError("Unexpected network/database access")

        import socket
        import sqlite3

        for fn in (adapter._parent, adapter.structure_basis, t6.contents):
            fn.cache_clear()
        with patch.object(socket, "socket", forbidden), patch.object(sqlite3, "connect", forbidden):
            assert t6.read_json(input_json) == excel.read_excel(input_excel) == report
        return {"network_and_sqlite_forbidden": True, "cold_caches": True}

    run("cold_offline_public_read", cold_offline)
    assert source_hashes == {str(p): digest(p.read_bytes()) for p in (input_json, input_excel)}
    assert git("diff", "--name-only", "HEAD") == baseline_status
    assert git("rev-parse", "HEAD") == HEAD
    summary = {
        "base": BASE,
        "head": HEAD,
        "tree": TREE,
        "groups": len(results),
        "unexpected": [r for r in results if r["result"] in {"error", "accepted"}],
        "observed_only": [r for r in results if r["expected"] == "observe"],
        "input_hashes_unchanged": source_hashes,
        "tracked_worktree_diff_unchanged": True,
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf8", newline="\n"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
