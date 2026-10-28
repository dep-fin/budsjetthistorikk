# P1/#52: retting etter sikkerhetsaudit

28. oktober 2026. Dette er et tillegg til den opprinnelige kandidaten
`4413a5f21be71ccd2ad5c885560da6bae2e8b885`, tre
`afc1eacfa74cec19e35a5cb49ee5907be5bfc877`, mot base
`29ac220f62b35062fc4203f054e2f757ca795b7c`. Det opprinnelige
delivery-manifest.json, candidate-code.json og alle tidligere byggejournaler
beholdes ordrett. De dokumenterer den daværende koden og er ikke nye
kontrollresultater for denne rettingen. Eget candidate.json oppgir nøyaktig
hvilke kodehasher som erstattes, og binder dette tilleggets faktiske byte.

## Rettede funn

Grunnlaget er den avsluttede [uavhengige sikkerhetsauditten](../reviews/security/REPORT.md),
dens skript, resultater, manifest og faktiske prøvefiler under
`.local/p1-file-audit/`. Begge konkrete feilaksepter er gjentatt med riktige
SHA-256 og full rapportlikhet i before.json; nett og SQLite var sperret.

P2-1: P1s egen Excel-leser krever nå eksportprofilens lokale rotrelasjoner,
én officeDocument-relasjon til xl/workbook.xml, entydige ikke-tomme ID-er,
de forventede lokale workbook-relasjonene og tilhørende deklarerte
innholdstyper. Eksterne relasjoner, ekstra relasjonsfiler og motstridende
target/type/innholdsdeklarasjoner avvises. Hver tillatt .rels-fil har
uttrykkelig semantikk. Gamle lesere og omtale_excel_guard.py er uendret.

P2-2: Før innkommende celleobjekter lastes med openpyxl, avstemmes hele
rå styles.xml kanonisk mot stiltabellen til den rekonstruerte P1-boken.
Cellestiler registreres i skriverens ark-/cellerekkefølge; bare stiltabellen
serialiseres, ikke hele den store arbeidsboken. Dette bevarer kontroll av
applyAlignment og øvrige xf-flagg som går tapt ved normalisering. Profilen
gjelder den avtalte lukkede P1-eksporten, ikke vilkårlige redigerte Excel-bøker.
De eksisterende celle-/type-/format-/lenke-/synlighetskontrollene består.

## TDD og etterkontroll

Public-file-grensen er read_excel() på faktiske skrevne, lukkede filer.
red-root.log/xml og red-style.log/xml viser én forventet DID NOT RAISE-feil
hver før sin retting. green-root.log/xml og green-style.log/xml viser samme
enkeltprøver bestått etter rettingen. Ingen gamle auditlogger er overskrevet.

targeted.log/xml inneholder den avgrensede etterkontrollen: de to funnene,
ti relasjons-/innholdstypevarianter, åtte rå stilflaggvarianter, åtte tidligere
negative presentasjonsprøver, gammel ID-/regnekontroll, faktisk fullmaktspar
og offline offentlig CLI. probe.py after prøver de to uendrede auditfilene
igjen og gjenleser de fem eksisterende autentiske P1-parene begge poster,
fullmakt346, tomt valg, feil år og ukjent indekskandidat med nett/SQLite sperret.
after.json avstemmer også hasher til alle de gamle bygge-/reviewfilene mot
before.json. ruff.log, format.log og mypy.log er faktiske statiske kontroller.

Resultat: **31 bestått / 13 utelatt på 233,46 sekunder**, ingen feil eller
skips. Begge eksakte auditfiler gir nå ValueError. Alle fem eksisterende
JSON-/Excel-par er like etter gjenlesing; begge-poster beholder 11/5, de
fire øvrige 0/0 og alle fem 67/25/7. 90 gamle bevis-/validatorfiler er
hashidentiske før/etter. ID-/regneprøven beholder 166039000 og 29185000 med
status avgrenset kontroll og de samme gamle objektene. Ruff og format er
grønne; mypy kontrollerer 76 kildefiler uten feil. candidate.json binder
logger, testfiler og de to erstattede kodehashene. bind_candidate.py viser
hvordan bindingen og bevaringskontrollen er utført.

## Reproduksjon

Fra repoets rot, med requirements-dev.txt og den dokumenterte lokale
Python-runtime/avhengighetsmappen:

```powershell
$p1Python = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = '.;.local/python'
& $p1Python -m pytest tests/test_perioderegister.py `
  -k 'external_package or disabled_raw or package_relationships or raw_style or false_hidden or old_ids or authorization_reopens or frozen_input' `
  -vv --durations=10 --basetemp=.local/p1-audit-fix-targeted-new
& $p1Python -m ruff check .
& $p1Python -m ruff format --check .
& $p1Python -m mypy
```

probe.py nekter å overskrive before.json/after.json. Ny reproduksjon kjøres
fra en kopi av skriptet i en ny kontrollmappe med de eksisterende hashbundne
auditinputene. before-fasen krever den opprinnelige koden; after-fasen krever
rettingen og den kopierte before.json. Manifestets registrerte hasher skal
kontrolleres før resultatene brukes som nytt bevis.

## Bevisgrenser

Dette tillegget kjører målrettede filprøver og statiske kontroller. Det
regenererer ikke det samlede 2,6 GB-arkivet og kjører ikke fullsuite eller
Linux-CI. Den tidligere fullsuiten gjelder sin opprinnelige kandidat.
Ny uavhengig etterkontroll og full CI er orkestratorens etterfølgende porter.
Native Excel/rendering er ikke målt på nytt; eksportens innhold og visuelle
profil er uendret. Ingen nettutnyttelse eller kodekjøring påstås.

Ingen kilde, gammel ID, schema5/B5-standard, monetær tolkning, 67/25/7-
grunnlag eller fem hendelser/elleve vedtaksfelt endres. Ingen faglig
årsbalanse, kontinuitet eller helårsdekning innføres. Ingen commit, push,
PR, GitHub-mutasjon eller neste ticket inngår i rettingsarbeidet.
