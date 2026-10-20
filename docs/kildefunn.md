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

Begrensning: Den avgrensede undersøkelsen fant ingen sikker positiv prøve på en endelig kapittel-/postbevilgning der hele det relevante sakskomplekset var uten proposisjonsgrunnlag. Det er ikke dokumentasjon på at slike vedtak ikke finnes. En konstruert test med manglende Prop.-metadata skal merkes som robusthetstest, ikke historisk kildebevis.

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

## Vedlikehold

Oppdater eksisterende funn når nye prøver presiserer det. Bevar skillet mellom observert kildeinnhold, en designanbefaling og et åpent spørsmål. Vesentlige nye funn skal få en kort inngang fra AGENTS.md eller relevant fag-/arbeidsdokument, slik at neste økt finner dem uten chatloggen.
