# Foreslått første leveranse og ticketoppdeling

Dette er et utkast til oppdeling, basert på brukerens avklaringer og vedleggene. Byggetickets er ikke publisert, og implementeringen er ikke startet. Oppdelingen skal gjennomgås med brukeren før publisering, jf. [arbeidsflyten](arbeidsflyt.md).

## Første leveranse

Endelige stortingsvedtak fra sesjonen 2026–2027 skal hentes, bevares, struktureres og lagres. Bevilgningshistorikk leveres som kontrollerbart Excel-uttrekk med kilder og synlige avvik. Daglig kjøring planlegges kl. 06.00 i Europe/Oslo.

Regjeringsforslag, komitéforslag, regnskap, eldre sesjonsimport, avansert fullmaktsstrukturering og interaktivt grensesnitt er senere utvidelser. Vedlagt Gul bok-fil kan gi katalogmetadata, med tydelig skille fra vedtakstall.

## Foreslåtte leveranser

| ID | Leveranse | Blokkert av | Kontrollerbart resultat |
| --- | --- | --- | --- |
| U1 | Kildeprøver og kontrollgrunnlag, eksisterende issue #2 | Ingen; faglig omfang må bekreftes | Reproduserbare vedtaksprøver, beløpsenheter og forslag til avstemming |
| B1 | Ett endelig bevilgningsvedtak fra kilde til lagring og Excel | U1 | Original kilde, én representativ strukturert beløpslinje og sporbar eksport fungerer samlet |
| B2 | Nye vedtak og kilderettelser uten dubletter | B1 | Gjentatt og avbrutt kjøring bevarer ID-er, kilderevisjoner og korrekte kjørerapporter |
| B3 | Følg postens opprinnelige bevilgning og senere endringer | B1 | Endringsvedtak, fra-/til-beløp og beregnet gjeldende bevilgning kan kontrolleres uten dobbeltelling |
| B4 | Særkapitler, inntekt, nettoresultat og underliggende spesifikasjon | B1 | Representative særtilfeller går fra kilde til korrekt klassifikasjon og Excel, også med negativt beløp og post 90–99 |
| B5 | Vedlikehold register og behandle uavklarte uttrekk | B1 | Manuell korrigering og kontrollstatus kan brukes på nytt med sporbarhet, uten å endre originalkilden |
| B6 | Samlet sesjonsuttrekk med departementsutvalg og dekningsrapport | B2, B3, B4, B5 | Alle aktuelle vedtak inventeres; eksport viser historikk, kilder og uavklarte/manglende deler, med avstemming |
| B7 | Daglig kjøring og videreføring over sesjonsskifte | B6 | Kjøring kl. 06.00, håndtering av tidssone, sesjonsskifte, gjenopptak og avtalt feilvarsling er demonstrert |

Hver byggeticket skal beskrive en smal, komplett funksjon gjennom nødvendige lag. Tabellen er ikke en oppdeling i bare database, parser og grensesnitt. Endelig størrelse vurderes etter U1. En for stor leveranse deles før oppstart.

B1 omfatter bare et representativt første tilfelle. Det ferdige systemet skal håndtere alle aktuelle kildelinjer eller gjøre manglene eksplisitte. Godkjente summer skal ikke skjule uavklarte beløp.

## Foreslåtte testgrenser

- Deterministiske faglige tester på lagrede kildeprøver: beløpsenheter, økes/reduseres, fra/til, nettoresultat, underposter og fullmaktsrammer.
- Klassifikasjonstester ved inntektsgrensen og eksplisitte oppslag for særserier. Konti 6000–9999 holdes utenfor bevilgningskapitlene.
- Integrasjonskontroll fra kilde til lagring, ny kjøring, rettelse, kontrollstatus og eksport.
- Live kildekontroll adskilt fra deterministisk CI, slik at en utilgjengelig nettside ikke skjules som feil i fagreglene.
- Excel-uttrekk avstemmes mot godkjente beløpslinjer og viser uavklarte eller ufullstendige beregninger.
- Sesjonsinventar og uavhengige kontrollkilder prøves før fullstendig dekning erklæres.

Testgrenser og kontrollgrunnlag må inngå i den bekreftede spesifikasjonen før de brukes som leveranseaksept.

## Beslutninger før gjennomføring

Arbeidsflaten for manuelt vedlikehold og kontroll, varslingskanal og teknologistakk må fastsettes. Azure tas opp igjen før plattformvalget blir styrende. Ingen produksjonsressurser eller daglig jobb er opprettet som del av planleggingen.
