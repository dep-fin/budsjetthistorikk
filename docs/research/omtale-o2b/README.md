# O2b/#35: begge 210-postene fra original til gjenlest JSON og Excel

Kontrollert 23. oktober 2026. Kandidaten bygger på main `6f7145d49a91325e9229bc89eee3b540cdced8ce`, etter levert O2a/#34 i PR #36. Eieren har gitt eget mandat for O2b. Dette er lokal implementering og kontroll; orkestratorens samlede review, separate sikkerhetsaudit, publisering, full CI og bekreftede merge er egne porter. Ingen av disse portene erklæres gjennomført her. #10 står åpen.

## Kontrakt og resultat

[Kontrakttillegget](../../omtale-pilot.md#o2b-utvidelse-fastsatt-før-kode-23-oktober-2026) ble skrevet før produktkode. A-formatet tillater flere seksjoner og relasjoner med samme feltbetydning. B beholder derfor `omtale-pilot-1`/`omtale-grunnlag-1`, men krever eksplisitt uttrekksversjon `o2b-html-pdf-1`. Den tidligere A-algoritmen og CLI-standardvalget er bevart. Et nytt revisjonssuffiks innen B gir nye seksjons-/grunnlags-ID-er med samme dokumenterte algoritme. De felles dataklassene har samme felter og gjeneksporteres fra den gamle Python-inngangen; modul-CLI og import bruker nå samme klasseidentitet.

Alle seks O1-originaler og fire støttefiler er bevart med uendrede byte og hasher. Ingen HTTP er gjort. Hele 210-grunnlaget har fortsatt **seks beløpsobservasjoner og to posthendelser**. Post 1 viser 160 243 000 / +5 796 000 / 166 039 000 kroner. Post 22 viser **32 185 000 / −3 000 000 / 29 185 000**. Før/etter er kildeobserverte beløp, ingen historisk startsaldo.

B har elleve seksjoner: A sine P1_PDF, P1, PN, PT, K1, KS, KT og V, samt P22, PT22 og K22. Tretten kildeverifiserte relasjoner binder dem til de to eksisterende hendelsene. P1, KS, KT og V har hver relasjoner til begge hendelsene; flere seksjoner knyttes til hver hendelse. Dette er faktisk mange-til-mange uten kopierte beløp eller P1-seksjoner.

P1 beholder hele avsnittet og begge kontiene i seksjonsomfanget. Den enkelte B-relasjonen angir én målpost. Post 22-relasjonen fra P1 gjelder bare omdisponeringsutsagnet; begrunnelsen sier uttrykkelig at lønnsforklaringen gjelder bare post 1. Ingen eksakt lønnskomponent beregnes. P22/K22 peker tilbake til post 1 og bevarer omtalenavnet «kulturmiljøforvaltning». PT22 og vedtaket bevarer rånavnet «kulturminneforvaltning». PN/post 60/Vega står som autentisk fullmaktskontekst uten relasjon til 210s beløpshendelser.

Et særskilt merket syntetisk relasjonsforslag fra K22 til post 1 bevares som tillegg, med eksplisitte hendelses-/seksjons-/belegg-ID-er, begrunnelse og status `uavklart`/`ikke_faglig_godkjent`. De tretten dokumenterte relasjonene består identisk. Forslaget gir et globalt avvik også ved tomt kontofilter. Konto/beløp alene er ingen inngang for å opprette en dokumentert relasjon.

## Akseptmatrise

| Krav | Faktisk kontroll og resultat |
| --- | --- |
| P22/K22 og komplett kjede | Autentiske originaler åpnes på nytt. Gjenlest JSON/Excel har full tekst, lokator, kildehash, hierarki, avsender, PT22/KT/V-belegg og eksisterende 210-revisjons-/observasjons-/hendelses-ID-er. De eksakte post 22-beløpene og begge rånavnene er kontrollert. |
| Felles P1 og ingen dobbelttelling | P1 har én identitet, to målrelasjoner og full opprinnelig tekst. Gjenlest grunnlag har seks observasjoner og to `step_id`-grupper. Ingen forslagstabell, omtale eller fullmakt gir en ny beløpsobservasjon. |
| Post 1, post 22, begge, tomt | Fire faktisk skrevne/gjenleste par viser henholdsvis 3, 3, 6 og 0 beløpsobservasjoner. Det globale grunnlaget og seksjons-ID-ene består. Post 1 får ingen post 22-beløpsrader gjennom P1. Tomt filter beholder kilder, relasjoner og globale avvik. |
| Uavklart forslag | Separat faktisk filpar bevarer grunn og belegg uten å erstatte kjeden. Lang begrunnelse med innledende `=` gjenleses fullt gjennom tekstfortsettelse og forblir tekst i Excel. PN avvises som foreslått 210-beløpskobling. |
| Falsk kobling og motstrid | Merkede syntetiske feil i postkobling, lønnsomfang, seksjonstekst, lokator og faglig status får omberegnede ytter-ID-er og skrives til JSON og inn i Excel-snapshotet. Gjenleseren avviser dem. Feil P22-mottaker og løs konto-/beløpsomtale gir synlig uavklart kjede i faktisk gjenleste par. |
| Tidligere A-filer | To ekte, før B eksisterende JSON-/Excel-par fra `outputs/o2a-210-post1-52f0545` er lest uten omskriving. Samme rapport-ID, åtte seksjoner og seks relasjoner består. JSON reserialiseres byteidentisk. Alle fire filhasher er uendret etter kontroll. |
| Uavhengig ny offisiell registrering | For hver av manglende, korrupt, motstridende og feilet omtale skrives/gjenleses tomt omtaleuttrekk med globale avvik. Deretter oppdages og lagres autentisk 40034229 i en ny database via ordinær `innlesning synkroniser`, tolkes med eksisterende v2 og eksporteres via ordinær analyse-CLI. Faktiske beløpsceller gjenleses. Ingen historisk Excel, register eller startsaldo brukes. Den gamle v1-parserens kontrollretur 2 beholdes. |
| Ressursgrenser og gamle resultater | Eksisterende O2a-grenseprøver for lange originaler, tekstfortsettelse, formeltegn, ZIP/XML, områder, metadata, kilde-/vedtaksbinding og forfalskede snapshot er kjørt. B6/B8/B9-regresjonene er kjørt uten endringer i deres produktkode, formater eller gamle ID-er. |
| Stabile uttak og versjon | Gjentatt identisk valg gir samme ID-er. Et uttrykkelig B-revisjonssuffiks gir nye seksjons-/grunnlags-ID-er med uendret B8-/beløpsgrunnlag. Tidligere par gjenleses med uendrede hasher, og overskriving av eksisterende filnavn avvises. |

Utførte lokale testkjøringer: O2a/O2b-grensen **127 bestått på 474,86 s**, B6/B8/B9 **126 bestått på 46,78 s**, deretter hele B-filen og begge A/B-CLI-/offline-prøvene **17 bestått på 99,56 s**. Ingen av disse kjøringene hadde hopp eller feil. Den første brede omtale-kjøringen startet før dataklassene ble flyttet til felles modul og B-begrunnelseskolonnen ble utvidet; den siste kjøringen dekker hele B-aksepten og CLI etter disse rettingene, inkludert en ekstra syntetisk prøve av en ufullstendig lokal tabell. Den sistnevnte prøven avdekket først manglende kontroll av kapittelradens lengde; rettingen bevarer tabellen med synlig motstrid i begge gjenleste filer. Alle seks siste leveransepar og de to ekte gamle A-parene er i tillegg gjenlest på nytt etter rettingen. Ruff check, Ruff format (96 Python-filer), mypy (53 produktmoduler), lokale dokumentlenker og `git diff --check` består. Fullsuite er overlatt til den avsluttende CI-porten og er ikke hevdet kjørt lokalt.

## Filer og reproduksjon

Den siste lokale leveransen ligger i checkoutets `work/omtale-o2b-leveranse-2/`. Der finnes `begge`, `post1`, `post22`, `tomt`, `syntetisk-forslag` og `offline`, hver som faktisk JSON/Excel-par, samt `kontroll.json`. Første leveranse i `work/omtale-o2b-leveranse-1/` er bevart. `offline.json` er byteidentisk med `begge.json` og er eksportert etter at databasen ble flyttet til utilgjengelig filnavn. Filene er selvforsynte; gjenlesing bruker de innebygde originalene, uten opprinnelig kildekatalog eller nett.

[verification.json](verification.json) bevarer faktiske filstørrelser, SHA-256, rapport-/grunnlags-ID-er, runtime, kildekontroll, testutfall og de gamle A-filene. Testene skriver egne tydelig merkede syntetiske feilfiler i nye kataloger under `work/`; autentiske originaler og gamle leveranser overskrives ikke.

Fra reporoten med pinnede `requirements-dev.txt`-avhengigheter:

```powershell
python -m ops.omtale_begge_proeve --output work/omtale-begge-ny --previous <ekte-o2a-katalog>
python -m pytest tests/test_omtale.py tests/test_omtale_o2b.py -q --basetemp work/omtale-test-ny
python -m pytest tests/test_b6.py tests/test_b8.py tests/test_b9.py -q --basetemp work/regresjon-ny
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

`--previous` er valgfritt ved reproduksjon uten tilgang til den tidligere lokale A-leveransen. Det lokale kompatibilitetsbeviset her bruker de ekte gamle filene, ikke nygenererte A-er. En fersk `--output`/`--basetemp` bevarer tidligere prøver.

Den offentlige B-CLI-en og dens offline-gjeneksport er også kjørt, med nye `work/omtale-o2b-cli-begge.*`/`work/omtale-o2b-cli-offline.*`. En tidlig CLI-kontroll avdekket separate dataklasseidentiteter ved `python -m`; felles dataklasser rettet dette. B og A har begge bestått den faktiske CLI-/offline-grensen etter rettingen.

## Visuell kontroll og begrensninger

Syv representative områder i den faktisk lagrede siste arbeidsboken er rendret med bundlet `@oai/artifact-tool` og visuelt kontrollert: Historikk, P22, K22, post 22-relasjonsomfang, kilder, globale avvik og innebygd frosset grunnlag. B utvider bare bredden på relasjonens begrunnelseskolonne, slik at lønnsavgrensningen er lesbar. A-eksportens layout er bevart. Tekniske HTML-/base64-/ID-felt er kontrollgrunnlag som åpnes ved behov; de er ikke en trykksatt dokumentgjengivelse. Ingen formler er lagt inn. Rendereren viser dato som serienummer 45642; den faktiske lagrede cellen har datoverdi 16.12.2024 og format `dd.mm.yyyy`, kontrollert med openpyxl. Ingen native Excel-applikasjon er startet eller prøvd.

Implement/TDD og regnearkskillen er fulgt ved den avtalte høye testgrensen. Første vertikale B-prøve feilet på manglende P22/K22/PT22 før implementering og bestod etterpå. Det innledende lokale pytest-tempområdet var utilgjengelig; alle reelle prøver bruker nye `work/`-kataloger. Pinnet `lxml 6.1.3`, `openpyxl 3.1.5` og `pypdf 6.10.0` er brukt. Ingen oppgradering eller ny avhengighet inngår.

O2b er fortsatt et smalt kontrolluttrekk for to posthendelser i 2024. Alle relasjoner er `ikke_faglig_godkjent`. Full dokument-/årsvisning i #37, faktisk komitéendring, andre saker, O3–O5, produksjonsdrift, årsdekning og faglig godkjenning inngår ikke. Hovedschema 5, B1/B2-parser, gamle v1/v2- og frosset-v1/v2-kontrakter, B5/B7/B8/B9 og ordinære standardvalg er bevart. #10, #13, #32 og #1 beholder sine rester.
