"Rebuild source-bound C06 research evidence offline; never writes original sources."

import gzip
import hashlib
import json
import subprocess
from pathlib import Path

from lxml import etree, html

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[2]
BASE = "49cc6e44851cf74e0aaea4eb333419e5598bfd95"
NS = {"s": "http://data.stortinget.no"}
EVIDENCE = []
SOURCES = {}
CACHE = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(name, value):
    (PACK / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def normalize(node):
    return " ".join(" ".join(node.itertext()).split())


def source(key, xml=False):
    if (key, xml) not in CACHE:
        data = (ROOT / SOURCES[key]).read_bytes()
        raw = gzip.decompress(data) if SOURCES[key].endswith(".gz") else data
        node = (
            etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
            if xml
            else html.fromstring(raw.decode("utf-8-sig"))
        )
        CACHE[key, xml] = (raw, node)
    return CACHE[key, xml]


def evidence(identifier, key, xpath, role, xml=False, inner=None):
    raw, tree = source(key, xml)
    found = tree.xpath(xpath, namespaces=NS if xml else {})
    if len(found) != 1:
        raise ValueError(f"ambiguous/missing evidence: {identifier} {len(found)} {xpath}")
    node = found[0]
    outer = tree.getroottree().getpath(node)
    if inner:
        node = html.fromstring(node.find(inner, NS).text)
    row = {
        "id": identifier,
        "source_key": key,
        "path": SOURCES[key],
        "source_sha256": digest(raw),
        "xpath": outer,
        "namespaces": NS if xml else {},
        "inner_html_field": inner,
        "text": normalize(node),
        "role": role,
        "text_representation": (
            "UTF-8 HTML/XML parse, descendant itertext joined, Unicode whitespace collapsed"
        ),
    }
    EVIDENCE.append(row)
    return row


def main():
    attempts = []
    for path in sorted((PACK / "originals").glob("*.meta.json")):
        data = path.read_bytes()
        meta = json.loads(data)
        row = dict(meta)
        row["hops"] = [dict(hop) for hop in meta["hops"]]
        row.update(
            metadata=path.relative_to(PACK).as_posix(),
            metadata_bytes=len(data),
            metadata_sha256=digest(data),
        )
        for hop in row["hops"]:
            if "archive" in hop:
                hop["archive"] = "originals/" + hop["archive"]
        attempts.append(row)
        if meta["state"] == "complete":
            SOURCES[meta["id"]] = (
                (PACK / "originals" / meta["hops"][-1]["archive"]).relative_to(ROOT).as_posix()
            )
    write("source-manifest.json", {"schema": "c06-transport-manifest-1", "sources": attempts})

    reused = {
        "K3-index": "docs/research/k3-arsinventar-50/originals/saker-2023-2024.xml.gz",
        "K3-decisions": "docs/research/k3-arsinventar-50/originals/ind-vedtak-2023-2024.xml.gz",
        "old-decisions": "docs/research/to-visninger-37/originals/aar/session-2023-2024.xml.gz",
        "R2-date-prop": "docs/research/r2-101000-54/originals/prop34-ch2.html.gz",
        "R2-date-inns": "docs/research/r2-101000-54/originals/inns91-all.html.gz",
        "R2-appendix4": "docs/research/r2-101000-54/originals/prop36-ch11.html.gz",
        "R2-method": "docs/research/k3-arsinventar-50/originals/prop36-ch5.html.gz",
    }
    SOURCES.update(reused)
    paths = set(reused.values())
    paths.add("docs/research/to-visninger-37/originals/aar/session-2023-2024.meta.json")
    # Old source manifests retain original times/URLs and failed transport status.
    for prefix in ("k3-arsinventar-50", "r2-101000-54", "to-visninger-37"):
        for name in ("source-manifest.json", "reused-sources.json"):
            candidate = f"docs/research/{prefix}/{name}"
            if (ROOT / candidate).exists():
                paths.add(candidate)
    for value in list(paths):
        if value.endswith(".gz"):
            meta = value[:-3] + ".meta.json"
            if (ROOT / meta).exists():
                paths.add(meta)
    files = []
    for path in sorted(paths):
        data = (ROOT / path).read_bytes()
        row = {
            "path": path,
            "bytes": len(data),
            "sha256": digest(data),
            "role": "reused_no_new_HTTP_observation",
        }
        if path.endswith(".gz"):
            raw = gzip.decompress(data)
            row.update(body_bytes=len(raw), body_sha256=digest(raw))
        files.append(row)
    write("reused-sources.json", {"schema": "c06-reused-sources-1", "files": files})

    evidence("IDX114", "K3-index", "/*/*[3]/*[114]", "index_identity_not_post_link", True)
    evidence("CASE", "case-99235-a2", "/*", "complete_case_metadata", True)
    evidence("CASE-chronology", "case-99235-a2", "//s:saksgang", "debate20_vote21", True)
    evidence(
        "VOTE-API", "votes-99235-a1", "//s:sak_votering", "23490_21_june_unanimous_sentinels", True
    )
    evidence(
        "VOTE-time",
        "votes-99235-a1",
        "//s:votering_tid",
        "source_local_timestamp_no_timezone_added",
        True,
    )
    evidence(
        "VOTE-decision-map",
        "decisions-23490-a1",
        "//s:voteringsvedtak_liste",
        "I_to_IV_to_853_856",
        True,
    )
    for number in range(1, 5):
        key = f"prop108-ch{number}-a1"
        # Main content nodes, not navigation or unrelated shell.
        if number in (1, 2):
            path = f"//*[@id='kap{number}']"
            if number == 1:
                path += "/parent::*"
        else:
            marker = "kap2-p9" if number == 3 else "kap2-p15"
            path = f"//*[@id='{marker}']/parent::*"
            if number == 4:
                path += "/parent::*"
        evidence(f"P108-ch{number}", key, path, "government_original_complete_chapter")
    for number in range(1, 9):
        evidence(
            f"P108-2-p{number}",
            "prop108-ch2-a1",
            f"//*[@id='kap2-p{number}']",
            "government_context",
        )
    for number in (15, 16, 17, 18):
        evidence(
            f"P108-proposal-{number - 14}",
            "prop108-ch4-a1",
            f"//*[@id='kap2-p{number}']",
            "government_proposal_not_appropriation",
        )
    for number in (1, 2):
        evidence(
            f"P108-app{number}-HTML",
            f"prop108-ch{number + 4}-appendix{number}-a1",
            f"//*[@id='ved{number}']",
            "appendix_image_catalogue_not_image_text",
        )
    for name in ("m1", "m2", "m3"):
        evidence(
            f"I442-{name}",
            "inns442-all-a1",
            f"//*[@id='{name}']",
            "committee_summary_comments_recommendation",
        )
    evidence(
        "DEBATE20",
        "debate-200624-sak15-a1",
        "//*[@data-strtngt-sak-sakid='99235']",
        "complete_case15_debate",
    )
    evidence(
        "DEBATE20-date", "debate-200624-sak15-a1", "//time[@datetime='20.06.2024']", "meeting_date"
    )
    evidence(
        "DEBATE20-vote-link",
        "debate-200624-sak15-a1",
        "//a[contains(.,'Votering, se fredag 21. juni')]",
        "explicit_following_day_vote_reference",
    )
    evidence(
        "VOTE21", "vote-ref210624-a1", "//*[@id='2024-06-20-15']", "complete_case15_voting_block"
    )
    evidence("VOTE21-date", "vote-ref210624-a1", "//time[@datetime='21.06.2024']", "meeting_date")
    evidence(
        "VOTE21-start",
        "vote-ref210624-a1",
        "//time[@datetime='2024-06-21T14:01:04']",
        "meeting_start_not_case_vote_time",
    )
    for roman, index in zip(("i", "ii", "iii", "iv"), range(1, 5), strict=True):
        evidence(
            f"I442-{roman}",
            "inns442-all-a1",
            f"//*[@id='m3']//*[@data-strtngt-romertallseksjon-romertall='{roman}']/p",
            "committee_recommendation",
        )
        evidence(
            f"F-{index}",
            "proposals-23490-a1",
            f"//s:voteringsforslag[{index}]",
            "proposal_40075780_40075783",
            True,
            "s:forslag_tekst",
        )
        evidence(
            f"VF-{index}",
            "proposals-23490-a1",
            f"//s:voteringsforslag[{index}]",
            "complete_proposal_metadata",
            True,
        )
        evidence(
            f"V21-{index}",
            "vote-ref210624-a1",
            f"//*[@id='2024-06-20-15']//*[contains(@class,'romertallseksjon')][{index}]/p[1]",
            "voted_recommendation",
        )

    comparisons = []
    for number, api_id in zip(range(853, 857), range(40033712, 40033716), strict=True):
        selector = f"//s:stortingsvedtak[s:id='{api_id}']"
        evidence(f"D{number}", "K3-decisions", selector, "complete_final_decision", True)
        evidence(
            f"D{number}-text",
            "K3-decisions",
            selector,
            "final_consent_not_post_amount",
            True,
            "s:stortingsvedtak_tekst",
        )
        evidence(
            f"D{number}-date",
            "K3-decisions",
            selector + "/s:stortingsvedtak_dato_tid",
            "21_june_source_date",
            True,
        )
        a = source("K3-decisions", True)[1].xpath(selector, namespaces=NS)[0]
        b = source("old-decisions", True)[1].xpath(selector, namespaces=NS)[0]
        left = etree.tostring(a, method="c14n", with_comments=False)
        right = etree.tostring(b, method="c14n", with_comments=False)
        comparisons.append(
            {
                "decision_number": number,
                "api_id": str(api_id),
                "case_id": "99235",
                "left_source": SOURCES["K3-decisions"],
                "right_source": SOURCES["old-decisions"],
                "left_body_sha256": digest(source("K3-decisions", True)[0]),
                "right_body_sha256": digest(source("old-decisions", True)[0]),
                "left_xpath": a.getroottree().getpath(a),
                "right_xpath": b.getroottree().getpath(b),
                "c14n_sha256_left": digest(left),
                "c14n_sha256_right": digest(right),
                "equal": left == right,
                "method": "lxml C14N complete objects, comments=False",
            }
        )
    for number in (2, 8, 9):
        evidence(
            f"R2-date-p{number}",
            "R2-date-prop",
            f"/html/body/main/div/div[3]/div[3]/div[2]/p[{number}]",
            "retrospective_20_june_statement",
        )
    evidence("R2-date-I91", "R2-date-inns", "//*[@id='m2_1']", "retrospective_20_june_statement")
    evidence(
        "R2-compensation-context",
        "R2-method",
        "//*[@id='kap5']/parent::*",
        "known_autumn_context_no_reopened_case",
    )
    for row in (292, 293, 294):
        evidence(
            f"R2-compensation-{row}",
            "R2-appendix4",
            f"//*[@id='ved4']//tbody/tr[{row}]",
            "old_independent_1429_1_estimate_not_C06_allocation",
        )
    write(
        "source-comparison.json",
        {"schema": "c06-canonical-decision-comparison-1", "decisions": comparisons},
    )

    images = json.loads((PACK / "appendix-image-inventory.json").read_text("utf-8"))["images"]
    visual = {
        11: (
            "Meetingbook-LO",
            (
                "Riksmeklarens møtebok, sak 2024-026 og 2024-027; LO STAT og YS"
                " STAT; staten v/ Digitaliserings- og forvaltningsdepartementet"
            ),
            "heading_and_parties",
        ),
        12: (
            "Response-LO",
            ("Svarfrist vart sett til 20. juni 2024. Meklinga vart avslutta kl. 08.20."),
            "meetingbook_last_paragraphs",
        ),
        13: (
            "Economy-LO",
            (
                "Berekna årslønsvekst 2023–2024 5,2 prosent; lønnsglidning 0,8 "
                "prosent; overheng 2,5 prosent; 75 prosent lokalt; 25 prosent "
                "sentralt; generelt tillegg 0,75 prosent; virkning 1. mai 2024."
            ),
            "protocol_Economy_paragraphs_manual_paraphrase",
        ),
        14: (
            "Scope-LO",
            (
                "Hovedtariffavtalen 1. mai 2024–30. april 2026; staten ved DFD "
                "og LO Stat; 1.1.2 omfang, 1.1.3 stillinger utenfor "
                "hovedtariffavtalen."
            ),
            "tariff_page1_sections_1.1.1_to_1.1.3_manual_paraphrase",
        ),
        16: (
            "Negotiation-LO",
            ("Forhandlingene skal for tariffperioden føres slik vedlegg 2 viser."),
            "tariff_page3_section_2.2_first_paragraph",
        ),
        50: (
            "False-1429-LO",
            "1429 Aspirant 357 000",
            "tariff_page37_plan90.910_Stillingskode_1429_not_budget_chapter",
        ),
        69: (
            "RA-LO",
            (
                "Klima- og miljødepartementet: Virksomhet Riksantikvaren → "
                "Forhandlingssted Riksantikvaren"
            ),
            "tariff_page56_internal_appendix2_KLD_block_both_columns_manual_transcription",
        ),
        77: (
            "Meetingbook-YS",
            (
                "Riksmeklarens møtebok, sak 2024-026 og 2024-027; LO STAT og YS"
                " STAT; staten v/ Digitaliserings- og forvaltningsdepartementet"
            ),
            "heading_and_parties",
        ),
        78: (
            "Response-YS",
            ("Svarfrist vart sett til 20. juni 2024. Meklinga vart avslutta kl. 08.20."),
            "meetingbook_last_paragraphs",
        ),
        79: (
            "Economy-YS",
            (
                "Berekna årslønsvekst 2023–2024 5,2 prosent; lønnsglidning 0,8 "
                "prosent; overheng 2,5 prosent; 75 prosent lokalt; 25 prosent "
                "sentralt; generelt tillegg 0,75 prosent; virkning 1. mai 2024."
            ),
            "protocol_Economy_paragraphs_manual_paraphrase",
        ),
        80: (
            "Scope-YS",
            (
                "Hovedtariffavtalen 1. mai 2024–30. april 2026; staten ved DFD "
                "og YS Stat; 1.1.2 omfang, 1.1.3 stillinger utenfor "
                "hovedtariffavtalen."
            ),
            "tariff_page1_sections_1.1.1_to_1.1.3_manual_paraphrase",
        ),
        82: (
            "Negotiation-YS",
            ("Forhandlingene skal for tariffperioden føres slik vedlegg 2 viser."),
            "tariff_page3_section_2.2_first_paragraph",
        ),
        116: (
            "False-1429-YS",
            "1429 Aspirant 357 000",
            "tariff_page37_plan90.910_Stillingskode_1429_not_budget_chapter",
        ),
        135: (
            "RA-YS",
            (
                "Klima- og miljødepartementet: Virksomhet Riksantikvaren → "
                "Forhandlingssted Riksantikvaren"
            ),
            "tariff_page56_internal_appendix2_KLD_block_both_columns_manual_transcription",
        ),
    }
    visual.update(
        {
            39: (
                "OU-LO",
                "§5.2: OU 0,24 % av lønnsmassen; trekk kr400 per arbeidstaker; "
                "resten arbeidsgiver. §5.3.1: 7 millioner til felles opplæring. "
                "Boliglån inntil2,3 millioner i §5.1 er en annen rolle.",
                "tariff_page26_sections5.1_5.2_5.3.1_manual_paraphrase",
            ),
            40: (
                "Competence-LO",
                "§5.3.2: 26 millioner til kompetanse; sentrale tiltak, søknadsbasert "
                "ordning og lederopplæring. DFØ behandler/innstiller søknader og "
                "utbetaler. §5.4: 4 millioner til omstilling. Ingen navngitt "
                "Riksantikvaren-tildeling i disse bestemmelsene.",
                "tariff_page27_sections5.3.2_5.3.3_5.4_manual_paraphrase",
            ),
            105: (
                "OU-YS",
                "§5.2: OU 0,24 % av lønnsmassen; trekk kr400 per arbeidstaker; "
                "resten arbeidsgiver. §5.3.1: 7 millioner til felles opplæring. "
                "Boliglån inntil2,3 millioner i §5.1 er en annen rolle.",
                "tariff_page26_sections5.1_5.2_5.3.1_manual_paraphrase",
            ),
            106: (
                "Competence-YS",
                "§5.3.2: 26 millioner til kompetanse; sentrale tiltak, søknadsbasert "
                "ordning og lederopplæring. DFØ behandler/innstiller søknader og "
                "utbetaler. §5.4: 4 millioner til omstilling. Ingen navngitt "
                "Riksantikvaren-tildeling i disse bestemmelsene.",
                "tariff_page27_sections5.3.2_5.3.3_5.4_manual_paraphrase",
            ),
        }
    )
    pdf_path = SOURCES["prop108-full-pdf-a1"]
    raw_pdf = gzip.decompress((ROOT / pdf_path).read_bytes())
    for page, (identifier, text, locator) in visual.items():
        image = next(row for row in images if row["pdf_page_1based"] == page)
        EVIDENCE.append(
            {
                "id": identifier,
                "source_key": "prop108-full-pdf-a1",
                "path": pdf_path,
                "source_sha256": digest(raw_pdf),
                "pdf_page_1based": page,
                "appendix": image["appendix"],
                "figure_ordinal": image["figure_ordinal"],
                "image_index": image["image_index"],
                "image_sha256": image["image_sha256"],
                "visual_locator": locator,
                "text": text,
                "role": "visual_observation_or_explicit_manual_paraphrase",
                "text_representation": (
                    "Manually read original embedded JPEG. Not exact-text XPath or OCR equality."
                ),
            }
        )
    write("evidence.json", {"schema": "c06-evidence-1", "evidence": EVIDENCE})

    ocr = json.loads(gzip.decompress((PACK / "appendix-ocr.json.gz").read_bytes()))
    page_journal = []
    groups = [
        (1, 2, "Riksmeklerens møtebok; parter, møter, svarfrist og signatur"),
        (3, 3, "Protokoll: likelydende avtaler og økonomiske forutsetninger"),
        (4, 5, "Hovedtariffavtale: parter/omfang, stillinger og lokale parter"),
        (6, 11, ("Forhandlingssted, lønnspolitikk, lokal avsetning, regler og tvister")),
        (
            12,
            26,
            ("Fellesbestemmelser: lønn, ansiennitet, arbeidstid, tillegg, permisjon, erstatning"),
        ),
        (27, 28, "Pensjon og AFP, årskull, variable tillegg"),
        (
            29,
            34,
            (
                "Boliglån, OU, kompetanse, omstilling, senior/livsfase, "
                "innleie, likestilling, ferie, varighet og protokoll"
            ),
        ),
        (
            35,
            55,
            ("Internt vedlegg1: lønnsplaner, stillingskoder, minstelønn, stiger og godskriving"),
        ),
        (56, 62, "Internt vedlegg2: virksomheter og forhandlingssteder"),
        (63, 63, "Internt vedlegg3: omstilling under trygghet"),
        (64, 65, "Interne vedlegg4/5: pensjonsgivende variable tillegg"),
    ]
    for image in images:
        page = next(row for row in ocr["pages"] if row["image"] == image["derived_filename"])
        ordinal = image["figure_ordinal"]
        topic = next(label for first, last, label in groups if first <= ordinal <= last)
        page_journal.append(
            {
                "pdf_page_1based": image["pdf_page_1based"],
                "appendix": image["appendix"],
                "figure_ordinal": ordinal,
                "image_sha256": image["image_sha256"],
                "ocr_text_sha256": digest(page["text"].encode()),
                "ocr_chars": len(page["text"]),
                "section_context": topic,
                "visual_review": image["pdf_page_1based"] in visual,
                "reading_mode": (
                    "OCR-assisted page/section screening; visual reading only when "
                    "visual_review=true"
                ),
                "result_boundary": (
                    "Tariff-/organisasjonskontekst, ikke i seg selv postvis "
                    "bevilgning. Ingen generell fraværskonklusjon basert på OCR "
                    "eller ordtreff."
                ),
                "unresolved_remainder": (
                    "Feilfri full transkripsjon og øvrig detaljert "
                    "visuell/rettslig/personellmessig anvendelseskontroll er ikke "
                    "påstått."
                ),
            }
        )
    write(
        "appendix-reading-journal.json",
        {
            "schema": "c06-appendix-reading-journal-1",
            "ocr_archive": "appendix-ocr.json.gz",
            "ocr_representation": ocr["representation"],
            "pages": page_journal,
        },
    )

    by_id = {row["id"]: row for row in EVIDENCE}
    stages = []
    for i, roman in enumerate(("i", "ii", "iii", "iv"), 1):
        selected = [f"I442-{roman}", f"F-{i}", f"V21-{i}", f"D{852 + i}-text"]
        strings = [by_id[key]["text"] for key in selected]
        stages.append(
            {
                "roman": roman,
                "evidence_ids": selected,
                "committee_proposal_vote_decision_text_equal": len(set(strings)) == 1,
                "government_evidence_id": f"P108-proposal-{i}",
                "government_literal_equal": by_id[f"P108-proposal-{i}"]["text"] == strings[0],
            }
        )
    write(
        "stage-comparison.json",
        {
            "schema": "c06-stage-comparison-1",
            "rows": stages,
            "government_difference": (
                "I: tenestetvistlova vs tjenestetvistloven; III: later text "
                "adds the explicit Prop.108 citation. These are preserved "
                "wording differences; no monetary proposal is constructed."
            ),
        },
    )

    preserved = []
    listing = subprocess.check_output(["git", "ls-tree", "-r", "-z", BASE], cwd=ROOT)
    for entry in listing.split(b"\0"):
        if not entry:
            continue
        metadata, pathname = entry.split(b"\t", 1)
        path = pathname.decode("utf-8")
        if path in ("AGENTS.md", "docs/kildefunn.md"):
            continue
        blob = metadata.decode().split()[2]
        data = (ROOT / path).read_bytes()
        raw_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        cleaned = raw_blob
        if raw_blob != blob:
            cleaned = (
                subprocess.check_output(["git", "hash-object", "--path", path, path], cwd=ROOT)
                .decode()
                .strip()
            )
        if cleaned != blob:
            raise AssertionError(f"protected file changed: {path}")
        preserved.append(
            {
                "path": path,
                "checkout_bytes": len(data),
                "checkout_sha256": digest(data),
                "base_git_blob": blob,
                "raw_git_blob": raw_blob,
                "verified_git_blob": cleaned,
            }
        )
    write(
        "preserved-files.json",
        {
            "schema": "c06-preserved-files-1",
            "base_commit": BASE,
            "representation": (
                "checkout bytes bind this Windows capture; exact raw Git blob "
                "or Git clean-filter blob permits independent platform checks. "
                "Legacy CRLF CSV blobs can match only the raw representation. "
                "All base tracked files except the two allowed additive "
                "pointers are protected."
            ),
            "files": preserved,
        },
    )
    print(
        json.dumps(
            {
                "attempts": len(attempts),
                "evidence": len(EVIDENCE),
                "preserved_files": len(preserved),
                "stages": stages,
            }
        )
    )


if __name__ == "__main__":
    main()
