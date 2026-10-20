# Kilder og behov for dataprøver

## Viktige funn før kildevalg

Les [varige kildefunn](kildefunn.md) før innlesning og dekningskontroll. Der er bevisene og kontrollkravene for bevilgningsendringer av typen ANNET samlet.

## Dokumenterte kilder

- [Vedtak](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/): sesjonsvis oversikt med ID, sak, dato, type og tekst. Budsjettvedtak har egen type. Teksten er ofte HTML; separate felt for kapittel, post og beløp er ikke dokumentert.
- [Voteringsvedtak](https://data.stortinget.no/dokumentasjon-og-hjelp/voteringsvedtak/): vedtak knyttet til en votering. Voteringsdata er tilgjengelige fra sesjonen 2011–2012.
- [Sak](https://data.stortinget.no/dokumentasjon-og-hjelp/sak/): saksopplysninger og dokumentkoblinger.
- [Publikasjoner](https://data.stortinget.no/dokumentasjon-og-hjelp/publikasjoner/) og [publikasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/publikasjon/): publikasjonshenvisninger og fulltekst.
- [Kommentar til voteringsdata](https://data.stortinget.no/dokumentasjon-og-hjelp/kommentar-til-datagrunnlaget-for-voteringer/): begrensninger ved voteringsgrunnlaget.

## Vedlagt faggrunnlag

Tre vedlegg er lest og analysert: R-101/2024, Statlig budsjettarbeid fra juni 2023 og Gul bok-datagrunnlaget for 2027. Se [faggrunnlaget](faggrunnlag.md) for kildefunn og [departementsregisteret](departementsregister.md) for kapittelkoblinger. Originalfilene er ikke lastet opp til repoet.

Gul bok-filen har 1 595 utfylte kapittel-/postrader og 579 kapitler. Den kan brukes som strukturert katalog- og forslagskilde. Den er ikke en vedtakskilde eller fasit for vedtatte beløp.

## Undersøkelser før valg av løsning

1. Kontroller at sesjonsoversikten dekker relevante vedtak, også bevilgningsendringer i sammensatte saker.
2. Undersøk som et avgrenset tillegg om regjeringsforslag har en enkel, tilgjengelig kildevei. Første leveranse skal kunne gjennomføres uten denne kilden. Omfattende uthenting fra regjeringen.no og manuell import planlegges som egne senere leveranser dersom det blir nødvendig.
3. Prøv uttrekk på opprinnelig budsjett, revidert budsjett, nysaldering, andre endringsproposisjoner og vedtak uten proposisjon.
4. Undersøk beløpsenheter, tabellstruktur, fortsettelsesrader, nye totalbeløp, endringsbeløp og romertallsvedtak.
5. Prøv koblinger mellom sak, proposisjon, innstilling, forslag, votering og endelig vedtak.
6. Undersøk publiseringsforsinkelser og rettelser. Vedtaksdato må ikke uten videre brukes som endringstidspunkt.
7. Prøv uavhengig avstemming mot blant annet Blå bok for opprinnelig vedtak og tilgjengelige bevilgningskolonner i senere kontrollkilder. Oppsummeringer er kontrollgrunnlag, ikke nye vedtak. Skill mellom kildeinventar, strukturering og godkjente analysetall.
8. Prøv post 24, underposter, negative nettoresultat, 90-poster, nye kapitler og kapitteltilknytning utenfor ordinære departementsserier.
9. Kontroller mot faktiske stortingskilder hvordan R-101/2024 og 2023-veilederens ulike beskrivelser av post 24 er representert. Bevar hierarkiet og unngå dobbeltelling uansett presentasjon.

Funnene skal skille mellom dokumenterte forhold, observerte dataprøver og forhold som fortsatt er uavklarte. Ingen dekningsgaranti kan utledes av dokumentasjonen alene.
