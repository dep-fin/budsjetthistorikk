"""Avgrenset, offline sikkerhetskontroll av fast kandidat for #54.

Skriver bare i denne auditmappen. Ingen HTTP, installasjon eller produktimport.
Kontrollagentens originalskript kjøres uendret; bare resultatmappen omdirigeres.
"""

from __future__ import annotations

import ast
import contextlib
import hashlib
import io
import json
import platform
import re
import runpy
import socket
import subprocess
import sys
import zlib
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

import lxml
import pypdf
from lxml import etree, html
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RESEARCH = ROOT / "docs/research/r2-101000-54"
BASE = "6b2441ee5e859d103ab44d78f12d33c374a89171"
CANDIDATE = "7af3153bda95726ac93d0780b918ae95440bae2d"
MAX_BODY = 32 * 1024 * 1024
CHECKS = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(name, condition, detail=None):
    CHECKS.append({"check": name, "passed": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError(name)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def safe_path(parent, name):
    path = (parent / name).resolve()
    check("manifest path stays in repository", path.is_relative_to(ROOT), name)
    return path


def bounded_gzip(data):
    dec = zlib.decompressobj(wbits=31)
    body = dec.decompress(data, MAX_BODY + 1)
    check("bounded gzip body", len(body) <= MAX_BODY and not dec.unconsumed_tail)
    check("single complete gzip member", dec.eof and not dec.unused_data)
    return body


def main():
    check("fixed HEAD", git("rev-parse", "HEAD").decode().strip() == CANDIDATE)
    check(
        "base ancestor",
        subprocess.run(["git", "merge-base", "--is-ancestor", BASE, CANDIDATE], cwd=ROOT).returncode
        == 0,
    )
    changed = git("diff", "--name-only", BASE + "..." + CANDIDATE).decode().splitlines()
    check(
        "whole candidate limited to research and pointers",
        all(
            p in ["AGENTS.md", "docs/kildefunn.md"] or p.startswith("docs/research/r2-101000-54/")
            for p in changed
        ),
        changed,
    )
    file_bindings = []
    secret_scan = []
    secret_patterns = [
        ("private key", rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        ("GitHub token", rb"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})\b"),
        ("AWS access key", rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
        ("Slack token", rb"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    ]
    for name in changed:
        committed = git("show", CANDIDATE + ":" + name)
        actual = (ROOT / name).read_bytes()
        representation = "exact bytes"
        if name in ["AGENTS.md", "docs/kildefunn.md"]:
            actual = actual.replace(b"\r\n", b"\n")
            representation = "UTF-8 LF for pointer documents"
        check("checkout equals fixed candidate", actual == committed, name)
        mode = git("ls-tree", CANDIDATE, "--", name).decode().split()[0]
        check("ordinary non-executable file", mode == "100644", name)
        file_bindings.append(
            {
                "path": name,
                "bytes": len(committed),
                "sha256": sha(committed),
                "git_mode": mode,
                "representation": representation,
            }
        )
        content = bounded_gzip(committed) if name.endswith(".gz") else committed
        for label, pattern in secret_patterns:
            if re.search(pattern, content):
                secret_scan.append({"path": name, "kind": label})
    check("no high confidence secret patterns", not secret_scan, secret_scan)
    for name in [
        "requirements.txt",
        "requirements-dev.txt",
        "innlesning",
        "analyse",
        "drift",
        "tests",
        ".github",
        "docs/research/k3-arsinventar-50",
        "docs/research/perioderegister-52",
    ]:
        check(
            "protected tree unchanged",
            not git("diff", "--name-only", BASE, CANDIDATE, "--", name),
            name,
        )

    sources = json.loads((RESEARCH / "source-manifest.json").read_bytes())["sources"]
    bindings = []
    metadata_summary = {
        "header_names": Counter(),
        "query_names": Counter(),
        "hosts": Counter(),
        "local_machine_fields": Counter(),
        "credentials_found": [],
        "sensitive_headers_found": [],
    }
    bodies = {}
    for row in sources:
        archive = safe_path(RESEARCH, row["archive"]).read_bytes()
        raw_meta = safe_path(RESEARCH, row["metadata"]).read_bytes()
        check(
            "archive pinned",
            sha(archive) == row["archive_sha256"] and len(archive) == row["archive_bytes"],
            row["id"],
        )
        check(
            "metadata pinned",
            sha(raw_meta) == row["metadata_sha256"] and len(raw_meta) == row["metadata_bytes"],
            row["id"],
        )
        body = bounded_gzip(archive)
        meta = json.loads(raw_meta)
        check(
            "body pinned",
            sha(body) == row["sha256"] == meta["body_sha256"]
            and len(body) == row["bytes"] == meta["body_bytes"],
            row["id"],
        )
        bodies[row["id"]] = body
        tr = meta["transport"]
        for key in ["local_ip", "filename_effective"]:
            if tr.get(key):
                metadata_summary["local_machine_fields"][key] += 1
        for key in ["url.user", "url.password", "urle.user", "urle.password"]:
            if tr.get(key):
                metadata_summary["credentials_found"].append([row["id"], key])
        for line in meta["response_headers_without_cookie"]:
            name, sep, value = line.partition(":")
            if sep:
                metadata_summary["header_names"][name.lower()] += 1
                if re.search(r"cookie|authorization|token|secret|api[-_]key", name, re.I):
                    metadata_summary["sensitive_headers_found"].append([row["id"], name])
        for key in ["requested_url", "final_url"]:
            url = urlsplit(row[key])
            check(
                "official HTTPS source",
                url.scheme == "https"
                and url.hostname
                in ["data.stortinget.no", "www.stortinget.no", "www.regjeringen.no"],
                row["id"],
            )
            check("no URL credentials", url.username is None and url.password is None)
            check(
                "ordinary public query parameters",
                all(
                    k in ["all", "ch", "sakid", "voteringid", "m"] for k, v in parse_qsl(url.query)
                ),
            )
        url = urlsplit(row["requested_url"])
        metadata_summary["hosts"][url.hostname] += 1
        metadata_summary["query_names"].update(k for k, v in parse_qsl(url.query))
        if row["http_complete"]:
            check(
                "successful TLS GET capture",
                tr["http_code"] == 200
                and tr["method"] == "GET"
                and tr["ssl_verify_result"] == 0
                and tr["size_upload"] == 0,
            )
        else:
            check(
                "failed capture empty",
                row["id"] == "sak101000.xml" and not body and meta["curl_exit"] == 6,
            )
        check("no private key in metadata", b"PRIVATE KEY-----" not in raw_meta)
        if body and row["id"].endswith(".xml"):
            check(
                "XML has no document type or entity declaration",
                not re.search(rb"<!\s*(?:DOCTYPE|ENTITY)\b", body, re.I),
                row["id"],
            )
            etree.fromstring(body, etree.XMLParser(resolve_entities=False, no_network=True))
        elif body and row["id"].endswith(".html"):
            html.fromstring(body.decode("utf-8"))
        bindings.append(
            {
                "id": row["id"],
                "archive_bytes": len(archive),
                "body_bytes": len(body),
                "body_sha256": sha(body),
                "status": row["status"],
            }
        )
    check("no credentials in transport fields", not metadata_summary["credentials_found"])
    check("no sensitive response header names", not metadata_summary["sensitive_headers_found"])
    check("expected source count", len(bindings) == 22)

    reused = json.loads((RESEARCH / "reused-sources.json").read_bytes())["files"]
    for row in reused:
        data = safe_path(ROOT, row["path"]).read_bytes()
        check(
            "reused file pinned",
            sha(data) == row["sha256"] and len(data) == row["bytes"],
            row["path"],
        )
        if "body_sha256" in row:
            body = bounded_gzip(data)
            check(
                "reused body pinned",
                sha(body) == row["body_sha256"] and len(body) == row["body_bytes"],
                row["path"],
            )
    evidence = json.loads((RESEARCH / "evidence.json").read_bytes())
    for name in evidence["sources"].values():
        safe_path(ROOT, name)
    for name in json.loads((RESEARCH / "source-comparison.json").read_bytes())["parents"]:
        safe_path(ROOT, name)
    for row in json.loads((RESEARCH / "delivery-manifest.json").read_bytes())["files"]:
        safe_path(ROOT, row["path"])

    # Små ufarlige parserprøver. Ingen eksterne ressursadresser eller lokale filer.
    tree = etree.fromstring(
        b'<!DOCTYPE r [<!ENTITY example "sentinel">]><r>&example;</r>',
        etree.XMLParser(resolve_entities=False, no_network=True),
    )
    check(
        "XML entity remains unresolved",
        tree.text is None and len(tree) == 1 and isinstance(tree[0], etree._Entity),
    )
    h = html.fromstring('<div><script>audit_marker = 1</script><img src="unfetched.png"></div>')
    check(
        "HTML treated as inert tree",
        len(h.xpath(".//script")) == 1 and h.xpath(".//img")[0].get("src") == "unfetched.png",
    )
    check("HTML parser defaults forbid network", "no_network=True" in etree.HTMLParser.__doc__)

    pdf = PdfReader(io.BytesIO(bodies["prop34.pdf"]))
    active_names = {"/JavaScript", "/JS", "/AA", "/Launch", "/EmbeddedFiles", "/RichMedia"}
    active = []
    local_open_actions = []
    checked_pdf_objects = 0
    for generation, entries in pdf.xref.items():
        if generation == 65535:
            continue
        for number in entries:
            obj = pypdf.generic.IndirectObject(number, generation, pdf).get_object()
            checked_pdf_objects += 1
            if isinstance(obj, dict):
                if "/OpenAction" in obj:
                    action = obj["/OpenAction"].get_object()
                    check(
                        "PDF open action is local page destination",
                        isinstance(action, dict)
                        and action.get("/S") == "/GoTo"
                        and set(action) == {"/D", "/S"},
                    )
                    local_open_actions.append(
                        {
                            "object": number,
                            "generation": generation,
                            "action": "/GoTo",
                            "destination_mode": str(action["/D"][-1]),
                        }
                    )
                for key in obj:
                    if str(key) in active_names:
                        active.append({"object": number, "generation": generation, "key": str(key)})
    check("PDF no active action or embedded file dictionary keys", not active, active)
    check(
        "PDF four readable text pages",
        len(pdf.pages) == 4 and all(page.extract_text() for page in pdf.pages),
    )

    script = RESEARCH / "reviews/source-control/verify_sources.py"
    reproduction = (RESEARCH / "reproduksjon.md").read_text("utf-8")
    codeblocks = re.findall(r"```python\n(.*?)\n```", reproduction, re.S)
    check("one reproduction codeblock", len(codeblocks) == 1)
    code_summary = []
    for name, code in [
        (str(script.relative_to(ROOT)), script.read_text("utf-8")),
        ("reproduksjon.md python block", codeblocks[0]),
    ]:
        tree = ast.parse(code)
        imports = []
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports += [n.name for n in node.names]
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
            elif isinstance(node, ast.Call):
                calls.append(ast.unparse(node.func))
        check(
            "no product imports",
            not any(n.split(".")[0] in ["innlesning", "analyse", "drift"] for n in imports),
            name,
        )
        check(
            "no dynamic execution or deserialization calls",
            not any(
                n
                in [
                    "exec",
                    "eval",
                    "compile",
                    "os.system",
                    "pickle.loads",
                    "pickle.load",
                    "yaml.load",
                ]
                for n in calls
            ),
            name,
        )
        check(
            "no shell subprocess argument",
            not any(isinstance(n, ast.keyword) and n.arg == "shell" for n in ast.walk(tree)),
            name,
        )
        code_summary.append(
            {
                "path": name,
                "sha256": sha(code.encode("utf-8")),
                "imports": sorted(set(imports)),
                "calls": sorted(set(calls)),
            }
        )

    # Kjør den uendrede kontrollkoden med fast publisert rårot. Den faste
    # resultatfilen omdirigeres hit for å bevare agentens kildekontrollbevis.
    namespace = runpy.run_path(str(script))
    namespace["main"].__globals__["HERE"] = HERE
    io_events = []
    process_events = []
    pending_process = {"argv": None}
    original_popen = subprocess.Popen

    def controlled_popen(argv, *args, **kwargs):
        if (
            not isinstance(argv, list)
            or Path(argv[0]).name not in ["git", "git.exe"]
            or argv[1] not in ["rev-parse", "merge-base", "show", "ls-tree"]
            or kwargs.get("shell")
        ):
            raise RuntimeError("Unexpected subprocess")
        process_events.append(argv)
        pending_process["argv"] = argv
        try:
            return original_popen(argv, *args, **kwargs)
        finally:
            pending_process["argv"] = None

    subprocess.Popen = controlled_popen

    def audit(event, args):
        if event == "open":
            filename, mode, flags = args
            if isinstance(filename, str | bytes):
                path = Path(filename).resolve()
                write = bool(flags & (0x1 | 0x2 | 0x40 | 0x200 | 0x400))
                if write and not path.is_relative_to(HERE):
                    raise RuntimeError("Write outside security evidence directory")
                if write:
                    io_events.append(str(path.relative_to(HERE)))
        elif event == "subprocess.Popen":
            executable, argv, cwd, env = args
            expected = pending_process["argv"]
            if expected is None or (argv != expected and argv != subprocess.list2cmdline(expected)):
                raise RuntimeError("Unexpected subprocess")
        elif event.startswith("socket."):
            raise RuntimeError("Network operation forbidden in audit rerun")

    sys.addaudithook(audit)

    def deny_network(*args, **kwargs):
        raise RuntimeError("Network operation forbidden in audit rerun")

    socket.socket = deny_network
    socket.create_connection = deny_network
    old_argv = sys.argv
    sys.argv = [str(script), "--raw-root", str(RESEARCH / "originals")]
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            namespace["main"]()
    finally:
        sys.argv = old_argv
    rerun_processes = process_events.copy()
    rerun = json.loads((HERE / "results.json").read_bytes())
    check("source control rerun pins HEAD", rerun["head_at_control"] == CANDIDATE)
    check(
        "source control rerun all checks pass",
        all(row["passed"] for row in rerun["checks"]),
        rerun["summary"],
    )
    check("rerun only writes redirected results", io_events == ["results.json"], io_events)
    binding = {
        "schema": "r2-security-candidate-1",
        "observed_utc": datetime.now(UTC).isoformat(),
        "base": BASE,
        "candidate": CANDIDATE,
        "candidate_tree": git("rev-parse", CANDIDATE + "^{tree}").decode().strip(),
        "files": file_bindings,
    }
    (HERE / "candidate.json").write_text(
        json.dumps(binding, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    result = {
        "schema": "r2-security-checks-1",
        "observed_utc": datetime.now(UTC).isoformat(),
        "base": BASE,
        "candidate": CANDIDATE,
        "audit_script_sha256": sha(Path(__file__).read_bytes()),
        "runtime": {
            "python": platform.python_version(),
            "lxml": lxml.__version__,
            "libxml": etree.LIBXML_VERSION,
            "pypdf": pypdf.__version__,
        },
        "source_bindings": bindings,
        "reused_file_count": len(reused),
        "metadata_summary": metadata_summary,
        "pdf_objects_inspected": checked_pdf_objects,
        "active_pdf_keys": active,
        "local_pdf_open_actions": local_open_actions,
        "code_summary": code_summary,
        "source_control_rerun_summary": rerun["summary"],
        "source_control_rerun_process_count": len(rerun_processes),
        "source_control_rerun_processes": rerun_processes,
        "source_control_rerun_writes": io_events[:1],
        "checks": CHECKS,
        "summary": {
            "check_count": len(CHECKS),
            "failures": sum(not row["passed"] for row in CHECKS),
            "new_archive_count": len(bindings),
            "new_body_bytes": sum(row["body_bytes"] for row in bindings),
            "max_new_body_bytes": max(row["body_bytes"] for row in bindings),
        },
    }
    (HERE / "checks.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
