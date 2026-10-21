# Godkjent første leveranse og ticketoppdeling

Spesifikasjonen, testgrensene og oppdelingen ble godkjent av prosjekteieren 20. oktober 2026. Byggetickets er publisert som #4–#10. Kildeundersøkelsen #2 er levert i PR #11 med [akseptmatrise og byggegrense](research/issue-2/byggestart.md). De tre historiske kildekonfliktene gir ikke godkjent additiv historikk, men er avgrenset og har eksplisitte kontrollkrav. Python, SQLite og openpyxl og byggemandatet for B1 (#4) er godkjent. B1 har et implementert vertikalt snitt for ett opprinnelig vedtak; videre oppstart følger ticketenes avhengigheter og mandat. Se [arbeidsflyten](arbeidsflyt.md).

## Første leveranse

Endelige stortingsvedtak fra sesjonen 2026–2027 skal hentes, bevares, struktureres og lagres. Bevilgningshistorikk leveres som kontrollerbart Excel-uttrekk med kilder og synlige avvik. Daglig kjøring planlegges kl. 06.00 i Europe/Oslo.

Regjeringsforslag, komitéforslag, regnskap, eldre sesjonsimport, avansert fullmaktsstrukturering og interaktivt grensesnitt er senere utvidelser. Vedlagt Gul bok-fil kan gi katalogmetadata, med tydelig skille fra vedtakstall.

## Publiserte leveranser

| ID | Leveranse | Blokkert av | Kontrollerbart resultat |
| --- | --- | --- | --- |
| U1 / #2 | Kildeprøver og kontrollgrunnlag, eksisterende issue #2 | Ingen; oppstart er bestilt | Reproduserbare vedtaksprøver, beløpsenheter og forslag til avstemming |
| B1 / #4 | Ett endelig bevilgningsvedtak fra kilde til lagring og Excel | U1 | Original kilde, alle åtte postlinjer i den valgte prøven og sporbar eksport fungerer samlet |
| B2 / #5 | Nye vedtak og kilderettelser uten dubletter | B1 | Gjentatt og avbrutt kjøring bevarer ID-er, kilderevisjoner og korrekte kjørerapporter |
| B3 / #6 | Følg postens opprinnelige bevilgning og senere endringer | B1 | Endringsvedtak, fra-/til-beløp og beregnet gjeldende bevilgning kan kontrolleres uten dobbeltelling |
| B4 / #7 | Særkapitler, inntekt, nettoresultat og underliggende spesifikasjon | B1 | Representative særtilfeller går fra kilde til korrekt klassifikasjon og Excel, også med negativt beløp og post 90–99 |
| B5 / #8 | Vedlikehold register og behandle uavklarte uttrekk | B1 | Excel-/CSV-endringer og kontrollstatus kan importeres og brukes på nytt med sporbarhet, uten å endre originalkilden |
| B6 / #9 | Samlet sesjonsuttrekk med departementsutvalg og dekningsrapport | B2, B3, B4, B5 | Alle aktuelle vedtak inventeres; eksport viser historikk, kilder og uavklarte/manglende deler, med avstemming |
| B7 / #10 | Daglig kjøring og videreføring over sesjonsskifte | B6 | Kjøring kl. 06.00, tidssone, sesjonsskifte, gjenopptak og GitHub-varsling uten dupliserte feilissues er demonstrert |

Hver byggeticket skal beskrive en smal, komplett funksjon gjennom nødvendige lag. Tabellen er ikke en oppdeling i bare database, parser og grensesnitt. Endelig størrelse vurderes etter U1. En for stor leveranse deles før oppstart.

B1 omfatter bare et representativt første tilfelle. Det ferdige systemet skal håndtere alle aktuelle kildelinjer eller gjøre manglene eksplisitte. Godkjente summer skal ikke skjule uavklarte beløp.

## Aksept for første leveranse

- Endelige vedtak fra sesjonen 2026–2027 kan leses inn, lagres og spores til originalkilden; nye sesjoner kan følges videre.
- Godkjente bevilgningslinjer viser budsjettår, kapittel, post, beløpsbetydning og vedtaksidentitet. Hver opprinnelige bevilgning og senere endring bevares.
- Gjentatt kjøring og kilderettelser fører ikke til dobbeltelling eller tap av kildehistorikk.
- Utgifter, inntekter, særkapitler, nettoresultater og underliggende spesifikasjon klassifiseres og telles korrekt. Fullmaktsrammer og regnskap summeres ikke inn som bevilgning.
- Excel-uttrekk støtter departements-/kapittel-/postutvalg og viser kilder, endringer og synlige mangler. Manglende grunnlag gir ikke en tilsynelatende komplett sum.
- Excel-/CSV-basert registervedlikehold og manuell kontroll kan gjenbrukes med sporbarhet. Utdaterte korreksjoner oppdages når kilden endres.
- Kjørerapport og GitHub-issue viser feil og uavklarte uttrekk. Gjentakelser oppdaterer samme issue; vellykkede kjøringer uten avvik gir ingen nye issues.
- Kjøring kl. 06.00 i Europe/Oslo er demonstrert i avtalt driftsmiljø. Koden alene regnes ikke som produksjonssatt daglig jobb.
- Kildeinventar og uavhengig avstemming dokumenterer dekningsgraden. Åpne avvik skal være synlige; leveransen kan ikke erklæres uttømmende før relevante mangler er avklart.

## Godkjente testgrenser

- Deterministiske faglige tester på lagrede kildeprøver: beløpsenheter, økes/reduseres, fra/til, nettoresultat, underposter og fullmaktsrammer.
- Klassifikasjonstester ved inntektsgrensen og eksplisitte oppslag for særserier. Konti 6000–9999 holdes utenfor bevilgningskapitlene.
- Integrasjonskontroll fra kilde til lagring, ny kjøring, rettelse, kontrollstatus og eksport.
- Live kildekontroll adskilt fra deterministisk CI, slik at en utilgjengelig nettside ikke skjules som feil i fagreglene.
- Excel-uttrekk avstemmes mot godkjente beløpslinjer og viser uavklarte eller ufullstendige beregninger.
- Sesjonsinventar og uavhengige kontrollkilder prøves før fullstendig dekning erklæres.

Disse testgrensene inngår i den godkjente spesifikasjonen. Konkrete kildeprøver og uavhengige kontrollkilder velges i U1 og dokumenteres før byggetickets gjennomføres. Nye produktvalg skal ikke skjules som tekniske testbeslutninger.

## Avklaringer før bygging

Excel-/CSV-filer er bekreftet arbeidsflate for manuelt vedlikehold og kontroll. GitHub-issues er bekreftet varslingskanal ved feil og uavklarte uttrekk. Gjentakelser oppdaterer samme issue; vanlige vellykkede kjøringer gir bare rapport.

Python, SQLite og openpyxl er valgt etter U1 for lokal innlesning og uttrekk, jf. [ADR 0001](adr/0001-lokal-innlesning.md). Eieren valgte 21. oktober 2026 en varig Windows-vert med lokal lagring for B7. Konkret vert, driftskonto, datamappe og eksisterende bakgrunnstilgang er utsatt av eieren. Kode og reviewbart oppsett leveres med [driftsmanual](b7-drift.md) og [deterministisk kontrollrapport](research/b7/README.md); faktisk oppgaveinstallasjon og driftsprøve gjenstår. #10 forblir åpen til dette er akseptert. Ingen produksjonsressurser eller daglig jobb er opprettet. Materielle endringer i omfang, testaksept eller ticketoppdeling legges frem på nytt før videre bygging. Endelig mottakersystem for felles bruk er fortsatt åpent.

## Relasjoner i GitHub

Publiseringsverktøyet støtter ikke skriving av native sub-issue- og avhengighetsrelasjoner. Ticketene har derfor eksplisitte «Del av #1» og «Blokkert av #N» i teksten. Oversikten i #1 samler ticketene. Dette er tekstlige relasjoner, ikke native GitHub-blokkeringer.
