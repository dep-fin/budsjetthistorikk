# Separat sikkerhetsetterkontroll av T5/#62 etter råbytebevaring

**Portstatus: BESTÅTT på den faste kandidaten nedenfor. Ingen åpne P1-/P2-sikkerhetsfunn. Temafunnet forblir lukket. De 49 tidligere manifestavvikene er faktisk lukket mot uendrede historiske hashverdier.**

| Binding | Fast verdi |
| --- | --- |
| Kandidat | `cd240e3b2f4846081d1f658faf0caec9cf4a7186` |
| Kandidattre | `1f32d2e81f8ff76fb3365d9c0fa6592fbb64eb39` |
| Base | `2f4ee30c9d8074076fc8042e208c4a4b6345db6b` |
| Tidligere sikkerhetskontrollert kandidat | `95ed8e60052d7731bb99386db572ba607c6b36a2` |
| Tidligere tre | `225382d23bf776a8c9ee1a81a8d27de90e1b8620` |
| Checkout | `C:\Users\marti\Documents\ChatGPT\Budsjetthistorikk\work\t5-prop16` |
| Faktisk lastet T5-Excel-leser | 16652 byte; SHA-256 `3f2a902567e1408ffb01fef625b38e98e334896b89979cdd6661caf565d4177e`; Git-blob `faa1453529b3fc38e2b8525d3c83eda687f068d8` |

Hele kandidaten siden base inngår i vurderingen. AGENTS, arbeidsflyt, issue-regler, ansvarsdeling, T5-kontrakten, T5-kontrollinngangen, tidligere sikkerhetsrapport, security-fix, integrasjonshjelperne, de tre sluttreviewene og byte-preservation er lest. #62-grunnlaget er de bevarte kravene i kontrakt/akseptmatrise og de tidligere reviewene; GitHub er ikke lest på nytt innen dette oppdragets GitHub-forbud. Ingen påstand om aktuell issue-/PR-status følger.

## Funn og bevarte sikkerhetsforutsetninger

Ingen nye prioriterte sikkerhetsfunn er identifisert. Produktet og kontrollhjelperne er uendret siden 95ed: **221** eksisterende filer under analyse, innlesning, ops, tester, drift og CI, samt rotattributter/pyproject, har samme Git-objekter. De to nye integrasjonshjelperne og øvrige eksisterende kontrollprogrammer er også uendret; alle endrede gamle blobber ligger i det uttrykkelige 62-filers råbyteutvalget. Dermed videreføres den tidligere auditens forutsetninger om API-er, gardering, terskler, kildepinner, gammel skriver og temaets faste payload uten ny tung fullkontroll.

Mot opprinnelig base er **1181/1183** filer fortsatt identiske Git-objekter. De eneste baseavvikene er de allerede foreliggende additive AGENTS-/kildefunnpekerne. Ingen gammel primærkilde, autentisk fixture, schema 5/B5-kode, standardutvalg eller gammel guardprofil er endret.

**Tidligere P2, temastyrt skjuling: fortsatt lukket.** Grensen er `analyse/proposisjon16_excel.py:286–295`, med etterfølgende stil-/cellekontroll. Egen ny kjøring skrev, lukket og gjenleste et offentlig JSON/XLSX-par med autentisk gammel T1-basis. Åtte faktiske temaendringer beholdt nøyaktig samme gyldige snapshot og alle andre ZIP-payloads, og ble avvist med `T5-Excel har endret tema for farger/skrift`:

- hvit `dk1`, endret systemfarge-fallback, minor-font, major-font, temanavn og fontskjemanavn, alle seks med uendret byteantall;
- UTF-8-BOM og XML-kommentar i temadelen.

Manglende tema, DOCTYPE/ekstern entitet, ekstern temarelasjon og feil temainnholdstype ble avvist av de tidligere pakk-/XML-grensene. Dette er offentlige leserutfall på faktiske filer, ikke native Excel-rendering.

Øvrige nye prober avviste ZIP-traversering, rå `applyFont`-omgåelse, duplikatnøkkel, NaN og en rehashet tredobling av IVs delte ramme gjennom både JSON og XLSX. Den forgiftede Excel-filen hadde kapsel og presentasjon skrevet fra samme forgiftede rapport og passerte beholderuttrekket. Eksisterende JSON/XLSX/originalkatalog ble avvist uten endrede byte. Alle **25** nye originaluttak var identiske med den validerte kapselen. Kald gjenlesing med tømte analyse-/innlesningscacher og sperret `socket.socket`/`sqlite3.connect` bestod.

## Attributter og manifesttillit

`reviews/.gitattributes:2–10`, `security-fix/.gitattributes:2` og `byte-preservation/.gitattributes:2` setter bare `text` og `whitespace`. Det finnes ingen filterkommando, diff-/mergedriver, encodingregel, `export-subst` eller annen kjøreinngang i tilleggene. De seks ekstra `-blank-at-eol`-unntakene gjelder bare to navngitte historiske prosesslogger og fire navngitte diffarkiver. De deaktiverer ingen produktkontroll.

Egen uttømmende `git check-attr --source=...`-sammenligning over kandidatens sporede stier viste attribusjonsendring for **125** stier, alle under de tre avgrensede kontrollmappene. Ingen regelendring treffer runtime, testfixture, primærkilde eller rotens gamle attributtfil. At `**` også gjelder framtidige filer innen kontrollmappene er den tilsiktede råbyteprofilen; mønsteret utvider ikke skopet til søsken eller foreldre.

Manifestverdiene ble lest direkte fra både 95ed og den nye kandidaten. JSON-innholdet i de to historiske manifestene og leveransemanifestet er identisk. Deretter ble faktiske Git-blobbyte kontrollert uavhengig:

| Uendret manifest | Avvik i 95ed | Avvik i cd240e3 |
| --- | ---: | ---: |
| `security-fix/manifest.json`, 18 bindinger | 9 | 0 |
| `reviews/integration/manifest.json`, 54 bindinger | 40 | 0 |
| `delivery-manifest.json`, 35 bindinger | 0 | 0 |

Dette er gjenoppretting av opprinnelige byte, ikke nye hashverdier som skjuler tap. Alle **49** nye blobber treffer de gamle manifestenes byteantall, SHA-256 og Git-blob-SHA-1. Alle **62** endrede gamle blobber treffer råbindingene; eneste forskjell fra hver tidligere Git-blob er eksakt CRLF→LF i den tidligere representasjonen. Hele det opprinnelige **104-filers** kontrollinventaret treffer sine bevarte råbindinger både i arbeidsflaten og Git. `git hash-object --path` med `core.autocrlf=true` og `false` ga korrekt opprinnelig rå blob-ID i **98/98** egne forsøk.

De fire `.py.original`-arkivene treffer sine opprinnelige byte-/SHA-/Git-bindinger og har samme blob som i 95ed. Det nye bytebevisets **17** manifestbindinger treffer kandidatblobene. Alle **11** nye JSON-filer i byte-preservation bestod egen streng syntakskontroll med duplikatnøkkel-/ikke-endelig-tall-avvisning.

Den gamle sikkerhetsrapportens P2, `results-final.json` med 70/69 og akseptert `theme_integrity`, security-fix sitt faktiske røde `DID NOT RAISE`-forsøk og begge tidligere Standards-/Spec-P2-rapporter er fortsatt historikk. De umaterialiserte replayfeilene med `AssertionError: .gitattributes` og returverdi 1 står fortsatt i det additive beviset. Den nye sikkerhetsporten omskriver ingen av disse attestene.

## Replay, stier og gjenoppretting

`byte-preservation/README.md:134–162` beskriver en ny, isolert arkivkopi. `replay-representation.json` er data med én fast operasjon, ikke et program eller en kommandoinngang. Alle **344** rader ble kontrollert mot faktisk kandidatblob, det uendrede historiske 1270-filers baselinemanifestet og de fire uttrykkelige arkivsubstitusjonene. Stiene er unike, relative, sporede regulære filer; ingen absolutt sti, kolon, bakstrek, `..` eller symlink forekommer. Hver lagret input er CR-fri og gir nøyaktig de gamle råhashene etter LF→CRLF. Ingen vilkårlig payload avledes eller godkjennes ved bare å oppdatere en hash.

Egen ny `git -c core.autocrlf=false archive` av **cd240e3** ble pakket ut under `.local/byte-final-security/byte-checks/candidate-copy` etter kontroll av alle arkivstier. Hele kandidatens tre består av regulære blobfiler. Før skriving ble alle kartets input-/outputbindinger og resolved målstier kontrollert. **342** filer krevde materialisering; de to eksisterende CSV-reglene leverte allerede historisk CRLF. Etterpå traff alle **1270** historiske råbindinger. Bare den nyopprettede kopien ble materialisert; basens/kandidatens kilder, råmanifest og resultater ble ikke skrevet om.

Den **uendrede** `compare_evidence.py` ble deretter faktisk kjørt mot denne ferske kopien, med eksplisitt rot, historisk d465-kandidat, base, replay og ny outputsti. Returverdi var **0**: 1270 bevaringsbindinger, 47 historiske security-fix-bindinger og fire like normaliserte ledgertyper. Denne kjøringen gjenbrukte de tidligere ferskgenererte historiske replayutdataene etter kontroll av samtlige **18** publiserte råbindinger til lokale ledgere/logger. Alle **ti** faktiske genererte JSON/XLSX-artefakter i de to variantene ble også bundet til størrelse/SHA-256 i de verifiserte ledgerne. De åtte hjelpeprosessene er ikke regenerert av denne auditen. XLSX-medlemmer ble sammenholdt av den uendrede sammenligneren; dens presise klokkeslett-/ZIP-/stiunntak ble beholdt.

Hjelperne bruker argumentlister uten shell og eksplisitte ref-/rotparametre. Publiserte refs med tilsvarende tre er fortsatt en gyldig modus. Historisk d465-replay beholder uttrykkelig den kjente temaaksepten og gir ingen sikkerhetsgodkjenning av gammelt produkt. Den nye porten bygger på faktisk cd240e3-kode og egne leserprober. Kontrollprogrammene og kartet forutsetter et uttrykkelig valgt, betrodd Git-tre og privat lokal output; de er ingen tjeneste for ubetrodde arkiver/kart. I dette skopet er ingen ny sti-, overskrivings-, kommando- eller gjenopprettingsrisiko identifisert.

## Egne bevis og begrensninger

**16 navngitte bevarings-/replaykontroller og 25 navngitte leserprober bestod**, med tilleggskontroll av historiske manifester og feilforsøk. Dette er antall kontrollgrupper/prober, ikke 41 uavhengige sikkerhetsegenskaper eller en fullsuite.

| Lokal ledger under `.local/byte-final-security/` | SHA-256 |
| --- | --- |
| `byte-checks/results.json` | `b67ccaa3013e264c2ec7ea5d8d98e009eb9de8b86f068fa3b71daaf35960c290` |
| `reader-probes-2/results.json` | `783f44ed3ae0cfdb3b880e9a9d8d23d94834e2ff064684c28fb8118502b79ee5` |
| `supplement.json` | `70fd8d6e1299dcd956d625a0b7840b0766b5f253ebe555c8ec5a3219a2720be7` |
| `byte-checks/comparison/replay-comparison.json` | `9eefe154423f6668b703435796edf40792c2a97193e5cda553a910c4b88c6ffb` |
| `attempts.json` | `2001d64a9a5be986742cbf20fc7893147e953e9571a11335ca98d015796be5eb` |

Første egen probekjøring stoppet fordi en tekstlig NaN-mutator søkte etter mellomrom som ikke finnes i kanonisk JSON. Input var dermed uendret og korrekt akseptert; dette var ingen akseptert angrepsfil. Første program/utdata er beholdt lokalt. Mutatoren fikk eksplisitt inputkonstruksjon og mutasjonsassert, og den komplette nye kjøringen på egen outputsti bestod.

Bundled Python og det oppgitte `c06-99235/.local/python-tools`-miljøet ble brukt. Kandidatens sporede arbeidsflate ble kontrollert før og etter; kildeindeksens SHA-256 var uendret. Bare denne dokumentariske rapporten og egne ignorerte bevisfiler er skrevet av auditen. Ingen produktretting, staging, commit eller GitHub-operasjon er utført.

Ingen ny primærkilde, fullsuite, gjentatt 70-/122-probereplay, ny full statisk kontroll, rendering, native Excel, nettverksklon, Linux-kjøring, junction-race eller samtidig ubetrodd lokal filskriver er omfattet. Per-fil no-clobber gir fortsatt ingen transaksjon over et helt filpar. Tidligere uendrede forutsetninger er overført ved faktisk bloblikhet og målrettet etterprøving. Publisert-klon-porten, øvrige reviewer, full CI og autorisert merge er egne porter; ingen av dem attesteres her.
