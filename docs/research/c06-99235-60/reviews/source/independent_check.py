"""Independent offline source checks. Does not import any C06 builder/verifier."""

import argparse
import datetime as dt
import gzip
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from lxml import etree, html
from pypdf import PdfReader

BASE = "49cc6e44851cf74e0aaea4eb333419e5598bfd95"
CANDIDATE = "9eb27cebf7ca4a99aeb30fa32245e41314e0d295"
ROOT = Path(__file__).resolve().parents[5]
PACKAGE = ROOT / "docs/research/c06-99235-60"
OUTPUT = Path(__file__).resolve().parent
NS = {"s": "http://data.stortinget.no"}
VISUAL = {11, 12, 13, 14, 16, 39, 40, 50, 69, 77, 78, 79, 80, 82, 105, 106, 116, 135}
result = {
    "schema": "c06-independent-source-check-1",
    "base": BASE,
    "candidate": CANDIDATE,
    "observed_utc": dt.datetime.now(dt.UTC).isoformat(),
    "checks": [],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(name, condition, detail=None):
    result["checks"].append({"name": name, "passed": bool(condition), "detail": detail})


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def raw(path):
    data = Path(path).read_bytes()
    return gzip.decompress(data) if str(path).endswith(".gz") else data


def norm(element):
    return " ".join(" ".join(element.itertext()).split())


def document(path):
    data = raw(path)
    if data.lstrip().startswith(b"<?xml"):
        return etree.fromstring(data, etree.XMLParser(resolve_entities=False, no_network=True))
    return html.fromstring(data.decode("utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def tree(revision):
    return {
        x.split(b"\t", 1)[1].decode("utf-8"): x.split()[2].decode("ascii")
        for x in git("ls-tree", "-rz", revision).split(b"\0")
        if x
    }


def source_url(url):
    p = urlsplit(url)
    return (
        p.scheme == "https"
        and p.hostname in {"data.stortinget.no", "www.stortinget.no", "www.regjeringen.no"}
        and p.port in {None, 443}
        and p.username is None
        and p.password is None
        and not p.fragment
        and not any(ord(c) <= 32 for c in url)
        and "\\" not in url
    )


def main(images=False):
    check("head_is_fixed_candidate", git("rev-parse", "HEAD").decode().strip() == CANDIDATE)
    left, right = tree(BASE), tree(CANDIDATE)
    changed = [p for p in left if left[p] != right.get(p)]
    added = sorted(set(right) - set(left))
    check(
        "only_two_base_files_changed",
        sorted(changed) == ["AGENTS.md", "docs/kildefunn.md"],
        changed,
    )
    check(
        "only_C06_files_added",
        all(p.startswith("docs/research/c06-99235-60/") for p in added),
        len(added),
    )
    check("existing_1070_git_blobs_unchanged", len(left) - len(changed) == 1070)
    preserved = read_json(PACKAGE / "preserved-files.json")["files"]
    check(
        "preservation_manifest_exhaustive",
        {p["path"] for p in preserved} == set(left) - set(changed),
    )
    for row in preserved:
        data = (ROOT / row["path"]).read_bytes()
        check(
            "preserved:" + row["path"],
            len(data) == row["checkout_bytes"]
            and sha(data) == row["checkout_sha256"]
            and left[row["path"]] == row["base_git_blob"],
        )

    delivery = read_json(PACKAGE / "delivery-manifest.json")
    for row in delivery["files"]:
        data = git("cat-file", "blob", right[row["path"]])
        check(
            "candidate_delivery:" + row["path"],
            len(data) == row["bytes"] and sha(data) == row["sha256"],
        )
    result["delivery_count"] = len(delivery["files"])

    transport = read_json(PACKAGE / "source-manifest.json")["sources"]
    responses = 0
    for source in transport:
        meta_bytes = (PACKAGE / source["metadata"]).read_bytes()
        check(
            "transport_metadata:" + source["id"],
            sha(meta_bytes) == source["metadata_sha256"]
            and len(meta_bytes) == source["metadata_bytes"],
        )
        meta = json.loads(meta_bytes)
        for hop in meta["hops"]:
            if "archive" in hop:
                hop["archive"] = "originals/" + hop["archive"]
        check(
            "metadata_manifest_equal:" + source["id"], all(source[k] == v for k, v in meta.items())
        )
        for i, hop in enumerate(source["hops"]):
            check("hop_url:" + source["id"] + str(i), source_url(hop["url"]))
            if "archive" not in hop:
                check(
                    "no_fabricated_response:" + source["id"],
                    hop["state"] == "transport_failed"
                    and not hop["body_complete"]
                    and "status" not in hop,
                )
                continue
            responses += 1
            archive = (PACKAGE / hop["archive"]).read_bytes()
            body = gzip.decompress(archive)
            check(
                "response_bytes:" + hop["archive"],
                len(archive) == hop["archive_bytes"]
                and sha(archive) == hop["archive_sha256"]
                and len(body) == hop["bytes"]
                and sha(body) == hop["sha256"]
                and hop["body_complete"],
            )
            headers = {k.lower(): v for k, v in hop["response_headers"]}
            check(
                "entity_representation:" + hop["archive"],
                headers.get("content-encoding", "identity") == "identity"
                and (
                    "content-length" not in headers or int(headers["content-length"]) == len(body)
                ),
            )
            if hop["status"] in (301, 302, 303, 307, 308):
                target = urljoin(hop["url"], headers["location"])
                check(
                    "redirect_binding:" + hop["archive"],
                    source_url(target)
                    and target == hop["redirect_target"]
                    and source["hops"][i + 1]["url"] == target,
                )
    result["transport"] = {
        "attempts": len(transport),
        "responses": responses,
        "successful_final_responses": sum(s["state"] == "complete" for s in transport),
    }
    for row in read_json(PACKAGE / "reused-sources.json")["files"]:
        data = (ROOT / row["path"]).read_bytes()
        check(
            "reused_archive:" + row["path"],
            len(data) == row["bytes"] and sha(data) == row["sha256"],
        )
        if "body_sha256" in row:
            body = gzip.decompress(data)
            check(
                "reused_entity:" + row["path"],
                len(body) == row["body_bytes"] and sha(body) == row["body_sha256"],
            )

    evidence = read_json(PACKAGE / "evidence.json")["evidence"]
    cache, strings = {}, {}
    for row in evidence:
        p = row["path"]
        check("evidence_source_hash:" + row["id"], sha(raw(ROOT / p)) == row["source_sha256"])
        if "pdf_page_1based" in row:
            continue
        if p not in cache:
            cache[p] = document(ROOT / p)
        located = cache[p].xpath(row["xpath"], namespaces=row.get("namespaces", {}))
        check("one_locator:" + row["id"], len(located) == 1)
        el = located[0]
        if row.get("inner_html_field"):
            el = html.fromstring(el.xpath(row["inner_html_field"], namespaces=NS)[0].text)
        text = norm(el)
        strings[row["id"]] = text
        check("exact_text:" + row["id"], text == row["text"])
    result["evidence"] = {
        "total": len(evidence),
        "machine_text": len(strings),
        "visual_requires_human_reading": len(evidence) - len(strings),
    }

    # Re-find process identities without using the supplied evidence XPaths.
    def cdoc(name):
        return document(PACKAGE / ("originals/" + name))

    case = cdoc("case-99235-a2.hop0.gz")
    events = {
        e.findtext("s:id", namespaces=NS): e.findtext("s:dato", namespaces=NS)
        for e in case.findall(".//s:saksgang_hendelse", NS)
    }
    check(
        "independent_case_dates",
        events["BEHS"] == "20.06.2024 00:00:00" and events["VOT"] == "21.06.2024 00:00:00",
        events,
    )
    vote = cdoc("votes-99235-a1.hop0.gz").find("s:sak_votering_liste/s:sak_votering", NS)
    fields = {etree.QName(x).localname: x.text for x in vote if len(x) == 0}
    check(
        "independent_vote_identity",
        fields["votering_id"] == "23490"
        and fields["sak_id"] == "99235"
        and fields["votering_tid"] == "2024-06-21T14:11:27.147"
        and fields["votering_resultat_type"] == "enstemmig_vedtatt",
        fields,
    )
    check(
        "sentinels_retained",
        all(fields[k] == "-1" for k in ["antall_for", "antall_mot", "antall_ikke_tilstede"]),
    )
    index = document(ROOT / "docs/research/k3-arsinventar-50/originals/saker-2023-2024.xml.gz")
    cases = index.findall("s:saker_liste/s:sak", NS)
    located = [
        (i + 1, x.findtext("s:innstilling_id", namespaces=NS))
        for i, x in enumerate(cases)
        if x.findtext("s:id", namespaces=NS) == "99235"
    ]
    check("independent_index_identity", located == [(114, "16526")], located)
    proposals = cdoc("proposals-23490-a1.hop0.gz").findall(
        "s:voteringsforslag_liste/s:voteringsforslag", NS
    )
    check(
        "four_proposals",
        [x.findtext("s:forslag_id", namespaces=NS) for x in proposals]
        == ["40075780", "40075781", "40075782", "40075783"],
    )
    old1 = document(ROOT / "docs/research/k3-arsinventar-50/originals/ind-vedtak-2023-2024.xml.gz")
    old2 = document(ROOT / "docs/research/to-visninger-37/originals/aar/session-2023-2024.xml.gz")
    comparisons = []
    for i in range(4):
        api = str(40033712 + i)
        path = './/s:stortingsvedtak[s:id="' + api + '"]'
        a, b = old1.find(path, NS), old2.find(path, NS)
        ca, cb = (etree.tostring(x, method="c14n", with_comments=False) for x in [a, b])
        vals = {etree.QName(x).localname: x.text for x in a if len(x) == 0}
        comparisons.append({"api": api, "object_c14n_sha256": sha(ca), "fields": vals})
        check("whole_decision_equal:" + api, ca == cb)
        check(
            "decision_identity:" + api,
            vals["stortingsvedtak_nummer"] == str(853 + i)
            and vals["sak_id"] == "99235"
            and vals["stortingsvedtak_dato_tid"] == "2024-06-21T00:00:00",
        )
        texts = [
            strings[k]
            for k in [
                "I442-" + ["i", "ii", "iii", "iv"][i],
                f"F-{i + 1}",
                f"V21-{i + 1}",
                f"D{853 + i}-text",
            ]
        ]
        check("independent_stage_comparison:" + api, len(set(texts)) == 1)
    result["decision_objects"] = comparisons
    government_equal = [
        strings[f"P108-proposal-{i + 1}"] == strings[f"F-{i + 1}"] for i in range(4)
    ]
    check(
        "government_wording_differences_retained",
        government_equal == [False, True, False, True],
        government_equal,
    )
    check(
        "retrospective_date_conflict_retained",
        all(
            "20. juni 2024" in strings[k]
            for k in ["R2-date-p2", "R2-date-p8", "R2-date-p9", "R2-date-I91"]
        ),
    )

    for appendix in [1, 2]:
        name = f"prop108-ch{appendix + 4}-appendix{appendix}-a1.hop0.gz"
        figures = cdoc(name).xpath("//figure")
        check(
            f"own_HTML_appendix_{appendix}_65_figures",
            len(figures) == 65
            and [norm(f) for f in figures] == [f"Figur {appendix}.{n}" for n in range(1, 66)],
        )

    pdf_raw = raw(PACKAGE / "originals/prop108-full-pdf-a1.hop0.gz")
    pdf = PdfReader(io.BytesIO(pdf_raw))
    inventory = read_json(PACKAGE / "appendix-image-inventory.json")
    journal = read_json(PACKAGE / "appendix-reading-journal.json")["pages"]
    ocr = json.loads(raw(PACKAGE / "appendix-ocr.json.gz"))
    by_image = {x["image"]: x for x in ocr["pages"]}
    actual = []
    screenings = []
    for page_no, page in enumerate(pdf.pages, 1):
        for ordinal, im in enumerate(page.images):
            item = {
                "pdf_page_1based": page_no,
                "image_index": ordinal,
                "image_name": im.name,
                "image_bytes": len(im.data),
                "image_sha256": sha(im.data),
                "derived_filename": f"page-{page_no:03d}-{ordinal}.jpg",
                "appendix": 1 if page_no <= 75 else 2,
                "figure_ordinal": page_no - (10 if page_no <= 75 else 76),
            }
            actual.append(item)
            ix = len(actual) - 1
            check("embedded_image:" + str(page_no), item == inventory["images"][ix])
            o = by_image[item["derived_filename"]]
            j = journal[ix]
            check(
                "ocr_journal_binding:" + str(page_no),
                j["image_sha256"] == item["image_sha256"]
                and sha(o["text"].encode("utf-8")) == j["ocr_text_sha256"]
                and len(o["text"]) == j["ocr_chars"]
                and j["visual_review"] == (page_no in VISUAL),
            )
            matches = list(
                re.finditer(
                    r"riksantikvar\w*|\b1429\b|l[øo]nnsmasse\w*|forholdsmess\w*|bevilg\w*|kapittel\w*",
                    o["text"],
                    re.I,
                )
            )
            screenings.append(
                {
                    "page": page_no,
                    "figure": item["figure_ordinal"],
                    "appendix": item["appendix"],
                    "chars": len(o["text"]),
                    "beginning": o["text"][:200],
                    "matches": [
                        o["text"][max(0, m.start() - 120) : m.end() + 180] for m in matches
                    ],
                    "journal_section": j["section_context"],
                }
            )
            if images and page_no in VISUAL:
                (OUTPUT / item["derived_filename"]).write_bytes(im.data)
    check("144_pdf_pages", len(pdf.pages) == 144 and inventory["pdf_pages"] == 144)
    check("130_images_130_ocr_130_journal", len(actual) == len(ocr["pages"]) == len(journal) == 130)
    check("65_images_each_appendix", Counter(x["appendix"] for x in actual) == {1: 65, 2: 65})
    check(
        "appendix_image_page_ranges",
        [x["pdf_page_1based"] for x in actual] == list(range(11, 76)) + list(range(77, 142)),
    )
    check(
        "18_visual_journal_pages",
        {x["pdf_page_1based"] for x in journal if x["visual_review"]} == VISUAL,
    )
    result["appendix_screening"] = screenings
    result["pdf"] = {
        "sha256": sha(pdf_raw),
        "pages": len(pdf.pages),
        "images": len(actual),
        "ocr_engine": ocr["engine"],
        "ocr_language": ocr["language"],
        "visual_pages": sorted(VISUAL),
    }

    candidates = read_json(ROOT / "docs/research/k3-arsinventar-50/case-candidates.json")
    opens = [x for x in candidates if x["status"].startswith("open")]
    totals = {
        "occurrences": len(candidates),
        "unique_cases": len({x["metadata"]["id"] for x in candidates}),
        "open_occurrences": len(opens),
        "open_unique_cases": len({x["metadata"]["id"] for x in opens}),
    }
    check(
        "historical_totals_unchanged",
        totals
        == {"occurrences": 67, "unique_cases": 66, "open_occurrences": 60, "open_unique_cases": 59},
        totals,
    )
    check(
        "99235_absent_historical_candidates",
        all(x["metadata"]["id"] != "99235" for x in candidates),
    )
    ledger = read_json(ROOT / "docs/research/k3-arsinventar-50/known-period-ledger.json")
    check(
        "five_events_eleven_fields_partial",
        ledger["monetary_event_count"] == 5
        and ledger["decision_amount_field_count"] == 11
        and ledger["year_coverage"] == "partial"
        and ledger["professional_annual_balance_approval"] is False,
    )
    result["historical_totals"] = totals
    reference = read_json(PACKAGE / "cross-reference-journal.json")["references"][1]
    claimed_visual = int(re.search(r"(\d+) nøkkelsider", reference["investigated_scope"])[1])
    result["nonblocking_findings"] = []
    if claimed_visual != len(VISUAL):
        result["nonblocking_findings"].append(
            {
                "priority": "P3",
                "path": "cross-reference-journal.json",
                "line": 34,
                "id": "J02",
                "claimed_visual_pages": claimed_visual,
                "journal_visual_pages": len(VISUAL),
                "finding": (
                    "J02 has an outdated visual-reading count; "
                    "the page journal and README document 18."
                ),
            }
        )
    result["script_sha256"] = sha(Path(__file__).read_bytes())
    result["failed"] = [x for x in result["checks"] if not x["passed"]]
    result["check_count"] = len(result["checks"])
    (OUTPUT / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                k: v
                for k, v in result.items()
                if k
                in [
                    "base",
                    "candidate",
                    "check_count",
                    "failed",
                    "transport",
                    "evidence",
                    "pdf",
                    "historical_totals",
                ]
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--images",
        action="store_true",
        help="Extract only the 18 visual review pages beside this script",
    )
    raise SystemExit(main(parser.parse_args().images))
