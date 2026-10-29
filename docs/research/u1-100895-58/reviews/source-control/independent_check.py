"""Independent offline source control of fixed U1 candidate; stdout only.

Does not import or execute the builder's verifier. Monetary rows are rediscovered
by walking original tables rather than trusting the supplied row locators.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[5]
PACK = ROOT / "docs/research/u1-100895-58"
BASE = "59485e6bb6e45dacf348451b380cf6ba3b5d8321"
CANDIDATE = "e34b2fae67df6417807109e36eaeadc4c40c89fc"
NS = {"s": "http://data.stortinget.no"}
counts = Counter()
cache = {}


def require(condition, control):
    if not condition:
        raise AssertionError(control)
    counts[control] += 1


def sha(data):
    return hashlib.sha256(data).hexdigest()


def document(name):
    return json.loads((PACK / name).read_text("utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def raw_source(path):
    data = (ROOT / path).read_bytes()
    return gzip.decompress(data) if str(path).endswith(".gz") else data


def parse(path, xml=False):
    if (path, xml) not in cache:
        raw = raw_source(path)
        parser = etree.XMLParser(no_network=True, resolve_entities=False)
        cache[path, xml] = etree.fromstring(raw, parser) if xml else html.fromstring(raw)
    return cache[path, xml]


def norm(node):
    return " ".join(" ".join(node.itertext()).split())


def one(root, xpath, namespaces=None):
    nodes = root.xpath(xpath, namespaces=namespaces or {})
    require(len(nodes) == 1, "unique_selection")
    return nodes[0]


def field(node, name):
    return node.findtext("s:" + name, namespaces=NS)


def monetary_rows(root):
    """Discover all amount rows from table structure and following level row."""
    derived = []
    for table in root.xpath(".//table"):
        chapter = None
        rows = table.xpath(".//tr")
        for index, row in enumerate(rows):
            cells = row.xpath("./td|./th")
            values = [norm(c) for c in cells]
            if len(values) == 4 and re.fullmatch(r"\d{3,4}", values[0]):
                chapter = values[0]
            if len(values) != 4 or not re.fullmatch(r"\d{1,2}", values[1]):
                continue
            require(chapter is not None, "discovered_chapter")
            require(re.fullmatch(r"[\d ]+", values[3]) is not None, "discovered_amount")
            direction = re.search(r"blir (auka|redusert) med$", values[2])
            require(direction is not None, "discovered_amount_role")
            next_cells = rows[index + 1].xpath("./td|./th")
            levels = norm(next_cells[2])
            match = re.fullmatch(r"frå kr ([\d ]+) til kr ([\d ]+)", levels)
            require(match is not None, "discovered_before_after")
            before, after = (int(v.replace(" ", "")) for v in match.groups())
            delta = int(values[3].replace(" ", ""))
            if direction.group(1) == "redusert":
                delta = -delta
            require(before + delta == after, "independent_row_arithmetic")
            derived.append(
                {
                    "account": chapter + "/" + str(int(values[1])),
                    "before": before,
                    "delta": delta,
                    "after": after,
                    "raw_delta": values[3],
                    "raw_role": values[2],
                    "raw_levels": levels,
                }
            )
    return derived


def triples(rows):
    return [(r["account"], r["before"], r["delta"], r["after"]) for r in rows]


def main():
    require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE, "fixed_candidate")
    require(git("merge-base", BASE, CANDIDATE).decode().strip() == BASE, "fixed_base")
    require(not git("diff", "--name-only", CANDIDATE).strip(), "no_tracked_worktree_mutation")
    attempts = document("source-manifest.json")["sources"]
    require(len(attempts) == 15, "fifteen_attempts")
    require(sum(a["state"] == "complete" for a in attempts) == 14, "fourteen_responses")
    for a in attempts:
        meta_raw = (PACK / a["metadata"]).read_bytes()
        meta = json.loads(meta_raw)
        require(
            len(meta_raw) == a["metadata_bytes"] and sha(meta_raw) == a["metadata_sha256"],
            "metadata_hash_size",
        )
        for key, value in meta.items():
            if key in a:
                if key == "archive":
                    require(
                        (PACK / a[key]).resolve() == (PACK / "originals" / value).resolve(),
                        "manifest_metadata_archive_resolution",
                    )
                else:
                    require(a[key] == value, "manifest_metadata_consistency")
        start = datetime.fromisoformat(a["started_utc"])
        end = datetime.fromisoformat(a["completed_utc"])
        require(
            datetime(2026, 10, 29, 13, 45, 35, tzinfo=UTC) < start <= end,
            "contract_and_request_time_order",
        )
        if a["state"] != "complete":
            require(
                a["id"] == "case100895.xml" and "archive" not in a and "sha256" not in a,
                "failed_attempt_has_no_body",
            )
            continue
        archive = (PACK / a["archive"]).read_bytes()
        raw = gzip.decompress(archive)
        require(
            len(archive) == a["archive_bytes"] and sha(archive) == a["archive_sha256"],
            "archive_hash_size",
        )
        require(len(raw) == a["bytes"] and sha(raw) == a["sha256"], "response_hash_size")
        require(a["status"] == 200, "response_status")
        headers = {k.lower(): v for k, v in a["response_headers"]}
        if "content-length" in headers:
            require(len(raw) == int(headers["content-length"]), "response_declared_length")
        require(
            headers.get("content-encoding", "identity") == "identity", "response_identity_encoding"
        )
        if a["id"].endswith(".xml"):
            parse(str((PACK / a["archive"]).relative_to(ROOT)), True)
            counts["complete_xml_parse"] += 1
        if a["id"].endswith(".html"):
            require(raw.rstrip().lower().endswith(b"</html>"), "html_end_envelope")
        if a["id"].endswith(".pdf"):
            require(raw.startswith(b"%PDF-") and b"%%EOF" in raw[-1024:], "pdf_envelope_only")
    for a in document("reused-sources.json")["files"]:
        raw = (ROOT / a["path"]).read_bytes()
        require(len(raw) == a["bytes"] and sha(raw) == a["sha256"], "reused_file_hash_size")
        require(raw == git("show", BASE + ":" + a["path"]), "reused_file_exact_base_blob")
        if "body_sha256" in a:
            body = gzip.decompress(raw)
            require(
                sha(body) == a["body_sha256"] and len(body) == a["body_bytes"],
                "reused_body_hash_size",
            )

    evidence = document("evidence.json")["evidence"]
    require(len(evidence) == len({e["id"] for e in evidence}) == 163, "all_163_evidence_unique")
    evid = {e["id"]: e for e in evidence}
    for e in evidence:
        raw = raw_source(e["path"])
        require(sha(raw) == e["source_sha256"], "evidence_source_hash")
        item = one(parse(e["path"], bool(e["namespaces"])), e["xpath"], e["namespaces"])
        if e["inner_html_field"]:
            item = html.fromstring(item.find(e["inner_html_field"], namespaces=NS).text)
        require(norm(item) == e["text"], "all_evidence_exact_extracted_text")

    def primary(name):
        return parse(
            str((PACK / "originals" / (name + ".gz")).relative_to(ROOT)), name.endswith(".xml")
        )

    index = parse("docs/research/k3-arsinventar-50/originals/saker-2024-2025.xml.gz", True)
    indexed = one(index, "/s:saker_oversikt/s:saker_liste/s:sak[616]", NS)
    require(field(indexed, "id") == "100895", "ordinal_616_case_identity")
    require(
        "16627" in norm(indexed) and "2024-2025" in norm(indexed), "index_recommendation_session"
    )
    maincase = primary("case100895-retry.xml")
    require(
        field(maincase, "id") == "100895" and field(maincase, "sak_sesjon") == "2024-2025",
        "new_case_identity_session",
    )
    exclusions = {"1541", "1542", "1543", "1565", "4565", "5579", "5607"}
    for case_id, chapters, recommendation in [
        ("100932", {"1541", "1542", "1543", "5579"}, "88"),
        ("100933", {"1565", "4565", "5607"}, "99"),
    ]:
        body = primary("case" + case_id + ".xml")
        require(
            field(body, "id") == case_id and field(body, "sak_sesjon") == "2024-2025",
            "sister_identity_session",
        )
        require(
            all(ch in norm(body) for ch in chapters) and "Innst. " + recommendation in norm(body),
            "sister_explicit_scope",
        )

    prop = one(primary("prop21-ch4.html"), "//*[@data-longdoc-content]")
    recommendation = one(primary("inns87-all.html"), "//*[@id='m3']")
    proposals = primary("vot23886-forslag.xml").findall(
        "s:voteringsforslag_liste/s:voteringsforslag", NS
    )
    require(
        [field(p, "forslag_id") for p in proposals] == [str(x) for x in range(40077034, 40077038)],
        "four_proposal_ids",
    )
    require(all(field(p, "forslag_type") == "tilraading" for p in proposals), "four_proposal_roles")
    vote = primary("case100895-voteringer.xml").findall("s:sak_votering_liste/s:sak_votering", NS)
    require(len(vote) == 1 and field(vote[0], "votering_id") == "23886", "one_case_vote_id")
    require(
        field(vote[0], "votering_tid") == "2024-12-17T19:29:01.44"
        and field(vote[0], "sak_id") == "100895",
        "vote_time_case",
    )
    require(
        field(vote[0], "votering_resultat_type") == "enstemmig_vedtatt"
        and field(vote[0], "vedtatt") == "true",
        "unanimous_adopted_vote",
    )
    require(
        [field(vote[0], f) for f in ("antall_for", "antall_mot", "antall_ikke_tilstede")]
        == ["-1"] * 3,
        "raw_vote_sentinels_preserved",
    )
    mappings = primary("vot23886-vedtak.xml").findall(
        "s:voteringsvedtak_liste/s:voteringsvedtak", NS
    )
    require(
        [field(m, "vedtak_nummer") for m in mappings] == [str(n) for n in range(226, 230)],
        "four_final_mappings",
    )
    for m, roman in zip(mappings, ("I", "II", "III", "IV"), strict=True):
        require(
            field(m, "vedtak_referanse").strip() == "(Komiteens tilråding " + roman + ". )",
            "exact_roman_mapping",
        )
    final_root = parse(
        "docs/research/k3-arsinventar-50/originals/ind-vedtak-2024-2025.xml.gz", True
    )
    old_root = parse("docs/research/to-visninger-37/originals/aar/session-2024-2025.xml.gz", True)
    finals = []
    canonical_results = []
    for number in range(226, 230):
        xp = "//s:stortingsvedtak[s:stortingsvedtak_nummer='" + str(number) + "']"
        obj = one(final_root, xp, NS)
        old = one(old_root, xp, NS)
        require(
            field(obj, "id") == str(40034094 + number - 226) and field(obj, "sak_id") == "100895",
            "final_id_case",
        )
        require(
            field(obj, "stortingsvedtak_dato_tid") == "2024-12-17T00:00:00", "final_decision_date"
        )
        canonical = etree.tostring(obj, method="c14n", with_comments=False)
        require(
            canonical == etree.tostring(old, method="c14n", with_comments=False),
            "four_complete_canonical_objects_match",
        )
        expected = next(
            r for r in document("source-comparison.json")["comparisons"] if r["number"] == number
        )
        require(
            len(canonical) == expected["canonical_bytes"]
            and sha(canonical) == expected["canonical_sha256"],
            "canonical_manifest_hash_size",
        )
        canonical_results.append(
            {"number": number, "sha256": sha(canonical), "bytes": len(canonical)}
        )
        finals.append(html.fromstring(field(obj, "stortingsvedtak_tekst")))
    record = one(
        parse("docs/research/r2-101000-54/originals/ref171224-votering.html.gz"),
        "//*[@id='2024-12-17-5']",
    )
    debate = one(primary("referat-debatt5.html"), "//*[@data-strtngt-sak-sakid='100895']")
    require("Ingen har bedt om ordet." in norm(debate), "complete_short_debate")
    require("samrøystes" in norm(record), "voting_record_adoption")
    derived = {
        "proposal": monetary_rows(prop),
        "committee": monetary_rows(recommendation),
        "vote_proposal": monetary_rows(html.fromstring(field(proposals[0], "forslag_tekst"))),
        "voting_record": monetary_rows(record),
        "decision226": monetary_rows(finals[0]),
    }
    selected = [r for r in derived["proposal"] if r["account"].split("/")[0] not in exclusions]
    excluded = [r for r in derived["proposal"] if r["account"].split("/")[0] in exclusions]
    require(
        len(derived["proposal"]) == 32 and len(selected) == 21 and len(excluded) == 11,
        "independent_32_21_11_split",
    )
    for stage in derived:
        if stage != "proposal":
            require(
                triples(derived[stage]) == triples(selected),
                "all_independently_discovered_stages_equal",
            )
        supplied = document("table-comparison.json")["stages"][stage]
        require(
            triples(derived[stage]) == triples(supplied), "complete_supplied_table_matches_original"
        )
        for actual, declared in zip(derived[stage], supplied, strict=True):
            require(
                (actual["raw_delta"], actual["raw_role"], actual["raw_levels"])
                == (declared["amount_raw"], declared["meaning_raw"], declared["before_after_raw"]),
                "supplied_raw_cell_content",
            )
    require(
        not {"1429/1", "1429/22", "1560/71"} & {r["account"] for r in selected},
        "no_target_or_C05_monetary_row",
    )
    for stage in (
        one(prop, "(.//*[@class='K-DEL-VEDTAKDEL'])[4]"),
        one(recommendation, ".//*[@data-strtngt-romertallseksjon-romertall='iv']"),
        html.fromstring(field(proposals[3], "forslag_tekst")),
        finals[3],
    ):
        text = norm(stage)
        require(
            all(
                v in text
                for v in (
                    "i 2024",
                    "1560",
                    "post 71",
                    "kan overførast",
                    "Opplæring og utvikling av tillitsvalde",
                )
            ),
            "C05_all_four_text_scopes",
        )
    for number, amount in [(1, "8 531"), (2, "627")]:
        text = norm(finals[number])
        require(
            all(
                v in text
                for v in ("i 2025", amount, "1. juli 2025", "seinare budsjettår", "kostnadsramm")
            ),
            "future_cost_frame_scope",
        )
    ledger = document("treatment-ledger.json")["rows"]
    refs = document("cross-reference-journal.json")["references"]
    require(len(ledger) == 13 and len(refs) == 12, "thirteen_ledger_twelve_crossrefs")
    for row in ledger + refs:
        require(all(eid in evid for eid in row["evidence_ids"]), "all_ledger_crossref_bindings")

    protected = document("preserved-files.json")["files"]
    require(len(protected) == 627, "protected_file_count")
    trees = {}
    for revision in (BASE, CANDIDATE):
        trees[revision] = {}
        for entry in git("ls-tree", "-rz", revision).split(b"\0"):
            if entry:
                description, name = entry.split(b"\t", 1)
                trees[revision][name.decode()] = description.split()[2].decode()
    for row in protected:
        path = row["path"]
        old = trees[BASE][path]
        new = trees[CANDIDATE][path]
        require(old == new, "protected_git_blob_unchanged")
        raw = (ROOT / path).read_bytes()
        if row["comparison_representation"] == "utf-8-lf":
            raw = raw.replace(b"\r\n", b"\n")
            require(
                sha(raw) == row["git_blob_sha256"] and len(raw) == row["git_blob_bytes"],
                "protected_declared_LF_representation",
            )
        else:
            require(
                sha(raw) == row["checkout_sha256"] and len(raw) == row["checkout_bytes"],
                "protected_exact_checkout",
            )
    require(not git("diff", "--name-only", CANDIDATE).strip(), "no_tracked_worktree_mutation")
    print(
        json.dumps(
            {
                "candidate": CANDIDATE,
                "base": BASE,
                "result": "PASS",
                "checked_utc": datetime.now(UTC).isoformat(),
                "independence": (
                    "Own implementation; no builder verifier imported or executed; "
                    "monetary tables rediscovered from raw table rows."
                ),
                "controls": dict(sorted(counts.items())),
                "source_counts": {
                    "attempts": len(attempts),
                    "responses": 14,
                    "evidence": len(evidence),
                    "ledger": len(ledger),
                    "crossrefs": len(refs),
                    "protected": len(protected),
                },
                "table_accounts": {k: triples(v) for k, v in derived.items()},
                "complete_canonical_decisions": canonical_results,
                "limits": [
                    "Offline frozen source observations; no new remote source version asserted.",
                    "PDF envelope only, no text or visual comparison.",
                    "Source control is not annual coverage, accounting approval, "
                    "production adoption, Standards/Spec or security audit.",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
