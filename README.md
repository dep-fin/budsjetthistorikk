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

Kildeundersøkelsen #2 er levert i PR #11. Python, SQLite og openpyxl er godkjent for lokal innlesning, og byggemandatet gjelder B1 (#4). B1 gir nå et smalt vertikalt snitt fra ett opprinnelig vedtak til bevart kilde, strukturerte SQLite-data og Excel. Daglig kjøring og full sesjonsdekning kommer i senere tickets. Mottakersystem og driftsplattform er åpne; Azure tas opp igjen før valget blir styrende.

## Kjør B1 lokalt

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
