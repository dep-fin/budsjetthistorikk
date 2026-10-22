# 2024: lønn, nysalderingsforslag og periodene i J/K/L

Undersøkt 22. oktober 2026 for #26 under #13, mot base `6b19a5ca7a74aa905e5ac42b7e624dacf81952bc`. **M har bare observerte nuller, mens den faktiske lønnskompensasjonen i 2024 ble foreslått sammen med nysalderingen. N har nå konkrete forslagsankre. L er en dokumentavgrenset restgruppe etter RNB; den kan ikke defineres bare ved en dato før nysaldering.** Dette er kildebevis og avgrensede matematikkontroller, ingen faglig kontrollavgjørelse eller årsdekning.

Den hashfestede originalen ved `da720e9dd4ebfff31d88c14488c5f3217d045786` er lest direkte som OOXML: 257 569 byte, SHA-256 `870d30d55b4f7f6791fe48ea2a15aa3e98d61946393385d0411e46a0169f60f3`. Originalen er uendret. Alle råbeløp er tolket fra den leksikalske `<v>`-teksten med `Decimal`, presisjon 80. Ingen avrunding eller toleranse er brukt. Faktor 1 000 000 er en uttrykkelig prøvd kandidatfaktor, ikke en ny generell normaliseringsregel.

[Maskinlesbare, begrensede bevis](stages-evidence.json) inneholder kilde-URL-er, dato/hash/byteantall, seks originale forslagsfelt med XPath, cellepekere og kontrollantall. HTML/PDF-foreldre, komplette rå-/restlister og undersøkelsesskriptene beholdes lokalt. De er ikke en ny publisert råpakke. `pilot2024.md` beskriver fortsatt den tidligere pilotkjøringens faktiske resultater; denne rapporten omskriver ikke pilotobservasjonene eller de tidligere `ikke_utfort`-radene i en lagret pakke.

## M: faktisk lønnskilde er funnet; null betyr ikke fravær av lønnskompensasjon

Alle `Rådata!M2:M1872` er numerisk 0: 1 871 nuller, ingen blanke eller ikke-null beløp. Dette er et fullkolonnefunn, ikke en stikkprøve. Det finnes derfor ingen positiv M-celle som kan bekrefte en millionfaktor eller et lønnstillegg.

[Prop. 36 S (2024–2025), kapittel 5](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=5), forklarer at den sene lønnsnemndbehandlingen førte til at kompensasjonen ble lagt inn som anslag i departementenes omgrupperingsproposisjoner. [Vedlegg 4](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=11) gir de enkelte kapittel/post-beløpene i kroner. Uttrekk av hele tabellens kontorader gir 165 positive poster, til sammen **2 620 361 000 kroner**, og én motpost på **2309/1, −2 620 361 000 kroner**. Fortegnssummen er 0. En kontroll som bare sammenligner totalsummen 0 med M, ville dermed gitt en misvisende bekreftelse.

På **20/1** foreslår [selve vedtaksforslaget i Prop. 36 S, romertall I](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=7) en økning på **2 006 000 kroner**, fra 107 671 000 til 109 677 000. Vedlegg 4 identifiserer samme beløp som lønnskompensasjon. I Excel er `M6=M7=0`, mens `N6=2.0059999999999998` og `N7=0`. Den matematiske postkandidaten fra N er `2005999.9999999998000000`, altså en ikke-null rå differanse på `−0.0000000002000000` kroner fra forslaget. Dokumentarket har `D2=2006000`, `E2=p36/24-25` og `F2=i90/24-25`. Forslagsfeltet, rå N-spor og senere dokumentrepresentasjon er tre forskjellige bevis.

Dette er tilstrekkelig til å avvise bruken «M=0 innebærer at lønnsoppgjøret mangler i årets endringer». Det er også et konkret motbevis mot å fylle M med den offentlige lønnsfordelingen og deretter legge den til uendret N. 20/1 ville da telle samme lønnskompensasjon to ganger. Den offentlige reserveposten er 2309/1; det er ikke grunnlag her for å bruke en antatt 2315-post.

**Tillatt nå:** råbevaring av M-nullene, kontroll mot vedlegg 4 og separat visning av offentlige lønnsforslag med egne kilder. **Fortsatt åpent:** hva produsenten mente med f179-nullene og en eventuell godkjent, særskilt lønnsfordeling. Ingen kilde dokumenterer at alle M-nullene er godkjente økonomiske nuller. Åpningen er dermed presis; den gjelder kolonnens betydning, ikke lenger fravær av en offentlig lønnskilde.

## N: forslagsidentitet er kontrollert uten å bruke vedtak som fasit

To tidligere tallankre er nå kontrollert mot de faktiske regjeringsforslagene:

| Excel og konto | Faktisk offentlig forslagsfelt | Resultat og presisjon |
| --- | --- | --- |
| `N1360=680`, 2541/70 | [Prop. 22 S (2024–2025), forslag, romertall I](https://www.regjeringen.no/no/dokumenter/prop.-22-s-20242025/id3075925/?ch=3), tabellens kapittel 2541/post 70: økning 680 000 000 kr, fra 12 210 400 000 til 12 890 400 000 | Eksakt ved faktor 1 000 000. Forslag av 22. november 2024; budsjettår 2024. Etterbeløpet har allerede med de særskilte 400 000 kronene i L. |
| `N1730=41500`, 5440/24 | [Prop. 27 S (2024–2025), tabell 3.1](https://www.regjeringen.no/no/dokumenter/prop.-27-s-20242025/id3075697/?ch=3), feltet for endring: 41 500 mill. kr; gjeldende nivå 191 800, foreslått nytt nivå 233 300 | Eksakt samsvar med det tabellrapporterte forslaget. Tabellen opplyser avrunding til nærmeste 100 mill. kr. Treffet gir ikke finere kildepresisjon. Forslaget er datert 22. november 2024; [det separate vedtaksforslaget](https://www.regjeringen.no/no/dokumenter/prop.-27-s-20242025/id3075697/?ch=5) er også lest. |

Kontrollene beviser forslag på bestemte felt. De tidligere vedtakstreffene godkjente ikke denne talltypen. På 5440 må komponentnivå og posttotal fortsatt skilles; tabell 3.1 viser uttrykkelig posttotalens endring, mens Prop. 36s register nedenfor viser komponentendringene.

### Bred, eksplisitt avgrenset kontroll av alle N-kontoer

[Prop. 36 S, vedlegg 2](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=9) og [vedlegg 3](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=10) er et samtidig offentlig register over vedtatte og foreslåtte endringer, med beløp i kroner og egne proposisjons-/innstillingsfelt. Registeret er **ikke lest som om alle rader er forslag**. Proposisjonssesjon, innstillingssesjon og tomme referansefelt er beholdt ved utvalgene.

Første, brede prøve velger alle registerrader med proposisjonssesjon `/24-25`: 747 rader og 742 kontonøkler. Hele Excel-siden har 1 693 kapittel/post-nøkler, hvorav 737 har ikke-null N-postkandidat. Alle 1 871 N-celler er med som innganger. Unionen er 1 694. Den gir 509 eksakte treff, 232 ikke-null differanser, 952 Excel-nullkontoer uten offentlig rad og én offentlig konto uten Excel, **5999/90**. Tre differanser er minst én krone: 855/22, 3855/60 og 1560/71. De tre ligger i L, ikke N.

Etter at dette er synliggjort, prøves en **utledet, dokumentavgrenset kandidatregel**: samme registerutvalg, uten `p4/24-25` og `p34/24-25`. Dette er en dokumentert ny kontrollhypotese, ikke et etterhåndsfrosset akseptgrunnlag. Den gir:

| Hele nøkkelunionen | Antall |
| --- | ---: |
| Excel-kontoer / offentlige kontonøkler / union | 1 693 / 739 / 1 694 |
| Eksakte Decimal-kandidattreff | 509 |
| Ikke-null råpresisjonsdifferanser | 229 |
| Excel-null uten offentlig rad | 955 |
| Bare offentlig kilde, 5999/90 | 1 |
| Ikke-null Excel-konto uten offentlig kontrollfelt | 0 |

Dermed er **alle 737 ikke-null N-postkandidater** omfattet av den offentlige registerkontrollen. Den 738. felles kontoen er 2470/24, der de registrerte komponentendringene summerer til 0. Ingen nullkonto uten registerrad regnes som treff. De 229 differansene er alle bevart som differanser; maksimum er `0.00001000000` kroner på 2800/50 (`N1413=-131111.79999999999` mot offentlig −131 111 800 000). Ingen av dem blir 0 eller godkjent NOK ved en skjult toleranse.

Dette er en bred kontroll mot det offisielle samtidige forslagsregisteret, med originale forslagskontroller på 20/1, 2541/70 og 5440/24. Det er **ikke** en påstand om at hver departementsproposisjons opprinnelige vedtaksforslag er lest og avstemt enkeltvis. Rå underposter er kun summert som merkede matematikkontroller. Ingen generell hierarkiregel, N-normalisering eller faglig godkjenning er gitt.

## J/K/L: den prøvde periodedelingen og dens grenser

Offisielle periodereferanser er konkrete, men definerer ikke automatisk arbeidsbokfeltene:

- [R-3/2024, 12. februar, side 1–2](https://www.regjeringen.no/globalassets/upload/fin/vedlegg/okstyring/rundskriv/arlige/2024/r-3-2024.pdf) beskriver vårens RNB-runde og planlagt fremleggelse 14. mai. [Stortingets budsjettside for 2024](https://www.stortinget.no/no/Saker-og-publikasjoner/Statsbudsjettet/statsbudsjettet-2024/) opplyser at RNB ble vedtatt 21. juni 2024.
- [Prop. 36 S, kapittel 1, tabell 1.1 fotnote 1](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=1) omtaler første halvår som medregnet RNB. Dette støtter at J er et nivå etter vårbehandlingen og at K omfatter RNB-endringer; det er ikke bevis for en streng kalenderdato for hver enkelt Excel-celle.
- [R-7/2024, 5. september, side 1–2](https://www.regjeringen.no/globalassets/upload/fin/vedlegg/okstyring/rundskriv/arlige/2024/r-7-2024.pdf) skiller høstens innspill, fristen 22. november for departementenes proposisjoner og planlagt nysaldering 29. november. Det sier uttrykkelig at lønnskompensasjonen i 2024 skal inngå i omgrupperingsproposisjonene. Fristene er saksbehandlingsfrister, ikke dokumenterte datagrenseverdier for Excel-feltene.

### Full numerisk kontroll

| Prøve, uten avrunding | Fullt kontrollomfang og resultat |
| --- | --- |
| `J − H − K` | Alle 1 871 rådatarader: 1 654 eksakt 0, 217 ikke-null rester. Største absolutt rest er `0.0000000000061` råenheter, dvs. `0.0000061` NOK ved kandidatfaktoren. Maksimum gjelder rad 673, 732/72. Dermed er `J=H+K` **ikke en eksakt identitet i alle råceller**. |
| `K − I` | Alle 1 871 rådatarader: 1 800 eksakt 0, 71 ulike. Største absolutt forskjell er 840 råenheter. I og K er følgelig ikke utbyttbare. 151/70 har fortsatt `I70=-20`, men `K70=0` og dokument-D43=0; det opprinnelige RNB-forslaget og resultatet skal holdes atskilt. |
| K mot offentlige registerrader med innstillingssesjon `/23-24` | Hele unionen på 1 693 kontonøkler: 613 offentlige nøkler, 501 eksakte treff og 112 ikke-null råpresisjonsdifferanser (maks. `0.0000004` NOK). 1 080 Excel-nullkontoer har ingen offentlig rad og er ingen treff. Dette er en dokumentavgrenset vårkontroll, ikke alle bevilgningsvedtaks datoer. |
| L mot registerradene `p121/23-24`, `p4/24-25`, `p34/24-25` | Alle fire ikke-null L-celler og fire offentlige kontonøkler treffer eksakt. Resten er 1 689 Excel-nullkontoer uten rad i dette firekontoomfanget. |

På 2541/70 er J nivået **12 210 000 000**, K endringen **−608 000 000**, L det senere tillegget **400 000**, og N nysalderingsforslaget **680 000 000**. De tidligere, separat bevarte v2-lokatorene for J/K/L står i [pilotkontrollen](../pilot2024.md). Det nye Prop. 22-forslaget bruker 12 210 400 000 som førbeløp. Dermed kan N-deltaet sammenholdes med J+L i denne ene kontoen; N er ikke et nytt nivå som skal legges oppå et allerede endret etterbeløp.

### Ls fire ikke-null celler

| Celle / konto | NOK-kandidat | Konkret kildekobling og behandlingsledd |
| --- | ---: | --- |
| `L1360`, 2541/70 | 400 000 | Offentlig register: `p121/23-24`, `i25/24-25`; dokument-D939 har samme referanser. Den tidligere v2-kontrollen gir et eksplisitt vedtatt delta. Proposisjonssesjonen alene kan ikke plassere beløpet i K. |
| `L797`, 855/22 | 458 000 000 | [Prop. 4 S, vedtaksforslag](https://www.regjeringen.no/no/dokumenter/prop.-4-s-20242025/id3065066/?ch=4), økning fra 3 718 857 000 til 4 176 857 000. Datert 25. oktober. Dokument-D518 har `p4/24-25` og `i57/24-25`. |
| `L1562`, 3855/60 | 75 000 000 | Samme originalforslag, økning fra 2 571 496 000 til 2 646 496 000; dokument-D1114 har samme dokumentgruppe. |
| `L1198`, 1560/71 | 14 200 000 | [Prop. 34 S, vedtaksforslag](https://www.regjeringen.no/no/dokumenter/prop.-34-s-20242025/id3076616/?ch=5), økning fra 233 100 000 til 247 300 000. Datert **29. november**, samme dag som Prop. 36 S. Dokument-D789 har `p34/24-25` og `i91/24-25`. `M1198=N1198=0`. |

Det siste tilfellet avgrenser en vesentlig rest: L kan ikke uten videre oversettes til «alle vedtak etter RNB, men før nysaldering», og M er ikke alle lønnsrelaterte budsjettendringer. Ls fire kontroller kan vises med eksakt dokumentomfang; en universell datodeling er fortsatt ubekreftet. Prop. 36s register viser p34 som forslag uten innstillingsreferanse på den observerte kilderevisjonen; dokumentarkets senere i91-referanse gir ikke registerets forslagsfelt vedtaksstatus.

K/L har tre kontoer med ikke-null i begge, L/N én og K/N 363. Dette er **kontooverlapp**, ikke bevis for dobbeltføring av samme hendelse. I den prøvde dokumentdelingen er p4/p34 lagt i L og utelatt fra N-kandidaten. Man kan ikke samtidig legge hele registerets høstutvalg til N og L. J inneholder den prøvde K-komponenten og kan ikke summeres som en ekstra endringshendelse sammen med H og K.

### En ekstra kontroll viser hvorfor forslag og dokumentutfall må forbli adskilt

Alle rådataenes kapittel/post-summer av `(K+L+N)×1 000 000` er sammenlignet med dokumentarkets beløpssummer **kun for rå Upost=0**. Dette er en intern diagnostikk, ingen uavhengig offisiell avstemming. Unionen har 1 693 nøkler: 685 eksakte, 302 ikke-null rester, 705 Excel-nullkontoer uten dokumentrad og én ikke-null konto uten dokument-posttotal. Den siste er 5440/24, som har dokumentkomponenter; en manglende posttotal skal ikke opprettes.

Seks rester er minst én krone: 118/70 (−5 mill.), 1420/32 (−270 mill.), 150/70 (−215 mill.), 315/78 (−10 mill.), 5800/50 (`−600000000.0000005000000` kr) og 732/70 (−100 mill.). Fortegnet er råaggregat minus dokumentaggregat. Alle øvrige 296 ikke-null rester er også bevart; énkronegrensen er bare en beskrivende inndeling. Disse seks er **ikke erklært feil i forslagskilden**. De understreker at ulike behandlingsledd ikke skal tvinges like. Den etterfølgende integrasjonskontrollen nedenfor har kildebelagt alle seks som forskjeller mellom forslag og vedtak. Rårestene beholdes fortsatt.

## Tillegg ved integrasjon: alle seks materialstratum-rester er kildebelagt

Kontrollert 22. oktober 2026 i [den begrensede restavledningen](stage-residuals.json). De seks restene følger ulike behandlingsledd. De fem utgiftstilleggene summerer til 600 mill. kroner; samme økning er innarbeidet i vedtaket om overføring fra Statens pensjonsfond utland.

| Konto | Forslagsgrunnlag i N / samtidige register | Komité-/vedtaksbeløp | Forklaring |
| --- | ---: | ---: | --- |
| 118/70 | Ingen rad i det avgrensede høstforslagsregisteret | +5 mill. kroner | Innst. 82 S, merknad og tilråding; vedtak 40034211. Fraværet blir ikke et observert forslagsbeløp 0. |
| 150/70 | Ingen rad i samme register | +215 mill. kroner | Innst. 82 S: 25 + 100 + 90 mill. kroner; samme vedtak. |
| 1420/32 | Ingen rad i samme register | +270 mill. kroner | Innst. 95 S, merknad om skogvern og tilråding; vedtak 40034220. |
| 315/78 | +119 mill. kroner i original Prop. 25 S, forslag I | +129 mill. kroner | Innst. 85 S foreslår 10 mill. kroner utover regjeringens forslag; vedtak 40034045. |
| 732/70 | +405 mill. kroner i original Prop. 23 S, forslag I | +505 mill. kroner | Innst. 94 S legger til 100 mill. kroner til Helse Nord; vedtak 40034229. |
| 5800/50 | +9 366 471 000 kroner i original Prop. 36 S, forslag I | +9 966 471 000 kroner | Innst. 90 S knytter økningen til de fire fagkomiteenes forslag og omtaler samlet 600 mill. kroner; vedtak 40034287. |

Alle seks vedtaksfelt er gjenfunnet direkte i det hashfestede sesjonssvaret for 2024–2025. Originale forslagsfelt, tilrådingstabeller og merknader har egne URL-er, responsbythasher og XPath-er i JSON-en. For 5800/50 blir differansen etter at den kildebelagte endringen på 600 mill. kroner holdes separat, fortsatt eksakt `−0.0000005` kroner fra rå N-leksem. Ingen toleranse fjerner denne resten.

Dette avklarer den konkrete økonomiske forskjellen per konto. Det gir ikke normalisering, dokumentasjon av produsentens alle kolonneregler, fullstendig proposisjonsdekning eller godkjenning av en additiv årsmodell. De tre formelle kjedekonfliktene gjelder andre forhold og består.

## Bidrag til alle ni matriserader

Statusene nedenfor er kontrollstatus i denne undersøkelsen. De tildeler ingen gjeldende B5-godkjenning eller normalisert NOK.

| Kolonne | Verifisert kildefunn / tillatt avgrenset kontrollbruk | Kandidatregel og gjenværende beslutning |
| --- | --- | --- |
| G | Tidligere ekte Gul bok-forslag på 1/1 er bevart i `pilot2024/proposal-refs.json`. | Nivå/regjeringsforslag; intet nytt bredt kontrollomfang her. Råpresisjon/hierarki står separat. |
| H | Hele saldert-unionen og de 726 presisjonssporene behandles i P13-P2s eget spor. | Ingen ny H-regel eller godkjenning i denne rapporten. |
| I | Tidligere originalt RNB-forslag på 151/70, −20 mill., bekrefter forslagsfeltet og forskjellen fra K. | RNB-forslag/endring; ingen likestilling med vedtak eller generell avrunding. |
| J | Nivå etter RNB på 2541/70; full kontroll av `J−H−K` viser 217 rårester. | Aggregert nivå for vårbehandlingen er en kildeunderbygd kandidat. Ingen ekstra delta eller eksakt universell råidentitet. |
| K | Vårregister med 613 nøkler; eksakte og ikke-eksakte råspor er skilt. | Aggregat med RNB medregnet. Dokumentutvalg og tillatt bruk må vedtas; dato alene er utilstrekkelig. |
| L | Alle fire ikke-null felt har konkrete offentlige dokumentankre; tre originale forslagsfelt er kontrollert nå og ett tidligere vedtak er bevart. | Dokumentavgrenset øvrig gruppe etter RNB. Ingen universell grense før 29. november eller ensartet talltype fra kolonnenavnet. |
| M | Hele M er rå 0. Faktisk offentlig lønnsfordeling finnes, og på 20/1 ligger beløpet i N. | Kun rå nullbevaring inntil produsent-/eieravklaring. Ingen påstand om null lønn eller automatisk innfylling. |
| N | Tre originale forslagsankre og registerkontroll av alle 737 ikke-null postkandidater; 229 ikke-null presisjonsspor, 5999/90 mangler i Excel. | Avgrenset forslags-/endringskandidat, med lønn inkludert på dokumentert kontrollkonto. Ikke vedtak. Hele originalproposisjonsunionen er ikke lest enkeltvis; normalisering/hierarki/godkjent bruk krever egne valg. |
| Dokument-D | Referansene på de berørte kontrollkontoene er bevart som relasjoner; tidligere dokumentunion består. | Faktor 1 og vedtaks-/komponentroller hører til det separate dokumentsporet. Ikke erstatt forslagsfelt med D ved avvik. |

## Kilderevisjon, reproduksjon og videre ansvar

Prop. 36-HTML-en er merket foreløpig utgave. Det tilknyttede [rettebrevet av 10. desember 2024](https://www.regjeringen.no/contentassets/3bd150ac17194379aaa8c0a73e0a765a/no/sved/rettebrev.pdf) er lastet ned og begge sider er visuelt lest. Det retter henvisningen for gasskjøpet fra Prop. 17 til **Prop. 27 S**, samt avgiftsomtalen for 5547/70–71. Brevet endrer ikke de oppgitte beløpsfeltene i disse kontrollene. Rettebrevet og det observerte HTML-innholdet har egne hasher; ingen korrigert kilderevisjon er diktet inn.

De nye offentlige foreldrene er hentet 22. oktober 2026. Eksakt URL, SHA-256 og størrelse står per kilde i JSON-en, herunder Prop. 36s HTML-kapitler 1/5/7/9/10/11, faktiske forslag i Prop. 22/27/34/4, R-3/R-7 og rettebrevet. Hashene gjelder hele de faktisk mottatte responsbytene, inklusive nettsidens rammeinnhold, ikke en redigert tekstversjon. XPath-ene er fra den tilhørende hashfestede HTML-en og er 1-baserte.

Reproduksjonsgrunnlaget er tydelig avgrenset:

1. Kontroller originalhash/byteantall og les alle numeriske råfelt direkte fra OOXML som Decimal; tell 0, positivt, negativt og eventuelt fravær hver for seg.
2. Beregn `J−H−K` og `K−I` per alle 1 871 originalrader. Ingen rest fjernes. Bevar konto, kildeceller og eksakte inngangsstrenger.
3. Les kontoradene i Prop. 36 vedlegg 2/3, med kapittel fra kapittelettiketten og post fra den konkrete raden. Summér bare de eksplisitt utvalgte kildefeltene; behold hver enkelt kildepeker. Totallinjer uten post blir ikke nye kontoer.
4. Gjør de fire uttrykkelige registerutvalgene i JSON-en; rapporter hele unionen, inkludert null uten rad og 5999/90. Kontroller de seks begrensede originale forslagsfeltene med kildehash/XPath.
5. Les alle kontorader i lønnsvedlegget, og hold positive tildelinger og negativ reserve adskilt. Sammenlign ikke bare fortegnssummen 0 med M.

De lokale skriptene `measure.py`, `compare_sources.py`, `final_counts.py` og `doc_identities.py` har hasher i JSON-en. Fullstendige restlister er lokale; en senere implementert kontroll må få sitt eget forhåndsfrosne omfang og kontrollidentitet. Det er ikke kjørt produksjonsimport, endret pilotpakke, rettet råbeløp eller skrevet kode i dette undersøkelsessporet.

Eieren må avklare tillatt faglig bruk for de konkrete forslagskontrollene, 2024s M-nullsemantikk, kildebegrunnet presisjonsbehandling og underpostkoblinger. De seks rå-/dokumentrestene er kontrollert nedenfor. Øvrige originale departementsforslag er ikke avstemt enkeltvis. Ingen offentlig kilde som definerer de interne f150/f176/f177/f179-feltene direkte, er funnet i de undersøkte proposisjonene, de to rundskrivene eller Stortingets budsjettoversikt. Det er et avgrenset negativt søkefunn, ingen påstand om at slik dokumentasjon ikke finnes.

Nye offisielle tall skal fortsatt leses inn uavhengig av den historiske Excel-filen, organisasjonsregister og startsaldo. #13 og #10 forblir åpne; dette sporet gir ingen driftsaksept eller komplett bevilgningskjede.
