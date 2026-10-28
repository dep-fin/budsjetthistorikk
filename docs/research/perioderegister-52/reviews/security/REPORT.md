# Uavhengig lokal sikkerhetsaudit av P1

Dato: 28. oktober 2026. Resultat: **rett to P2-funn i Excel-valideringen før sikkerhetsporten godkjennes**. Kilde-/modellkontrollen avviser de undersøkte semantiske forfalskningene, også etter ny beregning av innkommende ID-er og payloadhasher.

## Kandidat og utført avgrensning

- Arbeidsflate: `C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/p1-perioderegister`.
- Base: `29ac220f62b35062fc4203f054e2f757ca795b7c`.
- Kandidat/HEAD: `4413a5f21be71ccd2ad5c885560da6bae2e8b885`.
- Tree: `afc1eacfa74cec19e35a5cb49ee5907be5bfc877`.
- Hele diffens endrede kode, kontrakt, bygge-/kontrolldokumentasjon og relevante gjenbrukte validatorer inngikk. `candidate.json` bevarer endringslisten og SHA-256 til alle åtte endrede kjørbare filer. HEAD, ren Git-status og kodehasher ble kontrollert før og etter kjøring.
- AGENTS, arbeidsflyt, ansvarsdeling, P1-kontrakten og byggebevisene under `docs/research/perioderegister-52/` ble lest. Gamle, uendrede validatorer ble undersøkt der P1 bruker dem.
- Ingen produktkode, originalfil, Git-tilstand, GitHub-objekt eller annet eksternt system ble endret. Alle nye filer ligger i denne auditmappen. Inputfiler ble kopiert og hashkontrollert; originalene ble kontrollert uendret til slutt.

## Funn som må rettes

### P2-1: Eksternt hoveddokument i pakkens rotrelasjon blir godkjent

**Plassering i ny kode:** `analyse/perioderegister_excel.py:424–435`. Underliggende mangel ligger i gjenbrukt `analyse/omtale_excel_guard.py:356–372`: `_rels/.rels` blir bare XML-parset; den samme semantiske kontrollen som avviser eksterne workbook-relasjoner blir ikke brukt på pakkens rotrelasjoner.

Jeg endret bare `officeDocument`-relasjonen i `_rels/.rels` i en kopi av en gyldig bok:

```xml
<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
              Target="https://example.invalid/synthetic.xlsx"
              TargetMode="External" Id="rId1"/>
```

`read_excel()` godkjente filen og returnerte den samme rapporten som originalen. Den lokale `xl/workbook.xml`, cellene og offlinekapselen var uendret. Den eksterne hoveddokumentrelasjonen og den lokale arbeidsboken som openpyxl leste, var dermed ikke avstemt. En fil med dette avviket skal ikke godkjennes som en lukket P1-arbeidsbok. En faktisk Office-klient kan avvise eller behandle pakken annerledes; det er ikke prøvd her.

**Reproduserbart bevis:**

- `synthetic/container-root-external-office-document.xlsx`
- SHA-256 `929615ec56df384b1113fe57351d26948d8ae52b242fa4bc429537756a981a68`
- `results.jsonl`: `xlsx-root-external-office-document`, status `ACCEPTED`.
- `confirmed-findings.json`: samme rapport-ID og full modelllikhet, gjentatt med socket- og SQLite-kall blokkert. Ingen slike kall fant sted.

**Nødvendig retting:** Kontroller relasjonssemantikken for alle tillatte `.rels`-filer. Avvis `TargetMode="External"`, krev entydige relasjons-ID-er, og bind rotrelasjonens ene `officeDocument` til den faktiske lokale arbeidsboken. Kontroller at target/type og pakkens deklarerte innhold stemmer. Denne konkrete filen må gi `ValueError` før filen godkjennes. Ikke stol på at openpyxl bruker samme inngang som en Office-klient.

Dette funnet beviser en lokal container-/integritetsmangel. Det er **ikke** påvist nettverkstilgang, datautsending eller kodekjøring.

### P2-2: OOXML-flagg som styrer bruk av justering, faller utenfor stilkontrollen

**Plassering i ny kode:** `analyse/perioderegister_excel.py:469–474`, særlig sammenligningen av `actual.alignment`. Gjenbrukt `analyse/omtale_excel_guard.py:154–196` kontrollerer stiltabellindekser, men binder ikke `xf`-flaggene til den forventede eksportprofilen.

Jeg endret `applyAlignment="1"` til `applyAlignment="0"` i `cellXfs` i `xl/styles.xml`. De samme `alignment`-elementene med `wrapText="1"` ble stående. Alle celler, råverdier, offlinebyte, stiltabellindekser og arbeidsbokdimensjoner var ellers uendret. `read_excel()` godkjente filen og returnerte fullstendig samme rapport som originalen.

`applyAlignment` styrer om en celles deklarerte justeringsformat skal anvendes. Openpyxls deserialiserte `alignment` som sammenlignes her, bevarer ikke denne forskjellen i sammenligningsgrunnlaget. P1 godkjenner derfor filen uten å avstemme et formatflagg som kan endre blant annet tekstbryting og hvor mye av lange kilde-/statusfelt som blir synlig. Det er et konkret hull i den avtalte presentasjonskontrollen. Den faktiske effekten i native Excel er ikke målt i denne auditten.

**Reproduserbart bevis:**

- `synthetic/container-apply-alignment-zero.xlsx`
- SHA-256 `c10c3fa0f85ee0d501785d0ccfb5ec990c1aaff76d989baf258e8692dc7140a7`
- `results.jsonl`: `xlsx-apply-alignment-zero`, status `ACCEPTED`.
- `confirmed-findings.json`: alle sju innkommende `cellXfs` har `applyAlignment="0"`; filen godkjennes fortsatt med full rapportlikhet og blokkerte socket-/SQLite-kall.

**Nødvendig retting:** Avstem de relevante rå OOXML-stilelementene og anvendelsesflaggene mot skriverens forventede profil før den normaliserende openpyxl-lesingen brukes som bevis. En smal, uttrykkelig eksportgrammatikk eller en kanonisk sammenligning av de relevante stildelene er tilstrekkelig; en generell tolerant Excel-leser er ikke nødvendig for P1. Legg inn regresjonsprøve for denne filen og relevante `applyFont`/`applyFill`/`applyNumberFormat`-varianter.

## Kontroller og faktisk bevis

`results.jsonl` inneholder 56 unike hovedkontroller: 11 beståtte positive/integritetskontroller, 43 forventede avvisninger og de to akseptene ovenfor. `resource-publication-results.json` har ytterligere 15 kontroller: 13 forventede avvisninger og to beståtte publiseringskontroller. Akseptene ble deretter bekreftet separat i `confirmed-findings.json`.

### Autentiske kilder og selvhash

- Alle **130** katalogfiler ble lest direkte som Git-blobb fra den faste basen. Byteantall og SHA-256 stemte med P1-katalogen. Alle pinnede dekomprimerte representasjoner stemte også. Resultatet ligger i `catalog-base-proof.json`; det er ikke bare en sammenligning med filer fra samme innkommende rapport.
- Rapport- og basisvalideringen rekonstruerer forventet modell fra faste katalogankere. Eksisterende T4/T1 kontrolleres gjennom sine opprinnelige porter. Den nye P1-ID-en er ikke eneste anker.
- 21 separate JSON-muteringer fikk nye P1-objekt-ID-er, nye basis-/rapport-ID-er og oppdaterte referanser før offentlig `read_json()` ble kalt. År, post, fullmaktsrolle, monetær fullmaktsvirkning, originalalternativ som vedtatt, Prop.36 som hendelse, kandidatordinal/-år/-post, lokator, representasjonshash, skjulte hull, skjulte globale kandidat-ID-er, positiv årsdekning/-godkjenning, teksttap, kildeforelder/-hash, samlingstak, duplisert payload og ugyldig base64 ble avvist.
- I en ekstra prøve ble selve kildebyteinnholdet endret, og fysisk payload-ID, payloadhash, base64, påstått kildehash, kilde-ID og alle påfølgende P1-ID-er ble beregnet på nytt. Påstand om `kildeverifisert` ble fortsatt avvist mot den uavhengige katalogen.
- Fire av de forgiftede modellene ble skrevet som faktiske Excel-filer med tilsvarende forgiftet offlinekapsel og konsistente dimensjoner. Hver eksakte kapsel passerte `inspect_excel()` før offentlig `read_excel()` avviste årsløgnen, monetær fullmaktsvirkning, skjulte globale hull eller positiv årsdekning semantisk. Avvisningene skyldtes dermed ikke bare ødelagt ZIP eller feil kapselstørrelse.

### Positive par og offline

- Fem faktiske eksisterende JSON/XLSX-par ble kopiert, lukket og gjenlest: begge poster, fullmakt346, tomt utvalg, feil år og ukjent indekskandidat.
- Begge poster beholdt **11 vedtaksfelt / 5 monetære hendelser**. De øvrige fire hadde **0 / 0**. Alle fem beholdt globale **67 / 25 / 7**.
- Gammel regneport beholdt `166039000` og `29185000`, begge med `avgrenset kontroll`. Begge navigasjonsretninger og retur ble kontrollert mot samme grunnlag.
- Offentlig P1-CLI ble kjørt fra tom arbeidsmappe med ikke-eksisterende originalrot, blokkert nett/SQLite og kopiert frosset input. Nye JSON- og XLSX-filer ble faktisk skrevet, lukket og gjenlest til samme rapport. `offline-cli.json` og `offline/reexport.*` er bevisene.

### Container-, type- og ressursvern

- Dupliserte JSON-felt, NaN, for dyp JSON og 64 MiB + 1 byte ble avvist.
- Falsk synlig celleverdi, hvit brødtekstfont, skjult rad og formel ble avvist fra egne muterte bøker.
- Hashkontrollerte kopier av eksisterende negative containere ble gjenlest: duplisert ZIP-medlem, traversalnavn, ekstern workbook-relasjon, enorm dimensjon, for mange ZIP-medlemmer, DOCTYPE og ekspandert total over grensen ble avvist. Rotrelasjonsunntaket er det konkrete funnet ovenfor.
- Nye samlingstak for ledd, saks-/vedtakskandidater, hull, bevis og kilder, samt 4096 inventarrader per dokument, ble prøvd separat og avvist.
- Streng base64, kontroll av overlang base64 før dekoding og forkastelse av fremmed gzip ved uavhengig pin bestod. Den begrensede gzip-lesingen ble dessuten isolert med en **midlertidig syntetisk katalogoppføring i auditprosessen**; en original på 32 MiB + 1 ble avvist. Dette siste er en eksplisitt enhetsprøve av ressursporten, ikke et angrep som omgår den ekte faste katalogen.
- ZIP/XML, delgrenser, 16 MiB-payloadporten og parserinnstillinger ble gjennomgått i gjenbrukte validatorer. Ingen generell nettinnhenter, pickle, eval eller dynamisk import fra innkommende data ble funnet i P1.

### Trygg publisering og ordinært nytt vedtak

- JSON- og Excel-skrivere avviste eksisterende mål uten å endre sentinelinnholdet.
- En kontrollert lokal konkurrerende skriver opprettet JSON-målet etter forhåndssjekken, akkurat ved publisering. Den faktiske Windows-publiseringen ga `FileExistsError`, beholdt den andre skriverens byte og fjernet egen midlertidig fil. Det er Windows-bevis; Linux-grenen ble bare lest.
- Ett nytt, selvstendig 368-forløp ble kjørt gjennom offentlig ordinær synkronisering, råbevaring, tolkning og faktisk Excel i `ordinary-368/`, etter at motstridende P1 var avvist. Resultatet var **222 observasjoner / 74 hendelser**, hashidentisk råkilde, schema **5**, uendret B5-seedregister og bare gammel `round='uavklart'`. For kap.700/post1 ble de faktiske lagrede cellene kontrollert til før `304351000`, endring `6324000`, etter `310675000`. Ingen historisk Excel var nødvendig.

## Reproduksjon og logger

Python: `C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`. Arbeidsmappe er kandidatens rot. Sett `PYTHONPATH='.;.local/python'`.

- `audit.py` viser hele hovedprøven. Hovedkjøringen ble gjenopptatt med `--resume` og deretter `--ordinary` etter tre feil i selve audit-harnessen: null betydde uspesifisert gammel dekomprimert størrelse; en opprinnelig antatt tallcelle G2 var nå tom etter sortering; datasettetiketten `audit` var ugyldig og ble endret til den eksisterende `prove`. Disse avbruddene er bevart i loggen og er ikke godskrevet som produktfeil eller beståtte kontroller. Alle resterende planlagte deler ble fullført. Siste hovedloggpost bekrefter uendret kandidat og originalinput.
- `resource_publication.py` er de supplerende begrensede ressurs-/publiseringsprøvene.
- `confirm_findings.py` bekrefter de to akseptene uten nett-/SQLite-tilgang.
- `candidate.json`, `catalog-base-proof.json`, `results.jsonl`, `resource-publication-results.json`, `confirmed-findings.json` og `offline-cli.json` er de primære maskinlesbare bevisene.
- `synthetic/` inneholder de faktiske negative filene. `inputs/` er kontrollerte kopier. `artifact-manifest.json` binder auditfiler og resultater til sine SHA-256.

## Bevisgrenser

Denne auditten kjørte målrettede egne prøver og offentlig CLI, ikke full testsuite på nytt. Byggerens fullsuite-, gamle kompatibilitets-, fire ordinære 368- og renderingsresultater ble lest som byggebevis, men er ikke omtalt som egne kjøringer her. Ingen full Linux-CI, merge eller produksjons-/driftsaksept er utført eller påstått.

Native Excel og faktisk nett-/kodeutnyttelse er ikke prøvd. De to funnene gjelder målbare hull i godkjenningen av en lukket Excel-fil. Auditten gir ingen faglig årsbalanse, helårsdekning, ny B5-avgjørelse eller kontokontinuitet. Produktkoden er uendret; retting og etterkontroll tilhører neste steg for samme P1-kandidat.
