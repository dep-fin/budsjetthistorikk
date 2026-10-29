# Uavhengig kilde-, felt- og Excel-kontroll av T5/#62

Kilde-/feltport og avgrenset visuell Excel-port: **bestått**. Ingen funn med
prioritet P1, P2 eller P3 i det undersøkte snittet. Dette er en uavhengig
kontroll, ikke byggerens egen attest eller en full Standards/Spec-/sikkerhetsaudit.

Fast kandidat: `d46589cb9e99338e44fc805ee9882006ba657fd0`.
Kanonisk kandidat-tre: `df0eed6d6e8a0b2a07962e641ae05d1194a3304d`.
Fast base: `2f4ee30c9d8074076fc8042e208c4a4b6345db6b`.
Checkout: `work/t5-prop16`. Kontrollen endret ingen produktfiler, basefiler,
manifester, Git-indeks eller GitHub-tilstand. Nye egne kontrollartefakter
ligger bare her; midlertidige eksport-/PDF-prøver ligger i `.local/source-check`.

Issue #62 og alle kommentarer ble lest via GitHub-koblingen (ingen kommentarer
ved kontrollen). AGENTS, arbeidsflyt, issue-tracker, ansvarsdeling,
T5-/T1-kontraktene, ADR 0011, målbildet, forgreningsundersøkelsen, akseptmatrisen,
kilde-/kompatibilitetsbevis, reproduksjon, råkildekontroller, TDD-journal og
Excel-QA inngikk. Regneark- og PDF-skillene ble brukt til faktisk fil-/render-QA.
Ingen nye primærkilder ble hentet.

## Egne kilde- og feltprøver

[independent_check.py](independent_check.py) laget sin egen fasit ved å traversere
de to første tabellene i bevart Prop.-kapittel-4-HTML. Kapittel-/post, uttrykkelig
økes/reduseres, før-/ettertekst og faktiske celle-XPath-er ble lest før produktets
API ble brukt. Dette bruker ikke produktparseren eller byggerens kontrollarray
som fasit. Alle 37 triplers regnestykker før + delta = etter stemte.
[independent-control.json](independent-control.json) bevarer alle **111** egne
kontrollrader med originalcelle, XPath, forventet kroneverdi og produkt-ID.

- **37 trioer / 111 felt / 15 tabellkapitler**, med **27 utgift / 10 inntekt**.
  Prop.-HTML er råhash `ff1c5368…eca5e`; full PDF er `67771605…aa5db`.
  De eksakte hashene står i kontrollfilen. Alle felt hadde riktig beløp,
  betydning, 2024, NOK, multiplikator 1 og binding til originalens hash/lokator.
- PDF side **7–11** ble rendret fra den faktiske bevarte PDF-en og visuelt lest:
  alle tabellrader på side 7–9 og fullmaktene på side 10–11. Tabellen, nullen
  og de fem tallfestede fullmaktsrammene støtter HTML-kontrollen.
- **45 unike kontoangivelser** samsvarer eksakt med 37 tabellkontoer og de
  åtte øvrige angivelsene i kontrakten. 1533/45 er kontrollert i faktisk
  kapittel-2-HTML (`/html/body/main/div/div[3]/div[3]/div[4]/p` i den bevarte
  representasjonen; kontrollfilen har den beregnede eksakte lokatoren).
  1474/50 og /70 er kontekstreferanser i 1474/1-radens «kan nyttes under
  postene 50 og 70», ikke nye tabellgrupper.
- II–VI har **ni atomiske punkter**. Hvert punkts XPath, hele seksjonsteksten
  og HTML er avstemt mot originalen; 8 / 601,0 / 266,3 / 16,3 / 25 mill.
  kroner er i tillegg lest direkte fra punktets råtekst. IV har ett objekt,
  tre kontoer og **én 16 300 000-kroners ramme**. Ingen ny observasjon er
  vedtak eller fullmaktsramme forkledd som bevilgningsdelta.
- Alle **åtte grener** er kontrollert mot faktiske XML-vedtaksobjekters saks-ID
  og lokalt romertallsattributt. Tabellens 1429-grupper går til 100927; de
  øvrige 35 til 100889. V.1–2 går til 95 V / 40034224 (363); V.3 til 81 II /
  40034049 (211). 1533/45 finnes ikke i aktive greners kontoomfang og fikk
  ikke Innst. 95 i sitt aktive dokumentutvalg.
- Begge hele gamle XML-foreldre er dekomprimert og hashet: **9cfeaef5…** og
  **c5f3b900…**, hver 7 479 943 byte, med ulike råhasher. 210 og 211 er
  dessuten rekonstruert byteidentisk fra riktig forelders prefix, metadataført
  objektintervall og suffix. Bevaringskontrollen følger faktisk rårepresentasjon.
- Begge beriktigede 95-HTML-svar er lest og har ulike råhasher, men samme
  normaliserte m1–m4-tekst. Gjenbruksmanifestets datopresisjon og ukjente
  rettelseshistorikk består. Innst. 95-PDF side **1, 4 og 5** ble rendret og
  visuelt lest: «Beriktiget», unntaket for 1429, fullmaktene og V.1–2 fremgår.
  Ingen 95-beløp er lagt til T5s beløpsmodell.

## Faktiske filer, API, CLI og kompatibilitet

Egen kjøring skrev, lukket og leste **16 JSON/XLSX-par**, med **16 uavhengig
beregnede utvalgsfasiter**: utgift, inntekt/null, tekstkonto, 1533-kontekst,
1429/1, /22 og begge, tomt, 2025, manglende år, union av kapittel og konkrete
par, hele Prop., begge navigasjonsretninger og begge returvalg. Returparene
var eksakt like sine opprinnelige rapporter. Hver faktisk leser ga identisk
rapport og samme gamle typede T1-kapsel.

Resultatene er 105 nye forslagfelt, union **123/6/2**, Prop. **111/0/0**,
1429/1 og /22 hver **9/3/1**, begge **18/6/2**; øvrige tabellkontoer gir
**3/0/0**, mens tekst, tomt og år uten treff gir **0/0/0**. 4400/2 har
**518 000 / −518 000 / 0**; den siste er heltallsnull uten nullgrunn.

Hele den gamle basisen ble sammenlignet både typet og som hele JSON-objektet
mot den autentiske `tests/fixtures/t2/authentic-t1.json.gz`, lest med uendret
gammel leser. Dette omfatter samtlige gamle objekter, ID-er, step_id, runder,
kilde-/revisjonsbindinger, tolkninger og kontrollstatus. Gammel Prop.-post
beholder `structured_coverage=delvis_1429`; gjeldende status ligger i eget
identifisert overlay med den gamle dokument-ID-en som referanse.

Som en egen kontroll av den faktiske XLSX-presentasjonen ble alle **111
numeriske Forløp-celler** i egen dokumenteksport lest med openpyxl og avstemt
mot den selvstendige HTML-fasiten, uten produktleseren som cellefasit. Alle
ark, rader og kolonner var synlige, tallene var tallceller, og historiske og
gjeldende statusoverskrifter var riktige.

To ytterligere offentlige CLI-prøver brukte `--t1` og `--frosset`. Sistnevnte
brukte en kilde-rot som ikke eksisterer og eksporterte originaler. Begge skrev
faktiske JSON/XLSX-par som deretter ble gjenlest like; de ga henholdsvis 3 og
111 felt. [cli-control.json](cli-control.json) og CLI-loggene fører resultatet.
Dermed er det **18 egne faktisk skrevne/lukkede/gjenleste par** totalt.

Alle **25** originalrepresentasjoner ble eksportert fra kapselen og avstemt
med eksakt byteantall og SHA-256 mot de innebygde kildebytene. Byggerens 14
faktiske par i `.local/delivery-final` er i tillegg hashet; samtlige 28 filer
stemmer med `source-control.json`. Dette siste er hashkontroll av byggerparene,
ikke en påstand om 14 ytterligere uavhengig gjenleste par.

Egen omkjøring av de relevante eksisterende prøvene ga **27 bestått, 8
deselektert på 120,74 sekunder**; se [pytest-selected.log](pytest-selected.log).
Den omfatter alle ti konsistent rehashede semantiske angrep på begge lesere,
de ni container-/presentasjonsangrepene, typed innlesning uten analyseimport,
streng offline/no-clobber/CLI, presis års-/kontounion og alle fire reelle
tilleggstilstander ved ordinær 40034229-registrering. Semantikkangrepene
passerer `inspect_excel` før forventet semantisk avvisning. De fire
registreringsprøvene gir hver 222 observasjoner / 74 hendelser fra riktig
autentisk hash. Dette er egen utføring av byggerens tester; kildefasiten og
de 16 API-parene ovenfor er separat utformet kontroll.

Byggerens sju TDD-snitt og 35-testers logg er lest som historisk byggebevis.
Ingen påstand om uavhengig gjenskaping av de historiske røde tilstandene følger.

## Visuell kontroll av faktiske XLSX-filer

Alle åtte bevarte kandidatbilder i `../../visual/` ble åpnet og inspisert.
I tillegg importerte [render_actual.mjs](render_actual.mjs) egne faktiske
produkteksporter med bundlet `@oai/artifact-tool`, rendret **13 områder** og
lagret [egen renderjournal](render-control.json), med SHA-256 for innfil og
PNG. Alle 13 resulterende bilder ble åpnet og visuelt inspisert. Dette bygger
ikke en alternativ regnearkmodell.

Visuelt lest: utgiftstrioen, synlig inntektsnull, tekstkontoens og det tomme
utvalgets 0/0/0 mot globalt 123/6/2, IVs ene rammerad med tre kontoer, V.1–2
mot V.3, `ikke_strukturert_T6`, valgt/globalt fullmaktsskille, historisk T1-
mot gjeldende T5-status og dekningsforbeholdet. Hovedtall og nødvendige
overskrifter/statusfelt er leselige uten #### eller bortklipte beløp.

Lange ID-er, råtekst, bindingsarrayer og metadata er synlige celleforhåndsvisninger
med dokumentert klipping. Hele verdiene ligger i cellene/ordnede tekststykker
og består den tapsfrie gjenlesingen/originalgjenfinningen. Dette er akseptert
previewgrense, ikke fulltekstlayoutaksept. Rendringens engelske tusenskille er
ikke en prøve av norsk Excel-lokalisering. **Native Excel, interaktive klikk,
utskrift og uinspiserte celleområder er ikke visuelt attestert.**

## Byte-, Git- og reproduksjonsgrense

Alle **35** filer i leveransemanifestet er avstemt mot kandidatens faktiske
Git-blob med byteantall, SHA-256 og Git-blob-SHA-1, og mot checkout-byte med
bare manifestets uttrykkelig angitte normalisering. For kontrollerte
`UTF-8/LF`-filer er faktiske Git-filterstrømmer med `core.autocrlf=true` og
`false` prøvd og normalisert etter denne regelen. Alle stemmer. De gamle
råkildenes blobhasher er kontrollert separat uten normalisering.

Dermed gir fraværet av en ny lokal `.gitattributes`-regel ikke i seg selv et
funksjonsfunn i denne kandidaten: den dokumenterte LF-representasjonen er
etterprøvd. Dette er Git-blob-/filterkontroll på Windows; **ingen native Linux-
kjøring eller fersk publisert klon** er påstått av denne kontrolløren.
Kandidatens endrede eksisterende basefiler er bare AGENTS og kildefunn.

Begge kontrollskriptene tar `--root`, `--candidate` og `--base`. Kandidaten
kan være en annen tilgjengelig, publisert commit med identisk kanonisk tre;
ingen utilgjengelig lokal commit er eneste kontrollmodus. `render_actual.mjs`
tar dessuten `--runtime` til loaderens Node-katalog. Python-skriptet kan bruke
en ny `--output` ved fersk kjøring, og kan gjenlese egne ferdige prøvepar.
Ruff og formatkontroll for eget Python-kontrollskript bestod.

| Port | Status i denne kontrollen |
| --- | --- |
| M05/M14 – hele faste tabell og konto-/fullmaktsinventar | Bestått, egen originalfasit og PDF-inspeksjon |
| M13/M28 – avgrensede grener / bevarte beriktigede representasjoner | Bestått innen bevart kildegrunnlag |
| M22/M23/M27 – begge innganger, faktiske filer, retur og utvalg | Bestått, 18 egne filpar |
| M24 – celle-/synlighetskontroll og faktisk visuell QA | Bestått i de 13 angitte renderområdene, med previewgrensene over |
| M25 – autentisk legacy / gamle hele objekter | Bestått |
| M26 – ordinær registrering ved fire feiltilstander | Bestått, egen omkjøring av relevant test |
| Full Standards/Spec, sikkerhetsaudit, publisert fersk klon, full Linux-CI og merge | Separate porter hos orkestrator |

Ingen positiv helårsdekning, faglig årssaldo, T6-beløpsstrukturering eller
rekonstruert rettelseshistorikk følger av denne attesten.
