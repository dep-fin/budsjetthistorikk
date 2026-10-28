# Overlevering T4/#48

Lokal kandidat i `work/t4-fleraar`, branch `codex/t4-fleraar`, base main
`e374bdcad3bf18c44ccd7b813ce67b8f97327ee2`, før-kode-kontrakt
`fc2b62966d65147d5d3d2ad5c0670d4d4912399b`. Byggeren har ikke staged,
committet, pushet, skrevet til GitHub eller gjennomført egen review/audit.
Orkestratoren samler samme fryste kandidat til Standards/Spec og separat
audit, publiserer og følger full Linux-CI til faktisk autorisert merge.
#10/#32/#37 forblir åpne. Ingen neste ticket starter automatisk.

Lokal sluttkontroll: **1155 bestått/to eksisterende Windows-rettighetsskips,
2903,14 s**; alle **37 T4-tester** består. Ruff/format124 og mypy71 er grønne.
Den komplette filprøven ligger i **`work/t4-delivery-final/`**; tidligere
`work/t4-delivery/` er et avbrutt byggeforsøk, ikke sluttbevis. Eget
`work/t4-standalone/` viser 2025 uten T1. Syv kildefiler og én T1-kapsel i
`work/t4-dependency/` gir samme basis/rapport som komplett rot.

**Tidsgrensen krever faktisk Linux-CI:** den lokale fullsuiten tok 48 min
23,14 s mens ops-prøven delvis kjørte samtidig. T4s store matriseprøve tok
903,58 s. Ingen tester eller strenge leserkontroller er redusert, og CI har
fortsatt 40 minutter. [Målegrensen](ci-measurement.md) er uttrykkelig; bygget
er ikke bekreftet grønt innen denne Linux-rammen. Orkestratoren må kontrollere
den faktiske jobben og ved behov rette ytelse med hele aksepten bevart.

## Kandidatens filansvar

- `innlesning/fleraarspilot_model.py` og `innlesning/fleraarspilot.py`:
  separat immutable konvolutt/basis, to 201/2025-nivåer, eksakt oppskrift,
  T3-gjenbruk, helinventar og streng kilderekonstruksjon uten analyseimport.
- `analyse/fleraarspilot.py`: validert T1-kapsel, ID-union i minnet,
  års-/kontogruppering, begge innganger/retur, eksplisitt 2024-regnegrunnlag,
  streng JSON, offentlig opt-in modul-CLI.
- `analyse/fleraarspilot_excel.py`: fem hovedfaner, tilgjengelig kontroll,
  én offlinekapsel, årsbevisste lenker, streng faktisk presentasjonskontroll
  og gjenfinning av originalene. Etablert openpyxl-skriver videreføres.
- `tests/test_fleraarspilot.py`, `ops/fleraarspilot_proeve.py` og
  `ops/render_fleraarspilot.mjs`: autentiske akseptgrenser, fil-/kjerneprøve,
  rehashede negative filer, eldre kompatibilitet og rendering av skrevne bøker.

T4-adapteren rekonstruerer T3-objektene med den uendrede T3-regelen.
De separate JSON-/Excel-leserne binder T4s nye lukkede format uten å endre
gamle leseres betydning. Ingen gammel modul, schema, parser, B5-avgjørelse
eller standardinngang er endret. Nye formater kan leses uten originalrot,
nett, database eller historisk Excel. Innebygd T1 kreves bare for komplett
2024/210-grunnlag; tilgjengelige nye kilder kan bevares selvstendig.

## Reproduksjon på denne verten

Bruk nye output- og basetempnavn. Kildene og fixturearkivet finnes i repoet.
Pakkekatalogen nedenfor er vertens pinnede kontrollressurs, ingen ny
produktavhengighet. Fra annen vert: Python 3.12 og repoets requirements-dev.txt.

```powershell
$env:PYTHONPATH='C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a/work/spec-verify-deps'
$t4Python='C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $t4Python -m ruff check .
& $t4Python -m ruff format --check .
& $t4Python -m mypy
& $t4Python -m pytest -vv --durations=20 --basetemp work/t4-full-ny --junitxml=work/t4-full-ny.xml
& $t4Python -m ops.fleraarspilot_proeve --output work/t4-kontroll-ny --previous-root C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk --legacy-b6 C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/t1-41/work/resume-b6-compat/accept-b6.xlsx
```

Produktets separate kommando for et nytt flerårsuttrekk:

```powershell
python -m analyse.fleraarspilot --rot . --t1 <ekte-T1.json> --aar 2024 --aar 2025 --kapittel 1429 --json <ny.json> --excel <ny.xlsx>
python -m analyse.fleraarspilot --frosset <ny.json> --dokument vedtak201 --json <dok201.json> --excel <dok201.xlsx>
```

Rendering bruker den bundlede Node-/Artifact Tool-installasjonen fra
`load_workspace_dependencies`. Skriptet importerer bare de faktisk skrevne
XLSX-filene og eksporterer ingen ny arbeidsbok:

```powershell
$env:BUDSJETT_NODE_MODULES='C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'
$t4Node='C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
& $t4Node ops/render_fleraarspilot.mjs work/t4-kontroll-ny/both.xlsx work/t4-render-both-ny both
& $t4Node ops/render_fleraarspilot.mjs work/t4-kontroll-ny/document-vedtak201.xlsx work/t4-render-201-ny 201
& $t4Node ops/render_fleraarspilot.mjs work/t4-kontroll-ny/empty-multiyear.xlsx work/t4-render-empty-ny empty
```

Varig `delivery-manifest.json` fører kilde-/filhasher, alle tellerutvalg,
navigasjon/offline, negative par, fire kjerneforløp og ekte eldre kopier.
`verification.json` og kontrolloggene oppgir de endelige lokale portene.
`candidate-code.json` skiller faktiske Windows-byte fra Git-LF.
`rendering.json` og previewbildene dokumenterer visuell kontroll.

Sluttmanifestets SHA-256 er
`2a901e0008816b73a5606c87d332aaf1fb2ec403de388bd95ce89898a1c0e97a`.
Alle 326 manifestfiler og 133 eldre originaler/kopier er avstemt på nytt.
30 utvalgspar, ett offline-CLI-par, fire feil-/tomt-par, 19 rehashede negative
par, åtte presentasjonsfeil, 66 ekte tidligere par og én B6-bok inngår.
Kontrolljournalen avstemmer også faktiske 2025-celler og årsspesifikke lenker
til Forløp rad 11/12, alle 30 renderinger og lokale Markdown-lenkemål.

Native Excel er ikke kjørt. En separat gammel frozen-v1-rapport-JSON og
den gamle 857/554e-fullresponsen er ikke funnet/gjenlest. Positiv kontinuitet,
full årsdekning, faglig årsbalanse og drift er utenfor. Lokal fullsuite er
ingen bekreftelse på Linux-CI; 40-minuttersrammen og hele CI-utvalget består.
