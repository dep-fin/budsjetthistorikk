"""Independent, offline specification probes for the fixed U1 candidate."""

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
PREFIX = "docs/research/u1-100895-58/"
BASE = "59485e6bb6e45dacf348451b380cf6ba3b5d8321"
CANDIDATE = "e34b2fae67df6417807109e36eaeadc4c40c89fc"
NS = {"s": "http://data.stortinget.no"}
COUNTS = Counter()
CACHE = {}


def check(condition, group, detail=""):
    if not condition:
        raise AssertionError(f"{group}: {detail}")
    COUNTS[group] += 1


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def tree(ref):
    result = {}
    for row in git("ls-tree", "-rz", ref).split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            result[path.decode()] = meta.split()[2].decode()
    return result


def blob(path):
    if path not in CACHE:
        CACHE[path] = git("show", f"{CANDIDATE}:{path}")
    return CACHE[path]


def data(name):
    return json.loads(blob(PREFIX + name))


def raw(path):
    value = blob(path)
    return gzip.decompress(value) if path.endswith(".gz") else value


def doc(path, xml=False):
    if xml:
        return etree.fromstring(raw(path), etree.XMLParser(resolve_entities=False, no_network=True))
    return html.fromstring(raw(path))


def text(node):
    return " ".join(" ".join(node.itertext()).split())


def triples(node):
    """Discover all money rows before consulting the delivered table inventory."""
    found = []
    chapter = None
    pending = None
    for row in node.xpath(".//tr"):
        cells = [text(c) for c in row.xpath("./td|./th")]
        if len(cells) != 4:
            continue
        if re.fullmatch(r"\d{4}", cells[0]):
            chapter = cells[0]
        if re.fullmatch(r"\d{1,2}", cells[1]) and re.fullmatch(r"[\d ]+", cells[3]):
            check(pending is None and chapter is not None, "independent_table_structure")
            magnitude = int(cells[3].replace(" ", ""))
            check(("auka" in cells[2]) != ("redusert" in cells[2]), "independent_table_direction")
            pending = (
                f"{chapter}/{int(cells[1])}",
                -magnitude if "redusert" in cells[2] else magnitude,
            )
        match = re.fullmatch(r"frå kr ([\d ]+) til kr ([\d ]+)", cells[2])
        if match:
            check(pending is not None, "independent_before_after_has_change")
            before, after = (int(v.replace(" ", "")) for v in match.groups())
            check(before + pending[1] == after, "independent_arithmetic", pending[0])
            found.append((pending[0], before, pending[1], after))
            pending = None
    check(pending is None, "independent_no_unfinished_row")
    return found


def main():
    check(git("merge-base", BASE, CANDIDATE).decode().strip() == BASE, "fixed_base")
    check(git("rev-parse", "HEAD").decode().strip() == CANDIDATE, "fixed_candidate")
    before, after = tree(BASE), tree(CANDIDATE)
    changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
    check(len(changed) == 52, "candidate_file_count")
    check(
        all(p.startswith(PREFIX) or p in {"AGENTS.md", "docs/kildefunn.md"} for p in changed),
        "scope_only",
    )
    check(all(p not in before for p in changed if p.startswith(PREFIX)), "research_is_additive")
    for row in data("preserved-files.json")["files"]:
        check(
            before[row["path"]] == after[row["path"]] == row["git_blob_oid"],
            "protected_git_blobs",
            row["path"],
        )
    for row in data("delivery-manifest.json")["files"]:
        value = blob(row["path"])
        if row["representation"] == "utf-8-lf":
            value = value.replace(b"\r\n", b"\n")
        check(
            len(value) == row["bytes"] and hashlib.sha256(value).hexdigest() == row["sha256"],
            "candidate_manifest_blob",
            row["path"],
        )
    check(
        {r["path"] for r in data("delivery-manifest.json")["files"]}
        == changed - {PREFIX + "delivery-manifest.json"},
        "manifest_matches_candidate",
    )

    for row in data("source-manifest.json")["sources"]:
        meta_bytes = blob(PREFIX + row["metadata"])
        meta = json.loads(meta_bytes)
        comparable_meta = dict(meta)
        if "archive" in meta:
            comparable_meta["archive"] = (Path(row["metadata"]).parent / meta["archive"]).as_posix()
        check(
            all(row[k] == v for k, v in comparable_meta.items()),
            "manifest_transport_matches_sidecar",
            row["id"],
        )
        check(hashlib.sha256(meta_bytes).hexdigest() == row["metadata_sha256"], "metadata_digest")
        check(
            datetime(2026, 10, 29, 13, 45, 35, tzinfo=UTC)
            < datetime.fromisoformat(meta["started_utc"])
            <= datetime.fromisoformat(meta["completed_utc"]),
            "authorization_before_attempt",
        )
        if row["state"] == "complete":
            content = raw(PREFIX + row["archive"])
            check(
                len(content) == row["bytes"]
                and hashlib.sha256(content).hexdigest() == row["sha256"],
                "complete_source_digest",
            )
        else:
            check(
                row["state"] == "transport_failed" and "archive" not in row,
                "failed_attempt_without_source",
            )

    evidence = {e["id"]: e for e in data("evidence.json")["evidence"]}
    for row in evidence.values():
        node = doc(row["path"], bool(row["namespaces"]))
        selected = node.xpath(row["xpath"], namespaces=row["namespaces"])
        check(len(selected) == 1, "exact_locator_unique", row["id"])
        check(
            hashlib.sha256(raw(row["path"])).hexdigest() == row["source_sha256"],
            "exact_locator_digest",
        )
        node = selected[0]
        if row["inner_html_field"]:
            node = html.fromstring(node.find(row["inner_html_field"], NS).text)
        check(text(node) == row["text"], "exact_locator_text", row["id"])

    def primary(name, xml=False):
        return doc(PREFIX + "originals/" + name + ".gz", xml)

    proposal = primary("prop21-ch4.html")
    committee = primary("inns87-all.html")
    vote_proposals = primary("vot23886-forslag.xml", True)
    proposal_nodes = vote_proposals.findall("s:voteringsforslag_liste/s:voteringsforslag", NS)
    decision_root = doc(evidence["D-226"]["path"], True)
    decisions = {
        n: decision_root.xpath(
            f'//s:stortingsvedtak[s:stortingsvedtak_nummer="{n}"]', namespaces=NS
        )[0]
        for n in range(226, 230)
    }
    voting = doc(evidence["VOTE5"]["path"]).xpath('//*[@id="2024-12-17-5"]')[0]
    discovered = {
        "proposal": triples(proposal),
        "committee": triples(committee),
        "vote_proposal": triples(
            html.fromstring(proposal_nodes[0].findtext("s:forslag_tekst", namespaces=NS))
        ),
        "voting_record": triples(voting),
        "decision226": triples(
            html.fromstring(decisions[226].findtext("s:stortingsvedtak_tekst", namespaces=NS))
        ),
    }
    excluded = {"1541", "1542", "1543", "1565", "4565", "5579", "5607"}
    selected = [r for r in discovered["proposal"] if r[0].split("/")[0] not in excluded]
    check(len(discovered["proposal"]) == 32 and len(selected) == 21, "independent_sister_split")
    check(
        all(r[0] not in {"1429/1", "1429/22", "1560/71"} for r in selected),
        "no_target_money_or_C05_money_row",
    )
    for key, values in discovered.items():
        check(
            values
            == [
                (r["account"], r["before"], r["delta"], r["after"])
                for r in data("table-comparison.json")["stages"][key]
            ],
            "table_inventory_complete",
            key,
        )
        if key != "proposal":
            check(values == selected, "all_treatment_money_equal", key)

    case = primary("case100895-retry.xml", True)
    check(
        case.findtext("s:id", namespaces=NS) == "100895"
        and case.findtext("s:sak_sesjon", namespaces=NS) == "2024-2025",
        "case_identity",
    )
    check(
        all(ch in case.findtext("s:henvisning", namespaces=NS) for ch in excluded),
        "case_explicit_exclusions",
    )
    for case_id, title in [("100932", "Innst. 88"), ("100933", "Innst. 99")]:
        sister = primary(f"case{case_id}.xml", True)
        check(
            sister.findtext("s:id", namespaces=NS) == case_id
            and title in sister.findtext("s:henvisning", namespaces=NS),
            "sister_identity_only",
        )
    check(
        [n.findtext("s:forslag_id", namespaces=NS) for n in proposal_nodes]
        == [str(n) for n in range(40077034, 40077038)],
        "four_proposals",
    )
    mappings = primary("vot23886-vedtak.xml", True).findall(
        "s:voteringsvedtak_liste/s:voteringsvedtak", NS
    )
    for n, roman in zip(range(226, 230), ["I", "II", "III", "IV"], strict=True):
        decision, mapping, offer = decisions[n], mappings[n - 226], proposal_nodes[n - 226]
        check(
            mapping.findtext("s:vedtak_nummer", namespaces=NS) == str(n)
            and mapping.findtext("s:vedtak_referanse", namespaces=NS).strip()
            == f"(Komiteens tilråding {roman}. )",
            "roman_to_decision",
        )
        check(
            decision.findtext("s:id", namespaces=NS) == str(40034094 + n - 226)
            and decision.findtext("s:sak_id", namespaces=NS) == "100895",
            "decision_object_identity",
        )
        offer_text = text(html.fromstring(offer.findtext("s:forslag_tekst", namespaces=NS)))
        decision_text = text(
            html.fromstring(decision.findtext("s:stortingsvedtak_tekst", namespaces=NS))
        )
        if n > 226:
            check(offer_text == decision_text, "full_authority_proposal_to_decision")
        if n in {227, 228}:
            check(
                "i 2025" in decision_text
                and "seinare budsjettår" in decision_text
                and "kostnadsramme" in decision_text,
                "authority_year_and_role",
            )
        if n == 229:
            check(
                "i 2024" in decision_text
                and "1560" in decision_text
                and "post 71" in decision_text
                and "kan overførast" in decision_text,
                "C05_scope_and_year",
            )
    votes = primary("case100895-voteringer.xml", True).findall(
        "s:sak_votering_liste/s:sak_votering", NS
    )
    check(
        len(votes) == 1
        and votes[0].findtext("s:votering_id", namespaces=NS) == "23886"
        and votes[0].findtext("s:votering_resultat_type", namespaces=NS) == "enstemmig_vedtatt",
        "single_unanimous_vote",
    )
    check(
        [
            votes[0].findtext(f"s:{field}", namespaces=NS)
            for field in ["antall_for", "antall_mot", "antall_ikke_tilstede"]
        ]
        == ["-1", "-1", "-1"],
        "raw_vote_sentinels",
    )

    ledger = {r["id"]: r for r in data("treatment-ledger.json")["rows"]}
    check(
        len(ledger) == 13 and len(data("cross-reference-journal.json")["references"]) == 12,
        "separate_journal_inventory",
    )
    check(
        all(
            not r["product_adoption"] and r["professional_approval"] == "none"
            for r in ledger.values()
        ),
        "ledger_not_adopted",
    )
    for name, key in [
        ("treatment-ledger.json", "rows"),
        ("cross-reference-journal.json", "references"),
    ]:
        for row in data(name)[key]:
            check(
                all(e in evidence for e in row["evidence_ids"]), "journal_locators_bound", row["id"]
            )
    followup = data("candidate-followup.json")
    candidates = json.loads(blob("docs/research/k3-arsinventar-50/case-candidates.json"))
    historical = [
        r for r in candidates if r["session"] == "2024-2025" and r["ordinal_1based"] == 616
    ]
    check(
        len(historical) == 1
        and historical[0]["metadata"]["id"] == "100895"
        and historical[0]["metadata"]["innstilling_id"] == "16627",
        "historical_candidate_identity",
    )
    check(
        historical[0]["status"] == followup["historical_status"] == "open_title_candidate",
        "historical_status_untouched",
    )
    check(
        followup["selected_monetary_events"] == 5
        and followup["selected_decision_fields"] == 11
        and followup["global_gaps"] == [f"R{n}" for n in range(1, 8)],
        "five_eleven_and_R_gaps",
    )
    check(
        not followup["professional_annual_balance_approval"]
        and not followup["product_adoption"]
        and followup["year_coverage"] == "partial",
        "no_annual_or_product_adoption",
    )
    print(
        json.dumps(
            {
                "candidate": CANDIDATE,
                "base": BASE,
                "checked_utc": datetime.now(UTC).isoformat(),
                "checks": dict(COUNTS),
                "total": sum(COUNTS.values()),
                "failures": 0,
                "independently_discovered_money_rows": {k: len(v) for k, v in discovered.items()},
                "boundary": (
                    "Frozen Git blobs; no new HTTP, product tests, full CI, publication or merge. "
                    "Semantic reading is reported separately."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
