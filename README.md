# Budsjetthistorikk

Budsjetthistorikk skal gi Finansavdelingen i Finansdepartementet grunnlag for analyser og uttrekk av historiske budsjettforslag og budsjettvedtak.

Prosjektet har to adskilte deler:

- **Innlesning fra Stortinget:** hente, bevare og strukturere endelige vedtak og deres kilder.
- **Fremstilling av budsjetthistorikk:** søk, sammenligning, analyse og uttrekk fra det strukturerte datagrunnlaget.

Innlesningen skal kunne kjøres uten analysegrensesnittet. En dokumentert datakontrakt skal knytte delene sammen.

## Første leveranse

Første leveranse gjelder endelige stortingsvedtak fra sesjonen 2026–2027, også vedtak om budsjettet som foreslås i Prop. 1 S (2026–2027). Nye og endrede vedtak skal kontrolleres daglig. Budsjettår, kapittel, post og beløp skal struktureres. Både inntekter og utgifter inngår.

Alle bevilgningsendringer skal fanges opp, også i saker uten regjeringsproposisjon og i sammensatte lov- og budsjettsaker. Tvetydige uttrekk skal bevares og sendes til kontroll før de inngår i godkjente analysetall.

Regjeringens forslag og komitéforslag er egne fremtidige kilder. Regjeringsforslag kan tas inn tidlig dersom en enkel kildevei blir dokumentert; dette skal ikke forsinke vedtaksinnlesningen. Manuell innlesning er et mulig senere alternativ.

## Fremtidig analyse

Brukeren skal kunne velge departement, kapittel, post og kombinasjoner av disse. Visningen skal sammenstille beløp i regjeringens forslag, komiteens innstilling og endelig vedtak, med dokumentnummer og kildehenvisning for hvert ledd. Første uttrekk skal kunne leveres til Excel.

Eldre sesjoner, eksisterende historiske data og kapittel- og postomtale skal kunne innarbeides senere.

## Dokumentasjon og arbeidsmetode

- [Krav og åpne beslutninger](docs/krav.md)
- [Ansvarsdeling](docs/ansvarsdeling.md)
- [Kilder og behov for dataprøver](docs/kilder.md)
- [Fast arbeidsflyt med issues](docs/arbeidsflyt.md)
- [Innlesningsdelen](innlesning/README.md)
- [Analysedelen](analyse/README.md)

## Status

Avklaringer og planlegging pågår i issues #1–#3. Ingen produksjonskode eller daglig kjøring er implementert. Teknologistakk og mottakersystem er åpne. Azure er en mulig driftsplattform; valget skal tas opp igjen før det blir styrende for løsningen.
