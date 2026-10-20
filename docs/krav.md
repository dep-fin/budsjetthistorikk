# Krav og åpne beslutninger

## Formål og brukere

Finansavdelingen i Finansdepartementet skal kunne analysere og hente ut informasjon om historiske budsjettforslag og budsjettvedtak. Løsningen skal bevare sammenhengen mellom kilde, forslag, komitébehandling og endelig vedtak.

## Bekreftede krav

1. Ett privat repo: `depmartin/budsjetthistorikk`, med dokumentasjon og issues på norsk.
2. Tydelig skille mellom innlesning og fremstilling av budsjetthistorikk.
3. Første trinn skal lese inn alle vedtak med tekst og kildehenvisninger og strukturere budsjettår, kapittel, post og beløp fra bevilgningsvedtak.
4. Nye og endrede vedtak skal kontrolleres daglig.
5. Første innlesning starter i sesjonen 2026–2027, herunder Prop. 1 S (2026–2027). Stortingssesjon og budsjettår skal behandles som forskjellige begreper.
6. Budsjettomfanget omfatter opprinnelig budsjett, revidert budsjett, nysaldering og alle øvrige tilleggsproposisjoner og endringer gjennom året.
7. Bevilgningsvedtak som springer ut av representantforslag, komitéinitiativ eller andre saker, skal med også uten regjeringsproposisjon.
8. Rene lovforslag kan utelates. Bevilgningsendringer i saker som også inneholder lovforslag, skal fanges opp.
9. Tilhørende fullmakter og øvrige tekstvedtak inngår i budsjettomfanget.
10. Den samlede løsningen skal inneholde regjeringens bevilgningsforslag, komiteenes forslag og endringer, endelige vedtak og kapittel- og postomtale fra proposisjoner og innstillinger.
11. Eldre sesjoner og brukerens eksisterende historiske data skal kunne innarbeides senere.
12. Mottakersystemet er ikke bestemt.

## Fullstendighet

Målet er uttømmende dekning av bevilgningsendringer. Fullstendighet skal dokumenteres gjennom avstemming mot et uavhengig kontrollgrunnlag og tydelige kriterier. Hvilket kontrollgrunnlag som skal brukes, er åpent. En vellykket API-forespørsel dokumenterer ikke alene fullstendig dekning.

## Beslutninger som gjenstår

- Om proposisjonsforslag og komitéforslag skal struktureres i første leveranse eller i påfølgende leveranser.
- Første prioriterte analyser og uttrekk.
- Behandling av uavklarte og tvetydige budsjettall før de kan brukes i analyser.
- Hvilke beløpsbegreper, inntekter, underposter og fullmakter som trenger egne strukturer.
- Driftsmiljø, datalagring, tilgang, tidspunkt for kjøring og feilvarsling.
- Kontrollgrunnlag og akseptanse for fullstendighet.
- Håndtering av historiske korreksjoner, omposteringer og endringer i kapittel- og poststruktur.
- Format, omfang og kvalitet i eksisterende historiske data.

Tekniske forhold som kan undersøkes i dokumentasjon eller data, avklares ved undersøkelser. Brukeren tar beslutninger om behov, prioritering og aksept.
