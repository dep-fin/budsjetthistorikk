# Krav og åpne beslutninger

## Formål og brukere

Finansavdelingen i Finansdepartementet skal kunne analysere og hente ut historiske budsjettforslag og budsjettvedtak, med sporbarhet fra hvert beløp til kilden.

## Første leveranse

- Kilden er endelige stortingsvedtak fra Stortinget og Stortingets datatjenester.
- Innlesningen starter i sesjonen 2026–2027, herunder vedtak om budsjettet foreslått i Prop. 1 S (2026–2027). Sesjon og budsjettår er forskjellige begreper.
- Alle vedtak skal bevares med tekst og kildehenvisninger. Bevilgningsvedtak skal gi strukturerte opplysninger om budsjettår, kapittel, post og beløp.
- Nye og endrede vedtak skal kontrolleres daglig.
- Opprinnelig budsjett, revidert budsjett, nysaldering og øvrige bevilgningsendringer gjennom året inngår.
- Vedtak uten regjeringsproposisjon skal fanges opp. Rene lovforslag kan utelates; bevilgningsendringer i saker som også inneholder lovforslag, skal med.
- Tilhørende fullmakter og øvrige tekstvedtak inngår. Detaljeringsnivået for strukturering av fullmakter gjenstår å avklare.
- Excel er bekreftet som et første uttrekksformat. Omfanget av søk og visning i første leveranse gjenstår å avklare.

## Regler for budsjettall og datakvalitet

Brukerens klassifikasjonsregel er:

- Kapittelnummer under 3000: utgift.
- Kapittelnummer fra og med 3000: inntekt.

Klassifikasjonen skal utledes fra kapittelnummeret. Et ukjent eller ugyldig kapittel må avklares før klassifikasjon.

Tvetydige beløpsuttrekk skal bevares med originalkilden og legges til manuell kontroll. De skal holdes utenfor godkjente analysetall. Uavklarte opplysninger og manglende dekning skal være synlige.

## Senere kilder og analyse

Den samlede løsningen skal inneholde regjeringens bevilgningsforslag, komiteenes forslag og endringer, endelige vedtak og kapittel- og postomtale fra proposisjoner og innstillinger.

Første leveranse har vedtaksinnlesning som kjerne. Regjeringsforslag kan inkluderes dersom en enkel kildevei dokumenteres og ikke forsinker dette arbeidet. Brukeren opplyser at automatisk uthenting fra regjeringen.no er krevende; kildevei og tilgjengelighet er ikke kontrollert i prosjektet. Manuell import fra en annen kilde er et alternativ som må avklares ved senere kildeintegrasjon.

Visning 1 skal støtte utvalg på departement, kapittel, post og kombinasjoner av disse. For hvert budsjettgrunnlag skal den vise:

- Beløp i regjeringens forslag, proposisjonsnummer og kilde.
- Beløp i komiteens innstilling, innstillingsnummer og kilde.
- Vedtatt beløp, identifikasjon av stortingsvedtaket og kilde.

Manglende forslag eller innstillinger i første leveranse skal fremgå som manglende datagrunnlag.

Brukerens eksempel med kapittel 100 post 1 og beløpet 4 996 819 000 kroner illustrerer ønsket kobling mellom beløp og proposisjon. Det er ikke et kontrollert kildefunn eller et godkjent testgrunnlag.

Eldre sesjoner og brukerens eksisterende historiske data skal kunne innarbeides senere.

## Fullstendighet

Målet er uttømmende dekning av bevilgningsendringer. Dekning skal dokumenteres gjennom avstemming mot et uavhengig kontrollgrunnlag. Kontrollgrunnlaget og akseptansekriteriene må avklares. En vellykket API-forespørsel dokumenterer ikke alene fullstendig dekning.

## Drift og mottakersystem

Mottakersystemet er ikke bestemt. Azure er en mulig driftsplattform. Drift er fleksibel fordi innholdet er offentlig. Azure skal vurderes med brukeren på nytt før plattformvalget blir styrende for arkitektur eller driftssetting. Ingen skyressurser skal opprettes som del av planleggingen.

## Beslutninger som gjenstår

- Første leveranses grense mellom innlesning, Excel-uttrekk og visuelt grensesnitt.
- Hvordan visningen skal skille opprinnelig bevilgning, endringsbeløp og gjeldende bevilgning.
- Hvilke budsjettår som omfattes ved første sesjonsimport, og hvordan innlesningen videreføres over sesjonsskifter.
- Departementstilknytning ved omorganisering og overføring av kapitler.
- Strukturering av fullmakter i første leveranse.
- Manuell kontroll, godkjenning og retting i praksis.
- Kontrollgrunnlag for fullstendighet.
- Tidspunkt for kjøring, feilvarsling og senere driftsvalg.
- Senere import av historiske data.

Tekniske fakta undersøkes av agenten. Brukeren avgjør behov, prioriteringer og aksept.
