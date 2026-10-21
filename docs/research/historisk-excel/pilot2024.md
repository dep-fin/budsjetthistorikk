# Teknisk kontroll av hele 2024-piloten

Utført lokalt 21. oktober 2026 for #24 under #13. Dette er kontroll av den historiske adapteren og eksportløpet. Samsvar godkjenner ingen enkeltverdi, kjede eller årsdekning. #13 gjelder fortsatt øvrige år, og #10s faktiske driftsaksept gjenstår. Samlet review, separat sikkerhetsaudit, CI og merge er orkestratorens etterfølgende leveringsporter.

Denne rapporten gjelder den korrigerte `historisk-excel-2024-v3`, celleinventar `historisk-celler-3` og `historisk-sammenligning-2`. Nytt uttrekk er `8efe8b7f75226514d4b713f3259880e8df6c0666715ac2a811dae7a38997bf43`. Tolknings-/kontroll-ID-ene følger den aggregerte JSON-en. De tidligere lokale v1-/v2-databasene og fullpakkene er beholdt som egne tolkningsgrunnlag. V1-uttrekk `fd9408abdf04167241ed6bc5fdbcc7db51cfc2f087bf07f4ee5ee20c7e0fb645` og v2-uttrekk `c84d07592ad4ba6e1745445153c9fde8e5e6c3f6ece0ebeb888bd4f6e9400b96`, med sine sammenligningsrapporter, er gjenlest uendret. Databasehashene var like før og etter lesing, og alle tidligere pakkefiler har bevart hash/størrelse. Manifestene har fortsatt SHA-256 `940d4abc787575566625ae5370b373ac83c8ca10012f4c45332892121c3012ea` (v1) og `e7422a25f81d8840867689c455b1543474387ba3a7b4d706380ce2e68f507aaf` (v2).

## Original, inventar og faktisk eksport

Originalen er hentet binærsikkert fra `da720e9dd4ebfff31d88c14488c5f3217d045786:data/historisk/original/2024_samlet_inputdata.xlsx`. Den har SHA-256 `870d30d55b4f7f6791fe48ea2a15aa3e98d61946393385d0411e46a0169f60f3` og 257 569 byte. Bytene er bevart uendret i SQLite og kontrollert ved gjenlesing. Den historiske branchen er ikke flettet.

| Omfang | Fysiske OOXML-celler | Fraværende posisjoner i dimensjonen | Inventarposisjoner | Beløpsobservasjoner |
| --- | ---: | ---: | ---: | ---: |
| Rådata, A1:N1872 | 26 208 | 0 | 26 208 | 14 968 |
| Dokumentiltknyntning2024, A1:O1372 | 18 444 | 2 136 | 20 580 | 1 371 |
| Hele arbeidsboken | 44 652 | 2 136 | 46 788 | 16 339 |

Hver av de åtte rådatakolonnene har 1 871 observasjoner; dokument-D har 1 371. Overskrifter, metadata, referanser, blanke felt og ukjent innhold har egen disposisjon og stabil celle-ID. Originalen har ingen observerte formler. Rå XML, lagringstype, leksikalsk verdi, eventuell formel/cache, løst shared-string-innhold, skjulte rader/kolonner og arbeidsbokmetadata bevares. Stilintervallet på hele kolonnebredden utvider ikke rutenettet. Syntetiske prøver dekker fysisk innhold utenfor dimensjonen og formel-/feilceller.

Alle 1 371 dokumentobservasjoners kapittelnavn og formål er kontrollert mot en separat lesing av originalarbeidsboken og deretter i faktisk publisert Excel. Dokumentarkets J er kapittelnavn og H er postens formål. I bevares som separat rå stikkordstekst i inventar og radkontekst. D2 gir «Statsministerens kontor» og «Driftsutgifter». V1 brukte I/J feil; rettingen er gitt ny tolkningsidentitet og omskriver ingen lokalt lagret v1-observasjon.

Den faktiske pakken har 16 339 observasjoner, 46 788 celler, 16 339 kandidater, ni kolonneregler, 51 837 avviksrader og 4 312 sammenligningsrader. Avviksantallet er tekniske/faglige markeringer, blant annet gjentatt åpen enhet, organisasjon og hierarki; det er ikke 51 837 bekreftede økonomiske feil. Alle JSONL-filer og faktisk Excel med videreføringsdeler er lest tilbake mot SQLite før katalogpublisering, og hele den publiserte pakken er deretter kontrollert igjen. En gjentatt full kjøring gjenbrukte samme uttrekk og verifiserte samme pakke.

Den korrigerte v3-kjøringens manifest har SHA-256 `a7f93975b596ae3afd3e53b7825ff1027bc7a576c78640d02491fb30588714d7`. Kontroll-Excel er 26 528 236 byte, SHA-256 `bab6b4693e445023cadddea5b554db5fc07f97bfe4bf0ac61f209449d017a171`. Disse identifiserer den konkrete lokale eksporten; en ny database kan gi andre API-replay-ID-er og pakketidspunkter uten at kildeverdiene endres. Den [aggregerte rapporten](pilot2024/summary.json) bevarer konkrete uttrekks-/tolknings-/kontroll-ID-er.

## Hele H mot uavhengig Blå bok

Referansen er de 1 574 postnivåene i det allerede publiserte `blaabok_posts.json`, SHA-256 `7f85002b543a57b3948170f102dc581f66d5ca1b5c1372198433ecd05b0b337e`, 227 236 byte. Forelder er [Blå bok 2024](https://www.stortinget.no/globalassets/pdf/budsjettsiden/blaabok_2024.pdf), SHA-256 `7204477be2b1ed089ae2d2eca1307a96d5929d04ea5a0d874ca32eeae1a53bf8`. Side og y-posisjon følger hver referanse. Dette er PDF-forskningens postuttrekk, ingen ny full API-v2-replay.

Alle 1 871 H-celler inngår. De gir 1 693 kapittel/post-nøkler. Underpostceller summeres bare som et merket kontrollaggregat, med alle celle-/observasjons-ID-er beholdt. Mot referansens 1 574 nøkler er unionen **1 694**:

| Utfall | Nøkler |
| --- | ---: |
| Eksakte hele kronekandidater | 847 |
| Ikke-heltallige kronekandidater | 726 |
| Bare Excel | 120 |
| Bare referanse, 5999/90 | 1 |
| Ulike sammenlignbare heltallsbeløp | 0 |

De 120 Excel-nøklene omfatter 128 H-rader, alle med observert rå 0. De er fortsatt uten referanserad og blir ikke innlemmet i de 847 treffene. 5999/90 mangler i Excel og får ingen nullstart. Alle 726 desimalspor beholdes med eksakt Decimal-verdi. Ingen toleranse eller avrunding er brukt. Dette er kontroll av matematisk samsvar under den prøvde faktoren, uten generell enhets- eller hierarkigodkjenning.

## Hele dokument-D mot separat forskningsledger

Alle 1 371 dokumentrader er bevart. F er fylt på alle rader og har 26 innstillingsgrupper. E er fylt på 1 341 rader og mangler på 30. G mangler på alle disse 2024-radene. Dokumentreferanser er relasjoner til ett kildebeløp; de skaper ikke ekstra vedtak. Det er 1 359 postrader med rå underpostkode 0 og tolv komponentrader.

De 26 kontrollkoblingene er fryst fra det uavhengige `description_inventory.csv` før utfallet brukes. Hash er `3f267dddbd26434febd976c9a5b9940d40362d0fbedb567485857342871be56e`. Sammenligningsbeløpene hentes fra det allerede publiserte `api_events.csv`, SHA-256 `ab9ef8abe7f1b508d54ca17e6f88209d061a6a6e2c8f312d5444894686642e31`, 854 328 byte. Hele filen har 2 935 hendelsesrader, hvorav 1 574 opprinnelige og 1 361 senere representasjoner. Bare eksplisitte senere deltaer inngår her; `level_not_delta=True` holdes utenfor. Foreldrebyte, sesjoner og opprinnelig kildeproveniens følger [inputmanifestet](../issue-2/aar/input_manifest.json).

`description_inventory.csv` og `decision_inventory.csv` er tekstmetadata med fast CRLF i arbeidskopien gjennom `.gitattributes`. Deres rapporterte hasher identifiserer de faktisk leste kontrollbytene. Git lagrer disse to tekstblobene med LF; de er ikke rå HTTP-foreldre. Fast utsjekkingsformat gjør kontrollhashene like på Windows og Linux. De tidligere bytebevarte beløpsartefaktene og API-fixturene endres ikke.

Excel gir 1 355 gruppenøkler fra 1 359 postrader. Ledgeren gir 1 358 eksplisitte deltanøkler. Unionen er **1 359**: **1 354 eksakte kontrollaggregater**, én Excel-nøkkel uten referanse og fire referansenøkler uten Excel. Ingen felles heltallsbeløp avviker.

Excel-resten er i447, 151/70, `D43=0`. Referanserestene er RNB og nysaldering på 5999/90 samt de to gjentatte Havtil-deltaene på 1860/1 og 4860/1 i i93. Kildene beholdes; ingen mellomendring eller ny nullhendelse fyller restene.

Dette er en **egen forskningsrepresentasjon**, som også har 228/85 og 2440/31. Den endrer ikke v2-parseren eller de avgrensede v2-resultatene nedenfor. Ledgerens HTML-radnummer er 0-basert og merket slik. Det settes ikke direkte inn som en 1-basert v2-lokator.

## Separat reproduksjon av den avgrensede prøven

De samme tolv autentiske fixturene som i [pilotkontrollen](pilotkontroll.md) er lest gjennom uendret B2/SQLite og uttrykkelig `storting-belop-v2`. Alle **2 894 observasjoner** er gjenlest eksakt, og gjentatt uttrekk er identisk. Datasett `prove` gjelder bare API-fixture-replayen; Excel-observasjonene bruker `historisk`.

- H-utvalgets 375 nøkler gir **271 eksakte**, **103 presisjonsavvik** og **ett Excel-fravær**, 5999/90. Hele H-resultatet over erstatter ikke dette ankeret.
- De sju senere objektene gir **854 eksakte** dokumentdelta-kontroller og **sju rester** på unionen 861: tre Excel-nøkler uten sikkert v2-delta og fire v2-deltaer uten Excel.
- Seksten separat avledede komponentdifferanser gir **tolv eksakte** og **fire Excel-fravær ved beregnet 0**. Tre posttotaldifferanser er bevart separat med begge innganger og telles ikke som komponenter eller nye kildehendelser.

V2 gir fortsatt uavklart betydning på 228/85 i 40033719, til tross for råbeløpet 30 000 000. V2 lager fortsatt ingen beløpsobservasjon fra `(NY) 31` på 2440/31 i 40034226. Den separate ledgerens treff løser ingen av disse parsergrensene.

## Kontrollstatus for alle ni kolonner

Alle ni regler har åpen enhet/presisjon/stadium/betydning for generell faglig bruk. De konkrete kontrollene nedenfor er avgrensede bevis; de gir ingen godkjent kolonnetolkning. Normalisert NOK og kontrollert NOK står som null. Kronekandidaten er en separat Decimal-streng.

| Kolonne | Utført kontroll eller uttrykkelig rest |
| --- | --- |
| G, Gul bok | `G2` på 1/1 prøves mot regjeringens faktiske forslag 14 768 000 i [Prop. 1 S Gul bok, vedlegg 1](https://www.regjeringen.no/no/dokumenter/prop.-1-s-gul-bok-20232024/id2998593/?ch=10). Rå OOXML gir desimalspor, ingen avrunding. Et vedtak brukes ikke som forslag. |
| H, saldert | Hele nøkkelunionen mot Blå bok ovenfor; underpostrelasjonen er fortsatt åpen. |
| I, RNB-forslag | `I70=-20` på 151/70 gir −20 000 000, eksakt mot forslaget i [Prop. 104 S, kap. 151 post 70](https://www.regjeringen.no/no/dokumenter/prop.-104-s-20232024/id3039096/?ch=2). `K70=0` og dokument-D43=0 er andre kildefelt og andre behandlingsledd. |
| J, stilling inkl. RNB | `J1360=12210` på 2541/70 prøves mot v2s **etterbeløp** 12 210 000 000 i 40033719 `table[1]/tr[1071]/td[3]`. Treff er et nivå, ikke et delta. Hele periodedekningen er åpen. |
| K, første halvår | `K1360=-608` prøves mot −608 000 000 i 40033719 `table[1]/tr[1070]/td[5]`, med dokument-D938 bevart separat. Aggregatet oppretter ingen ekstra hendelse. |
| L, etter RNB | `L1360=0.4` prøves mot 400 000 i 40033805 `table[1]/tr[4]/td[4]`, med dokument-D939 separat. Perioder og overlapp er åpne. |
| M, lønnsoppgjør | `ikke_utfort`: intet frosset uavhengig beløpsfelt for faktisk talltype og omfang. Dette er en åpen kontroll hos eieren. |
| N, nysalderingsforslag | `ikke_utfort`: intet frosset faktisk forslagsfelt. Samme tall som et senere vedtak ville ikke verifisert forslagsstatusen. Dette blokkerer denne sammenligningens aksept, uten å blokkere råimporten. |
| Dokument-D | Hele 26-gruppeunionen og separate komponentkontroller over. Faktor 1 er prøvd, men generell talltype, hierarki og hendelseskobling godkjennes ikke. |

G/I-kildene er lest fra offisielle nettsider 21. oktober 2026 og bevart lokalt. HTML-foreldrene har henholdsvis SHA-256 `09fca3a509d9b2d342187fee691b5faf378373fe25992538c8f6735cbe194bd8` (998 471 byte) og `94cb91928eb173665de6111d13de6562b663fad8a4eddcdd01daab7b7fdf4594` (1 014 253 byte). Den [begrensede referansefilen](pilot2024/proposal-refs.json) bevarer URL, foreldrehash, nøyaktig XPath, konto, talltype og kontrollbeløp. Full HTML publiseres ikke her. M og N har egne `ikke_utfort`-rader; de skjules ikke som beståtte kontroller.

## Regresjoner, kompatibilitet og videre ansvar

De fem nødvendige review-/auditfunnene er rettet med offentlige regresjonsprøver: H/I/J holdes atskilt; alle formelvarianters tilstedeværelse sperrer cache som kronekandidat; gjenbruk av shared strings og gjentatte råkontekster har samlede grenser; sammenligningsomfang bindes til valgt tolkning/kandidat og referansens faktiske kildeår; og alle runnerutdata kollisjonskontrolleres før første skriving. Sammendrag publiseres atomisk uten overskriving. Den autentiske originalen er også prøvd som en fil kalt `summary.json` i utdatakatalogen: kollisjonen avvises, ingen database opprettes og originalhashen er uendret.

Den siste områdesperren i v3 gjelder også array/shared/dataTable-celler uten eget `<f>`, når de ligger i et deklarert resultatområde. Små syntetiske prøver viser bevart cache og egen XML, synlig avvik og ingen kandidat/treff for både anker og dekket celle; en numerisk celle utenfor området beholder kandidaten. Sen XML-plassering av anker og fysisk cache utenfor arkdimensjonen er prøvd. Enkeltcelle-array og blanke/fraværende posisjoner bevares. Ugyldige, ustøttede og overlappende områder avvises, og samlet deklarert areal kan ikke overskride posisjonsgrensen. Begrensede kolonneintervaller kontrollerer eksisterende inventar uten å materialisere formelrektanglets celler. Den autentiske originalen har ingen formler; de rapporterte beløpskontrollene og antallene er uendret.

V2 teller høyst 16 777 216 tegn samlet løst celleinnhold og reserverer høyst 268 435 456 konservativt beregnede JSON-tegn for materialisert innhold. Hver shared-string-bruk teller, også når ZIP-innholdet er lite. Hele radkonteksten serialiseres én gang per rad; alle beholdte gjentakelser budsjetteres før større hash-/JSON-kopier. Lange legitime tekster og Excel-videreføring er fortsatt prøvd innen grensene. Dette er eksplisitte omfangsgrenser, ingen generell garanti for vilkårlig store arbeidsbøker.

Den lukkede kontrollprofilen angir år, valuta, kildefaktor, talltype, betydning, nivå, side, stadium, periode og referansegrunnlag. Den ligger fra v2 i tolkningen og hver kandidat, og må samsvare med kontrollens og referansens omfang. Ukjent eller uforenlig omfang avvises før frysing, selv ved samme tallverdi. H-nivå, dokumentdelta og avledet komponentdifferanse har egne profiler; komponentkontrollen krever begge innganger. Profilene er matematiske hypoteser for de valgte kildefeltene. De endrer ingen åpen faglig observasjonsakse, og D får ingen oppdiktet felles behandlingsrunde.

Deterministiske CI-prøver bruker små, tydelig syntetiske arbeidsbøker og allerede offentlige autentiske API-fixtures. De prøver kilde–SQLite–gjenåpning–pakke–faktisk Excel, presisjon, blank/fravær/null, flere dokumentreferanser, skjult/ukjent innhold, formel-/feilceller, ZIP/XML-/ressursvern, nye immutable kilder/tolkninger og eksplisitt forgjenger. Avbrudd før lagring, etter lagring/før pakke og tapt kvittering etter katalogpublisering prøves. Endrede JSONL-, manifest-, Excel- og videreføringsfelt avvises, også når en angriper oppdaterer filhashen.

En autentisk ny kilde på en konto uten registeroppslag/start går gjennom uendret offisiell innlesning, lagring, gjenlesing og Excel fra en egen tom database og arbeidsmappe. Prøven gjentas med fraværende, korrupt og motstridende historisk fil. Det nye deltaet bevares; beregning som trenger start får `manglende_start`. Den gamle standardparseren er fortsatt v1, og eldre skrivere kan skrive i en pilotdatabase uten å miste historiske resultater.

Teknisk kildebevaring, åpen kolonnetolkning, faglig godkjenning og årsdekning har separate statusfelt. Ingen historisk departementskode gis dagens registerkobling. Kjedekonfliktene **1860/1, 4860/1 og 5999/90** er fortsatt sperret. Eieren må avklare generell kolonnebetydning, M/N-kilder, historisk organisasjon og hierarki før faglig bruk innen de berørte omfangene.

## Publiserbarhet og reproduksjon

Den nye offentlige leveransen inneholder kode, syntetiske testdata produsert i testene, denne rapporten, aggregert JSON og to begrensede kontrollreferanser fra offentlig publiserte regjeringsdokumenter. Forskningsreferansene og API-fixturene er tidligere publiserte filer og identifiseres med egne hasher/foreldre. Ingen ny kopi av original-XLSX, fullstendig celleinventar eller kandidatfil legges til Git. Interne filstier i originalens metadata gjengis ikke i rapporten eller den offentlige JSON-en. Full lokal pakke er beholdt i arbeidsområdet.

Reproduksjonskommandoer, offentlige funksjoner, pakkeformat og ressursgrenser står i [pilotveiledningen](../../historisk-pilot.md). CI trenger ingen historisk original eller live kilde. Faktisk fullkontroll krever den hashfestede originalen og kjøres separat lokalt.

De nye offentlige avledningene er hashfestet slik: `pilot2024/summary.json` er 4 460 byte, SHA-256 `96a6c1821fe7830a9b5d129e85eb004ea193ffdcfad0e4d26644250993414047`; `pilot2024/proposal-refs.json` er 2 650 byte, SHA-256 `a575250891ca2165074b104d9c82b0f2b0131bf6a7e06f84dc754dea6bca7751`. Den første er en aggregert lokal kontrollavledning fra originalhashen og de oppgitte kontrollreferansene. Den andre avleder to begrensede forslagsfelt fra de to offentlige HTML-foreldrene med XPath. Ingen av dem inneholder fullstendig råinventar eller interne filstier. Begge nye avledninger er lagret med UTF-8/LF. Forslagsfilens konti, beløp, HTML-foreldre og XPath-er er semantisk uendret; den har fått eksplisitt referanseomfang og kildeår. De tidligere bytehashene `79bd3b92dc873da026bcb806a4be06b981418e44f2286795df6d3b0781cbcecb` (v1-sammendrag), `cf26032eee53433bb82099ff27a3d3db49486f16a478418c2dfbb46745326a29` (v2-sammendrag) og `a8ba319e88496b7a50b7398ebe2b825e4f0530c4acb704a0e4b239184eca06dc` (tidligere forslagsavledning) identifiserer eldre avledninger. De nye hashene ovenfor erstatter ingen rå kilde- eller foreldrehash.

## Utførte kodekontroller

Den samlede testsuiten er kjørt én gang etter v3-rettingene: **556 bestått, to hoppet over, 229,92 sekunder**. Vertens rettigheter tillot verken den eksisterende Windows-prøvens symbolske lenke eller opprettelse av hardlink i kollisjonsprøven. De øvrige 74 pilotprøvene er kjørt målrettet. Områderegresjonen var rød gjennom offentlig import: H3 uten eget `<f>` ga feilaktig kandidat 2 000 000 under array/shared/dataTable. Den er grønn med v3, også gjennom sammenligning. Det er lagt til 18 testtilfeller siden v2, inkludert immutable v2-gjenlesing. Ruff check, Ruff format-kontroll og streng mypy for alle 44 produktmoduler er bestått. Full ny kjøring og gjentakelse på samme v3-database gjenbrukte uttrekk, kontroll-ID-er, sammendrag og verifisert pakke. Begge kjøringer kontrollerte originalhashen etter eksport. Det er ikke utført installasjon/driftsprøve, faglig godkjenning, eget samlet leveringsreview, separat sikkerhetsaudit eller merge som del av rettingsrollen.

`git diff --check` er bestått for hele kandidaten mot basen `a3fb29f4e72e1355d1625bbcfba2eef2595dd9cf`; begge nye arkivfiler er i tillegg kontrollert med `git diff --no-index --check` mot tom fil. Den vanlige Git-indeksen og commit-historikken er ikke endret. De offentlige JSON-avledningene og det frosne syntetiske v2-arkivet har eksplisitt bytebevaring med dokumentert hash. De hashfestede råkildene er ikke linjeavslutningsendret.
