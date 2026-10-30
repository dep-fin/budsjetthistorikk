"""Replay archived and integrated helpers on one explicit, isolated Git candidate.

The candidate must have the historical pre-theme-fix behavior expected by the
audit helpers. Use a published equivalent commit with the same tree if needed.
No checkout, index staging, commit, or historical output is modified.
"""

import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from zipfile import ZipFile


def binding(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, workspace, output = (
        args.root.resolve(),
        args.workspace.resolve(),
        args.output.resolve(),
    )
    assert not workspace.exists() and not output.exists()
    workspace.mkdir(parents=True)
    output.mkdir(parents=True)

    def git(*parts):
        return subprocess.check_output(["git", "-C", str(root), *parts])

    candidate = git("rev-parse", "--verify", args.candidate + "^{commit}").decode().strip()
    base = git("rev-parse", "--verify", args.base + "^{commit}").decode().strip()
    tree = git("rev-parse", candidate + "^{tree}").decode().strip()
    target = workspace / "target"
    target.mkdir()
    archive = git("archive", "--format=zip", candidate)
    with ZipFile(io.BytesIO(archive)) as bundle:
        assert all((target / name).resolve().is_relative_to(target) for name in bundle.namelist())
        bundle.extractall(target)

    # Private index copy plus explicit work tree prevents refreshing the source index.
    gitdir = Path(git("rev-parse", "--absolute-git-dir").decode().strip())
    index = workspace / "index"
    shutil.copyfile(gitdir / "index", index)
    environment = dict(os.environ)
    environment.update(
        GIT_DIR=str(gitdir),
        GIT_WORK_TREE=str(target),
        GIT_INDEX_FILE=str(index),
        GIT_OPTIONAL_LOCKS="0",
    )
    subprocess.run(
        ["git", "-C", str(target), "diff", "--quiet", candidate],
        env=environment,
        check=True,
    )
    reader = "analyse/proposisjon16_excel.py"
    candidate_reader = binding(target / reader)
    working_reader = binding(root / reader)
    identity = {
        "candidate": candidate,
        "tree": tree,
        "base": base,
        "target": str(target),
        "git_archive_sha256": hashlib.sha256(archive).hexdigest(),
        "candidate_reader": candidate_reader,
        "source_working_reader": working_reader,
        "source_working_reader_is_target": working_reader == candidate_reader,
        "source_index_before": binding(gitdir / "index"),
    }
    write_json(output / "target.json", identity)
    reviews = root / "docs/research/proposisjon16-62/reviews"
    executions = []

    def run(variant, name, relative, arguments):
        helper = reviews / relative
        if variant == "original":
            helper = helper.with_name(helper.name + ".original")
        command = [
            sys.executable,
            str(helper),
            "--root",
            str(target),
            "--candidate",
            candidate,
            "--base",
            base,
            *map(str, arguments),
        ]
        started = time.monotonic()
        result = subprocess.run(
            command,
            cwd=target,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        (output / (variant + "-" + name + ".log")).write_bytes(result.stdout)
        executions.append(
            {
                "variant": variant,
                "helper": str(helper),
                "helper_binding": binding(helper),
                "command": command,
                "exit_code": result.returncode,
                "seconds": round(time.monotonic() - started, 3),
            }
        )
        write_json(output / "executions.json", executions)
        assert result.returncode == 0, (variant, name, result.stdout[-3000:])

    for variant in ("original", "integrated"):
        run(
            variant,
            "artifact-checks",
            "security/artifact_checks.py",
            ["--output", output / (variant + "-artifact-checks.json")],
        )
        run(
            variant,
            "standards",
            "standards/controls.py",
            ["--output", output / (variant + "-standards.json")],
        )
        artifacts = workspace / (variant + "-probes")
        run(variant, "probes", "security/probes.py", ["--output", artifacts])
        shutil.copyfile(artifacts / "results.json", output / (variant + "-probes.json"))
        run(
            variant,
            "verified",
            "security/verify_outcomes.py",
            ["--artifacts", artifacts, "--output", output / (variant + "-verified.json")],
        )

    identity["source_index_after"] = binding(gitdir / "index")
    assert identity["source_index_before"] == identity["source_index_after"]
    identity["source_working_reader_after"] = binding(root / reader)
    assert identity["source_working_reader_after"] == working_reader
    subprocess.run(
        ["git", "-C", str(target), "diff", "--quiet", candidate],
        env=environment,
        check=True,
    )
    write_json(output / "target.json", identity)
    print(json.dumps({"executions": len(executions), "output": str(output)}))


if __name__ == "__main__":
    main()
