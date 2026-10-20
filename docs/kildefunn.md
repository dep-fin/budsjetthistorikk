# Varige kildefunn for innlesningen

Dette er faglige og tekniske funn som skal brukes på tvers av agentøkter. Dokumentet ligger på main og gjelder også før hele forskningsarbeidet i #2 er ferdig. Funn, kildebevis og konsekvens holdes samlet.

## Bevilgningsendringer finnes også som ANNET

**Observert 20. oktober 2026:** Stortingets API klassifiserer konkrete bevilgningsendringer som `ANNET`. Et uttrekk av bare `stortingsvedtak_type.id = BUDSJETT` mister derfor relevante vedtak.

| Prøve | Sesjon | Vedtaksnummer | Vedtaks-ID | Sak-ID | API-type |
| --- | --- | --- | --- | --- | --- |
| RNB 2024 | 2023–2024 | 857 | 40033719 | 98919 | ANNET |
| Nysaldering 2024 | 2024–2025 | 428 | 40034287 | 100289 | ANNET |

### Kildebevis

- [RNB-vedtak 857](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033719&p=98919), med endringer blant annet på kapittel 21 post 1.
- [Nysalderingsvedtak 428](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034287&p=100289), med konkrete fra-/til-beløp og bevilgningsendringer.
- API-typen er kontrollert i [sesjonsresponsen 2023–2024](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2023-2024) og [sesjonsresponsen 2024–2025](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).
- [Versjonsfestet kontrollrapport med hentetider og SHA-256](https://github.com/depmartin/budsjetthistorikk/blob/5fdff33c73629c29215b4fc68a5bf8928639e7ed/docs/research/issue-2/kontrollkilder.md). Ved registreringen 20. oktober 2026 var den bredere undersøkelsen fortsatt under arbeid i [#2](https://github.com/depmartin/budsjetthistorikk/issues/2) og [utkast-PR #11](https://github.com/depmartin/budsjetthistorikk/pull/11).

### Konsekvens for innlesning og tester

1. Bevar vedtaksoversikten på tvers av API-typer. Bruk innhold og relevante saks-/dokumentkoblinger til å identifisere bevilgningskandidater.
2. Behandle ANNET-eksemplene som kildeprøver i dekningskontrollen. De skal kunne finnes selv om BUDSJETT-filteret ville utelatt dem.
3. API-type skal bevares som kildemetadata og skal ikke alene avgjøre om vedtaket er relevant.
4. At noen ANNET-vedtak inneholder bevilgninger betyr ikke at alle ANNET-vedtak gjør det. Ukjente eller tvetydige kandidater skal gi synlige kontrollavvik.
5. Fullstendighet krever mer enn kontroll av vedtakstype: kildeinventar og uavhengig avstemming skal brukes sammen.

Disse kontrollene er tatt inn i byggeticketene [#7](https://github.com/depmartin/budsjetthistorikk/issues/7) og [#9](https://github.com/depmartin/budsjetthistorikk/issues/9).

## Sakens dokumentgruppe er ikke et inngangskrav

**Kontrollert 20. oktober 2026:** Et initiativ fra Stortingets presidentskap om Akersgata-forprosjektet ble fulgt opp med en endelig økning på **9 700 000 kroner** på kapittel **41 post 45** for 2025, i vedtak **1149**, ID **40035422**, sak **103529**. Sakens direkte dokumentgruppe er melding, mens relevante fellesinnstillinger også viser proposisjoner.

Initiativvedtak **486**, ID **40034385**, ba om at bevilgning skulle fremmes senere. Det er ikke selv en kapittel-/postbevilgning. Endelig fullmaktsvedtak **1156**, ID **40035429**, har ramme **72 mill. kroner** for forpliktelser; dette er ikke en ekstra årsbevilgning.

Konsekvens: Finn kandidater fra alle vedtak og innholdet deres. Bevar sak, dokumentgruppe og initiativ som proveniens. Verken en direkte Prop.-lenke, dokumentgruppen proposisjon, et kronebeløp eller en tom relasjonsliste alene avgjør om en endelig bevilgning finnes. Skill anmodning, sats, fullmaktsramme og faktisk bevilgningslinje.

Kildebevis: [endelig bevilgning](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035422&p=103529), [initiativvedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034385&p=101938), [separat fullmakt](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40035429&p=103529) og [versjonsfestet rapport og saksgraph](https://github.com/depmartin/budsjetthistorikk/blob/53a44e819dcbf1d73df57969cb7cb8864a7310b3/docs/research/issue-2/stortingsinitiativ.md).

Den første avgrensede undersøkelsen av nyere sesjoner fant ikke en sikkert selvstendig bevilgning. Et senere målrettet søk fant en autentisk positiv prøve: **vedtak 249, ID 40005719, 6. februar 2003**, bevilger **7 000 000 kroner på kapittel 41 post 21** til Mehamn-kommisjonen. Fulltekstene til representantforslaget, komitéinnstillingen, presidentskapets bevilgningsinnstilling og den parallelle lovinnstillingen viser ingen proposisjon som grunnlag for bevilgningen. Dette er en kontrollert relevant kildekjede, ikke en påstand om hele ulykkens forhistorie. [Endelig vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40005719&p=26250) og [versjonsfestet rapport og fasit](https://github.com/depmartin/budsjetthistorikk/blob/50871d870d1e8d80aba03069bb30ee9d533db77f/docs/research/issue-2/selvstendig-bevilgning.md).

I de historiske saksmetadataene avviker dessuten eksport-ID fra dokumentets forsamling og kanoniske URL (for eksempel inno-200203-114 mot inns-200203-114). Bevar avviket og kontroller publikasjonen mot tittel, URL og innhold; ikke rett råverdien stilltiende. Oppnevning, taushetsplikt og innsynsregler i samme sak er negative bevilgningsprøver. Eldre HTML i denne prøven er et historisk kildebevis og utvider ikke første leveranses startdato.

## Bevilgninger kan vedtas direkte uten komitéinnstilling

**Kontrollert 20. oktober 2026 etter eksempel fra prosjekteieren:** [Vedtak 599 (2025–2026)](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40036289&p=107811), ID **40036289**, 26. mars 2026, er type **ANNET**. Det reduserer inntektsbevilgningene på **5538/70–72** med henholdsvis **1 154 167 000**, **2 175 000 000** og **1 250 000 kroner**. Saken ble etter dokumentert prosedyrevedtak behandlet direkte uten komitéinnstilling; grunnlaget er et representantforslag og et erstattende forslag i salen. Ingen proposisjon inngår i den undersøkte behandlingskjeden. Manglende Prop.- eller Innst.-kobling skal derfor ikke føre til eksklusjon.

Samme sak inneholder både satser, faktiske kapittel-/postendringer og anmodninger. Bevar elementene hver for seg. Vedtak 598 har en separat endring på 5543/70 og skal ha sin egen identitet. Vedtak 591–597 og 600 skal ikke gi ekstra bevilgningslinjer.

Kilden har et faktisk tallavvik: vedtakssiden, sesjons-API-et og forslags-API-et viser til-beløpet for 5538/70 som `I 615 833`. Voteringsreferatets HTML og publikasjons-XML viser **1 615 833 000**, i samsvar med før minus reduksjon. Bevar råavviket og referatet som avklaringskilde. Ingen generell regel skal bytte I med 1, legge til nuller eller stille overskrive tall med beregnet verdi. Dette er motstrid mellom representasjoner, ikke en observert rettelse over tid.

[Versjonsfestet rapport, kildefasit, rå API-objekter og kontrollresultater](https://github.com/depmartin/budsjetthistorikk/blob/131ad9d6bcf62c2e1e6156784fd02d21e0a5876d/docs/research/issue-2/vedtak599/README.md). Prøven er eldre enn produksjonsstarten 2026–2027 og endrer ikke startavgrensningen.

## Statsregnskapets bevilgningskolonne har et hentbart originalgrunnlag

**Kontrollert 20. oktober 2026:** Den offentlig tilbudte [PDF-en for Statsrekneskapen 2024](https://www.regjeringen.no/contentassets/1d45fede74ff4ef18ce06bbd6163c723/nn-no/pdfs/stm202420250003000dddpdfs.pdf) ga HTTP 200, selv om en tidligere direkte HTML-forespørsel ga 403. Bruk en uttrykkelig publisert alternativ representasjon når den er tilgjengelig; dette betyr ikke at alle adresser eller årganger er hentbare.

PDF-ens tabell 2.1 og 2.2 har enhet 1 000 kroner. Alle 1 655 uttrukne postrader har Løyving som stemmer eksakt mot 594 kapittelsummer og begge totalsummer. Løyving er årets bevilgning; Samla løyving inkluderer overføring, og Rekneskap er utfall. Sumkontroll mot PDF-en validerer uttrekket, ikke hele vedtakskjeden.

[Versjonsfestet rapport, kildehash og kontrollgrunnlag](https://github.com/depmartin/budsjetthistorikk/blob/100a591ea10209f8cc85b2e190cbb5e1af482bb2/docs/research/issue-2/varig-kildegrunnlag.md). Bevar kildepresisjonen og skill mellom manglende kolonne og nullbeløp.

## Sesjon og kilderettelser krever full sammenligning

**Kontrollert 20. oktober 2026:** Virkelige vedtak om budsjettåret 2024 ligger i to sesjoner. Sakens opprinnelige sesjon kan dessuten være forskjellig fra vedtakets sesjon. En datomarkør alene er ikke tilstrekkelig for å oppdage etterslep eller rettelser.

Kilden viser siste versjon og dokumenterer ikke en rettelseslogg eller en bindende tidsgrense for gamle rettelser. Bevar gode råversjoner og sammenlign vedtaksobjekter per ID. Endret responstid alene er transportmetadata. Endret innhold med samme ID krever ny kildeversjon og ny vurdering av berørte kjeder; en manglende ID i ett svar er et avvik, ikke automatisk sletting.

To faktiske sesjonshentinger viste bare ulike responstidspunkter. Beløpsrettelse, sen innkomst og midlertidig fravær ble prøvd som tydelig merkede syntetiske kontrolltilfeller. De er ikke observasjoner av en reell historisk rettelse. [Versjonsfestede prøver og begrensninger](https://github.com/depmartin/budsjetthistorikk/blob/100a591ea10209f8cc85b2e190cbb5e1af482bb2/docs/research/issue-2/varig-kildegrunnlag.md).

## En katalog er ikke en uttømmende liste over senere poster

**Kontrollert 20. oktober 2026:** Vedtak 526, ID 40034443, 25. mars 2025, bevilger 454 000 000 kroner på ny post 32 under eksisterende kapittel 900. Kombinasjonen 0900/32 finnes ikke i den undersøkte opprinnelige kapittel 900-tabellen for 2025.

Bevar derfor beløpslinje og kilde selv om katalogoppslaget feiler. Opprett synlig kontrollbehov og et sporbarhetsgrunnlag for katalogutvidelse. Manglende førbeløp er ikke i seg selv bevis på nullstart. [Endelig vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034443&p=102001) og [versjonsfestet kildeprøve](https://github.com/depmartin/budsjetthistorikk/blob/100a591ea10209f8cc85b2e190cbb5e1af482bb2/docs/research/issue-2/ny-katalogpost.json).

## Sluttsaldo og hele hendelseskjeden krever ulike kontroller

**Kontrollert 20. oktober 2026:** Hele 2024-materialet er avstemt. Alle 1 625 felles DFØ-/statsregnskapsposter stemmer eksakt for årets bevilgning. Alle 43 nøkkelforskjeller er forklart: 30 regnskapsrader med null bevilgning og 13 bevilgninger som er reversert til null. Alle 1 574 Blå bok-poster stemmer mot de opprinnelige vedtakene.

Dette gjør ikke hele hendelseskjeden automatisk korrekt. To publiserte vedtak gjentar samme endring for 1860/01 og 4860/01, og 5999/90 har motstrid mellom forrige saldo og senere førbeløp. Sluttsaldo er kontrollert, men hendelsesrollene undersøkes fortsatt. Bevar kildenes observasjoner og synlige konflikter; ikke fjern like beløp eller opprett en endring bare for å få summen til å stemme. [Versjonsfestet årsavstemming med inventar og avviksledgere](https://github.com/depmartin/budsjetthistorikk/blob/a3a9b90e50e170855b51d87d86fd1d4fe89a02ab/docs/research/issue-2/aar/README.md).

Årsprøven viser dessuten to bevilgningstabeller uten standardinnledning om statsbudsjettet. Kun søk på denne innledningen ville mistet 76 posthendelser. Kandidatinnlesning må bevare alle vedtak og kombinere innhold, tabellstruktur og saksreferanser.

DFØs rå inntektsfortegn er motsatt vedtakets fortegn i hele den kontrollerte 2024-årgangen. Dette er en kildeavhengig normalisering, ikke en endring av regelen om inntekt/utgift etter kapittel. Overføring mellom år er egne felt og holdes utenfor årets bevilgningsendringer.

## Vedlikehold

Oppdater eksisterende funn når nye prøver presiserer det. Bevar skillet mellom observert kildeinnhold, en designanbefaling og et åpent spørsmål. Vesentlige nye funn skal få en kort inngang fra AGENTS.md eller relevant fag-/arbeidsdokument, slik at neste økt finner dem uten chatloggen.
