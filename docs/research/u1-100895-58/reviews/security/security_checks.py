"""Bounded, offline security checks for the fixed U1 candidate.

Run from the checkout root with the documented Python/lxml environment.
Only this review directory receives fixtures and results. No source HTTP is made.
"""

import contextlib
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACK = HERE.parents[1]
ROOT = PACK.parents[2]
BASE = "59485e6bb6e45dacf348451b380cf6ba3b5d8321"
CANDIDATE = "e34b2fae67df6417807109e36eaeadc4c40c89fc"
HOSTS = {"data.stortinget.no", "www.stortinget.no", "www.regjeringen.no"}
RESULTS = []
OBSERVATIONS = {}
FIXTURES = None


def result(name, condition, detail=None):
    RESULTS.append({"name": name, "passed": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError(name)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def git_blobs(ref, paths):
    requests = b"".join((ref + ":" + p + "\n").encode("utf-8") for p in paths)
    completed = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=ROOT, input=requests, stdout=subprocess.PIPE, check=True
    )
    stream = io.BytesIO(completed.stdout)
    blobs = {}
    for path in paths:
        oid, kind, size = stream.readline().decode("ascii").strip().split(" ")
        assert kind == "blob"
        data = stream.read(int(size))
        assert len(data) == int(size) and stream.read(1) == b"\n"
        blobs[path] = (oid, data)
    assert not stream.read()
    return blobs


def load(name):
    return json.loads((PACK / name).read_text("utf-8"))


def module(name):
    spec = importlib.util.spec_from_file_location("audit_" + name, PACK / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def contained(base, name):
    path = base / name
    return (
        not Path(name).is_absolute()
        and ":" not in name
        and "\\" not in name
        and ".." not in Path(name).parts
        and path.resolve().is_relative_to(base.resolve())
    )


def manifests():
    result("fixed_candidate_head", git("rev-parse", "HEAD").decode().strip() == CANDIDATE)
    changed = git("diff", "--name-only", BASE + "..." + CANDIDATE).decode().splitlines()
    result(
        "candidate_has_52_authorized_files",
        len(changed) == 52
        and all(
            p in {"AGENTS.md", "docs/kildefunn.md"} or p.startswith("docs/research/u1-100895-58/")
            for p in changed
        ),
    )
    candidate_blobs = git_blobs(CANDIDATE, changed)
    for path in changed:
        original = candidate_blobs[path][1]
        local = (ROOT / path).read_bytes()
        if path in {"AGENTS.md", "docs/kildefunn.md"}:
            local = local.replace(b"\r\n", b"\n")
        result("candidate_blob_" + path, local == original)
    paths = []
    attempts = load("source-manifest.json")["sources"]
    maximum = {"archive_bytes": 0, "response_bytes": 0, "ratio": 0}
    for row in attempts:
        paths.append((PACK, row["metadata"]))
        metadata = json.loads((PACK / row["metadata"]).read_text("utf-8"))
        result(
            "metadata_manifest_identity_" + row["id"],
            all(row[k] == v for k, v in metadata.items() if k != "archive"),
        )
        urls = [metadata["requested_url"]]
        if metadata.get("final_url"):
            urls.append(metadata["final_url"])
        result(
            "recorded_https_source_hosts_" + row["id"],
            all(
                urlsplit(u).scheme == "https"
                and urlsplit(u).hostname in HOSTS
                and urlsplit(u).username is None
                and urlsplit(u).password is None
                for u in urls
            ),
        )
        result(
            "requests_have_no_auth_or_cookie_" + row["id"],
            {k.lower() for k in metadata["request_headers"]} == {"user-agent", "accept-encoding"},
        )
        if "archive" in row:
            paths.append((PACK, row["archive"]))
            archive = (PACK / row["archive"]).read_bytes()
            raw = gzip.decompress(archive)
            maximum["archive_bytes"] = max(maximum["archive_bytes"], len(archive))
            maximum["response_bytes"] = max(maximum["response_bytes"], len(raw))
            maximum["ratio"] = max(maximum["ratio"], len(raw) / len(archive))
            result(
                "complete_archived_entity_" + row["id"],
                len(raw) == row["bytes"]
                and sha(raw) == row["sha256"]
                and sha(archive) == row["archive_sha256"]
                and metadata["archive"] == Path(row["archive"]).name,
            )
    for name, key in [
        ("reused-sources.json", "files"),
        ("preserved-files.json", "files"),
        ("delivery-manifest.json", "files"),
        ("evidence.json", "evidence"),
    ]:
        paths.extend((ROOT, r["path"]) for r in load(name)[key])
    result(
        "all_886_manifest_paths_contained",
        len(paths) == 886 and all(contained(base, path) for base, path in paths),
        len(paths),
    )
    result(
        "all_candidate_paths_regular_not_symlinks",
        all(not (ROOT / p).is_symlink() and (ROOT / p).is_file() for p in changed),
    )
    preserved = load("preserved-files.json")["files"]
    preserved_paths = [r["path"] for r in preserved]
    base_blobs = git_blobs(BASE, preserved_paths)
    after_blobs = git_blobs(CANDIDATE, preserved_paths)
    for row in preserved:
        oid, before = base_blobs[row["path"]]
        after = after_blobs[row["path"]][1]
        result(
            "pinned_base_blob_" + row["path"],
            before == after
            and len(before) == row["git_blob_bytes"]
            and sha(before) == row["git_blob_sha256"]
            and oid == row["git_blob_oid"],
        )
    actual = {p.relative_to(PACK).as_posix() for p in (PACK / "originals").iterdir() if p.is_file()}
    expected = {r["metadata"] for r in attempts} | {
        r["archive"] for r in attempts if "archive" in r
    }
    result("originals_have_no_unmanifested_files", actual == expected and len(actual) == 29)
    OBSERVATIONS["new_archive_maxima"] = maximum
    OBSERVATIONS["preserved_base_blobs_checked"] = len(preserved)
    OBSERVATIONS["changed_files"] = len(changed)
    # Scan all committed additions, including decompressed public originals. Report names only.
    patterns = {
        "github_pat": re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{60,})"),
        "aws_access_key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
        "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "bearer_token": re.compile(
            rb"Authorization\s*[:=]\s*[\"']?Bearer\s+[A-Za-z0-9_.-]{20,}", re.I
        ),
    }
    hits = []
    for path in changed:
        raw = candidate_blobs[path][1]
        if path.endswith(".gz"):
            raw = gzip.decompress(raw)
        hits.extend(
            {"file": path, "pattern": name} for name, regex in patterns.items() if regex.search(raw)
        )
    result("no_high_confidence_credential_patterns", not hits, hits)


class Response:
    status = 200

    def __init__(
        self,
        body=b"<html><body>public source</body></html>",
        url="https://data.stortinget.no/eksport/sak?sakid=100895",
        partial=False,
    ):
        self.body = body
        self.url = url
        self.partial = partial
        self.headers = {"Content-Length": str(len(body))}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, *args):
        if self.partial:
            from http.client import IncompleteRead

            raise IncompleteRead(self.body[:5], len(self.body) - 5)
        return self.body


def acquisition():
    acquire = module("acquire")
    test_root = FIXTURES / "capture"
    test_root.mkdir(parents=True, exist_ok=True)
    acquire.__file__ = str(test_root / "acquire.py")
    dest = test_root / "originals"
    default_url = "https://data.stortinget.no/eksport/sak?sakid=100895"

    def run(identifier, url=default_url, response=None, error=None):
        out = io.StringIO()
        with (
            patch.object(sys, "argv", ["acquire.py", identifier, url]),
            patch.object(
                acquire.urllib.request,
                "urlopen",
                side_effect=error,
                return_value=response or Response(),
            ) as request,
            contextlib.redirect_stdout(out),
        ):
            try:
                acquire.main()
                return None, request.call_count
            except Exception as exc:
                return exc, request.call_count

    for i, identifier in enumerate(
        [
            "../outside",
            "..\\outside",
            "C:\\outside",
            "a/b",
            "a:b",
            "..",
            ".",
            "-",
            "a\n",
            "a ",
            "a\x00b",
        ]
    ):
        exc, calls = run(identifier)
        result("identifier_reject_" + str(i), isinstance(exc, ValueError) and calls == 0)
    for i, url in enumerate(
        [
            "file:///etc/passwd",
            "http://data.stortinget.no/",
            "https://evil.invalid/",
            "https://data.stortinget.no.evil.invalid/",
            "https://data.stortinget.no@evil.invalid/",
            "https://data.stortinget.no:443@evil.invalid/",
            "ftp://data.stortinget.no/",
        ]
    ):
        exc, calls = run("reject-url-" + str(i), url)
        result("url_reject_" + str(i), isinstance(exc, ValueError) and calls == 0)
    body = b"<html>\r\n\x00 exact bytes \xc3\xa6</html>"
    exc, calls = run("success.html", response=Response(body=body))
    metadata = json.loads((dest / "success.html.meta.json").read_text("utf-8"))
    result(
        "capture_preserves_complete_entity_bytes",
        exc is None
        and calls == 1
        and gzip.decompress((dest / "success.html.gz").read_bytes()) == body
        and metadata["sha256"] == sha(body)
        and metadata["state"] == "complete",
    )
    saved = {p.name: p.read_bytes() for p in dest.iterdir()}
    exc, calls = run("success.html")
    result(
        "duplicate_capture_rejected_before_network_no_clobber",
        isinstance(exc, FileExistsError)
        and calls == 0
        and saved == {p.name: p.read_bytes() for p in dest.iterdir()},
    )
    exc, calls = run("transport.xml", error=urllib.error.URLError("offline synthetic DNS failure"))
    m = json.loads((dest / "transport.xml.meta.json").read_text("utf-8"))
    result(
        "transport_failure_keeps_attempt_without_fabricated_body",
        exc is None
        and calls == 1
        and m["state"] == "transport_failed"
        and "archive" not in m
        and not (dest / "transport.xml.gz").exists(),
    )
    exc, _ = run("partial.xml", response=Response(partial=True))
    m = json.loads((dest / "partial.xml.meta.json").read_text("utf-8"))
    result(
        "partial_response_never_marked_complete",
        exc is None
        and m["state"] == "transport_failed"
        and "archive" not in m
        and not (dest / "partial.xml.gz").exists(),
    )
    error_body = b"<html>synthetic 404</html>"
    error = urllib.error.HTTPError(default_url, 404, "Not Found", {}, io.BytesIO(error_body))
    exc, _ = run("error.html", error=error)
    m = json.loads((dest / "error.html.meta.json").read_text("utf-8"))
    result(
        "http_error_body_archived_as_error_not_success",
        exc is None
        and m["state"] == "http_error"
        and m["status"] == 404
        and gzip.decompress((dest / "error.html.gz").read_bytes()) == error_body,
    )
    # No request is sent. Exercise urllib's actual redirect construction
    # and the helper's final-host handling.
    redirect = urllib.request.HTTPRedirectHandler().redirect_request(
        urllib.request.Request(default_url), None, 302, "Found", {}, "https://example.invalid/other"
    )
    exc, _ = run("redirect.html", response=Response(url=redirect.full_url))
    m = json.loads((dest / "redirect.html.meta.json").read_text("utf-8"))
    result(
        "redirect_limit_observed_without_network",
        exc is None
        and m["state"] == "complete"
        and urlsplit(m["final_url"]).hostname == "example.invalid",
    )
    OBSERVATIONS["redirect_host_guard"] = (
        "initial URL only; cross-host final URL accepted and recorded"
    )
    OBSERVATIONS["acquire_resource_limits"] = (
        "50-second urllib socket timeout; no byte limit or total deadline"
    )


def parsers_and_tamper():
    verify = module("verify")
    fixtures = FIXTURES / "parsing"
    fixtures.mkdir(parents=True, exist_ok=True)
    secret = fixtures / "local-entity.txt"
    secret.write_text("LOCAL-ENTITY-MUST-NOT-EXPAND", encoding="utf-8")
    xml = fixtures / "external.xml"
    xml.write_text(
        '<!DOCTYPE r [<!ENTITY ex SYSTEM "' + secret.as_uri() + '">]><r>&ex;</r>', encoding="utf-8"
    )
    raw, parsed = verify.source(xml.relative_to(ROOT).as_posix(), True)
    result(
        "xml_external_file_entity_not_expanded",
        b"<!DOCTYPE" in raw and "LOCAL-ENTITY-MUST-NOT-EXPAND" not in verify.normalized(parsed),
    )
    internal = fixtures / "internal.xml"
    internal.write_bytes(b'<!DOCTYPE r [<!ENTITY ex "SHOULD-NOT-EXPAND">]><r>&ex;</r>')
    result(
        "xml_internal_entity_not_expanded",
        "SHOULD-NOT-EXPAND"
        not in verify.normalized(verify.source(internal.relative_to(ROOT).as_posix(), True)[1]),
    )
    html_path = fixtures / "untrusted.html"
    html_path.write_bytes(
        b'<html><body><script>throw new Error("not executed")</script>'
        b'<img src="file:///not-read"><p onclick="alert(1)">text</p></body></html>'
    )
    node = verify.source(html_path.relative_to(ROOT).as_posix(), False)[1]
    result("html_only_parsed_to_data", node.xpath("//p")[0].text == "text")
    try:
        node.xpath("document('file:///not-read')")
        rejected = False
    except Exception:
        rejected = True
    result("xpath_has_no_document_function", rejected)
    baseline_read = verify.read_json
    mutations = [
        (
            "source-manifest.json",
            lambda d: d["sources"][0].update(metadata_sha256="0" * 64),
            "transport_metadata_hash",
        ),
        (
            "source-manifest.json",
            lambda d: d["sources"][0].update(sha256="0" * 64),
            "response_hash",
        ),
        (
            "evidence.json",
            lambda d: d["evidence"][0].update(text="synthetic mismatch"),
            "evidence_exact_text",
        ),
    ]
    for name, mutate, expected in mutations:
        data = copy.deepcopy(baseline_read(name))
        mutate(data)
        verify.CACHE.clear()
        verify.COUNTS.clear()

        def altered(requested, data=data, name=name):
            return data if requested == name else baseline_read(requested)

        caught = None
        with (
            patch.object(verify, "read_json", side_effect=altered),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            try:
                verify.main()
            except AssertionError as exc:
                caught = str(exc)
        result(
            "tampering_rejected_" + expected,
            caught is not None and caught.startswith(expected + ":"),
        )
    OBSERVATIONS["manifest_trust"] = (
        "repository-reviewed manifests are trusted inputs, not an untrusted-input sandbox"
    )


if __name__ == "__main__":
    manifests()
    with tempfile.TemporaryDirectory(prefix="security-fixtures-", dir=HERE) as fixture_dir:
        FIXTURES = Path(fixture_dir).resolve()
        assert FIXTURES.is_relative_to(HERE.resolve())
        acquisition()
        parsers_and_tamper()
    report = {
        "schema": "u1-security-checks-1",
        "checked_utc": datetime.now(UTC).isoformat(),
        "base_commit": BASE,
        "candidate_commit": CANDIDATE,
        "runtime": sys.version,
        "total_checks": len(RESULTS),
        "failures": sum(not r["passed"] for r in RESULTS),
        "observations": OBSERVATIONS,
        "checks": RESULTS,
        "boundary": (
            "Offline synthetic negatives plus candidate/base Git-blob checks; "
            "no source HTTP or product suite."
        ),
    }
    (HERE / "security-results.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        json.dumps({k: v for k, v in report.items() if k != "checks"}, ensure_ascii=False, indent=2)
    )
