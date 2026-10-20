# Issue #2 – kildeundersøkelse av Stortingets API

Undersøkelsen er utført 20. oktober 2026. Dette er et dokumentert kandidatgrunnlag for senere B1-arbeid, ikke produksjonsimplementering. Alle konklusjoner nedenfor gjelder de lagrede svarene. Utforskeren bevarte råsvar, hentemetadata og kontrollskript som lokale mellomfiler. Orkestratoren publiserer rapporten og et avgrenset dataunderlag; kontrollskriptene er ikke produksjonskode og følger ikke med i repoet.

## Funn som påvirker videre arbeid

1. **Vedtaksteksten finnes faktisk i sesjonsendepunktet.** Begge prøvene ga HTTP 200 og gyldig XML med `versjon=1.6`, navnerom `http://data.stortinget.no`, vedtaks-ID, sak-ID, vedtaksnummer, dato, type og HTML som tekst i `stortingsvedtak_tekst`. Den ferdige sesjonen 2024–2025 ga 1 260 vedtak; 2026–2027 ga 24 vedtak på hentetidspunktet. Dokumentasjonen beskriver endepunktet som en oversikt over alle vedtak i en sesjon. Dette er ikke en uavhengig bekreftelse av fullstendighet. [Vedtak-dokumentasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/), [2024–2025](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [2026–2027](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2026-2027).
2. **`BUDSJETT` er utilstrekkelig som eneste filter.** Det opprinnelige budsjettvedtaket 40033944 er `BUDSJETT`, mens den konkrete bevilgningsendringen 40033805, nysalderingstabellen 40034287 og RNB-tabellen 40035422 alle er `ANNET`. Dette er observerte eksempler, ikke en uttømmende klassifikasjonsregel. [Sesjonens råkilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).
3. **Voteringsvedtak gir nyttige koblinger, men ingen tekst i de undersøkte prøvene.** Fire voteringsvedtak-svar omfatter 54 elementer; samtlige har `vedtak_tekst i:nil="true"`. Hovedendepunktets HTML bør derfor undersøkes som tekstkilde, mens voteringene brukes til sporing. Dette utelukker ikke at andre voteringsvedtak kan ha tekst. [23520](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23520), [23798](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23798), [26265](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=26265), [26266](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=26266).
4. **Samme vedtaksinnhold finnes flere steder.** Hele teksten for 40033805 finnes også i XML for Innst. 25 S og møtereferatet 5. november 2024 etter fjerning av alle blanktegn. Dette dokumenterer tekstoverlapp i denne prøven, ikke at kildene er uavhengige eller at alle vedtak gjentas identisk. [Innstilling](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-025s), [referat](https://data.stortinget.no/eksport/publikasjon?publikasjonid=refs-202425-11-05), [sesjonskilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).
5. **Beløp må tolkes sammen med tabellstrukturen og ordene.** Prøvene inneholder fra-/til-beløp på en egen rad, endringsbeløp i forskjellige tallkolonner, nye bevilgninger uten fra-/til-beløp, underposter med positive og negative beløp, summer og tekstfullmakter uten vedtatt beløp. En generell «siste tall i raden»-regel er ikke underbygget av prøvene. Se de konkrete prøvene nedenfor og [råkilden](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).

## Henting og kontroller

Python `urllib.request` hentet rå byte med 35 sekunders timeout, fast User-Agent og to sekunders pause etter hvert svar, én forespørsel om gangen. Ingen masseinnhenting eller parallell henting ble brukt. Stortinget oppgir en grense på 100 API-kall per minutt og HTTP 429 ved overskridelse. Ingen HTTP 429 ble observert. [Publisert API-grense](https://data.stortinget.no/nyhetsoversikt/begrensning-pa-api-kall/).

Første forsøk i standardmiljøet feilet med `URLError(gaierror(11001, 'getaddrinfo failed'))` kl. 11:34:24, 11:34:26 og 11:34:28 UTC. Webverktøyets fallback meldte at de to eksport-URL-ene og den forsøkte `/dokumentasjon/` ikke var tilgjengelige gjennom verktøyet. Tillatt kjøring med nettverksadgang hentet deretter API-svarene. Den feilaktige dokumentasjonsstien `/dokumentasjon/` svarte faktisk HTTP 404; korrekt dokumentasjon finnes under `/dokumentasjon-og-hjelp/`. Ingen råsvar ble lagret for DNS-feil eller 404. UTC-tidene i metadata er tidspunkt rett før forespørselen; HTTP `Date` og kildens `respons_dato_tid` er bevart separat.

Følgende kontroller er utført i et lokalt inspeksjonsskript. Resultatene er bevart i [API-kontrollresultatene](api-kontroller.json):

- Parsing av begge sesjoners XML og telling av vedtak, typer, unike ID-er, sak-ID-er, tomme tekstfelt og tekster med `<table`.
- Bytevis sammenligning av gjentatte svar før og etter at kun innholdet i `respons_dato_tid` ble erstattet med en fast markør.
- Kontroll av de oppgitte fra-/til-regnestykkene og summer av underposter i utvalgte post 24-tabeller.
- Kontroll av nil-tekst og vedtaksnummer i de fire voteringsvedtak-svarene.
- Tekstsammenligning av ett vedtak mot to publikasjoner etter fjerning av blanktegn, inkludert harde mellomrom. Ingen annen semantisk normalisering ble utført.

## Sesjonstelling og gjentatt henting

| Sesjon | Vedtak / unike ID-er | Unike sak-ID-er | Typer | Tomme tekster | HTML-tekster med tabell |
|---|---:|---:|---|---:|---:|
| 2024–2025 | 1 260 / 1 260 | 472 | ANMOD 485; ANNET 517; BUDSJETT 257; RO 1 | 0 | 154 |
| 2026–2027 | 24 / 24 | 3 | ANMOD 18; ANNET 6 | 0 | 1 |

Tallene er telling av elementer i de lagrede svarene, ikke telling av bevilgningslinjer. En HTML-tabell er ikke i seg selv en bevilgningstabell. Av de 154 vedtakstekstene med tabell i 2024–2025 er 62 klassifisert `ANNET`; `table_candidates.json` inneholder kandidatene. Datoene i den ferdige sesjonsprøven spenner fra 4. oktober 2024 til 20. juni 2025; i 2026–2027 fra 6. til 13. oktober 2026. [2024–2025](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [2026–2027](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2026-2027).

| Sesjon | Første henting UTC | Gjentatt henting UTC | Rå byte like? | Like etter bare tidsfeltnormalisering? |
|---|---|---|---|---|
| 2024–2025 | 11:34:46.321003 | 11:36:13.372089 | Nei | Ja |
| 2026–2027 | 11:34:44.011276 | 11:36:18.771517 | Nei | Ja |

De eksakte hentetidene skal leses fra manifestet nedenfor dersom avrundede eller manuelle tabelltider avviker. Hvert av sesjonssvarene har ett `respons_dato_tid`-element. For 2024–2025 gikk kildefeltet fra `2026-10-20T13:34:46.1397306+02:00` til `2026-10-20T13:36:13.2223874+02:00`; for 2026–2027 fra `2026-10-20T13:34:43.8900177+02:00` til `2026-10-20T13:36:18.5824977+02:00`. Etter at dette feltet var erstattet, var resten byteidentisk. Normaliserte SHA256 er henholdsvis `69c6c91f1501ff709f970fd32ac82832bc330ea8a081d589239d19c50003bcfa` og `6c3f8378461ad8b9c82efc2d86622bbcce1f3090bc63a8d45654f09e9edfbed4`. Begge endepunktene er oppført med separate råfiler og kilde-URL-er i manifestet.

Dette viser volatil responstid og uendret øvrig innhold mellom akkurat disse hentetidspunktene. Det viser verken en fremtidig rettelse, at eldre innhold aldri endres, eller komplett dekning av alle relevante budsjettvedtak.

## Dokumenterte koblinger og observerte ID-er

Dokumentasjonen gir kjeden `stortingsvedtak.sak_id` → `sak?sakid=…` og `voteringer?sakid=…` → `votering_id` → `voteringsvedtak?voteringid=…`. Vedtaksoversikten gir også URL-er til sak og vedtak. Et voteringsvedtak har vedtaksnummer, kode, kommentar, referanse og tekst; dokumentasjonen oppgir ikke et felt for hovedoversiktens store vedtaks-ID i dette svaret. [Vedtak](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/), [sak](https://data.stortinget.no/dokumentasjon-og-hjelp/sak/), [voteringer](https://data.stortinget.no/dokumentasjon-og-hjelp/voteringer/), [voteringsvedtak](https://data.stortinget.no/dokumentasjon-og-hjelp/voteringsvedtak/).

| Prøve | Hovedoversikt: ID / nummer / sak | Votering | Voteringsvedtak | Observert kobling |
|---|---|---|---|---|
| Enkel endring | 40033805 / 14 / 100001 | 23520, vedtatt, enstemmig | nummer 14, kode «Andre vedtak», nil-tekst | Sak og nummer samsvarer; store vedtaks-ID finnes i hovedoversikten |
| Opprinnelig budsjett og fullmakt | 40033944 / 113 og 40033945 / 114, sak 100215 | 23798 | to elementer, nummer 113 og 114, begge nil-tekst | Én votering gjelder flere vedtak |
| RNB | 40035422 / 1149 / 103529 | 26265 | 49 elementer med nummer 1149–1197, alle nil-tekst | Én votering dekker mange vedtak; hovedtabellen er ett av dem |
| RNB, ytterligere deler | samme sak 103529 | 26266 | nummer 1198 og 1199, begge nil-tekst | Flere voteringer må vurderes innen samme sak |

Kilder: [sak 100001](https://data.stortinget.no/eksport/sak?sakid=100001), [voteringer 100001](https://data.stortinget.no/eksport/voteringer?sakid=100001), [vedtak 23520](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23520), [voteringer 100215](https://data.stortinget.no/eksport/voteringer?sakid=100215), [vedtak 23798](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23798), [voteringer 103529](https://data.stortinget.no/eksport/voteringer?sakid=103529), [vedtak 26265](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=26265), [vedtak 26266](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=26266), [hovedoversikt](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).

Den undersøkte RNB-saken har 78 voteringsposter. API-et oppgir `votering_tema`, men dokumentasjonen sier at dette må sammenholdes med forslagsteksten for å forstå delene det stemmes over. Alle 54 vedtaksnumre lot seg entydig koble til én hovedoversikts-ID innen den angitte sesjonen og den aktuelle sak-ID-en. Denne lokale kontrollen beviser ikke generell unikhet. De fire voteringsvedtak-prøvene gir derfor ikke grunnlag for å påstå at en enkelt votering svarer til én bevilgningslinje. [RNB-voteringer](https://data.stortinget.no/eksport/voteringer?sakid=103529), [dokumentasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/voteringer/).

Sakens `publikasjon_referanse_liste` har `eksport_id` bare når publikasjonen er tilgjengelig for eksport. `publikasjon?publikasjonid=…` leverer publikasjons-XML i trykkeriformat, eller HTML ved `format=html`, og ikke JSON. I sak 100001 finnes eksport-ID-ene `inns-202425-025s` og `refs-202425-11-05`; regjeringens proposisjon har nil i `eksport_id`, men egen URL. [Sak-dokumentasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/sak/), [publikasjon-dokumentasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/publikasjon/), [faktisk sak](https://data.stortinget.no/eksport/sak?sakid=100001).

## Representative bevilgningsprøver

### Opprinnelig budsjett 2025

Vedtak **40033944**, nummer **113**, 13. desember 2024, sak **100215**, type `BUDSJETT`, innledes med bevilgning på statsbudsjettet for 2025. Tabellen har utgifts- og inntektsdel, kapittel på egne rader, poster på senere rader og to kolonner merket «Kroner». Det er beløpsnivåer, ikke fra-/til-/endringsbeløp. [Vedtakets publiserte URL](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033944&p=100215), [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [sak](https://data.stortinget.no/eksport/sak?sakid=100215).

| Del | Kap. | Post | Formål, forkortet | Vedtatt beløp i kroner |
|---|---:|---:|---|---:|
| Utgift | 42 | 1 | Driftsutgifter | 10 478 000 |
| Utgift | 42 | 75 | Internasjonale organisasjoner og nettverk | 250 000 |
| Utgift | 43 | 1 | Driftsutgifter | 118 311 000 |
| Utgift | 44 | 1 | Driftsutgifter | 49 986 000 |
| Utgift | 45 | 1 | Driftsutgifter | 31 322 000 |
| Utgift | 51 | 1 | Driftsutgifter | 669 959 000 |
| Utgift | 51 | 75 | Internasjonale organisasjoner og nettverk | 29 791 000 |
| Sum utgifter | | | | 910 097 000 |
| Inntekt | 3051 | 2 | Refusjon utland | 300 000 |
| Sum inntekter | | | | 300 000 |

Tallene er transkribert fra den ene tabellen i [API-vedtaket](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025); uttrekket finnes i `selected_tables.json` og den dekodede vedtaksteksten i `40033944.html`. Tabellen har `colspan=5` i deloverskrifter; det finnes derfor rader med annet antall fysiske celler enn kolonner.

### RNB 2025

Vedtak **40035422**, nummer **1149**, 20. juni 2025, sak **103529**, type `ANNET`, har en stor tabell med 1 426 HTML-rader i det enkle inspeksjonsuttrekket. Første endring gjelder kap. 20 post 1: fra **116 121 000** til **110 121 000** kroner, redusert med **6 000 000**. Kap. 21 post 1 økes fra **197 674 000** til **205 874 000**, med **8 200 000** kroner. Endringsbeløpene ligger her i den siste av to kroner-kolonner; fra-/til-beløp står på egen etterfølgende rad. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [publisert vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035422&p=103529).

Sak **103529** er `type=budsjett`, `dokumentgruppe=melding`, med Meld. St. 2 og Innst. 540 S i henvisningen. De konkrete bevilgningsvedtakene ligger altså på en sak hvor den direkte regjeringspublikasjonen er en melding. Dette er **ikke** en prøve som beviser et helt budsjettvedtak uten proposisjonsgrunnlag: saken har forbindelser til andre saker, og sak 103526 har blant annet `fellesinnst` til 103529 og 103528, sistnevnte med tittelen Tilleggsbevilgninger og omprioriteringer i statsbudsjettet 2025. [Sak 103529](https://data.stortinget.no/eksport/sak?sakid=103529), [sak 103526](https://data.stortinget.no/eksport/sak?sakid=103526).

### Nysaldering 2024

Vedtak **40034287**, nummer **428**, 19. desember 2024, sak **100289**, type `ANNET`, er Ny saldering av statsbudsjettet 2024. Den inneholder 239 HTML-rader i inspeksjonsuttrekket. Kap. 20 post 1 økes fra **107 671 000** til **109 677 000** med **2 006 000** kroner. Kap. 21 post 1 økes fra **192 299 000** til **201 399 000** med **9 100 000** kroner. Også her er fra-/til-beløp på egen rad. Sakens referanser er Prop. 36 S og Innst. 90 S (2024–2025), med eksport-ID `inns-202425-090s` og referat `refs-202425-12-19`. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [sak](https://data.stortinget.no/eksport/sak?sakid=100289).

Denne prøven og de opprinnelige/RNB-prøvene ovenfor ligger i samme stortingssesjon, men gjelder ikke alle samme budsjettår. Rapporten hevder derfor ikke å ha fulgt ett komplett budsjettår fra første til siste vedtak.

### Andre endringer og fravær av fra-/til-beløp

Vedtak **40033805**, nummer **14**, 5. november 2024, sak **100001**, type `ANNET`, øker kap. 2541 post 70 (dagpenger, overslagsbevilgning) med **400 000** kroner, fra **12 210 000 000** til **12 210 400 000**. Regnestykket stemmer. Tabellen har én kroner-kolonne og bare én endret post. Sakens egen `sak_sesjon` er **2023–2024**, mens innstillingen og vedtaket er fra 2024–2025; sesjon for opprinnelig sak og sesjon for vedtak må dermed holdes fra hverandre. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [sak](https://data.stortinget.no/eksport/sak?sakid=100001), [publisert vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033805&p=100001).

Vedtak **40034443**, nummer **526**, 25. mars 2025, sak **102001**, type `ANNET`, bevilger **454 000 000** kroner på ny kap. 900 post 32 til sjøfibersamband og reduserer kap. 1760 post 45 med **227 000 000** kroner. Denne tabellen har **ikke fra-/til-beløp** for noen av disse to radene. Fravær er dermed en faktisk observert variant, ikke et nettverksproblem. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [publisert vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034443&p=102001).

## Vanskelige beløps- og teksttilfeller

### Post 24, netto og underposter

Opprinnelig budsjettvedtak **40034067**, nummer **232**, sak **100186**, har kap. **2445 Statsbygg**, post **24 Driftsresultat**, med underposter i formålskolonnen og underpostbeløp i en egen tallkolonne:

| Underpost | Opprinnelig 2025, kroner | RNB 2025, kroner |
|---|---:|---:|
| 1 Driftsinntekter | −6 558 000 000 | −6 558 000 000 |
| 2 Driftsutgifter | 2 848 358 000 | 2 843 358 000 |
| 3 Avskrivninger | 1 655 000 000 | 1 655 000 000 |
| 4 Renter av statens kapital | 1 690 000 000 | 1 690 000 000 |
| Samlet driftsresultat | −364 642 000 | −369 642 000 |

I originaltabellen står resultatet i neste beløpskolonne på samme rad som siste underpost. I RNB-vedtak **40035422** har resultatet egen rad merket «Sum:». Ingen eksplisitt fra-/til-/endringsformulering står på disse post 24-radene i RNB-prøven. Summeringen er kontrollert. Differansen −5 000 000 er en **beregning fra de to prøvene**, ikke et eksplisitt endringsbeløp transkribert fra RNB-raden. Tallene dokumenterer den observerte nettostrukturen, men rapporten fastsetter ikke en generell regnskapsregel for alle post 24-vedtak. [Begge vedtak i API-kilden](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [original](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034067&p=100186), [RNB](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035422&p=103529).

En supplerende prøve er **40034231**, nummer **371**, sak **100198**, kap. **5440**, post **24**: underposter **300 310 000 000 − 42 600 000 000 − 2 000 000 000 − 32 100 000 000 − 4 900 000 000 = 218 710 000 000** kroner. Her er inntektene positive og kostnadskomponentene negative; tabellen har seks fysiske kolonner og deloverskrifter med `colspan=6`. For en senere parser er dette en konkret grunn til å bevare kolonneposisjon, fortegn og underpoststruktur. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034231&p=100198).

### 90-poster

Vedtak **40034278**, nummer **418**, sak **100236**, er `BUDSJETT` og inneholder faktiske 90-poster. I inntektsdelen er kap. **5310 post 90** (redusert lån og rentegjeld) **14 754 325 000**, kap. **5310 post 93** (omgjøring av utdanningslån til stipend) **8 651 746 000**, og kap. **5999 post 90** (lån) **176 336 383 000** kroner. Prøven er et beløpsgrunnlag for 90-poster; den er ikke grunnlag for å blande dem inn i andre utgifts-/inntektssummer uten en separat økonomisk avgrensning. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034278&p=100236), [sak](https://data.stortinget.no/eksport/sak?sakid=100236).

### Tekstfullmakter med og uten tabell

Vedtak **40033945**, nummer **114**, samme sak som originaltabellen 40033944, er en merinntektsfullmakt som kobler kap. **51 post 1** til kap. **3051 post 2**. Den omtaler også kap. **1633 post 1** og overføring av ubrukt bevilgning. Den har ingen tabell og ikke ett vedtatt kronebeløp å hente ut som bevilgningsendring. Begge vedtak er likevel `BUDSJETT`. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033945&p=100215).

RNB-vedtak **40035426**, nummer **1153**, er også en merinntektsfullmakt, nå som en tabell: kap. **714 post 22** kan overskrides mot tilsvarende merinntekter under kap. **5572 post 74**. Tabellen har to tekstkolonner og ingen kroner-kolonne. Det er dermed observert både tekstfullmakt uten tabell og fullmaktstabell uten bevilgningsbeløp. [API-kilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035426&p=103529).

### Blandet lov-/budsjettgrunnlag

Prop. **145 LS (2024–2025)** opptrer som felles kilde for **103526**, `type=budsjett`, og **103527**, `type=lovsak`. Begge detaljsvar peker på den andre med `relasjon_type=sammekilde`. Budsjettsaken har Innst. 540 S, mens lovsaken har Innst. 516 L og eksport-ID-er `vedtak-202425-136` til `vedtak-202425-140`. Det er dermed observert separate saks-ID-er for budsjett- og lovdel av samme proposisjonsgrunnlag. Dette er ikke en prøve på en lovparagraf som i seg selv fastsetter en bevilgningslinje. [Budsjettsak 103526](https://data.stortinget.no/eksport/sak?sakid=103526), [lovsak 103527](https://data.stortinget.no/eksport/sak?sakid=103527), [saksoversikt](https://data.stortinget.no/eksport/saker?sesjonid=2024-2025).

## Samme tekst i flere kilder og håndtering av duplikater

For den enkle endringen 40033805 er den komplette HTML-tekstverdien dekodet til tekst og kontrollert mot hele publikasjons-XML-en. Etter fjerning av blanktegn er den en sammenhengende delstreng i både innstilling **inns-202425-025s** og referat **refs-202425-11-05**. Tabellen har de samme fem radene i begge publikasjoner: kolonneoverskrift, utgiftsoverskrift, kapittel, post/endringsbeløp og fra-/til-rad. I innstillingen finnes også forklarende prosa som angir størrelser i **mill. kroner**, mens selve vedtakstabellen har enhet **Kroner**. Enheten kan derfor ikke hentes én gang for hele publikasjonen. [Innstilling](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-025s), [referat](https://data.stortinget.no/eksport/publikasjon?publikasjonid=refs-202425-11-05), [hovedkilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).

Anbefaling for videre arbeid, basert på denne prøven: behold hovedvedtakets ID og kildehenvisninger som proveniens; bruk tekstoverlapp til kontroll, og ikke tell den gjentatte teksten fra innstilling og referat som nye budsjettendringer. Kobling på vedtaksnummer bør avgrenses med sesjon og sak; prøvene dokumenterer ikke at nummer alene er en global nøkkel. Votering 23798 og 26265 viser dessuten at koblingen mellom votering og vedtak ikke er én-til-én. [Kontrollkilder](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23798), [RNB-kobling](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=26265).

## Anbefalt første B1-prøve og gjenstående hull

**Første B1-prøve anbefales å være 40033805**, nummer 14, sak 100001, votering 23520. Den er liten nok til manuell fasit: én post, én kroner-kolonne, eksplisitt økning og fra-/til-beløp, én vedtaksnummerkobling og to publikasjonskilder for samme tekst. Samtidig avdekker den to viktige avgrensninger: bevilgningsendringen er `ANNET`, og voteringsvedtakets tekst er nil. Fasit bør inneholde kapittel **2541**, post **70**, budsjettår **2024**, endring **+400 000**, før **12 210 000 000**, etter **12 210 400 000**, enhet **kroner**, merknad **overslagsbevilgning** og bevarte råkilde-ID-er. [Vedtakskilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [saks- og publikasjonskoblinger](https://data.stortinget.no/eksport/sak?sakid=100001), [voteringskobling](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23520).

Neste avgrensede prøver bør være 40033944 + 40033945 (beløpsvedtak og tekstfullmakt i samme votering), 40034443 (ny post og endring uten fra-/til), deretter 40034067 + 40035422 for post 24. Den store RNB-tabellen bør først brukes til bredde etter at en liten manuelt kontrollert prøve fungerer.

Følgende er **ikke** dokumentert som ferdig dekket:

- Fullt budsjettår: opprinnelig 2025 og RNB 2025 er observert, men nysalderingsprøven gjelder 2024. Sesjon 2025–2026 er ikke hentet i denne undersøkelsen.
- Fullstendig utvalg av relevante vedtak i den ferdige sesjonen. Alle elementer er talt, men hver tekst er ikke faglig klassifisert. Tallene 154 og 62 er tabellheuristikk, ikke bevilgningsdekning.
- Et bevilgningsvedtak der hele sakskomplekset mangler proposisjon. RNB-sakens direkte dokumentgruppe er melding, men felles innstilling og relaterte saker hindrer en slik konklusjon.
- Faktisk endring eller rettelse av et vedtaksinnhold over tid. Gjentatt henting ga bare ulike responstidsfelt.
- Historiske variasjoner før 2024–2025, alt av rowspan/colspan og uvanlige enheter, samt alle varianter av fortegn, underposter og fullmakter.
- Full kontroll av hver RNB-votering, hver alternativ votering, voteringsforslag og lovvedtaksdokument. De oppgitte ID-ene er kontrollgrunnlag, ikke påstand om komplett graf.
- Rettighets- og faglige betydninger av alle posttyper. Rapporten viser faktiske strukturer og tall fra kildene; økonomiske avgrensninger må fastsettes særskilt før produksjonsberegninger.

## Kildemanifest

[Maskinlesbart hentemanifest](api-hentinger.json) følger rapporten. To avledede små vedtakstekster følger som [opprinnelig vedtak](proever/40033944.html.txt) og [endringsvedtak](proever/40033805.html.txt). De er dekodede utdrag fra XML, ikke originale HTTP-responser.

Lokale råfiler er lagret uendret som `.raw`. `.meta.json` inneholder URL, UTC-hentetid, HTTP-status, responsheadere, byteantall og SHA256. `.html`, `.txt`, `.text`, `.parsed.json` og `selected_tables.json` er avledede inspeksjonsfiler og skal ikke forveksles med råsvar. SHA256 nedenfor gjelder bare lagrede rå byte. Alle tidspunkt gjelder 2026-10-20 og er UTC.

| Råfil / kilde | HTTP | Hentet UTC | Byte | SHA256 |
|---|---:|---|---:|---|
| [docs-home.raw](https://data.stortinget.no/) | 200 | 2026-10-20T11:38:04.378472+00:00 | 39702 | `9061f30e5de268f16d45b4a8c125fd59c24e7de388c6ad2447e6d94c86522e86` |
| [docs-publikasjon.raw](https://data.stortinget.no/dokumentasjon-og-hjelp/publikasjon/) | 200 | 2026-10-20T11:35:55.595907+00:00 | 56329 | `3d347840c68d6b1b4fe82f5640e522a9bfb0d3853a73dcbc6cd02f41f90ce464` |
| [docs-rate.raw](https://data.stortinget.no/nyhetsoversikt/begrensning-pa-api-kall/) | 200 | 2026-10-20T11:38:49.097714+00:00 | 34911 | `e991ccdbe727ddc334a2cf33a9ec9afc3d9151c7b087a297e63ec72180e750ce` |
| [docs-sak.raw](https://data.stortinget.no/dokumentasjon-og-hjelp/sak/) | 200 | 2026-10-20T11:35:48.836574+00:00 | 45970 | `d4a7d3fb19352ae6907c9611b66a1e7e8a6166425ed56ec862130f5d43bc414f` |
| [docs-teknisk.raw](https://data.stortinget.no/dokumentasjon-og-hjelp/teknisk-dokumentasjon/) | 200 | 2026-10-20T11:36:50.502034+00:00 | 38600 | `6d23a6bdb62ceb995c0bf30a17c316971b4c71d82262b462873a3f9f9e4080a3` |
| [docs-vedtak.raw](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/) | 200 | 2026-10-20T11:35:46.632818+00:00 | 42172 | `73bc598844c41b07275e01a8a1e46f3b3ff468240ff9cf709498bb98f6fdd418` |
| [docs-voteringer.raw](https://data.stortinget.no/dokumentasjon-og-hjelp/voteringer/) | 200 | 2026-10-20T11:35:51.052609+00:00 | 54988 | `0cf64477fe80ee46abe8974570312f22dd679ac3fd339f1d7f56f21e1794309e` |
| [docs-voteringsvedtak.raw](https://data.stortinget.no/dokumentasjon-og-hjelp/voteringsvedtak/) | 200 | 2026-10-20T11:35:53.281054+00:00 | 37457 | `5b0a939950f4d8ac81b49d2f3ddbd556523feddf87815647f6640b8af2a9d28f` |
| [docs (ingen råfil)](https://data.stortinget.no/dokumentasjon/) | <HTTPError 404: 'Not Found'> | 2026-10-20T11:34:52.193186+00:00 | — | `—` |
| [publikasjon-inns-202425-025s.raw](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-025s) | 200 | 2026-10-20T11:36:39.885400+00:00 | 12742 | `3f7145cb3e6f2658c6dd418ff76267085328f460afecaa364d7b93fa3a859d23` |
| [publikasjon-refs-202425-11-05.raw](https://data.stortinget.no/eksport/publikasjon?publikasjonid=refs-202425-11-05) | 200 | 2026-10-20T11:36:41.960706+00:00 | 315689 | `74cf714a3d9bebd86d6db27638e52e8de7f1af309649d3a638ab9727d47788d8` |
| [sak-100001.raw](https://data.stortinget.no/eksport/sak?sakid=100001) | 200 | 2026-10-20T11:35:57.846391+00:00 | 12733 | `e74dc4a16bef1b7c16aa8ee60f0babf39a03bd2c286b9d9747d8a3ed20e716fb` |
| [sak-100215.raw](https://data.stortinget.no/eksport/sak?sakid=100215) | 200 | 2026-10-20T11:36:08.769833+00:00 | 19059 | `a085464451ffddcdcc3cb1502d34c099f9960842258a6004a7f788245ec166c0` |
| [sak-100236.raw](https://data.stortinget.no/eksport/sak?sakid=100236) | 200 | 2026-10-20T11:36:10.842366+00:00 | 33365 | `eb64ebe232c4eec35ffb73b8fbd3df1c2d19314bcdaa9ec46fad8340ea698da1` |
| [sak-100289.raw](https://data.stortinget.no/eksport/sak?sakid=100289) | 200 | 2026-10-20T11:36:06.002146+00:00 | 14619 | `d75f7a90bcc2cb2e5e81577f4823714f41023e6e3fc708e2a2f2d85847268df6` |
| [sak-103526.raw](https://data.stortinget.no/eksport/sak?sakid=103526) | 200 | 2026-10-20T11:37:59.103599+00:00 | 13752 | `c737d33b4b777e8420a5c44a124cf9a6591ea728241ad1d06d107ef6cdc3cbec` |
| [sak-103527.raw](https://data.stortinget.no/eksport/sak?sakid=103527) | 200 | 2026-10-20T11:38:01.918230+00:00 | 24000 | `b7bb203eba140c10c4f6439fe4c6e440c8c3af1bf34ae1bef0419c10193cedbc` |
| [sak-103529.raw](https://data.stortinget.no/eksport/sak?sakid=103529) | 200 | 2026-10-20T11:36:03.256497+00:00 | 13111 | `9c2aee1df5a5aff2d78c50a2b0a45711bd850ea21f9ec912ac11a00a530cc77c` |
| [saker-2024-2025.raw](https://data.stortinget.no/eksport/saker?sesjonid=2024-2025) | 200 | 2026-10-20T11:36:44.270014+00:00 | 3816113 | `97b3c7fad5b7d4546d1efd7349ce2d7ff980ad475c5babd78e0a69a416c95234` |
| [stortingsvedtak-2024-2025-repeat.raw](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025) | 200 | 2026-10-20T11:36:13.372089+00:00 | 7479943 | `ac3ca50a9b93e016e891f630e7ef2257da2cf1ddf824b7ccb9106e8c34954b81` |
| [stortingsvedtak-2024-2025.raw](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025) | 200 | 2026-10-20T11:34:46.321003+00:00 | 7479943 | `6d7859369de69105c957cb8dbc520a077355b4c9d4452f1605f7954deccea2ac` |
| [stortingsvedtak-2026-2027-repeat.raw](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2026-2027) | 200 | 2026-10-20T11:36:18.771517+00:00 | 480829 | `a18c5b6398b491c301aa790cb1458130ac69b1369939246bc7e78d7f3b43004c` |
| [stortingsvedtak-2026-2027.raw](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2026-2027) | 200 | 2026-10-20T11:34:44.011276+00:00 | 480829 | `f22814ccac5dd5ee47bfd6f985b1a93de5fc674d935141f497243ce8fdd5ebbe` |
| [vedtak-web-40033805.raw](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033805&p=100001) | 200 | 2026-10-20T11:38:53.402511+00:00 | 75643 | `ccd084c48bfa8a92b1ccfcf0ef8b88fcc0c78b6b65007d772ca9cff7c450d6e9` |
| [voteringer-100001.raw](https://data.stortinget.no/eksport/voteringer?sakid=100001) | 200 | 2026-10-20T11:36:01.146586+00:00 | 4240 | `07a02f02be05299a6a6c79f0eb2aad6ffab5b7925cbb2368739b71fdd68b6da8` |
| [voteringer-100215.raw](https://data.stortinget.no/eksport/voteringer?sakid=100215) | 200 | 2026-10-20T11:37:56.994341+00:00 | 2329 | `23d27695156b9b05655957498f50ac90882029c891ab37f1dc7e5071a70eeac2` |
| [voteringer-103529.raw](https://data.stortinget.no/eksport/voteringer?sakid=103529) | 200 | 2026-10-20T11:36:48.330199+00:00 | 151237 | `27b34cad213ec2d384fc72e5e008fc3d2f574f4c3dbb1573dc8416deac274830` |
| [voteringsvedtak-23520.raw](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23520) | 200 | 2026-10-20T11:36:37.792702+00:00 | 761 | `4d166ac08c57d5501dac9c5f239a64fe9a92ca0767956a1ab6ca358bdcdba921` |
| [voteringsvedtak-23798.raw](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=23798) | 200 | 2026-10-20T11:38:51.326726+00:00 | 1205 | `feeaa75f586f3251e522b8f3a67cb9242c205469d62466e311e0c5aed7513049` |
| [voteringsvedtak-26265.raw](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=26265) | 200 | 2026-10-20T11:37:52.365666+00:00 | 19956 | `5f8741c788c54ce87f7ade404d5907f4fac3a42a83390920904de5b4424e6c10` |
| [voteringsvedtak-26266.raw](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=26266) | 200 | 2026-10-20T11:37:54.892333+00:00 | 1171 | `334f67b3a7dad1e36dd2e202f24e77d58f0a89fbf3f06645f26c5bb08d68f5c0` |
