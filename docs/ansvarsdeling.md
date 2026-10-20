# Ansvarsdeling

## Innlesning fra Stortinget

Området `innlesning/` skal håndtere oppdagelse, henting, kildebevaring, endringsdeteksjon og strukturering av endelige vedtak. Hvert strukturert element skal kunne spores til originalkilden. Delen skal kunne kjøres uten analysegrensesnittet.

Senere innlesning av regjeringsforslag, komitéforslag og manuelle kilder skal ha adskilte kildeadaptere. Tilgjengeligheten til en ny kilde skal ikke styre om vedtaksinnlesningen kan kjøres.

## Felles datakontrakt

Datakontrakten skal skille mellom endelig vedtak, regjeringsforslag og komitéforslag. Den skal beskrive sesjon, budsjettår, kapittel, post, beløp, beløpets betydning, kildedokument, dokumentnummer, versjon og kontrollstatus.

Departementstilknytning skal kunne vedlikeholdes manuelt med gyldighetsperiode. Bruk administrativ departementskode og særskilt Gul bok-gruppering som adskilte opplysninger, jf. [registergrunnlaget](departementsregister.md). Historikken skal skille forslag, bevilgningsvedtak, kilderettelser, fullmaktsrammer og regnskap. Underposter bevares som underliggende spesifikasjon og holdes adskilt fra posttotaler. Python og SQLite er godkjent for lokal B1-innlesning; openpyxl brukes til Excel. Den implementerte grensen er beskrevet i [datakontrakt v1](datakontrakt.md) og [ADR 0001](adr/0001-lokal-innlesning.md).

## Analyse og fremstilling

Området `analyse/` skal bruke den dokumenterte kontrakten til søk, sammenligning, visning og eksport. Første prioriterte visning er beskrevet i [kravgrunnlaget](krav.md). Den omfatter utvalg på departement, kapittel og post og sporbare beløp fra forslag, innstilling og vedtak.

Analysedelen skal gjøre manglende datagrunnlag og uavklarte uttrekk synlige. Første leveranse gir Excel-uttrekk og synlig kontrollstatus. Et interaktivt grensesnitt og flere kildeintegrasjoner kommer senere.

## Endringer på tvers

Tickets skal beskrive konsekvenser for begge deler når datakontrakten endres. Innlesning og analyse skal kunne kjøres og driftssettes hver for seg. Azure er en mulig senere plattform; kildebehandling og faglige regler skal kunne prøves lokalt.
