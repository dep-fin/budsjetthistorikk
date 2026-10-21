# Budsjetthistorikk

Budsjetthistorikk skal gi Finansavdelingen i Finansdepartementet grunnlag for analyser og uttrekk av historiske budsjettforslag og budsjettvedtak.

Prosjektet har to adskilte deler:

- **Innlesning fra Stortinget:** hente, bevare og strukturere endelige vedtak og deres kilder.
- **Fremstilling av budsjetthistorikk:** søk, sammenligning, analyse og uttrekk fra det strukturerte datagrunnlaget.

Innlesningen skal kunne kjøres uten analysegrensesnittet. En dokumentert datakontrakt skal knytte delene sammen.

## Første leveranse

Første leveranse gjelder endelige stortingsvedtak fra sesjonen 2026–2027, også vedtak om budsjettet som foreslås i Prop. 1 S (2026–2027). Nye og endrede vedtak skal kontrolleres daglig. Budsjettår, kapittel, post og beløp skal struktureres. Både inntekter og utgifter inngår.

Alle bevilgningsendringer skal fanges opp, også i saker uten regjeringsproposisjon og i sammensatte lov- og budsjettsaker. Tvetydige uttrekk skal bevares og sendes til kontroll før de inngår i godkjente analysetall. Første leveranse gir lagring og et kontrollerbart Excel-uttrekk; det interaktive grensesnittet kommer senere. Planlagt daglig kjøring er kl. 06.00 norsk tid. Excel-/CSV-filer brukes til manuelt registervedlikehold og kontroll. Feil og uavklarte uttrekk varsles med GitHub-issues; gjentakelser oppdaterer samme issue.

Regjeringens forslag og komitéforslag er egne fremtidige kilder. Regjeringsforslag kan tas inn tidlig dersom en enkel kildevei blir dokumentert; dette skal ikke forsinke vedtaksinnlesningen. Manuell innlesning er et mulig senere alternativ.

## Fremtidig analyse

Brukeren skal kunne velge departement, kapittel, post og kombinasjoner av disse. Visningen skal sammenstille beløp i regjeringens forslag, komiteens innstilling og endelig vedtak, med dokumentnummer og kildehenvisning for hvert ledd. Første uttrekk skal kunne leveres til Excel.

Historikken skal vise hvert forslag, vedtak og endring gjennom året, frem til regnskapstallet. Regnskap og fullmaktsrammer holdes adskilt fra vedtatte bevilgninger. Eldre sesjoner, eksisterende historiske data og kapittel- og postomtale skal kunne innarbeides senere.

## Dokumentasjon og arbeidsmetode

- [Krav og åpne beslutninger](docs/krav.md)
- [Ansvarsdeling](docs/ansvarsdeling.md)
- [Kilder og behov for dataprøver](docs/kilder.md)
- [Departementsregister og kapitteltilknytning](docs/departementsregister.md)
- [Faglige funn fra vedleggene](docs/faggrunnlag.md)
- [Godkjent leveranseplan](docs/leveranseplan.md)
- [Fast arbeidsflyt med issues](docs/arbeidsflyt.md)
- [Innlesningsdelen](innlesning/README.md)
- [Analysedelen](analyse/README.md)

## Status

Kildeundersøkelsen #2 er levert i PR #11. Python, SQLite og openpyxl er godkjent for lokal innlesning. B1 (#4) gir ett opprinnelig vedtak fra kilde til SQLite og Excel. B2 (#5) legger til kildeinventar, kildeobservasjoner, innholdsrevisjoner og gjenopptak. B3 (#6) har en egen adapter og beregner historikk for uttrykkelig valgte revisjoner/tolkninger, konto og år. B1/B2s lagrede resultater og parserbredde beholdes. Daglig kjøring og samlet sesjonseksport kommer i senere tickets. Mottakersystem og driftsplattform er åpne; Azure tas opp igjen før valget blir styrende.

## Kjør B1 lokalt

For B3 brukes fortsatt samme Python-miljø. Se [B3-kontrakten](docs/datakontrakt.md#b3--beløpsobservasjoner-og-valgt-historikk) for avgrensningene og [kildeprøvene](tests/fixtures/b3/README.md) for autentiske og syntetiske tester.

Krever Python 3.12. Kjør fra repoets rot. Bruk et separat virtuelt miljø:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
.venv/Scripts/python -m ruff check .
```

På Linux/macOS brukes `.venv/bin/python`. For vanlig bruk er `requirements.txt` tilstrekkelig. CI kjører de deterministiske kontrollene på pull requests og ved manuell oppstart.

Frakoblet demonstrasjon av den historiske prøven, vedtak **40033944**, nr. **113**, fra 2024–2025:

```powershell
python -m innlesning hent --vedtak-id 40033944 --sesjon 2024-2025 --historisk-proeve --database demo.sqlite --response tests/fixtures/40033944.derived.xml --metadata tests/fixtures/40033944.metadata.json --excel demo.xlsx
```

Bruk miljøets Python også i denne kommandoen. Prøven er et avledet XML-utdrag med egen hash og tydelig proveniens. Den viser åtte opprinnelige bevilgningslinjer for 2025: utgifter **910 097 000 kroner** og inntekter **300 000 kroner**. Den representerer ett vedtak. Den samlede leveransens startsesjon er fortsatt 2026–2027.

Utelat `--response` og `--metadata` for å hente hele sesjonsresponsen fra det faste offentlige API-et. `--sesjon` har standardverdien `2026-2027`; et valgt vedtak må oppgis med `--vedtak-id`. For eldre prøver kreves `--historisk-proeve`. En vellykket HTTP-respons bevares byteidentisk i SQLite, også når valgt vedtak ikke kan struktureres.

Kommandoen skriver kjørings-ID og status som JSON. Returkoder er 0 for strukturert prøve, 2 for kontrollbehov og 1 for innlesningsfeil. Et manglende eller tvetydig beløp vises tomt med kontrollbehov. Godkjente summer gis da ikke. Nett-/transportfeil gir feilstatus; det opprettes ingen tom, vellykket import.

Eksport kan kjøres senere uten nett eller ny innlesning:

```powershell
python -m analyse --database demo.sqlite --kjoring <kjørings-ID> --excel kontroll.xlsx
```

Se [innlesningens grense](innlesning/README.md), [datakontrakt v1](docs/datakontrakt.md), [teknologivalget](docs/adr/0001-lokal-innlesning.md) og [fixtureproveniens](tests/fixtures/README.md).

## Kjør B2 lokalt

Synkroniser hele startsesjonens kildeinventar med den samme HTTP-adapteren:

```powershell
python -m innlesning synkroniser --database budsjett.sqlite --sesjon 2026-2027
```

Lagret XML kan brukes med `--response` og `--metadata`. Ingen vedtaksdato eller API-type brukes som filter. JSON-rapporten viser nye/uendrede/rettede/manglende ID-er, konkrete revisjoner, feil og kontrollbehov. Returkode er 0 for fullført uten kontrollbehov (eller forberedt jobb), 2 for fullført med kontrollbehov og 1 for feil. Ukjent tekst bevares til kontroll. Et gyldig kildeinventar er ingen garanti om komplett faglig strukturering.

For å sikre gjenopptaks-ID før publisering, bruk `--forbered`. Denne kommandoen bevarer råbyte og jobb som `venter`; noter JSON-feltet `kjoring`. Gjenopptak og rapportlesing trenger bare database og den ID-en:

```powershell
python -m innlesning gjenoppta --database budsjett.sqlite --kjoring <jobb-ID>
python -m innlesning rapport --database budsjett.sqlite --kjoring <jobb-ID>
```

En ventende jobb blokkerer ny jobb i samme datasett/sesjon. Gjenopptak bruker de lagrede bytene; det trengs ingen opprinnelig kildefil eller nettilgang. Fullført gjenopptak oppretter ingen nye observasjoner, revisjoner eller postrader. Feil ved publisering gir rollback; ingen delvis sesjon blir gjeldende. Eldre kilde-/hentetid enn siste vellykkede observasjon gir bevart feiljobb. Manuelle gamle snapshot skal ikke presenteres som nyere kilde; bruk en separat prøvedatabase for historisk replay.

Den autentiske historiske fixturen er et utdrag og krever uttrykkelig valgt ID. Den brukes derfor med valgt omfang, ikke som full sesjon:

```powershell
python -m innlesning synkroniser --database b2-proeve.sqlite --sesjon 2024-2025 --historisk-proeve --vedtak-id 40033944 --response tests/fixtures/40033944.derived.xml --metadata tests/fixtures/40033944.metadata.json
python -m analyse --database b2-proeve.sqlite --revisjon <revision_id fra kjørerapporten> --excel b2-valgt-versjon.xlsx
```

`--vedtak-id` begrenser **importomfanget**. Full inventering kjøres uten dette flagget; etterpå kan én rapportert `revision_id` eksporteres separat. `--excel` på `synkroniser` krever valgt ID og eksporterer bare dette vedtaket. Samlet sesjonsbevilgning ligger i B6. Historiske/syntetiske prøver er isolert fra produksjonsinventaret, også når samme database brukes.

B1-kommandoene og gamle kjørings-ID-er består. Gamle prøverapporter adopteres ikke automatisk som B2-vedtak. Excel viser valgt råhash og revisjons-ID separat, med historisk/gjeldende status, siste observasjon og revisjonsbundne kontrollhenvisninger. Se [datakontrakten](docs/datakontrakt.md#b2--kildeinventar-observasjoner-og-revisjoner) og [ADR 0002](docs/adr/0002-kildeobservasjoner.md) for normalisering, rekkefølge, migrering og kontrollstatus.

## Kjør B3 lokalt

Synkroniser ønskede kilder med B2 først. Velg hver rapportert revisjon eksplisitt. Tolkningen henter ingen nettdata og endrer ingen B1/B2-resultater:

```powershell
python -m innlesning tolk --database budsjett.sqlite --revisjon <revisjons-ID> --tolkning storting-belop-v1
```

Resultatet gir `belopsuttrekk` og tolknings-ID. Runde kan velges med `--runde nysaldering --rundegrunnlag "<konkret dokument/kildebevis>"`; uten sikkert grunnlag forblir runden uavklart. Et datoanslag brukes aldri som rundebevis.

Lagre de ønskede uttreks-ID-ene i en JSON-utvalgsfil, for eksempel `utvalg.json` for den kontrollerte prøven 2541/70 i 2024:

```json
{
  "dataset": "prove",
  "extraction_ids": ["<originalens uttreks-ID>", "<RNBs uttreks-ID>", "<øvrig uttreks-ID>", "<siste endrings uttreks-ID>"],
  "budget_year": 2024,
  "chapter": "2541",
  "post": "70"
}
```

```powershell
python -m analyse --database budsjett.sqlite --utvalg utvalg.json --excel historikk.xlsx
python -m analyse --database budsjett.sqlite --beregning <lagret beregnings-ID> --excel historikk-igjen.xlsx
```

Excel viser `Historikk`, `Beløpsobservasjoner` og `Grunnlag og kontroll`. Før/delta/etter, rå og normaliserte verdier, separate beregnede saldoer, kilde-/tolkningsidentitet, avvik og ferskhet følger med. Manglende start, ukjent ledd, uklar rekkefølge og lokale/kronologiske konflikter sperrer avstemt saldo. Like beløp fjernes aldri automatisk. Bevarte sluttkildetall vises også ved sperret kjede.

`avstemt_utvalg` gjelder bare det eksplisitte utvalget; det er ingen faglig godkjenning eller erklæring om komplett sesjon/budsjettår. En ny kilderevisjon kan gjøre beregningen utdatert, også etter A → B → A. Den gamle beregningen og dens rågrunnlag bevares. Full historisk Excel-import, registervedlikehold, manuell avklaring og sesjonsdekning følger egne tickets. V1s avgrensning består; B4-utvidelsen velges separat nedenfor. Se [kontrakten](docs/datakontrakt.md#b3--beløpsobservasjoner-og-valgt-historikk).

## Kjør B4 lokalt

Tolk ønsket B2-revisjon med v2 og eksporter hele uttrekket, også for rene tekstvedtak:

```powershell
python -m innlesning tolk --database budsjett.sqlite --revisjon <revisjons-ID> --tolkning storting-belop-v2
python -m analyse --database budsjett.sqlite --belopsuttrekk <beløpsuttrekks-ID> --excel kontroll.xlsx
```

V2 bevarer post 24, nummererte komponenter, negative nettoresultater, kildens navn og stikkord. Posttotal og komponenter har egne cellepekere og hierarkirelasjoner. For en historikk på underpost velges for eksempel `"detail_level": "underpost", "subpost": "1"` i utvalgsfilen; uten dette brukes posttotalen alene. Senere nivåoppstillinger uten uttrykkelig delta vises som etterbeløp og sperrer additiv saldo med `mangler_delta`.

Inntekt/utgift følger kapittel. Kapitalregnskapskonti holdes utenfor bevilgningssaldoen; 90-poster under kapittel 6000 er bevilgninger. Organisasjonsgrunnlaget har bare ni dokumenterte kapitteloppslag for **2027**, med separate fdep-/gdep-koder og registerhash i tolkningsidentiteten. Ukjent oppslag bevarer beløpet og gir avvik. En regneavstemming godkjenner ingen organisasjonskobling.

Uttrekkseksporten viser alle observasjoner, hierarki, organisasjon, avvik og hele B2-vedtaksteksten. Tekstfullmakter, anmodninger og uavklart tekst kan kontrolleres uten bevilgningskjede. Ingen fullmaktsramme normaliseres til additiv årsbevilgning. Historikkeksporten har også fulltekst for valgte revisjoner, med videreføring av lange felt. V1-ID-er, lagrede tolkninger og B1/B2-resultater består. Se [B4-kontrakten](docs/datakontrakt.md#b4--særtilfeller-med-eksplisitt-tolkning-v2) og [prøvenes proveniens](tests/fixtures/b4/README.md).

## Kjør B5 lokalt

B5 gir registervedlikehold og faglige kontrollavgjørelser gjennom Excel/CSV, med separate godkjente enkeltbeløp og kontrollerte resultater. [Arbeidsflyten og filformatene](docs/b5-arbeidsfiler.md) viser hele rundturen uten kodeendringer; [B5-kontrakten](docs/datakontrakt.md#b5--registervedlikehold-og-faglige-avgjørelser) beskriver API, immutabilitet og SQLite 4.

```powershell
python -m innlesning.maintenance --database budsjett.sqlite register-seed
python -m innlesning.maintenance --database budsjett.sqlite register-export --snapshot <snapshot-ID> --output register.xlsx
# Rediger hele kandidatregisteret med år, kilde og begrunnelse.
python -m innlesning.maintenance --database budsjett.sqlite register-import --input register.xlsx
python -m innlesning.maintenance --database budsjett.sqlite reinterpret --revision <B2-revisjons-ID> --register <nytt-snapshot-ID>
python -m innlesning.maintenance --database budsjett.sqlite basis-define --description "Avgrenset kontroll mot navngitt kildebevis"
python -m innlesning.maintenance --database budsjett.sqlite basis-activate --extraction <nytt-uttrekks-ID> --register <nytt-snapshot-ID> --control <kontrollgrunnlag-ID>
python -m innlesning.maintenance --database budsjett.sqlite control-export --extraction <nytt-uttrekks-ID> --register <nytt-snapshot-ID> --control <kontrollgrunnlag-ID> --output kontroll.csv
# Bevar faktisk bevisfil med evidence-add, og fyll ut avgjørelse/begrunnelse/kontrollør/bevis-ID.
python -m innlesning.maintenance --database budsjett.sqlite control-import --input kontroll.csv
python -m innlesning.maintenance --database budsjett.sqlite reprocess --extraction <nytt-uttrekks-ID> --register <nytt-snapshot-ID> --control <kontrollgrunnlag-ID> --output kontrollerte-belop.xlsx
```

Velg `.xlsx` eller `.csv` for begge arbeidsfiler. Importresultatet har varig ID og ark/rad/felt-diagnostikk; `import-read --id <ID>` leser dette igjen. `register-head` viser gjeldende publisert register. En ny fil kan ikke overskrive en nyere avgjørelse eller feil base. Historisk lesing og ny alternativ tolkning aktiverer ingen kontroller. Kilde-, register-, tolknings- og kontrollgrunnlag har overgangsvern ved A → B → A. Tidligere råbyte, JSON, observasjons-ID-er og tekniske beregninger består.

Startregisteret bruker bare brukerens navn/forkortelser og de ni tidligere dokumenterte 2027-koblingene. Postkatalogen starter tom; original Gul bok-fil er ikke kontrollert på nytt. 900/32 må opprettes med 2025-bevis, og får ingen inngående nullbevilgning. 5538/70 kan få en særskilt signert referatbundet etterbeløpskorreksjon; råteksten `I 615 833` beholdes. Godkjent enkeltbeløp gir ingen årsdekning eller automatisk kjedegodkjenning. Havtil-/5999-konflikter består. Historisk Excel-import og rolleforvaltning inngår ikke.
