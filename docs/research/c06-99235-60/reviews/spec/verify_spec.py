"""Read fixed C06 Git objects and record bounded independent spec evidence."""

import gzip
import hashlib
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from lxml import etree, html

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PREFIX = "docs/research/c06-99235-60/"
BASE = "49cc6e44851cf74e0aaea4eb333419e5598bfd95"
CANDIDATE = "9eb27cebf7ca4a99aeb30fa32245e41314e0d295"
NS = {"s": "http://data.stortinget.no"}
CHECKS = []


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def blob(path):
    return git("show", f"{CANDIDATE}:{path}")


def read_json(name):
    return json.loads(blob(PREFIX + name))


def xml(name):
    return etree.fromstring(
        gzip.decompress(blob(PREFIX + "originals/" + name)),
        etree.XMLParser(resolve_entities=False, no_network=True),
    )


def check(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    CHECKS.append({"name": name, "actual": actual, "expected": expected})


def tree(revision):
    return {
        line.split(b"\t", 1)[1].decode(): line.split(b"\t", 1)[0].split()[2].decode()
        for line in git("ls-tree", "-r", "-z", revision).split(b"\0")
        if line
    }


def text(node):
    return " ".join(" ".join(node.itertext()).split())


def main():
    check("merge_base", git("merge-base", BASE, CANDIDATE).decode().strip(), BASE)
    before, after = tree(BASE), tree(CANDIDATE)
    protected = {p: sha for p, sha in before.items() if p not in {"AGENTS.md", "docs/kildefunn.md"}}
    check("protected_base_file_count", len(protected), 1070)
    check(
        "protected_Git_objects_unchanged",
        all(after.get(p) == sha for p, sha in protected.items()),
        True,
    )
    changed = git("diff", "--name-only", BASE + "..." + CANDIDATE).decode().splitlines()
    check("changed_file_count", len(changed), 74)
    check(
        "scope",
        all(p in {"AGENTS.md", "docs/kildefunn.md"} or p.startswith(PREFIX) for p in changed),
        True,
    )
    manifest = read_json("delivery-manifest.json")
    for row in manifest["files"]:
        data = blob(row["path"])
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
    check("manifest_Git_blobs", len(manifest["files"]), 73)

    case = xml("case-99235-a2.hop0.gz")
    check("case_session", case.findtext("s:sak_sesjon", namespaces=NS), "2023-2024")
    check("case_id", case.findtext("s:id", namespaces=NS), "99235")
    chronology = {
        n.findtext("s:id", namespaces=NS): n.findtext("s:dato", namespaces=NS)
        for n in case.findall(".//s:saksgang_hendelse", NS)
    }
    check("debate_day", chronology["BEHS"], "20.06.2024 00:00:00")
    check("vote_day", chronology["VOT"], "21.06.2024 00:00:00")
    votes = xml("votes-99235-a1.hop0.gz")
    vote_rows = votes.findall(".//s:sak_votering", NS)
    check("complete_local_vote_list", len(vote_rows), 1)
    vote = vote_rows[0]
    check("vote_id", vote.findtext("s:votering_id", namespaces=NS), "23490")
    check("vote_time", vote.findtext("s:votering_tid", namespaces=NS), "2024-06-21T14:11:27.147")
    check(
        "vote_result", vote.findtext("s:votering_resultat_type", namespaces=NS), "enstemmig_vedtatt"
    )
    proposals = xml("proposals-23490-a1.hop0.gz").findall(".//s:voteringsforslag", NS)
    check(
        "proposal_ids",
        [n.findtext("s:forslag_id", namespaces=NS) for n in proposals],
        [str(n) for n in range(40075780, 40075784)],
    )
    check(
        "proposal_roles",
        [n.findtext("s:forslag_type", namespaces=NS) for n in proposals],
        ["tilraading"] * 4,
    )
    final_map = xml("decisions-23490-a1.hop0.gz").findall(".//s:voteringsvedtak", NS)
    check(
        "final_decision_numbers",
        [n.findtext("s:vedtak_nummer", namespaces=NS) for n in final_map],
        [str(n) for n in range(853, 857)],
    )

    evidence = {n["id"]: n for n in read_json("evidence.json")["evidence"]}
    source_cache = {}
    for identifier in (
        "P108-ch1",
        "P108-ch2",
        "P108-ch3",
        "P108-ch4",
        "I442-m1",
        "I442-m2",
        "I442-m3",
        "DEBATE20",
        "VOTE21",
        "R2-date-p2",
        "R2-date-p8",
        "R2-date-p9",
        "R2-date-I91",
    ):
        row = evidence[identifier]
        if row["path"] not in source_cache:
            raw = gzip.decompress(blob(row["path"]))
            source_cache[row["path"]] = html.fromstring(raw.decode("utf-8-sig"))
        located = source_cache[row["path"]].xpath(row["xpath"])
        check("source_text_" + identifier, text(located[0]), row["text"])
    check(
        "explicit_autumn_appropriation_stage",
        "haustsesjonen 2024" in evidence["P108-ch2"]["text"],
        True,
    )
    check(
        "debate_forward_link", "Votering, se fredag 21. juni" in evidence["DEBATE20"]["text"], True
    )
    check(
        "vote_refers_to_prior_debate", "debattert 20. juni 2024" in evidence["VOTE21"]["text"], True
    )
    for identifier in ("R2-date-p2", "R2-date-p8", "R2-date-p9", "R2-date-I91"):
        check(
            "retained_conflict_" + identifier, "20. juni 2024" in evidence[identifier]["text"], True
        )
    stages = read_json("stage-comparison.json")["rows"]
    for row in stages:
        check(
            "four_stage_wording_" + row["roman"],
            len({evidence[key]["text"] for key in row["evidence_ids"]}),
            1,
        )

    candidate = read_json("candidate-followup.json")
    old_candidates = json.loads(blob("docs/research/k3-arsinventar-50/case-candidates.json"))
    check(
        "historical_membership", any(n["metadata"]["id"] == "99235" for n in old_candidates), False
    )
    check("historical_occurrences", len(old_candidates), 67)
    check("selected_monetary_events", candidate["selected_monetary_events"], 5)
    check("selected_decision_fields", candidate["selected_decision_fields"], 11)
    check("global_gaps", candidate["global_gaps"], [f"R{n}" for n in range(1, 8)])
    journal = read_json("appendix-reading-journal.json")["pages"]
    check("appendix_journal_pages", len(journal), 130)
    check("journal_visual_pages", sum(n["visual_review"] for n in journal), 18)
    image_rows = read_json("appendix-image-inventory.json")["images"]
    for page in (69, 135):
        row = next(n for n in image_rows if n["pdf_page_1based"] == page)
        local_image = ROOT / ".local/c06-images" / row["derived_filename"]
        check(
            "visually_inspected_image_hash_" + str(page),
            hashlib.sha256(local_image.read_bytes()).hexdigest(),
            row["image_sha256"],
        )
    j02 = read_json("cross-reference-journal.json")["references"][1]
    stated_count = int(re.search(r"(\d+) nøkkelsider", j02["investigated_scope"]).group(1))
    result = {
        "schema": "c06-independent-spec-review-1",
        "checked_utc": datetime.now(UTC).isoformat(),
        "base": BASE,
        "candidate": CANDIDATE,
        "candidate_tree": git("rev-parse", CANDIDATE + "^{tree}").decode().strip(),
        "checks_passed": len(CHECKS),
        "checks": CHECKS,
        "finding": {
            "id": "SP1",
            "priority": "P3",
            "blocking": False,
            "journal_J02_stated_visual_pages": stated_count,
            "actual_journal_visual_pages": 18,
        },
        "manual_review": [
            "Read full #60 and #37 body; current #56/#58 handoffs via connector.",
            "Read proposition, recommendation, debate/voting and retrospective dates.",
            "Visually inspected PDF images 69/135: Riksantikvaren in both columns under KLD.",
            "Read helpers, ledgers, journal limits, compatibility records and issue-assessment.",
        ],
        "boundary": (
            "Spec review only; no new HTTP/source fetch, complete visual appendix review, "
            "full product suite, security attestation, CI, publication or merge."
        ),
    }
    (HERE / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        json.dumps(
            {"checks_passed": len(CHECKS), "findings": [result["finding"]]}, ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()
