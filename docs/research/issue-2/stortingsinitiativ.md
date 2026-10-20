# Issue #2 – vedtak uten direkte proposisjonsgrunnlag og Stortingets egne initiativer

Kildeundersøkelse utført 20. oktober 2026. Dette er kilde- og testgrunnlag, ikke produksjonskode. Utforskeren utførte ingen GitHub-endringer. Orkestratoren publiserer denne rapporten som del av kildeundersøkelsen.

## Konklusjon

Undersøkelsen dokumenterer en **endelig bevilgningsendring som følger opp et selvstendig initiativ fra Stortingets presidentskap**, men som blir vedtatt innenfor en bredere budsjettbehandling med proposisjonsgrunnlag: kap. **41**, post **45**, budsjettår **2025**, økning **9 700 000 kroner**, fra **175 247 000** til **184 947 000 kroner**. Den endelige kilden er vedtak **1149**, ID **40035422**, 20. juni 2025, sak **103529**. Denne linjen er en positiv bevilgningsprøve selv om sakens direkte dokumentgruppe er `melding`. Det skal ikke være et inngangskrav for innhenting eller klassifisering at en sak har dokumentgruppe `proposisjon` eller en direkte Prop.-lenke. [Endelig vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035422&p=103529), [vedtaks-API](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).

Tre forskjellige spørsmål må holdes fra hverandre:

| Spørsmål | Dokumentert resultat |
|---|---|
| (a) Endelig kapittel-/postbevilgning i en selvstendig sak uten direkte proposisjon, der proposisjonsgrunnlag heller ikke fremkommer i undersøkte relevante relasjoner/publikasjoner | Ingen sikker positiv prøve funnet i det avgrensede utvalget nedenfor. Dette sier ikke at slike vedtak ikke finnes. |
| (b) Konkret Stortings-/presidentskapsinitiert bevilgningsendring innenfor bredere budsjettbehandling med Prop.-relasjoner | Positiv prøve: Akersgata-forprosjektet, +9 700 000 kroner på kap. 41 post 45 i endelig vedtak 1149. |
| (c) Anmodning om at forslag til bevilgning fremmes senere | Vedtak 486/40034385 og vedtak 39/40033837 er negative bevilgningsprøver. De er vedtatte beslutninger, men fastsetter ikke selv en kapittel-/postbevilgning. |

Det er et strengere forskningsspørsmål å kreve at et helt sakskompleks skal være fritt for alle proposisjoner enn å kreve at produktet også skal fange opp Stortingets egne vedtak. Manglende positiv prøve på (a) gir derfor ikke grunnlag for å gjøre Prop.-tilstedeværelse til et produktkrav.

## Positiv prøve (b): Stortingets Akersgata-prosjekt

Kjeden er dokumentert med både saksmetadata, innstilling, eksplisitt henvisning i proposisjonen og den endelige vedtaksteksten:

1. **Initiativ:** Sak **101938**, dokumentgruppe `innstillingssaker`, presidentskapet (`PRES`), henvisning **Innst. 131 S (2024–2025)**. Saksdetaljens publikasjoner er innstillingen `inns-202425-131s` og referatet `refs-202425-02-20` (debatt og votering). `sak_relasjon_liste` er tom. Innstillingens innledning sier at presidentskapet fremmer forprosjektet, mens punkt 3.3 legger finansieringsbeslutningen til RNB. [Saksdetalj](https://data.stortinget.no/eksport/sak?sakid=101938), [hele innstillingen via API](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-131s).
2. **Første endelige beslutning:** Vedtak **486**, ID **40034385**, 20. februar 2025, samtykker til forprosjektet og ber om at presidentskapet fremmer forslag til bevilgning i RNB 2025. Dette er ikke årets bevilgning. At API-relasjonslisten er tom er ikke bevis for fravær av annen kildebakgrunn: selve Innst. 131 S viser i bakgrunnen også til omtale i **Prop. 1 S (2024–2025)**. [Vedtak 486](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034385&p=101938), [innstillingen](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-131s).
3. **Konkret bevilgningsforslag:** I **Prop. 146 S (2024–2025)**, kapittel 2, omtalen «Kap. 41 Stortinget», post 45, henvises uttrykkelig til vedtak 486 og Innst. 131 S. Forprosjektet anslås samlet til 72 mill. kroner; 9,7 mill. kroner skal påløpe i 2025. Proposisjonen foreslår derfor en økning på 9,7 mill. kroner på kap. 41 post 45. Dette er den eksplisitte tekstlige forbindelsen mellom initiativsaken og budsjettbehandlingen; den finnes selv om API-et ikke har en egen relasjonskant mellom 101938 og 103529. [Proposisjonens kapittel 2](https://www.regjeringen.no/no/dokumenter/prop.-146-s-20242025/id3100917/?ch=2).
4. **Felles budsjettbehandling:** Sak **103529** gjelder Meld. St. 2 og Innst. 540 S. Den har `fellesinnst` til **103528**, som gjelder Prop. 146 S, og **103526**, som gjelder Prop. 145 LS. Innst. 540 S oppgir alle tre dokumentene på forsiden. Det er derfor uriktig å kalle hele RNB-behandlingen proposisjonsfri på grunnlag av dokumentgruppen til 103529. [103529](https://data.stortinget.no/eksport/sak?sakid=103529), [103528](https://data.stortinget.no/eksport/sak?sakid=103528), [103526](https://data.stortinget.no/eksport/sak?sakid=103526), [Innst. 540 S](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-540s).
5. **Endelig bevilgning:** Vedtak 1149/40035422 fastsetter den kontrollerte linjen nedenfor. Samme linje finnes i den lagrede Innst. 540 S, men innstillingen er kontrollkilde; den endelige vedtaksteksten avgjør den vedtatte bevilgningen. [Vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035422&p=103529).

| Felt | Kontrollert verdi |
|---|---|
| Vedtak / ID / dato / sak | 1149 / 40035422 / 20.06.2025 / 103529 |
| Budsjettår / side | 2025 / utgift |
| Kapittel / post | 41 Stortinget / 45 Større utstyrsanskaffelser og vedlikehold |
| Stikkord / enhet | kan overføres / kroner |
| Endring | +9 700 000 |
| Fra / til | 175 247 000 / 184 947 000 |
| Regnekontroll | 175 247 000 + 9 700 000 = 184 947 000 |

Tabellens kapittel står på egen rad, posten på neste rad og fra-/til-beløp på en etterfølgende rad. Tallene er kontrollert mot den dekodede HTML-en, ikke hentet fra en søketrefftekst. Normalisert linje, identifikatorer og kontrollresultater ligger i [kontrollfasiten](initiativ-fasit.json); vedtaksteksten er bevart i `40035422.html` som avledet inspeksjonsfil. Råsvarene står i manifestet.

**Fullmakten er et eget vedtak:** **1156**, ID **40035429**, samme dato/sak, gir adgang til forpliktelser utover gitt bevilgning med samlet ramme for nye forpliktelser og gammelt ansvar på inntil **72 mill. kroner** under kap. 41 post 45. Dette er ikke en ytterligere bevilgning på 72 mill. kroner for 2025 og skal ikke legges til økningen på 9,7 mill. kroner. [Vedtak 1156](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035429&p=103529).

## Dokumentert saksgraph og kildegrenser

| Fra | Dokumentert kant / henvisning | Til |
|---|---|---|
| 101938 | publikasjon | Innst. 131 S, `inns-202425-131s`; referat `refs-202425-02-20` |
| 101938 | tom API-relasjonsliste; ikke grunnlag for å stoppe tekstundersøkelsen | Innst. 131 S omtaler Prop. 1 S i bakgrunnsteksten |
| vedtak 486 / Innst. 131 S | uttrykkelig henvisning i Prop. 146 S, kap. 41 post 45 | bevilgningsforslag +9,7 mill. kroner i 2025 |
| 103529 | `fellesinnst` | 103526 og 103528 |
| 103528 | `fellesinnst` | 103526 og 103529 |
| 103528 | publikasjon, direkte proposisjon | Prop. 146 S; eksport-ID nil, lenke til regjeringen.no |
| 103526 | `fellesinnst` | 103529 og 103528 |
| 103526 | `sammekilde` | 103527 |
| 103527 | `sammekilde` | 103526 |
| 103526 og 103527 | direkte henvisning | Prop. 145 LS; henholdsvis Innst. 540 S og Innst. 516 L |
| 103529, 103528, 103526 | felles publikasjon | Innst. 540 S, `inns-202425-540s` |
| 103529 | endelige vedtak | 1149/40035422, bevilgning; 1156/40035429, fullmakt |

Dette er en dokumentert relevant delgraph, ikke et løfte om å ha hentet alle omtaler og vedlegg gjennom all forhistorie. For (b) trengs den eksplisitte initiativ- og bevilgningskjeden, ikke fravær av Prop. i grafen. For å hevde (a) i en senere undersøkelse må også tekstlige referanser og fellesinnstillinger undersøkes. Proposisjonens kapittel 2 er lest for relevant avsnitt; innstilling 131s sine PDF-vedlegg er ikke hentet.

## Negative prøver

- **Vedtak 486/40034385, sak 101938:** Selvstendig presidentskapssak, men ingen kapittel-/postbevilgning i dette vedtaket. Formuleringen gjelder et senere bevilgningsforslag. Det finnes dessuten Prop.-omtale i innstillingens bakgrunn. Dette er en god negativ test mot å tolke både et kostnadsestimat og et samtykke til prosjekt som årets bevilgning.
- **Vedtak 39/40033837, sak 98915:** Dokument 8:160 S (2023–2024) og Innst. 34 S (2024–2025), representantforslag om veisystemet i Oslo. Vedtaket ber regjeringen komme tilbake med forslag om å øke bevilgningen til Akershus fylkeskommune. Det fastsetter verken et konkret kronebeløp eller en kapittel-/postendring. Saksdetaljen har tom relasjonsliste, men dette endrer ikke vedtakets innhold. [Saksdetalj](https://data.stortinget.no/eksport/sak?sakid=98915), [vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033837&p=98915).
- **Vedtak 623/40034607, sak 103284:** Presidentskapets Innst. 240 S fastsetter lønnssatser for Høyesteretts medlemmer, herunder 2 607 300 og 2 248 900 kroner. Dette er satser, ikke en bevilgning på en kapittel-/postlinje. Saksdetaljen har ingen relasjoner og bare innstilling og referat som publikasjoner. Referatets eksport-ID er faktisk `refe-202425-05-06`, mens lenke-URL-en bruker `refs-202425-05-06`; feilstavelsen er ikke rettet eller brukt som bevis. [Saksdetalj](https://data.stortinget.no/eksport/sak?sakid=103284), [vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034607&p=103284).
- **Vedtak 1133/40035396, sak 103087:** Et faktisk vedtatt godtgjørelsesbeløp i et representantforslags saks-ID er heller ikke automatisk en bevilgning. Saken har Dokument 8:262 S og Innst. 536 S. `fellesinnst` forbinder den med **104059**, godtgjøringsutvalgets innstilling; 104059 har motsatt kant tilbake. Innst. 536 S behandler godtgjørelser sammen med representantforslaget. Det endelige vedtaket fastsetter årssatser, ikke kapittel/post. [103087](https://data.stortinget.no/eksport/sak?sakid=103087), [104059](https://data.stortinget.no/eksport/sak?sakid=104059), [Innst. 536 S](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-536s).
- **RNB 2024, vedtak 857/40033719, sak 98919:** En annen endelig bevilgningstabell på en meldingssak. Saksdetaljen gir `fellesinnst` til **98918**, **98916** og **99234**. I den lagrede saksoversikten er disse henholdsvis Prop. **104 S**, **103 LS** og **106 S**, alle med Innst. 447 S. Dette avkrefter en proposisjonsfri (a)-tolkning allerede uten ytterligere grafutvidelse. Saksdetaljene for de tre nabosakene er ikke hentet; kildebeviset for deres henvisninger er sesjonsoversikten. [98919](https://data.stortinget.no/eksport/sak?sakid=98919), [saksoversikt 2023–2024](https://data.stortinget.no/eksport/saker?sesjonid=2023-2024).
- **Eldre målrettet kontroll:** Innst. **197 S (2019–2020)** om pandemitiltak ble hentet og kontrollert. Forsiden oppgir uttrykkelig **Prop. 52 S**, unntatt kap. 2541 post 70, og **Prop. 53 LS** bokstav B. At komiteen både omtaler egne tiltak og gir flere anmodninger gjør ikke denne innstillingen til bevis for et helt proposisjonsfritt vedtak. Ingen endelig vedtaks-ID eller selvstendig bevilgningsendring uten Prop.-grunnlag er etablert fra denne ene eldre kontrollen; den fremmes derfor ikke som positiv fasit. [Innst. 197 S](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-201920-197s).

## Numerisk søkeavgrensning

Første søkegrunnlag var de allerede lagrede 2024–2025-svarene og saksoversikten. Deretter ble det allerede lagrede vedtakssvaret for 2023–2024 koblet mot en ny hentet saksoversikt for samme sesjon. Ingen komplette nye vedtaksår ble massehentet.

Alle vedtak ble koblet til saksoversikt på sak-ID. Det var **0 ukoblede** i begge sesjoner. Deretter ble vedtak på saker med dokumentgruppe forskjellig fra `proposisjon` undersøkt med dette eksplisitte, brede søkefilteret i HTML-teksten: `<table` **eller** regex `bevilg|løyv|statsbudsjettet|kap\.\s*\d`, uten skille mellom store/små bokstaver. Dette er et avgrenset søk, ikke en validert fullstendig bevilgningsklassifikator. Første smalere filter (`<table` eller `bevilg`) ga 36 og 30 kandidater; det ble utvidet før konklusjonen.

| Sesjon | Saker i oversikt | Vedtak | Unike saker for vedtak | Vedtak på ikke-proposisjonssaker | Kandidater i utvidet filter / saker |
|---|---:|---:|---:|---:|---:|
| 2024–2025 | 727 | 1 260 | 472 | 724 | 65 / 16 |
| 2023–2024 | 637 | 923 | 380 | 560 | 51 / 12 |

Saksoversiktene er sesjonsendepunktenes egne utvalg og kan inkludere saker behandlet i en annen sesjon. Det er vedtaksendepunktet som avgrenser vedtakssesjonen. Filteret ble brukt til kandidatfinning; det er ikke et forslag om å ekskludere proposisjonssaker eller kreve en bestemt dokumentgruppe i produktet. `screening.json` inneholder alle 116 kandidat-ID-er, deres saker, vedtaksnumre og normaliserte tekster. De identifiserte bevilgningstabellene på ikke-proposisjonssaker i dette utvalget er RNB-tabellene; øvrige treff er anmodninger, satser, prosedyrevedtak eller fullmakter. Rammevedtaket for 2024 har beløp, men ikke en endelig kapittel-/postbevilgning og er skilt fra det spørsmålet.

## Testgrunnlag og gjenstående søk

Bruk **40035422, kap. 41 post 45** som positiv test for innhenting fra en meldingssak og for presidentskapets initiativ som ender i en ordinær bevilgningslinje. Bevar proveniens 101938 → vedtak 486 → Prop. 146 S → Innst. 540 S → vedtak 1149, og hold årets 9,7 mill. kroner atskilt fra fullmakten på 72 mill. kroner. Dette dokumenterer kategori (b), ikke kategori (a).

Bruk **40034385** og **40033837** som negative tester for anmodning om fremtidig bevilgning, **40034607** og **40035396** som negative tester for satstabeller, og **40035429** som separat fullmaktstest. Oppdagelse av kandidater bør ta utgangspunkt i alle endelige vedtak og tekstinnhold, med sak og dokumentgruppe som proveniens. En eventuell teknisk test med utelatt Prop.-metadata må merkes som en konstruert robusthetstest; den er ikke en historisk positiv (a)-kilde.

Et neste avgrenset søk etter (a) kan starte i eldre sesjoners `innstillingssaker` og `representantforslag` med endelig vedtakstekst som sier «I statsbudsjettet ...» og har kapittel/post/beløp, og med egne Stortingskapitler som prioritet. Sjekk også komitéinitierte krisebevilgninger i mars–april 2020, men følg forslag → votering → endelig vedtak før noe kalles bevilgning. Den undersøkte Innst. 197 S er allerede avklart som Prop.-basert; nye søk bør ikke gjenbruke den som bevis for (a). Ingen kilde fra et annet år er hentet systematisk her.

## Henting, bevaring og kontroll

Bundled Python ble brukt: `C:\Users\marti\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`. Offentlige kilder ble hentet sekvensielt med minst to sekunders pause, fast User-Agent og 35 sekunders timeout. Standardkall for saksoversikten 2023–2024 feilet **2026-10-20T11:55:39.364856+00:00** med `URLError(gaierror(11001, 'getaddrinfo failed'))`. Et avgrenset tillatt nettverkskall hentet deretter de offentlige kildene. Ingen HTTP 429 ble observert. Suksessmetadata har URL, forespørselstid UTC, HTTP-status, headere, byteantall og SHA256. Tiden er rett før forespørselen; kildens responstid og HTTP Date er separate felt.

`final_checks.py` kontrollerer XML-parsing, full sak-ID-kobling i disse to korpusene, kandidatantall, råfilhash mot metadata, aritmetikken for kap. 41 post 45 og at den samme normaliserte beløpslinjen finnes i endelig vedtak og Innst. 540 S. Det kontrollerer dessuten at Prop. 146 S uttrykkelig henviser til vedtak 486 og 9,7 mill. kroner i 2025. Alle disse kontrollene passerte. Dette er kontroller av konkrete kildebevis; de beviser ikke fullstendig historisk dekning eller en generell parser.

Alle `.raw` er uendrede svar. `.html`, `.text`, JSON-uttrekk og skript er avledet inspeksjonsmateriale. Bare denne filen er sluttrapport. API-versjonen i undersøkte XML-oversikter er 1.6. Ingen kildeinstruksjoner er utført; dokumentene er behandlet som data.

## Kildemanifest

SHA256 gjelder de lagrede rå bytene, ikke normalisert tekst. Arvede kilder peker på opprinnelige råfiler; hentetidene er deres opprinnelige hentetider. URL, hentetid, status og alle kontrollerte råfilhasher ligger i [hentemanifestet](initiativ-hentinger.json). Responsheadere og store råfiler er bevart lokalt, ikke versjonert i repoet.

| Råfil / kilde-URL | Hentet UTC | Byte | SHA256 |
|---|---|---:|---|
| [prop146-ch2.raw](https://www.regjeringen.no/no/dokumenter/prop.-146-s-20242025/id3100917/?ch=2) | 2026-10-20T11:58:43.907009+00:00 | 940733 | `780fc907e9a8ee1932072807456d869e8079ed646fda1b3cf182fb4d2763f92f` |
| [prop146-html.raw](https://www.regjeringen.no/id/PRP202420250146000DDDEPIS) | 2026-10-20T11:58:23.555610+00:00 | 56248 | `684e0d2df68f631401364c6f831d46ed41c131c60d0da5b42f30944332197e53` |
| [pub-inns-201920-197s.raw](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-201920-197s) | 2026-10-20T11:57:35.832225+00:00 | 166784 | `af1606e6b9725a91c0173ded58d0e3dfaa51d1288a9e443fb3437d9792a43845` |
| [pub-inns-202425-131s.raw](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-131s) | 2026-10-20T11:56:40.522096+00:00 | 26330 | `d8ecf596dad107dd0778d013da460c665484e7faeb0e4844aa882254936d6fce` |
| [pub-inns-202425-536s.raw](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-536s) | 2026-10-20T11:56:42.651607+00:00 | 33224 | `ddeb9e4f8c7a87dea4350754acc720b2629ed99b305eedb49080b8dc7f96bbff` |
| [pub-inns-202425-540s.raw](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-202425-540s) | 2026-10-20T11:57:20.626689+00:00 | 9952983 | `551218050e4a5f33c8baa8e8733997bf38875b8b9533feaeca9ea44148bd7456` |
| [sak-101938.raw](https://data.stortinget.no/eksport/sak?sakid=101938) | 2026-10-20T11:55:59.313034+00:00 | 7238 | `8962ca2841b45f8c3b111b3cb682d27f1526fd70cd3076bdb6a26dcb60ee5e28` |
| [sak-103087.raw](https://data.stortinget.no/eksport/sak?sakid=103087) | 2026-10-20T11:56:01.788197+00:00 | 22876 | `1eca46406d5a2a56a424f67fa5de120909e19e542f66ac8cd751b992e4099b86` |
| [sak-103284.raw](https://data.stortinget.no/eksport/sak?sakid=103284) | 2026-10-20T11:56:04.296139+00:00 | 6985 | `9751ba786c9853135089553ab26439eabc2ea0a3164e4cc6d2ac228217ea5827` |
| [sak-103528.raw](https://data.stortinget.no/eksport/sak?sakid=103528) | 2026-10-20T11:56:47.168264+00:00 | 13146 | `f8f43199ab3504193affeeb07b172d8cd5b55cbeb39d6e77425a5d5ad3632b89` |
| [sak-104059.raw](https://data.stortinget.no/eksport/sak?sakid=104059) | 2026-10-20T11:56:44.862194+00:00 | 8713 | `de98aaa65582fbe094b74dc292458d6116373fa1cc088b1385b57454a7991a52` |
| [sak-98915.raw](https://data.stortinget.no/eksport/sak?sakid=98915) | 2026-10-20T11:56:07.068093+00:00 | 27922 | `a2a9b2e3b88286e206f9a3b471273cc70829ec5aefaf9263f89d0963c80d0c41` |
| [sak-98919.raw](https://data.stortinget.no/eksport/sak?sakid=98919) | 2026-10-20T11:56:49.237170+00:00 | 13572 | `dae5937812c99c5bedb0752dab83d5e81d0c1aeed9b90c95412a61f83d5f03e1` |
| [saker-2023-2024.raw](https://data.stortinget.no/eksport/saker?sesjonid=2023-2024) | 2026-10-20T11:55:53.084447+00:00 | 3485620 | `876498e4caf6b48d2708f54a096b1e065fc472645ba0decac3904bcb13826eb7` |
| [stortingsvedtak-2024-2025.raw](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025) | 2026-10-20T11:34:46.321003+00:00 | 7479943 | `6d7859369de69105c957cb8dbc520a077355b4c9d4452f1605f7954deccea2ac` |
| [saker-2024-2025.raw](https://data.stortinget.no/eksport/saker?sesjonid=2024-2025) | 2026-10-20T11:36:44.270014+00:00 | 3816113 | `97b3c7fad5b7d4546d1efd7349ce2d7ff980ad475c5babd78e0a69a416c95234` |
| [sak-103529.raw](https://data.stortinget.no/eksport/sak?sakid=103529) | 2026-10-20T11:36:03.256497+00:00 | 13111 | `9c2aee1df5a5aff2d78c50a2b0a45711bd850ea21f9ec912ac11a00a530cc77c` |
| [sak-103526.raw](https://data.stortinget.no/eksport/sak?sakid=103526) | 2026-10-20T11:37:59.103599+00:00 | 13752 | `c737d33b4b777e8420a5c44a124cf9a6591ea728241ad1d06d107ef6cdc3cbec` |
| [sak-103527.raw](https://data.stortinget.no/eksport/sak?sakid=103527) | 2026-10-20T11:38:01.918230+00:00 | 24000 | `b7bb203eba140c10c4f6439fe4c6e440c8c3af1bf34ae1bef0419c10193cedbc` |
| [vedtak-2023-2024.xml](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2023-2024) | 2026-10-20T11:35:51.910747+00:00 | 6816165 | `554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf` |

## Etterprøvbart kandidatutvalg

Tabellen gir samtlige sak-ID-er og vedtaks-ID-er som ble fanget av det endelige filteret. Detaljpublikasjoner er undersøkt målrettet som beskrevet over; listen innebærer ikke at alle disse sakene fikk egne detaljkall. Normalisert tekst per vedtak ligger i `screening.json`.

| Sesjon / sak | Dokumentgruppe / henvisning i oversikt | Vedtaks-ID-er i filteret |
|---|---|---|
| 2024-2025 / [94524](https://data.stortinget.no/eksport/sak?sakid=94524) | dokumentserien; Dokument 19 (2022-2023), Innst. 30 S (2024-2025) | 40033816 |
| 2024-2025 / [98915](https://data.stortinget.no/eksport/sak?sakid=98915) | representantforslag; Dokument 8:160 S (2023-2024), Innst. 34 S (2024-2025) | 40033837 |
| 2024-2025 / [97332](https://data.stortinget.no/eksport/sak?sakid=97332) | melding; Meld. St. 34 (2023-2024), Innst. 55 S (2024-2025) | 40033874 |
| 2024-2025 / [100590](https://data.stortinget.no/eksport/sak?sakid=100590) | melding; Meld. St. 6 (2024-2025), Innst. 128 S (2024-2025) | 40034346 |
| 2024-2025 / [100708](https://data.stortinget.no/eksport/sak?sakid=100708) | representantforslag; Dokument 8:17 S (2024-2025), Innst. 134 S (2024-2025) | 40034358 |
| 2024-2025 / [100243](https://data.stortinget.no/eksport/sak?sakid=100243) | representantforslag; Dokument 8:7 S (2024-2025), Innst. 133 S (2024-2025) | 40034365 |
| 2024-2025 / [97309](https://data.stortinget.no/eksport/sak?sakid=97309) | melding; Meld. St. 33 (2023-2024), Innst. 150 S (2024-2025) | 40034591 |
| 2024-2025 / [101371](https://data.stortinget.no/eksport/sak?sakid=101371) | melding; Meld. St. 9 (2024-2025), Innst. 242 S (2024-2025) | 40034610 |
| 2024-2025 / [102337](https://data.stortinget.no/eksport/sak?sakid=102337) | representantforslag; Dokument 8:111 S (2024-2025), Innst. 306 S (2024-2025) | 40034733 |
| 2024-2025 / [103529](https://data.stortinget.no/eksport/sak?sakid=103529) | melding; Meld. St. 2 (2024-2025), Innst. 540 S (2024-2025) | 40035421, 40035497, 40035499, 40035501, 40035505, 40035511, 40035520, 40035525, 40035422, 40035423, 40035424, 40035425, 40035426, 40035427, 40035428, 40035429, 40035430, 40035431, 40035432, 40035433, 40035434, 40035435, 40035436, 40035437, 40035438, 40035439, 40035440, 40035441, 40035442, 40035443, 40035444, 40035445, 40035446, 40035447, 40035448, 40035450, 40035452, 40035453, 40035455, 40035456, 40035458, 40035459, 40035461, 40035468, 40035470, 40035471, 40035474, 40035475, 40035477 |
| 2024-2025 / [100344](https://data.stortinget.no/eksport/sak?sakid=100344) | innstillingssaker; Innst. 1 S (2024-2025) | 40033794, 40033795 |
| 2024-2025 / [101938](https://data.stortinget.no/eksport/sak?sakid=101938) | innstillingssaker; Innst. 131 S (2024-2025) | 40034385 |
| 2024-2025 / [103284](https://data.stortinget.no/eksport/sak?sakid=103284) | innstillingssaker; Innst. 240 S (2024-2025) | 40034607 |
| 2024-2025 / [103867](https://data.stortinget.no/eksport/sak?sakid=103867) | innstillingssaker; Innst. 531 S (2024-2025) | 40035387 |
| 2024-2025 / [102295](https://data.stortinget.no/eksport/sak?sakid=102295) | dokumentserien; Dokument 18 (2024-2025), Innst. 473 S (2024-2025) | 40035389 |
| 2024-2025 / [103087](https://data.stortinget.no/eksport/sak?sakid=103087) | representantforslag; Dokument 8:262 S (2024-2025), Innst. 536 S (2024-2025) | 40035396 |
| 2023-2024 / [95557](https://data.stortinget.no/eksport/sak?sakid=95557) | melding; Meld. St. 1 (2023-2024), Innst. 2 S (2023-2024) | 40032587, 40032589, 40032593, 40032586 |
| 2023-2024 / [96109](https://data.stortinget.no/eksport/sak?sakid=96109) | representantforslag; Dokument 8:24 S (2023-2024), Innst. 154 S (2023-2024) | 40033046 |
| 2023-2024 / [96688](https://data.stortinget.no/eksport/sak?sakid=96688) | representantforslag; Dokument 8:51 S (2023-2024), Innst. 195 S (2023-2024) | 40033152 |
| 2023-2024 / [98038](https://data.stortinget.no/eksport/sak?sakid=98038) | representantforslag; Dokument 8:106 S (2023-2024), Innst. 383 S (2023-2024) | 40033502 |
| 2023-2024 / [98443](https://data.stortinget.no/eksport/sak?sakid=98443) | representantforslag; Dokument 8:142 S (2023-2024), Innst. 376 S (2023-2024) | 40033524 |
| 2023-2024 / [98244](https://data.stortinget.no/eksport/sak?sakid=98244) | melding; Meld. St. 15 (2023-2024), Innst. 412 S (2023-2024) | 40033562 |
| 2023-2024 / [97360](https://data.stortinget.no/eksport/sak?sakid=97360) | melding; Meld. St. 23 (2023-2024), Innst. 360 S (2023-2024) | 40033633 |
| 2023-2024 / [98919](https://data.stortinget.no/eksport/sak?sakid=98919) | melding; Meld. St. 2 (2023-2024), Innst. 447 S (2023-2024) | 40033773, 40033777, 40033780, 40033783, 40033719, 40033720, 40033721, 40033722, 40033723, 40033724, 40033725, 40033726, 40033727, 40033728, 40033730, 40033731, 40033732, 40033733, 40033734, 40033735, 40033736, 40033737, 40033738, 40033739, 40033740, 40033742, 40033743, 40033744, 40033747, 40033753, 40033754, 40033755, 40033756, 40033757, 40033761, 40033762 |
| 2023-2024 / [95880](https://data.stortinget.no/eksport/sak?sakid=95880) | innstillingssaker; Innst. 1 S (2023-2024) | 40031491, 40031492 |
| 2023-2024 / [96718](https://data.stortinget.no/eksport/sak?sakid=96718) | innstillingssaker; Innst. 117 S (2023-2024) | 40032665 |
| 2023-2024 / [98552](https://data.stortinget.no/eksport/sak?sakid=98552) | representantforslag; Dokument 8:152 S (2023-2024), Innst. 423 S (2023-2024) | 40033665 |
| 2023-2024 / [99313](https://data.stortinget.no/eksport/sak?sakid=99313) | innstillingssaker; Innst. 451 S (2023-2024) | 40033692 |

## Publikasjonsreferanser i hentede saksdetaljer

`graph.json` bevarer alle publikasjonsreferanser og API-relasjonskanter fra de ti undersøkte saksdetaljene, inklusive `eksport_id`, lenketekst og URL. Publikasjonene i manifestet er de som er hentet og lest. Andre referanser nedenfor er dokumenterte pekere fra saksdetaljene, ikke påstand om at deres fulle innhold er lest.

| Sak | Alle publikasjons-ID-er / lenkede dokumenter i detaljsvaret |
|---|---|
| 101938 | [inns-202425-131s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-131s/); [refs-202425-02-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-02-20/1); [refs-202425-02-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-02-20/voteringer#200225-1) |
| 103087 | [dok8-202425-262s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Representantforslag/2024-2025/dok8-202425-262s/); [refs-202425-04-24](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-04-24/referatsaker/); [inns-202425-536s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-536s/); [refs-202425-06-19](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-19/5); [refs-202425-06-19](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-19/voteringer#190625-5) |
| 103284 | [inns-202425-240s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-240s/); [refe-202425-05-06](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-05-06/1); [refe-202425-05-06](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-05-06/voteringer#060525-1) |
| 103528 | [Prop. 146 S (2024-2025)](http://www.regjeringen.no/id/PRP202420250146000DDDEPIS); [refs-202425-05-15](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-05-15/referatsaker/); [inns-202425-540s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-540s/); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/7); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/voteringer#200625-7) |
| 104059 | [inns-202425-536s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-536s/); [refs-202425-06-19](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-19/5); [refs-202425-06-19](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-19/voteringer#190625-5) |
| 98915 | [dok8-202324-160s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Representantforslag/2023-2024/dok8-202324-160s/); [refs-202324-05-21](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2023-2024/refs-202324-05-21/referatsaker/); [inns-202425-034s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-034s/); [refs-202425-11-14](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-11-14/5); [refs-202425-11-19](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-11-19/voteringer#141124-5) |
| 98919 | [Meld. St. 2 (2023-2024)](http://www.regjeringen.no/id/STM202320240002000DDDEPIS); [refs-202324-05-14](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2023-2024/refs-202324-05-14/referatsaker/); [inns-202324-447s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2023-2024/inns-202324-447s/); [refs-202324-06-21](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2023-2024/refs-202324-06-21/3); [refs-202324-06-21](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2023-2024/refs-202324-06-21/voteringer#210624-3) |
| 103529 | [Meld. St. 2 (2024-2025)](http://www.regjeringen.no/id/STM202420250002000DDDEPIS); [refs-202425-05-15](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-05-15/referatsaker/); [inns-202425-540s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-540s/); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/7); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/voteringer#200625-7) |
| 103526 | [Prop. 145 LS (2024-2025)](http://www.regjeringen.no/id/PRP202420250145000DDDEPIS); [refs-202425-05-15](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-05-15/referatsaker/); [inns-202425-540s](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-540s/); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/7); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/voteringer#200625-7) |
| 103527 | [Prop. 145 LS (2024-2025)](http://www.regjeringen.no/id/PRP202420250145000DDDEPIS); [refs-202425-05-15](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-05-15/referatsaker/); [inns-202425-516l](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-516l/); [refs-202425-06-17](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-17/5); [vedtak-202425-136](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Beslutninger/Lovvedtak/2024-2025/vedtak-202425-136/); [vedtak-202425-137](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Beslutninger/Lovvedtak/2024-2025/vedtak-202425-137/); [vedtak-202425-138](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Beslutninger/Lovvedtak/2024-2025/vedtak-202425-138/); [vedtak-202425-139](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Beslutninger/Lovvedtak/2024-2025/vedtak-202425-139/); [vedtak-202425-140](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Beslutninger/Lovvedtak/2024-2025/vedtak-202425-140/); [refs-202425-06-17](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-17/voteringer#170625-5); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/2); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/3); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/4); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/5); [refs-202425-06-20](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-06-20/6) |
