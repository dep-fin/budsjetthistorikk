# ADR 0001: Python, SQLite og openpyxl for lokal innlesning

Status: godkjent av prosjekteieren 20. oktober 2026. Byggemandatet gjelder B1 (#4).

## Bakgrunn og alternativer

U1 viser at kilden er sesjonsvis XML med HTML-tabeller og at et kontrolluttrekk må bevare kildeidentitet, beløpsbetydning og avvik. Innlesning skal kunne kjøres lokalt og uavhengig av et senere analysegrensesnitt. Språk, lagringsmodell og eksportbibliotek påvirker videre kode og datakontrakt. Et senere bytte krever omarbeiding og migrering; beslutningen dokumenteres derfor som ADR.

Python er valgt fremfor TypeScript eller .NET fordi den smale kjeden trenger tabellbehandling, lokal filkontroll og Excel, og ikke et webgrensesnitt. SQLite gir transaksjoner og samlet, flyttbar lagring av råbyte og strukturerte rader uten en databasetjeneste. PostgreSQL eller en administrert skydatabase ville gitt en driftsavhengighet før mottaksmiljøet er avklart. CSV/JSON alene gir svakere kontroll med atomisk lagring av kilder og tilhørende rader.

openpyxl gir kontrollerbar XLSX med numeriske beløp, eksplisitte tekstceller og virkelige hyperlenker. Et pandas-lag er unødvendig for dette eksportformatet. lxml leser XML og HTML med avskrudd DTD-/entitetsoppløsning og nettverk; råkilden beholdes uendret.

## Beslutning

- Python 3.12 er kjørerammen for B1. Bibliotekversjonene er pinnet i `requirements*.txt`.
- SQLite lagrer rårespons og strukturerte opplysninger i samme transaksjon. Kildehash og kjørings-ID er separate identiteter.
- `innlesning/` henter og strukturerer. `analyse/` leser [datakontrakt v1](../datakontrakt.md) og eksporterer med openpyxl.
- Deterministiske tester bruker en autentisk, avledet XML-fixture og litteral kildefasit. Live HTTP er adskilt fra CI.

## Konsekvenser og grenser

B1 krever ingen server, skyressurs eller analyseapplikasjon. SQLite-filen er et lokalt arbeidsgrunnlag. Flerbrukerdrift, automatiske migreringer og mottakersystemintegrasjon er ikke valgt. Azure og driftsplattform skal tas opp med brukeren før de blir styrende.

B1 importerer ett valgt originalvedtak per kjøring og eksporterer én kjøring. Nye vedtak, kilderettelser, sammensatt historikk og samlet sesjonsdekning følger senere tickets. Ingen kode i B1 gjør disse produktbeslutningene implisitt.
