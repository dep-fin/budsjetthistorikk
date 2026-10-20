# Issue 2 – kontrollkilder for endelige bevilgningsvedtak

Undersøkt 20. oktober 2026. Rapporten gjelder kildeundersøkelse. Utforskeren endret ikke produksjonskode eller GitHub-innhold; rapporten publiseres av orkestratoren som dokumentasjon til #2. «Dokumentert» viser til kildens egen beskrivelse. «Observert» viser til innhold som faktisk ble hentet eller lest. Anbefalingene er faglige vurderinger på dette grunnlaget.

## Hovedfunn

**Et uttrekk av bare `stortingsvedtak_type.id = BUDSJETT` er dokumentert utilstrekkelig for å følge alle bevilgningsendringer gjennom året.** I de lagrede API-svarene er både RNB-vedtak 857 av 21. juni 2024 og nysalderingsvedtak 428 av 19. desember 2024 klassifisert `ANNET`. Begge inneholder konkrete bevilgningsendringer, jf. [RNB-vedtaket, ID 40033719](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033719&p=98919), [nysalderingsvedtaket, ID 40034287](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034287&p=100289) og [API-svar 2023–2024](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2023-2024)/[2024–2025](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).

**En anvendelig uavhengig kontrollkilde finnes hos DFØ.** Den offisielle ZIP-filen «Full historikk over bevilgninger» kunne hentes og analyseres. Den har beløp og kildebeskrivelser på kapittel/post. Fire små avstemminger for 2024 stemmer mellom DFØ, Blå bok, endringsvedtak og bevilgningskolonnen i statsregnskapet. Dette underbygger metoden, men dokumenterer ikke fullstendig dekning av alle poster eller alle år. [DFØs nedlastingsside](https://statsregnskapet.dfo.no/last-ned), [prøvd ZIP-fil](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_full_historikk.zip).

## Kontrollkildene og kandidatgrunnlaget

### 1. Saldert budsjett: Blå bok

**Dokumentert:** Blå bok 2024 oppsummerer vedtatte inntekter og utgifter etter Stortingets behandling av innstillingene 2–17 høsten 2023. Den avgrenser dermed kontrollen til det opprinnelige, salderte budsjettet for 2024. Innledningen viser til Lovdata for skatte-, avgifts- og tollvedtak. Kilden dekker også andre vedtak og svalbardbudsjettet. [Blå bok 2024, innledning s. 5](https://www.stortinget.no/globalassets/pdf/budsjettsiden/blaabok_2024.pdf).

**Observert:** PDF-filen ble hentet med HTTP 200, 124 PDF-sider. Trykt side 9 er PDF-side 11. Den siden er både tekstuttrukket og visuelt kontrollert i `blaabok-side9.png`. Tabellene på denne siden har beløp i **kroner**. Samleoversikten på trykt side 6 bruker derimot **1 000 kroner**. Enheten må derfor registreres per tabell. Det er ikke funnet et tilknyttet strukturert saldert-CSV/XLSX på den prøvde Stortinget-siden. [Blå bok](https://www.stortinget.no/globalassets/pdf/budsjettsiden/blaabok_2024.pdf), [budsjettoversikt 2024](https://www.stortinget.no/no/Saker-og-publikasjoner/Statsbudsjettet/statsbudsjettet-2024).

**Historikk:** Stortingets oversikt har lenker til Blå bok for 1993–2026. Dette er observert lenkedekning; innholdet i samtlige årganger er ikke hentet eller kontrollert. [Vedtatt statsbudsjett](https://stortinget.no/no/Saker-og-publikasjoner/Statsbudsjettet/Vedtatt-budsjett/).

### 2. DFØ: bevilgninger – all historikk

**Dokumentert:** DFØ beskriver dette som månedlig oppdatert bevilgningshistorikk med stortingsvedtakene bak bevilgningene på kapittel/post. Kolonnebeskrivelsen skiller bevilget beløp, overført beløp fra foregående år og beløp som kan overføres. `Tildelings_periode` beskrives som året og måneden proposisjonen ble fremmet. Det er dermed ikke en dokumentert vedtaksdato. [Nedlastingsside og kolonnebeskrivelse](https://statsregnskapet.dfo.no/last-ned), [kolonnebeskrivelse som CSV](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_beskrivelse_av_kolonner.csv).

**Observert i råfilen:** ZIP-filen er 1 238 069 byte og inneholder én CSV på 16 022 138 byte. CSV-en har 55 452 datarader, 18 kolonner og år 2014–2026. Det er 4 268 rader for 2024. Semikolonseparasjon, siterte felt, desimalkomma og Windows-1252 ble brukt ved vellykket innlesing. `Post_id` inneholder kapittel og post samlet, eksempelvis `002001`. Ledende nuller må bevares. Beløpsstørrelsene i de fire kontrollene er kroner; dette er kontrollert mot Blå bok og vedtakene, mens kolonnebeskrivelsen bare sier «Bevilget beløp». [Rå ZIP-fil](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_full_historikk.zip).

**Databehandling som krever oppmerksomhet:** Alle prøvde 2024-rader har `Periode=202401`, også endringer knyttet til proposisjoner i mai og november. `Tildelings_periode` varierer. Saldert 0020/01 er splittet på 80 255 000 og 27 416 000 kroner med samme tekstbeskrivelse. Disse må summeres. De er ikke to forskjellige stortingsvedtak. Tilsvarende er økningen på 0021/01 i RNB delt i 9 000 000 og 3 000 000 kroner. Ingen av disse radene gir stortingsvedtakets ID direkte. [Rå ZIP-fil](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_full_historikk.zip); utvalget er bevart i [avstemmingsdata](kontroll-avstemming.json); det lokale CSV-uttrekket følger ikke med i repoet.

Overførte bevilgninger inngår i `Bevilgning_beløp` i de prøvde radene. En ukritisk sum ville derfor gi samlet disponibel bevilgning. Ved kontroll av årets vedtatte bevilgning ble overført beløp holdt utenfor. Dette er en verifisert regel for utvalget; en generell produksjonsregel bør først prøves mot flere radtyper og år. [Rå ZIP-fil](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_full_historikk.zip).

### 3. Statsrekneskapen 2024: bevilgningskolonnen

**Dokumentert og lest gjennom nettverktøyet:** Meld. St. 3 (2024–2025), dokument-ID **3097946**, vedlegg 2, tabell 2.1, oppgir utgifter i **1 000 kroner**. Kolonnene er blant annet `Overført frå 2023`, `Løyving`, `Samla løyving` og `Rekneskap`. De fire kontrollene nedenfor bruker **Løyving**, mens `Samla løyving` også kontrolleres separat. [Vedlegg 2, tabell 2.1](https://www.regjeringen.no/no/dokumenter/meld.-st.-3-20242025/id3097946/?ch=7).

Vedlegget er tilgjengelig som HTML-tabeller gjennom nettverktøyet. Siden tilbyr også PDF, EPUB og Word. Disse formatene ble observert som lenker; råfilene ble ikke hentet. Direkte Python-henting av HTML-en ga **HTTP 403**. Det er derfor ikke lagret eller SHA256-kontrollert noe originalt regjeringsråsvar. Ingen alternative regjeringsendepunkter ble prøvd for å omgå dette. Det er et svakere revisjonsspor for denne kontrollkilden enn for de lagrede Stortinget- og DFØ-filene. [Samme vedlegg](https://www.regjeringen.no/no/dokumenter/meld.-st.-3-20242025/id3097946/?ch=7).

### 4. RNB, nysaldering og øvrige endringer

For 2024 gir [RNB-saken, sak-ID 98919](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=98919) forbindelsen mellom Meld. St. 2, Innst. 447 S og vedtakene 21. juni. DFØ peker i prøvepostene på **Prop. 104 S (2023–2024), Innst. 447 S**. Det konkrete beløpsvedtaket er **857**, API-ID **40033719**. Det endrer blant annet 0021/01 fra 180 299 000 til 192 299 000 kroner. [Vedtak 857](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033719&p=98919).

Nysalderingsgrunnlaget er **Prop. 36 S (2024–2025)**, regjeringsdokument-ID **3076783**, med **Innst. 90 S** og Stortingets **vedtak 428**, API-ID **40034287**, sak-ID **100289**, 19. desember 2024. Proposisjonen ble fremmet 29. november. Det er Stortingets vedtak som er prøvd som endelig endringskilde. [Proposisjonen](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/), [vedtak 428](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034287&p=100289).

## Gjennomførte avstemminger

Alle beløp nedenfor er **kroner**, etter at statsregnskapets tall er multiplisert med 1 000.

| Kapittel/post | Saldert, Blå bok | RNB-endring | Nysalderingsendring | Sum årets bevilgning | Statsregnskapets Løyving | Overført fra 2023 | Samla løyving |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0020/01 | 107 671 000 | 0 i prøvd kjede | 2 006 000 | 109 677 000 | 109 677 000 | 3 406 000 | 113 083 000 |
| 0021/01 | 180 299 000 | 12 000 000 | 9 100 000 | 201 399 000 | 201 399 000 | 6 980 000 | 208 379 000 |
| 0024/01 | 119 438 000 | 3 800 000 | 2 427 000 | 125 665 000 | 125 665 000 | 3 693 000 | 129 358 000 |
| 0041/21 | 800 000 | 613 000 | 0 i prøvd kjede | 1 413 000 | 1 413 000 | 619 000 | 2 032 000 |

Kilder til tabellen: [Blå bok, trykt side 9](https://www.stortinget.no/globalassets/pdf/budsjettsiden/blaabok_2024.pdf), [RNB-vedtak 857](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033719&p=98919), [nysalderingsvedtak 428](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034287&p=100289), [DFØs rådata](https://statsregnskapet.dfo.no/nedlasting/bevilgninger_full_historikk.zip), [statsregnskapets tabell 2.1](https://www.regjeringen.no/no/dokumenter/meld.-st.-3-20242025/id3097946/?ch=7). Nullene er manglende endringer i den undersøkte kjeden, ikke en påstand basert på fullstendig gjennomgang av alle årets vedtak.

**Kontroll av et opprinnelig vedtak:** Vedtak **193**, 15. desember 2023, API-ID **40032763**, sak-ID **95780**, `BUDSJETT`, inneholder blant annet 0020/01 = 107 671 000, 0021/01 = 180 299 000 og 0024/01 = 119 438 000 kroner. Alle tre stemmer med Blå bok, trykt side 9, og summert saldertbeløp hos DFØ. [Vedtak 193](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40032763&p=95780), [Blå bok](https://www.stortinget.no/globalassets/pdf/budsjettsiden/blaabok_2024.pdf).

**Kontroll mot feil begrep:** På 0020/01 er statsregnskapets regnskapsutfall 108 793 000 kroner. Dette avviker både fra `Løyving` 109 677 000 og `Samla løyving` 113 083 000. Valg av feil kolonne gir derfor en påviselig feil også i et lite eksempel. [Tabell 2.1](https://www.regjeringen.no/no/dokumenter/meld.-st.-3-20242025/id3097946/?ch=7).

## APIets dekning og tidsavgrensning

**Dokumentert:** Endepunktet er sesjonsbasert og leverer vedtakstekst, vanligvis HTML i XML, samt vedtaks-ID, saks-ID, dato og type. Dokumentasjonen beskriver en liste over alle vedtak knyttet til angitt sesjon. Den garanterer ikke at bevilgningsendringer er ensbetydende med typen `BUDSJETT`. [API-dokumentasjon for vedtak](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/).

Datasettet ble introdusert 16. oktober 2019. Dette er lanseringsdato, og etablerer ikke i seg selv historisk startår eller fullstendighet bakover. Det ble ikke funnet en uttrykkelig historisk dekningsgaranti i de undersøkte sidene. Denne delundersøkelsen har hentet og kontrollert API-svar for **2023–2024** og **2024–2025**; eldre sesjoner er ikke prøvd her. [Lanseringsmeldingen](https://data.stortinget.no/nyhetsoversikt/vedtak-presidentskapet-og-horinger/), [API-dokumentasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/).

For budsjettåret 2024 ligger det opprinnelige vedtaket i desember 2023 og endringene i juni og desember 2024. De observerte vedtakene fordeler seg derfor på to sesjoner. Å filtrere bare etter kalenderåret i vedtaksdato ville miste den opprinnelige bevilgningen. Å hente bare sesjon 2023–2024 ville miste desemberendringene. [Vedtak 193](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40032763&p=95780), [vedtak 428](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034287&p=100289).

Stortinget opplyser dessuten at datagrunnlaget oppdateres, at bare siste versjon vises, og at APIet har grense på 100 kall per minutt. Råsvar og hentetid bør derfor bevares ved undersøkelser som skal kunne etterprøves. [Om tjenesten](https://data.stortinget.no/om-datatjenesten/).

## Anbefalt videre kontroll og gjenstående begrensninger

1. Bruk Blå bok som startkontroll for hvert budsjettår. Prøv hele posttabellen mot de opprinnelige stortingsvedtakene før en årgang merkes som komplett.
2. Hent alle vedtakstyper i relevante sesjoner. Finn bevilgningskandidater ut fra selve vedtaksteksten og saks-/publikasjonsreferanser. De observerte `ANNET`-vedtakene må inngå.
3. Rekonstruer endringskjeden per budsjettår, kapittel og post. Bevar både økning/reduksjon og eksplisitt før-/etterbeløp. Etterbeløpet i ett vedtak bør stemme med førbeløpet i neste. Prøv også nye og avsluttede poster, negative inntektsbeløp og rettelser.
4. Bruk DFØs bevilgningshistorikk som et uavhengig register over kandidatendringer og sluttsummer. Kartlegg alle kildebeskrivelser og radtyper før summeringsreglene fastsettes. Dato i DFØ-feltet skal ikke uten videre brukes som stortingsvedtaksdato.
5. Avstem årets bevilgning mot `Løyving` i statsregnskapet, og kontroller overføringer separat mot `Samla løyving`. Avvik må få konkret forklaring, eksempelvis fullmaktsfordeling eller manglende vedtak. Sluttbeløp alene beviser ikke at alle mellomliggende endringer er funnet; utlignende mangler kan gi samme sluttbeløp.

Disse punktene er anbefalinger på grunnlag av de konkrete kildeprøvene over. **Det er ikke gjennomført en fullstendig avstemming av alle 2024-poster eller av alle årets endringer.** Det neste verifiserbare steget er å avstemme alle 2024-rader i DFØ-filen mot alle vedtakstekster i de to lagrede sesjonene, og deretter mot hele tabell 2.1/2.2 i statsregnskapet. Den siste kontrollen krever et varig, autorisert råeksemplar av statsregnskapet. Denne undersøkelsen beviser at kilder og metode finnes, og viser konkret hvorfor `BUDSJETT` alene svikter.

## Henting og revisjonsspor

Direkte henting i sandkassen ga først DNS-feil. Deretter ble offentlig nettverkstilgang brukt til ordinære forespørsler. Stortinget og DFØ svarte HTTP 200. Regjeringen svarte HTTP 403 på den ene direkte forespørselen. Nettverktøyet kunne lese en indeksert/ekstrahert versjon av regjeringssiden, men dette er ikke et lagret originalt HTTP-svar. Ingen blokkering er omgått.

Råfilene ble bevart som lokale mellomfiler under undersøkelsen. Originale PDF-, XML- og ZIP-filer er ikke versjonert i denne dokumentasjons-PR-en. Tidspunktene er UTC; lokal Oslo-tid var UTC+2. Fullstendige URL-er, status, innholdstype og byteantall finnes i undersøkelsens lokale hentemanifester. Tabellen nedenfor bevarer kildehashene i repoet. Avledede kontrolluttrekk er ikke fremstilt som originale kilder.

| Råfil | Hentet UTC 20.10.2026 | Status | SHA256 |
|---|---|---|---|
| blaabok_2024.pdf | 11:35:12 | 200 | 7204477be2b1ed089ae2d2eca1307a96d5929d04ea5a0d874ca32eeae1a53bf8 |
| vedtak-dokumentasjon.html | 11:35:14 | 200 | d3aef50795614777c939fd7b71197aebb856927a625e851de20ddd013d5f831d |
| om-datatjenesten.html | 11:35:14 | 200 | a93d5f7da2dbb0b112027fdb793301eb79e685726078d0ee785dfe89880b38e4 |
| dfo-last-ned.html | 11:35:51 | 200 | f7178906ac2ab75bee9467ad273d43a857b0856d3e09e0e0a7069b2584033902 |
| nyhetsoversikt.html | 11:35:51 | 200 | 3af33c6e06e37d7a0374be57ef2cb071a66d715fc355cbe61f2d812de35a03c6 |
| stortinget-2024.html | 11:35:51 | 200 | 05ac0560e3d0bef9a7fa71a26dd7e33ecc418a0739eb7fd000da1684f10e85f6 |
| vedtak-2023-2024.xml | 11:35:51 | 200 | 554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf |
| bevilgninger_full_historikk.zip | 11:36:08 | 200 | 8ac148291d0215b0a3d053fc4ca9ac5dcc27e18cecb93927209b9cef015a8439 |
| bevilgninger_kolonner.csv | 11:36:10 | 200 | d335692dd8a1aa703538d2ca2f23f250195d57a6e4e3ae0eaf963c3923ef03cf |
| vedtak-2024-2025.xml | 11:36:10 | 200 | 9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680 |
| vedtak193.html | 11:37:33 | 200 | da756181419ac6a3187febbd042389e215b45de9f981bb1f8f80010f3cda2435 |
| vedtak857.html | 11:37:33 | 200 | 2d93e5ca2d7e729095b4a0c176c4c881c90da5aac45926d210e77d49920d416f |
| vedtak428.html | 11:37:34 | 200 | 4fc843dc0a6da1baec69e1decc4d060644927509ce19052c33b43bca69d32115 |

For den utpakkede CSV-en og øvrige lokale mellomfiler er hasher bevart i [filhashlisten](kontroll-filhashes.json). Listen beskriver lokale mellomfiler, ikke filer som alle følger med i repoet. De eksterne kildefilenes nedlastingstid og URL skal leses fra manifestene, også når en lokalt utpakket fil er opprettet senere.
