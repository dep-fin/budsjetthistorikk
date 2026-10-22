# P13-P2: dokumentrester og to adaptergrenser i 2024

Kildekontroll 22. oktober 2026 for #26 under #13, mot kodegrunnlag `6b19a5ca7a74aa905e5ac42b7e624dacf81952bc`. Research-skillen, regnearkskillens leseregler og FINs språkprofil er brukt. Mandatet avgrenser arbeidet til kildefunn og reproduksjon, uten parserendring eller faglig aktivering. [Bevisfilen](decisions-evidence.json) har kildehash, URL, hentetid, felt, lokatorer, utførte kontroller og foreslåtte fremtidige forventninger. Status `source_verified` gjelder kildeinnhold; `professional_approval=false` gjelder hele leveransen.

De fem dokumentrestene har tre forklaringer. 151/70 har ingen endringsrad i den vedtatte RNB-tabellen, mens Excel bevarer en nullmarkering. Begge 5999/90-endringene mangler i Excel og inngår samtidig i en bekreftet kildekonflikt. De to Havtil-restene gjentar overganger som allerede finnes under en annen vedtaksidentitet. De tre berørte kjedene forblir sperret. De to adaptergrensene kan beskrives entydig mot kildene, men uendret v2 beholder sine gamle resultater.

## Frosset kontroll og utført reproduksjon

Originalen er lest direkte fra `da720e9dd4ebfff31d88c14488c5f3217d045786:data/historisk/original/2024_samlet_inputdata.xlsx`, SHA-256 `870d30d55b4f7f6791fe48ea2a15aa3e98d61946393385d0411e46a0169f60f3`, 257 569 byte. Ingen arbeidsbok er lagret på nytt. Rå OOXML-tall er lest som Decimal. Dokumentarket heter `Dokumentiltknyntning2024`.

Hele sammenligningen er beregnet på nytt fra alle 1 371 dokumentrader og det allerede publiserte `api_events.csv`, SHA-256 `ab9ef8abe7f1b508d54ca17e6f88209d061a6a6e2c8f312d5444894686642e31`. De samme 26 innstillingsgruppene som i [P1](../pilot2024.md) er brukt. Bare eksplisitte endringsrader med `level_not_delta != True` inngår. Forskningsfilens 0-baserte `row` er aldri brukt direkte som 1-basert lokator.

| Kontrollgrunnlag | Resultat |
| --- | ---: |
| Dokumentrader med rå underpostkode 0 | 1 359 |
| Excel-gruppenøkler etter merket kontrollaggregering | 1 355 |
| Eksplisitte deltanøkler i forskningsledgeren | 1 358 |
| Full nøkkelunion | 1 359 |
| Eksakte kontrollaggregater | 1 354 |
| Excel-nøkkel uten referanserad | 1 |
| Referansenøkler uten Excel-rad | 4 |
| Ulike felles beløp | 0 |

De tolv komponentradene er utenfor denne postkontrollen. De fire ekstra postradene aggregeres bare innen den frosne gruppe-/kapittel-/postnøkkelen. Kildecellene bevares separat; et aggregat oppretter ingen ny hendelse. Ingen toleranse, avrunding, fuzzy-deduplisering eller nullpåfylling inngår.

Alle tolv autentiske B3/B4/B6-fixtures er dessuten kjørt gjennom uendret `sync_saved` → B2/SQLite → uttrykkelig `storting-belop-v2`. Alle **2 894 observasjoner** er kontrollert mot lagret gjenlesing, forventet antall og identisk gjentatt uttrekk. Tolkningen er fortsatt `0cfb813792c1b5a607981719de27024fe2608fba6504bd9df4f4eb812f87cc4f`. Parserfilens SHA-256 er fortsatt `b9c9f3d0993ce66236a591b07bffbed132668b899035c86e09b9f63b7b3821b3`.

To nye komplette offisielle sesjonssvar er hentet, men er **ikke** kjørt som full v2-replay. Alle direkte felter i de tolv relevante vedtaksobjektene er sammenlignet kanonisk mot fixturene; alle er like, inklusive nøyaktig HTML-tekst. Nye sesjonshasher er `66aa3ac5e93598fbbf2c02577c025395ea43a6bb7148e83a79f639bac9b09a57` (2023–2024) og `c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42` (2024–2025). Endret transportkonvolutt gir ingen ny bevilgning. Kildene er [sesjon 2023–2024](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2023-2024) og [sesjon 2024–2025](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025), hentet 22. oktober 2026.

## 151/70: begrunnet fravær av en endringsrad

Excel har `D43=0`, `E43=p104/23-24` og `F43=i447/23-24`. I rådata er `H70=J70=415.26`, `I70=-20` og `K70=0`. Regjeringens forslag er en reduksjon på 20 mill. kroner. Dette er kontrollert i bevart original HTML fra 21. oktober, SHA-256 `94cb91928eb173665de6111d13de6562b663fad8a4eddcdd01daab7b7fdf4594`, XPath `/html/body/main/div/div[3]/div[3]/div[33]/p`, og gjenlest 22. oktober. [Prop. 104 S kap. 151 post 70](https://www.regjeringen.no/no/dokumenter/prop.-104-s-20232024/id3039096/?ch=2).

Flertallet i Innst. 447 S omtaler en økning på 20 mill. kroner på posten. Dette står i punkt 1.1, XPath `/html/body/div[2]/div/main/div[2]/div/div[7]/div/div/div/div[2]/div[1]/p[47]`. Den endelige tilrådingens tabell, det vedtatte forslaget **40076251** under votering **23457**, vedtak **40033719** og referatets vedtatte tabell har alle **ingen 151/70-rad**. Tabellen går fra kapittel 151 til post 71 og videre til postene 73 og 74. Hele den relevante tabellen er kontrollert; alternative partiforslags rader er holdt utenfor. [Innst. 447 S](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2023-2024/inns-202324-447s/?all=true), [vedtatt forslag](https://data.stortinget.no/eksport/voteringsforslag?voteringid=23457), [referat 21. juni](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2023-2024/refs-202324-06-21/voteringer).

Votering 23457 vedtok A og B samtlige romertall med 55 mot 46 stemmer kl. 14.30.00. Sammenholdt med regjeringens reduksjonsforslag forklarer flertallsmerknaden og den vedtatte tabellen hvorfor posten ikke trenger en endringsrad. Den avgrensede klassifiseringen er `documented_no_change_row_in_adopted_table`. Excel-null kan brukes som dokumentert markering av uendret resultat i dette kontrollomfanget. Null er fortsatt **ikke et observert nullvedtak**. Det opprettes ingen bevilgningshendelse og ingen ekstra +20 mill.-hendelse fra merknaden. [Voteringsresultat i sak 98919](https://data.stortinget.no/eksport/voteringer?sakid=98919).

## 5999/90: Excel-fravær og fortsatt kjedekonflikt

Begge offisielle endringsrader mangler i dokumentarket. Originalbudsjettets 5999/90 mangler også i rådata, jf. [P1](../pilot2024.md). Dette er verifisert kildefravær i Excel. Offisielle vedtak viser reelle beløpsrader; utelatelsen kan derfor ikke godkjennes som fullstendig vedtaksdekning.

| Vedtak og kildefelt | 1-basert v2-lokator | Kroner og betydning |
| --- | --- | ---: |
| 40033025, original 2024 | `table[1]/tr[62]/td[4]` | Nivå 101 874 353 000 |
| 40033719, RNB | `table[1]/tr[1487]/td[5]` | Endring −101 874 353 000 |
| Samme vedtak, før/etter | `table[1]/tr[1488]/td[3]` | 101 874 353 000 → 0 |
| 40034287, nysaldering | `table[1]/tr[238]/td[4]` | Endring +18 497 356 000 |
| Samme vedtak, før/etter | `table[1]/tr[239]/td[3]` | 101 874 353 000 → 120 371 709 000 |

Enheten i tabellene er uttrykkelig kroner. RNB-raden finnes i Innst. 447 S, vedtatt forslag 40076251 og referat 21. juni. Nysalderingsraden finnes i Innst. 90 S, vedtatt forslag **40078385** under votering **23945**, og referat 19. desember. Votering 23945 vedtok resten av I samt II–IV enstemmig, etter egen behandling av 5800/50. Begge kontrollene er dermed knyttet til vedtatte tekster. [RNB-vedtaket](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40033719&p=98919), [Innst. 90 S](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-090s/?all=true), [nysalderingens forslag](https://data.stortinget.no/eksport/voteringsforslag?voteringid=23945), [referat 19. desember](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-19/voteringer).

Lokalt stemmer begge før + endring = etter. Kronologisk stemmer RNBs etterbeløp 0 ikke med nysalderingens førbeløp 101 874 353 000. Bokstavelig kjedesum blir 18 497 356 000; nysalderingens observerte sluttbeløp er 120 371 709 000. Differansen 101 874 353 000 gir ingen kildeobservert mellomøkning. Klassifiseringen er `excel_missing_and_published_chain_conflict`, med separat kontrollert sluttbeløp og sperret additiv kjede. Postens finansieringsrolle er behandlet i [den tidligere kildeundersøkelsen](../../issue-2/finansiering/README.md); den gir ingen tillatelse til å omskrive RNB-raden.

## Havtil: to vedtaksidentiteter med samme overgang

Excel har bare `D881=10988000` for 1860/1 og `D1211=-2400000` for 4860/1, begge knyttet til i99/24-25. I i93/24-25 mangler begge rader. Følgende opplysninger er bekreftet mot de nye sesjonssvarene og uendret v2:

| Konto | Før, kroner | Delta, kroner | Etter, kroner | Lokator i 40034064 / 40034226 |
| --- | ---: | ---: | ---: | --- |
| 1860/1 | 349 324 000 | +10 988 000 | 360 312 000 | Delta `tr[68]/td[5]` / `tr[32]/td[5]`; før/etter `tr[69]/td[3]` / `tr[33]/td[3]` |
| 4860/1 | 85 800 000 | −2 400 000 | 83 400 000 | Delta `tr[165]/td[5]` / `tr[43]/td[5]`; før/etter `tr[166]/td[3]` / `tr[44]/td[3]` |

Alle lokatorene ligger i `table[1]`. Vedtak **221 / 40034064**, 17. desember, og **365 / 40034226**, 18. desember, har forskjellige identiteter og datoer. Begge par finnes i komiteenes tilråding, voteringsforslag **40077095** og **40077047**, og de relevante referatene. Voteringene **23880** og **23976** vedtok henholdsvis I–III og I samt III enstemmig. [Innst. 99 S](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-099s/?all=true), [Innst. 93 S](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-093s/?all=true), [forslag 23880](https://data.stortinget.no/eksport/voteringsforslag?voteringid=23880), [forslag 23976](https://data.stortinget.no/eksport/voteringsforslag?voteringid=23976).

Innst. 93 S sier samtidig at kapittel 1860 og 4860 behandles av arbeids- og sosialkomiteen. Denne avgrensningen står fortsatt sammen med postene i den publiserte tilrådingen. De undersøkte kildeversjonene og målrettede søk 22. oktober ga ingen konkret uttaksrettelse. Tidligere visuell kontroll av den beriktigede PDF-en og departementets dokumenterte økonomiske gjennomføring er beskrevet i [Havtil-undersøkelsen](../../issue-2/dobling/README.md). Den nye kontrollen omfatter HTML, XML og stemmeresultater; ingen ny visuell PDF-kontroll eller ny råhenting av tildelingsbrevet hevdes.

Restene klassifiseres `excel_missing_repeated_transition_two_adopted_decision_ids`. En økonomisk opptelling én gang per overgang har kildebegrunnelse, men eventuell aktivering krever en særskilt, sporbar faglig avgjørelse. Begge formelle vedtaksobservasjoner bevares. Godkjent additiv kjede forblir sperret. Å telle på nytt gir 371 300 000 og 81 000 000 kroner og bryter med de publiserte før-/etterparene. Likhet mellom HTTP-hentinger av samme ID kan håndteres av B2; likt beløp på **to** vedtaks-ID-er kan ikke slettes ved generell deduplisering. [Referat 17. desember, sak 3](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-17/voteringer), [referat 18. desember, sak 14](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-18/voteringer).

## 228/85 og 2440/31: dokumenterte forventninger til en ny tolkning

**228/85:** Excel `D124=30000000` treffer forskningsledgeren. Uendret v2 lager én observasjon på `table[1]/tr[143]/td[5]`, med råbeløp `30 000 000`, enhet `Kroner`, NOK, faktor 1, presisjon hele kroner og `amount_kr=30000000`. Betydningen er fortsatt `uavklart`, med `ukjent_ledd` og `til_kontroll`. Kildens inline-markering deler ordet som `b<span …>evilges</span>`. Parserens tekstlesing gir «b evilges med». Det samme markupmønsteret finnes i tilråding, vedtatt forslag og referat. Dette er en adaptergrense i betydningstolkningen; beløpsenheten er allerede uttrykkelig dokumentert.

Kildens sammenheng er en ny bevilgning under endringer i 2024-budsjettet. Fremtidig forventning er **endring +30 000 000 kroner**, på postnivå og som enkeltledd. Ingen før- eller etterobservasjon finnes i raden. Disse feltene skal forbli fraværende. Prop. 104 S omtaler særtilskuddet på ny post 85 og 30 mill. kroner, bevart original XPath `/html/body/main/div/div[3]/div[3]/div[91]/p`. [Forslaget](https://www.regjeringen.no/no/dokumenter/prop.-104-s-20232024/id3039096/?ch=2), [vedtatt RNB-forslag](https://data.stortinget.no/eksport/voteringsforslag?voteringid=23457).

**2440/31:** Excel `D914=11900000000` treffer forskningsledgeren. Den autentiske raden er `table[1]/tr[37]`, med postråtekst `(NY) 31`, formål «Kjøp av eigardelar, blir løyvd med» og beløpsfelt `td[5]=11 900 000 000`. Tabellhodet sier `Kroner`. Uendret v2 lager **ingen** observasjon for denne kontoen og bevarer radavviket. To selvstendige mønstre trenger behandling i en ny adapter: markøren `(NY)` må skilles fra postnummeret, og nynorsk «blir løyvd med» må gjenkjennes. Bare en kontoendring ville fortsatt etterlate betydningen uavklart.

Fremtidig forventning er **endring +11 900 000 000 kroner**, NOK, faktor 1, hele kroner, post 31, enkeltledd og budsjettår 2024. Markøren `(NY)` og råverdien bevares. Ingen førbeløpsobservasjon eller nullstart opprettes. Samme rad finnes i Innst. 93 S, forslag 40077047 og referat 18. desember. Regjeringens formelle forslag har samme bevilgning i kroner. Forslagets særskilte oversikt viser dessuten gjeldende 0, ny 11 900 og endring 11 900 **mill. kroner**. Dette er egne forslagsfelter; forslagsnull skal ikke settes inn som et manglende førfelt i vedtaket. [Prop. 27 S vedtaksforslag I](https://www.regjeringen.no/no/dokumenter/prop.-27-s-20242025/id3075697/?ch=5), [forslagets SDØE-oversikt](https://www.regjeringen.no/no/dokumenter/prop.-27-s-20242025/id3075697/?ch=3).

Følgende målrettede regresjoner anbefales for en eventuell **ny** adapter-/tolkningsversjon. De er forventninger, og er ikke implementert som parserendring her:

1. Reproduser v2 uendret: 228/85 gir én uavklart observasjon på 30 000 000; 2440/31 gir ingen observasjon; hele fixtureutvalget gir 2 894. De utførte prøvene ovenfor dekker dette.
2. Prøv ny tolkning mot den autentiske splittede ordmarkeringen, med rå HTML og kronerfelt bevart. En generell sammenskriving av vilkårlige ord tillates ikke.
3. Prøv `(NY) 31` og «blir løyvd med» samlet, med positivt endringsbeløp, bevart markør og fraværende før-/etterfelt. «Ny» alene gir aldri nullstart.
4. Bevar eksisterende v2-JSON, ID-er og standardvalg. Ny tolkning får egen identitet og må vise begge resultatene side om side.
5. Bevar sperrene på 1860/1, 4860/1 og 5999/90, også om de to adaptergrensene senere løses. En parserretting kan ikke forene de publiserte kjedekonfliktene.

## Anbefalte matriserader og tillatt kontrollbruk

| D-omfang | Verifisert kildefunn | Tillatt bruk i kontrollmatrisen | Gjenværende grense |
| --- | --- | --- | --- |
| Alle 26 grupper, kode 0 | 1 354 eksakte aggregater og fem navngitte rester | Eksakt matematisk kontroll med faktor 1, alle cellepekerne bevart | Ingen generell godkjenning av dokumentidentitet, hierarki eller årsdekning |
| i447, 151/70, D43 | Observert Excel-null; ingen vedtatt endringsrad | Forklart nullmarkering/uendret resultat; rårest beholdes | Ingen ny nullhendelse eller +20 mill.-hendelse |
| i447 og i90, 5999/90 | Offisielle deltaer uten Excel-rader; før/etter-konflikt | Vis begge kildebeløp og separat sluttbeløpskontroll | Additiv kjede sperret; eier må godkjenne eventuell avklart bruksrolle |
| i93, 1860/1 og 4860/1 | To vedtak gjentar overgangene fra i99 | Vis begge identiteter og forslag om avgrenset ikke-additiv rolle | Ingen formell uttaksrettelse; ingen automatisk opptellingsvekt eller generell deduplisering |
| i447, 228/85, D124 | Råbeløp og kroner verifisert; v2-betydning uavklart | Kildekontrollert beløpsanker, fremtidig tolkningsforventning separat | Eksisterende v2-observasjon forblir uavklart |
| i93, 2440/31, D914 | Ny bevilgning og kroner verifisert; v2 mangler observasjon | Kildekontrollert beløpsanker og synlig parserrest | Ny adapter kreves; ingen nullstart |

Faglig aksept og aktivering av tillatt analysebruk er separate fra disse kildefunnene. Nye offisielle tall kan fortsatt registreres uten historisk Excel, gammelt register eller inngående startsaldo. Manglende start sperrer bare beregninger som trenger den. #13 og #10 forblir åpne.

## Reproduksjon, bevis og begrensninger

Skriptene og komplette råresponser ligger bare lokalt under `work/p2-decisions/` i det ytre arbeidsområdet. `reproduce.py` leser originalbloben, beregner hele D-unionen, gjenoppretter de tolv B2-fixturene i `bounded.sqlite` og kontrollerer lagring/gjentakelse. `inspect_sources.py` viser tabell-/avsnittssteder i de offentlige kildene. `build_evidence.py` kontrollerer alle HTTP-hasher, sammenligner de tolv aktuelle objektene og bygger den begrensede bevisfilen. `check_evidence.py` verifiserer alle 20 HTML-lokatorer, seks lokale før/delta/etter-forhold, tre bevarte kjedekonflikter og begge uendrede adapterutfall; resultatet er `all_passed` i lokal `checks.json`. Kjør med P1s eksisterende Python 3.12-miljø, med repoet `work/p13-p2` som kodegrunnlag. Ingen skript trenger å kjøre fra produksjonsområdet eller endre originalene.

De utførte kontrollene omfatter full D-union, alle tolv uendrede fixtureuttrekk, begge aktuelle adaptergrenser, lokal før/delta/etter-aritmetikk, begge Havtil-voteringer, RNB-/nysalderingsvoteringene og de tilhørende forslagene og referatene. Fullstendige sesjonssvar er kildekontroll, mens 1 354-treffresultatet fortsatt er sammenligning mot den hashfestede forskningsledgeren. Ingen ny full v2-årsavstemming, kjedegodkjenning eller generell kolonnenormalisering hevdes.

Ny direkte henting av Prop. 104 S og korrekt Prop. 27 S ga HTTP 403. P1s bytebevarte Prop. 104 S er verifisert og gjenlest; Prop. 27 S er lest på den offisielle nettsiden uten påstått råhash. Ingen innlogging eller tilgangsomgåelse er brukt. HTML- og XML-kildene gir tabellstruktur og eksakte beløpsfelt; ny PDF-rendering inngår ikke. Negative rettelsesfunn er avgrenset til de undersøkte dokumentene og målrettede søkene, uten garanti om alle historiske publikasjoner.

Offentlig bevisfil inneholder bare begrensede kontrollrader, kildeidentiteter og korte tekstutdrag fra offentlige dokumenter. Ingen ny kopi av originalarbeidsboken, fullstendig historisk celleinventar, interne metadatafilstier eller komplett sesjonsråfil legges til repoet. Produksjonskode, eksisterende v2-resultater, gamle pakker, GitHub og drift er uendret.
