# Separat sluttsikkerhetsaudit av T5/#62

**Portstatus: BESTÅTT for den faste kandidaten nedenfor. Ingen åpne P1-/P2-sikkerhetsfunn. Det tidligere P2-temafunnet er lukket ved egen etterprøving.**

| Binding | Fast verdi |
| --- | --- |
| Kandidat | `95ed8e60052d7731bb99386db572ba607c6b36a2` |
| Kandidattre | `225382d23bf776a8c9ee1a81a8d27de90e1b8620` |
| Base | `2f4ee30c9d8074076fc8042e208c4a4b6345db6b` |
| Checkout | `C:\Users\marti\Documents\ChatGPT\Budsjetthistorikk\work\t5-prop16` |
| Faktisk lastet T5-leser, SHA-256 | `3f2a902567e1408ffb01fef625b38e98e334896b89979cdd6661caf565d4177e` |
| Leserens byteantall / Git-blob | `16652` / `faa1453529b3fc38e2b8525d3c83eda687f068d8` |

Auditen omfatter hele kandidaten siden base: nye modell-/adapter-/analyse-/Excel-moduler, CLI, kontrollhjelpere, tester, dokumentasjon og kontrollarkiv. AGENTS, arbeidsflyt, ansvarsdeling, issue-regler, hele #62 med gjeldende kommentar, T1-/T5-kontraktene, hele den opprinnelige sikkerhetsrapporten, security-fix-pakken og integrasjonens programmer/bevis er gjennomgått. Sporede arbeidsfiler var identiske med kandidaten før og etter probene. Bare denne nye dokumentariske rapporten og egne ignorerte filer i `.local/final-security` er skrevet av auditen.

## Funn og etterkontroll

**Lukket P2 — temastyrt skjuling av status og feltbindinger.** Sted: `analyse/proposisjon16_excel.py:286–295`; samvirkende rå stilkontroll på linje 301 og celle-/synlighetskontroller på linje 304–351.

Den nye leseren binder hele `xl/theme/theme1.xml`, både størrelse og byte, til skriverens `theme_xml`. Kontroll av lokal temarelasjon og innholdstype kommer først. Dette binder også fontskjemaet, som påvirker celler med `scheme=minor`. Det er ingen kontroll som bare søker etter en kjent hvit fargeliteral. Diffen mot den gamle kandidaten endrer importene og denne lesergrensen; `_book` og eksportskriveren er uendret.

Det opprinnelige angrepet er kjørt på nytt mot **95ed**, og avvises nå med `T5-Excel har endret tema for farger/skrift`. Åtte egne alternative temaendringer ble deretter skrevet som faktiske XLSX-filer. Alle beholdt samme gyldige snapshot og øvrige ZIP-payloads og ble avvist med samme temafeil:

- hvit `srgbClr` med utfyllende XML-mellomrom, slik at temadelens byteantall er uendret;
- endret systemfarge-fallback, minor-font og major-font, hver med uendret byteantall;
- et annet temanavn med uendret byteantall;
- XML-kommentar, UTF-8-BOM og endret navn på fontskjemaet.

Dermed er også fem nærvarianter som passerer størrelseslikheten faktisk stanset av bytekontrollen. Manglende tema, ekstern temarelasjon, feil temainnholdstype, DOCTYPE og tema over metadatagrensen ble avvist av de tidligere beholder-/pakkgrensene. Native Excel-rendering av angrepsfilene er ikke utført; vurderingen bygger på faktiske OOXML-byte, uendret kapsel og offentlige leserutfall.

Ingen nye prioriterte sikkerhetsfunn er identifisert i den avgrensede lokale angrepsflaten. Standards-sporets tidligere valgfrie P3 om kontopredikatduplisering er ingen sikkerhetsblokkering og er ikke rettet her.

## Egne faktiske prøveutfall

**122 navngitte kontroller bestod; ingen angrepsfil ble uventet akseptert.** Dette består av 70 retargeterte kontroller og 52 egne nærvariant-/positivkontroller. Det er ingen påstand om 122 uavhengige sikkerhetsegenskaper eller fullsuite.

Den historiske `security/probes.py` ble kopiert til ignorert lokalt kontrollområde. Bare forventningen om at temaangrepet skulle aksepteres ble erstattet med forventet avvisning. `verify_outcomes.py` fikk tilsvarende endring. Kandidat, base, tre, faktisk modulrot og ren sporet arbeidsflate ble kontrollert eksplisitt. Begge kjøringer brukte den rettede kandidaten, og ikke integrasjonens gamle isolerte d465-mål. De øvrige 69 kontrollene og tersklene ble beholdt.

| Grense | Faktisk utfall |
| --- | --- |
| Gyldig offentlig filpar og legacy | Ny JSON/XLSX ble skrevet, lukket og gjenlest. T1-basis var lik autentisk gammel fixture; 105 nye felt og full union 123/6/2 bestod. Gammel leser leste autentisk T1. |
| Streng JSON | Duplikatnøkkel, ekstra felt, bool/desimaltall i heltallsfelt, NaN og begge Infinity-varianter ble avvist. Fil over 64 MiB ble avvist før parsing. |
| Rehashet semantikk | 14 tidligere og fem nye forgiftninger ga **38 avvisninger** gjennom faktiske JSON- og XLSX-lesere. Objekter/basis/rapport ble identifisert på nytt; XLSX-kapsel og presentasjon ble skrevet fra samme forgiftede rapport og passerte beholderuttrekket. |
| Semantiske angrep | Dekket falskt beløp og null, rolle, år, betydning, step-ID, forfatter, råverdi, gammel vedtaksidentitet, 1533-grenlekkasje, oppdelt/tredoblet delt ramme, falsk dekning/telling, skjulte globale hull, feil feltbinding, falskt vedtaksstadium/kontekst og endret kildekatalogrekkefølge. Avvisningen kom fra type-/original-/basisrekonstruksjon. |
| Kildepayload | Rehashet falsk kildeverifisert HTML, ugyldig og for stor base64 ble avvist. Uoverensstemmende gzip over 32 MiB utpakket ble ikke dekomprimert; forsøk på å oppgradere den til kildeverifisert ble avvist. |
| Excel-celler og synlighet | Formler, tekstlig/boolsk null, flyttallsleksikal null, stilomdirigering, rå `applyFont`/fontskjemaendring, skjult rad/kolonne/ark, null kolonnebredde, rik tekst, feil chunkrekkefølge og for stor radpeker ble avvist. |
| Pakker og lenker | Eksterne relasjoner, ekstern internlenke, uventede/traverserende eller dupliserte ZIP-medlemmer/celler, ekstra arkrelasjon, alternativ kompresjonsmetode, DOCTYPE og deklarert utpakking over 128 MiB ble avvist. |
| Lang ubetrodd tekst | Over 60 000 tegn fra den offentlige manuelle relasjonsinngangen, med formellignende `HYPERLINK`-tekst, ble bevart bokstavelig gjennom JSON/XLSX og ordnede videreføringsark. Ingen formelceller. |
| Offline | Begge offentlige lesere bestod etter cachetømming med `socket.socket` og `sqlite3.connect` sperret. `--frosset`-CLI bestod med ikke-eksisterende kilderot. |
| No-clobber | Eksisterende JSON/XLSX og originalkatalog ble avvist uten endrede filhasher. En faktisk Windows-publiseringsrace beholdt vinnerens byte og fjernet midlertidig JSON. |
| Originaluttak | Alle **25** råpayloads var byteidentiske med den validerte kapselen; 21 ble også sammenholdt med tilgjengelige direkte repositoryfiler. |
| Ordinær vedtaksregistrering | Fire faktiske manglende/feilede/korrupte/motstridende T5-importer ble fulgt av ordinær 40034229-synkronisering, rålagring, v2-tolkning, SQLite, analyse og Excel: **222 observasjoner / 74 hendelser** i hver prøve. |
| Gyldige tidligere eksporter | Alle **14** eksisterende par i `.local/delivery-final` ble gjenlest med den nye leseren og var lik JSON-rapportene og den gamle T1-basis. I tillegg bestod de nye eksportene fra egen probe, CLI og langtekstprøve. |

Stikontroll er også gjennomgått i `innlesning/proposisjon16.py:225–254` og `analyse/proposisjon16_excel.py:387–402`: katalogen er eksplisitt og pinnet, rapporten valideres før originaluttak, resolved sti må ligge under valgt rot, ny originalkatalog kreves, og råpayloadfiler åpnes med `xb`. Ingen katalogsti kommer fra et vilkårlig ZIP-medlem. Junction-/symlink-racer er ikke utført.

## Kontrollhjelpere, arkiv og bytebetydning

De nye integrasjonshjelperne er lokale vedlikeholderprogrammer for en uttrykkelig valgt Git-kandidat og egne replayfiler. De er ikke offentlige lesere for vilkårlige opplastede arkiver. `replay_helpers.py:47–75` bruker argumentliste til Git/prosesser, lager `git archive` fra valgt ref, kontrollerer målsti før uttak og bruker privat indekskopi. `compare_evidence.py:116–159` binder målref/tre, arkivkart og AST-sammenligning. Ingen nettverks-/database-/dynamisk kodeinngang er lagt til produktleserne gjennom disse programmene. Kontrollhjelpernes hele arkivinnlesning og repo-fixturebaserte gzip-kontroller vurderes innen denne lokale tillitsgrensen; det kreves ikke generell arkivtjenesteinfrastruktur.

Egen AST-kontroll bekreftet identisk AST for `artifact_checks.py` og `standards/controls.py`. For `probes.py` og `verify_outcomes.py` ble likhet bekreftet etter eksplisitt oppdeling av fleraliasimporter og sortering av sammenhengende importblokker. Dette bekrefter de øvrige kontrollbetingelsene, men innebærer ingen generell antakelse om sideeffektfri importrekkefølge. Integrasjonens bevarte før/etter-ledgere gjelder samme gamle d465-mål og viser 70/69 i begge varianter. De er historiske regresjonsbevis, ikke sikkerhetsgodkjenningen av 95ed; denne rapportens egne kjøringer gir den nye etterkontrollen.

Faktiske kandidatblobber og rå arbeidsfiler ble kontrollert separat:

- Alle fire `.py.original`-arkiver stemmer eksakt med kartets størrelse, SHA-256 og Git-blob-SHA-1. De har LF både i checkout og Git; her er det ingen skjult CRLF-konvertering.
- Alle 1270 historiske baselinebindinger stemmer mot råbyte, med de fire eksplisitte arkivsubstitusjonene. De 47 `preserved-before`-bindingene, 18 security-fix-manifestbindingene og 54 integrasjonsmanifestbindingene stemmer også mot erklærte råbyte.
- Disse historiske råbytemanifestene er **ikke alle LF-/Git-manifester**: henholdsvis 365/1270, 12/47, 9/18 og 40/54 oppføringer har Git-blob lik råfil etter CRLF→LF, men annen råhash. Ingen øvrige forskjeller ble funnet. De skal ikke omtales som eksakt Git-blobsamsvar, og råbevaringsdelen av hjelpeprogrammene forutsetter den dokumenterte checkoutrepresentasjonen. Ingen ny Linux-/fersk-klon-kjøring av denne råbevaringsdelen er påstått.
- Leveransemanifestets **35** oppføringer stemmer derimot direkte med kandidatens Git-byte, størrelse, SHA-256 og Git-blob-ID og oppgitt LF-representasjon. Alle **48** nye JSON-artefakter bestod streng syntakskontroll, og **18** PNG-er bestod signatur-/CRC-/størrelseskontroll. PNG-kontrollen er ingen visuell QA/full billeddekoding.
- **1181 av 1183 basefiler** har identiske Git-objekter; bare de to additive AGENTS-/kildefunnpekerne er endret. Gamle skrivere/guardprofiler, originalkilder, fixtures, legacyformater, schema 5/B5, standardvalg og CI med 90-minuttersgrense er bevart.

## Bevis og begrensninger

Egne resultater ligger under `.local/final-security`; de er midlertidige lokale bevis, ikke nye sporede kjørbare filer eller endrede historiske manifester. De viktigste ledgerne er bundet slik:

| Lokal ledger | SHA-256 |
| --- | --- |
| `verified.json` — 70/70, råuttak og kald offline-etterkontroll | `0a9cfa1f27d0a392948fbb842ff19c5d4637f7d34791061d894271b1601875b5` |
| `near/results.json` — 38 nye negative og 14 positive kontroller | `a8b6d30be179cf041cd094cf6db9eeb0817f73e23ebdd89065634d6eeac65ef5` |
| `artifact-checks.json` — kandidatens manifest/JSON/PNG | `90a3e745cec8f2d57f2ba79291191d9ea066a35dd95e5f747b418b64a4885cca` |
| `archive-binding.json` — råbyte mot faktiske Git-blobber | `d977535d90df9c86de7ad48f09181b397d8a78fffa290b47d0f68d9240d2817f` |
| `ast-verified.json` — egen kontroll av fire hjelperendringer | `5be0938c89f4c9ac65e97f2febf5ffcf0df3f4b72b5cbe13707728f5e36d5641` |

Egne replayprogrammer tar eksplisitt `--root`, `--candidate`, `--base` og egne nye outputstier. Tilgjengelig publisert ref med samme tre kan brukes; ingen utilgjengelig gammel lokal SHA er nødvendig for den nye sikkerhetsetterkontrollen. Den tidligere d465-forventningen er uttrykkelig erstattet i de ignorerte kopiene, og originale programmer/resultater er bevart.

Ingen ny primærkilde er hentet. Ingen produktretting, staging, commit eller GitHub-skriving er utført. Hele testfilen på 38 tester, fullsuite, Ruff/mypy, ny visuell QA, fersk klon, POSIX-publisering, Windows-junction-racer eller Linux-CI er ikke kjørt av denne auditen. Atomisk publisering er kontrollert per fil; `export_pair` lover ingen transaksjon over begge filene. Ingen tjeneste med samtidige ubetrodde lokale filskrivere er omfattet.

**Sikkerhetsporten er bestått på 95ed-kandidaten. Full CI og bekreftet merge er fortsatt egne, uutførte porter i denne rapporten.**
