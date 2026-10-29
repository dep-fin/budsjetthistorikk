"""Uavhengig, avgrenset råkildekontroll for #54. Ingen nett- eller produktimport.

Kjør fra reporoten. --raw-root kan peke til byteidentisk publisert originalkatalog.
Skriver bare egne kontrollresultater ved siden av dette skriptet.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import lxml
import pypdf
from lxml import etree, html
from pypdf import PdfReader

NS = {"s": "http://data.stortinget.no"}
BASE = "6b2441ee5e859d103ab44d78f12d33c374a89171"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
K3 = ROOT / "docs/research/k3-arsinventar-50"
OUT: dict = {"base": BASE, "source_bindings": [], "passages": [], "checks": []}
BODIES: dict[str, bytes] = {}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(element) -> str:
    return " ".join(" ".join(element.itertext()).split())


def check(label: str, condition: bool, detail=None):
    OUT["checks"].append({"check": label, "passed": bool(condition), "detail": detail})
    assert condition, (label, detail)


def binding(meta_path: Path, archive_path: Path, expected=None):
    raw_meta = meta_path.read_bytes()
    meta = json.loads(raw_meta)
    archive = archive_path.read_bytes()
    body = gzip.decompress(archive)
    ident = meta["id"]
    archive_expected = meta.get("archive_sha256", meta.get("gzip_sha256"))
    check(ident + ": gzip", sha(archive) == archive_expected)
    check(ident + ": body", sha(body) == meta["body_sha256"])
    check(ident + ": bytes", len(body) == meta["body_bytes"])
    if expected:
        check(
            ident + ": reused binding",
            all(
                [
                    sha(raw_meta) == expected["metadata_sha256"],
                    sha(archive) == expected["archive_sha256"],
                    sha(body) == expected["body_sha256"],
                ]
            ),
        )
    transport = meta.get("transport", {})
    status = meta.get("http_code", transport.get("http_code", meta.get("status")))
    item = {
        "id": ident,
        "archive_path": str(archive_path.relative_to(ROOT)).replace("\\", "/"),
        "metadata_path": str(meta_path.relative_to(ROOT)).replace("\\", "/"),
        "archive_sha256": sha(archive),
        "archive_bytes": len(archive),
        "metadata_sha256": sha(raw_meta),
        "metadata_bytes": len(raw_meta),
        "body_sha256": sha(body),
        "body_bytes": len(body),
        "requested_url": meta.get("requested_url", meta.get("url")),
        "final_url": meta.get(
            "url_effective", meta.get("final_url", transport.get("url_effective"))
        ),
        "started_utc": meta.get("started_utc", meta.get("retrieved_utc")),
        "completed_utc": meta.get("completed_utc"),
        "http_status": status,
        "curl_exit": meta.get("curl_exit"),
        "representation": meta.get("representation"),
        "used_as_document": status == 200 and len(body) > 0,
    }
    OUT["source_bindings"].append(item)
    BODIES[ident] = body


def hdoc(source: str):
    return html.fromstring(BODIES[source].decode("utf-8"))


def xdoc(source: str):
    return etree.fromstring(
        BODIES[source], parser=etree.XMLParser(resolve_entities=False, no_network=True)
    )


def passage(source: str, selector: str, *, xml=False, label=None):
    doc = xdoc(source) if xml else hdoc(source)
    nodes = doc.xpath(selector, namespaces=NS)
    check((label or source + selector) + ": unique", len(nodes) == 1, len(nodes))
    node = nodes[0]
    item = {
        "label": label or source + selector,
        "source": source,
        "body_sha256": sha(BODIES[source]),
        "selector": selector,
        "absolute_xpath": node.getroottree().getpath(node),
        "namespaces": NS if xml else {},
        "normalized_text": norm(node),
        "derived_serialized_fragment": etree.tostring(node, encoding="unicode", with_tail=False),
    }
    OUT["passages"].append(item)
    return node


def embedded(source: str, object_selector: str, field: str, label: str):
    node = passage(source, object_selector, xml=True, label=label)
    text = node.findtext("s:" + field, namespaces=NS)
    check(label + ": HTML field", bool(text))
    frag = html.fromstring(text)
    OUT["passages"][-1]["embedded_html_field"] = field
    OUT["passages"][-1]["embedded_html"] = text
    OUT["passages"][-1]["embedded_normalized_text"] = norm(frag)
    return frag


def rows(node):
    return [[norm(c) for c in r.xpath("./td|./th")] for r in node.xpath(".//tbody/tr")]


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--raw-root", type=Path, default=ROOT / ".local/r2-recon")
    args = args.parse_args()
    raw = args.raw_root.resolve()
    OUT["observed_at_utc"] = datetime.now(UTC).isoformat()
    OUT["runtime"] = {
        "python": platform.python_version(),
        "lxml": lxml.__version__,
        "pypdf": pypdf.__version__,
    }
    OUT["script_sha256"] = sha(Path(__file__).read_bytes())
    OUT["raw_root"] = str(raw)
    OUT["head_at_control"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    check(
        "research base is ancestor of current HEAD",
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT, check=False
        ).returncode
        == 0,
    )
    metas = sorted(raw.glob("*.meta.json"))
    check("22 acquired representations", len(metas) == 22, len(metas))
    for meta in metas:
        binding(meta, meta.with_name(meta.name.removesuffix(".meta.json") + ".gz"))
    reuse_path = K3 / "source-manifest.json"
    reuse_bytes = reuse_path.read_bytes()
    OUT["reused_k3_manifest_sha256"] = sha(reuse_bytes)
    reused_ids = [
        "ind-vedtak-2023-2024.xml",
        "ind-vedtak-2024-2025.xml",
        "prop36-ch5.html",
        "sak100289.xml",
        "saker-2024-2025.xml",
    ]
    for ident in reused_ids:
        item = [x for x in json.loads(reuse_bytes)["sources"] if x["id"] == ident][0]
        expected = {
            "archive_sha256": item["archive_sha256"],
            "metadata_sha256": item["metadata_sha256"],
            "body_sha256": item["sha256"],
        }
        binding(
            K3 / "originals" / (ident + ".meta.json"), K3 / "originals" / (ident + ".gz"), expected
        )
    check("failed DNS is not a document", BODIES["sak101000.xml"] == b"")

    # O1s gamle avrundede tekst kontrolleres på nytt i originalen. Denne nye
    # undersøkelsen erstatter ikke hva O1 faktisk hadde kildebelegg for.
    o1 = ROOT / "docs/research/omtale-o1"
    o1_manifest_bytes = (o1 / "source-manifest.json").read_bytes()
    OUT["o1_context_manifest_sha256"] = sha(o1_manifest_bytes)
    OUT["context_source_bindings"] = []
    for ident in ["prop16s-ch2.html", "prop16s-ch4.html"]:
        entry = [
            x
            for x in json.loads(o1_manifest_bytes)
            if x.get("status") == 200 and x["file"] == "originals/" + ident
        ][0]
        data = (o1 / entry["file"]).read_bytes()
        check(
            ident + ": original O1 hash",
            sha(data) == entry["sha256"] and len(data) == entry["bytes"],
        )
        check(
            ident + ": base bytes",
            data
            == subprocess.check_output(
                ["git", "show", BASE + ":docs/research/omtale-o1/" + entry["file"]], cwd=ROOT
            ),
        )
        BODIES[ident] = data
        OUT["context_source_bindings"].append(
            {
                "id": ident,
                "body_sha256": sha(data),
                "body_bytes": len(data),
                "original_transport": entry,
                "representation": "unchanged O1 HTML HTTP body; no new fetch",
            }
        )

    # Eksakte K3-byte og P1s katalog. Ingen selvhash eller import av produktet.
    pinned_paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE, "docs/research/k3-arsinventar-50"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    pinned_paths += ["innlesning/perioderegister_catalog.py"]
    pins = []
    for name in pinned_paths:
        old = subprocess.check_output(["git", "show", BASE + ":" + name], cwd=ROOT)
        actual = (ROOT / name).read_bytes()
        pins.append(
            {
                "path": name,
                "sha256": sha(actual),
                "base_sha256": sha(old),
                "unchanged": actual == old,
                "equal_after_checkout_crlf": actual.replace(b"\r\n", b"\n") == old,
            }
        )
    OUT["unchanged_pins"] = pins
    check("K3 exact bytes unchanged", all(x["unchanged"] for x in pins[:-1]), len(pins) - 1)
    check("P1 catalog unchanged except checkout CRLF", pins[-1]["equal_after_checkout_crlf"])

    # Indeksens identitet er sesjon + ordinal + råkildeversjon.
    index = xdoc("saker-2024-2025.xml")
    case_nodes = index.xpath("/s:saker_oversikt/s:saker_liste/s:sak", namespaces=NS)
    check("complete observed index length", len(case_nodes) == 727, len(case_nodes))
    candidate = passage(
        "saker-2024-2025.xml",
        "/s:saker_oversikt/s:saker_liste/s:sak[624]",
        xml=True,
        label="index-624",
    )
    check("candidate 624 is 101000", candidate.findtext("s:id", namespaces=NS) == "101000")
    passage(
        "sak101000-retry.xml",
        "/s:detaljert_sak/s:publikasjon_referanse_liste",
        xml=True,
        label="case101000-publications",
    )
    passage(
        "sak100289.xml",
        "/s:detaljert_sak/s:publikasjon_referanse_liste",
        xml=True,
        label="case100289-publications",
    )

    # Hele Prop.34s publiserte kapitler og hele tilrådingen.
    for source, ids in {
        "prop34-ch1.html": ["kap1"],
        "prop34-ch2.html": [
            "kap2",
            "kap2-1",
            "kap2-2",
            "kap2-1-p10",
            "kap2-1-p2",
            "kap2-1-p8",
            "kap2-1-p9",
        ],
        "prop34-ch3.html": ["kap3", "kap3_ch1", "kap3_ch1_ch1"],
        "prop34-ch4.html": ["ch5"],
        "prop34-ch5.html": ["ch6"],
        "inns91-all.html": ["m1", "m2", "m2_1", "m2_2", "m2_3", "m2_3_1", "m2_3_1_1", "m3"],
    }.items():
        for ident in ids:
            passage(source, "//*[@id='" + ident + "']", label=source + "#" + ident)
    prop = hdoc("prop34-ch5.html").xpath("//*[@id='ch6']")[0]
    committee = hdoc("inns91-all.html").xpath("//*[@id='m3']")[0]
    check(
        "Prop34 complete proposal has I/II", [norm(n) for n in prop.xpath(".//h2")] == ["I", "II"]
    )
    check(
        "Innst91 complete recommendation has I/II",
        [
            n.get("data-strtngt-romertallseksjon-romertall")
            for n in committee.xpath(".//*[@data-strtngt-romertallseksjon-romertall]")
        ]
        == ["i", "ii"],
    )
    check("Innst91 one monetary table", len(committee.xpath(".//table")) == 1)
    expected_rows = [
        ["1560", "", "Tariffavtalte avsetningar", ""],
        [
            "",
            "71",
            "Opplæring og utvikling av tillitsvalde, kan overførast , blir auka med",
            "14 200 000",
        ],
        ["", "", "frå kr 233 100 000 til kr 247 300 000", ""],
    ]
    check("all Prop34 monetary rows", rows(prop) == expected_rows, rows(prop))
    check("all Innst91 monetary rows", rows(committee) == expected_rows, rows(committee))
    check(
        "recommendation by whole committee despite separate remarks",
        "fremmes av en samlet komité" in norm(committee),
    )
    body91 = hdoc("inns91-all.html")
    OUT["inns91_main_sections"] = [
        (n.get("id"), norm(n.xpath("./h2|./h3|./h4")[0]) if n.xpath("./h2|./h3|./h4") else None)
        for n in body91.xpath("//*[@id='m1']/../div[@id]")
    ]
    OUT["inns91_default_sections"] = [
        n.get("id") for n in hdoc("inns91.html").xpath("//div[starts-with(@id,'m')]")
    ]

    # Hele sak-6-debatten og konkret voteringsblokk (ikke metadata alene).
    passage("ref171224-debatt6.html", "//div[@class='strtngt_sak']", label="complete-case6-debate")
    vote_ref = passage(
        "ref171224-votering.html", "//*[@id='2024-12-17-6']", label="case6-vote-reference"
    )
    check("plenary reproduces all I monetary rows", rows(vote_ref) == expected_rows)
    check("plenary unanimous", "samrøystes vedteken" in norm(vote_ref))
    votes = xdoc("voteringer101000.xml")
    check(
        "101000 has exactly one API vote in observed response",
        len(votes.xpath("s:sak_votering_liste/s:sak_votering", namespaces=NS)) == 1,
    )
    vote = passage(
        "voteringer101000.xml",
        "/s:sak_votering_oversikt/s:sak_votering_liste/s:sak_votering[s:votering_id='23887']",
        xml=True,
        label="vote23887",
    )
    check(
        "23887 unanimous, both romans",
        vote.findtext("s:votering_resultat_type", namespaces=NS) == "enstemmig_vedtatt"
        and vote.findtext("s:votering_tema", namespaces=NS) == "Romertallene I og II.",
    )
    check(
        "23887 sentinels remain -1",
        all(
            vote.findtext("s:" + key, namespaces=NS) == "-1"
            for key in ["antall_for", "antall_mot", "antall_ikke_tilstede"]
        ),
    )
    prop_api = xdoc("voteringsforslag23887.xml")
    check(
        "23887 exactly two proposals",
        len(prop_api.xpath("s:voteringsforslag_liste/s:voteringsforslag", namespaces=NS)) == 2,
    )
    decisions = xdoc("ind-vedtak-2024-2025.xml")
    selected = decisions.xpath(
        "s:stortingsvedtak_liste/s:stortingsvedtak[s:sak_id='101000']", namespaces=NS
    )
    check(
        "101000 exactly two final decisions",
        {n.findtext("s:id", namespaces=NS) for n in selected} == {"40034098", "40034099"},
    )
    roman_texts = []
    for proposal, decision, number, roman in [
        ("40077003", "40034098", "230", "i"),
        ("40077004", "40034099", "231", "ii"),
    ]:
        pp = embedded(
            "voteringsforslag23887.xml",
            "/s:voteringsforslag_oversikt/s:voteringsforslag_liste/s:voteringsforslag[s:forslag_id='"
            + proposal
            + "']",
            "forslag_tekst",
            "proposal" + proposal,
        )
        dd = embedded(
            "ind-vedtak-2024-2025.xml",
            "/s:stortingsvedtak_oversikt/s:stortingsvedtak_liste/s:stortingsvedtak[s:id='"
            + decision
            + "']",
            "stortingsvedtak_tekst",
            "decision" + number,
        )
        link = passage(
            "voteringsvedtak23887.xml",
            "/s:voteringsvedtak_oversikt/s:voteringsvedtak_liste/s:voteringsvedtak[s:vedtak_nummer='"
            + number
            + "']",
            xml=True,
            label="vote23887-decision" + number,
        )
        check(
            "23887 maps to " + number,
            roman.upper() + "." in link.findtext("s:vedtak_referanse", namespaces=NS),
        )
        check(proposal + " same final text", norm(pp) == norm(dd))
        rr = committee.xpath(".//*[@data-strtngt-romertallseksjon-romertall='" + roman + "']")[0]
        check(proposal + " same recommendation body", " ".join(norm(rr).split()[1:]) == norm(dd))
        if roman == "i":
            check("230 all monetary rows", rows(dd) == expected_rows)
        else:
            check(
                "231 is non-tabular general rule",
                not dd.xpath(".//table") and "flest årsverk i den einskilde verksemda" in norm(dd),
            )
        roman_texts.append(norm(dd))
        obj = decisions.xpath(
            "s:stortingsvedtak_liste/s:stortingsvedtak[s:id='" + decision + "']", namespaces=NS
        )[0]
        check(
            number + ": final identity and date",
            obj.findtext("s:stortingsvedtak_nummer", namespaces=NS) == number
            and obj.findtext("s:sak_id", namespaces=NS) == "101000"
            and obj.findtext("s:stortingsvedtak_dato_tid", namespaces=NS) == "2024-12-17T00:00:00",
        )
    prop_rule = norm(prop.xpath(".//*[@id='kap3-p11']")[0])
    check(
        "II textual inflection difference retained",
        prop_rule.replace("medlem av", "medlemer av") == roman_texts[1],
    )

    # Primærkildens eksakte anslag finnes i eget vedlegg, uavhengig av regnerest.
    annex_heading = passage("prop36-ch11.html", "//*[@id='ved4']/h1", label="annex4-actual-heading")
    check(
        "annex4 exact heading",
        norm(annex_heading) == "4 Endring av utgifter som følge av lønnsoppgjøret for statsansatte",
    )
    fin = passage("prop36-ch5.html", "//*[@id='kap5']", label="prop36-ch5-complete")
    check(
        "FIN says department proposals and annex4",
        "departementenes omgrupperingsproposisjoner" in norm(fin) and "vedlegg 4" in norm(fin),
    )
    annex = hdoc("prop36-ch11.html")
    table = annex.xpath("//main//table")[0]
    all_rows = table.xpath("./tbody/tr")
    check(
        "complete annex4 table",
        len(annex.xpath("//main//table")) == 1 and len(all_rows) == 373,
        len(all_rows),
    )
    check(
        "annex4 unit kroner",
        [norm(x) for x in table.xpath("./thead/tr")] == ["Kap. Post Formål Kroner"],
    )
    for ordinal in [292, 293, 294]:
        passage(
            "prop36-ch11.html",
            "/html/body/main/div/div[3]/div[3]/div/div/table/tbody/tr[" + str(ordinal) + "]",
            label="annex4-row" + str(ordinal),
        )
    check(
        "annex4 exact 1429 salary estimate",
        [[norm(c) for c in r.xpath("./td")] for r in all_rows[291:294]]
        == [
            ["1429", "", "Riksantikvaren:", ""],
            ["", "1", "Driftsutgifter", "2 796 000"],
            ["1471", "", "Norsk Polarinstitutt:", ""],
        ],
    )
    OUT["annex4_structure"] = {
        "rows": len(all_rows),
        "chapter1429_row": 292,
        "post1_row": 293,
        "next_chapter_row": 294,
        "next_chapter": "1471",
        "post22_in_this_block": False,
    }
    o1_salary = passage(
        "prop16s-ch2.html", "//*[@id='kap2-p24']", label="O1-unchanged-rounded-salary"
    )
    passage("prop16s-ch2.html", "//*[@id='kap2-p25']", label="O1-unchanged-post22")
    check(
        "O1 salary is rounded estimate",
        "2,8 mill. kroner" in norm(o1_salary) and "anslag" in norm(o1_salary),
    )
    for ordinal in range(43, 49):
        passage(
            "prop16s-ch4.html",
            "(//table)[1]/tbody/tr[" + str(ordinal) + "]",
            label="O1-proposal1429-row" + str(ordinal),
        )
    embedded(
        "ind-vedtak-2024-2025.xml",
        "/s:stortingsvedtak_oversikt/s:stortingsvedtak_liste/s:stortingsvedtak[s:id='40034048']",
        "stortingsvedtak_tekst",
        "existing-decision210",
    )
    passage("inns90-all.html", "//*[@id='m1_3_18_1_1']", label="central-reserve-summary2309-1")
    passage("inns90-all.html", "//*[@id='m1_5_1']", label="salary-summary-in-inns90")

    # Den smale fullmaktskjeden 36 -> 90 -> 429. Ingen faktisk postanvendelse.
    rec_actor = passage(
        "inns90-all.html",
        "//*[@id='m3']/div[@class='strtngt_komtilrading num_ja']/p[1]",
        label="inns90-recommendation-actor",
    )
    check(
        "Innst90 whole committee except 5800/50",
        norm(rec_actor)
        == (
            "Komiteens tilråding fremmes av en samlet komité, med unntak av kap. 5800 post 50, "
            "som fremmes av komiteens medlemmer fra Arbeiderpartiet, Senterpartiet og "
            "Sosialistisk Venstreparti."
        ),
    )
    fin_proposal = passage("prop36-ch7.html", "//*[@id='kap5-p15']/..", label="prop36-proposal-II")
    rec429 = passage(
        "inns90-all.html",
        "//*[@id='m3']//*[@data-strtngt-romertallseksjon-romertall='ii']",
        label="inns90-recommendation-II",
    )
    pp429 = embedded(
        "voteringsforslag23945.xml",
        "/s:voteringsforslag_oversikt/s:voteringsforslag_liste/s:voteringsforslag[s:forslag_id='40078386']",
        "forslag_tekst",
        "proposal40078386",
    )
    dd429 = embedded(
        "ind-vedtak-2024-2025.xml",
        "/s:stortingsvedtak_oversikt/s:stortingsvedtak_liste/s:stortingsvedtak[s:id='40034289']",
        "stortingsvedtak_tekst",
        "decision429",
    )
    v429 = passage(
        "voteringer100289.xml",
        "/s:sak_votering_oversikt/s:sak_votering_liste/s:sak_votering[s:votering_id='23945']",
        xml=True,
        label="vote23945",
    )
    passage(
        "voteringsvedtak23945.xml",
        "/s:voteringsvedtak_oversikt/s:voteringsvedtak_liste/s:voteringsvedtak[s:vedtak_nummer='429']",
        xml=True,
        label="vote23945-decision429",
    )
    check(
        "23945 unanimously adopts II/III/IV",
        v429.findtext("s:votering_resultat_type", namespaces=NS) == "enstemmig_vedtatt"
        and "romertallene II, III og IV" in v429.findtext("s:votering_tema", namespaces=NS),
    )
    check("429 identical proposal/final", norm(pp429) == norm(dd429))
    fullmakt = (
        "Stortinget samtykker i at Finansdepartementet kan øke maksimalgrensen for overføring "
        "av ubrukte driftsbevilgninger til 2025 tilsvarende kompensasjonen for lønnsoppgjøret "
        "2024, og fastsette en overføring som minimum tilsvarer kompensasjonen, slik at "
        "virksomhetene har dekning for etterbetaling som skyves til 2025."
    )
    for name, node in [("36", fin_proposal), ("90", rec429), ("40078386", pp429), ("429", dd429)]:
        check(
            name + ": exact full authorization passage",
            any(norm(p) == fullmakt for p in node.xpath(".//p")),
        )
    check("429 no monetary table", not dd429.xpath(".//table"))

    # Avgrenset kontroll av kildekonflikten; ingen full juniundersøkelse.
    june = []
    for ident, number in [
        ("40033712", "853"),
        ("40033713", "854"),
        ("40033714", "855"),
        ("40033715", "856"),
    ]:
        obj = passage(
            "ind-vedtak-2023-2024.xml",
            "/s:stortingsvedtak_oversikt/s:stortingsvedtak_liste/s:stortingsvedtak[s:id='"
            + ident
            + "']",
            xml=True,
            label="june-decision" + number,
        )
        june.append(
            {
                "id": ident,
                "number": number,
                "date": obj.findtext("s:stortingsvedtak_dato_tid", namespaces=NS),
                "case": obj.findtext("s:sak_id", namespaces=NS),
            }
        )
    check(
        "June API objects say 21 June, case99235",
        all(n["date"] == "2024-06-21T00:00:00" and n["case"] == "99235" for n in june),
    )
    OUT["june_date_conflict"] = {
        "api": june,
        "prop34_ch2": "20. juni 2024",
        "inns91_m2_1": "20. juni 2024",
        "status": "source_conflict_preserved; actual June proceedings outside this slice",
    }

    # Selvstendig uttrekk fra hele PDF-en, uten påstand om visuell kontroll.
    pdf = PdfReader(io.BytesIO(BODIES["prop34.pdf"]))
    check("Prop34 PDF four pages", len(pdf.pages) == 4)
    OUT["pdf_pages"] = [
        {
            "page_1based": i + 1,
            "text": page.extract_text(),
            "representation_sha256": sha(BODIES["prop34.pdf"]),
        }
        for i, page in enumerate(pdf.pages)
    ]
    OUT["summary"] = {
        "source_count": len(OUT["source_bindings"]),
        "context_source_count": len(OUT["context_source_bindings"]),
        "source_statuses": {
            str(status): sum(x["http_status"] == status for x in OUT["source_bindings"])
            for status in [0, 200]
        },
        "passage_count": len(OUT["passages"]),
        "checks_passed": len(OUT["checks"]),
        "product_adoption": False,
        "evidence_json_used": False,
        "builder_reports_used": False,
        "visual_pdf_check_claimed": False,
    }
    (HERE / "results.json").write_text(
        json.dumps(OUT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(OUT["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
