# Issue 2 – full årsavstemming for budsjettåret 2024

Kontrollert 20. oktober 2026. Leveransen er en kildeundersøkelse med lokale kontrollfiler. Produksjonskode og GitHub-innhold er ikke endret. Språkprofilen `fin-spraak` er brukt. «Kildeobservasjon» betegner lest originalinnhold; «kontroll» betegner utførte beregninger; «vurdering» betegner konklusjoner på dette grunnlaget.

## Bevaring i repoet

Denne rapporten gjengir den fullførte årsundersøkelsen. CSV-ledgere, de opprinnelige DFØ-feltene for alle 4 268 2024-rader, de 2 935 API-posthendelsene og inventar for alle 2 183 vedtak er versjonert her. Store opprinnelige HTTP-svar og PDF-er samt undersøkelsesskripter er bare mellomlagret lokalt; URL-er og SHA-256 er dokumentert. Lokale filstier og skriptlisten nedenfor beskriver undersøkelsesøkten og er ikke en installasjonsveiledning. Dette er statisk kildegrunnlag, ikke en produksjonsparser.

[Sluttposter](post_ledger.csv) · [Kilde/post-ledger](source_ledger.csv) · [Hele API-inventaret](session_inventory.csv) · [API-hendelser](api_events.csv) · [Før/etter-kjeder](chain_ledger.csv) · [Alle DFØ-rader for 2024](dfo2024.csv) · [Regnskapsavstemming](statsregnskap_ledger.csv) · [43 omfangsforskjeller](scope_residual_ledger.json) · [Seks hendelsesavvik](residual_ledger.json) · [Kontrollutfall](verification.json)

## Konklusjon og avgrenset godkjenning

**DFØs sluttbevilgning for hele 2024 er avstemt mot hele bevilgningskolonnen i Statsrekneskapen 2024. Denne sluttavstemmingen er godkjennbar. En fullstendig, sammenhengende kjede av stortingsvedtak er fortsatt ikke godkjennbar for tre poster.** Kildekonfliktene gjelder 1860/01, 4860/01 og 5999/90. De er avgrenset og tallfestet nedenfor. Kontrollen er utvidet fra fire prøveposter til alle årgangens rader og poster.

- Alle **4 268 DFØ-rader**, **1 638 DFØ-poster** og **41 beskrivelser** er inventert. **3 165 rader** gjelder årets bevilgning; **1 103 rader** gjelder overføring mellom år.
- Alle **1 655 poster** i statsregnskapets tabell 2.1 og 2.2 inngår. På de **1 625 felles nøklene** er differansen i årets bevilgning **0 kroner på hver post**. Begge kilder har **1 614 poster med en sluttbevilgning forskjellig fra null**, med fullstendig beløpssamsvar.
- De **30 PDF-postene uten DFØ-nøkkel** har alle null i Løyving og ikke-null regnskapsutfall. De **13 DFØ-postene uten PDF-nøkkel** er dokumenterte bevilgninger som senere er reversert til null. Alle 43 omfangsforskjeller er ført separat. Manglende felt er ikke erstattet med et oppdiktet nullbeløp.
- Samtlige felles utgiftsposter, **1 189**, stemmer også for overført fra 2023, samlet bevilgning og overført til 2025. Hele kolonnene summerer til henholdsvis **20 803 386 000**, **2 972 710 197 000** og **22 821 878 000 kroner** i begge kilder.
- Hele Blå bok-tabellen, **1 574 poster**, stemmer post for post med de **24 identifiserte opprinnelige API-vedtakene**. DFØs saldertrader dekker 1 573 av disse. Finansieringspost 5999/90 har en særskilt historikkforskjell.
- De to sesjonsresponsene inneholder **2 183 unike vedtak**. De **50 identifiserte bevilgningstabellene for 2024** gir **2 935 posthendelser**: 1 574 opprinnelige beløp og 1 361 senere posthendelser. **2 930 hendelser, 99,83 pst.**, samsvarer beløpsmessig med DFØ etter gruppering på kilde/kapittel/post.
- En bokstavelig summering av API-hendelsene gir tre avvikende sluttsaldoer. **1 627 av 1 630 årsbevilgningsposter, 99,82 pst.**, stemmer med DFØ. Totalsamsvar etter en manuell justering ville ikke dokumentere en komplett hendelseskjede.

Ingen manglende offentlig råfil hindrer nå 2024-avstemmingen. Restarbeidet gjelder tolkning/retting av konkrete primærkildekonflikter og faglig behandling av disse tre kjedene.

## Primærkilder, tidsrom og enheter

1. **DFØ, full historikk over bevilgninger.** Lagret CSV fra den offisielle ZIP-en, hentet 20. oktober 2026 kl. 11:36:08 UTC. Kontrolluttrekket er alle rader med `År=2024`. Beløp er kroner, med tre desimaler i råfilen; de aktuelle verdiene kan representeres eksakt som hele kroner. Råfilen er Windows-1252, semikolondelt, med desimalkomma. Identifikatorer leses som tekst. [Nedlastingsside](https://statsregnskapet.dfo.no/last-ned), [ZIP](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_full_historikk.zip), [kolonnebeskrivelse](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_beskrivelse_av_kolonner.csv).
2. **Stortingets vedtaks-API, sesjonene 2023–2024 og 2024–2025.** Lagrede svar hentet kl. 11:35:51 og 11:36:10 UTC. Vedtaksdatoene i unionen går fra 5. oktober 2023 til 20. juni 2025. De identifiserte 2024-bevilgningene omfatter opprinnelige vedtak 14.–20. desember 2023 og endringer 19. juni–19. desember 2024. Beløpstabellene angir kroner. [2023–2024](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2023-2024), [2024–2025](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), [API-dokumentasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/).
3. **Blå bok 2024.** Lagret PDF hentet kl. 11:35:12 UTC. Hele posttabellen på PDF-sider 11–74, trykte sider 9–72, er trukket ut. Disse tabellene bruker kroner. Oppsummeringer tidligere i dokumentet bruker en annen enhet og er ikke lest inn som posthendelser. [Original PDF](https://www.stortinget.no/globalassets/pdf/budsjettsiden/blaabok_2024.pdf).
4. **Meld. St. 3 (2024–2025), Statsrekneskapen 2024, vedlegg 2.** Offisiell PDF hentet kl. 11:55:23 UTC. Tabell 2.1 dekker utgifter på PDF-sider 92–169 og tabell 2.2 inntekter på sider 170–199. Enheten er **1 000 kroner**; denne kontrollen multipliserer med 1 000. Kolonnen **Løyving** brukes for årets bevilgning. **Samla løyving** kontrolleres separat. **Rekneskap** summeres ikke inn i bevilgningskjeden. [Dokumentforside](https://www.regjeringen.no/no/dokumenter/meld.-st.-3-20242025/id3097946/), [offisiell PDF](https://www.regjeringen.no/contentassets/1d45fede74ff4ef18ce06bbd6163c723/nn-no/pdfs/stm202420250003000dddpdfs.pdf).
5. **Sakskoblinger og direkte vedtakssider.** Lagret API-respons for saker i 2024–2025 knytter høstvedtakene til innstilling og proposisjon. Tre direkte vedtakssider ble hentet kl. 12:03:06 UTC for kontroll av konfliktene. Alle ga HTTP 200. Den komplette API-teksten er gjenfunnet i den tilsvarende nettsiden for alle tre. [Saker 2024–2025](https://data.stortinget.no/eksport/saker?sesjonid=2024-2025).

Kravene er lest fra [docs/krav.md](https://github.com/depmartin/budsjetthistorikk/blob/main/docs/krav.md), GitHub-blob `9d4e2ec0832580129158532b5c0dce15565da212`, og [docs/kildefunn.md](https://github.com/depmartin/budsjetthistorikk/blob/main/docs/kildefunn.md), blob `e6f57d487c9acab966702df105dc412e0c7107ad`. De er kravkontekst. Tallkontrollene bygger på de offentlige primærkildene.

## Faktiske kontroller av alle DFØ-rader

| Radtype | Rader | Unike poster innen typen | Sum utgifter, kroner | Sum inntekter, kroner |
|---|---:|---:|---:|---:|
| Saldert | 1 754 | 1 573 | 2 951 103 483 000 | 2 849 229 130 000 |
| Senere bevilgningsrader | 1 411 | 990 | 803 328 000 | 102 677 681 000 |
| Overført fra 2023 | 540 | 535 | 20 803 386 000 | 0 |
| Overføres til 2025 | 563 | 559 | 0 i Bevilgning_beløp | 0 |

Inntekter er normalisert til bevilgningens fortegn. DFØ lagrer inntektsbevilgninger med motsatt fortegn fra vedtakene/PDF-tabellen. Normalisering skjer etter kapittelnummer: kapittel 3000–5999 skifter fortegn. Negative beløp beholdes deretter, blant annet netto driftsresultat og negativt inntektsanslag. Regelen er kontrollert på hele 2024-materialet ved eksakt postvis samsvar med statsregnskapet. Den er ikke gjennom denne undersøkelsen prøvd på andre år.

Alle 4 268 rader har `Periode=202401`. `Tildelings_periode` har åtte verdier: 202401 (2 857 rader), 202404 (3), 202405 (600), 202406 (31), 202409 (1), 202410 (2), 202411 (770) og 202412 (4). Dette er ikke Stortingets vedtaksdatoer. Eksempelvis er DFØ-raden merket 27. september for Prop. 121 S knyttet til vedtak 5. november. Datoene er bevart i hver sin betydning.

På **alle 540 overføringsrader fra 2023** er `Bevilgning_beløp = Bevilgning_overført_beløp`, og feltet overføres til neste år er null. De **563 radene til 2025** har null i Bevilgning_beløp og bare beløp i `Bevilgning_overføres_beløp`. Samtlige 3 165 øvrige rader har null i begge overføringsfelt. Årets bevilgning er derfor i denne årgangen summen av Bevilgning_beløp fratrukket overført fra 2023, eller ekvivalent summen av de 3 165 årsradene. Årets utgifter og inntekter blir begge **2 951 906 811 000 kroner**.

Rader med lik beskrivelse er ikke deduplisert. De 1 754 saldertradene blir 1 573 postbeløp. Oppsplitting kan være administrative delbeløp eller underkomponenter. DFØ gir ingen vedtaks-ID og heller ikke entydige identifikatorer for alle delbeløpene. Koblingen er derfor dokumentert på summeringsnivå kilde/kapittel/post, med alle originalrader bevart. **Alle 41 beskrivelser**, tilknyttede API-ID-er, rad-/postantall og delsummer står i `description_inventory.csv/json`.

## Opprinnelig budsjett og hele API-inventaret

Alle **1 574 Blå bok-poster** stemmer eksakt med de identifiserte 24 opprinnelige API-tabellene. Uttrekket ga 1 574 unike nøkler og ingen uavsluttede beløp. Tabellen summerer til **2 951 103 483 000 kroner i både utgifter og inntekter**, inklusive finansieringspost 5999/90. Alle 1 573 poster i DFØs saldertrader stemmer etter summering. Den eneste opprinnelige API-/Blå bok-posten uten DFØ-saldertrad er 5999/90 = **101 874 353 000 kroner**.

PDF-uttrekket bruker post- og beløpskolonne, slik at kapittelsummer og departementssummer ikke telles som poster. Netto post 24 beholdes som posttotal. PDF-sidene 54 og 74, trykte sider 52 og 72, er også gjengitt og visuelt kontrollert, særlig Statsbyggs komponenter, kapittel 5685 ved sideskifte og statslånemidlene. Tidligere visuell kontroll av trykt side 9 er gjenbrukt. Samtlige 64 tabellsider er maskinlest; de er ikke alle manuelt kontrollert linje for linje.

| Sesjon | Vedtak | BUDSJETT | ANNET | ANMOD | RO | GRUNNLOV | Vedtak med HTML-tabell |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023–2024 | 923 | 225 | 426 | 268 | 3 | 1 | 139 |
| 2024–2025 | 1 260 | 257 | 517 | 485 | 1 | 0 | 154 |

Ingen ID kolliderer i unionen på 2 183 vedtak. Inventaret bevarer metadata og utvalgsklassifisering for hvert vedtak. De 50 bevilgningstabellene består av **24 BUDSJETT** med opprinnelige beløp og **26 ANNET** med senere 2024-hendelser. Et BUDSJETT-filter ville miste samtlige 1 361 identifiserte senere posthendelser i denne årgangen.

Kandidatene er funnet fra eksplisitt budsjettår og bevilgningsinnhold. To høstvedtak, **40034048** og **40034229**, begynner direkte med tabelloverskriften uten standardinnledningen om statsbudsjettet. De er funnet gjennom tabellheader og sak/tittel. Et filter bare på standardinnledningen ville miste **76 posthendelser**. Alle 50 vedtak med saks-ID, dato, nummer, URL og dokumentreferanser står i `decision_inventory.csv/json`.

Øvrige objekter er bevart som annet innhold (1 641), fullmakt/samtykke (433), annet uttrykkelig budsjettår (49) eller eget Svalbardbudsjett (10). Dette er maskinelle inventarklasser, ikke en generell semantisk garanti. Et ekstra søk etter 2024 og konkrete beløpsoperasjoner i ikke-valgte objekter ga bare skattevedtak **40032731**, som fastsetter skatteregler. De 140 tabellobjektene som nevner 2024 er dermed ikke 140 bevilgningsendringer. Svalbardbudsjettets interne kapittelserie er adskilt; statsbudsjettets kap. 480 inngår.

DFØ-radene er gruppert på innstilling og post, med saldert som egen gruppe. Flere proposisjoner og egne komitéendringer kan inngå i én innstilling. RNB-gruppen i447/23–24 omfatter Prop. 104 S, Prop. 106 S og egne i447-rader. Høstens proposisjoner er også delt mellom komiteer. Verken proposisjonsnummer eller departementsnavn alene er en unik hendelsesnøkkel.

| Kontrolltrinn | Omfang | Eksakt samsvar | Uavklart/avvik |
|---|---:|---:|---:|
| DFØ-årsbeløpsrader mot API etter kilde/post-gruppering | 3 165 | 3 163 rader, 99,94 pst. | 1 nullrad uten API-hendelse; 1 sluttbeløpsrad 5999/90 |
| API-posthendelser mot DFØ-kilde/post | 2 935 | 2 930, 99,83 pst. | 4 API-hendelser uten DFØ-motpart; 1 ulikt beløp |
| Bokstavelig API-saldo mot DFØ | 1 630 poster | 1 627, 99,82 pst. | 3 poster |
| Blå bok mot opprinnelig API-beløp | 1 574 poster | 1 574 | 0 |
| DFØ mot Løyving på felles nøkler | 1 625 poster | 1 625 | 0 beløpsavvik |

De 3 163 avstemte DFØ-radene utgjør **6 794 851 289 000 kroner**, eller **98,26 pst.**, av den absolutte verdien av årsradene på 6 915 222 998 000 kroner. Denne absoluttsummen er et teknisk dekningsmål med inntekter, utgifter og positive/negative komponenter; den er ikke et budsjettaggregat. Finansieringsposten forklarer gjenværende beløpsmasse. Den ene øvrige raden er null.

`source_ledger.csv/json` inneholder **alle 2 936 kilde/post-kombinasjoner**, inklusive seks ikke-eksakte statuser. Originalradnummer og API-ID/tabellrad bevarer beviset for koblingen. Fravær og observert null har ulike statuser.

## Før-/etter-kjeden og underposter

Av 1 361 senere posthendelser har **1 303 eksplisitte fra-/til-beløp**. Alle oppfyller lokal aritmetikk før + endring = etter. På **1 299** stemmer førbeløpet også med rekonstruert foregående saldo. Én hendelse, 4700/85 i vedtak 40034212, oppgir eksplisitt førbeløp null uten opprinnelig post og har dokumentert nullstart. De siste tre har kjedekonflikt, jf. residualene nedenfor.

**55 hendelser** har uttrykkelig ny post og bevilgningsbeløp uten fra-/til-par. De er bevart med dette kildegrunnlaget. For **tre post-24-hendelser** som oppgir nytt driftsresultatnivå er endringen beregnet fra forrige dokumenterte nivå. Den trykte nye totalen er ikke lagt til som delta.

Alle **sju post-24-presentasjoner** – fire opprinnelige og tre senere – er også kontrollert på underkomponentene. Ikke-null komponentbeløp/-endringer stemmer som multiset med DFØs delrader. Nettoresultatet summeres én gang. 2470/24 har uendret netto **−15 000 000 kroner** ved høstvedtaket, mens komponentene endres med **−15 000 000**, **+14 000 000** og **+1 000 000 kroner**. En kontroll bare av posttotal ville miste denne strukturelle endringen. For 5440/24 er RNB-nivået **191 800 000 000** og høstnivået **233 300 000 000 kroner**; beregnede endringer er **−104 100 000 000** og **+41 500 000 000 kroner**. Hele kontrollen står i `component_ledger.json`.

## Hele årsavstemmingen mot statsregnskapet

Varig PDF og tabelluttrekk fra den separate råkildekontrollen er brukt som input. Dette arbeidet har deretter koblet **alle** DFØ-poster og rekonstruerte API-beløp. SHA256 for original PDF og brukt avledet uttrekk inngår i inputmanifestet.

| Kontrollkolonne | DFØ, kroner | Statsrekneskapen, kroner | Differanse |
|---|---:|---:|---:|
| Årets bevilgning, utgifter | 2 951 906 811 000 | 2 951 906 811 000 | 0 |
| Årets bevilgning, inntekter | 2 951 906 811 000 | 2 951 906 811 000 | 0 |
| Overført fra 2023, utgifter | 20 803 386 000 | 20 803 386 000 | 0 |
| Samlet disponibel bevilgning, utgifter | 2 972 710 197 000 | 2 972 710 197 000 | 0 |
| Overført til 2025, utgifter | 22 821 878 000 | 22 821 878 000 | 0 |

Dette er også en postvis kontroll: alle **1 625 felles poster**, herav **1 189 utgiftsposter** og **436 inntektsposter**, har eksakt samsvar for årets bevilgning. De fire utgiftskolonnene stemmer på hver felles utgiftspost. Hele nøkkelforskjellen er avklart for bevilgningskolonnen:

**13 DFØ-poster uten PDF-rad:** 0325/71, 0648/21, 1645/23, 2460/58, 2460/90, 3400/02, 3634/85, 4400/02, 4634/86, 5572/74, 5605/89, 5614/81 og 5672/85. Alle har dokumentert opprinnelig bevilgning og senere reversering til null i både DFØ og API. Ingen har overføring inn/ut. Beviset, inklusive begge vedtaks-ID-er og beløp, er ført for hver post i `scope_residual_ledger.csv/json`. En katalog bare fra årsregnskapets sluttabell ville eksempelvis miste både bevilgningen og reverseringen på 2460/58, hver på **1 750 000 000 kroner**.

**30 PDF-poster uten DFØ-rad:** 0100/89, 0140/89, 0740/61, 0740/70, 0740/71, 0740/72, 0740/73, 3061/03, 3100/89, 3140/89, 3200/02, 3320/03, 3451/40, 3455/01, 3571/90, 3853/01, 4100/40, 4313/02, 4520/02, 4531/01, 4540/04, 4550/85, 4800/10, 4820/03, 4820/10, 4860/10, 5309/96, 5341/91, 5440/85 og 5603/81. Alle har null i årets Løyving og ikke-null regnskapsutfall. På de sju utgiftspostene er også overførings- og samlet bevilgningskolonne null. Dette forklarer nøkkelforskjellen i den kontrollerte bevilgningskolonnen. Fullmakten eller annen regnskapsføringshjemmel bak hvert regnskapsutfall er ikke kartlagt og kan ikke utledes fra regnskapsbeløpet. Radene skal ikke konstrueres som bevilgningshendelser.

**Åtte DFØ-poster har bare overført bevilgning fra 2023:** 0457/21, 0646/71, 0882/61, 0922/51, 0922/76, 1148/72, 1500/45 og 1541/61. De har ingen identifisert årsbevilgningshendelse i 2024, men finnes i statsregnskapet med null i årets Løyving. Overføringsbeløpene stemmer. De er dermed ikke manglende årets bevilgning.

`statsregnskap_ledger.csv/json` dekker unionen på **1 668 nøkler** og skiller faktisk tilstedeværelse fra beløp lik null. `post_ledger.csv/json` dekker alle 1 638 DFØ-poster med saldert, endringer, overføring inn/ut, API-saldo og residual. `scope_residual_ledger.csv/json` har alle 43 omfangsforskjeller, inklusive PDF-side og faktisk regnskapsbeløp eller API-bevis for reversering.

## Eksplisitt residualledger for hendelseskjeden

Residual er **DFØ-beløp minus API-beløp**, normalisert til vedtakets fortegn. «Mangler» er fravær av tilsvarende rad, ikke observert null. Maskinfilen bevarer forskjellen.

| Rest | Gruppe / post | DFØ | API | Residual, kroner | Status |
|---|---|---:|---:|---:|---|
| R1 | Saldert, 5999/90 | Mangler | 101 874 353 000 | −101 874 353 000 | API og Blå bok har original finansiering; ingen DFØ-saldertrad |
| R2 | i447/23–24, 5999/90 | Mangler | −101 874 353 000 | +101 874 353 000 | RNB reduserer eksplisitt til null; ingen DFØ-endringsrad |
| R3 | i90/24–25, 5999/90 | 120 371 709 000 | +18 497 356 000 | +101 874 353 000 | DFØ-raden er numerisk sluttbeløpet; vedtaket viser endring fra opprinnelig beløp |
| R4 | i93/24–25, 1860/01 | Mangler | +10 988 000 | −10 988 000 | Samme før/endring/etter gjentas etter tidligere vedtak |
| R5 | i93/24–25, 4860/01 | Mangler | −2 400 000 | +2 400 000 | Samme før/endring/etter gjentas etter tidligere vedtak |
| R6 | i447/23–24, 0151/70 | 0 | Mangler | 0 | DFØ-nullrad uten funnet beløpshendelse |

### R1–R3: finansieringspost 5999/90

[Opprinnelig vedtak 40033025](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033025&p=95566) og Blå bok oppgir **101 874 353 000 kroner**. [RNB, vedtak 857 / 40033719](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033719&p=98919) reduserer med samme beløp til null. [Nysaldering, vedtak 428 / 40034287](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034287&p=100289) viser derimot **fra 101 874 353 000 til 120 371 709 000**, med endring **+18 497 356 000 kroner**. Nysalderingens førbeløp er dermed **101 874 353 000 kroner høyere** enn saldoen etter bokstavelig innlesing av RNB.

DFØ har bare én 2024-rad for posten, på **120 371 709 000 kroner**, merket 19. desember, Prop. 36 S / Innst. 90 S. Statsregnskapets Løyving er samme sluttbeløp. En regel som behandler alle DFØ-rader merket proposisjon som endringer, vil derfor være feil her. Summering av alle API-deltaene gir **18 497 356 000 kroner**, mens nysalderingens etterbeløp og begge sluttkilder er **120 371 709 000 kroner**.

**Status:** Sluttsaldo er verifisert; den bokstavelige kjeden har et dokumentert brudd. En særskilt finansierings-/oppsummeringssemantikk, manglende hendelse eller kilderettelse må dokumenteres fra behandlingsgrunnlaget før kjeden godkjennes. Forskjellen kan ikke lukkes ved å oppfinne en mellomliggende økning. Den direkte nysalderingssiden bekrefter API-teksten, så en ren API-parsingsfeil forklarer ikke funnet.

### R4–R5: gjentatte Havindustritilsynet-beløp

[Vedtak 40034064, 17. desember 2024](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034064&p=100898), Innst. 99 S, endrer 1860/01 **349 324 000 → 360 312 000** og 4860/01 **85 800 000 → 83 400 000 kroner**. [Vedtak 365 / 40034226, 18. desember](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034226&p=100894), Innst. 93 S, gjentar de samme før-/etterbeløpene og deltaene.

DFØ har endringene én gang, under p17/24–25 i99/24–25. Statsregnskapets Løyving er **360 312 000** og **83 400 000 kroner**. Bokstavelig tillegg av begge vedtak gir **371 300 000** og **81 000 000 kroner**. Første vedtaks etterbeløp stemmer ikke med andre vedtaks førbeløp.

**Konflikten er bekreftet på nettsidene.** Sakshenvisningen for energivedtaket oppgir dessuten «unntatt kap. 1860 og 4860». Dette taler for overlapp i kildepublisering eller saksavgrensning, men fastslår ikke hvilket rettslig vedtak som skal anses rettet. Hele API-teksten finnes på de respektive direkte vedtakssidene. Automatisk deduplisering bare etter like beløp ville kunne fjerne reelle, like endringer i andre saker.

**Status:** Sluttsaldo er verifisert. Gjentatte observasjoner og kildekonflikt skal bevares. Innstilling og møte-/voteringsreferat eller utgiverens rettelse må underbygge at den senere observasjonen ikke er en ny additiv endring før dette brukes som godkjent kjederegel.

### R6 og øvrig reststatus

0151/70 har en DFØ-rad på nøyaktig null under RNB. Posten finnes med øvrig budsjettgrunnlag. Ingen konkret nullendring er funnet i RNB-tabellen. Raden står som **nullrad uten beløpshendelse**, med residual null og bevart råspor. Den skal ikke telles som et nytt stortingsvedtak.

De 43 nøkkelforskjellene er avklart for bevilgningsavstemmingen ovenfor. **Ingen kroner-residual står ufordelt mellom DFØ og statsregnskapets årsbevilgning eller overføringskolonner.** Tre kjedekonflikter står åpne som kilde-/hendelsesavvik. Bokstavelige API-sluttsummer er **2 951 917 799 000 kroner i utgifter** og **2 850 030 058 000 kroner i inntekter**, mens begge kontrollerte sluttkilder er **2 951 906 811 000** i hver gruppe.

## Forvekslingsrisikoer før bygging

- **Fullmaktsramme og bevilgning:** Overskridelsesfullmakter på 272 mill. kroner i vedtak 40033720 og 3 mill. kroner i 40033723 er samtykker med rammer. De er ikke lagt til som eksplisitt vedtatte endringsbeløp. Et regnskapsutfall på en nullbevilget post dokumenterer heller ikke et manglende bevilgningsvedtak. Fullmakt og eventuell bruk må ha egne objekter. [RNB-saken](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=98919).
- **Overføring og årets vedtak:** Overført fra 2023 inngår i DFØs disponible beløp og i Samla løyving. Å summere dette inn i årets vedtatte bevilgning ville øke utgiftene med **20 803 386 000 kroner**. Overført til 2025 er egen kolonne, ikke negativ 2024-endring.
- **Stikkord og beløp:** Vedtak 40034066 tilføyer «kan overførast» på 0634/79. Det er et faktisk tekstvedtak uten nytt beløp og må bevares. [Sak 100898](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=100898).
- **Oppdrag og regnskapsutfall:** Utredningsoppdrag, godtgjørelsessatser, skatteregler og samtykke til fremtidige forpliktelser er ikke kapittel/post-bevilgninger. Referanser og tall er utilstrekkelige kjennetegn. Komitéfordelingen i vedtak 40031491 er et konkret tabellrikt eksempel uten nye bevilgningsbeløp.
- **Nettopost, komponent og oppsummering:** Posttotal og underposter trenger hierarki. Oppsummerte nivåer må skilles fra deltaer. SPKs nullsummerende komponentendring og de tre nivåtabellene viser dette i faktiske kilder. 5999/90 viser at en sluttsum også kan stå i en DFØ-rad med beskrivelse som peker på et endringsvedtak.
- **Forslag og vedtak:** DFØ peker ofte på proposisjonsdato/-nummer, mens innstilling og vedtak kan være fordelt mellom komiteer. Regjeringsforslag skal ikke erstatte vedtatt endring. Kildedato, vedtaksdato og registreringsperiode må holdes adskilt.

## Begrensninger, manglende avklaringer og anbefalt aksept

**Faktisk utført:** Hele 2024-årgangen er inventert og avstemt. Alle Blå bok-poster er kontrollert mot opprinnelig API, og hele statsregnskapets bevilgningskolonner er koblet. Alle ikke-eksakte hendelses-/nøkkelstatuser finnes i eksplisitte kontrollfiler. Arbeidet omfatter postvis kontroll, kildegruppert kontroll, lokal aritmetikk, kjedekontroll og komponentkontroll. Totalsamsvar brukes ikke som bevis på komplett hendelseshistorikk.

**Begrensninger:** API-inventaret dekker de to faktisk lagrede sesjonene. Det er ingen uavhengig garanti for at alle historiske rettslige hendelser er korrekt publisert. Klassifisering av øvrige objekter er regelbasert og bevarer alle objektene for kontroll. Statsregnskapets tabelluttrekk har etter den separate råkildekontrollen eksakt samsvar i Løyving mot alle 594 kapittelsummer og begge totalsummer. Alle 108 tabellsider er ikke manuelt kontrollert. PDF gir i prinsippet tusenkroners presisjon; her er samsvaret eksakt etter enhetskonvertering. Ingen dekningskonklusjon for andre budsjettår følger automatisk.

Statsregnskapets trykte kapittelsum for **overført fra 2023** på kap. 0702 viser `103 0101`. Postene summerer til **103 011 i 1 000 kroner** og stemmer med DFØ og samlet bevilgning minus årets bevilgning. Avviket er bevart i råkildekontrollen og gir ingen postvis residual her. Små avrundingsdifferanser i regnskaps-/avvikskolonnene er heller ikke rettet eller brukt til å endre bevilgningsbeløp.

**Det som faktisk mangler for full hendelsesaksept:**

1. Dokumentert behandlings-/rettelsesforklaring for gjentatt publisering av 1860/01 og 4860/01 i 40034064 og 40034226, slik at observasjonene får korrekt hendelsesrolle.
2. Dokumentert finansierings-/vedtakssemantikk eller rettelse som forklarer hvorfor RNBs null på 5999/90 følges av et førbeløp lik originalbudsjettet i nysalderingen. Ingen økning skal konstrueres fra differansen alene.
3. Faglig beslutning om hvordan bekreftede kildekonflikter vises og sperres i godkjente analysetall. Kildeobservasjon, beregnet kjede og kontrollert sluttsaldo trenger hver sin status.

**Anbefalt aksept:** Godkjenn hele 2024-sluttavstemmingen DFØ ↔ statsregnskapet og originalbudsjettet API ↔ Blå bok som verifiserte kontrollgrunnlag. Bevar de tre postenes sluttsaldo som kontrollert kildetall. Hele årets hendelsesdekning bør fortsatt ha status **uavklart på tre poster**, uten automatisk tilpasning for å få totalsummer til å stemme. Kildeundersøkelsen gir nå konkret grunnlag for kontrollgrensene før bygging, men ikke et ubetinget komplett-stempel på alle kjedene.

## Revisjonsspor og kontrollfiler

`input_manifest.json` angir faktiske SHA256, byteantall og stier for brukte råfiler, nedlastingsmanifester og statsregnskapsuttrekket. Arvede filer har sine opprinnelige hentetider i originalmanifestene. `web_manifest.json` har URL, UTC-tid, HTTP-status, byteantall og SHA256 for de tre nye vedtakssidene. Etter vanlig DNS-feil i sandkassen ble samme ordinære offentlige forespørsler kjørt med nettverkstilgang. Ingen innlogging, omgåelse eller pakkeinstallasjon ble brukt. `derived_manifest.json` gir hash for avledede kontrollfiler, skript og rapport; manifestet selv holdes utenfor.

Alle nye filer nedenfor ligger i `work/issue2/fortsettelse/aar/`:

| Kontrollfil | Innhold |
|---|---|
| `dfo2024.csv/json` | Alle 4 268 rader, råfilradnummer, opprinnelige felt og normalisering |
| `description_inventory.csv/json` | Alle 41 beskrivelser, delsummer og API-grupper |
| `session_inventory.csv/json`, `api_all.json` | Alle 2 183 vedtak, utvalgsstatus og bevart full API-tekst |
| `decision_inventory.csv/json` | Alle 50 valgte vedtak med metadata og primær-URL |
| `api_events.csv`, `api_events_derived.json` | Alle 2 935 posthendelser, originalrad, delta/fra/til og nivågrunnlag |
| `source_ledger.csv/json` | Alle 2 936 kilde/post-kombinasjoner med DFØ-rad og API-ID/tabellrad |
| `chain_ledger.csv/json` | Før-/etter-kjede og eksplisitte kildekonflikter |
| `component_ledger.json` | Alle sju netto-/underpostpresentasjoner og komponentkontroller |
| `post_ledger.csv/json` | Alle 1 638 DFØ-poster, årsbevilgning og overføringer |
| `statsregnskap_ledger.csv/json` | Alle 1 668 nøkler i PDF/DFØ-unionen, kolonnevise differanser |
| `scope_residual_ledger.csv/json` | Alle 43 nøkkelforskjeller med bevis, status og PDF-side |
| `residual_ledger.csv/json` | Alle seks ikke-eksakte kilde/post-statuser, R1–R6 |
| `blaabok_posts.json`, `blaabok_lines.json` | Alle 1 574 Blå bok-poster med side og posisjon |
| `web_text_check.json` | Tre direkte vedtakssider og faktisk API-tekstsamsvar |
| `metrics.json` | Maskinlesbare antall, dekningsmål og summer |

Skriptene er lokale undersøkelsesverktøy. Hovedrekkefølge fra arbeidsområdets rot: `inventory.py`, `extract.py`, `reconcile.py`, `source_link.py`, `chains.py`, `components.py`, `metrics.py`, `audit_inventory.py`, `pdf_extract.py`, `finalize_control.py`, `statsregnskap_reconcile.py` og `scope.py`. Kjør med `C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`. `pdf_text.py` og `pdf_render.py` gir supplerende PDF-kontroll. `fetch_web.py` og `check_web.py` gjelder nettsideprøvene; nedlasting behøves ikke for å reprodusere beregningene fra bevarte filer. Manifester fornyes sist med `hash_manifest.py`.

Inngående statsregnskapsuttrekk er `work/issue2/fortsettelse/varig/statsrekneskap2024-posts.csv/json`, med rå PDF og detaljerte tabell-/kapittelkontroller i samme mappe. Fremtidige rådataendringer må være ny kildeversjon og ny kontroll, uten overskriving av dette kontrollgrunnlaget.

## SHA256 for sentrale inputfiler

| Input | SHA256 |
|---|---|
| `bevilgninger_full_historikk.zip` | `8ac148291d0215b0a3d053fc4ca9ac5dcc27e18cecb93927209b9cef015a8439` |
| `bevilgninger_full_historikk.csv` | `c69c59d9a94417f6f24a6e59f0defbe2549366d76a9cde06c41c3d80c1a713b1` |
| `blaabok_2024.pdf` | `7204477be2b1ed089ae2d2eca1307a96d5929d04ea5a0d874ca32eeae1a53bf8` |
| `vedtak-2023-2024.xml` | `554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf` |
| `vedtak-2024-2025.xml` | `9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680` |
| `statsrekneskapen2024.pdf` | `f46e7c3613176e064b2d87b07c66608f38c4bd88d980795e51ada42bb52ba9fb` |
| `statsrekneskap2024-posts.csv` | `2dbb699d7e17dd4d02c36f7abce94cbd90611148d4982a9d146bf21e958671c6` |
