# Uavhengig defensiv sikkerhetsaudit av P2 / #56

29. oktober 2026. **Sikkerhetsporten består for den faste kandidaten. Ingen nødvendige eller valgfrie sikkerhetsrettinger ble funnet i det undersøkte omfanget.** Dette er en separat audit av hele #56-diffen og de gjenbrukte offentlige filgrensene.

## Fast kandidat og mandat

- Arbeidsflate: `C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/p2-r2-adopsjon`.
- Base: `c041ad8ed3e2f8316896b6ff2364d3470024a992`.
- HEAD: `c2a55be0dd64b3f7617dc20453cc8cfdd9b44167`.
- Tree: `20f3750b6a30850607c11c4e5047256724dcd423`.
- Hele diffen, de ti nye kjørbare filene, kontrakten, testene, kontrollhjelperne og byggebevisene er gjennomgått. De gjenbrukte P1/T4/T1-, JSON-, payload-, ZIP/XML-, relasjons-, stil- og publiseringsportene er undersøkt der kandidaten bruker dem. Kandidatens kodehasher er kontrollert før og etter egne kjøringer.

AGENTS, arbeidsflyt, begrepsregler, ansvarsdeling, relevante domene-/P1-/P2-kontrakter, P1s opprinnelige sikkerhetsfunn og avsluttede etterkontroll er lest. Hele #56 og kommentarene, samt #54s gjeldende ferdigstatus og kommentarer, er hentet fra GitHub. #54 er ferdig i base-commit; eldre R2/K3/P1-rapporter med kandidatbundne «gjenstår»-tekster er historiske. Ingen slike filer eller bindinger er omskrevet.

Auditten brukte bare lokale kontrollfiler og har ikke endret produktkode, kilder, eldre kontrollfiler, Git-tilstand eller GitHub. Ingen agent ble delegert arbeid. Det ble ikke aktivert eksterne lenker eller formler, kontaktet eksterne angrepsmål eller endret drift.

## Funn

**0 nødvendige og 0 valgfrie sikkerhetsfunn.** Ingen undersøkt forfalskning ble feilakseptert, og ingen fullført negativ produktkontroll ga uventet unntakstype. Det er derfor ingen produktretting, fil-/linjefestet sårbarhet eller ny risikopåstand å følge opp fra denne auditten.

## Faktiske kontroller

`results.jsonl` inneholder **63 unike hovedkontroller: 13 beståtte positive-/integritetskontroller og 50 forventede ValueError-avvisninger**. Offentlig offline-CLI og fire friske ordinære 368-forløp er dokumentert separat. Kontrollene nedenfor er kjørt på nytt av auditor; byggerens tidligere beståtte resultater er ikke telt som nye auditkjøringer.

### Uavhengige kildeankere og gammel basis

Alle **69 katalogfiler** er lest direkte som Git-blobb fra den faste basen. Faktisk byteantall og SHA-256 stemmer med kodekatalogen. Hver komprimert original er dekomprimert og kontrollert mot separat representasjonshash og størrelse. Dermed bygger kontrollen på et annet anker enn den innkommende JSON-filens egen hash. `catalog-base.json` bevarer resultatene.

Alle **527 eksisterende produkt-, test-, kilde-, manifest-, avhengighets- og CI-filer** under de kontrollerte grensene er identiske med basen. Ingen eldre leser eller schema-/B5-/standardbane er endret. Workflowen har fortsatt hele testutvalget, Ruff/format/mypy og 90-minuttersgrensen. `.gitattributes` legger bare til bytebevaring av R2- og nye P2-bevis.

Den nye rapportens typede P1-basis er dessuten sammenlignet direkte med den autentiske tidligere `outputs/p1-52-973db1f/p1-1429-2024.json`. De er like, med samme basis-ID og alle gamle objekter. Begge-poster-rapporten beholder **11 vedtaksfelt / 5 monetære hendelser**; post 22 beholder **4 / 2**. Ingen ny AmountObservation eller faktisk fullmaktsbruk er innført.

### JSON og semantikk etter koordinert rehash

Auditten laget **23 egne forgiftede JSON-filer** med en separat implementert DAG-rehash, oppdaterte referanser og nye basis-/rapport-ID-er. Alle nye objekt-, basis- og rapportselvhasher er kontrollert separat i `summary.json`. Der P1 ble endret, ble også P1-objektene og P1-basis reidentifisert.

Alle 23 ble avvist: anslag fremstilt som vedtak, feil år eller post 22, O1-rest fremstilt som eksakt primærbeløp, faktisk fullmaktsbruk, ny 2025-bevilgning, oppfunnet overføringsbeløp, feil vedtaks-/forslags-/voterings-ID, feil komitéaktør, feil XPath eller representasjonshash, falsk gammel kandidat-ID, skjult status/kryssreferanser/kandidatliste/R1–R7, positiv årsdekning/-godkjenning, duplisert payload og endrede kildebyte med ny payloadhash, påstått kildehash og alle avhengige ID-er. De to koordinerte P1/P2-forfalskningene nådde den gamle P1-rekonstruksjonen og ble avvist der.

Fire av disse modellene ble skrevet og lukket som egne Excel-filer med nøyaktig den forgiftede kapselen: anslag som vedtak, uberettiget post 22, faktisk fullmaktsbruk og falsk gammel kandidat-ID. Alle fire passerte `inspect_excel()` med konsistente dimensjoner og nøyaktig kapseltekst før offentlig `read_excel()` avviste semantikken. Avvisningene skyldtes dermed den kildebundne modellen og ikke bare ugyldig ZIP eller kapselstørrelse.

Den gjennomgåtte rekonstruksjonen er `innlesning/perioderegister_r2.py:177` og `:729`; gammel basis valideres først i `analyse/perioderegister_r2.py:54`. Den strenge konvolutt-/felt-/typegrensen og rapportrekonstruksjonen ligger i `analyse/perioderegister_r2.py:158` og `:169`. Ukjente felt, boolsk verdi i heltallsfelt, feil nulltype og innkommende selverklærte roller får ingen generell tillit gjennom den typede dekoderen og likhetskontrollen.

### Excel, aktive innslag og ressurser

Fem eksisterende faktiske JSON/XLSX-par ble kopiert, hashkontrollert, lukket og gjenlest med de offentlige leserne: begge poster, post 22, tomt valg, feil år og dokument 429. Hvert par ga samme rapport. Alle fem beholdt globale **67 / 25 / 7**, én separat statusoppdatering og tolv kryssreferanser. Tomt valg, feil år og 429 hadde null valgte monetære hendelser.

Egne skrevne ZIP/XML-varianter ble avvist for endret `applyAlignment`, hvit tekst, feil tallformat, skjult rad/kolonne/arbeidsbok, feil filter og feil synlig år. De to tidligere P1-funnklassene er altså fortsatt dekket i P2: råstilen bindes til rekonstruert `styles.xml`, og rotens hoveddokumentrelasjon bindes til den lokale arbeidsboken. Dette skjer gjennom P1s uendrede `_style_profile` og `_package_profile`, kalt av `analyse/perioderegister_r2_excel.py:374` før godkjenning.

Harmløs formel `1+1`, ekstern rot-/workbook-relasjon med `example.invalid`, DOCTYPE og `../outside.txt` i ZIP ble avvist uten aktivering. Tre av byggerens begrensede ressursfiler ble kopiert byteidentisk og sendt gjennom offentlig leser på nytt: duplisert medlem, for mange medlemmer og for stort dekomprimert arkiv. De ble avvist før celletolking. Egen for stor dimensjon, duplisert JSON-nøkkel, NaN, 3000 nivåers JSON og **64 MiB + 1 byte** ble også avvist.

Kodegjennomgangen bekrefter fast kildekatalog, rotbundet import, 16 MiB payloadgrense, pinnet og begrenset dekomprimering, XML uten DTD-/entitets-/nettoppslag, lukkede ZIP-medlemsnavn og en snever OOXML-grammatikk. Originaleksportens filnavn kommer fra validerte digester; innkommende kildebaner brukes ikke som outputnavn. Ingen ny nettinnhenter er lagt til.

### Offline og publisering

Den offentlige `analyse.perioderegister_r2`-CLI-en ble kjørt fra en egen tom arbeidsmappe, med kopiert frosset input og ikke-eksisterende originalrot. `socket.create_connection`, `socket.socket.connect/connect_ex` og `sqlite3.connect` var blokkert i prosessen. CLI-en åpnet 429, skrev nye JSON-/Excel-filer og eksporterte originalene. De lukkede filene ble deretter gjenlest i samme sperrede prosess og var like. **187 eksporterte rådigester** ble rehashet mot index, med riktige byteantall. 429 hadde null valgte monetære hendelser og beholdt 67/25/7. `offline-cli.json` bevarer faktisk stdout og exitkode 0.

Eksisterende JSON- og Excel-filer med sentinelinnhold ble bevart. Begge skrivere ble også prøvd med en lokal, kontrollert publiseringsrace: først etter validert temporærfil ble et konkurrerende mål opprettet. Publisering ga FileExistsError og bevarte det konkurrerende sentinelinnholdet. Originaleksport avviste en eksisterende outputkatalog og bevarte innholdet. Dette underbygger de enkelte filenes atomiske publisering og vern mot overskriving; det hevdes ingen ekstra transaksjon over hele filparet.

### Offisiell innlesning, schema 5 og B5

Fire **egne friske** lokale 368-forløp ble kjørt etter henholdsvis manglende, feilet, korrupt og semantisk motstridende tillegg. De brukte offentlig registrering/råbevaring, offentlig tolkning og analyse-CLI samt faktisk Excel-gjenlesing gjennom den uendrede ordinære kontrollhjelperen. Ingen historisk Excel var nødvendig som input.

Hver database ga **222 observasjoner / 74 hendelser**, schema **5**, identisk seedet B5-register og gammel `round='uavklart'`. Råoriginalen ble bevart. Den faktisk skrevne 700/1-trioen var **304 351 000 / 6 324 000 / 310 675 000**. `ordinary.json` og de fire lokale `ordinary-v2-*`-mappene binder resultatene.

Første auditforsøk brukte feil datasettstreng `audit` til `begin_source_attempt` og ble avvist med «Ukjent datasett» før ordinærflyten. Dette var en feil i auditens egen oppstart, ikke et produktfunn. Skriptet er bevart som `ordinary-first-attempt.py`; alle fire tellende forsøk brukte støttet `prove` og nye `ordinary-v2-*`-mapper. Ingen tidligere database eller logg ble overskrevet.

## Bevis og reproduksjon

Auditens kontrollrot er `.local/security-56`. Skriptene er `audit.py`, `old-boundary.py`, `offline.py`, `ordinary.py` og `bind.py`. `artifact-manifest.json` binder deres faktiske byte, kopierte innfiler, egne negative filer, nye eksporter og isolerte databaser. Små resultat-/kandidatfiler og skriptkopier er bevart sammen med rapporten. Kandidatens ti kodehashinger og alle brukte inputkopier ble kontrollert uendret etter hovedkjøringen.

Runtime: `C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`, med `PYTHONPATH` satt til absolutt checkoutrot og `../p1-perioderegister/.local/python`. Ingen avhengighet ble installert eller oppgradert. Ny reproduksjon må bruke en ny tom kontrollrot og tilsvarende endret `OUT`; eksisterende auditfiler skal beholdes.

## Bevisgrenser

Dette er lokale defensive fil-/integritetskontroller og kodegjennomgang. Native Excel, ny visuell rendering, live kildeinnhenting, reell datautsending/kodeutnyttelse og drift er ikke prøvd. Auditten gjør ingen ny faglig vurdering av fullmaktsbruk, årsdekning, årsbalanse eller kontokontinuitet.

Fullsuite, Ruff/format/mypy og alle eldre kompatibilitetsfiler ble ikke kjørt på nytt av auditor. Byggerens logger og den avgrensede kontrollhjelperrettingen er lest, og produkt-/testkode samt gammel CI er kontrollert mot fast kandidat. Full Linux-CI er en egen påfølgende leveringsport; denne auditten hevder ikke at den er kjørt eller at #56 er flettet. R2/K3/P1s eldre manifestbindinger og leveringsstatus er bevart.
