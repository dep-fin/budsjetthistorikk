# H 2024: presisjon, restliste og hierarki

Kildekontroll utført 22. oktober 2026 for P13-P2/#26 under #13, mot basen `6b19a5ca7a74aa905e5ac42b7e624dacf81952bc`. [Aggregert resultat og proveniens](precision-summary.json) er maskinlesbart. Dette er en forskningsavledning med et betinget presisjonsforslag. Ingen normalisert eller kontrollert verdi, tidligere tolkning, kjede eller faglig godkjenning er endret. #13 og #10 forblir åpne. Nye offisielle kilder skal fortsatt behandles uavhengig av Excel-historikken.

## Grunnlag og etterprøvbarhet

Originalen er hentet binærsikkert fra `da720e9dd4ebfff31d88c14488c5f3217d045786:data/historisk/original/2024_samlet_inputdata.xlsx`: 257 569 byte, SHA-256 `870d30d55b4f7f6791fe48ea2a15aa3e98d61946393385d0411e46a0169f60f3`. Alle 1 871 H-cellers leksikalske XML-verdier og kapittel/post/underpost er sammenholdt med den eksisterende v3-pakkens celler, observasjoner og kandidater. Pakkemanifestets hash er `a7f93975b596ae3afd3e53b7825ff1027bc7a576c78640d02491fb30588714d7`; de tre faktisk leste JSONL-filene er kontrollert mot manifestets hash og størrelse. H-observasjonenes normaliserte/kontrollerte beløp er fortsatt null.

Beløpsreferansen er det tidligere publiserte `docs/research/issue-2/aar/blaabok_posts.json`, 227 236 byte, SHA-256 `7f85002b543a57b3948170f102dc581f66d5ca1b5c1372198433ecd05b0b337e`. Dette er sammenligning mot et eksisterende avledet beløpsuttrekk, ingen ny full parsing av PDF-beløp. Original [Blå bok 2024](https://www.stortinget.no/globalassets/pdf/budsjettsiden/blaabok_2024.pdf) er også hentet på nytt 22. oktober: 3 842 617 byte, SHA-256 `7204477be2b1ed089ae2d2eca1307a96d5929d04ea5a0d874ca32eeae1a53bf8`, identisk med den dokumenterte forelderen. En separat koordinatbasert **kontonøkkelskanning** av PDF-side 11–74, trykt side 9–72, gir nøyaktig samme 1 574 kapittel/post-nøkler. Den skanner kontokoder og kildeplassering, og oppretter ingen ny beløpsreferanse. PDF-side 11 og 74 er dessuten rendret og visuelt kontrollert.

Hele lokal-ledgeren beholder alle 1 694 unionnøkler med celle-/observasjons-/kandidat-ID, leksikalsk verdi, eksakt Decimal-kroneverdi, referanserad og differanse. `ledger.jsonl`: 1 858 305 byte, SHA-256 `fdefab468ed78be626f78439d92c4feb89799f9f547116b05104d93fa03917f9`. Den ligger sammen med original, kildesnapshots, eksperimenter og separate rest-/hierarkilister i det lokale arbeidsområdet `work/p2-precision`, utenfor produktrepoet. Fullt inventar, råpakker, arbeidsbokmetadata og interne filstier er ikke kopiert til denne rapporten eller den offentlige JSON-en.

## Hele unionen er disponert

| Baseline uten avrunding eller toleranse | Én H-rad | To H-rader | Nøkler |
| --- | ---: | ---: | ---: |
| Eksakt heltallig kronekandidat | 808 | 39 | 847 |
| Ikke-heltallig kronekandidat | 595 | 131 | 726 |
| Bare Excel, observert rå 0 | 112 | 8 | 120 |
| Bare referanse, 5999/90 | 0 | 0 | 1 |
| **Union** | **1 515** | **178** | **1 694** |

Excel har 1 693 nøkler og referansen 1 574; 1 573 er felles. Ingen felles heltallig kandidat avviker. De to H-radene i en nøkkel summeres kun som et merket kontrollaggregat. Tabellen gir ingen godkjenning av komponentrelasjonen.

## Måling av samtlige 726 presisjonsspor

Differansen er `sum(Decimal(original H-leksem) × 1 000 000) − referanse i hele kroner`, uten binær flyttallsaritmetikk i pengesummen. Alle 726 er målt. De omfatter 857 H-rader, hvorav 131 nøkler har to rader.

| Absolutt differanse i kroner | Nøkler |
| --- | ---: |
| Større enn 0 og mindre enn 0,00000001 | 460 |
| Fra 0,00000001 til under 0,0000001 | 197 |
| Fra 0,0000001 til under 0,000001 | 53 |
| Fra 0,000001 til under 0,00001 | 14 |
| Fra 0,00001 til og med 0,00002 | 2 |
| **Sum** | **726** |

Det fullstendige eksakte histogrammet står i JSON-en. 388 differanser er negative og 338 positive. Minste absolutte differanse er `1E-13` kr; største er `0.00002000000` kr. Signert minimum er `-0.00001000000` og maksimum `0.00002000000` kr. De to største er:

- `H537`, 571/60: leksikalsk `170591.75599999999`, kandidat `170591755999.99999000000`, referanse 170 591 756 000 kr; differanse −0,00001 kr.
- `H1872`, 5800/50: leksikalsk `336484.23200000002`, kandidat `336484232000.00002000000`, referanse 336 484 232 000 kr; differanse +0,00002 kr, Blå bok PDF-side 74/trykt 72.

Dermed kan en mikrogrense fra den tidligere avgrensede prøvens 103 nøkler ikke overføres til hele H. To spor er på minst 0,00001 kr, og ytterligere 14 ligger fra 0,000001 til under 0,00001 kr.

På **cellenivå** gir 787 H-celler ikke-heltall i kroner. 418 residualer er negative og 369 positive. 783 slike celler ligger i de 726 ikke-heltallige nøklene; fire ligger i to ellers eksakte aggregatnøkler, fordi to residualer opphever hverandre. Av de 726 nøklene har 669 én slik celle og 57 to. Aggregering kan altså skjule presisjonsspor. Største individuelle residual er også 0,00002 kr. Avrunding per celle og etter aggregering gir samme heltall for alle 1 693 Excel-nøkler i dette eksperimentet; dette beviser ingen generell additivitet.

### Binær representasjon og et avgrenset regelforslag

For hver celle er nærmeste hele krone beregnet fra det bevarte Decimal-leksemet, uten referansebeløpet som input. Alle 787 ikke-heltallige celler har nøyaktig samme binære 64-bits flyttallsverdi som dette heltallet dividert med 1 000 000. Avstanden mellom de to binære tallene er dermed 0 ULP. Den **leksikalske Decimal-avstanden** til heltallskandidaten er samtidig høyst `0.8796093022208` ULP i råenheten. En antatt grense på en halv ULP ville derfor vært feil. Dette er forenlig med binær serialisering av den samme tallverdien; det beviser ikke hvilken programvare eller eksportoperasjon som skapte filen.

Den konservative kandidaten `H2024-binary-compatible-integer-NOK-proposal-1` er frosset i separat JSON før ny numerisk sammenligning. Regelen gjelder bare originalhashen over, 2024, `Rådata`, H, og krever:

1. Separat dokumentert millionenhet og relevant post-/komponentomfang. Ingen formel eller ikke-numerisk verdi.
2. `n = (Decimal(leksem) × 1000000).to_integral_value(ROUND_HALF_EVEN)`.
3. `abs(Decimal(leksem) − n/1000000) <= Decimal.from_float(math.ulp(float(leksem)))` og `float(leksem) == float(n/1000000)`.
4. `math.ulp(float(leksem)) × 1000000 < 0.5`, slik at intervallet er langt smalere enn en krone og ikke kan romme to hele kroneverdier.

Flyttall brukes her bare til å undersøke representasjonen; kandidaten og differansen beregnes med Decimal. Største observerte ULP-bredde i kroner blant alle H-celler er om lag 0,0001164153 kr. Ingen referanseavhengig nærmeste-verdi, tusenavrunding eller bred absolutt samsvarstoleranse inngår. Et tidlig deskriptivt forsøk med absolutt tak på 0,0001 kr er beholdt lokalt, men anbefales ikke som kildebegrunnet regel.

Den uavhengige talltransformasjonen produserer og lagrer alle cellekandidater **før** referansebeløp kobles på: 1 871/1 871 består de numeriske vilkårene; kontrollaggregater gir 1 573/1 573 eksakte treff, inklusive alle 726 tidligere ikke-heltallige nøkler. Regelhash: `518c469ad313e58df0498aab78486f80a946608fe37dabb9784b09be334e4180`. Lokal kandidatfilhash: `787573cfdfb51d3c1351997323ed0844fd02743fa6ecedf8fd5c5bcb29f130d6`. Regelen er utformet etter den deskriptive målingen; dette er ingen blind holdout-validering eller faglig godkjenning.

**Det avgrensede kilde-/faktorsamsvaret er verifisert.** Faktoren 1 000 000 gir kontrollkandidater mot de 1 573 felles postaggregatene. Etter den separate numeriske regelen gir alle 1 573 eksakt samsvar. Dette kildefunnet krever ingen eksportmanual i tillegg til de utførte kontrollene. Blå bok viser kroner; alle 1 574 referansebeløp er hele kroner og multipler av 1 000.

**Generell enhet, normalisering og hierarki er separate spørsmål.** Arbeidsboketiketten angir saldert stadium uten uttrykkelig enhet. Ingen opprinnelig eksportinstruks som fastsetter en generell millionenhet, er funnet. Regelen er fortsatt et forslag, og kontrollaggregater er ingen godkjent komponentrelasjon. De gamle `normalized_kr` og `controlled_kr` står uendret som null. En eventuell aktivering krever en ny versjonert beslutning for et uttrykkelig omfang; funnet over godkjenner ingen andre kolonner eller år.

## De 120 Excel-restene: kildeomfang fremfor oppdiktet null

Alle 120 er fraværende i det originale Blå bok-hovedbudsjettets postnøkkelsett, også ved den nye nøkkelskanningen. De omfatter 128 H-celler, alle med numerisk rå 0. 75 nøkler ligger på kapitler uten hovedbudsjettkapittel; 45 mangler som post innen et kapittel som finnes. Fravær her beviser ikke at kontoen aldri har eksistert eller ikke kan brukes gjennom året.

| Kategori med kildebevis | Nøkler | Konsekvens |
| --- | ---: | --- |
| Gamle konti i offisiell flyttetabell, med ny konto til stede i Blå bok | 64 | Bevar Excel-raden som gammel kontoposisjon; ikke opprett nullbevilgning eller flytt beløpet automatisk. |
| Uttrykkelig nullomfang i offisiell flyttetabell, 1530/30 | 1 | Kontoen er dokumentert selv om en bevilgningsrad mangler; null er ingen ny bevilling eller ny start. |
| Post mangler i eksisterende Blå bok-kapittel; årsak ikke fastslått | 39 | Oppbevar som kildeobservert null med konkret reststatus. |
| Kapittel mangler i hovedbudsjettet; årsak ikke fastslått | 16 | Bevar konto og null; ingen konklusjon om ikke-eksistens eller startsaldo. |
| **Sum** | **120** | **Ingen blir referansebeløp 0.** |

De 64 flyttingene er dokumentert ved [Prop. 1 S Tillegg 2, vedlegg 2](https://www.regjeringen.no/no/dokumenter/prop.-1-s-tillegg-2-20232024/id3013673/?ch=6), tabellrad for eksakt gammel/ny kapittel/post. Eksempler er 510/1 → 1510/1, 540/23 → 1540/23, 3505/90 → 4565/90 og 5570/70 → 5579/70. Alle 64 nye kontonøkler er til stede i den uavhengige Blå bok-referansen. De åtte restnøklene med to H-rader tilhører denne gruppen; gruppen har 72 H-rader. Det er ikke brukt en generell +1000-regel: 525 → 1520, 545 → 1550 og 546 → 1551 er moteksempler. Enkelte kapittel beholdes også gjennom omorganiseringen, blant annet 2445.

[Tillegg 2, punkt 2.2](https://www.regjeringen.no/no/dokumenter/prop.-1-s-tillegg-2-20232024/id3013673/?ch=2) forklarer at vedlegget også omfatter poster uten foreslått bevilgning. Tabellen har uttrykkelig 530/30 → 1530/30 med 0 i tusen kroner. Dette er et konkret moteksempel til at fravær fra hovedbudsjettets beløpsrader betyr ikke-eksisterende konto. Den eksakte raden og XPath er beholdt i lokal klassifikasjonsledger.

De resterende 55 er også søkt som nøyaktig kapittel/post i [Gul boks opprinnelige hovedforslag, vedlegg 1](https://www.regjeringen.no/no/dokumenter/prop.-1-s-gul-bok-20232024/id2998593/?ch=10), uten treff. Dette undersøker bare forslagsoversiktens kontoomfang, og bruker ikke forslagsbeløp som vedtak. For de 39 finnes kapittelet, men ikke posten, eksempelvis 118/75, 228/85, 2440/31 og 5460/89. For de 16 finnes ikke hovedbudsjettkapittelet, eksempelvis 951/71, 3952/90, 5547/70 og 5584/70. Beviset gjelder de oppgitte hovedtabellene, og avgjør ikke om raden er en senere opprettet post, en tidligere brukt reservekonto, en gammel kontoplanposisjon eller en lokal katalogplassholder. Eierens neste oppgave er å fremskaffe eksportens katalog-/nullsemantikk og eventuelle konkrete opprettelses-/avviklingsvedtak for disse 55. Ingen av dem kan godkjennes som faktisk bevilgning 0 på dette grunnlaget.

Komplett lokal klassifikasjon har én post per restnøkkel, original-/referanseomfang, eksisterende kapittelside og postliste, eventuell offisiell flytting og XPath. `classification.json`: SHA-256 `f2f2c986ceb6ed39048766ddbe57c8368007dea3e1c8c738293bcae5fa7c0748`, 118 321 byte. Den offentlige rapporten gir kategorier og kildebelagte representanter; rå celleinventar for hele restlisten forblir lokalt.

## 5999/90 er et faktisk Excel-fravær

Blå bok PDF-side 74, trykt side 72, kapittel 5999/post 90, har 101 874 353 000 kr. Originalsidens beløp og plassering er visuelt kontrollert, og samsvarer med det eksisterende avledede JSON-uttrekket. Kontoen finnes ikke blant originalens H-rader. Dette er statsbudsjettets finansieringspost og inngår i kontrollunionen. Den får ingen konstruert Excel-rad, nullstart eller balanserende mellomendring; den tidligere sperrede finansieringskjeden er fortsatt sperret.

## Hierarki og tillatt bruk

Alle 178 nøkler med flere H-rader har nøyaktig to rader: underpost 1 og 2 på post 1, med henholdsvis lønn/godtgjørelser og varer/tjenester i arbeidsbokens tekst. Ingen av dem inneholder samtidig underpost 0. 170 finnes i Blå bok: 39 er eksakte i baseline og 131 har presisjonsspor. Åtte gamle kontonøkler uten Blå bok-post har begge H-rader 0. Det er dermed ikke observert samtidig posttotal og komponenter innen H, men dette er ikke et bevis for generell hierarkisemantikk på tvers av ark eller kolonner.

For eksempel viser original `H6` og `H7` 20/1, kodene 1 og 2. De numeriske kandidatene summeres til 107 671 000 kr etter den separate presisjonsregelen; Blå bok PDF-side 11, trykt 9, viser én posttotal med dette beløpet. Offentlig primærkilde dokumenterer posttotalen, men gir ikke den interne arbeidsbokens fordeling mellom de to radene. Disse 170 summene kan derfor beholdes som merkede kontrollaggregater med begge innganger. De er fortsatt ikke godkjente komponentrelasjoner eller kildeobserverte nye posttotaler.

Det finnes også 21 **enkeltstående** postnøkler med underpost 1 eller 2. Koden beviser ikke at en annen komponent mangler. 1/1 er et konkret varsel: `H2` har kode 2 og arbeidsboktekst for varer/tjenester, mens original Blå bok kaller bevilgningen apanasje. Lik konto og beløp etablerer ingen universell betydning for kode 2.

Post 24 har et annet dokumentert kildehierarki. Blå bok PDF-side 55, trykt 53, viser seks komponenter under 2470/24 og én total på −15 000 000 kr. H har kun `H1352`, underpost 0, med `-15`, som numerisk svarer til totalen under millionhypotesen. Tilsvarende har H bare totalraden for 2445/24 og 5440/24, mens originalen viser egne komponenter, sistnevnte på PDF-side 69, trykt 67. Det er tillatt å kontrollere den konkrete H-raden mot **kildens posttotal**, og holde kildekomponentene som spesifikasjon uten å legge dem til totalen. De skal ikke summeres med H-totalen eller behandles som den samme typen som Hs interne lønns-/vareinndeling. Dokumentarkets komponentdeltaer er en annen kontroll og arver ingen generell relasjon herfra.

| H-omfang | Tillatt nå | Gjenstående port |
| --- | --- | --- |
| Alle 1 871 H-celler | Råbevaring, identifiserte Decimal-kandidater og synlige kontrollutfall | Dokumentert enhet og eventuell versjonert normaliseringsbeslutning |
| 1 403 felles nøkler med én H-rad | Eksakt kontroll mot dokumentert postfelt under prøvd faktor/presisjon | Riktig detaljnivå per rad, særlig de 17 kodede enkeltposisjonene i dette fellesutvalget |
| 170 felles nøkler med to H-rader | Kontrollaggregat med begge celle-ID-er | Eksportinstruks eller annet bevis for at dette er uttømmende, ikke-overlappende komponenter |
| 120 Excel-rester | Observert 0 og klassifikasjon/reststatus | Ingen generell nullgodkjenning; 55 kontoårsaker og eksportens nullsemantikk krever avklaring |
| 5999/90 | Separat offisiell referanse og synlig Excel-fravær | Ingen Excel-start eller kjedegodkjenning konstrueres |

Dette kontrollgrunnlaget overføres ikke til G/I/J/K/L/M/N eller dokument-D. Det godkjenner heller ikke historisk organisasjon eller periodedekning. De 726 sporene har ingen numeriske uteliggere under den foreslåtte binære representasjonskontrollen, men enhetsporten og de berørte hierarkiforholdene består.

## Nye kildebyte og reproduksjon

Alle nye nettsider er lest 22. oktober 2026 og beholdt lokalt. Hashene gjelder de faktisk hentede responsbytene, ikke eldre snapshots eller nettsiden som en uforanderlig kildeenhet.

| Lokal kildeidentitet | Byte | SHA-256 | Lokator |
| --- | ---: | --- | --- |
| Tillegg 2, vedlegg 2 | 100 729 | `db08dd2e55426ced1190d05d844ef4c4516956b6a666bdf1e42335ba157cfee3` | Gammel/ny kapittel/post-tabell; nøyaktig XPath per lokal klassifikasjon |
| Tillegg 2, kapittel 2 | 79 426 | `75ff9f4cc1561c634272f790c4d3263581e9bc8ac1e09c7f0761ad582ec77b47` | Punkt 2.2, avsnittet om vedlegg 2 og poster uten bevilgning |
| Gul bok, vedlegg 1 | 997 103 | `57d13cf12ca164bca2d82be82e5ba1902357353b757cd924fe7517c2e027ca06` | Hovedforslagets nøyaktige kapittel/post-rader |

Reproduksjon krever originalen, den hashfestede v3-pakken og den uendrede avledede Blå bok-JSON-en. De lokale eksperimentskriptenes hash, kandidatfil, fullledger og klassifikasjonsfiler er oppgitt i sammendraget. Ingen av skriptene ligger i produktrepoet. Fremgangsmåten kan også gjenbygges uten dem:

1. Hent originalbyte med `subprocess.check_output(['git','show','da720e9dd4ebfff31d88c14488c5f3217d045786:data/historisk/original/2024_samlet_inputdata.xlsx'])`, verifiser hash/størrelse og les H direkte med ZIP/XML. Ingen `Workbook.save` eller reberegning.
2. Knytt H-cellene til v3-pakkens celle-ID-er via ark/celle og verifiser konto, leksikalsk verdi og pakkens filhash. Beregn Decimal med presisjon 80 og faktor 1 000 000. Grupper alle H-rader på kapittel/post, og behold alle innganger.
3. Lag hele unionen med det eksisterende Blå bok-uttrekket. Rapporter de fire baselineutfallene, signerte differanser, eksakt histogram og individuelle residualer før en regel anvendes.
4. Frys det uttrykkelige kandidatforslaget. Beregn og lagre heltallskandidater med bare H som numerisk input, utfør ULP-/binærkontrollene, og sammenlign først deretter med referansebeløpene. Manglende referanse forblir manglende.
5. Hent de fire offisielle kildene med URL/hash over. Kontroller alle 120 restnøklers fravær i hovedtabellenes nøkkelsett; slå eksakt gammel konto opp i flyttetabellen. Behold 55 konkrete uavklarte kontoårsaker og skillet mellom kildeomfang og faktisk nullbevilgning.

Utførte kontroller omfatter alle original-H-leksemer/kontoer, manifest-/filhash, alle 1 694 disposisjoner, alle 726 differanser, alle 787 individuelle presisjonsspor, begge avrundingsrekkefølger, alle numeriske vilkår i kandidatforslaget, de 120 restnøklene mot primærkildens kontoomfang og de 64 offisielle flyttingene. Originalhash og de leste v3-filene er uendret. Ingen produksjonskode eller GitHub-status er endret, og ingen faglig godkjenning eller løsning av de tre historiske kjedekonfliktene er utstedt.
