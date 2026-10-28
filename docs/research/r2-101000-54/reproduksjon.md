# Reproduksjon og kontrollgrense

Kjørt med Python 3.12.14, lxml 6.1.1 og pypdf 6.10.0 på Windows. Ingen
produktkode eller produktdatabase importeres. Kjør fra repoets rot med disse
avhengighetene. P1s lokale venv manglet lxml ved første forsøk; det forsøket
var ikke en bestått kontroll. De fullførte kontrollene brukte den bundlete
Python-kjøretiden. Ingen avhengighet ble installert eller oppgradert.

Alle kilde-/kontrollfiler i denne mappen har `-text` i den lokale
.gitattributes-filen. De hasher faktiske byte. Manifestets to pekerdokumenter
AGENTS.md og docs/kildefunn.md hasher uttrykkelig UTF-8/LF, tilsvarende
Git-blobben; Windows-checkout kan ha CRLF. Ingen råkilde normaliseres.

Kommandoen nedenfor leser manifestet, transportmetadata, alle nye og gjenbrukte
originalfiler, alle lokatorer og tekster, tabellceller, PDF-side-/teksthentingen,
kanonisk vedtakssammenligning, registerinvarianter, journalhenvisninger og
lokale lenkemål. Den sjekker også uendret produkt/K3/P1 mot basen.
Resultatet skrives til standard output; originaler og journaler overskrives ikke.

Kopier kodeblokken til en midlertidig fil utenfor den sporede leveransen, for
eksempel .local/r2-check.py, og kjør `python .local/r2-check.py`. For å kontrollere
faktiske Git-blobbyte etter commit, gi full kandidat-SHA som første argument:
`python .local/r2-check.py <full-kandidat-SHA>`. Dette forutsetter at alle
manifestførte filer er committet i den valgte revisjonen.

```python
"""Offline kontroll for dokumentert R2-reproduksjon; ingen produktimport eller nett."""

import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from lxml import etree, html
from pypdf import PdfReader

ROOT = Path.cwd()
BASE = ROOT / "docs/research/r2-101000-54"
BASE_COMMIT = "6b2441ee5e859d103ab44d78f12d33c374a89171"
counts = Counter()


def read_json(path):
    return json.loads(path.read_text("utf-8"))


def check(condition, name, detail=""):
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    counts[name] += 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def body(path):
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def parse_xml(data):
    return etree.fromstring(data, etree.XMLParser(resolve_entities=False, no_network=True))


for row in read_json(BASE / "reused-sources.json")["files"]:
    data = (ROOT / row["path"]).read_bytes()
    check(len(data) == row["bytes"] and digest(data) == row["sha256"], "reused_file", row["path"])
    if "body_sha256" in row:
        raw = gzip.decompress(data)
        check(len(raw) == row["body_bytes"] and digest(raw) == row["body_sha256"], "reused_body")

sources = read_json(BASE / "source-manifest.json")["sources"]
check(len(sources) == 22 and sum(r["http_complete"] for r in sources) == 21, "transport_attempt_count")
check(all(any(r["id"] == f"prop34-ch{i}.html" and r["http_complete"] for r in sources) for i in range(1, 6)), "all_five_proposal_chapters")
for row in sources:
    data = (BASE / row["archive"]).read_bytes()
    check(len(data) == row["archive_bytes"] and digest(data) == row["archive_sha256"], "source_archive", row["id"])
    raw = gzip.decompress(data)
    check(len(raw) == row["bytes"] and digest(raw) == row["sha256"], "source_body", row["id"])
    meta = (BASE / row["metadata"]).read_bytes()
    check(len(meta) == row["metadata_bytes"] and digest(meta) == row["metadata_sha256"], "source_metadata", row["id"])
    m = json.loads(meta)
    check(m["body_sha256"] == row["sha256"] and m["body_bytes"] == len(raw), "transport_body_binding")
    complete = m["curl_exit"] == 0 and m["transport"]["http_code"] == 200
    check(complete == row["http_complete"], "transport_status")
    if complete:
        check(m["transport"]["size_download"] == len(raw), "transport_size_download")
        if row["id"].endswith(".xml"):
            parse_xml(raw)
            counts["complete_xml"] += 1
        elif row["id"].endswith(".html"):
            check(raw.rstrip().lower().endswith(b"</html>"), "complete_html_end")
    else:
        check(row["id"] == "sak101000.xml" and m["curl_exit"] == 6 and len(raw) == 0, "preserved_dns_failure")

pdf_check = read_json(BASE / "pdf-check.json")
pdf_body = body(BASE / "originals/prop34.pdf.gz")
pdf = PdfReader(io.BytesIO(pdf_body))
check(len(pdf.pages) == pdf_check["page_count"] == 4, "pdf_page_count")
for index, page in enumerate(pdf.pages):
    text = page.extract_text()
    check(digest(text.encode("utf-8")) == pdf_check["pages"][index]["extracted_text_sha256"], "pdf_page_text_hash")

evidence = read_json(BASE / "evidence.json")
ns = evidence["namespaces"]
for row in evidence["evidence"]:
    raw = body(ROOT / evidence["sources"][row["source"]])
    check(digest(raw) == row["body_sha256"], "evidence_hash", row["id"])
    tree = parse_xml(raw) if row["kind"] == "xml" else html.fromstring(raw.decode("utf-8"))
    found = tree.xpath(row["xpath"], namespaces=ns)
    check(len(found) == 1, "evidence_xpath", row["id"])
    node = found[0]
    if "nested_html_field_xpath" in row:
        fields = node.xpath(row["nested_html_field_xpath"], namespaces=ns)
        check(len(fields) == 1, "nested_html_field", row["id"])
        node = html.fromstring(fields[0].text)
    text = " ".join("".join(node.itertext()).split())
    check(text == row["text"], "evidence_text", row["id"])
    if "rows" in row:
        cells = [[" ".join("".join(c.itertext()).split()) for c in tr.xpath("./td|./th")]
                 for tr in node.xpath("./thead/tr|./tbody/tr|./tr")]
        check(cells == row["rows"], "table_cells", row["id"])

comparison = read_json(BASE / "source-comparison.json")
parents = [parse_xml(body(ROOT / path)) for path in comparison["parents"]]
for row in comparison["decisions"]:
    xpath = "/s:stortingsvedtak_oversikt/s:stortingsvedtak_liste/s:stortingsvedtak[s:id=$id]"
    objects = [tree.xpath(xpath, namespaces=ns, id=row["decision_api_id"]) for tree in parents]
    check(all(len(found) == 1 for found in objects), "decision_unique")
    canonical = [etree.tostring(found[0], method="c14n") for found in objects]
    check(canonical[0] == canonical[1], "decision_canonical_equal")
    check(len(canonical[0]) == row["canonical_bytes"] and digest(canonical[0]) == row["canonical_sha256"], "decision_canonical_hash")

ids = {row["id"] for row in evidence["evidence"]}
check(len(ids) == len(evidence["evidence"]), "evidence_unique_ids")
for filename, key in [("treatment-ledger.json", "rows"), ("cross-reference-journal.json", "references")]:
    for row in read_json(BASE / filename)[key]:
        for id in row["evidence_ids"]:
            check(id in ids, "ledger_evidence_reference", id)

by_id = {r["id"]: r for r in evidence["evidence"]}
for id in ["R36", "R37"]:
    rows = by_id[id]["rows"]
    check(len(rows) == 4 and rows[1][0] == "1560" and rows[2][1] == "71", "whole_1560_71_table")
    check(rows[2][3].replace(" ", "") == "14200000", "proposal_delta")
    check("233100000" in rows[3][2].replace(" ", "") and "247300000" in rows[3][2].replace(" ", ""), "proposal_before_after")
check(by_id["R27"]["text"].startswith("1429") and by_id["R28"]["text"] == "1 Driftsutgifter 2 796 000" and by_id["R29"]["text"].startswith("1471"), "compensation_local_scope")
check("enstemmig_vedtatt" in by_id["R31"]["text"] and "23887" in by_id["R31"]["text"], "adopted_vote_23887")
check("enstemmig_vedtatt" in by_id["S-vot23945"]["text"] and "23945" in by_id["S-vot23945"]["text"], "adopted_vote_23945")
check("40077003" in by_id["R33"]["text"] and "40077004" in by_id["R33"]["text"], "two_named_proposals")
check("40078386" in by_id["R38"]["text"], "named_transfer_proposal")
ledger = read_json(BASE / "treatment-ledger.json")
by_row = {r["id"]: r for r in ledger["rows"]}
check(by_row["D230"]["budget_year"] == 2024 and by_row["D230"]["accounts"] == ["1560/71"] and by_row["D230"]["amounts"] == {"currency":"NOK", "before":233100000, "delta":14200000, "after":247300000}, "ledger_230_scope_and_amount")
check(by_row["FIN-1429-1"]["amounts"]["source_observed_compensation_estimate"] == int("".join(by_id["R28"]["text"].split()[-3:])), "ledger_compensation_value")
check(by_row["D231"]["amounts"] is None and by_row["FULLMAKT429"]["amounts"] is None, "non_monetary_roles")
check(by_row["O1-OMDISPONERING"]["amounts"]["derived_residual"] == 5796000 - 3000000, "derived_residual_separate")
check(ledger["conclusion"]["annual_coverage"] == "partial" and ledger["conclusion"]["professional_approval"] is False, "no_positive_annual_approval")

k3 = ROOT / "docs/research/k3-arsinventar-50"
candidates = read_json(k3 / "case-candidates.json")
check(len(candidates) == 67, "pinned_case_count")
check(len({row["metadata"]["id"] for row in candidates}) == 66, "pinned_unique_case_count")
check(sum(row["status"] == "open_title_candidate" for row in candidates) == 60, "pinned_open_case_count")
journal = read_json(k3 / "coverage-journal.json")
check(len(journal["decisions"]) == 25 and journal["open_without_dictionary_hits"] == 2158, "pinned_decision_count")
selected = [row for row in candidates if row["session"] == "2024-2025" and row["ordinal_1based"] == 624]
check(len(selected) == 1 and selected[0]["metadata"]["id"] == "101000", "candidate_identity")

allowed = {"AGENTS.md", "docs/kildefunn.md"}
changed = subprocess.check_output(["git", "diff", "--name-only", BASE_COMMIT], cwd=ROOT, text=True).splitlines()
check(all(p in allowed or p.startswith("docs/research/r2-101000-54/") for p in changed), "base_unchanged_outside_scope", repr(changed))
for p in ["docs/research/k3-arsinventar-50", "docs/research/perioderegister-52", "innlesning", "analyse", "drift", "tests", ".github", "docs/perioderegister.md"]:
    result = subprocess.run(["git", "diff", "--quiet", BASE_COMMIT, "--", p], cwd=ROOT, check=False)
    check(result.returncode == 0, "protected_tree_unchanged", p)

for p in BASE.rglob("*.json"):
    if "reviews" in p.relative_to(BASE).parts:
        continue
    read_json(p)
    counts["json_parsed"] += 1
for p in [*BASE.rglob("*.md"), ROOT / "AGENTS.md", ROOT / "docs/kildefunn.md"]:
    if p.is_relative_to(BASE) and "reviews" in p.relative_to(BASE).parts:
        continue
    for target in re.findall(r"\]\(([^)]+)\)", p.read_text("utf-8")):
        if target.startswith(("http:", "https:", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0].strip("<>")
        check((p.parent / path).exists(), "local_markdown_target", f"{p}: {target}")

if (BASE / "delivery-manifest.json").exists():
    manifest = read_json(BASE / "delivery-manifest.json")
    expected = {p.relative_to(ROOT).as_posix() for p in BASE.rglob("*") if p.is_file() and p.name != "delivery-manifest.json" and "reviews" not in p.relative_to(BASE).parts} | allowed
    check({r["path"] for r in manifest["files"]} == expected, "manifest_inventory")
    for row in manifest["files"]:
        data = (ROOT / row["path"]).read_bytes()
        if row["representation"] == "utf-8-lf":
            data.decode("utf-8")
            data = data.replace(b"\r\n", b"\n")
            check(b"\r" not in data and not data.startswith(b"\xef\xbb\xbf"), "manifest_text_representation")
        check(len(data) == row["bytes"] and digest(data) == row["sha256"], "manifest_file", row["path"])
        if len(sys.argv) > 1:
            git_blob = subprocess.check_output(["git", "show", f"{sys.argv[1]}:{row['path']}"], cwd=ROOT)
            check(git_blob == data, "manifest_git_blob", row["path"])

print(json.dumps({"schema":"r2-verification-1", "checked_utc": datetime.now(UTC).isoformat(), "base_commit":BASE_COMMIT, "runtime":sys.version, "checks":dict(counts), "total_checks":sum(counts.values()), "failures":0, "git_revision":sys.argv[1] if len(sys.argv)>1 else None, "boundary":"Offline fil-/kildekontroll. Ingen produkttestsuite, ny HTTP, uavhengig kontroll, CI eller merge er utført av denne kommandoen."}, ensure_ascii=False, indent=2))
```

## Manifest og gjentatt kjøring

[verification.json](verification.json) er byggerens faktisk avsluttede
kontrollkjøring. [delivery-manifest.json](delivery-manifest.json) har alle
byggerfiler i denne mappen unntatt seg selv, pluss AGENTS og kildefunn.
`reviews/**` eies av uavhengig kontroll og er uttrykkelig utelatt fra
byggerens manifest. Orkestratoren kan inkludere ferdige kontrollrapporter
i et separat sluttmanifest. Manifestet har ingen hash av seg selv.

Etter en dokumentretting oppdateres berørte poster med SHA-256/byte etter
deres oppgitte representasjon. Manifestet regenereres etter lagring av
kontrollresultatet; kommandoen kjøres deretter igjen uten å endre dette
lagrede resultatet. Dermed unngås en selvsiterende hashsyklus. En ny
rapportrevisjon krever ny manifest-/Git-blobkontroll.

De nye HTTP-originalene ble hentet av en separat utforsker med avgrenset
GET/curl, deretter gzip-komprimert tapsfritt. Innhenterne og andre
engangshjelpere er bevart bare i ignorert .local/. Denne reproduksjonen
krever de publiserte kildearkivene, ikke tilgang til den lokale mappen,
nettet, tidligere arbeidsflater eller denne samtalen. Kilde-URL-er,
observasjonstider og originale metadata ligger i kildemanifestet/sidevognene.
En ny henting gir en ny HTTP-observasjon og kan ha nye byte; den erstatter
ikke de bevarte originalene.

Dette er fil-/kildekontroller, ikke en generell semantisk årsundersøkelse.
PDF-tekstuttrekk beviser ikke visuell layout; ingen slik kontroll påstås.
Uavhengig kildekontroll, full Linux-CI og faktisk merge rapporteres av
orkestratoren separat. Ingen lokal full produkttestsuite er gjentatt av
byggeren for denne dokument-/kildedatakandidaten.
