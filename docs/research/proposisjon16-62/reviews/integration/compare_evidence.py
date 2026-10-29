"""Compare helper replay and preservation evidence using explicit Git refs."""

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZipFile


def binding(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def load(path):
    return json.loads(path.read_text("utf8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf8")


def compare_xlsx(left, right):
    differences = []
    with ZipFile(left) as before, ZipFile(right) as after:
        assert before.namelist() == after.namelist()
        for name in before.namelist():
            old, new = before.read(name), after.read(name)
            entry = {"member": name}
            if old != new:
                assert name == "docProps/core.xml", name
                pattern = rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:[^>]*>)"
                entry["timestamp_elements_before"] = [
                    m.group().decode() for m in re.finditer(pattern, old)
                ]
                entry["timestamp_elements_after"] = [
                    m.group().decode() for m in re.finditer(pattern, new)
                ]
                assert len(entry["timestamp_elements_before"]) == 2
                assert len(entry["timestamp_elements_after"]) == 2
                assert re.sub(pattern, rb"\1__TIMESTAMP__\2", old) == re.sub(
                    pattern, rb"\1__TIMESTAMP__\2", new
                )
            first, second = before.getinfo(name), after.getinfo(name)
            assert all(
                getattr(first, field) == getattr(second, field)
                for field in (
                    "compress_type",
                    "flag_bits",
                    "external_attr",
                    "create_system",
                    "extra",
                    "comment",
                )
            )
            if first.date_time != second.date_time:
                entry["zip_date_time_before"] = first.date_time
                entry["zip_date_time_after"] = second.date_time
            if len(entry) > 1:
                differences.append(entry)
    return {
        "name": left.name,
        "original": binding(left),
        "integrated": binding(right),
        "all_member_payloads_equal_except_listed_core_timestamps": True,
        "differences": differences,
    }


class SplitImports(ast.NodeTransformer):
    def visit_ImportFrom(self, node):
        return [ast.ImportFrom(module=node.module, names=[n], level=node.level) for n in node.names]


class SortImportBlocks(ast.NodeTransformer):
    def generic_visit(self, node):
        node = super().generic_visit(node)
        for field, value in ast.iter_fields(node):
            if not isinstance(value, list):
                continue
            result, imports = [], []
            for item in [*value, None]:
                if isinstance(item, ast.Import | ast.ImportFrom):
                    imports.append(item)
                else:
                    result.extend(sorted(imports, key=ast.dump))
                    imports.clear()
                    if item is not None:
                        result.append(item)
            setattr(node, field, result)
        return node


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, replay, output = args.root.resolve(), args.replay.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    integration = Path(__file__).resolve().parent

    def git(ref):
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--verify", ref], text=True
        ).strip()

    candidate, base = git(args.candidate + "^{commit}"), git(args.base + "^{commit}")
    target = load(replay / "target.json")
    assert (target["candidate"], target["base"], target["tree"]) == (
        candidate,
        base,
        git(candidate + "^{tree}"),
    )
    mapping = load(integration / "original-helper-map.json")["files"]
    mapped = {row["path"]: row["original_path"] for row in mapping}
    baseline = load(integration / "baseline-files.json")["files"]
    unchanged = []
    for row in baseline:
        actual = binding(root / mapped.get(row["path"], row["path"]))
        assert actual == {k: row[k] for k in ("bytes", "sha256")}, row["path"]
        unchanged.append({"historical_path": row["path"], "verified_path": mapped.get(row["path"])})
    fix = root / "docs/research/proposisjon16-62/security-fix"
    historical = load(fix / "preserved-before.json")
    for row in historical:
        assert binding(root / mapped.get(row["path"], row["path"])) == {
            k: row[k] for k in ("bytes", "sha256")
        }, row["path"]
    fix_manifest = load(fix / "manifest.json")["files"]
    for row in fix_manifest:
        assert binding(root / row["path"]) == {k: row[k] for k in ("bytes", "sha256")}
    write(
        output / "preservation.json",
        {
            "baseline_bindings": len(unchanged),
            "current_paths_byte_identical": len(unchanged) - len(mapped),
            "archived_helper_paths_byte_identical": len(mapped),
            "historical_security_fix_preserved_before_bindings": len(historical),
            "historical_security_fix_manifest_bindings": len(fix_manifest),
            "helper_path_map": mapped,
            "note": "Security-fix path bindings describe the state before helper integration; "
            "the four helper entries are verified at their exact .original archives.",
        },
    )
    ast_results = []
    for row in mapping:
        old = ast.parse((root / row["original_path"]).read_text("utf8"))
        new = ast.parse((root / row["path"]).read_text("utf8"))
        exact = ast.dump(old) == ast.dump(new)
        canonical_old = SortImportBlocks().visit(SplitImports().visit(old))
        canonical_new = SortImportBlocks().visit(SplitImports().visit(new))
        imports_only = ast.dump(canonical_old) == ast.dump(canonical_new)
        assert imports_only, row["path"]
        ast_results.append(
            {
                "path": row["path"],
                "exact_ast_equal": exact,
                "ast_equal_after_splitting_and_sorting_contiguous_from_import_blocks": imports_only,
                "integrated_binding": binding(root / row["path"]),
                "original_binding": binding(root / row["original_path"]),
            }
        )
    write(output / "ast-comparison.json", ast_results)
    scratch = Path(target["target"]).parent
    xlsx_comparison = [
        compare_xlsx(scratch / "original-probes" / name, scratch / "integrated-probes" / name)
        for name in ("clean.xlsx", "accepted-theme-white.xlsx", "literal-long.xlsx")
    ]
    write(output / "generated-xlsx-comparison.json", xlsx_comparison)
    transformations = []
    comparisons = []

    def normalize(value, variant, pointer=""):
        if isinstance(value, dict):
            return {k: normalize(v, variant, pointer + "/" + k) for k, v in value.items()}
        if isinstance(value, list):
            return [normalize(v, variant, pointer + "/" + str(i)) for i, v in enumerate(value)]
        if isinstance(value, str):
            before = value
            artifacts = str(Path(target["target"]).parent / (variant + "-probes"))
            for path, label in ((artifacts, "<ARTIFACTS>"), (target["target"], "<TARGET>")):
                value = value.replace(path.replace("\\", "\\\\"), label).replace(path, label)
            if pointer == "/probes/63/detail":
                # The caller validates the named probe below before applying this exception.
                value = re.sub(r"<ARTIFACTS>(?:\\{1,2}|/)tmp[^\\/'\s]+\.json", "<TEMP_JSON>", value)
            if value != before:
                transformations.append(
                    {"variant": variant, "pointer": pointer, "before": before, "after": value}
                )
        return value

    excluded_artifact_fields = []
    for name in ("artifact-checks", "standards", "probes", "verified"):
        raw = {v: load(replay / (v + "-" + name + ".json")) for v in ("original", "integrated")}
        if name in ("probes", "verified"):
            for result in raw.values():
                assert result["probes"][63]["name"] == "atomic_no_clobber_race"
                assert result["probe_count"] == 70
                assert result["unexpected_acceptances"] == ["theme_integrity"]
        normalized = {v: normalize(data, v) for v, data in raw.items()}
        if name == "verified":
            for variant, data in normalized.items():
                for i, artifact in enumerate(data["artifacts"]):
                    if artifact["name"].endswith(".xlsx"):
                        excluded_artifact_fields.append(
                            {
                                "variant": variant,
                                "pointer": "/artifacts/" + str(i) + "/sha256",
                                "name": artifact["name"],
                                "sha256": artifact.pop("sha256"),
                            }
                        )
                        counterpart = next(
                            row for row in xlsx_comparison if row["name"] == artifact["name"]
                        )
                        if counterpart["original"]["bytes"] != counterpart["integrated"]["bytes"]:
                            excluded_artifact_fields.append(
                                {
                                    "variant": variant,
                                    "pointer": "/artifacts/" + str(i) + "/bytes",
                                    "name": artifact["name"],
                                    "bytes": artifact.pop("bytes"),
                                }
                            )
        equal = normalized["original"] == normalized["integrated"]
        comparisons.append({"helper": name, "all_remaining_fields_equal": equal})
        for variant, data in normalized.items():
            write(output / (variant + "-" + name + "-normalized.json"), data)
    write(
        output / "replay-comparison.json",
        {
            "candidate": candidate,
            "base": base,
            "tree": target["tree"],
            "comparisons": comparisons,
            "path_and_temporary_filename_substitutions": transformations,
            "excluded_generated_xlsx_artifact_fields": excluded_artifact_fields,
            "executions": load(replay / "executions.json"),
            "limits": "Helper equivalence on the historical candidate only. "
            "No new security acceptance of the P2-fixed working tree.",
        },
    )
    assert all(row["all_remaining_fields_equal"] for row in comparisons), comparisons
    print(json.dumps({"preserved": len(unchanged), "comparisons": comparisons}))


if __name__ == "__main__":
    main()
