# Reproduser P2 fra bevarte kilder og faktiske filer

Fra checkout med Python 3.12 og requirements-dev.txt. Dette arbeidet brukte
den bundlete Python-runtime med P1s allerede installerte pinnede avhengigheter;
ingen installasjon eller oppgradering ble gjort. `PYTHONPATH` skal være
absolutt ved offlineprøven fra tom arbeidsmappe.

```powershell
$p2Python = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = (Resolve-Path '../p1-perioderegister/.local/python').Path
& $p2Python -m pytest tests/test_perioderegister_r2.py tests/test_perioderegister.py tests/test_fleraarspilot.py -q --basetemp=.local/p2-targeted-ny
& $p2Python -m ops.perioderegister_r2_proeve --output .local/p2-acceptance-ny `
  --previous-root ../.. `
  --legacy-b6 ../../outputs/t4-48-3f856d8/compatibility/B6/accept-b6.xlsx
& $p2Python -m ops.perioderegister_r2_guards `
  --source .local/p2-acceptance-ny/both.xlsx --output .local/p2-guards-ny
```

Velg alltid nye kontrollrøtter og outputnavn. Kontrollverktøyets
`--resume-after` gjenopptar bare etter en uttrykkelig ferdig fase og krever
at tidligere `both.json` og `progress.json` finnes. En avbrutt eller feilende
fase regnes ikke som bestått. Rett en kontrollhjelper før gjenopptak og bevar
feilloggen; ikke overskriv opprinnelige kilder eller tidligere leveranser.

Verktøyet skriver/lukker/gjenleser konto-/dokument-/navigasjonspar. 26
syntetiske negative par får nye konsistente DAG-ID-er og en ny bok med den
nøyaktig forgiftede kapselen. `inspect_excel` må først returnere samme JSON
før offentlig JSON-/Excel-leser avviser semantikken. Avvisningsgrunnen
lagres per filtype. Egne presentasjons- og ZIP/XML-/ressursprøver supplerer.

Offentlig frisk import kan bruke én autentisk gammel T1-kapsel:

```powershell
& $p2Python -c "import gzip,pathlib; pathlib.Path('.local/p2-t1-ny.json').write_bytes(gzip.decompress(pathlib.Path('tests/fixtures/t2/authentic-t1.json.gz').read_bytes()))"
& $p2Python -m analyse.perioderegister_r2 --rot . --t1 .local/p2-t1-ny.json `
  --aar 2024 --konto 1429/1 --konto 1429/22 `
  --json .local/p2-frisk-ny.json --excel .local/p2-frisk-ny.xlsx
```

Frosset input velger det nye formatet eksplisitt gjennom den nye modulen.
Det krever ingen kildeimport, database, originalrot eller nett:

```powershell
& $p2Python -m analyse.perioderegister_r2 `
  --frosset .local/p2-acceptance-ny/both.json --rot .local/finnes-ikke `
  --dokument vedtak429 --json .local/p2-fullmakt-ny.json `
  --excel .local/p2-fullmakt-ny.xlsx --originaler .local/p2-originaler-ny
```

Akseptverktøyet kjører denne offentlige CLI-grensen fra en egen tom mappe,
med `socket.create_connection`, `socket.socket.connect/connect_ex` og
`sqlite3.connect` sperret. Resultatet gjenleses deretter i samme sperrede
prosess. Eksporterte originaler og index verifiseres mot kapslens hasher.

Gamle filer leses fra hashkontrollerte kopier med gamle lesere. Reproduser
med faktisk tidligere leveranse under `--previous-root/outputs`, aldri en
ny fil som etterpå betegnes som gammel. Kontrollene bruker uendrede
`old_pair`, `_compatibility`, `verify_legacy_b6` og `_ordinary`. Fire ulike
tilleggsfeil etterfølges av fire egne ordinære 368-databaser med B5-seed,
råbevaring, CLI-tolkning/analyse og faktisk Excel-gjenlesing.

```powershell
& $p2Python -m ruff check .
& $p2Python -m ruff format --check .
& $p2Python -m mypy
& $p2Python -m pytest -vv --durations=20 --basetemp=.local/p2-full-suite-ny
```

Full lokal suite kjøres én gang etter de målrettede portene. Hele Linux-CI
med 90-minuttersgrense skal senere kjøres av orkestratoren på publisert
kandidat. Ingen testfilter, skip, timeoutendring eller `continue-on-error`
innføres i workflowen.

Read-only rendering bruker artifact-tool etter at openpyxl har lukket og
gjenlest eksporten. Det er ingen alternativ produktforfatter eller native
Excel-aksept:

```powershell
$p2Node = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
$env:BUDSJETT_NODE_MODULES = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'
& $p2Node ops/render_perioderegister_r2.mjs .local/p2-acceptance-ny/both.xlsx .local/p2-render-both-ny
& $p2Node ops/render_perioderegister_r2.mjs .local/p2-acceptance-ny/empty.xlsx .local/p2-render-empty-ny
```

`candidate-code.json` oppgir representasjon og SHA-256 per kjørbar fil.
`delivery-manifest.json` binder leverte kontroll-/dokumentfiler med faktisk
bytehash; de to endrede kontekstpekerne bindes uttrykkelig som UTF-8/LF.
Gamle R2/K3/P1-manifester eller originale kontrollresultater oppdateres ikke.

De to bevarte supplerende kontrollene kan kjøres direkte som Python-kilde.
Velg nye resultatnavn. Hashprøven kjøres først etter at alle 26 negative
par er ferdig skrevet; den bruker ingen semantisk leser for de forgiftede
filene, men kontrollerer deres faktiske nye og gamle DAG-selvhasher og
referanser separat fra avvisningsporten.

```powershell
$env:PYTHONPATH = (Resolve-Path '.').Path + [IO.Path]::PathSeparator + (Resolve-Path '../p1-perioderegister/.local/python').Path
& $p2Python docs/research/perioderegister-r2-56/hash-probe.txt `
  --root .local/p2-acceptance-ny --output .local/p2-hash-probe-ny.json
& $p2Python docs/research/perioderegister-r2-56/reuse-probe.txt `
  --new .local/p2-acceptance-ny/both.json --output .local/p2-physical-reuse-ny.json
& $p2Python -m ops.perioderegister_r2_bindings `
  --new .local/p2-acceptance-ny/both.json --previous-root ../.. `
  --output .local/p2-compatibility-bindings-ny.json
```
