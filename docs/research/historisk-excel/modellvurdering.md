# Kontroll av faktiske historiske Excel-filer 2013–2025

Undersøkt 20.10.2026, skrivebeskyttet innholdskontroll. Kilden er branch `feature/historisk-excel-2013-2025`, festet til revisjon `da720e9dd4ebfff31d88c14488c5f3217d045786`. Dette er kildefunn og modellråd, ikke godkjenning av historiske analysetall. Ingen originalarbeidsbok er lagret på nytt eller endret.

## Grunnlag og dekning

[Foreløpig kildebeskrivelse](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/docs/historiske-excel-2013-2025.md) ble lest før filene. Alle 13 faktiske originaler ble lastet ned fra samme revisjon og kontrollert mot [kilderegisterets SHA-256 og byteantall](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/kilderegister.csv). Alle 13 samsvarer. Profilen omfatter alle celler i alle 26 ark, ikke bare stikkprøver.

| År og original | Rådataposter | Dokumentrader | Kap/post/upost-nøkler med flere dokumentrader |
|---|---:|---:|---:|
| [2013](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2013_samlet_inputdata.xlsx) | 1 835 | 1 067 | 234 |
| [2014](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2014_samlet_inputdata.xlsx) | 1 999 | 1 065 | 256 |
| [2015](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2015_samlet_inputdata.xlsx) | 1 805 | 1 221 | 297 |
| [2016](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2016_samlet_inputdata.xlsx) | 1 818 | 1 075 | 240 |
| [2017](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2017_samlet_inputdata.xlsx) | 1 807 | 1 136 | 255 |
| [2018](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2018_samlet_inputdata.xlsx) | 1 796 | 1 081 | 237 |
| [2019](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2019_samlet_inputdata.xlsx) | 1 801 | 1 140 | 279 |
| [2020](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2020_samlet_inputdata.xlsx) | 1 802 | 1 473 | 392 |
| [2021](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2021_samlet_inputdata.xlsx) | 1 799 | 1 407 | 368 |
| [2022](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2022_samlet_inputdata.xlsx) | 1 840 | 1 464 | 363 |
| [2023](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2023_samlet_inputdata.xlsx) | 1 811 | 1 860 | 458 |
| [2024](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2024_samlet_inputdata.xlsx) | 1 871 | 1 371 | 371 |
| [2025](https://github.com/depmartin/budsjetthistorikk/blob/da720e9dd4ebfff31d88c14488c5f3217d045786/data/historisk/original/2025_samlet_inputdata.xlsx) | 1 836 | 1 271 | 328 |

Totalt 23 820 rådataposter og 16 631 dokumentrader, eksklusive overskrifter. Overskriftene er identiske mellom årgangene innen hver arktype: 14 rådatakolonner og 15 dokumentkolonner, som beskrevet i kildebeskrivelsen. Arknavnene stemmer også, inkludert `Rådata2025` og skrivemåten `DokumentiltknyntningYYYY`. Ingen formler ble funnet i de 26 arkene. Beløp er numeriske, rådatabeløp både heltall og desimaltall, dokumentbeløp heltall. Ingen tomme beløpsceller ble funnet; dette beviser ikke at kildens null betyr et reelt nullbeløp. Dokumentbeløpene omfatter 7 123 negative og 37 uttrykkelige nuller.

## Viktigste funn med konkrete kildeceller

### 1. Enhetshypotesen må korrigeres og verifiseres før importgodkjenning

Det er sterk intern støtte for **millioner kroner i rådata og kroner i dokumentarket**, ikke tusen kroner i rådata. Eksempel 2013: `Rådata!N3=2`, mens `Dokumentiltknyntning2013!A2:D2=(1,50,0,2000000)`. Eksempel 2025: kap. 20/post 1 har `Rådata2025!I6=K6=-6`, og `Dokumentiltknyntning2025!A2:D2=(20,1,0,-6000000)`. 2025s underpost 2 ligger på rådatarad 7 med nullendring, mens dokumentets rad 2 er postnivå (`upost_nr=0`).

Et uavhengig offisielt kontrollanker er [Blå bok 2013, trykt side 8](https://www.stortinget.no/globalassets/pdf/vedtatt-budsjett/vedtatt_budsjett2013.pdf) og [vedtak 74 i sak 55105](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?p=55105): kap. 1/post 1 er 10 032 000 kroner. Den faktiske arbeidsbokens `Rådata!H2=10.032` (underpost 1, eneste rådatarad for denne posten) samsvarer ved faktor 1 000 000. Kontrollankeret er kontrollert mot den offisielle vedtakssiden; rå XML i arbeidsboken bekrefter H2 som `10.032`. Dette verifiserer én konkret sammenligning og støtter milliontolkningen, men godkjenner ikke automatisk alle års kolonner og dokumentbeløp.

En prøverelasjon `(f176 + f177 + Nysald-prop) × 1 000 000 = sum dokumentbeløp` stemmer innen 0,001 kroner for 10 066 av 10 190 eksakt felles kap/post/upost-nøkler. Relasjonen er bare et undersøkelsesverktøy: den inkluderer ikke lønnsoppgjøret, og de to arkene kan beskrive ulike behandlingsledd. Den godkjenner verken hele beløpsenheten eller additivitet. Uavhengig kildeavstemming av et bredere utvalg per år og beløpskolonne gjenstår. Modellen må bevare rå numerisk verdi, original enhet/ukjent enhet, eventuell normalisert kroneverdi og brukt omregningsregel.

Rå OOXML inneholder også flyttallsspor: 2015 `Rådata!G2` er lagret som `10.829000000000001`, selv om openpyxl viser 10.829. Ikke bruk binære flyttall som faglig pengemodell. Bevar originalbyte og definer dokumentert presisjon/avrunding før kroner godkjennes. En avrundingsregel skal ikke gjette bort reelle desimaler.

### 2. Budsjettstadium, beløpsbetydning og behandlingsledd er forskjellige akser

2025 kap. 100/post 21 (`Rådata2025!B36:N36`) har saldert `H36=11.979`, RNB-forslag `I36=0`, stilling inkl. RNB `J36=6.979` og første halvårs tillegg `K36=-5`. Dokumentrad 15 har endring -5 000 000, tom proposisjonskode og `F15=i540/24-25`. RNB-forslag og senere/stortingsbehandlet resultat er derfor ikke utskiftbare. Det er 100 rader i 2025 og mellom 58 og 197 per år hvor f148 og f176 er forskjellige.

Gul bok/saldert/f150 er navngitte nivå-/stadiekandidater. f148, f176, f177, f179 og Nysald-prop er endrings-/aggregatkandidater som må få særskilt fortolkning. Ikke summer et nivå med alle endringskolonner uten å vite hvilke perioder og hendelser som allerede inngår. En aggregert f176-verdi kan ikke uten videre gjøres til ett nytt stortingsvedtak.

### 3. 2015 har en konkret datakvalitetsfelle

Alle 1 805 celler i `Rådata!J2:J1806` (f150) er **numerisk 0**. Samtidig er `H2=10.829` og `H3=169.386`. I 1 770 rader stemmer ikke `f150 = saldert + f176` innen toleranse 0,0000001 råenheter. Dette beviser ikke årsaken, men nullkolonnen kan ikke presenteres som verifisert budsjettstilling eller tolkes automatisk som manglende/null kroner. Bevar observert null med en særskilt faglig kontrollmarkering. Også 2013 (3 rader), 2016 (85) og 2018 (1) bryter den prøverelasjonen. Andre årgangers treff er ikke bevis på en universell regel.

### 4. To kildeark har forskjellig detaljeringsgrad

Ingen rådataark har gjentatt `(Kap, Post, Upost)`. Ingen av de 13 rådataarkene har samtidig underpost 0 og ikke-null underpost for samme kap/post. Dermed ble den foreløpige risikoen for samtidig posttotal og underposter **ikke observert innen rådataarkene**. Det finnes likevel postnivå i dokumentarket og underposter i rådata. 2025 kap. 20/post 1 er rådataradene 6–7 med underpost 1 og 2; dokumentrad 2 har underpost 0. En direkte kobling på kap/post vil gjenta dokumentbeløpet på to rådatarader, mens kobling på kap/post/upost mister treffet.

Underposter 1–2 i vanlige driftsrader og underposter opptil 6 i dokumentarkene må bevares. Eksempel 2013 `Dokumentiltknyntning2013!A687:D694` har kap. 2470/post 24 og flere positive/negative underpostkomponenter. Posttekst «Driftsinntekter» på en slik komponent endrer ikke kapittelets utgiftsklassifikasjon. Modellen trenger eksplisitt nivå, parent/komponentrelasjon og en regel for hvilke rader som summeres i et bestemt uttrekk. `0`, ukjent underpost og konkret underpost må kunne holdes fra hverandre.

### 5. Dokumenthenvisninger er flertydige, flere per beløp og iblant ufullstendige

I 2025 er kap/post/upost-nøkkelen gjentatt for 328 nøkkelgrupper i dokumentarket. Dette er ikke automatisk dubletter: kap. 21/post 1 rad 3 har 8 200 000 med `p146/24-25` og `i540/24-25`; rad 4 har 10 100 000 med `p26/25-26` og `i75/25-26`. Ingen eksakt identiske hele dokumentrader og ingen gjentatt kombinasjon av kap/post/upost + alle tre dokumentkoder ble funnet i noen av årgangene. Faglig dublettkontroll kan likevel ikke reduseres til dette testresultatet.

2017 rad 495 har alle tre referanser: `p141/16-17`, `i445/16-17`, `v963/16-17`. Ett beløp må kunne ha flere dokumentrelasjoner med rolle; tre referanser beviser ikke tre separate beløp eller at samme beløp er regjeringens forslag, komitéforslaget og vedtaket. Skap ikke tre finansielle hendelser fra én kildebeløpsrad.

Det finnes beløp med bare vedtaksreferanse: 2021 `Dokumentiltknyntning2021!A356:G356=(581,70,0,260000000,None,None,v663/20-21)`. 2014 rad 978 har `G978=VedtakRNB`; 2015 rad 30 har `G30=VedtakDok8`. Disse er ikke entydige dokumentidentifikatorer. 2021 rad 1001 har den mulig trunkerte strengen `v1280/20-2`; behold den ordrett og la tolket sesjon/lenke være uavklart. Ingen obligatorisk proposisjon, innstilling eller Storting-API-ID kan kreves for å bevare en historisk rad.

### 6. Budsjettår, sesjon og dato må holdes separat

2025 dokumentrad 4 gjelder filens budsjettår 2025, men viser sesjon `25-26`. Dette er ikke i seg selv feil: budsjettåret og sesjonen er ulike dimensjoner. Bevar budsjettår fra filinventar, rå dokumentkode og eventuell sikkert tolket sesjon hver for seg. Arbeidsbøkene inneholder ikke en egen vedtaksdato-kolonne. Ikke konstruer dato eller full hendelsesrekkefølge fra radrekkefølge eller behandlingsrunde alene.

### 7. Departement og øvrig organisasjon må være årsspesifikk

2025 kap. 20 dokumentrad 2 har `K2/gdep_nr=92`, `L2/fdep_nr=16`, `O2=Regjeringen`, mens rådata `A6=16`. 2015 kap. 1 har `Rådata!A2=5`, mens 2013/2025 samme kapittel har 15. Historiske koder kan altså ikke overstyres med dagens navn og nummeroppsett. Bevar Dep, gdep_nr, fdep_nr og gdep_navn hver for seg med kilde og budsjettår; behold også omr_nr og kat_nr. Ingen av de kap/post-koblingene som kunne sammenlignes hadde rådata-Dep forskjellig fra dokumentets fdep_nr, men dette er en observert sammenheng, ikke en universell kontrakt.

### 8. Forslag og endelig behandling kan avvike mellom arkene

2025 kap. 1850/post 75 har `Rådata2025!N1287=0`, men `Dokumentiltknyntning2025!D769=25000000` med bare `i75/25-26`. Kap. 5800/post 50 har rådata `N1837=31790.393`, dokument `D1272=34352393000`, sammen med proposisjon og innstilling. Dette er observerte avvik, ikke automatisk feil. En mulig forklaring er forskjell mellom nysalderingsforslag og vedtatt resultat; den krever dokumentkontroll. Ikke korriger ett ark til det andre eller bruk differansen som en ny selvstendig vedtakshendelse uten bevis.

Ingen regnskapskolonne ble funnet i de 26 arkene. Historikk til og med regnskap krever ytterligere kilde, ikke ommerking av Nysald-prop eller f150.

## Konsekvens for nåværende modell

Krav, GLOSSARY og ansvarsdeling peker allerede riktig: separate kildeadaptere, skille forslag/vedtak/regnskap, nivå/endring, underposter og tidsavgrensede departementsregistre. Arkitekturen trenger derfor ingen omstart. **Den implementerte B1-modellen er derimot for smal som felles historisk modell.** `Decision` krever Storting-identitet og API-metadata når et vedtak finnes, `Allocation` har ikke underpost/stadium/enhet/departement eller selvstendig budsjettår, og `Report` binder beløp til ett vedtak. B2s identitet og revisjoner gjelder nettopp Storting-objekter; de er ikke generelle historiske Excel-identifikatorer. Eksisterende HTTP-proveniensgrense kan heller ikke ta en arbeidsbok uten feilaktige metadata.

Før historisk import og samlet fremstilling bør en separat kontrakt beskrive minst:

- Kildeartefakt og import: kildeart, filnavn/hash/byteantall, budsjettår, ark/rad/celle, originalverdi, adapter-/tolkningsversjon og kontrollstatus. Identitet fra kilde og plassering er adskilt fra faglig hendelsesidentitet.
- Tallobservasjon: kapittel/post/underpost/nivå, budsjettår, original og tolket enhet, normalisert beløp der avklart, talltype (forslag/vedtak/regnskap/uavklart), stadium/behandlingsrunde og beløpsbetydning (nivå/endring/komponent/aggregat). Kildeverdier og avledede tall må være adskilt.
- Dokumentreferanser som egne relasjoner med råkode, tolket type/nummer/sesjon, rolle, eventuell verifisert URL og kontrollstatus. Det skal være mulig med flere eller ingen identifiserte dokumenter per observasjon.
- Historiske registeropplysninger med gyldighet og separate koder for administrasjon, Gul bok, programområde og kategori. Ikke overskriv kildens navn med moderne navn.
- Avstemming mellom overlappende kilder/aggregater og hendelser før godkjent summering. Bevar uavklarte konflikter og manglende dekning. Ingen automatisk B2-sammenslåing med senere API-materiale bare fordi år/kap/post/beløp samsvarer.
- Fremtidig kapittel-/postomtale som egen kildeforankret tekst med dokument/versjon/seksjon og relasjon til kapittel/post. Tekst kan eksistere uten beløp; samme beløp kan ha flere tekstreferanser.

Bevar B1/B2 som kompatible innganger for deres dokumenterte snitt. Historiske reelle data bør få et uttrykkelig historisk datasett og adapter, ikke merkes som `prove` for å passere B2s produksjonsgrense 2026–2027. Dette er et forslag til videre spesifikasjon, ikke en allerede vedtatt migreringsbeslutning.

## Anbefalt oppfølging i arbeidsplanen

Dette er forslag til videre arbeid, ikke oppstart av en byggeticket eller endring av godkjent leveranseomfang:

1. **Før bygging av #6:** spesifiser et lite, felles observasjonsformat der talltype, behandlingsrunde og beløpsbetydning er adskilt. Opprinnelig vedtak og senere vedtatte endringer er det første støttede snittet. En aggregert historisk kolonne skal kunne bevares uten å bli oppdiktede enkeltvedtak. Dette viderefører #6s allerede godkjente krav om plass til senere kilder; full historisk import trenger ikke blokkere #6.
2. **I #7/#8:** bruk konkrete underpost- og departementsprøver fra filene til å kontrollere kildehierarki, tidsavgrensede registre og manglende oppslag. Avklar særlig om rådataarkets underpostinndeling har samme faglige betydning som underpostene i dokumentarket før sammenkobling.
3. **For #13:** avklar enheter og kolonnenes behandlingsledd, og del eventuell bygging i små komplette importleveranser. Begynn med ett budsjettår fra uendret original til sporbare observasjoner og kontrolluttrekk; prøv deretter årgangsvariasjonene og avstemming. Originalfiler som nå ligger på historikkbranchen trenger ikke kopieres inn i denne dokumentasjonsleveransen.
4. **Ved senere forslag, regnskap og omtale:** legg til egne adaptere mot samme faglige kontrakt. Kapittel-/postomtale lagres som egne dokumentseksjoner, med tekst, versjon, lokator og relasjoner til år/kapittel/post. Tekstlagring skal kunne brukes uten en beløpsrad. Manglende omtale i historiske filer skal vises som manglende kilde.

Et langt observasjonsformat med én beløpsobservasjon per kildecelle eller dokumentrad gjør nye budsjettstadier mulige uten nye beløpskolonner i databasen. Kildenære felter og uavklarte verdier beholdes; normaliserte felter får dokumentert tolkning og proveniens. Fremtidige analysevisninger kan pivotere formatet tilbake til kolonner. Det konkrete databaseskjemaet og migreringen avgjøres i den aktuelle byggeticketen.

## Reproduksjon og begrensninger

Read-only openpyxl 3.1.5 ble brukt til full inventering, og standardbibliotekets ZIP/XML til å inspisere rå numerisk cellerepresentasjon. Undersøkelsen brukte to lokale profileringsskript og JSON-profiler utenfor produktrepoet. Metoden var å kontrollere hash/byteantall mot inventaret, lese alle ark med både formel- og verdiinnstilling, telle nøkler og datatyper, sammenholde eksakte nøkler mellom arkene og inspisere utvalgte rå XML-celler. Filhashene ble kontrollert på nytt etter lesingen; alle samsvarte. Ingen `Workbook.save` ble brukt. Råarbeidsbøkene ved den festede revisjonen, tabellen og cellehenvisningene over er det varige kontrollgrunnlaget. Ingen Excel-reberegning er hevdet; det finnes ingen observerte formler som krever slik beregning. Kontrollresultatene gjelder den festede revisjonen. Én offisiell enhetskontroll inngår som beskrevet ovenfor. Kolonnenes fullstendige faglige betydning, enheter for alle år/kolonner, dokumentkodenes autoritative koblinger og fullstendighet mot eksterne kilder er ikke samlet uavhengig verifisert i denne filgjennomgangen.
