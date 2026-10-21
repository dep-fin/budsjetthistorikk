# ADR 0007: Eksplisitt sesjonssammenstilling uten nytt tilstandshode

Valgt for B6/#9, 21. oktober 2026. B2 kjenner kildeinventaret, B3/B4 har immutable tolkninger, og B5 har uttrykkelig aktivering og faglig godkjenning. Et nytt automatisk «siste godkjente sesjonsresultat» ville kunne gjenbruke eldre godkjenninger etter avvisning, bytte historisk register eller miste vedtak uten beløpsuttrekk.

Analysen leser derfor et eksplisitt utvalg av lagrede inventarjobber, uttrekk, kontrollresultater og eventuelle historikkberegninger. Hovedsesjon og supplerende inngående kilder fra andre sesjoner har separate dekningsrader. Inventaret behandles globalt før beløpsfiltre. Ikke-valgte kjente ID-er, fravær, nyere forsøk og alternative revisjoner blir synlige avvik. En ny offentlig B2-leser samler inventar og kildeoverganger i ett snapshot. B6 avviser en sammenstilling dersom databasen endres under lesing.

Rapporten er en datert vurdering av uforanderlige inn-data med separat aktuell ferskhet. Ingen ny SQL-tabell, skjemaversjon eller resultataktivering innføres. Dette er valgt fremfor et persistert B6-hode, som ville krevd en ny ugyldiggjøringsmodell ved alle kilde-/register-/tolknings-/kontrolloverganger. Utvalgs-JSON, rapportgrunnlag og eksisterende resultat-ID-er følger Excel-filen og bevarer grunnlaget for gjentatt eksport.

Aktuelle godkjente enkeltverdier må komme fra et valgt, gjeldende B5-resultat og den eksakte faglige avgjørelsen. Nyere avvisning/til kontroll, endret aktivering eller kildeovergang sperrer dem; historiske effektive verdier beholdes merket. Teknisk B3-avstemming kan ikke oppfylle faglig godkjenning. Konservative kontroller av start, lokal aritmetikk og kjedekonflikter brukes bare som sperrer mot komplette summer, aldri til å konstruere nye kildebeløp eller lagre nye B3-beregninger.

Rå-, B5- og kjedeavvik samles fra ufiltrert observasjonsgrunnlag og bevares med filterstatus. Kjedekontrollen mister dermed ikke inngående grunnlag eller konflikter ved beløpsfiltrering. Et filtrert uttrekk gir bare en uttrykkelig delsum; globale avvik kan aldri skjules bak en komplett filtersum.

Avstemming har en validert modell for budsjettår, periode, beløpsbegrep, nivå, valuta/enhet og konto. Referanser har forventet verdi eller uttrykkelig fravær samt kildehash/lokator/begrunnelse. Unionen av nøklene bevares. En separat, hashfestet reproduksjon av 2024-undersøkelsen leser bevarte råfelt og gjentar DFØ-/Løyving-/Blå bok-kontrollene. Dette er valgt fremfor å kopiere forskningsrapportens tidligere kontrollprosent eller å innføre en generell regnskapsadapter i B6.

Excel bruker eksisterende tekstsikker skriving og videreføring av lange felt. Faktiske beløpsceller/ID-er leses tilbake før publisering. Midlertidig fil publiseres atomisk uten overskriving av et eksisterende mål. B6 erklærer ingen automatisk uttømmende faglig sesjons-/årsdekning; gjenværende kilder, strukturering, kontroller og historiske konflikter fremgår.
