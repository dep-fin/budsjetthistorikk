# Standards: ikke bestått

Hele kandidaten `95ed8e60052d7731bb99386db572ba607c6b36a2`, tre
`225382d23bf776a8c9ee1a81a8d27de90e1b8620`, er vurdert mot base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b` med tredottdiff; 140 filer,
committene d46589c og 95ed8e6.

Standardgrunnlag: AGENTS, arbeidsflyt, issue-tracker, begrepsregler/GLOSSARY,
ansvarsdeling, ADR 0011, T1-/T5-kontrakter, observasjon-1/datakontrakt,
pyproject og .gitattributes. Ingen CONTRIBUTING/CODING_STANDARDS finnes.
Verktøyhåndhevet stil og avtalte separate formatmoduler gir ingen smellfunn.

**Dokumentert brudd: 1 P2 – råbytebindingene overlever ikke Git.**
`security-fix/manifest.json:132–136` og
`reviews/integration/manifest.json:27–31` krever `representation="raw bytes"`
med byteantall, SHA-256 og Git-blob-SHA-1. Likevel avviker **9/18** og
**40/54** bindinger fra kandidatens faktiske blobber. Alle 49 avvik er eksakt
CRLF→LF-konvertering. Eksempel: `security-fix/tests-38.log` er manifestført
med 732 byte, men Git inneholder 724 byte; faktisk SHA-256 er
`afff5668a5849af19705f193aca0e4144016232ff1289da15dc291c32c97e3d5`,
mot oppgitt `1c2331f61099931d34685206f969c3fc45820c8253efb6aabeffc8a403c84938`.
Ingen T5-attributt bevarer disse råbytene. Lokal Windows-kontroll passerer,
mens en LF-checkout/arkivert kandidat bryter bindingene. Påstanden om direkte
manifesttreff i `reviews/integration/README.md:32–34` kan derfor ikke overføres
til Git-kandidaten. Bevar de opprinnelige råartefaktene med eksplisitt
byteprofil og legg til ny kontrollbinding; historiske rapporter/manifester
skal beholde sitt tids-/stikart.

**Skjønn: 1 valgfri P3, mulig Duplicated Code.**
`analyse/proposisjon16.py:64–69` og `analyse/proposisjon16_excel.py:34–39`
gjentar `account.split("/")[0] in selection.chapters or
tuple(account.split("/")) in selection.accounts` og årsvilkåret. Et felles
kontopredikat kan hindre senere semantisk drift. Ingen aktuell atferdsfeil;
ikke et dokumentert regelbrudd.

**Egne kontroller:** Git-objekter/SHA-256/størrelser, AST/importgrense og
registrerte replayledgere, dokumentert i `.local/final-standards/results.json`.
1181/1183 baseblobber er uendret; bare additive AGENTS-/kildefunnpekere avviker.
Gamle produktfiler/kilder er urørt. Leveransemanifestets 35 bindinger består.
Alle fire hjelperoriginaler består; to AST-er er identiske, to har bare
importforskjeller. Registrerte normaliserte replayutfall er like.
Adapteren har ingen analyseimport. Temarettingen og tre regresjonsvarianter
er lest; 38-testloggen er separat byggebevis, ikke ny kjøring.

**Portstatus: IKKE BESTÅTT – ett P2, én valgfri P3.** Ingen ny fullsuite,
runtime-/visuell aksept, kilde-/Spec-/sikkerhetsattest, CI eller mergebekreftelse.
