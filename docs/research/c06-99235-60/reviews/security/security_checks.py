"""Independent, offline security probes of one fixed C06 Git candidate.

Only this review directory receives files. No source downloads or mutations.
"""

import contextlib
import copy
import datetime as dt
import email.message
import gzip
import hashlib
import io
import json
import re
import socket
import subprocess
import sys
import tempfile
import types
import urllib.error
import urllib.request
import urllib.response
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath
from unittest.mock import patch

from lxml import etree
from PIL import Image

HERE = Path(__file__).resolve().parent
PACK = HERE.parents[1]
ROOT = PACK.parents[2]
BASE = "49cc6e44851cf74e0aaea4eb333419e5598bfd95"
CANDIDATE = "9eb27cebf7ca4a99aeb30fa32245e41314e0d295"
PREFIX = PACK.relative_to(ROOT).as_posix() + "/"
COUNTS = Counter()
OBSERVATIONS = {}


def check(condition, label):
    if not condition:
        raise AssertionError(label)
    COUNTS[label] += 1


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def blob(path, revision=CANDIDATE):
    return git("show", f"{revision}:{path}")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def candidate_json(name):
    return json.loads(blob(PREFIX + name))


def load(name):
    filename = PACK / f"{name}.py"
    module = types.ModuleType(name)
    module.__file__ = str(filename)
    sys.modules[name] = module
    exec(compile(blob(PREFIX + filename.name), str(filename), "exec"), module.__dict__)
    return module


def fixed_candidate():
    check(git("rev-parse", "HEAD").decode().strip() == CANDIDATE, "fixed_head")
    changed = git("diff", "--name-only", BASE, CANDIDATE).decode().splitlines()
    check(len(changed) == 74, "candidate_74_changed_files")
    check(
        all(p in ("AGENTS.md", "docs/kildefunn.md") or p.startswith(PREFIX) for p in changed),
        "authorized_diff_paths",
    )
    listing = git("ls-tree", "-r", "-z", CANDIDATE)
    modes = {}
    candidate_metadata = {}
    for entry in listing.split(b"\0"):
        if entry:
            metadata, name = entry.split(b"\t", 1)
            modes[name.decode()] = metadata.decode().split()[0]
            candidate_metadata[name.decode()] = metadata
    for path in changed:
        check(modes[path] == "100644", "changed_files_are_regular")
        actual = (ROOT / path).read_bytes()
        if path in ("AGENTS.md", "docs/kildefunn.md"):
            actual = actual.replace(b"\r\n", b"\n")
        check(actual == blob(path), "changed_checkout_matches_fixed_blob")
    base_entries = git("ls-tree", "-r", "-z", BASE).split(b"\0")
    protected = 0
    for entry in base_entries:
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        path = name.decode()
        if path in ("AGENTS.md", "docs/kildefunn.md"):
            continue
        check(candidate_metadata[path] == metadata, "protected_base_blob_unchanged")
        protected += 1
    OBSERVATIONS["candidate"] = {"changed_files": len(changed), "protected_base_files": protected}
    return changed


class Reply:
    def __init__(self, status=200, headers=None, body=b"ok"):
        self.status = status
        self.headers = headers or {}
        self.body = body
        self.closed = False

    def read(self, size):
        result, self.body = self.body[:size], self.body[size:]
        return result

    def close(self):
        self.closed = True


def run_capture(acquire, replies, initial="https://www.stortinget.no/a", identifier="probe"):
    calls = []

    def fake(req):
        calls.append(req.full_url)
        result = replies[len(calls) - 1]
        if isinstance(result, BaseException):
            raise result
        return result

    with tempfile.TemporaryDirectory(dir=HERE) as directory:
        dest = Path(directory)
        meta = acquire.capture(identifier, initial, dest, fake)
        for hop in meta["hops"]:
            if "archive" in hop:
                check(
                    gzip.decompress((dest / hop["archive"]).read_bytes()) is not None,
                    "probe_archive_is_readable",
                )
        check(
            json.loads((dest / (identifier + ".meta.json")).read_text("utf-8"))
            == json.loads(json.dumps(meta)),
            "probe_return_matches_saved_metadata",
        )
        return meta, calls


def transport_probes(acquire):
    invalid = [
        "http://www.stortinget.no/x",
        "ftp://www.stortinget.no/x",
        "file:///C:/secret",
        "https://127.0.0.1/x",
        "https://[::1]/x",
        "https://evil.example/x",
        "https://www.stortinget.no.evil.example/x",
        "https://www.stortinget.no./x",
        "https://www.stortinget.no:80/x",
        "https://www.stortinget.no:8443/x",
        "https://www.stortinget.no:65536/x",
        "https://www.stortinget.no:notaport/x",
        "https://user@www.stortinget.no/x",
        "https://user:pass@www.stortinget.no/x",
        "https://@www.stortinget.no/x",
        "https://www.stortinget.no@evil.example/x",
        "https://www.stortinget.no\\@evil.example/x",
        "https://www.stortinget.no/#fragment",
        "https://www.stortinget.no/a\nInjected: value",
        "https://www.stortinget.no/a\x00b",
        " https://www.stortinget.no/x",
        "https://www%2estortinget.no/x",
    ]
    for url in invalid:
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            calls = []
            try:
                acquire.capture(
                    "initial", url, Path(directory), lambda req, calls=calls: calls.append(req)
                )
            except ValueError:
                pass
            else:
                raise AssertionError(f"invalid initial URL accepted: {url!r}")
            check(
                not calls and not list(Path(directory).iterdir()), "bad_initial_rejected_before_IO"
            )
    for status in (301, 302, 303, 307, 308):
        for target in invalid:
            # urljoin can remove leading C0 whitespace; acceptance is safe when the actual
            # resolved outgoing URL meets the exact boundary. Those cases are tested below.
            if target.startswith(" ") or "\n" in target:
                continue
            meta, calls = run_capture(acquire, [Reply(status, {"Location": target}, b"redirect")])
            check(
                len(calls) == 1 and meta["state"] == "redirect_rejected",
                "bad_redirect_rejected_before_next_request",
            )
    for identifier in ("..", "../x", "a/b", "a\\b", "C:x", "/absolute", "*", "a\n", "a\x00"):
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            calls = []
            try:
                acquire.capture(
                    identifier,
                    "https://www.stortinget.no/a",
                    Path(directory),
                    lambda req, calls=calls: calls.append(req),
                )
            except ValueError:
                pass
            else:
                raise AssertionError("identifier validation failed")
            check(not calls and not list(Path(directory).iterdir()), "bad_identifier_before_IO")
    for host in acquire.HOSTS:
        for port in ("", ":443"):
            acquire.validate_url("https://" + host + port + "/x")
            check(True, "allowed_exact_host_default_or_443")
    meta, calls = run_capture(
        acquire, [Reply(302, {"Location": " https://www.stortinget.no/b"}), Reply(200)]
    )
    check(
        meta["state"] == "complete" and calls[-1] == "https://www.stortinget.no/b",
        "normalized_location_still_respects_exact_outgoing_host",
    )
    meta, calls = run_capture(
        acquire,
        [
            Reply(302, {"Location": "/b"}),
            Reply(307, {"Location": "//www.regjeringen.no/c"}),
            Reply(308, {"Location": "https://evil.example/d"}),
        ],
    )
    check(
        meta["state"] == "redirect_rejected"
        and calls
        == [
            "https://www.stortinget.no/a",
            "https://www.stortinget.no/b",
            "https://www.regjeringen.no/c",
        ],
        "valid_intermediates_then_host_escape_blocked",
    )
    meta, calls = run_capture(acquire, [Reply(302, {"Location": "/loop"}) for _ in range(9)])
    check(len(calls) == 9 and meta["state"] == "redirect_limit", "redirect_limit_no_tenth_request")
    meta, calls = run_capture(acquire, [Reply(302)])
    check(meta["state"] == "transport_failed" and len(calls) == 1, "missing_location_not_complete")
    meta, _ = run_capture(acquire, [Reply(200, {"Content-Length": "99"}, b"short")])
    check(
        meta["state"] == "transport_failed"
        and not meta["hops"][0]["body_complete"]
        and meta["hops"][0]["bytes"] == 5,
        "content_length_partial_preserved_not_complete",
    )
    meta, _ = run_capture(acquire, [TimeoutError("synthetic pre-response failure")])
    check(
        meta["state"] == "transport_failed" and "archive" not in meta["hops"][0],
        "pre_response_failure_has_no_fabricated_archive",
    )
    for status in (404, 500):
        meta, _ = run_capture(acquire, [Reply(status, {}, b"error bytes")])
        check(
            meta["state"] == "http_error" and meta["hops"][0]["body_complete"],
            "http_error_body_preserved_separate_state",
        )

    class Partial(Reply):
        def read(self, size):
            import http.client

            raise http.client.IncompleteRead(b"partial\r\n\x00", 99)

    meta, _ = run_capture(acquire, [Partial()])
    check(
        meta["state"] == "transport_failed" and meta["hops"][0]["bytes"] == 10,
        "incomplete_read_partial_bytes_preserved",
    )

    class Oversize(Reply):
        def read(self, size):
            return b"X" * size

    meta, _ = run_capture(acquire, [Oversize()])
    check(
        meta["state"] == "transport_failed"
        and not meta["hops"][0]["body_complete"]
        and meta["hops"][0]["bytes"] == 80 * 1024 * 1024 + 65536,
        "capture_byte_limit_preserves_bounded_incomplete_response",
    )
    with tempfile.TemporaryDirectory(dir=HERE) as directory:
        dest = Path(directory)
        acquire.capture(
            "once",
            "https://www.stortinget.no/a",
            dest,
            lambda req: Reply(200, {}, b"bytes\r\n\x00\xc3\xb8"),
        )
        before = {p.name: p.read_bytes() for p in dest.iterdir()}
        with patch.object(acquire, "request_once", side_effect=AssertionError("network forbidden")):
            try:
                acquire.capture(
                    "once",
                    "https://www.stortinget.no/a",
                    dest,
                    lambda req: (_ for _ in ()).throw(AssertionError("called")),
                )
            except FileExistsError:
                pass
            else:
                raise AssertionError("overwrite accepted")
        check(before == {p.name: p.read_bytes() for p in dest.iterdir()}, "attempt_no_overwrite")
        check(
            gzip.decompress((dest / "once.hop0.gz").read_bytes()) == b"bytes\r\n\x00\xc3\xb8",
            "success_preserves_exact_binary_bytes",
        )

    # Exercise urllib's real HTTPErrorProcessor/HTTPRedirectHandler stack, not
    # only the injected capture callback. Fake HTTPS transport never opens a socket.
    real_build_opener = urllib.request.build_opener
    for status in (301, 302, 303, 307, 308):
        calls = []

        class FakeHTTPS(urllib.request.HTTPSHandler):
            def https_open(self, req, calls=calls, status=status):
                calls.append(req.full_url)
                headers = email.message.Message()
                headers["Location"] = "/second" if len(calls) == 1 else "https://evil.example/third"
                response = urllib.response.addinfourl(
                    io.BytesIO(b"redirect body"), headers, req.full_url, status
                )
                response.msg = "Found"
                return response

        with patch.object(
            urllib.request,
            "build_opener",
            lambda *handlers: real_build_opener(*handlers, FakeHTTPS()),
        ):
            with tempfile.TemporaryDirectory(dir=HERE) as directory:
                meta = acquire.capture("realstack", "https://www.stortinget.no/a", Path(directory))
                check(
                    meta["state"] == "redirect_rejected"
                    and calls
                    == ["https://www.stortinget.no/a", "https://www.stortinget.no/second"],
                    "real_urllib_stack_blocks_redirect_escape",
                )
    OBSERVATIONS["transport_probes"] = {
        "invalid_initial_urls": len(invalid),
        "redirect_statuses": [301, 302, 303, 307, 308],
        "real_sockets_opened": 0,
    }


def bounded_paths_and_contents(changed, acquire):
    manifest = candidate_json("source-manifest.json")["sources"]
    actual_redirects, body_sizes, ratios = [], [], []
    expected_originals = set()
    for row in manifest:
        acquire.validate_url(row["requested_url"])
        sidecar = candidate_json(row["metadata"])
        expected_originals.add(row["metadata"])
        check(sidecar["id"] == row["id"] and sidecar["state"] == row["state"], "sidecar_identity")
        check(
            set(row["request_headers"]) == {"User-Agent", "Accept-Encoding"},
            "no_request_credentials",
        )
        for index, hop in enumerate(row["hops"]):
            acquire.validate_url(hop["url"])
            check(hop["url"] == sidecar["hops"][index]["url"], "observed_hop_bound_to_sidecar")
            if "archive" not in hop:
                check(row["state"] == "transport_failed", "observed_no_response_failure")
                continue
            expected_originals.add(hop["archive"])
            compressed = blob(PREFIX + hop["archive"])
            raw = gzip.decompress(compressed)
            check(len(raw) == hop["bytes"] and sha(raw) == hop["sha256"], "observed_entity_hash")
            check(
                len(compressed) == hop["archive_bytes"]
                and sha(compressed) == hop["archive_sha256"],
                "observed_archive_hash",
            )
            check(hop["body_complete"] and hop["state"] == "complete", "observed_complete_hop")
            body_sizes.append(len(raw))
            ratios.append(len(raw) / len(compressed))
            if "redirect_target" in hop:
                acquire.validate_url(hop["redirect_target"])
                headers = dict((k.lower(), v) for k, v in hop["response_headers"])
                resolved = urllib.parse.urljoin(hop["url"], headers["location"])
                check(
                    resolved == hop["redirect_target"] == row["hops"][index + 1]["url"],
                    "observed_raw_location_resolves_to_next_valid_hop",
                )
                actual_redirects.append(
                    {
                        "id": row["id"],
                        "status": hop["status"],
                        "from": hop["url"],
                        "to": hop["redirect_target"],
                    }
                )
    candidate_originals = {p[len(PREFIX) :] for p in changed if p.startswith(PREFIX + "originals/")}
    check(candidate_originals == expected_originals, "no_unlisted_originals")
    path_fields = {
        "path",
        "metadata",
        "archive",
        "source",
        "left_source",
        "right_source",
        "ocr_archive",
    }
    total_path_fields = 0

    def walk(value):
        nonlocal total_path_fields
        if isinstance(value, dict):
            for key, item in value.items():
                if key in path_fields and isinstance(item, str) and "://" not in item:
                    check(
                        not PureWindowsPath(item).drive
                        and not PureWindowsPath(item).is_absolute()
                        and not PurePosixPath(item).is_absolute()
                        and "\\" not in item
                        and ".." not in PurePosixPath(item).parts,
                        "manifest_relative_path_no_traversal",
                    )
                    total_path_fields += 1
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    secret_patterns = {
        "github_token": rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})",
        "aws_access_key": rb"(?:AKIA|ASIA)[A-Z0-9]{16}",
        "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "auth_bearer": rb"(?:Authorization\s*[:=]\s*|Bearer\s+)[A-Za-z0-9._~+/=-]{20,}",
    }
    for path in changed:
        data = blob(path)
        if path.endswith(".gz"):
            data = gzip.decompress(data)
        if path.endswith(".json") or path.endswith(".json.gz"):
            walk(json.loads(data))
        for label, pattern in secret_patterns.items():
            check(re.search(pattern, data) is None, "secret_pattern_no_match_" + label)
        if path.endswith((".md", ".py", ".ps1")):
            for target in re.findall(rb"\]\(([^)]+)\)", data):
                check(
                    not target.lower().startswith(
                        (b"javascript:", b"data:", b"file:", b"vbscript:")
                    ),
                    "authored_link_no_active_or_local_scheme",
                )
    OBSERVATIONS["originals"] = {
        "attempts": len(manifest),
        "complete_attempts": sum(r["state"] == "complete" for r in manifest),
        "response_hops": len(body_sizes),
        "maximum_body_bytes": max(body_sizes),
        "maximum_gzip_expansion_ratio": max(ratios),
        "observed_redirects": actual_redirects,
        "path_fields_checked": total_path_fields,
    }


def parser_and_pdf_probes(build, verify, extract):
    with tempfile.TemporaryDirectory(dir=HERE) as directory:
        temp = Path(directory)
        marker = temp / "sentinel.txt"
        marker.write_text("SECURITY_SENTINEL_NEVER_EXPAND", encoding="utf-8")
        documents = [
            b'<!DOCTYPE root [<!ENTITY x "SECURITY_SENTINEL_NEVER_EXPAND">]><root>&x;</root>',
            (
                '<!DOCTYPE root [<!ENTITY x SYSTEM "' + marker.as_uri() + '">]><root>&x;</root>'
            ).encode(),
            b'<!DOCTYPE root [<!ENTITY x SYSTEM "https://evil.example/x">]><root>&x;</root>',
        ]
        for index, data in enumerate(documents):
            path = temp / f"entity-{index}.xml"
            path.write_bytes(data)
            for module in (build, verify):
                module.CACHE.clear()
                if module is build:
                    module.SOURCES["security_probe"] = str(path)
                    raw, node = module.source("security_probe", True)
                else:
                    raw, node = module.source(str(path), True)
                check(
                    b"SECURITY_SENTINEL_NEVER_EXPAND" not in etree.tostring(node),
                    "candidate_xml_parser_never_expands_entities",
                )
                check(raw == data, "xml_parser_preserves_raw_bytes")
    build.CACHE.clear()
    build.SOURCES.pop("security_probe", None)
    verify.CACHE.clear()
    result = extract.inventory()
    check(
        result == candidate_json("appendix-image-inventory.json"),
        "regenerated_pdf_inventory_equals_candidate",
    )
    check(result["pdf_pages"] == 144 and len(result["images"]) == 130, "known_pdf_extent")
    raw = gzip.decompress(blob(PREFIX + "originals/prop108-full-pdf-a1.hop0.gz"))
    reader = extract.PdfReader(io.BytesIO(raw))
    dims, image_bytes = [], []
    for page in reader.pages:
        for embedded in page.images:
            data = embedded.data
            with Image.open(io.BytesIO(data)) as image:
                dims.append(image.size)
                image.verify()
            image_bytes.append(len(data))
            check(True, "known_embedded_jpeg_decodes")
    root = reader.trailer["/Root"]
    action = root.get("/OpenAction")
    action = action.get_object() if action is not None else {}
    check(action.get("/S") == "/GoTo", "known_pdf_open_action_is_page_navigation")
    OBSERVATIONS["pdf"] = {
        "pdf_pages": len(reader.pages),
        "embedded_images": len(dims),
        "maximum_image_bytes": max(image_bytes),
        "maximum_image_pixels": max(w * h for w, h in dims),
        "width_range": [min(w for w, h in dims), max(w for w, h in dims)],
        "height_range": [min(h for w, h in dims), max(h for w, h in dims)],
        "catalog_open_action_present": "/OpenAction" in root,
        "catalog_open_action_type": str(action.get("/S")),
        "catalog_additional_actions_present": "/AA" in root,
        "boundary": (
            "Image extraction/decoding only; no JavaScript/action/form/link execution or OCR rerun."
        ),
    }
    # Remote image names must not become extraction filenames.
    with tempfile.TemporaryDirectory(dir=HERE) as directory:
        temp = Path(directory)
        (temp / "originals").mkdir()
        (temp / "originals/prop108-full-pdf-a1.hop0.gz").write_bytes(gzip.compress(b"synthetic"))
        fake_image = types.SimpleNamespace(name="../../outside.jpg", data=b"synthetic JPEG bytes")
        fake_reader = types.SimpleNamespace(pages=[types.SimpleNamespace(images=[fake_image])])
        with (
            patch.object(extract, "PACK", temp),
            patch.object(extract, "PdfReader", lambda stream: fake_reader),
        ):
            synthetic = extract.inventory(temp / "images")
        check(
            [p.name for p in (temp / "images").iterdir()] == ["page-001-0.jpg"],
            "untrusted_pdf_image_name_cannot_escape_output_directory",
        )
        check(
            synthetic["images"][0]["image_name"] == "../../outside.jpg",
            "raw_pdf_name_remains_metadata_only",
        )
    return result


def refresh_manifest_probe(refresh):
    intercepted = {}

    def capture_write(path, text, *args, **kwargs):
        check(path == PACK / "delivery-manifest.json", "refresh_writes_only_own_manifest")
        intercepted[path.name] = text.encode("utf-8")
        return len(text)

    with patch.object(Path, "write_text", capture_write), contextlib.redirect_stdout(io.StringIO()):
        refresh.main()
    check(
        intercepted["delivery-manifest.json"] == blob(PREFIX + "delivery-manifest.json"),
        "refresh_manifest_reproduces_candidate_bytes",
    )


def builder_verification_and_tamper_probes(build, verify, image_inventory):
    verify.COUNTS.clear()
    verify.CACHE.clear()
    with (
        patch.object(sys, "argv", [str(PACK / "verify.py"), CANDIDATE]),
        contextlib.redirect_stdout(io.StringIO()) as stream,
    ):
        verify.main()
    result = json.loads(stream.getvalue())
    (HERE / "builder-verify-current.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    check(result["failures"] == 0, "unmodified_builder_verify_passes_fixed_candidate")
    actual_read_json = verify.read_json
    for target, mutate, expected in (
        (
            "source-manifest.json",
            lambda value: value["sources"][0].update(metadata_sha256="0" * 64),
            "metadata_hash",
        ),
        (
            "source-manifest.json",
            lambda value: value["sources"][1]["hops"][0].update(sha256="0" * 64),
            "entity_binding",
        ),
        (
            "evidence.json",
            lambda value: value["evidence"][0].update(text="tampered text"),
            "exact_derived_text",
        ),
    ):

        def mutated_read(name, target=target, mutate=mutate):
            value = copy.deepcopy(actual_read_json(name))
            if name == target:
                mutate(value)
            return value

        verify.COUNTS.clear()
        verify.CACHE.clear()
        with (
            patch.object(verify, "read_json", mutated_read),
            patch.object(verify, "inventory", lambda: image_inventory),
        ):
            try:
                verify.main()
            except AssertionError as exc:
                check(str(exc).startswith(expected + ":"), "tamper_rejected_" + expected)
            else:
                raise AssertionError("tamper not detected")
    # Rebuild in memory: all candidate source/parser logic runs, but writes are
    # intercepted. It must reproduce each generated artifact byte-for-byte.
    outputs = {}
    build.EVIDENCE.clear()
    build.SOURCES.clear()
    build.CACHE.clear()
    with (
        patch.object(build, "write", lambda name, value: outputs.update({name: value})),
        contextlib.redirect_stdout(io.StringIO()),
    ):
        build.main()
    for name, value in outputs.items():
        data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
        check(data == blob(PREFIX + name), "in_memory_rebuild_equals_candidate_artifact")
    OBSERVATIONS["rebuild"] = {
        "artifacts": sorted(outputs),
        "builder_verify_checks": result["total_checks"],
    }


def main():
    changed = fixed_candidate()
    acquire = load("acquire")
    extract = load("extract_appendices")
    build = load("build_evidence")
    verify = load("verify")
    refresh = load("refresh_manifest")
    # Any accidental real network is an audit failure, including XML lookups.
    with (
        patch.object(
            socket, "create_connection", side_effect=AssertionError("offline audit forbids sockets")
        ),
        patch.object(
            socket.socket, "connect", side_effect=AssertionError("offline audit forbids sockets")
        ),
    ):
        transport_probes(acquire)
        bounded_paths_and_contents(changed, acquire)
        image_inventory = parser_and_pdf_probes(build, verify, extract)
        builder_verification_and_tamper_probes(build, verify, image_inventory)
        refresh_manifest_probe(refresh)
    # Reconfirm candidate files after all executable probes; do not include peers' reviews.
    for path in changed:
        data = (ROOT / path).read_bytes()
        if path in ("AGENTS.md", "docs/kildefunn.md"):
            data = data.replace(b"\r\n", b"\n")
        check(data == blob(path), "candidate_unchanged_after_probes")
    result = {
        "schema": "c06-independent-security-audit-1",
        "checked_utc": dt.datetime.now(dt.UTC).isoformat(),
        "base_commit": BASE,
        "candidate_commit": CANDIDATE,
        "runtime": sys.version,
        "checks": dict(COUNTS),
        "total_checks": sum(COUNTS.values()),
        "failures": 0,
        "observations": OBSERVATIONS,
        "boundary": (
            "Offline fixed-candidate security audit only; no HTTP/TLS replay, OCR rerun, "
            "full product suite, CI, PR or merge."
        ),
    }
    (HERE / "security-results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"checks": result["total_checks"], "failures": 0, "candidate": CANDIDATE}))


if __name__ == "__main__":
    main()
