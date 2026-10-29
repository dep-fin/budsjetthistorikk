# Akseptledger for lokal P2-kandidat

Base er c041ad8. Før-kode-kontrakten er lokal 52ba019/publisert ed993868.
`candidate-code.json` binder de ti nye kjørbare kode-/kontrollfilene med
faktiske SHA-256. Fullsuitens opprinnelige binding er bevart separat i
`candidate-code-before-control-fix.json`; den ene senere hjelperrettingen
og dens prøver er avgrenset nedenfor. Ingen commit eller GitHub-mutasjon
er gjort av byggeren.

De målrettede portene dekker ny P2-filgrense, gamle P1/T4-regresjoner,
kilde-/rollekonstanter, navigasjon, strengt gjenleste celler og rehashede
negative filer. Full lokal suite kjører én gang med hele testutvalget.
Faktisk avsluttet resultat oppgis i checks/commands.json og nedenfor.

Lokal kontrollrot er `.local/p2-acceptance-52ba019`. Filene er faktiske nye
eksporter, lukket og gjenlest med samme typede grunnlag. Kontrollens
`progress.json` er en gjenopptaksjournal; bare endelig `verification.json`
regnes som fullført aksept. De store JSON-/Excel-/negative filene ligger
lokalt og bindes av det publiserbare filmanifestet i verification.json.

`compatibility-bindings.json` sammenholder ny P1-basis direkte med den
autentiske tidligere P1-filen, hele T4-basis med tidligere T4 og den
ordrette T1-kapselen med tidligere T1/den pinnede gzip-fixturen. Alle
gamle observasjoner og dokument-ID-er samsvarer. 527 eksisterende filer
under produkt/test/kilde/CI/avhengighetsgrensene er uendret mot c041ad8.

`guards.json` har 14 forventede avvisninger av syntetiske ZIP/XML-,
rot-/innholdstype-/råstil-, formel-, JSON- og ressursbrudd. Ingen ekstern
lenke eller formel ble aktivert. `rendering.json` binder 16 read-only
renderinger av begge-/tomt-valget og beskriver rendererens grenser.

Samlet Standards/Spec, separat sikkerhetsaudit, full Linux-CI og bekreftet
merge er etterfølgende porter hos orkestratoren. Disse hevdes ikke utført
av byggeren. Ingen positiv M21, årsbalanse, kontinuitet eller drift følger.

## Avsluttede resultater

Alle lokale prosesser er avsluttet med beståtte porter. Full suite ble
kjørt nøyaktig én gang: **1 224 bestått, to eksisterende Windows-skips,
0 feil, 2 924,14 sekunder**. Alle 1 226 tester ble samlet uten filter.
Skips gjelder gammel symbolsk databaselenke og historisk hardlink-prøve;
ingen ny skip eller CI-endring er innført. Ruff, format (147 filer) og
mypy (81 kildefiler) bestod. Python 3.12.14, lxml 6.1.3/libxml2 2.11.9,
openpyxl 3.1.5 og pytest 8.3.5 er faktisk brukt.

Før fullsuiten bestod 101 målrettede P2/P1/T4-tilfeller på 1 319,26 sekunder,
og fem nye permanente semantiske Excel-tilfeller bestod separat på 68,33
sekunder. Etter hjelperrettingen bestod alle 25 P2-tester igjen på 177,70
sekunder, samt Ruff/format/mypy. Loggene og kommandoenes exitkoder står i checks/.

- 46 nye valg-/navigasjons-/retur-/repetisjonspar er skrevet, lukket og
  gjenlest. /1 har 7/3, /22 har 4/2 og begge har 11/5 vedtaksfelt/hendelser.
  Nye dokumenter, feil år og tomt valg har 0/0. Alle relevante komplette
  utvalg beholder nøyaktig samme 67/25/7-ID-er, synlig R1–R7 og kandidatgrunner.
- Et eget offlinepar er skrevet og gjenlest i offentlig CLI fra tom mappe,
  med nett/SQLite sperret og ikke-eksisterende originalrot. 187 eksporterte
  rådigester og index er kontrollert mot kapslen.
- Alle 26 rehashede negative JSON-/Excel-par passerte containerporten med
  nøyaktig den forgiftede kapselen før begge offentlige lesere avviste
  semantikken. `hash-probe.json` kontrollerer dessuten deres faktiske nye
  og gamle selvhasher og ID-referanser. Åtte presentasjonsavvisninger og
  14 ytterligere ZIP/XML-/JSON-/ressursavvisninger er separate kontroller.
- 14 kompatibilitetsresultater omfatter ekte O2a/O2b-, B8/B9/B6-, T1-, T4-
  og P1-filer samt én gammel B6-bok. Originalene er hashkontrollert før/etter
  og gjenlest med gamle lesere. De gamle testene og den uendrede T4-/P1-basis
  er kontrollert separat fra disse filene.
- Fire **nye, separate** ordinære 368-databaser etter hjelperrettingen ga
  hver 222 observasjoner/74 hendelser, identisk B5-register, schema 5,
  gammel `round='uavklart'`, bevart råkilde og faktisk Excel-trio for 700/1:
  304 351 000 / 6 324 000 / 310 675 000. Ingen historisk Excel var inngangskrav.
- 69 kodepinnede kildefiler er kontrollert byteeksakt mot katalog og Git,
  med faktisk tekst/celler/XPath fra alle 74 belegg. Rapporten er
  26 835 258 byte, største nye payload 644 339 byte og største representasjon
  i R2-katalogen 7 479 943 byte. Alle nye tak består; P1s gamle større
  kildegrunnlag valideres under sine uendrede tak.

`archive-recheck.json` dokumenterer ny streaming-rehash av alle 401 faktisk
manifestførte kontrollfiler, 3 084 248 448 byte, og alle ti endelige kodefiler,
uten avvik. Store filer ligger lokalt; kontrolljournaler/hasher publiseres.

## Avgrenset retting av kontrollhjelper

Den første akseptkjøringen stoppet etter bestått offlinefase fordi
kontrollhjelperen brukte ikke-eksisterende AmountObservation-felt
`amount_meaning/normalized_kr`. Det første ordinære 368-forløpet hadde
allerede skrevet og gjenlest sin Excel. Feilen lå i hjelperens etterkontroll.
Riktige offentlige felt er `meaning/amount_kr`.

Fullsuiten ble fullført først med ti uendrede kodebindinger. Deretter ble
bare disse to attributtnavnene rettet i `independent_368`; alle øvrige
AST-noder og all produkt-/testkode er uendret. Fire friske databaser ble
kjørt i `retry-after-control-fix/`, og resten av aksepten ble gjenopptatt.
Det første forsøket er bevart og teller ikke som en av de fire nye prøvene.
`control-correction.json`, patch, opprinnelig feillogg, før-binding og
etterkontroller skiller disse kandidatene. Lokal fullsuite gjentas ikke for
denne rene hjelperrettingen; hele Linux-CI på endelig publisert kandidat
er fortsatt orkestratorens port.
