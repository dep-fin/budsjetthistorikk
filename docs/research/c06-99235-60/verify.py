"Offline C06 source, locator, chronology and preservation checks; no network."

import gzip
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from acquire import validate_url
from extract_appendices import inventory
from lxml import etree, html

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[2]
BASE = "49cc6e44851cf74e0aaea4eb333419e5598bfd95"
NS = {"s": "http://data.stortinget.no"}
COUNTS = Counter()
CACHE = {}


def check(condition, name, detail=""):
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    COUNTS[name] += 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(name):
    return json.loads((PACK / name).read_text("utf-8-sig"))


def normalize(node):
    return " ".join(" ".join(node.itertext()).split())


def source(path, xml=False):
    if (path, xml) not in CACHE:
        data = (ROOT / path).read_bytes()
        raw = gzip.decompress(data) if path.endswith(".gz") else data
        node = (
            etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
            if xml
            else html.fromstring(raw.decode("utf-8-sig"))
        )
        CACHE[path, xml] = (raw, node)
    return CACHE[path, xml]


def main():
    context = read_json("context-snapshot.json")
    check({r["number"] for r in context["items"]} == {37, 50, 52, 54, 56, 58, 60}, "context_issues")
    issue = next(r["issue"] for r in context["items"] if r["number"] == 60)
    contract_time = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
    check(issue["created_at"] == "2026-10-29T16:21:08Z", "published_contract_time")
    attempts = read_json("source-manifest.json")["sources"]
    check(len(attempts) == 16, "attempt_count")
    check(sum(r["state"] == "complete" for r in attempts) == 15, "complete_attempt_count")
    original_names = set()
    for row in attempts:
        metadata = (PACK / row["metadata"]).read_bytes()
        original_names.add(row["metadata"])
        check(len(metadata) == row["metadata_bytes"], "metadata_bytes", row["id"])
        check(digest(metadata) == row["metadata_sha256"], "metadata_hash", row["id"])
        actual = json.loads(metadata)
        check(
            datetime.fromisoformat(row["started_utc"]) > contract_time,
            "contract_before_every_attempt",
        )
        check(row["completed_utc"] >= row["started_utc"], "attempt_time_order")
        validate_url(row["requested_url"])
        COUNTS["allowed_start_url"] += 1
        check(
            row["request_headers"]
            == {"User-Agent": "budsjetthistorikk-research/60", "Accept-Encoding": "identity"},
            "request_headers",
        )
        for index, hop in enumerate(row["hops"]):
            validate_url(hop["url"])
            check(hop["url"] == actual["hops"][index]["url"], "hop_url_binding")
            if "archive" not in hop:
                check(
                    row["id"] == "case-99235-a1" and row["state"] == "transport_failed",
                    "documented_no_response_dns_failure",
                )
                continue
            original_names.add(hop["archive"])
            data = (PACK / hop["archive"]).read_bytes()
            raw = gzip.decompress(data)
            check(
                len(data) == hop["archive_bytes"] and digest(data) == hop["archive_sha256"],
                "archive_binding",
            )
            check(len(raw) == hop["bytes"] and digest(raw) == hop["sha256"], "entity_binding")
            check(hop["body_complete"] and hop["state"] == "complete", "complete_observed_hop")
            headers = {k.lower(): v for k, v in hop["response_headers"]}
            check(headers.get("content-encoding", "identity") == "identity", "identity_entity")
            if "content-length" in headers:
                check(len(raw) == int(headers["content-length"]), "content_length")
            if "redirect_target" in hop:
                validate_url(hop["redirect_target"])
                check(
                    index + 1 < len(row["hops"])
                    and hop["redirect_target"] == row["hops"][index + 1]["url"],
                    "redirect_to_next_validated_hop",
                )
            if index == len(row["hops"]) - 1:
                check(row["final_url"] == hop["url"] and hop["status"] == 200, "final_url_status")
                kind = headers.get("content-type", "")
                if "html" in kind:
                    check(raw.rstrip().lower().endswith(b"</html>"), "complete_html_end")
                if "xml" in kind:
                    etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
                    COUNTS["complete_xml"] += 1
                if "pdf" in kind:
                    check(
                        raw.startswith(b"%PDF") and b"%%EOF" in raw[-1024:], "complete_pdf_envelope"
                    )
    check(
        original_names == {p.relative_to(PACK).as_posix() for p in (PACK / "originals").iterdir()},
        "all_original_attempt_files_in_manifest",
    )

    for row in read_json("reused-sources.json")["files"]:
        data = (ROOT / row["path"]).read_bytes()
        check(
            len(data) == row["bytes"] and digest(data) == row["sha256"], "reused_file", row["path"]
        )
        if "body_sha256" in row:
            raw = gzip.decompress(data)
            check(
                len(raw) == row["body_bytes"] and digest(raw) == row["body_sha256"], "reused_entity"
            )

    image_inventory = read_json("appendix-image-inventory.json")
    regenerated = inventory()
    check(regenerated == image_inventory, "complete_pdf_image_inventory")
    check(
        image_inventory["pdf_pages"] == 144 and len(image_inventory["images"]) == 130,
        "pdf_and_appendix_extent",
    )
    check(
        Counter(r["appendix"] for r in image_inventory["images"]) == {1: 65, 2: 65},
        "both_own_appendices",
    )
    ocr_bytes = gzip.decompress((PACK / "appendix-ocr.json.gz").read_bytes())
    ocr = json.loads(ocr_bytes)
    check(len(ocr["pages"]) == 130 and ocr["language"] == "en-US", "ocr_extent_and_limit")
    check(
        {r["image"] for r in ocr["pages"]}
        == {r["derived_filename"] for r in image_inventory["images"]},
        "ocr_all_embedded_pages",
    )
    journal = read_json("appendix-reading-journal.json")
    check(len(journal["pages"]) == 130, "all_appendix_pages_journaled")
    for row, image in zip(journal["pages"], image_inventory["images"], strict=True):
        check(
            row["pdf_page_1based"] == image["pdf_page_1based"]
            and row["image_sha256"] == image["image_sha256"],
            "page_journal_binding",
        )
        page = next(r for r in ocr["pages"] if r["image"] == image["derived_filename"])
        check(row["ocr_text_sha256"] == digest(page["text"].encode()), "page_ocr_binding")
    check(
        sum(row["visual_review"] for row in journal["pages"]) == 18, "explicit_visual_review_extent"
    )

    evidence = read_json("evidence.json")["evidence"]
    by_id = {row["id"]: row for row in evidence}
    check(len(by_id) == len(evidence) == 87, "unique_evidence")
    for row in evidence:
        if "pdf_page_1based" in row:
            image = next(
                r
                for r in image_inventory["images"]
                if r["pdf_page_1based"] == row["pdf_page_1based"]
            )
            check(row["source_sha256"] == image_inventory["pdf_sha256"], "visual_pdf_hash")
            check(
                row["image_sha256"] == image["image_sha256"]
                and row["figure_ordinal"] == image["figure_ordinal"],
                "visual_locator_binding",
            )
            continue  # Manual observations/paraphrases need independent visual source review.
        raw, tree = source(row["path"], bool(row["namespaces"]))
        check(digest(raw) == row["source_sha256"], "evidence_source_hash", row["id"])
        found = tree.xpath(row["xpath"], namespaces=row["namespaces"])
        check(len(found) == 1, "unique_exact_xpath", row["id"])
        node = found[0]
        if row["inner_html_field"]:
            node = html.fromstring(node.find(row["inner_html_field"], NS).text)
        check(normalize(node) == row["text"], "exact_derived_text", row["id"])

    for row in read_json("source-comparison.json")["decisions"]:
        left_raw, left = source(row["left_source"], True)
        right_raw, right = source(row["right_source"], True)
        check(
            digest(left_raw) == row["left_body_sha256"]
            and digest(right_raw) == row["right_body_sha256"],
            "two_session_entity_hashes",
        )
        a = etree.tostring(left.xpath(row["left_xpath"])[0], method="c14n", with_comments=False)
        b = etree.tostring(right.xpath(row["right_xpath"])[0], method="c14n", with_comments=False)
        check(a == b and row["equal"], "complete_canonical_decisions_equal")
        check(digest(a) == row["c14n_sha256_left"] == row["c14n_sha256_right"], "canonical_hash")
    for row in read_json("stage-comparison.json")["rows"]:
        texts = [by_id[key]["text"] for key in row["evidence_ids"]]
        check(
            len(set(texts)) == 1 and row["committee_proposal_vote_decision_text_equal"],
            "four_stage_text_equality",
        )
        check(
            (by_id[row["government_evidence_id"]]["text"] == texts[0])
            == row["government_literal_equal"],
            "government_wording_preserved",
        )
    check(by_id["VOTE-time"]["text"] == "2024-06-21T14:11:27.147", "precise_vote_time")
    check(
        "Votering, se fredag 21. juni" in by_id["DEBATE20-vote-link"]["text"],
        "debate_to_next_day_vote",
    )
    check(
        "debattert 20. juni 2024" in by_id["VOTE21"]["text"]
        and "enstemmig vedtatt" in by_id["VOTE21"]["text"],
        "voting_block_identity_outcome",
    )
    for identifier in ("R2-date-p2", "R2-date-p8", "R2-date-p9", "R2-date-I91"):
        check(
            "20. juni 2024" in by_id[identifier]["text"],
            "contradictory_retrospective_statement_retained",
        )

    for name, field in (
        ("treatment-ledger.json", "rows"),
        ("cross-reference-journal.json", "references"),
    ):
        for row in read_json(name)[field]:
            check(
                bool(row["evidence_ids"]) and set(row["evidence_ids"]) <= by_id.keys(),
                "all_curated_references_resolve",
                row["id"],
            )
    candidate = read_json("candidate-followup.json")
    candidates = json.loads(
        (ROOT / "docs/research/k3-arsinventar-50/case-candidates.json").read_text("utf-8")
    )
    check(
        len(candidates) == 67 and len({r["metadata"]["id"] for r in candidates}) == 66,
        "historical_67_66",
    )
    check(
        not any(r["metadata"]["id"] == "99235" for r in candidates)
        and not candidate["historical_candidate_membership"],
        "99235_not_historical_candidate",
    )
    check(candidate["global_gaps"] == [f"R{i}" for i in range(1, 8)], "R1_R7_unchanged")
    check(
        candidate["selected_monetary_events"] == 5
        and candidate["selected_decision_fields"] == 11
        and not candidate["product_adoption"],
        "no_new_product_event",
    )

    preserved = read_json("preserved-files.json")
    check(preserved["base_commit"] == BASE, "preservation_base")
    check(len(preserved["files"]) == 1070, "all_base_files_except_additive_pointers")
    for row in preserved["files"]:
        data = (ROOT / row["path"]).read_bytes()
        raw_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if raw_blob == row["raw_git_blob"]:
            check(
                len(data) == row["checkout_bytes"] and digest(data) == row["checkout_sha256"],
                "exact_protected_checkout_bytes",
                row["path"],
            )
        verified = raw_blob
        if verified != row["base_git_blob"]:
            verified = (
                subprocess.check_output(
                    ["git", "hash-object", "--path", row["path"], row["path"]], cwd=ROOT
                )
                .decode()
                .strip()
            )
        check(verified == row["base_git_blob"], "protected_git_representation", row["path"])
    changed = (
        subprocess.check_output(["git", "diff", "--name-only", BASE], cwd=ROOT)
        .decode()
        .splitlines()
    )
    check(
        all(
            path in ("AGENTS.md", "docs/kildefunn.md")
            or path.startswith("docs/research/c06-99235-60/")
            for path in changed
        ),
        "only_authorized_changed_paths",
    )
    workflow = (ROOT / ".github/workflows/check.yml").read_text("utf-8")
    check(
        "timeout-minutes: 90" in workflow and "python -m pytest -vv --durations=20" in workflow,
        "complete_ci_and_90_minutes_preserved",
    )

    for path in PACK.rglob("*.json"):
        if "reviews" not in path.relative_to(PACK).parts:
            json.loads(path.read_text("utf-8-sig"))
            COUNTS["json_parsed"] += 1
    for path in [*PACK.glob("*.md"), ROOT / "AGENTS.md", ROOT / "docs/kildefunn.md"]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text("utf-8")):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            check(
                (path.parent / target.split("#", 1)[0].strip("<>")).exists(),
                "local_markdown_target",
                target,
            )
    manifest_path = PACK / "delivery-manifest.json"
    if manifest_path.exists():
        manifest = read_json("delivery-manifest.json")
        actual = {
            p.relative_to(ROOT).as_posix()
            for p in PACK.rglob("*")
            if p.is_file()
            and p.name != "delivery-manifest.json"
            and not {"reviews", "__pycache__"}.intersection(p.relative_to(PACK).parts)
        } | {"AGENTS.md", "docs/kildefunn.md"}
        check(
            {r["path"] for r in manifest["files"]} == actual, "delivery_manifest_complete_inventory"
        )
        for row in manifest["files"]:
            data = (ROOT / row["path"]).read_bytes()
            if row["representation"] == "utf-8-lf":
                data = data.replace(b"\r\n", b"\n")
            check(
                len(data) == row["bytes"] and digest(data) == row["sha256"],
                "delivery_file_hash",
                row["path"],
            )
            if len(sys.argv) == 2:
                blob = subprocess.check_output(
                    ["git", "show", f"{sys.argv[1]}:{row['path']}"], cwd=ROOT
                )
                check(blob == data, "candidate_git_blob_bytes", row["path"])
    print(
        json.dumps(
            {
                "schema": "c06-offline-verification-1",
                "checked_utc": datetime.now(UTC).isoformat(),
                "base_commit": BASE,
                "runtime": sys.version,
                "checks": dict(COUNTS),
                "total_checks": sum(COUNTS.values()),
                "failures": 0,
                "git_revision": sys.argv[1] if len(sys.argv) == 2 else None,
                "boundary": (
                    "Builder offline checks only. No new HTTP, independent "
                    "review/audit, full product suite, Linux CI, publication or "
                    "merge. Visual paraphrases are image-bound but require "
                    "independent reading."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
