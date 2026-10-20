# Budsjetthistorikk

Budsjetthistorikk skal gi Finansavdelingen i Finansdepartementet grunnlag for analyser og uttrekk av historiske budsjettforslag og budsjettvedtak.

Prosjektet samles i ett privat repositorium med to adskilte deler:

- **Innlesning fra Stortinget:** oppdage, hente, bevare og strukturere vedtak og relevante dokumenter.
- **Fremstilling av budsjetthistorikk:** søk, sammenligning, analyse og uttrekk fra det strukturerte datagrunnlaget.

Innlesningen skal kunne kjøres uten at analyseløsningen kjører. Delene skal dele dokumenterte begreper og dataformater. Valg av programmeringsspråk, database og driftsplattform er åpne.

## Bekreftet omfang

Første utviklingstrinn er daglig innlesning av nye vedtak og strukturerte budsjettall. Startpunktet er stortingssesjonen 2026–2027, herunder Prop. 1 S (2026–2027).

Den samlede løsningen skal dekke alle bevilgningsforslag fra regjeringen og alle vedtatte bevilgningsendringer gjennom året, også uten tilknytning til en proposisjon. Dokumenttype alene skal ikke avgrense relevante bevilgningsendringer.

På sikt skal løsningen også inneholde komitéforslag, kapittel- og postomtale og eldre historikk. Brukeren har eksisterende historiske data som skal kunne innarbeides senere. Rekkefølgen for utvidelsene avklares før implementering.

## Dokumentasjon

- [Krav og åpne beslutninger](docs/krav.md)
- [Ansvarsdeling](docs/ansvarsdeling.md)
- [Kilder og behov for dataprøver](docs/kilder.md)
- [Arbeidsflyt med issues](docs/arbeidsflyt.md)
- [Innlesningsdelen](innlesning/README.md)
- [Analysedelen](analyse/README.md)

## Status

Prosjektet er under avklaring. Repositoriet inneholder foreløpig dokumentasjon og planleggingsissues. Det er ikke implementert innlesning, database, analysegrensesnitt eller daglig kjøring.
