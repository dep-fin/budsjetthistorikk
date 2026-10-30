# Avgrenset retting av T5s temabinding

29. oktober 2026. Utgangspunkt er kandidat
`d46589cb9e99338e44fc805ee9882006ba657fd0`, tre
`df0eed6d6e8a0b2a07962e641ae05d1194a3304d`, på base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b`.
Dette er byggerens lokale P2-retting. Orkestrator fryser ny kandidat og eier
nye uavhengige porter. De opprinnelige rapportene under `../reviews/` er
historiske bevis for den gamle kandidaten og er bevart byteidentisk.

## Årsak og retting

`Inventar!M:N` og `Kontoer!H` bruker standardfontens `theme=1`, samt
temaskrift via `scheme=minor`. `styles.xml` og celleobjektene bevarer disse
pekerne; de bestemmer ikke alene effektiv farge eller skrift. Endring av
bare temaets `dk1` til hvit kunne derfor skjule gjeldende T5-status og
feltbindinger, selv om kapsel, verdier, stiler og relasjoner var uendret.

`analyse/proposisjon16_excel.py::read_excel` sammenligner nå hele
`xl/theme/theme1.xml`, både størrelse og byte, med `openpyxl.writer.theme.theme_xml`
fra den eksisterende pinnede skriveren. Dette er formatets faste profil,
ikke en søking etter en bestemt hvit fargeliteral. Alle temafarger,
fontskjemaer og øvrig temainnhold omfattes. Alternative serialiseringer av
temaet avvises også; dette er en bevisst streng produkteksportprofil.

Først kjøres etablert beholder-/XML-kontroll og pakkprofilen. Sistnevnte
binder temadelen til den lokale temarelasjonen og forventet innholdstype.
Deretter kontrolleres temapayload, før rapportrekonstruksjon, rå stilprofil
og faktiske celler/oppsett/lenker. Ingen gammel guardmodul er endret.
Eksportskriveren og rå-/JSON-innholdet er uendret.

## Rødt og grønt

Implement- og TDD-filene i den lokale mattpocock-pakken 1.3.1 ble lest og fulgt
ved den allerede autoriserte offentlige `export_pair`/`read_excel`-grensen.
Mandatet legger slutt-review, commit og fullsuite hos orkestrator.

Den nye testen skrev og lukket en ekte T5-eksport, endret bare temadelen,
og kontrollerte at `inspect_excel` fortsatt returnerte nøyaktig samme gyldige
kapsel. Celleverdier/stilpekere og ufylt bakgrunn ble beholdt. Før
produktrettingen feilet forventet avvisning gjennom offentlig `read_excel`
med `DID NOT RAISE`: **1 feilet, 35 utelatt**, 55,86 sekunder ([red.log](red.log)).
Samme test etter rettingen bestod: **1 bestått, 35 utelatt**, 52,95 sekunder
([green.log](green.log)).

Deretter ble testen utvidet med to andre faktiske temagrenser:
systemfargen `window` med hvit fallback og temaskriftens `minorFont/latin`
endret til `Wingdings`. Alle variantene bevarer kapselen og alle andre
ZIP-medlemmer. [control-results.json](control-results.json) dokumenterer
tre avvisninger med T5s egen temafeil, ikke feil i transport eller kapsel.

## Positive filprøver og bevaring

Den målrettede kontrollhjelperen gjenleste alle **14 tidligere skrevne
JSON/XLSX-par** i `.local/delivery-final`, også begge innganger, retur,
utgift, inntekt/null, tekst, tomt, kontekst og 1429-utvalg. Hver Excel var
lik den offentlige JSON-leserens rapport, og den gamle typede T1-kapselen
var lik den autentiske fixturen. I tillegg ble én ny gyldig Excel skrevet,
lukket og gjenlest. Temaet i ny eksport var byteidentisk med det gamle;
`Forløp!G4` beholdt heltallsnull og celletypen `n`.

[preserved-before.json](preserved-before.json) binder 38 reviewfiler,
alle åtte representative PNG-er og den autentiske T1-fixturen før
produktrettingen. Hjelperen kontrollerte alle **47** byte-/hashbindingene
etterpå. Ingen bildebevis er erstattet eller rendret på nytt: skriveren
og de gyldige eksportenes presentasjon er uendret. Dette er bevaring av
tidligere visuell QA, ingen ny native Excel-aksept.

Bare ny T5-leser, ny T5-testfil og en kort T5-kontraktsforklaring er endret,
med deres tre tilhørende bindinger i leveransemanifestet. Tilleggets egne
bevis bindes i [manifest.json](manifest.json). Gamle T1/T2/T3/T4/P1/P2,
fixtures, kilder, schema 5/B5, standardvalg og CI-konfigurasjon er urørt.
Diff mot opprinnelig base har fremdeles bare de tidligere additive
AGENTS-/kildefunnpekerne som endrede basefiler.

## Kontroller og reproduksjon

Produkt-Ruff bestod for `analyse innlesning drift ops tests` og den nye
hjelperen; formatkontrollen bestod for 144 filer. Konfigurert `python -m mypy`
bestod for 85 kildefiler. Loggene ligger her.

Hele den nye T5-testfilen bestod: **38 tester på 172,24 sekunder**
([tests-38.log](tests-38.log)). De opprinnelige 35 testene er beholdt,
og de tre nye temavariantene er lagt til. Ingen gammel testfil eller
testutvelgelse er endret.

Hele `ruff check .` rapporterte **42 eksisterende feil** i fire reviewhjelpere:
`security/artifact_checks.py`, `security/probes.py`,
`security/verify_outcomes.py` og `standards/controls.py`. Hele
formatkontrollen ville formattert de samme fire filene; øvrige 173 var
allerede formatert. Disse historiske bevisfilene er ikke endret.
Orkestrator håndterer integrasjonen separat.

Fra en ny klon med tilgjengelig kandidat og pinnede avhengigheter kan
gyldige filpar først lages med den etablerte hjelperen. Bruk nye outputnavn:

```powershell
python -m ops.proposisjon16_proeve --root . --output .local/t5-fix-exports --base BASE --candidate KANDIDAT
python docs/research/proposisjon16-62/security-fix/probe.py --root . --candidate KANDIDAT --base BASE --exports .local/t5-fix-exports --output .local/t5-fix-replay --expect rejected
python -m pytest tests/test_proposisjon16.py -q --basetemp .local/t5-fix-tests
python -m ruff check analyse innlesning drift ops tests docs/research/proposisjon16-62/security-fix/probe.py
python -m ruff format --check analyse innlesning drift ops tests docs/research/proposisjon16-62/security-fix/probe.py
python -m mypy
```

Alle refs gis som argumenter. Kontrollhjelperen registrerer kandidat/base,
faktiske leser-/testhasher og eventuelle sporede arbeidsendringer; den
krever ingen hardkodet upublisert SHA. For historisk reproduksjon kan samme
hjelper kjøres mot den gamle checkouten og dens faktiske filpar, med
`--expect accepted`. I denne kjøringen er kandidatfeltet utgangspunktet,
mens leserhashen binder den lokale rettingen; det er ingen påstand om at
rettingen allerede inngår i denne committen.

Ingen primærkildehenting, gammel testendring, fullsuite, egen sikkerhetsattest,
ny uavhengig portgodkjenning, staging, commit, PR, full CI eller merge inngår.
