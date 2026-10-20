# Arbeidsflyt med issues

Arbeidet følger en issuebasert prosess med avklaringer før bygging. Grilling-metoden brukes til å avklare beslutninger i runder. Prosessen under er prosjektets foreslåtte arbeidsflyt; detaljer fastsettes når avklaringene er avsluttet.

## Fra behov til gjennomføring

1. Avklar formål, avgrensning, prioriteringer og aksept med brukeren.
2. Samle bekreftede krav i en overordnet kravissue med henvisning til dokumentasjonen.
3. Bruk avgrensede undersøkelsesissues til usikre kilde- og dataspørsmål.
4. Del godkjente krav i små leveranser som kan kontrolleres samlet. Hver byggeticket skal gi et etterprøvbart resultat.
5. Angi avhengigheter og hvilke tickets som er startklare.
6. Gjennomfør én byggeticket på egen branch med én pull request. Beskriv problem, endring og relevante kontroller.
7. Gjennomgå endringen mot både krav og kodestandarder. Kjør relevante tester og CI før sammenslåing.
8. Oppdater dokumentasjon og lukk issuet når akseptansekriteriene er oppfylt.

## Innhold i en byggeticket

- Problem og ønsket resultat.
- Kobling til overordnede krav.
- Avgrensning og berørte deler.
- Avhengigheter.
- Observerbare akseptansekriterier.
- Relevante dataprøver og kontrollopplegg.
- Eventuelle beslutninger som må være tatt før start.

Overordnede kravissues gir kontekst. De skal ikke brukes som uavgrensede byggetickets. Foreslåtte tickets og åpne spørsmål innebærer ikke at implementeringen er startet.

## Første planleggingsissues

Opprett en overordnet kravissue, en kildeundersøkelse for fullstendig bevilgningsdekning og en avklaring av første leveranse. Byggetickets konkretiseres etter at brukeren har bekreftet den samlede forståelsen.
