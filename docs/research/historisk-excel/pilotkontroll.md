# Avgrenset tallprøve og anbefalt pilotår for historisk Excel

Kontrollert 21. oktober 2026 mot kodegrunnlag `ae80c6a594f33bd83d63feea2d1f26a59b341185`. Dette er forskningsgrunnlag for en startklar plan under [#13](https://github.com/depmartin/budsjetthistorikk/issues/13), ikke produksjonsimport eller faglig godkjenning. #13 og spesifikasjonen [#1](https://github.com/depmartin/budsjetthistorikk/issues/1), begge uten kommentarer ved lesingen, er lest sammen med repoets arbeids-, begreps- og kilderegler. [Observasjonsformatet](../../observasjonsformat.md), [filkontrollen](modellvurdering.md) og [varige kildefunn](../../kildefunn.md) gjelder fortsatt.

## Anbefaling og faktisk kontrollomfang

**Anbefal budsjettår 2024 som første pilot.** Valget støttes nå av en faktisk Excel–Storting-prøve, i tillegg til det eksisterende uavhengige kontrollgrunnlaget. Originalarbeidsboken har sammenlignbare salderte nivåer og dokumenttilknyttede beløp gjennom både 2023–2024 og 2024–2025. Den egner seg også til å prøve fortegn, post 24, underposter, flere dokumentrader, null, ukjent stadium og de tre kjente kildekonfliktene.

Prøven omfatter **fem opprinnelige og sju senere vedtaksobjekter** fra de eksisterende autentiske B3-, B4- og B6-fixturene. Alle tolv er kjørt gjennom uendret `sync_saved` → B2/SQLite → `extract_revision` med **`storting-belop-v2`**. Alle **2 894 beløpsobservasjoner** er lest tilbake og sammenlignet eksakt med adapterresultatet. Gjentatt uttrekk av samme revisjon ga identisk resultat. Den konkrete tolkningen har ID `0cfb813792c1b5a607981719de27024fe2608fba6504bd9df4f4eb812f87cc4f`.

Dette er et avgrenset utvalg, **ingen utført helårsavstemming mellom Excel og API**. Utvalget følger tilgjengelige autentiske fixtures og dokumenterte forskningskoblinger; det er en utforskende prøve uten påstand om representativitet eller forhåndsregistrerte forventninger. Fem opprinnelige objekter gir 375 postnivåer. Sju senere objekter gir 858 eksplisitte postendringer; før-/etterbeløp og komponentnivåer telles separat. Ingen årsprosent eller fullstendighetsprosent beregnes fra utvalget. De tidligere **1 625 / 43** gjelder DFØ ↔ statsregnskapets PDF og er **ikke Excel-treff**. De 1 574 opprinnelige treffene i #2 gjelder API ↔ Blå bok. Disse er støtte for årvalget, ikke gjenbrukt som resultat av denne prøven.

**Verifisert:** tallene, kildeposisjonene, replayen og de eksplisitte differanse-/fraværsstatusene nedenfor. **Foreløpig:** faglig tolkning og omregningsregler avgrenset til de prøvde kolonnene og radene. **Uavklart:** generell kolonnesemantikk, avrundingspolicy, full dokument-/hendelseskobling og hele årets Excel-dekning. Ingen av kildene er utpekt som fasit for den andre.

Historikken skal ikke styre eller bremse registreringen av nye tall. Pilotplanen bør bruke det eksisterende lange observasjonsformatet som utgangspunkt, med mulighet for en begrunnet forbedring før bygging. Nye Storting-observasjoner skal kunne registreres selv om historisk normalisering eller registerkobling fortsatt er uavklart.

## Kilder, uendrede byte og proveniens

Excel-originalen er lest binærsikkert med `git show` fra revisjon **`da720e9dd4ebfff31d88c14488c5f3217d045786`**, som også er historikkbranchens kontrollerte head. [Originalfilen](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2024_samlet_inputdata.xlsx) er **257 569 byte**, SHA-256 **`870d30d55b4f7f6791fe48ea2a15aa3e98d61946393385d0411e46a0169f60f3`**. Hashen er kontrollert før og etter lesingen. Ingen `Workbook.save`, originalendring, filpublisering eller merge av historikkbranchen inngår.

Arbeidsboken har `Rådata` med 1 871 datarader og 14 kolonner, og `Dokumentiltknyntning2024` med 1 371 datarader og 15 kolonner. Rådata har 1 693 kapittel/post-nøkler. Beløpsfeltene i sammenligningen er lest fra originalens OOXML-`<v>` som `Decimal`; openpyxl 3.1.5 brukes til navn, nøkler og referanser. Dette bevarer desimalspor som et vanlig flyttallsuttrekk kan skjule. Det er ikke foretatt Excel-reberegning.

| API-objekt og fixture | Rolle i prøven | Observasjoner |
| --- | --- | ---: |
| [40032763](../../../tests/fixtures/b4/40032763.json) | Opprinnelig, blant annet 2445/24 | 74 |
| [40032791](../../../tests/fixtures/b4/40032791.json) | Opprinnelig, blant annet 2460/24 | 114 |
| [40032850](../../../tests/fixtures/b3/40032850.json) | Opprinnelig, blant annet 2470/24 og 2541/70 | 124 |
| [40032976](../../../tests/fixtures/b4/40032976.json) | Opprinnelig, blant annet 5440/24 | 49 |
| [40033025](../../../tests/fixtures/b3/40033025.json) | Opprinnelig, blant annet 5999/90 | 31 |
| [40033719](../../../tests/fixtures/b3/40033719.json) | RNB 2024, kontrollgruppe i447/23-24 | 1 732 |
| [40033805](../../../tests/fixtures/b3/40033805.json) | Øvrig endring, i25/24-25 | 3 |
| [40034064](../../../tests/fixtures/b3/40034064.json) | Høstendringer, i99/24-25 | 214 |
| [40034226](../../../tests/fixtures/b3/40034226.json) | Høstendringer, i93/24-25 | 60 |
| [40034287](../../../tests/fixtures/b3/40034287.json) | Nysaldering, i90/24-25 | 265 |
| [40034048](../../../tests/fixtures/b6/40034048.json) | ANNET uten standardinnledning, i81/24-25 | 6 |
| [40034229](../../../tests/fixtures/b6/40034229.json) | ANNET uten standardinnledning, i94/24-25 | 222 |

Lenkene viser sidevogner til uendrede, komplette enkeltobjekter. De er **delvise, avledede fixtures**, ikke hele sesjonsresponser. [Kontrollgrunnlaget](pilotkontroll/kontrollgrunnlag.json) bevarer full SHA-256, byteantall, foreldreartefakt, URL og hentetid for hvert objekt, adapterens kildehash og de lokale B2-revisjons-/uttrekks-ID-ene. Foreldrene er:

- [Sesjon 2023–2024](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2023-2024), bevart 20.10.2026 kl. 11.35.51 UTC: 6 816 165 byte, SHA-256 `554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf`.
- [Sesjon 2024–2025](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), bevart 20.10.2026 kl. 11.36.10 UTC: 7 479 943 byte, SHA-256 `9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680`.

Ingen ny HTTP-henting er gjort. Fixture-replay bruker eksisterende B2-krav `historical_sample=True`, som gir datasett `prove`. **Det er ikke et valg av datasett for historisk Excel.** Den kommende Excel-adapteren skal bruke `historisk` uten oppdiktede API-metadata. Prøvedatabasen og eksperimentskriptene ligger utenfor produksjonsrepoet under `work/p13-probe`.

## Avstemmingsregler

1. Budsjettår er uttrykkelig **2024**. Sesjon, vedtaksdato og behandlingsrunde følger API-objektet. En desemberdato brukes ikke til å omklassifisere `uavklart` runde til nysaldering. Forskningsgruppene nedenfor er kontrollkoblinger, ikke endringer av adapterens klassifikasjon.
2. Saldert `Rådata!H` prøves som nivå i millioner kroner mot adapterens observerte `meaning=nivaa`, `detail_level=post`. For de 36 tilfellene med flere rådatarader summeres de valgte underpostcellene først til et **separat kontrollaggregat**. Råobservasjonene beholdes. Sammenfallende summer vedtar ingen generell underpost-/hendelsesidentitet.
3. Dokumentets D-beløp prøves i kroner. Gruppér på `(doknr20, kap_nr, post_nr, upost_nr)`, behold alle E:G-referanser og radidentiteter, og sammenlign bare `upost_nr=0` med adapterens eksplisitte post-`endring`. Fire RNB-nøkler har to dokumentrader med ulike proposisjoner: de summeres kun i kontrollaggregatet for den felles innstillingsgruppen. Ingen av radene slettes eller omgjøres til flere vedtak.
4. Koblingen mellom vedtaks-ID og innstillingsgruppe er uttrykkelig oppgitt i kontrollgrunnlaget og hentet fra [#2s bevarte hendelsesledger](../issue-2/aar/api_events.csv) med støtte i [beskrivelsesinventaret](../issue-2/aar/description_inventory.csv). Denne sekundære forskningskoblingen brukes til utvalg, mens selve API-beløpet hentes på nytt gjennom dagens adapter. Den gir ingen automatisk faglig hendelsessammenslåing.
5. Fravær har `None`/blankt verdi-felt og egen status. Ingen `get(..., 0)` brukes ved sammenligning. Et beløp med `meaning=uavklart` er ikke et godkjent delta selv om tallet finnes. API-før, -etter, posttotal og underkomponenter er egne observasjoner og legges ikke til endringene.
6. Millionfaktoren testes uten avrunding. Ikke-heltallige kronekandidater får presisjonsavvik. Dokument-D og API er heltall. Inntektsfortegn beholdes slik disse kildene oppgir dem. DFØs motsatte rå inntektsfortegn overføres **ikke** til Excel. Kapittel 1–2999/3000–5999 bestemmer utgift/inntekt.

## Resultater: saldert nivå

| Opprinnelig objekt | API-postnivåer | Excel til stede | Eksakte hele kroner | Ikke-heltallige kronekandidater | Excel mangler |
| --- | ---: | ---: | ---: | ---: | ---: |
| 40032763 | 70 | 70 | 30 | 40 | 0 |
| 40032791 | 112 | 112 | 71 | 41 | 0 |
| 40032850 | 118 | 118 | 100 | 18 | 0 |
| 40032976 | 44 | 44 | 44 | 0 | 0 |
| 40033025 | 31 | 30 | 26 | 4 | 1 |
| **Sum** | **375** | **374** | **271** | **103** | **1** |

Alle 271 sammenligninger med hele kronekandidater er eksakte. Ingen av de øvrige 103 er godkjent gjennom avrunding. Avstanden til API-verdien er i alle disse tilfellene høyst **0,000001 kroner**, men den kontraktsmessige presisjonstolkningen er fortsatt åpen. Blant annet har `Rådata!H2` originalverdi **`14.768000000000001`**, ikke bare visningsverdien 14,768. Multiplikasjon med én million gir **14 768 000,000000001**, mot API 40032763 `table[1]/tr[4]/td[5]` **14 768 000**. Dette er en normaliseringsavklaring, ikke påvist økonomisk uenighet. Alle 103 spor er beholdt i [avviksfilen](pilotkontroll/avvik.csv).

Den manglende nøkkelen er **5999/90**, mens API 40033025 `table[1]/tr[62]/td[4]` har **101 874 353 000 kroner**. Nøkkelen finnes verken i rådata- eller dokumentarket i den kontrollerte arbeidsboken. Fraværet er ikke et observert saldert nullbeløp. Tabellen over bruker det uttrykkelige API-utvalgets 375 nøkler, med 374 i Excel. Den globale nøkkelunionen med alle 1 693 Excel-nøkler er 1 694; de øvrige **1 319** er **utenfor kontrollutvalget**, ikke dokumenterte API-mangler. Ingen av dem er regnet som treff eller fjernet fra arbeidsbokinventaret.

Konkrete strenge nivåtreff er `H1340=-334.642` på 2445/24 mot 40032763 `tr[79]/td[5]` −334 642 000; `H1349=102.5` på 2460/24 mot 40032791 `tr[101]/td[5]` 102 500 000; `H1352=-15` på 2470/24 mot 40032850 `tr[87]/td[5]` −15 000 000; og `H1730=295900` på 5440/24 mot 40032976 `tr[62]/td[5]` 295 900 000 000 kroner. Alle lokatorer har prefiks `table[1]/`. Den negative 2445-verdien er fortsatt en utgiftspost.

## Resultater: dokumentbeløp og eksplisitte endringer

| Gruppe / API-ID | Excel-rader, upost 0 | API-endringer | Felles sammenlignbare nøkler | Eksakte | Beløpsdiff | Excel uten sammenlignbart API-delta | API uten Excel |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| i447/23-24 / 40033719 | 606 | 601 | 600 | 600 | 0 | 2 | 1 |
| i25/24-25 / 40033805 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| i99/24-25 / 40034064 | 69 | 69 | 69 | 69 | 0 | 0 | 0 |
| i93/24-25 / 40034226 | 17 | 18 | 16 | 16 | 0 | 1 | 2 |
| i90/24-25 / 40034287 | 92 | 93 | 92 | 92 | 0 | 0 | 1 |
| i81/24-25 / 40034048 | 2 | 2 | 2 | 2 | 0 | 0 | 0 |
| i94/24-25 / 40034229 | 74 | 74 | 74 | 74 | 0 | 0 | 0 |
| **Sum** | **861** | **858** | **854** | **854** | **0** | **3** | **4** |

Excel-radene gir **857 unike gruppenøkler** fordi fire RNB-nøkler har to rader. Unionen av Excel og tolkede API-deltaer er 861 nøkler; det er et tilfeldig tallmessig sammenfall med antallet Excel-rader. API har ingen gjentatt post-delta-nøkkel innen de sju valgte objektene. De fire Excel-multipler er **288/73 (D163+D164)**, **845/70 (D498+D499)**, **1543/1 (D782+D783)** og **5579/70 (D1307+D1308)**. De respektive kontrollsummene er −90 746 000, −63 000 000, −3 729 000 og −7 029 000 kroner, alle likt API-deltaet. Råreferansene p104 og p106 er bevart som to ulike dokumentbidrag.

Det er viktig å skille tre ulike årsaker bak Excel-rader uten **sammenlignbart** API-delta:

| Konto og kilde | Faktisk funn | Status og konsekvens |
| --- | --- | --- |
| 151/70, i447, `Dokumentiltknyntning2024!D43=0` | Ingen tilsvarende beløpsobservasjon i det replayede RNB-objektet. `Rådata!I70=-20`, mens `K70=0`, støtter at forslag og faktisk endringsaggregat kan avvike. | Bevar observert Excel-null og API-fravær separat. Ingen ny nullhendelse. |
| 228/85, i447, `D124=30000000` | API **har** 30 000 000 i `table[1]/tr[143]/td[5]`, men v2 gir `meaning=uavklart`, `ukjent_ledd`, fordi HTML-tekstuttrekket blir «b evilges med». | Manglende sikker delta-klassifikasjon, **ikke manglende råtall**. Ingen ommerking eller parserretting er utført. |
| 2440/31, i93, `D914=11900000000` | Rå API-rad `table[1]/tr[37]` har posttekst **`(NY) 31`**, «blir løyvd med» og **11 900 000 000** i `td[5]`. V2 bevarer fullteksten, men lager ingen beløpsobservasjon og gir `uklassifisert_rad`. | Konkret dekningsgrense i dagens adapter. Tallet må ikke beskrives som null eller ferdig tolket. |

De fire API-deltaene uten Excel-rad er RNB 5999/90 **−101 874 353 000** (`40033719`, `tr[1487]/td[5]`), nysaldering 5999/90 **+18 497 356 000** (`40034287`, `tr[238]/td[4]`) og de gjentatte Havtil-deltaene i 40034226: 1860/1 **+10 988 000** (`tr[32]/td[5]`) og 4860/1 **−2 400 000** (`tr[43]/td[5]`). Alle lokatorer har prefiks `table[1]/`.

Excel har Havtil-beløpene én gang i i99: **D881=10 988 000** og **D1211=−2 400 000**, likt 40034064. Det avgjør ikke hvilken publisert observasjon som rettslig er additiv. Begge API-identiteter og de tre kjedesperrene **1860/1, 4860/1 og 5999/90** skal fortsatt beholdes. Prøven avdekker ingen ny bekreftet økonomisk kildekonflikt blant de sammenlignbare heltallsbeløpene; den dokumenterer presisjons- og uttrekksgrenser og allerede kjente omfangsforskjeller.

## Stadier og underposter: observerte felt og forskningsavledede deltaer

2541/70 er en konkret kjede der de valgte objektene og arbeidsboken faktisk møtes. Alle beløp nedenfor er kroner etter den prøvde faktoren. Ingen av rådatakolonnene skal importeres som ekstra vedtak i tillegg til dokumentradene.

| Excel-celle og råverdi | Prøvd betydning | Faktisk API-kontrollanker |
| --- | --- | --- |
| `Rådata!H1360=12818` | Saldert nivå | 40032850 `table[1]/tr[92]/td[5]`: 12 818 000 000 |
| `I1360=-608` | RNB-forslagets endring i akkurat denne cellen | Samme tall som vedtatt endring, men forslagsstatusen består |
| `K1360=-608`, dokument `D938=-608000000` | Førstehalvårsaggregat og separat dokumentbeløp | 40033719 `tr[1070]/td[5]`: −608 000 000 |
| `J1360=12210` | Stilling inklusive RNB | 40033719 `tr[1071]/td[3]`, **etterfeltet**: 12 210 000 000 |
| `L1360=0.4`, dokument `D939=400000` | Aggregat etter RNB og separat dokumentbeløp | 40033805 `tr[4]/td[4]`: +400 000 |
| `N1360=680`, dokument `D940=680000000` | Nysald-prop og separat dokumentbeløp | 40034064 `tr[80]/td[5]`: +680 000 000 |

De siste fire API-lokatorene har prefiks `table[1]/`. Adapteren observerer før og etter i samme fysiske celle med ulike `amount_field`; det er ikke to endringer. Den avledede saldoen blir 12 890 400 000 for akkurat denne kildeprøvde kjeden. Rådata G (**Gul bok / forslag**) og M (**lønnsoppgjør**) er ikke uavhengig enhets-/stadiegodkjent av denne prøven. Et tallmessig samsvar for N gjør ikke hele **Nysald-prop** til stortingsvedtak.

For post 24 leverer dagens adapter opprinnelige komponentnivåer og senere **`etter_belop`**, **ikke komponentdeltaer**. `Etter − valgt førnivå` er separat beregnet for tre uttrykkelige par, de samme post-24-presentasjonene som er dokumentert i [#2s komponentledger](../issue-2/aar/component_ledger.json). Dette er forskningsberegning med dokumenterte innganger, ikke ny produksjonsparseratferd:

- **5440/24, 40032976 → 40033719:** fem komponentdifferanser stemmer eksakt mot dokumentcellene **D1232, D1234, D1236, D1238, D1240**. Posttotal går fra 295 900 000 000 til 191 800 000 000. Den **avledede** endringen er −104 100 000 000, lik `Rådata!K1730 × 1 000 000`. `J1730=191800` er et nivå.
- **2470/24, 40032850 → 40034064:** dokumentets **D926=−15 000 000**, **D927=+14 000 000** og **D928=+1 000 000** stemmer med tre komponentdifferanser. De øvrige tre komponentdifferansene er beregnet 0 og har **ingen Excel-dokumentrad**. Posttotalen står uendret −15 000 000. Nullsum er derfor ikke «ingen komponentendring».
- **5440/24, 40033719 → 40034226:** fire ikke-null komponentdifferanser stemmer mot **D1233, D1235, D1237, D1239**. Den femte er beregnet 0 uten Excel-dokumentrad. Ny observert total er 233 300 000 000. Den **avledede** endringen +41 500 000 000 stemmer med `N1730 × 1 000 000`, men N beholder etiketten forslag.

Det gir **16 komponentdifferanser**, **12 sammenlignbare dokumentrader med 12 eksakte treff** og **fire fraværende Excel-rader med beregnet API-differanse 0**. Ingen av de fire fraværene er fylt ut med observert null. Tre posttotalberegninger holdes separat, uten dobbelttelling. [Komponentkontrollen](pilotkontroll/komponentkontroll.csv) har eksakt før-/etter-ID, lokator, beløp, underpost og Excel-celle for alle 19 kontrollrader. Koblingen er avgrenset til disse kildeparene; den er ingen generell regel for rådataarkets underposter.

## Konsekvenser for plan og aksepttester

2024 er startklart som **avgrenset pilotplan** med råkildebevaring, langt observasjonsformat og eksplisitt kontrolluttrekk. Det er ikke startklart som ubetinget normalisert helårsimport. Følgende akseptgrenser følger av prøven:

1. Bevar uendret Excel-original med hash/byteantall, korrekt ark og celle. Alle G:N-celler og dokument-D kan registreres som råobservasjoner før enhet/stadium godkjennes. Original null, manglende rad og uavklart normalisering er egne tilstander. Registrering av nye Storting-tall skal fungere parallelt.
2. Reproduser de **271 eksakte salderttreffene**, og behold **103** ikke-heltallige kronekandidater med rå OOXML-streng og avvik inntil en uttrykkelig presisjonsregel er dokumentert. Ingen skjult avrunding, tusenkroners tilpasning eller sletting av desimalspor. 5999/90 skal være fraværende på Excel-siden, med API-grunnlaget synlig separat.
3. Reproduser de **854** eksakte postendringskontrollene og de **sju** eksplisitte omfangs-/tolkningsrestene. Bevar de fire RNB-multiplenes to dokumentreferanser og separate råverdier. Treff gjelder kontrollaggregat, ikke at hvert dokumentbeløp er et selvstendig vedtak.
4. Bevar dagens v2-resultat for **228/85** og fulltekst-/uttrekksavviket på **2440/31**. Eventuell senere parserutvidelse må ha egen versjon og avgrensede regresjonsprøver. Denne planen løser ikke avvik ved å skrive om eksisterende B1/B2 eller tidligere v1/v2-resultater.
5. Prøv 2541/70 for nivå, forslag, RNB, etter-RNB og høstendring. Prøv post-24-hierarkiet med observerte nivåer og separat forskningsberegning. Nettoresultat, komponent og dokumentaggregat må ikke summeres samtidig. Ingen ny post får automatisk inngående null.
6. Kontroller at begge Havtil-observasjoner og 5999/90 fortsatt sperrer berørt additiv kjede, også når et sluttbeløp eller Excel-aggregat ser rimelig ut. Faglig kontrollavgjørelse, råkilde og beregning skal ha hver sin status.
7. Bruk datasett **historisk** for Excel-adapteren og separat API-adapter. Bevar upost 0, ukjent underpost og konkrete underposter hver for seg. Manglende 2024-organisasjonsoppslag skal synes, men ikke hindre kildebevaring. Replayen har 2 894 `mangler_organisasjonsoppslag` fordi valgt startregister ikke dekker disse historiske kontoene; dette er ikke en beløpsnormaliseringsfeil eller faglig godkjenning.
8. Vis **ikke utført** for full årsavstemming, resterende 38 av de 50 valgte årsobjektene fra #2, andre årganger, generell G/I/J/K/L/M/N-semantikk, regnskap og rettslig løsning av konfliktene. Før en senere helårsgodkjenning må hele årets eksplisitte konto-/stadieutvalg avstemmes fra de faktiske valgte kildene.

## Kontrollartefakter og reproduksjon

De tre små kontrollartefaktene inneholder resultater og kildelokatorer, ingen originalarbeidsbok eller nye private filer:

- [kontrollgrunnlag.json](pilotkontroll/kontrollgrunnlag.json): manifest, kildehash/URL/hentetid, lokale replay-ID-er, inngangs-/adapterhash og antall. Resultat-ID-er kan variere ved en ny B2-database; varig kontrollnøkkel er kildehash + vedtaks-ID + lokator + beløpsfelt.
- [avvik.csv](pilotkontroll/avvik.csv): **111 kontrollrader**: 103 presisjonsspor og åtte øvrige rester, inklusive originalbudsjettets 5999-fravær. `missing_api` betyr fravær av det valgte, sikre deltafeltet, presisert med råkildens innhold der tallet faktisk finnes. Blank beløpsside er fravær, aldri numerisk 0.
- [komponentkontroll.csv](pilotkontroll/komponentkontroll.csv): 16 komponent- og tre separate posttotalberegninger. `derived_delta` er uttrykkelig forskningsavledet; `observed_field=etter_belop` angir hva adapteren faktisk observerte.

Python-oppskriften nedenfor er også kjørt fra en ny scratchdatabase og ga samme antall som manifestet. Den er dokumentasjon av undersøkelsen, ikke produksjonskode. Lagre den utenfor repoet og kjør fra repoets rot, for eksempel med den tilgjengelige bundlete Python-runtime og en scratchmappe som argument. Den henter originalen gjennom Git, verifiserer alle inngangs-/adapterhashene, kjører de eksisterende offentlige grensene, kontrollerer SQLite-rundtur og gjentakelse, og etterprøver tallene i tabellene. Den etterlater en separat scratchdatabase for kontroll. Ingen historisk registergodkjenning eller produksjonsimport kreves for råtallsammenligningen.

```python
"""Kjør fra repoets rot med en skrivbar scratchmappe som eneste argument."""
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path
from zipfile import ZipFile

import openpyxl

root = Path.cwd()
sys.path.insert(0, str(root))
from innlesning import extract_revision, read_extraction, read_sync, sync_saved
from innlesning.observations import Interpretation, encode

manifest = json.loads((root / 'docs/research/historisk-excel/pilotkontroll/kontrollgrunnlag.json').read_text(encoding='utf-8'))
for item in manifest['code_and_research_inputs']:
    assert hashlib.sha256((root / item['path']).read_bytes()).hexdigest() == item['sha256']
book = manifest['workbook']
raw = subprocess.check_output(['git', 'show', book['git_revision'] + ':' + book['path']])
assert len(raw) == book['bytes']
assert hashlib.sha256(raw).hexdigest() == book['sha256']
wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=False)
ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with ZipFile(io.BytesIO(raw)) as archive:
    cells = {
        i: {c.attrib['r']: c.find('m:v', ns).text
            for c in ET.fromstring(archive.read(f'xl/worksheets/sheet{i}.xml')).findall('.//m:c', ns)
            if c.find('m:v', ns) is not None and c.attrib.get('t', 'n') == 'n'}
        for i in (1, 2)
    }
rawrows = defaultdict(list)
for n, row in enumerate(list(wb.worksheets[0].values)[1:], 2):
    rawrows[tuple(row[1:3])].append(Decimal(cells[1][f'H{n}']) * 1000000)
docrows = defaultdict(list)
for n, row in enumerate(list(wb.worksheets[1].values)[1:], 2):
    docrows[(row[5], *row[:3])].append(Decimal(cells[2][f'D{n}']))

observations = []
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(exist_ok=True, parents=True)
directory = tempfile.mkdtemp(prefix='p13-replay-', dir=scratch)
database = Path(directory) / 'replay.sqlite'
for source in manifest['sources']:
    path = root / source['fixture']
    blob = path.read_bytes()
    assert hashlib.sha256(blob).hexdigest() == source['sha256']
    metadata = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
    job = sync_saved(database, blob, metadata, historical_sample=True, decision_id=source['id'])
    revision = read_sync(database, job).entries[0].revision_id
    interpretation = Interpretation(adapter_version='storting-belop-v2')
    extraction = extract_revision(database, revision, interpretation=interpretation)
    assert interpretation.id == manifest['adapter_interpretation_id']
    assert encode(asdict(extraction)) == encode(asdict(read_extraction(database, extraction.id)))
    assert extraction == extract_revision(database, revision, interpretation=interpretation)
    assert len(extraction.observations) == source['count']
    observations.extend(extraction.observations)

original = Counter()
for o in observations:
    if (o.meaning, o.detail_level) != ('nivaa', 'post'):
        continue
    values = rawrows.get((int(o.chapter), int(o.post)))
    if values is None:
        original['missing_excel'] += 1
    else:
        amount = sum(values, Decimal(0))
        status = 'fractional_kr' if amount != amount.to_integral_value() else 'match' if amount == o.amount_kr else 'difference'
        original[status] += 1
assert dict(original) == manifest['summary']['original_H']['status_counts']
print('Saldert H:', dict(original))
for identifier, group in manifest['source_group_mapping'].items():
    api = defaultdict(list)
    for o in observations:
        if o.api_id == identifier and (o.meaning, o.detail_level) == ('endring', 'post'):
            api[(int(o.chapter), int(o.post), 0)].append(o)
    excel = {k[1:]: values for k, values in docrows.items() if k[0] == group and k[3] == 0}
    statuses = Counter()
    for key in set(api) | set(excel):
        a, e = api.get(key), excel.get(key)
        status = 'missing_excel' if e is None else 'missing_api' if a is None else 'multiple_api' if len(a) != 1 else 'match' if sum(e, Decimal(0)) == a[0].amount_kr else 'difference'
        statuses[status] += 1
    assert dict(statuses) == manifest['summary'][group]['status_counts']
    print(group, dict(statuses))

component_status = Counter()
for before_id, after_id, chapter, group in [
    ('40032976', '40033719', '5440', 'i447/23-24'),
    ('40032850', '40034064', '2470', 'i99/24-25'),
    ('40033719', '40034226', '5440', 'i93/24-25'),
]:
    before = {o.subpost: o for o in observations if (o.api_id, o.chapter, o.post) == (before_id, chapter, '24')}
    after = {o.subpost: o for o in observations if (o.api_id, o.chapter, o.post) == (after_id, chapter, '24')}
    for code, o in after.items():
        delta = o.amount_kr - before[code].amount_kr
        e = docrows.get((group, int(chapter), 24, int(code))) if code is not None else None
        status = 'post_total_separate' if code is None else 'match' if e is not None and sum(e, Decimal(0)) == delta else 'missing_excel_zero_delta' if e is None and delta == 0 else 'difference'
        component_status[status] += 1
assert dict(component_status) == manifest['components']
print('Komponenter:', dict(component_status))
assert len(observations) == manifest['summary']['fixture_observations'] == 2894
assert hashlib.sha256(raw).hexdigest() == book['sha256']
wb.close()
```

Originalhashen er fortsatt uendret. Ingen produksjonskode, originalfil, GitHub-status eller faglig avgjørelse er endret av denne kontrollen.
