# B9: Historikk som hovedvisning

B9/#30 endrer Excel-presentasjonen i det uttrykkelige B8-uttrekket. Arbeidsboken åpner på **Historikk**, som er første ark og har nøyaktig 13 kolonner. Bruk samme offentlige kommandoer og saksutvalg som i [B8-veiledningen](b8-saksdokumenter.md). Velg alltid et nytt filnavn. Ingen nye databasefelt, parserregler, aktiveringer eller JSON-versjoner innføres.

| Kolonne | Grunnlag og betydning |
| --- | --- |
| Kapittelnummer | Den valgte kildeobservasjonens kapittel. |
| Postnummer | Den valgte kildeobservasjonens post. |
| Kapittelnavn | Kildens `chapter_name`, uten oppslag i dagens register. |
| Postnavn | Kildens `purpose`, med forsiktig utskilling av dokumenterte stikkord og terminale handlingsord. |
| Stikkord | Den eksplisitt valgte B8-berikelsen. Manglende eller uavklart tolkning står synlig. |
| Dato | Kildeobservert vedtaksdato, som Excel-datocelle med format `dd.mm.yyyy`. |
| Vedtaksnummer | Formelt nummer med sesjon, eksempelvis `210 (2024-2025)`. Teknisk API-ID står i detaljfanen. |
| Innstillingsnummer | Alle valgte henvisninger av typen innstilling på saksnivå. |
| Proposisjon | Alle valgte proposisjonshenvisninger på saksnivå. |
| Beløp før vedtak | Entydig kildeobservert `for_belop` i kroner. |
| Vedtatt endring | Entydig kildeobservert `endring` i kroner. |
| Beløp etter vedtak | Entydig kildeobservert `etter_belop` i kroner. |
| Kontrollstatus | Lesbare mangler, avvik, faglig kontroll og ferskhet fra den fryste lokale vurderingen. |

Beløpene vises som numeriske hele kroner, med `kr` i celleformatet. Manglende før-, endrings- eller etterbeløp gir tom celle og forklaring. Observert null forblir numerisk null. Det beregnes ingen saldo i disse tre kolonnene. Et generelt `nivaa` omdøpes ikke til et etterbeløp: verdien og betydningen står i Kontrollstatus og beholdes i detaljfanen. Førbeløp i kilden er fortsatt ikke et faglig godkjent historisk startgrunnlag.

Ulike revisjoner, tolkninger, budsjettår, omfang, valuta/enhet, detaljeringsnivåer og komponenter holdes adskilt. Gjentatte kildebeløp med samme rolle blir ikke summert eller valgt vilkårlig: hovedcellen er tom og avviket forklares. Visningen gir ingen additiv totalsum eller ny faglig godkjenning. Kontrollstatus opplyser om blant annet manglende start, register- og kontrollgrunnlag, uavklart stikkord, lokale kildeferskheter og globale avvik før filtre. Nye avvikskoder har synlig tekstlig reservevisning.

Navnerensingen fjerner bare de kjente terminale uttrykkene «, økes med», «, reduseres med» og de dokumenterte tilsvarende variantene. Kjente stikkord fjernes bare når de finnes i den eksakte formålsraden i valgt berikelse. Uavklart resttekst beholdes. Manglende eller motstridende kildenavn vises som uavklart; dagens kontoplan brukes aldri til å fylle hullet. Full råtekst og kildepekere er bevart.

En enkelt dokumenthenvisning har direkte klikkbar metadata-URL. Flere henvisninger vises samlet i samme celle med lenke til **Saksdokumenter**, der hver referanse har sin egen klikkbare URL. Flere dokumenter gir aldri flere beløpsrader eller flere hovedkolonner. Saksrelasjon er ingen bevist postvis forslagstilknytning; dette står i Kontrollstatus. Dokumentinnhold og faktisk tilgjengelighet er fortsatt ikke kontrollert av eksporten.

**Historikkdetaljer** er den tidligere B8-historikken, synlig og med alle sine 39 kolonner for 210-prøven. Flere dokumenter utvider fortsatt dokumentkolonnene i denne reservefanen. Budsjettår, sesjon, underpost, detaljnivå, alle rå/korrigerte/effektive/godkjente beløpsvarianter, observasjons-ID-er, lokatorer, kildehash, revisjon, tolkning og avvik beholdes. Lange felt fortsetter i navngitte videreføringsark med korrigerte cellepekere. Øvrige kilde-, dokument-, kontroll- og dekningsark består.

Når filteret ikke gir beløpsrader, viser Historikk én uttrykkelig statusrad med tomme konto-/beløpsceller og globale avvik/ferskhet. Den er ingen beløpshendelse. Inventaret og avvik utenfor filtre beholdes i sine opprinnelige ark. Kontrollstatus lenker til **Avvik**.

Eksporten bruker bare en allerede frosset `SaksReport`, inkludert dens eksakte kildeobservasjoner og valgte berikelser. Også et tidligere `b6-frozen-2`-snapshot kan få den nye Excel-visningen uten tilgjengelig database, historisk Excel, register eller startsaldo. Rapport-ID, JSON-innhold og gamle B1–B7-eksportvalg er uendret. [Kontrollrapporten](research/b9/README.md) beskriver faktisk gjenlesing, kildebevis og begrensninger. #10s utsatte driftsaksept består.

`verify_saks_excel` kan fortsatt kontrollere tidligere B8-filer med den opprinnelige detaljerte Historikk og Sesjonsgrunnlag først, uten å skrive om filen. For denne gamle visningen forventes B8s opprinnelige videreføringspekere fra før innsetting av dokumentkolonner; teksten kontrolleres fortsatt mot feltets faktiske sluttplassering. Den [frosne kompatibilitetsprøven](../tests/fixtures/b9/README.md) er skrevet av den opprinnelige B8-eksporten. Nye B9-filer krever de flyttede pekerne og kontrolleres i tillegg for hovedvisning, dato-/kroneformat og dokumentlenker. Hele hovedteksten gjenbygges fra hovedcellen og alle videreføringer og sammenlignes med det frosne grunnlaget. Hoved- og detaljfanenes videreføringer kontrolleres for forventet arknavn, overskrifter, cellepekere, delnummer, rekkefølge og full tekst. Manglende eller ekstra videreføringsark/-rader/-kolonner og tekst lagret som formler avvises.
