# Standards-review P1 / #52

Fast kandidat `4413a5f21be71ccd2ad5c885560da6bae2e8b885`, tre
`afc1eacfa74cec19e35a5cb49ee5907be5bfc877`, mot
`29ac220f62b35062fc4203f054e2f757ca795b7c`. HEAD og rent arbeidstre er
kontrollert; begge committer `407fdbc` og `4413a5f` inngår.

**Dokumenterte regelbrudd: ingen funnet.** Ansvarsgrensen er bevart:
innlesning importerer ikke analyse, mens utvalg, navigasjon, filgjenlesing og
Excel ligger i analyse, jf. `docs/ansvarsdeling.md:3–25`, ADR 0011 og
`docs/perioderegister.md:164–168`. Gamle filer endres ikke. Ny kontrakt,
kildekatalog, kildefunn, reproduksjon og byggebevis følger koden, jf.
`docs/arbeidsflyt.md:43,59–65`. AGENTS-pekeren har konkret utløser og to
relevante mål; writing-for-agents er lest. Ingen CONTRIBUTING.md eller
CODING_STANDARDS.md finnes i kandidaten. Verktøyhåndhevet stil er ikke
duplisert som reviewfunn.

**Baselineheuristikk, skjønn, lav prioritet:** Mulig *Primitive Obsession* i
`innlesning/perioderegister_catalog.py:5`: `CATALOG: dict[str, tuple[str, int,
str, int, str]]`. Én kildepinn består av fem posisjonsbestemte primitive
verdier, og arkivhash hentes med `CATALOG[name][0]` i
`innlesning/perioderegister.py:111,170`. En navngitt immutable katalogpost
ville skille arkivhash/-størrelse fra representasjonshash/-størrelse og
metadata. Dette er vedlikeholdsskjønn, ingen dokumentert regelbrist eller
observert funksjonsfeil; det er ikke en leveringsblokkering.

**Kontroller:** Hele kandidatens kode, tester, kontrakt og kontrollhjelpere
er lest. Egen skrivebeskyttet kontroll bekreftet åtte kjørbare filbindinger
(arbeidsbyte og Git-byte), alle 416 manifestfiler / 2 591 148 727 byte og
130 katalogkilder mot eksakte baseblobs samt gzip-representasjonene. Alle
endrede JSON-filer parses. JUnit/logg bekrefter 1 179 bestått, to skips,
24 P1-prøver; Ruff/format/mypy er grønne. Tre hashbundne bildeutsnitt er
inspisert, inkludert fullmaktens tomme beløpsfelt og tomt utvalgs 67/25/7.

Fullsuite er ikke kjørt på nytt. Linux-CI, native Excel og sikkerhetsaudit
inngår ikke i dette Standards-resultatet. Byggerjournalenes tidligere
HEAD/stage beskriver overleveringstidspunktet; egne filbindinger knytter
bevisene til den faste reviewkandidaten.

Egne bevis: `.local/p1-standards/evidence-audit.json`,
`verified-manifest-files.json`, `verified-source-catalog.json` og
`review-notes.md`; reproduksjon: `audit_evidence.py` i samme mappe.
