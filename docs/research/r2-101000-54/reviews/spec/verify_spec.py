"""Målrettet Spec-etterkontroll av fast #54-kandidat; bare offline og egen output."""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from lxml import etree, html

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
PACK = ROOT / "docs/research/r2-101000-54"
BASE = "6b2441ee5e859d103ab44d78f12d33c374a89171"
CANDIDATE = "7af3153bda95726ac93d0780b918ae95440bae2d"
FIRST = "c61dcc7c9221aa485a764c954323e0aac25b9e82"
NS = {"s": "http://data.stortinget.no"}
OUT = {
    "schema": "r2-spec-independent-check-1",
    "base": BASE,
    "candidate": CANDIDATE,
    "checked_utc": datetime.now(UTC).isoformat(),
    "checks": [],
    "inventory": [],
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def check(name, condition, detail=None):
    OUT["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError((name, detail))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def readj(path):
    return json.loads(path.read_text("utf-8"))


def raw(path):
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def hd(name):
    return html.fromstring(raw(PACK / "originals" / (name + ".gz")).decode("utf-8"))


def xd(path):
    return etree.fromstring(raw(path), etree.XMLParser(resolve_entities=False, no_network=True))


def norm(node):
    return " ".join("".join(node.itertext()).split())


def main():
    check("fixed HEAD", git("rev-parse", "HEAD").decode().strip() == CANDIDATE)
    check("fixed merge base", git("merge-base", BASE, CANDIDATE).decode().strip() == BASE)
    names = git("diff", "--name-only", BASE + "..." + CANDIDATE).decode().splitlines()
    check("complete candidate has 64 files", len(names) == 64)
    check(
        "only research and durable pointers changed",
        all(
            n in {"AGENTS.md", "docs/kildefunn.md"} or n.startswith("docs/research/r2-101000-54/")
            for n in names
        ),
    )
    for name in names:
        blob = git("show", CANDIDATE + ":" + name)
        current = (ROOT / name).read_bytes()
        compared = (
            current.replace(b"\r\n", b"\n")
            if name in {"AGENTS.md", "docs/kildefunn.md"}
            else current
        )
        check("candidate file binding: " + name, compared == blob)
        record = {"path": name, "bytes": len(blob), "sha256": sha(blob)}
        if name.endswith(".json"):
            value = json.loads(blob)
            record["json_type"] = type(value).__name__
        elif name.endswith(".gz"):
            decoded = gzip.decompress(blob)
            record.update(body_bytes=len(decoded), body_sha256=sha(decoded))
        else:
            blob.decode("utf-8")
        OUT["inventory"].append(record)
    protected = [
        "docs/research/k3-arsinventar-50",
        "docs/research/perioderegister-52",
        "innlesning",
        "analyse",
        "drift",
        "tests",
        ".github",
        "docs/perioderegister.md",
    ]
    for path in protected:
        check(
            "protected tree: " + path,
            git("diff", "--name-only", BASE, CANDIDATE, "--", path) == b"",
        )

    for source in readj(PACK / "source-manifest.json")["sources"]:
        meta = readj(PACK / source["metadata"])
        check(
            "transport observation fields: " + source["id"],
            all(
                source[key] == meta[key]
                for key in ["id", "requested_url", "started_utc", "completed_utc"]
            )
            and source["curl_exit"] == meta["curl_exit"]
            and source["final_url"] == meta["transport"]["url_effective"],
        )

    annex = hd("prop36-ch11.html")
    heading = norm(annex.get_element_by_id("ved4").find("h1"))
    expected_heading = "4 Endring av utgifter som følge av lønnsoppgjøret for statsansatte"
    check("F1 original heading", heading == expected_heading)
    readme = (PACK / "README.md").read_text("utf-8")
    ledger = readj(PACK / "treatment-ledger.json")
    rows = {r["id"]: r for r in ledger["rows"]}
    check("F1 corrected README", expected_heading in readme)
    check("F1 corrected FIN-1429-1 ledger", expected_heading in rows["FIN-1429-1"]["finding"])
    for name in ["README.md", "treatment-ledger.json"]:
        old = git("show", FIRST + ":docs/research/r2-101000-54/" + name).decode("utf-8")
        check(
            "F1 old source label preserved as historical: " + name,
            "Lønnskompensasjon 2024" in old and expected_heading not in old,
        )
    original_names = [n for n in names if "/originals/" in n]
    for name in original_names:
        check(
            "F1 unchanged original: " + name,
            git("show", FIRST + ":" + name) == git("show", CANDIDATE + ":" + name),
        )
    table = annex.xpath("//main//table")[0]
    table_rows = [[norm(c) for c in r.xpath("./td|./th")] for r in table.xpath("./tbody/tr")]
    check(
        "independent local compensation scope and value",
        len(table_rows) == 373
        and table_rows[291:294]
        == [
            ["1429", "", "Riksantikvaren:", ""],
            ["", "1", "Driftsutgifter", "2 796 000"],
            ["1471", "", "Norsk Polarinstitutt:", ""],
        ],
    )
    check("compensation unit", norm(table.xpath("./thead")[0]) == "Kap. Post Formål Kroner")
    raw_cell = table.xpath("./tbody/tr[293]/td[4]")[0]
    check(
        "raw compensation cell with only edge whitespace stripped",
        "".join(raw_cell.itertext()).strip() == "2\u00a0796 000",
    )
    check(
        "salary estimate stays proposal",
        rows["FIN-1429-1"]["budget_year"] == 2024
        and rows["FIN-1429-1"]["accounts"] == ["1429/1"]
        and rows["FIN-1429-1"]["amounts"]["adopted_new_event"] is None,
    )
    check(
        "separate residual",
        rows["O1-OMDISPONERING"]["amounts"]["derived_residual"] == 5796000 - 3000000
        and rows["O1-OMDISPONERING"]["amounts"]["rounded_source_salary_million"] == 2.8,
    )
    check(
        "fullmakt no invented actual amount",
        rows["FULLMAKT429"]["amounts"] is None
        and rows["FULLMAKT429"]["transfer_target_year"] == 2025
        and ledger["conclusion"]["decision429_actual_Riksantikvaren_transfer"] == "unknown",
    )
    check(
        "no global positive annual acceptance",
        ledger["conclusion"]["annual_coverage"] == "partial"
        and ledger["conclusion"]["professional_approval"] is False
        and ledger["conclusion"]["product_monetary_events_unchanged"] == 5
        and ledger["conclusion"]["product_decision_fields_unchanged"] == 11,
    )
    toc = hd("prop34-ch1.html")
    chapter_links = {
        a.get("href", "").split("?ch=", 1)[1].split("#")[0].split("&")[0]
        for a in toc.iter("a")
        if "?ch=" in a.get("href", "")
    }
    check(
        "complete published Prop34 chapter set",
        chapter_links == {"1", "2", "3", "4", "5"},
        sorted(chapter_links),
    )
    debate = next(
        n for n in hd("ref171224-debatt6.html").iter("div") if n.get("class") == "strtngt_sak"
    )
    check(
        "complete debate closing boundary",
        "Flere har ikke bedt om ordet til sak nr. 6." in norm(debate),
    )

    # Re-evaluate every independently published source-control passage against its raw body.
    source_control = readj(PACK / "reviews/source-control/results.json")
    source_paths = {s["id"]: ROOT / s["archive_path"] for s in source_control["source_bindings"]}
    source_paths.update(
        {
            s["id"]: ROOT / "docs/research/omtale-o1/originals" / s["id"]
            for s in source_control["context_source_bindings"]
        }
    )
    for passage in source_control["passages"]:
        data = raw(source_paths[passage["source"]])
        doc = (
            xd(source_paths[passage["source"]])
            if passage["namespaces"]
            else html.fromstring(data.decode("utf-8"))
        )
        nodes = doc.xpath(passage["selector"], namespaces=passage["namespaces"])
        check(
            "source-control passage re-read: " + passage["label"],
            len(nodes) == 1
            and sha(data) == passage["body_sha256"]
            and " ".join(" ".join(nodes[0].itertext()).split()) == passage["normalized_text"],
        )
    check(
        "source-control 204 historical checks",
        len(source_control["checks"]) == 204 and all(r["passed"] for r in source_control["checks"]),
    )
    check(
        "source-control script binding",
        source_control["script_sha256"]
        == sha((PACK / "reviews/source-control/verify_sources.py").read_bytes()),
    )
    comparison = readj(PACK / "reviews/source-control/candidate-comparison.json")
    check(
        "source-control comparison is explicitly historical",
        comparison["candidate_revision"] == FIRST,
    )
    for row in comparison["compared_candidate_files"]:
        check(
            "historical candidate comparison: " + row["path"],
            sha(git("show", FIRST + ":" + row["path"])) == row["commit_sha256"]
            and row["same_bytes"],
        )
    for row in comparison["raw_copy_parity"]:
        check(
            "candidate original parity retained: " + row["candidate_path"],
            sha((ROOT / row["candidate_path"]).read_bytes()) == row["sha256"]
            and row["byteidentical"],
        )

    journal = readj(PACK / "cross-reference-journal.json")["references"]
    evidence_ids = {r["id"] for r in readj(PACK / "evidence.json")["evidence"]}
    check(
        "12 named cross-reference boundaries",
        [r["id"] for r in journal] == [f"C{i:02}" for i in range(1, 13)],
    )
    check(
        "cross-reference provenance and explicit results",
        all(
            r["status"] and r["result"] and set(r["evidence_ids"]).issubset(evidence_ids)
            for r in journal
        ),
    )
    live = readj(HERE / "live-context-comparison.json")
    check(
        "complete live issue and comment context",
        all(
            r["body_matches_live"] and r["comments_match_live"] and r["title_matches_live"]
            for r in live["results"]
        ),
    )
    builder_replay = readj(HERE / "builder-replay.json")
    check(
        "published builder reproduction on fixed blobs",
        builder_replay["git_revision"] == CANDIDATE
        and builder_replay["total_checks"] == 818
        and builder_replay["failures"] == 0,
    )
    source_replay = readj(HERE / "source-replay.json")
    check(
        "source script rerun on corrected fixed candidate",
        source_replay["head_at_control"] == CANDIDATE
        and source_replay["summary"]["checks_passed"] == 204
        and all(r["passed"] for r in source_replay["checks"]),
    )
    OUT["F1_recheck"] = {
        "heading_xpath": "//*[@id='ved4']/h1",
        "observed_heading": heading,
        "cell_xpath": raw_cell.getroottree().getpath(raw_cell),
        "observed_raw_cell": "".join(raw_cell.itertext()),
        "source_body_sha256": sha(raw(PACK / "originals/prop36-ch11.html.gz")),
        "status": "closed_on_7af3153",
    }
    OUT["summary"] = {
        "checks_passed": len(OUT["checks"]),
        "candidate_files": len(names),
        "necessary_findings": 0,
        "optional_findings": 0,
        "boundaries": [
            "offline raw-source rereading, no new HTTP authenticity proof",
            "no product test suite, native Excel, visual PDF, CI, or merge performed",
            "actual 231/429 application, June date conflict, other R1-R7 remain unresolved",
        ],
    }
    (HERE / "independent-results.json").write_text(
        json.dumps(OUT, ensure_ascii=False, indent=2) + "\n", "utf-8"
    )
    print(json.dumps(OUT["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
