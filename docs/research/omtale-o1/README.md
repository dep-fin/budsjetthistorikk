# O1: kildeundersøkelse for vedtak 210, kapittel 1429 post 1 og 22

Kontrollert 22. oktober 2026. Del av [#32](https://github.com/depmartin/budsjetthistorikk/issues/32). **O1 er utført og godkjent som kildegrunnlag. O2-oppdelingen er godkjent; #34/O2a er autorisert, #35/O2b er publisert uten byggemandat.** Undersøkelsen alene implementerte ingen produktfunksjon. O2a-kandidaten og dens konkrete kontrakt dokumenteres i [pilotveiledningen](../../omtale-pilot.md). #10 står åpen.

## Resultat

210 er egnet som første komplette omtaleprøve. Proposisjonen forklarer uttrykkelig omdisponeringen mellom postene og lønnsøkningen på post 1. Innstillingen gjengir forklaringen, har uttrykkelig støtte fra samlet komité og tilrår de samme eksakte beløpene som regjeringen. Plenumsreferatet dokumenterer at denne innstillingen ble enstemmig vedtatt. Den eksisterende vedtaksprøven identifiserer beløpsvedtaket som 210/40034048, sak 100927, 16. desember 2024. Dette er en dokumentert kjede gjennom behandlingsleddene, utover B8s saksrelasjon.

Prøven dokumenterer **ingen komitéendring eller mindretallsbegrunnelse**. En slik prøve må velges særskilt for O3. Regjeringens begrunnelse for forslaget kan kobles til den vedtatte endringen, men blir ikke dermed Stortingets egen begrunnelsesordlyd eller et bevis for tiltakets faktiske virkning.

## Lest grunnlag og avgrensning

AGENTS.md, arbeidsflyt, issue tracker, begrepsregler, GLOSSARY.md, kravgrunnlag, leveranseplan, omtaleplan, ansvarsdeling og observasjonsformat er lest. B8/B9-veiledningene, kildeprøvene og ADR 0010 er kontrollert. Gjeldende #32 er hentet i sin helhet; kommentarkoblingen returnerte **ingen kommentarer**. [Snapshotet](issue32-snapshot.json) bevarer det hentede grunnlaget. Startpunkt i repoet var `d74d2cb` (PR #33). Vedtaks- og saksprøvene nedenfor gjenbrukes uendret, uten ny faglig godkjenning.

Undersøkelsen gjelder nysalderingsforslag for **budsjettåret 2024**, dokumenter i **sesjonen 2024–2025**. Den dekker ikke årets samlede endringer, kontokontinuitet over år eller lønnsoppgjørets detaljberegning. Henvisningen til Finansdepartementets nysalderingsproposisjon er bevart, men den kilden er ikke undersøkt her.

## Originaler, representasjoner og versjoner

Alle seks vellykkede HTTP-responskropper er bevart byteidentisk i [originals](originals). [Manifestet](source-manifest.json) har forespurt og endelig URL, faktiske byteantall/SHA-256, start-/sluttid i UTC, status og relevante responsheadere. `Set-Cookie` er utelatt fra transportmetadata; originalkroppene er uendret. Hentetid er ikke publiseringsdato. Hashen identifiserer den observerte representasjonen, ikke en konstruert felles HTML/PDF-revisjon.

| Representasjon | Byte | SHA-256 |
| --- | ---: | --- |
| Prop. 16 S, full PDF | 733 075 | `677716056269c07b8ec81bcae91d814b975123791635548281038d9beb3aa5db` |
| Prop. 16 S, HTML kapittel 2 | 100 808 | `258d26e6d324bde709bf3d1cb660d7eb6f4248f537d4b0c77e095f17697cf8df` |
| Prop. 16 S, HTML forslag | 118 163 | `ff1c53688a155c2cb9d8d37a8d40550e56b5c5c1d2d171c30519ef49227eca5e` |
| Innst. 81 S, full PDF | 331 688 | `5a29d0553991759d8ddc234899647e9e6b5e1f2885bf13edccfb26105a6be496` |
| Innst. 81 S, full HTML | 107 925 | `e7069d74e911fb868812bb34f68b41d210b4e33035c1317cbedd296ac1101e95` |
| Plenumsreferat, voterings-HTML | 2 094 710 | `22170a60f769e89642b2e52525899903020de25938aa2b566ea28d11f85fb2e5` |

[Regjeringens dokumentinngang](https://www.regjeringen.no/no/dokumenter/prop.-16-s-20242025/id3075774/) identifiserer Prop. 16 S og tilrådingen 22. november 2024. Den fullstendige [PDF-en](https://www.regjeringen.no/contentassets/65a4e1b12ca242b6b7c5958edd9dc5c1/no/pdfs/prp202420250016000dddpdfs.pdf) bevarer også kapitler som ikke er hentet som HTML. De to HTML-filene er **delrepresentasjoner**, ikke komplett proposisjons-HTML. [Innstillingens HTML](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-081s/?all=true) og [PDF](https://www.stortinget.no/globalassets/pdf/innstillinger/stortinget/2024-2025/inns-202425-081s.pdf) identifiserer familie- og kulturkomiteen, Prop. 16 S kap. 1429 og dato 9. desember 2024. Dokumentidentitet og kontrollert samsvar for de aktuelle passasjene knytter formatene sammen; det er ingen påstand om identisk tekst eller byte i hele dokumentene.

Første shellforsøk ga DNS-feil og ingen responsbyte. Første Python-henting fra regjeringen.no ga 403; forespørsel med `User-Agent: Mozilla/5.0` ga deretter 200. De tre feilforsøkene er bevart i manifestet uten dokumenthash, fordi responskropp ikke ble bevart i disse forsøkene. Et prøvd `eksport/vedtak?vedtakid=40034048` ga 404 og er ikke et dokumentert API-endepunkt. Det brukes ikke videre. Vedtaksbeviset er i stedet repoets allerede bevarte B6-prøve. Ingen av disse feilene betyr manglende faglig omtale.

## Presise tekststeder og nødvendig kontekst

[passages.json](passages.json) inneholder 18 kildebundne HTML-blokker med full blokk-HTML, full tekst, kildehash, HTML-ID og absolutt XPath. Dette er **avledet undersøkelsesmateriale**, ikke en implementert omtaleeksport eller besluttet datakontrakt. UTF-8 er eksplisitt; mellomrom og opprinnelig markup står i originalen. [PDF-tekstene](prop16s.txt) og [innstillingsteksten](inns81s.txt) er avledet med versjonsregistrert pypdf. De erstatter ikke originalene eller deres leserekkefølge.

| Belegg | Nøyaktig lokator i bevart representasjon | Hierarki og kontekst |
| --- | --- | --- |
| P1: regjeringens post 1-omtale | `prop16s-ch2.html`: `#kap2-p24`, i `#kap2_ch7_ch1`; PDF trykt side 3, høyre spalte nederst | 2 Endringsforslag → Kap. 1429 Riksantikvaren → Post 01 Driftsutgifter. Hele avsnittet bevares, med både omdisponering og lønn. Kapitteloverskrift står i søskenblokk `#kap2_ch7`, ikke som DOM-forfader. |
| P22: regjeringens post 22-omtale | Samme HTML: `#kap2-p25`, i `#kap2_ch7_ch2`; PDF side 4, venstre spalte øverst | Samme kapittel → Post 22 Flerårige prosjekter kulturmiljøforvaltning, kan overføres. Kapitteloverskriften og post 1 står på foregående PDF-side. |
| PN: nabokontekst uten 210-beløpskobling | `#kap2_ch7_ch3`, `#kap2-p26`; PDF side 4 | Post 60, Vega og stikkordsfullmakt. Bevares som kontekst, uten kobling til 210s post 1-/22-endringer. |
| PT: regjeringens eksakte forslag | `prop16s-ch4.html`: første tabells `tbody/tr[43]` gir kapittel, `[44–45]` post 01 og `[46–47]` post 22; PDF side 8 | Forslag til vedtak → I → Utgifter → kap. 1429. Tabellens overskrifter finnes på PDF-side 7. Eksakte absolutte XPaths står i passages.json. |
| K1/K22: innstillingens sammendrag | `inns81s.html`: `#m1_1_1 > div.krnl_chapter > p`, `#m1_1_2 > div.krnl_chapter > p`; PDF side 1, venstre spalte | Sammendrag `#m1` → Kap. 1429 `#m1_1` → Post 1/22. Dette gjengir regjeringens forslag. Post 60 `#m1_1_3` er nabokontekst. |
| KS: komiteens støtte | `#m2 > div > p`; PDF side 1, høyre spalte nederst | Komiteens merknader, navngitte medlemmer fra Ap, H, Sp, FrP, SV og V. Hele støtteavsnittet bevares. |
| KT: komiteens tilråding | `#m3`; PDF side 2 | Innledende tekst sier samlet komité; `div[data-strtngt-romertallseksjon-romertall='i'] table tbody`: rad 1 kapittel, rad 2–3 post 1, rad 4–5 post 22. II gjelder post 60. |
| V: vedtakelse av tilrådingen | `votering-161224.html`: `#2024-12-16-25` | Votering i sak nr. 25 → innledende dokumenthenvisning til Innst. 81 S/Prop. 16 S kap. 1429 → gjengitt I og II → voteringsresultat. Hele blokken er bevart. |

Radnumre er 1-baserte innen den oppgitte `tbody`, og PDF-sidene er trykte sidetall som her samsvarer med 1-baserte PDF-sider. De fem relevante PDF-sidene (Prop. 3, 4, 8 og Innst. 1, 2) er rendret fra lokale originaler med pypdfium2 og visuelt kontrollert. Side-/spalteplassering og tabellens leserekkefølge er dermed kontrollert utover maskinelt tekstuttrekk.

## Bevis for konto og behandlingsledd

Regjeringens [postomtale](https://www.regjeringen.no/no/dokumenter/prop.-16-s-20242025/id3075774/?ch=2#kap2_ch7_ch1) knytter 3 mill. kroner på post 1 uttrykkelig til egne stillinger som skal erstatte konsulenter innen digital systemutvikling. Den navngir post 22 som finansiering. [Post 22-avsnittet](https://www.regjeringen.no/no/dokumenter/prop.-16-s-20242025/id3075774/?ch=2#kap2_ch7_ch2) peker uttrykkelig tilbake til post 01. Dette gir postbevis og bevis for omdisponeringsforslaget, med en felles forklaring for to poster. Lønnsforklaringen i P1 gjelder bare post 1.

| Konto, budsjettår 2024 | Før | Endring | Etter | Beviskjede og grense |
| --- | ---: | ---: | ---: | --- |
| 1429/1 | 160 243 000 | +5 796 000 | 166 039 000 | P1 → PT → K1 + KS + KT → V → 210. Forklaring: 3 mill. omdisponering og avrundet lønnsanslag. Hele økningen kan ikke tilskrives konsulenttiltaket. |
| 1429/22 | 32 185 000 | −3 000 000 | 29 185 000 | P22 og omdisponeringsdelen av P1 → PT → K22 + KS + KT → V → 210. Reduksjonen og mottakerposten er uttrykkelig angitt. |

Beløpene i tabellen er kontrollert i regjeringens forslag, komiteens tilråding, gjengivelsen ved voteringen og B6-vedtaksprøven. Forslag, tilråding og endelig vedtak er fortsatt separate talltyper. O1 registrerer ingen nye beløpsobservasjoner.

Den uendrede [B6-prøven](../../../tests/fixtures/b6/40034048.xml) har SHA-256 `2a540261f110b761a0213516c8ad72844d0285744ca0f1cdd4cb1afce06f0850`. XML-lokator med navnerom `http://data.stortinget.no`: `/stortingsvedtak_oversikt/stortingsvedtak_liste/stortingsvedtak[1]`; feltene `id`, `sak_id`, `stortingsvedtak_nummer`, `stortingsvedtak_dato_tid` og `stortingsvedtak_tekst` binder identitet, sak og ordlyd. Innen det dekodede HTML-feltets romertall I har tabellens tbody rad 1 kapittel, rad 2–3 post 1 og rad 4–5 post 22. Dette er et **avledet bytebevarende utdrag**, ikke en ny full API-respons: [sidevognen](../../../tests/fixtures/b6/40034048.json) dokumenterer fullresponsens hash, objektets byteposisjon og uttrekksmetoden.

[B8s komplette saksrespons](../../../tests/fixtures/b8/sak-100927.xml), SHA-256 `2ee25b327b78772523d56317c752e35f5134eef60db9536f6dea3c94ad8fed27`, binder sak 100927 til proposisjonen, Innst. 81 S og referatet. Lokator `/detaljert_sak/publikasjon_referanse_liste`: referanse 1 proposisjon, 3 innstilling, 5 votering. Denne saksrelasjonen er støttebevis, ikke alene postbevis. Den andre saken 100889/Innst. 95 S skal ikke arve 1429-koblingene. [Støttemanifestet](supporting-manifest.json) hashfester de fire eksisterende filene som er gjenbrukt.

Det separate [plenumsbeviset](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-16/voteringer#2024-12-16-25) identifiserer både dokumentene og kapittelavgrensningen, gjengir de to postforslagene og fastslår enstemmig vedtakelse. Sammen med 210-originalen dokumenterer det vedtakelse av den konkrete tilrådingen. Det er ikke utledet fra lik konto/beløp eller dokumentmetadata alene.

## Roller, tolkninger og uavklarte forhold

- **Regjeringen:** P1/P22 er forklaring på regjeringsforslaget. K1/K22 er komiteens sammendrag av dette, ikke en ny uavhengig begrunnelse.
- **Samlet komité:** KS støtter regjeringens forslag; KT fremmes av samlet komité. Ingen særskilt flertallsgruppe eller mindretallsmerknad er funnet ved kontroll av hele den tosidige innstillingen. Dette er kontrollert fravær i denne innstillingen, ikke en generell status for hele plenumsdebatten.
- **Stortinget:** V dokumenterer enstemmig vedtakelse. Vedtaksordlyden gir eksakte postendringer, men gjentar ikke forklaringene. Støtte og vedtakelse er separate relasjoner til omtalen.
- **Beregning/tolkning:** 5 796 000 − 3 000 000 = 2 796 000. Dette er en beregnet rest, ikke et kildeobservert eksakt lønnsbeløp. P1/K1 bruker anslått 2,8 mill. og samlet 5,8 mill. Bevar de avrundede utsagnene uten å overskrive tabellbeløpet eller opprette ekstra vedtatte komponenter.
- **Uavklart detaljgrunnlag:** Finansdepartementets videre lønnsomtale og beregning er ikke kontrollert. Antall stillinger, faktisk konsulentbesparelse og gjennomføring kan ikke fastslås fra disse passasjene. Ingen hypotese om slike virkninger er opphøyet til kildefaktum.
- **Rånavn:** Post 22 heter kulturmiljøforvaltning i omtalen og kulturminneforvaltning i forslag-/vedtakstabellene. Begge bevares. «01» og «1» bevares rått, med eventuell separat kanonisk kontokode.
- **Omtale uten beløpskobling til 210:** Post 60/Vega gjelder fullmaktsleddet II og det separate vedtak 211, ikke de to beløpshendelsene. Det skal være mulig å beholde teksten med tom relasjon til 210s posthendelser og eksplisitt grunn.
- **Feilaktig rollearv:** Mindretallsomtale i fellesdebatten for sakene 23–25 kan gjelde Prop. 25 S/Innst. 85 S. Den er ikke en mindretallsbegrunnelse under Innst. 81 S. Se [uavhengig komitékontroll](komite-kontroll.md).

Strukturert beviskjede er ikke faglig godkjenning av startsaldo, historisk kjede eller årsdekning. Seks før-/endrings-/etterobservasjoner i eksisterende 210-grunnlag beskriver **to posthendelser**. Flere tekster, forslag og relasjoner skal ikke øke hendelsesantallet. De to vedtatte deltaene er heller ikke et mål på «konsulentbesparelse» som kan summeres over begge postene.

## Kontroll og videre mandat

`hent-originaler.py` er kun avgrenset undersøkelsesinnhenting; vellykkede originaler overskrives ikke ved gjentatt kjøring. Feilloggen er historisk, og skriptet skal ikke brukes som versjons-/rettelsesadapter. `kontroller-kilder.py` kontrollerer de seks vellykkede originalhashene og lager passages.json/PDF-tekstene på nytt uten nettverk. Bibliotekversjonene står i passages.json. Ingen funksjonstest eller faktisk omtaleeksport er hevdet utført i O1.

[Utført kontroll](verification.json): seks originalhash-/bytekontroller, fire uendrede støttefiler, 18 gjenfunne HTML-blokker med eksakt tekst, 82 lokale dokumentlenker, fem visuelt kontrollerte PDF-sider og syntakskontroll av de to undersøkelsesskriptene bestod. `git diff --cached --check` bestod med bevarte kildemellomrom. Alle seks Git-blober er kontrollert mot mottatt originalhash; avgrensede .gitattributes-regler hindrer linjeskiftnormalisering. Ruff var ikke tilgjengelig i den bundlete kjøretiden; produktets tester/CI er ikke kjørt for denne dokument- og kildeleveransen. Kontrollskriptet kjøres med `python docs/research/omtale-o1/kontroller-kilder.py` fra reporoten og krever lxml og pypdf som angitt i passages.json. PDF-rendringen brukte pypdfium2; de midlertidige bildene ligger utenfor repoet i arbeidsområdets `outputs/o1-pdf-kontroll`.

Se [godkjent O2-spesifikasjon og oppdeling](o2-forslag.md) for leveranse, avhengigheter og akseptkriterier. Prosjekteieren godkjente oppdelingen og gjennomføring av #34/O2a 22. oktober 2026. #35/O2b krever eget senere mandat. O1-originalene og deres hasher beholdes uendret i O2a-kandidaten.
