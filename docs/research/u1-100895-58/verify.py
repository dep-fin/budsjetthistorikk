"""Offline source, locator and compatibility checks for research ticket 58."""

import gzip
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[3]
PACK = Path(__file__).resolve().parent
BASE = "59485e6bb6e45dacf348451b380cf6ba3b5d8321"
NS = {"s": "http://data.stortinget.no"}
COUNTS: Counter[str] = Counter()
CACHE = {}


def check(condition, name, detail=""):
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    COUNTS[name] += 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(name):
    return json.loads((PACK / name).read_text("utf-8"))


def normalized(node):
    return " ".join(" ".join(node.itertext()).split())


def source(path, xml=False):
    if (path, xml) not in CACHE:
        raw = (ROOT / path).read_bytes()
        if path.endswith(".gz"):
            raw = gzip.decompress(raw)
        parser = etree.XMLParser(resolve_entities=False, no_network=True)
        node = etree.fromstring(raw, parser) if xml else html.fromstring(raw)
        CACHE[path, xml] = (raw, node)
    return CACHE[path, xml]


def main():
    attempts = read_json("source-manifest.json")["sources"]
    check(len(attempts) == 15, "transport_attempt_count")
    check(sum(r["state"] == "complete" for r in attempts) == 14, "complete_response_count")
    for row in attempts:
        meta = (PACK / row["metadata"]).read_bytes()
        check(len(meta) == row["metadata_bytes"], "transport_metadata_size", row["id"])
        check(digest(meta) == row["metadata_sha256"], "transport_metadata_hash", row["id"])
        values = json.loads(meta)
        check(values["started_utc"] > "2026-10-29T13:45:35", "contract_before_source_work")
        check(values["completed_utc"] >= values["started_utc"], "transport_time_order")
        if row["state"] != "complete":
            check(row["id"] == "case100895.xml", "recorded_dns_failure")
            check("archive" not in row and "bytes" not in row, "no_fabricated_response")
            continue
        data = (PACK / row["archive"]).read_bytes()
        raw = gzip.decompress(data)
        check(len(data) == row["archive_bytes"], "archive_size", row["id"])
        check(digest(data) == row["archive_sha256"], "archive_hash", row["id"])
        check(len(raw) == row["bytes"] == values["bytes"], "response_size", row["id"])
        check(digest(raw) == row["sha256"] == values["sha256"], "response_hash", row["id"])
        check(values["status"] == row["status"] == 200, "http_200")
        headers = {k.lower(): v for k, v in values["response_headers"]}
        if "content-length" in headers:
            check(int(headers["content-length"]) == len(raw), "http_content_length")
        check(headers.get("content-encoding", "identity") == "identity", "entity_representation")
        if row["id"].endswith(".html"):
            check(raw.rstrip().lower().endswith(b"</html>"), "complete_html_end")
        if row["id"].endswith(".xml"):
            etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
            COUNTS["complete_xml"] += 1
        if row["id"].endswith(".pdf"):
            check(raw.startswith(b"%PDF") and b"%%EOF" in raw[-1024:], "complete_pdf_envelope")

    for row in read_json("reused-sources.json")["files"]:
        raw = (ROOT / row["path"]).read_bytes()
        check(len(raw) == row["bytes"] and digest(raw) == row["sha256"], "reused_file")
        if "body_sha256" in row:
            body = gzip.decompress(raw)
            check(len(body) == row["body_bytes"], "reused_body_size")
            check(digest(body) == row["body_sha256"], "reused_body_hash")

    evidence = read_json("evidence.json")["evidence"]
    by_id = {row["id"]: row for row in evidence}
    check(len(by_id) == len(evidence) == 163, "unique_evidence_ids")
    for row in evidence:
        raw, node = source(row["path"], bool(row["namespaces"]))
        check(digest(raw) == row["source_sha256"], "evidence_source_hash", row["id"])
        selected = node.xpath(row["xpath"], namespaces=row["namespaces"])
        check(len(selected) == 1, "evidence_unique_xpath", row["id"])
        actual = selected[0]
        if row["inner_html_field"]:
            actual = html.fromstring(actual.find(row["inner_html_field"], NS).text)
        check(normalized(actual) == row["text"], "evidence_exact_text", row["id"])

    comparison = read_json("table-comparison.json")
    triples = {}
    for stage, rows in comparison["stages"].items():
        triples[stage] = []
        for row in rows:
            key = row["source_key"]
            path = next(e["path"] for e in evidence if e["source_key"] == key)
            _, node = source(path, key.endswith(".xml") or key == "K3-decisions")
            if row["inner_html_field"]:
                found = node.xpath(row["outer_xpath"], namespaces=NS)
                check(len(found) == 1, "table_outer_object")
                node = html.fromstring(found[0].find(row["inner_html_field"], NS).text)
            delta_node = node.xpath(row["delta_xpath"])
            before_after_node = node.xpath(row["before_after_xpath"])
            check(len(delta_node) == len(before_after_node) == 1, "table_unique_cell")
            check(normalized(delta_node[0]) == row["amount_raw"], "table_delta_raw")
            text = normalized(before_after_node[0])
            check(text == row["before_after_raw"], "table_before_after_raw")
            match = re.fullmatch(r"frå kr ([\d ]+) til kr ([\d ]+)", text)
            check(bool(match), "table_monetary_syntax")
            before, after = [int(s.replace(" ", "")) for s in match.groups()]
            magnitude = int(row["amount_raw"].replace(" ", ""))
            delta = magnitude * (-1 if "redusert" in row["meaning_raw"] else 1)
            check(
                (before, delta, after) == (row["before"], row["delta"], row["after"]),
                "table_values",
            )
            check(before + delta == after, "table_arithmetic")
            cells = delta_node[0].getparent().xpath("./td|./th")
            check(normalized(cells[1]) == row["post_raw"], "table_raw_post")
            check(normalized(cells[2]) == row["meaning_raw"], "table_raw_meaning")
            check(
                row["account"] == row["chapter"] + "/" + str(int(row["post_raw"])),
                "account_identity",
            )
            preceding = delta_node[0].getparent().xpath("preceding-sibling::tr")
            chapter_cells = [r.xpath("./td|./th") for r in preceding]
            chapters = [
                normalized(c[0])
                for c in chapter_cells
                if c and re.fullmatch(r"\d{3,4}", normalized(c[0]))
            ]
            check(bool(chapters) and chapters[-1] == row["chapter"], "table_chapter_context")
            triples[stage].append((row["account"], before, delta, after))
    expected = [
        r for r in triples["proposal"] if r[0].split("/")[0] not in comparison["excluded_chapters"]
    ]
    check(len(triples["proposal"]) == 32 and len(expected) == 21, "full_proposal_and_split")
    for stage in ("committee", "vote_proposal", "voting_record", "decision226"):
        check(triples[stage] == expected, "all_selected_stage_triples_equal", stage)
    check("1560/71" not in [r[0] for r in expected], "stikkord_not_monetary_row")

    old_path = "docs/research/to-visninger-37/originals/aar/session-2024-2025.xml.gz"
    new_path = "docs/research/k3-arsinventar-50/originals/ind-vedtak-2024-2025.xml.gz"
    for row in read_json("source-comparison.json")["comparisons"]:
        canonical = []
        for path in [new_path, old_path]:
            node = source(path, True)[1].xpath(row["xpath"], namespaces=NS)
            check(len(node) == 1, "unique_canonical_decision")
            check(node[0].find("s:id", NS).text == row["id"], "canonical_decision_id")
            check(node[0].find("s:sak_id", NS).text == "100895", "canonical_decision_case")
            canonical.append(etree.tostring(node[0], method="c14n", with_comments=False))
        check(canonical[0] == canonical[1], "complete_canonical_decisions_equal")
        check(len(canonical[0]) == row["canonical_bytes"], "canonical_size")
        check(digest(canonical[0]) == row["canonical_sha256"], "canonical_hash")

    for name, key in [
        ("treatment-ledger.json", "rows"),
        ("cross-reference-journal.json", "references"),
    ]:
        for row in read_json(name)[key]:
            for eid in row["evidence_ids"]:
                check(eid in by_id, "ledger_evidence_reference", eid)
    ledger = {r["id"]: r for r in read_json("treatment-ledger.json")["rows"]}
    check(ledger["U06"]["amount"] is None and ledger["U06"]["accounts"] == ["1560/71"], "C05_scope")
    check(ledger["U08"]["budget_year"] == ledger["U09"]["budget_year"] == 2025, "cost_frame_year")
    proposal_path = by_id["F-4"]["path"]
    proposals = source(proposal_path, True)[1].findall(
        "s:voteringsforslag_liste/s:voteringsforslag", NS
    )
    check(
        [p.find("s:forslag_id", NS).text for p in proposals]
        == ["40077034", "40077035", "40077036", "40077037"],
        "four_exact_proposal_ids",
    )
    mapping_path = by_id["vot23886-vedtak.xml"]["path"]
    mappings = source(mapping_path, True)[1].findall(
        "s:voteringsvedtak_liste/s:voteringsvedtak", NS
    )
    check(
        [m.find("s:vedtak_nummer", NS).text for m in mappings] == ["226", "227", "228", "229"],
        "four_exact_decision_mappings",
    )
    check("IV." in mappings[-1].find("s:vedtak_referanse", NS).text, "C05_roman_mapping")
    check("1560" in by_id["F-4"]["text"], "C05_proposal_content")
    check("enstemmig_vedtatt" in by_id["case100895-voteringer.xml"]["text"], "unanimous_vote")
    followup = read_json("candidate-followup.json")
    check(
        followup["selected_monetary_events"] == 5 and followup["selected_decision_fields"] == 11,
        "five_eleven_preserved",
    )
    check(
        followup["year_coverage"] == "partial"
        and not followup["professional_annual_balance_approval"],
        "no_annual_adoption",
    )
    for row in read_json("preserved-files.json")["files"]:
        raw = (ROOT / row["path"]).read_bytes()
        if row["comparison_representation"] == "utf-8-lf":
            raw.decode("utf-8")
            canonical = raw.replace(b"\r\n", b"\n")
            check(
                len(canonical) == row["git_blob_bytes"]
                and digest(canonical) == row["git_blob_sha256"],
                "preserved_declared_text_representation",
                row["path"],
            )
        else:
            check(
                len(raw) == row["checkout_bytes"] and digest(raw) == row["checkout_sha256"],
                "preserved_exact_byte_file",
                row["path"],
            )
    diff = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True)
    check(
        all(
            p in {"AGENTS.md", "docs/kildefunn.md"} or p.startswith("docs/research/u1-100895-58/")
            for p in diff.splitlines()
        ),
        "only_authorized_scope_changed",
    )
    for path in [*PACK.glob("*.md"), ROOT / "AGENTS.md", ROOT / "docs/kildefunn.md"]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text("utf-8")):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            local = target.split("#", 1)[0].strip("<>")
            check((path.parent / local).exists(), "local_markdown_target", target)
    manifest = PACK / "delivery-manifest.json"
    if manifest.exists():
        expected_files = {
            p.relative_to(ROOT).as_posix()
            for p in PACK.rglob("*")
            if p.is_file()
            and p.name != "delivery-manifest.json"
            and "reviews" not in p.relative_to(PACK).parts
        } | {"AGENTS.md", "docs/kildefunn.md"}
        check(
            {row["path"] for row in read_json(manifest.name)["files"]} == expected_files,
            "delivery_manifest_inventory",
        )
        for row in read_json(manifest.name)["files"]:
            raw = (ROOT / row["path"]).read_bytes()
            if row["representation"] == "utf-8-lf":
                raw = raw.replace(b"\r\n", b"\n")
            check(
                len(raw) == row["bytes"] and digest(raw) == row["sha256"],
                "delivery_file",
                row["path"],
            )
    print(
        json.dumps(
            {
                "schema": "u1-verification-1",
                "checked_utc": datetime.now(UTC).isoformat(),
                "base_commit": BASE,
                "runtime": sys.version,
                "lxml": etree.LXML_VERSION,
                "checks": dict(COUNTS),
                "total_checks": sum(COUNTS.values()),
                "failures": 0,
                "boundary": (
                    "Offline source/locator/table/file checks; no new HTTP, product import, "
                    "independent review, full CI or merge."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
