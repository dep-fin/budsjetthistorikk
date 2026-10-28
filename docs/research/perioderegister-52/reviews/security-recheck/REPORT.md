# Uavhengig lokal sikkerhetsetterkontroll av P1/#52

28. oktober 2026. **Begge tidligere P2-funn er avklart for den faste rettede kandidaten. Ingen nye nødvendige sikkerhetsrettinger ble funnet i denne avgrensede etterkontrollen.**

## Kandidat og omfang

- Arbeidsflate: `C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/p1-perioderegister`.
- Base for samlet P1-leveranse: `29ac220f62b35062fc4203f054e2f757ca795b7c`.
- Tidligere auditert kandidat: `4413a5f21be71ccd2ad5c885560da6bae2e8b885`.
- Fast rettet kandidat: `aec0269b9d6216cc03f9688e62c33a94cfa6cb6c`.
- Tree: `c4c7944dac1510ba428a20440b40f33ebfb8430c`.

AGENTS.md, arbeidsflyten, ansvarsdelingen, P1-kontrakten, P1-kontrollen, hele den tidligere sikkerhetsrapporten og rettingens README/manifest ble lest. Kodediffen `4413a5f..aec0269` ble undersøkt sammen med den gjenbrukte ZIP/XML-/relasjons-/stilkontrollen. De eneste nye produktendringene i denne diffen ligger i P1s Excel-leser; de gamle leserne og `omtale_excel_guard.py` er uendret. Tester, bevisfiler og binærbevarende Git-attributter er egne tillegg.

Dette er en separat defensiv lokal etterkontroll av de to rettingene og deres endrede sikkerhetsforutsetninger. Den erstatter ikke den tidligere samlede Standards/Spec-gjennomgangen eller auditten av hele P1-diffen.

## Avklaring av funnene

### P2-1: eksternt hoveddokument i rotrelasjonen — avklart

`analyse/perioderegister_excel.py:427–498` krever nøyaktig de to tillatte relasjonsfilene, lokale type-/target-par, entydige ikke-tomme ID-er, de tillatte attributtene og de forventede innholdsdeklarasjonene. Rotens `officeDocument` bindes til `xl/workbook.xml`. `TargetMode` inngår ikke i den tillatte grammatikken. Ekstra relasjonsfiler avvises. Kontrollen kalles på linje 523, før innkommende rapportmodell rekonstrueres.

Den eksakte tidligere feilaksepterte filen ble kopiert uten byteendring fra `.local/p1-file-audit/synthetic/` og sendt gjennom offentlig `read_excel()`:

- `container-root-external-office-document.xlsx`
- SHA-256: `929615ec56df384b1113fe57351d26948d8ae52b242fa4bc429537756a981a68`
- Faktisk resultat: `ValueError: P1-Excel har ugyldig lokal pakkrelasjon: _rels/.rels`.

Ytterligere 20 skrevne og lukkede filer ble avvist: eksterne core-/app-/stil-/temareferanser, ekstra ubrukt ekstern relasjon på rot/workbook, eksplisitt `Internal`-modus, manglende/dupliserte ID-er, duplisert relasjon, target-alias med `..`, feil namespace, ekstra worksheet-relasjonsfil samt motstridende, dupliserte, manglende og ekstra innholdsdeklarasjoner. Ingen av disse ble godkjent eller ga en uventet unntakstype.

### P2-2: rå anvendelsesflagg i stiltabellen — avklart

`analyse/perioderegister_excel.py:501–513` registrerer den rekonstruerte skriverens stiler i samme ark-/cellerekkefølge og sammenligner hele rå `styles.xml` kanonisk med den forventede stiltabellen. Sammenligningen bruker dermed også rå `xf`-flagg og andre stildeler som kan gå tapt i openpyxls celleobjekter. Kontrollen kalles på linje 529 før `load_workbook()` på linje 530. Den eksisterende celle-/format-/lenke-/synlighetskontrollen består.

Den andre eksakte tidligere feilaksepterte filen ble også kopiert uten byteendring og gjenlest gjennom offentlig `read_excel()`:

- `container-apply-alignment-zero.xlsx`
- SHA-256: `c10c3fa0f85ee0d501785d0ccfb5ec990c1aaff76d989baf258e8692dc7140a7`
- Faktisk resultat: `ValueError: P1-Excel avviker i rå OOXML-stilprofil`.

Ytterligere 15 skrevne og lukkede råstilvarianter ble avvist: fjernet/nullstilt `applyAlignment`, `applyFont`, `applyFill`, `applyNumberFormat`, `applyBorder`, `applyProtection`, `quotePrefix`, `pivotButton`, anvendelsesflagg på `cellStyleXfs`, skjult navngitt stil og ekstra `dxfs`. Avvisningene skjedde i den nye råstilkontrollen.

En egen positiv fil med omordnet relasjons-/innholdstyperekkefølge og omordnet XML-attributtrekkefølge i stiltabellen ble godkjent med full rapportlikhet. Kontrollen forveksler altså ikke disse rekkefølgeforskjellene med de prøvde semantiske stil-/containerendringene. Den avtalte profilen er fortsatt den lukkede P1-eksporten, med de pinnede bibliotekversjonene.

## Faktisk utførte positive kontroller

Alle fem eksisterende autentiske P1-par ble kopiert, hashkontrollert og gjenlest gjennom offentlig `read_json()` og `read_excel()`: begge poster, fullmakt346, tomt valg, feil år og ukjent indekskandidat. Hvert JSON-/Excel-par ga samme komplette rapport.

- Begge poster beholdt 11 vedtaksfelt og 5 monetære hendelser; de fire øvrige beholdt 0/0.
- Alle fem beholdt globalt 67 sakskandidater, 25 vedtakskandidater og 7 hull, konstant delvis årsdekning og manglende faglig årsbalansegodkjenning.
- Gammel regneport beholdt `166039000` og `29185000`, begge med `avgrenset kontroll`. Dokumentåpning/retur for fullmakt346 og retur til konto-/årsgrunnlaget beholdt samme basis.
- Offentlig P1-CLI ble kjørt fra en faktisk tom arbeidsmappe med kopiert frosset JSON og en ikke-eksisterende originalrot. Den skrev nye JSON-/Excel-filer som deretter ble lukket og gjenlest til samme rapport. Den nye JSON-filen har samme SHA-256 som den kopierte referansen.

Under filkontrollene og i CLI-prosessen var `socket.create_connection`, `socket.socket.connect`, `socket.socket.connect_ex` og `sqlite3.connect` sperret. Ingen slike kall ble registrert. Det ble ikke utført nettverksprøver eller brukt andre eksterne systemer.

## Bevis, bevaring og reproduksjon

`results.jsonl` og `summary.json` dokumenterer **47 registrerte kontroller: 37 forventede ValueError-avvisninger og 10 beståtte positive-/integritetskontroller**, uten feilaksepter eller uventede produktunntak. Dette omfatter de to eksakte opprinnelige filene, 35 nye negative filer, fem positive par, positiv omordning, regning/navigasjon, offline-CLI og kandidat-/bevaringskontroller.

`candidate-before.json` og `candidate-after.json` er identiske. De binder 258 filer: alle sporede Python-/MJS-filer, P1s eksisterende bygge-/review-/rettingsbevis, de brukte originalparene, de to opprinnelige negative filene og utvalgte opprinnelige auditmanifester. HEAD/tree og ren Git-status ble kontrollert før og etter. Kodehashene til rettingen er fortsatt `4451dc7c44b3167f4fc053a8a634745221d5e152a4c712699b56ee7e4b18e4d6` for `analyse/perioderegister_excel.py` og `f1f94510bb09e2f4e02073e6ff7ee548c4920db158a5946b832a29d418d6e71d` for testfilen.

`recheck.py` viser de faktiske prøvene. `recheck.log` og `recheck-initial.py` bevarer første kjøring, som stanset på en TypeError i auditens egen XML-mutator (`lxml.attrib.update` kalt med navngitte argumenter). Den uferdige filen ble ikke godskrevet som produktkontroll. Mutatoren ble rettet, og `--resume` kontrollerte først kandidat-/originalhashene og gjenopptok de resterende prøvene uten å overskrive tidligere logger eller uferdig fil. `resume.log` viser fullføringen. Dette var en harnessfeil, ikke et produktfunn.

Runtime: `C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`, `PYTHONPATH='.;.local/python'`. Full ny reproduksjon skal bruke en ny tom undermappe under `.local/p1-security-recheck/` og endre skriptets `OUT` til den undermappen; eksisterende bevis skal beholdes. `bind.py` kontrollerer de avsluttede resultatene og bevaringen på nytt og skriver `artifact-manifest.json` med byteantall/SHA-256 for alle egne filer, inkludert denne rapporten og de faktiske kopierte/muterte arbeidsbøkene.

## Bevisgrenser

Etterkontrollen kjørte egne målrettede lokale filprøver og offentlig offline-CLI. Den kjørte ikke fullsuite, ny Ruff/format/mypy, Linux-CI, alle gamle kompatibilitetspar, 130 kildeblobber mot Git-basen eller alle tidligere semantiske rehash-prøver på nytt. Deres tidligere resultater gjelder sine oppgitte kandidater; denne rapporten gjør dem ikke om til nye kjøringer. Orkestratorens fulle CI gjenstår som separat port.

Native Excel/rendering, faktisk nettverks-/kodeutnyttelse og driftsaksept er ikke prøvd. Godkjenningen gjelder den avgrensede lokale filgrensen og de to konkrete rettingene. Ingen ny faglig årsdekning, årsbalanse, kontokontinuitet eller monetær fullmaktsvirkning følger av kontrollen. Ingen produktfil, brukt originalfil, Git-/GitHub-tilstand eller annet system ble endret; alle egne skript, resultater og denne sluttrapporten ligger under `.local/p1-security-recheck/`.
