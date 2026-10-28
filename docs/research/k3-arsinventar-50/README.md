# K3 / #50 – kildeinventar for 1429/1 og /22, budsjettåret 2024

Undersøkt 28. oktober 2026 fra T4-merge `37c6ad4572c030a6b3309201d836bb0c0c51f9c6`.
Dette er en kunnskapsleveranse under [#37](https://github.com/depmartin/budsjetthistorikk/issues/37),
ikke produktkode eller en godkjent årsbalanse. [M21-resultatet](m21.md) er **presist
avgrenset restusikkerhet**. Positiv helårsdekning er fortsatt åpen.

## Resultat som endrer neste byggesnitt

De tre kjente monetære vedtakene er ikke et komplett dokumentregister. I tillegg
finnes **vedtak 346 / 40032933, 19. desember 2023**: merinntektsfullmakt for
**1429/1 i 2024**, mot 4429/2 og /9. Det skal inngå som eget dokumentert
fullmaktsledd, uten ny tallfestet bevilgningsendring. Dette er type `BUDSJETT`;
RNB 857 og nysaldering 210 er `ANNET`. Begge typer må undersøkes.
[Vedtaksbevis](decision-evidence.json), [dekningsjournal](coverage-journal.json).

Opprinnelig behandling inneholder dessuten autentiske parallelle forslag:
Innst. 14 S viser for 1429/1 nivå **153 620 tusen kroner fra Høyre** og
**156 243 tusen kroner fra Fremskrittspartiet**, mot regjeringens/flertallets
161 243 tusen. Parentesene −7 623 og −5 000 er avvik fra forslagsgrunnlaget,
ikke vedtatte årsdeltaer. Tilrådingen og vedtak 341 er 161 243 000 kroner.
Ingen av alternativene er dermed det vedtatte /1-nivået. Separat formell
votering av hvert opprinnelig primærbudsjett er ikke ferdig kartlagt her;
ikke merk disse med et oppfunnet forslagsnummer eller stemmetall.
[Innst. 14 S §4.34.1, §4.37 og §7](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2023-2024/inns-202324-014s/?all=true),
[eksakte tabellokatorer og råceller](table-locators.json).

Regjeringens [Prop. 36 S vedlegg 3](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=10)
er en nyttig **uavhengig kildeliste**, ikke et nytt vedtak: under 1429 viser den
/1 +5 796 000 fra `p16/24-25` og −1 000 000 fra `p104/23-24`/`i447/23-24`,
og /22 −3 000 000 fra `p16/24-25`. Vedlegg 6 viser saldert 161 243/32 185,
periodens foreslåtte endringer +4 796/−3 000 og status 166 039/29 185,
alle i tusen kroner. Kolonnen for endringer i selve Prop. 36 er «−» for disse
postene. Dette støtter det kjente utvalget på proposisjonens tidspunkt;
en tabell over **vedtatt eller foreslått** er ingen uttømmende vedtaksgodkjenning.
[Vedlegg 6](https://www.regjeringen.no/no/dokumenter/prop.-36-s-20242025/id3076783/?ch=13),
[råoriginaler/transport/hash](source-manifest.json).

## Etterprøvbart kildeunivers og faktisk undersøkelse

Universet er et navngitt, frosset kildeutvalg. Det er ikke definert som «alle
dokumenter som gir treff på 1429».

| Delunivers | Bevaring og faktisk kontroll | Bevisgrense |
| --- | --- | --- |
| U1: alle vedtaksobjekter i API-sesjonene 2023–2024 og 2024–2025 | 923 + 1 260 = **2 183** komplette objekter, alle typer. To tidligere responser gjenbrukes; to nye komplette svar 28.10 er også bevart. Alle objekt-ID-er og kanoniserte objekter er uendret mellom hentingene. Hvert objekts ID, sak, dato, tittel, type og søkeordskontroll finnes i [vedtaksregisteret](decision-register.json). | [Versjonskontrollen](source-comparison.json) gjelder disse fire konkrete svarene. Senere rettelser og senere sesjoner er utenfor snapshotet. |
| U2: komplette saksindekser for samme sesjoner, hentet 28.10.2026 | **637 + 727 = 1 364 indeksposter**. Titler/henvisninger er undersøkt med konto-/institusjons-/fagord og statsbudsjett/RNB 2024. **67 kandidatposter / 66 unike saker** er bevart i [sakskandidatlisten](case-candidates.json). | Et indekstreff er ikke postkobling. 60 kandidatposter / 59 unike saker står åpne etter fulltekstgrensen nedenfor. |
| U3: opprinnelig budsjett | Prop. 1 S KLD, kapittel 3 og forslag kapittel 6; hele Innst. 14 S; Innst. 2 S kapittel 3; sak 95776; komplett plenumsreferat 19.12.2023; tillegg 1 og 2, se journalen. | Regjeringen-HTML med `ch=` er komplette svar for kapitler, ikke nødvendigvis hele dokumentet. Gul bok/Blå bok og alle partiers originalpublikasjoner er ikke ny fullstrukturert her. |
| U4: RNB | Prop. 104 forslag kapittel 5; tidligere og ny komplett Innst. 447; sak 98918/98919/99234; Prop. 106 kapittel 1–4; hele saks-API-et for voteringer og konkret kobling til 857. | Ett nytt 447-forsøk og to referatforsøk ble avbrutt og beholdes ufullstendige. Senere komplett 447 har samme kontrollerte normaliserte hovedtekst som den gamle. De sju navngitte RNB-pakkene har nå sikre voteringsutfall; øvrige løse/endrede forslag er ikke uttømmende lukket. |
| U5: nysaldering og øvrige saker | Prop. 16 → Innst. 81 → 210/211 gjenbrukes fra O1/T1/T3. Søstergren 95 er separat. Prop. 36 vedlegg 3 og 6 kontrolleres mot kjente poster. Alle U1-typer og U2-dokumentgrupper er med i screening. | Felles Prop./sak gir ikke arvet postkobling. Øvrige åpne saker, forslag i salen og indirekte kontoomfang er restusikkerhet. |

Screeningen i U1 brukte `1429`, `Riksantikvar`, `kulturminne` og `kulturmiljø`,
uten vedtakstypefilter og uten krav om kjent proposisjon. Det ga **25 objekter**.
Alle 25 har nå en konkret inkluderings-/ekskluderingsgrunn og kildepeker i
[journalen](coverage-journal.json); kapittelblokk, uttrykkelig årsinnledning
og fullmaktstekst kan kontrolleres i [vedtaksbevisene](decision-evidence.json).
De øvrige **2 158 objektene** er markert *ingen ordbokstreff; semantisk
eksklusjon ikke utført*. De er ikke borte fra registeret, og utgjør et konkret
restomfang. Dette er en bredere undersøkelse enn 1429-søk alene, men heller
ikke fire søkeord kan bevise fravær av indirekte endringer.

U1 fordeler seg på ANMOD 268/485, ANNET 426/517, BUDSJETT 225/257,
GRUNNLOV 1/0 og RO 3/1. Kandidatene har henholdsvis 12 og 13 objekter.
[Omberegnbare summer](universe-summary.json).

Tillegg 1, tillegg 2 og Prop. 106 er bevart som henholdsvis tre, seks og fire
publiserte HTML-kapitler/vedlegg gjennom nye svar og uttrykkelig refererte
tidligere originaler. Hvert svar beholder sin egen observasjonstid og hash;
kapitlene presenteres ikke som én samtidig hentet helfil.

## Dokument- og postbevis per runde

| Runde/ledd | Kontrollert kildebelegg | Korrekt betydning og gjenstående grense |
| --- | --- | --- |
| Originalforslag, datert 2023 | Prop. 1 S KLD kapittel 3 → 12.30 → kap. 1429; kapittel 6 forslagstabell `tbody/tr[64–67]` | /01 161 243 og /22 32 185 i tusentabellen; forslagstabellen 161 243 000 / 32 185 000 kroner. Egne rånavn beholdes. Forslag, ikke vedtak. |
| Innst. 14 S (2023–2024) | §4.34.1, §4.34.3, §4.37 og tilråding §7, rammeområde 3 I og VI | Flertallet Ap/Sp/SV støtter regjeringen. Tabellen med H/FrP-alternativene har egne avsendere. /22 mangler blant akkurat §4.37-tabellens utvalgte avviksrader; det er ikke generelt fravær av alternativer. Tilråding I har nivåene; VI har merinntektsfullmakten. |
| Plenum 19.12.2023, sak 5 | Hele referatet, voteringsdel sak 5; avslutning 21.44.08 | Komiteens innstilling vedtatt 54–45. Dette knytter tilrådingens bevilgninger og VI til behandlingen. Alternativenes separate primærbehandling er fortsatt et eget hull. |
| Endelig 341 og 346 | 40032928 og 40032933 i komplett 66aa-forelder | 341: to opprinnelige 2024-nivåer. 346: fullmakt /1, ingen beløpsobservasjon av en ny årsbevilgning. |
| Tillegg 1 til Prop. 1 | Hele endringskapittel 1 og forslag kapittel 3 | Fullmakt 1481/25 til skogkreditter/utslippsenheter; konkret annet kontoomfang gir eksklusjon for /1,/22. |
| Tillegg 2 til Prop. 1 | Ny innledning/tilråding/forslag kapittel 1/3/4; tidligere kapittel 2 og vedlegg 2 via referanse | Forslagets endringstabeller og fullmakter gjelder KDD/DFD-omorganisering og angitte NFD/ED-/salderingsendringer. Ingen endring av valgte 1429-poster i det undersøkte endringsforslaget. Ingen generell årskontinuitet utledes. |
| RNB Prop. 104 | Forslag kapittel 5, 1429-blokken til neste kapittel | /1 −1 000 000, fra 161 243 000 til 160 243 000; /60 og /70 er andre poster. Ingen /22 i akkurat denne blokken. |
| RNB Innst. 447 | Komplett gammel HTML, tilråding kapittel 7, tabell i `div[81]`, 1429 `tbody/tr[821–829]` | /1 −1 mill. med samme før/etter; /60,+5 mill.; /70,+2 mill.; /71,−2 mill. Neste kapittel 1432 avgrenser blokken. Ingen /22-beløpsrad her. |
| RNB parallelle forslag | Komplett 447 kapittel 6: H forslag 1, FrP 2, SV 21, Rødt 22, V 29, MDG 49, KrF 54; full saks-API for voteringer | Alle sju pakker har /1 −1 mill. med samme før/etter, og alle sju ble forkastet. Sju pakker gir ingen nye vedtatte hendelser. Avsenderattributter, blokker og utfall er bevart i [voteringsbevisene](voting-evidence.json). Ingen /22 i disse avgrensede 1429-blokkene. |
| Tillegg Prop. 106 | Kapittel 2 og hele forslag kapittel 4 | Omtalte kapitler 288, 572, 845, 1543, 5579; forslagstabellens monetære kapitler 288, 845, 1543, 5579. Konkret annet kontoomfang, ikke valgt 1429-endring. Kildens «mot tidligere foreslått» er ikke delta mot vedtatt saldo. |
| RNB vedtak 857 | 40033719, hele 66aa-forelder, eksisterende T3-bevis | /1 −1 mill.; ingen /22 i kontrollert blokk. Saken står under en melding og har fellesinnstilling med Prop. 104/106. Direkte dokumentgruppe er ikke bevilgningskriterium. |
| Nysaldering Prop. 16/81/210 | Eksisterende O1-originaler/transport; uendrede T1/T3-identiteter | /1 +5 796 000 fra 160 243 000 til 166 039 000; /22 −3 000 000 fra 32 185 000 til 29 185 000. Fem kjente monetære posthendelser over tre runder består. |
| Prop. 36 | Vedlegg 3 `tbody/tr[1008–1014]`; vedlegg 6 `tbody/tr[789–794]` | Kildeliste/foreslått årsstatus i egne roller. Den er ikke en ekstra monetær hendelse, og tom vedtakskolonne er ikke postvis vedtakelsesbevis. |

Alle XPaths gjelder den hashbundne representasjonen. `table[1]/tr[n]` i eldre
pilotrapporter flater ut hode- og kroppsrader; `tbody/tr[n]` i ny DOM-ledger
utelater hoderaden. Derfor er eksempelvis vedtak 857s gamle tr822 det samme
kapittelankeret som DOM `tbody/tr[821]`. Dette er lokatorregler, ingen endret
original eller ny beløpstolkning.

### Navngitte voteringskoblinger

[API-originalene](source-manifest.json) og [eksakte XML-/HTML-lokatorer](voting-evidence.json)
binder sak 95776/votering 22032 til forslag 40073884 → vedtak 341 og
forslag 40073889 → vedtak 346. Voteringen var 54–45. Den beviser de vedtatte
tilrådingsleddene, ikke en separat avstemning av H/FrPs opprinnelige nivåer.

| RNB-forslag | Votering | For–mot | Utfall |
| --- | --- | --- | --- |
| KrF 54 | 23425 | 2–99 | Forkastet |
| MDG 49 | 23426 | 1–99 | Forkastet |
| V 29 | 23427 | 4–97 | Forkastet |
| R 22 | 23428 | 4–96 | Forkastet |
| SV 21 | 23429 | 8–93 | Forkastet |
| FrP 2 | 23430 | 13–87 | Forkastet |
| H 1 | 23431 | 22–79 | Forkastet |
| Tilråding A/B | 23457 | 55–46 | Vedtatt; vedtak 857 er A.I |

H- og FrP-pakkene har egne bevarte forslags-API-svar, henholdsvis
40076318 og 40076319. Tilrådingens forslag 40076251 er bevart separat.
De fem andre pakkenes tekster er bevart i komplett 447; egen forslags-API
er ikke hentet for dem. Nysalderingens votering 23873 er enstemmig og
binder 210/211 til de separate romertallene I/II. Alle disse API-ene er
andre kildeobservasjoner enn de endelige vedtakene og skaper ingen nye
vedtatte beløpshendelser.

## Begrunnede ekskluderinger og åpne kandidater

Vedtak 334 og 408 i sesjon 2023–2024 har faktiske 1429-beløp, men sier uttrykkelig
**statsbudsjettet 2023**. De er konkrete årseksklusjoner. 201/401/427 i neste
sesjon gjelder uttrykkelig **2025**, selv om datoene er i 2024. 347 gjelder
andre 1429-poster; 211 er bevart som /60-kontekst. Komitéfordeling, anmodning om
kulturminneloven, Svalbard-kapitler, 5582/70 og 1352/76 blir heller ikke
1429/1- eller /22-endringer. Journalen gir egen grunn per kandidat, og
originalens øvrige innhold beholdes.

Saker uten kjent proposisjon er **ikke forhåndsekskludert**. Alle U1-objekter
inngår uavhengig av saksgruppe; U2 har også melding/ikke_spesifisert.
RNB-sak 98919 er en konkret kontroll av at en melding kan være sakskontekst
for monetære vedtak. Denne undersøkelsen har ikke funnet en ny sikkert
selvstendig /1-/22-bevilgning uten proposisjon, og har heller ikke bevist
at ingen slik finnes. [Tidligere autentiske eksempler på andre kontoer](../../kildefunn.md)
er metodegrunn, ikke nye 2024-hendelser på valgt konto.

De **60 åpne indekskandidatpostene** er navngitt med ID, tittel, henvisning,
gruppe, status, kildeordinal og begrunnelse. De omfatter andre opprinnelige
komitégrener, tillegg, lønns-/salderingssaker og andre 2024-saker.
De er ikke semantisk ekskludert bare fordi tittelen gjelder et annet
departement. Samme kilde kan forgrenes; en senere gjennomgang må kontrollere
det faktiske kontoomfanget. Kildenes kryssreferanser er bevart i
[saksrelasjonene](case-relations.json); uundersøkte referater/partipublikasjoner
står som restusikkerhet fremfor å bli arvet som postkoblinger.

## Statusgrense og neste arbeid

Rådekning, postkobling, strukturering og faglig godkjenning er separate.
Komplett rå 447 betyr ikke at alle dens tekster er strukturerte. Forslagets
nivå eller en alternativ pakke gir ingen ny vedtatt virkning. Vedtak 346
har sikker /1-/2024-kobling, men ingen tallfestet monetær virkning. Registeret
har ingen B5-godkjenning eller faglig årsbalanse. Produktets T3/T4-observasjoner,
gamle ID-er, kilder, schema 5 og standardvalg er uendret.

Et lite senere byggesnitt bør først vise dette **delvise perioderegisteret**
med den nye fullmakten og alle navngitte hull i begge innganger og faktisk
gjenleste JSON-/Excel-filer. Det skal ikke ha en positiv helårsstatus.
[Snittforslag og ny startprompt](neste-snitt.md), [overlevering](OVERLEVERING.md),
[reproduksjon og manifest](reproduksjon.md). Ingen T5/T6, kontinuitet/K2,
faglig saldo eller drift starter automatisk. #10/#32/#37 står åpne.
