# Integrasjon av T5s kontrollhjelpere

29. oktober 2026. Fire nye reviewhjelpere er gjort klare for hele repositoryets
Ruff- og formatkontroll. Produktkode, tester, skriver, primærkilder,
guardprofiler, coredokumenter og leveransemanifest er byteidentiske med
arbeidsflaten ved starten av dette steget. Den ferdige lokale P2-rettingen
og dens tre leveransemanifestbindinger består. Valgfri Standards-P3 er urørt.

## Eksakte originaler og historiske bindinger

Før første hjelperendring ble de fire filene kopiert med råbyte, uten
linjeskiftkonvertering, til samme mappe med `.original`-suffiks.
Arkivnavnene slutter ikke på `.py`, og inngår derfor ikke i Ruff-skanningen.
[original-helper-map.json](original-helper-map.json) fører opprinnelig sti,
arkivsti, byteantall, SHA-256 og Git-blob-SHA-1.

| Hjelper under `reviews/` | Originalbyte | Original SHA-256 |
| --- | ---: | --- |
| `security/artifact_checks.py` | 3398 | `6787c8917149b207201596afed940deb75e6d5abf92af300b0315ad45a69d761` |
| `security/probes.py` | 22848 | `381eb401386728d046e412a19fd7d8c8c14a25ea0ee7cb732050468305ba2e7a` |
| `security/verify_outcomes.py` | 5516 | `ab28d3df593e8d7111144ed268394e732afe32a20b441d29f34e3d945babe675` |
| `standards/controls.py` | 4194 | `3278c7877fda6895fcd0c887d139bb08adca975983a9d94b7ac7cdfd8c1f80cb` |

[baseline-files.json](baseline-files.json) bandt 1270 eksisterende filer før
endringen. [preservation.json](comparison/preservation.json) bekrefter at 1266
fortsatt er byteidentiske på samme sti, og at de fire hjelperoriginalene er
byteidentiske på sine arkivstier. Dette bevarer alle gamle reviewrapporter,
ledgere, logger, bilder og security-fix-filer.

De **47** bindingene i security-fix/preserved-before.json etterprøves fortsatt:
de fire hjelperstiene slås opp i det nye pathkartet og verifiseres mot
`.original`; de øvrige 43 verifiseres på opprinnelig sti. Alle **18**
filbindingene i security-fix/manifest.json stemmer fortsatt direkte.
Begge gamle manifestfiler er uendret. **Historiske security-fix-manifestbindinger
gjaldt før dette integrasjonssteget**; de er ikke omskrevet til å attestere
de formatterte hjelperbytene på de gamle stiene.

## Hva som ble endret

Ruff rettet tre I001-importblokker; format endret de samme fire filene som
den historiske formatloggen oppga. Seks lange tekstkonstanter ble delt i
tilstøtende Python-strengliteraler uten å endre de ferdige tekstverdiene.
Ellers gjelder endringene mellomrom, linjebryting, parenteser og oppsett.
Ingen kontrollbetingelse, terskel, feilfangst, forventet verdi eller
løkkebinding ble endret. Ingen B023-/late-binding-retting var nødvendig.

[AST-sammenligningen](comparison/ast-comparison.json) viser identisk AST,
uten kildeposisjoner, for `artifact_checks.py` og `standards/controls.py`.
`probes.py` og `verify_outcomes.py` har **ikke** identisk AST:

- I probes er kombinerte `from analyse`, `from innlesning.visningspilot`
  og `from analyse.omtale` delt til separate importsetninger. Samme navn og
  aliaser beholdes, i samme relative rekkefølge.
- I verify_outcomes flyttes `from openpyxl import load_workbook` foran
  de lokale analyse-/innlesningsimportene, fortsatt inne i `main` etter
  ref-/arbeidsflatekontrollen.

Etter uttrykkelig oppdeling av fleraliasimporter og sortering av sammenhengende
importblokker er AST lik også for disse to. Dette beviser at de øvrige
AST-delene og importbindingene er like; det er ingen generell påstand om
at endret importrekkefølge alltid er uten sidevirkning. Faktisk før/etter-replay
dekker den konkrete forskjellen. De fire `.diff`-filene og
[helper-diffs.json](helper-diffs.json) fører hele tekstendringen.

## Samme mål i før/etter-kjøring

Begge hjelpervariantene ble kjørt mot samme isolerte eksport av historisk
d465-kandidat, laget med `git archive`, i `.local/control-integration/target`.
Denne kandidaten har det kjente aksepterte temaangrepet. P2-rettingen fra
arbeidsflaten ble **ikke** kopiert til målet. [target.json](replay/target.json)
binder refs, tre, arkivhash, faktisk mål-leser og faktisk arbeidsflate-leser:

- Isolert d465-leser: `bd0fe777cb4b9f569f6c42a0f24bc5eec2ff040c36c78ef741ef8357ede2fafd`.
- Bevart lokal P2-leser: `3f2a902567e1408ffb01fef625b38e98e334896b89979cdd6661caf565d4177e`.

Git brukte eksplisitt arbeidsrot, eksisterende objektlager, privat indekskopi
og `GIT_OPTIONAL_LOCKS=0`. Ingen staging eller commit ble gjort.
Kandidatens sporede målinnhold var rent før og etter kjøringen; kildeindeksens
hash og P2-leserens hash var uendret. Originale resultater ble aldri brukt
som outputmål. Rå replayledgere og prosesslogger ligger bare i `replay/`;
faktiske store prøvefiler ligger i den nye `.local/control-integration`-mappen.

| Kontroll, før og etter | Faktisk utfall |
| --- | --- |
| artifact_checks | 35 manifestbindinger, åtte strenge JSON-filer og åtte PNG-konvolutter; alle bestått |
| standards/controls | 1181 av 1183 gamle Git-blobber uendret, to additive kontekstfiler og 35 manifestbindinger; bestått |
| security/probes | 70 prober, 69 bestått og ett forventet akseptert `theme_integrity` på gammel kandidat, i begge varianter |
| security/verify_outcomes | 70/69 og samme ene temaaksept; 25 råpayloads, kald offline-prøve, 123/6/2 og lang bokstavelig tekst bekreftet i begge varianter |

Alle åtte prosesser returnerte 0. Kjøretidene var henholdsvis 2,500/2,593,
2,078/2,125, 86,718/82,391 og 13,079/12,828 sekunder før/etter.
[executions.json](replay/executions.json) fører eksakte kommandoer,
hjelperhasher, returverdier og tider. Alle sammenlignede kontrollutfall og
øvrige ledgerfelter er like etter de presise metadataunntakene nedenfor.

Dette er en regresjonskontroll av hjelperendringene. Den opprinnelige
`security/results.json` inneholder historiske harnessverdier som senere
ble etterkontrollert i `results-final.json`. Begge er bevart uendret.
Replay bruker den bevarte siste skriptversjonen og skriver egne ledgere;
den hevder ikke å gjenskape alle tidligere mellomtilstander.

## Presise sammenligningsunntak

[replay-comparison.json](comparison/replay-comparison.json) og de normaliserte
ledgere fører alle faktiske før-/etterverdier. Bare dette normaliseres eller
utelates fra ledgerlikheten:

1. `probes[61].detail` (`no_clobber_original_directory`): egen outputrot blir
   `<ARTIFACTS>`. `probes[63].detail` (`atomic_no_clobber_race`): samme rotnormalisering
   og det tilfeldig genererte `tmp*.json`-filnavnet. Feilkode, feiltekst,
   målnavn og alle bestått-/bevaringsresultater består. Dette gjelder både
   probeledgeren og den etterkontrollerte ledgeren; ingen annen detaljtekst
   endret seg ved normaliseringen.
2. I etterkontrollert ledger: `artifacts[1]`, `[2]` og `[4]`, henholdsvis
   clean.xlsx, accepted-theme-white.xlsx og literal-long.xlsx, får
   `sha256` og `bytes` holdt utenfor likhetstesten. Rå hash/størrelse er
   bevart for begge varianter. Størrelsene var 2887280/2887284,
   2887254/2887258 og 2892983/2892979 byte. Begge JSON-artefaktenes hash
   og størrelse er beholdt i sammenligningen og er like.
3. Prosessloggenes absolutte kommando-/outputstier, hjelperhash og kjøretid
   er kjøringsmetadata og inngår ikke i ledgerlikheten. Alle åtte
   returverdiene er eksplisitt kontrollert til 0.

XLSX-unntaket er begrunnet med faktisk ZIP-medlemskontroll, ikke antatt
binær likhet: [generated-xlsx-comparison.json](comparison/generated-xlsx-comparison.json)
viser at alle medlemsnavn, rekkefølge og utpakkede payloadbyte er like,
med eneste payloadunntak tekstinnholdet i `dcterms:created` og
`dcterms:modified` i `docProps/core.xml`. Disse klokkeslettene og medlemmenes
ZIP-datoer er dokumentert før/etter. Andre kontrollerte ZIP-egenskaper er
like. Komprimeringen av de ulike klokkeslettene gir de nevnte små
størrelsesforskjellene. Kapsel, tema, stiler, ark, relasjoner og faktiske
kontrollutfall er ikke utelatt fra sammenligningen.

## Hele statiske kontroller og grense

[ruff-all.log](ruff-all.log), [format-all.log](format-all.log),
[mypy.log](mypy.log) og [static-results.json](static-results.json) gjelder
hele arbeidsflaten med integrerte hjelpere og de nye replayhjelperne:
`ruff check .`, `ruff format --check .` og konfigurert `mypy`.
Alle bestod; formatkontrollen omfatter 179 filer og mypy 85 kildefiler.
Historiske security-fix-logger er ikke endret.

De 38 T5-testene er ikke gjentatt: ingen produkt-/testforutsetning er endret
i dette steget, og den tidligere P2-kjøringen er bevart. Ingen fullsuite,
full leveranseprøve, ny primærkildekontroll eller ny rendering er utført.
Ingen ny uavhengig sikkerhetsgodkjenning av P2-arbeidsflaten følger av
replay på d465. Orkestrator må fryse en ny kandidat og bestille relevante
uavhengige porter før publisering. Ingen GitHub-mutasjon, staging, commit,
publisering, full Linux-CI eller merge inngår.

## Reproduksjon

Begge nye hjelpeprogrammer og de fire integrerte hjelperne bruker eksplisitt
rot/kandidat/base. Tilgjengelige publiserte refs med tilsvarende kandidat-/basetre
kan brukes; d465 er dokumentasjon av denne kjøringen, ikke en hardkodet
utilgjengelig ref i programmene. Historisk replay krever treet med den
opprinnelige temaaksepten som audit-hjelperne forventer. Nye outputnavn kreves:

```powershell
python docs/research/proposisjon16-62/reviews/integration/replay_helpers.py --root . --candidate GAMMEL_KANDIDAT --base BASE --workspace .local/t5-helper-replay-ny --output docs/research/proposisjon16-62/reviews/integration/replay-ny
python docs/research/proposisjon16-62/reviews/integration/compare_evidence.py --root . --candidate GAMMEL_KANDIDAT --base BASE --replay docs/research/proposisjon16-62/reviews/integration/replay-ny --output docs/research/proposisjon16-62/reviews/integration/comparison-ny
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

Denne kjøringen brukte bundled Python og `PYTHONPATH` fra
`work/c06-99235/.local/python-tools`. De eksakte absolutte kommandoene ligger
i kjøringsmetadata. [manifest.json](manifest.json) binder integrasjonsbevisene
separat og endrer ingen gammel leveranse- eller security-fix-manifestfil.
