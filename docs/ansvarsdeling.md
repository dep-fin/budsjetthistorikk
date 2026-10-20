# Ansvarsdeling

## Innlesning fra Stortinget

Området `innlesning/` skal håndtere oppdagelse, henting, kildebevaring, endringsdeteksjon og strukturering av endelige vedtak. Hvert strukturert element skal kunne spores til originalkilden. Delen skal kunne kjøres uten analysegrensesnittet.

Senere innlesning av regjeringsforslag, komitéforslag og manuelle kilder skal ha adskilte kildeadaptere. Tilgjengeligheten til en ny kilde skal ikke styre om vedtaksinnlesningen kan kjøres.

## Felles datakontrakt

Datakontrakten skal skille mellom endelig vedtak, regjeringsforslag og komitéforslag. Den skal beskrive sesjon, budsjettår, kapittel, post, beløp, beløpets betydning, kildedokument, dokumentnummer, versjon og kontrollstatus.

Departementstilknytning og endringer gjennom budsjettåret må avklares før kontrakten fastsettes. Database og programmeringsspråk er ikke valgt.

## Analyse og fremstilling

Området `analyse/` skal bruke den dokumenterte kontrakten til søk, sammenligning, visning og eksport. Første prioriterte visning er beskrevet i [kravgrunnlaget](krav.md). Den omfatter utvalg på departement, kapittel og post og sporbare beløp fra forslag, innstilling og vedtak.

Analysedelen skal gjøre manglende datagrunnlag og uavklarte uttrekk synlige. Hvordan dette vises i første leveranse, avklares før bygging.

## Endringer på tvers

Tickets skal beskrive konsekvenser for begge deler når datakontrakten endres. Innlesning og analyse skal kunne kjøres og driftssettes hver for seg. Azure er en mulig senere plattform; kildebehandling og faglige regler skal kunne prøves lokalt.
