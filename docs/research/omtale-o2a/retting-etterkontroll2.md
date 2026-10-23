# O2a: andre retting av kildebinding og Excel-områder

Rettingen gjelder lokale endringer over `d45dee7d0aea26939ecea6a1187084d4448de3a8`, tree `28ed7c806237f63affd2252e35167ccffb3209bb`, på `codex/34-omtale-post1`, sammenligningsbase `d74d2cb`. Mandatet gjelder tre funn fra etterkontrollen. Tidligere rettingsbevis og alle tidligere leveransebyte er bevart. Dette er en byggerkontroll; samlet review, separat sikkerhetsaudit og endelig CI håndteres av orkestratoren. Den forrige separate sikkerhetskontrollen ble stoppet av verktøyets automatiske risikofilter og er ikke et bestått bevis.

## Rettet atferd

| Funn | Kontroll mot originalen | Faktisk filbevis |
| --- | --- | --- |
| P1: konsistent endret sesjon kunne gi seks kildeverifiserte relasjoner til en annen hendelsesgruppe | Sesjonen leses fra XML-konvolutten og den bevarte metadatafilen. Eksisterende `validate_source` og B1s `structure_node` rekonstruerer dokumentmetadata og artefaktidentitet. Hele vedtaksobjektets bevarte metadata sammenlignes; kildeenhet, inventar, kildeobservasjon, dokumentkontekst og valgt uttrekk må følge samme original/revisjon. Hendelsesgruppen beregnes fra originalens sesjon og ID. | Begge eksakte `forged-source-session-correct-locator`-filer avvises. Ny eksport fra det samme forfalskede B8-grunnlaget beholder råfeltene, viser `vedtaksbinding_motstrid` og grunnlagsavvik, og har **0 relasjoner** i faktisk gjenlest JSON og XLSX. |
| P2: `chapter_raw=1428` kunne skjules i både rader og uttrekk | Lokal kapittel-/postkontekst kontrollerer rå og kanonisk konto, navn, formål/handling, beløpstekst, års-/dokumentmetadata, enhet/valuta/faktor, full rad-HTML og lokator. Konsistens mellom oppdiktede snapshotfelt erstatter ikke originaltabellen. | Begge eksakte `forged-raw-account`-filer avvises. Ny eksport fra samme feilgrunnlag viser grunnlagsavvik og **0 relasjoner** i begge faktiske filer. Selvstendige prøver endrer også postens råkode, underpost, navn, formål, dato/sesjon, årsbelegg, tittel, enhet, valuta, faktor, dokumentreferanse og valgfri hendelses-ID. |
| P2: `hyperlink/@ref` kunne utløse stor celleallokering før kontroll | Bare én unik fysisk celle tillates som hyperlenkens `ref`; også et degenerert område som `A1:A1` avvises. Samme tidlige kontroll dekker øvrige tillatte områder og indekser i ark, arbeidsbok og stiltabell. Ukjente arkattributter, feil indeksreferanser og strukturer som eksporten ikke produserer, avvises. | Den bevarte `hyperlink-range.xlsx` avvises med **0 inputkall** til openpyxl. Målt lokal kontrolltid var 0,0052 s. Små XML-fixturer og en sentinel stanser før inputinnlasting. Ingen storallokering eller ressursbelastning er gjennomført. |

De fire nye feilfilene og seks tidligere reviewangrep er faktisk forsøkt gjenlest og avvist. De to nye, uttrykkelig merkede feilparene ligger i `work/omtale-etterkontroll2-retterbevis/`. Eksakte inn-/utfilhasher, rapport-ID-er, feilmeldinger og bevarte tidligere filer finnes i [maskinlesbart retterbevis](retting-etterkontroll2.json).

B2s revisjons-ID er en UUID som utstedes ved lokal innlesning. Den er ikke et XML-felt eller en innholdshash. Kontrollen binder samme valgte UUID gjennom inventar, observasjon, dokumentkontekst og uttrekk til det kontrollerte originalinnholdet. Den gir ingen ekstern attestasjon av UUID-ens utstedelse. Tidligere ID-er og parser-/fingerprintregler er uendret; ingen ny ID-betydning er innført.

En særskilt kompatibilitetsprøve endrer bare responskonvoluttens tid, med tydelig syntetisk proveniens, og registrerer den gjennom ordinær B2. Samme byteidentiske vedtaksobjekt beholder UUID, opprinnelig artefakt, tolkning og observasjoner. Et nytt valgt inventar beholder seks kildeverifiserte relasjoner i faktisk gjenlest JSON/Excel. Senere responsers råhash/metadata er adskilt fra uttrekkets første originalpeker; B2s etablerte fingerprintregel er ikke erstattet av krav om identiske konvoluttbyte.

## TDD og kontroller

Testgrensen er den allerede godkjente original → seksjon → relasjon → skrevet og faktisk gjenlest JSON/Excel. Før retting feilet sesjonsprøven og råkapittelprøven fordi de lagrede filene fortsatt hadde kildeverifiserte relasjoner. Hyperlenkeprøven traff sentinel foran inputinnlasting før retting, uten at inputen fikk materialiseres. Prøvene bestod etter hver retting. Detaljert sluttresultat står i retterbevisets `checks`.

Alle kommandoer er kjørt fra `C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a` med:

```powershell
$env:PYTHONPATH='C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a/work/spec-verify-deps;C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a'
$taskPython='C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $taskPython -m pytest -q tests/test_omtale.py --basetemp work/fix2-focused-complete
& $taskPython -m pytest -q tests/test_b6_authentic.py tests/test_b6_cli.py tests/test_b8.py tests/test_b9.py --basetemp work/fix2-compatibility-final
& $taskPython -m ops.omtale_proeve --output work/omtale-post1-etterkontroll2-leveranse
& $taskPython -m ruff check .
& $taskPython -m ruff format --check .
& $taskPython -m mypy
git diff --check
```

Avhengighetsmålet er `C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a/work/spec-verify-deps`. Faktisk lastet `lxml 6.1.3`, `openpyxl 3.1.5` og `pypdf 6.10.0` er dokumentert sammen med Python 3.12.14, eksekverbar og `PYTHONPATH`. Den endelige omtalesuiten bestod med **92 prøver på 292,22 s**, inkludert 32 små område-/indeksprøver og B2-konvoluttkompatibilitet. B6/B8/B9-kompatibilitetskjøringen bestod med **128 prøver på 49,15 s**. Ruff check og format bestod for 92 filer, mypy for 51 produktmoduler, `git diff --check` og 46 lokale fillenker i fem endrede dokumenter bestod. Ingen ny fullsuite er kjørt; endelig fullsuite hører til CI. Den tidligere fullsuiten og tidligere rettingsresultater gjelder sine opprinnelige kandidater.

## Ny autentisk leveranse og bevaring

`work/omtale-post1-etterkontroll2-leveranse/` er en ny katalog med faktisk gjenlest JSON og Excel, uendret B8/B9-grunnlag og offline reeksport etter at SQLite-filen er gjort utilgjengelig. Rapport-ID er `22e216820b2b2d17fd43016d8be437a8cbdfaf4cbd8920b871aec0acd55d7143`; basis-ID er fortsatt `4fb6187784cfe233a89ce5d7180b4d76b3de669125d70c8eead7d70e9a0986a1`. Et nytt datert B8-snapshot gir ny rapport-ID, uten å endre tidligere resultater. Inventaret har seks observasjoner, to opprinnelige hendelsesgrupper, åtte seksjoner og seks kildeverifiserte post 1-relasjoner med `ikke_faglig_godkjent`.

De tidligere autentiske rapportene `299de472b0c01c64983a7816b178991fa5f76e4737bb33e86fb99d9f1f87de13` og `6021e1344038b6727f76cb09e77e382b4b5b1a48948acd977df0849eba391eb3` gjenleses med uendrede ID-er og kildegrunnlag. Gamle B8-JSON/B9-Excel er åpnet og kontrollert uten omskriving. Alle ti original-/støttefiler er byteidentiske. Ingen nye layoutendringer eller native Excel-prøver hevdes. Ressursgrenser og avvist innhold er dokumentert i [pilotkontrakten](../../omtale-pilot.md). #35 bygges ikke; #10 står åpen.
