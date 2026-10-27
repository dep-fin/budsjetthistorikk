# Overlevering T3/#46

Byggerens lokale leveranse fra base `c1cb156d50fb986794e2af8b20a131209e4707a7`,
tre `ae70d77b07662bb0e01276237c8d802d98e00117`, i isolert checkout
`work/t3-forlop` på `codex/t3-2024-forlop`. Ingen staging, commit, push, egen
review/audit eller merge er utført av byggeren. Orkestratoren fryser hele
kandidaten og gjør de uavhengige portene, PR, CI og allerede autorisert merge.
Foreldrene #37/#32 og drift #10 forblir åpne.

Lokale porter er bestått: **1118 tester, to eksisterende Windows-
rettighetsskips, 1512,57 s**; alle 46 T3-tester bestått. Ruff check/format
(118 filer), mypy (67 kildefiler), lokale lenker og full manifestkontroll er
grønne. T3s andel i JUnit er 153,345 s inkludert fixturetid. Ingen tester,
strenge kontrollregler eller CI-utvalg er redusert; 30-minuttersrammen og
parserversjonslogging er beholdt. Faktisk Linux-CI gjenstår hos orkestratoren.

## Finn leveranse og kontroll

Sluttartefaktene ligger i **`work/t3-delivery/20261027-builder-04/`** i dette
checkoutet. Tidligere `builder-01`–`builder-03` er bevarte byggetilstander,
avgrenset i [TDD-journalen](tdd-journal.md), og er ikke sluttkandidatens bevis.
`manifest.json` har faktiske filhasher, alle nye par, serialiserte forekomster,
negative filer, fire offentlige kjerne-CLI-forløp og gamle kompatibilitetsfiler.
`source-audit.json` har byteoppskrifter/foreldre og den gamle 857-kontrollrollen.
Begge journalene arkiveres varig sammen med `verification.json` her i repoet.
Ingen avgjørende kildefunn eller kontrollresultater finnes bare i ignorert work.

[Kontrakten](../../forlopspilot.md), [resultat og grenser](README.md),
[20-punkts akseptledger](aksept.md), kilde-/filjournaler og previewbilder gir
inngangen for en ny økt. Faktiske kodefilhasher og LF-normaliserte hasher oppgis
hver for seg der Windows-CRLF er ulik Git-LF. Originalbyte har egne råhasher;
de skal aldri normaliseres for å få et kontrolltreff.

## Kjør kontrollen på denne verten

Python3.12.14, repoets pinnede pakker og bundlet Node fra
`load_workspace_dependencies` ble brukt. Lokal pakkekatalog er bare en
kontrollressurs; den er ingen produkt- eller CI-avhengighet.

```powershell
$env:PYTHONPATH='C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a/work/spec-verify-deps'
$t3Python='C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $t3Python -m pytest tests/test_forlopspilot.py -q --durations=12 --basetemp work/t3-test-ny
& $t3Python -m ruff check .
& $t3Python -m ruff format --check .
& $t3Python -m mypy
& $t3Python -m pytest -vv --durations=20 --basetemp work/t3-full-ny
```

Fra fersk vert: Python3.12 og `pip install -r requirements-dev.txt`.
Hele Linux-workflowen og dens 30-minuttersramme/parserversjonslogging er bevart.
Windows er lokal kontroll, ikke påstått kjørt Linux-CI eller native Excel.

Full autentisk kilde-/filprøve, med gamle lokale originaler når tilgjengelig:

```powershell
python -m ops.forlopspilot_proeve --output work/t3-delivery/ny --previous-root C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk --legacy-b6 C:/Users/marti/Documents/Codex/2026-10-20/fortsett-med-6-i-depmartin-budsjetthistorikk/work/b6/work/accept-b6.xlsx
node ops/render_forlopspilot.mjs work/t3-delivery/ny/both.xlsx work/t3-delivery/ny/render-both
node ops/render_forlopspilot.mjs work/t3-delivery/ny/empty.xlsx work/t3-delivery/ny/render-empty empty
```

Ops-prøven trenger bare repoets kilder/ekte T1-arkiv når de to valgfrie gamle
banene utelates. `BUDSJETT_NODE_MODULES` kan peke til den bundlede pakkemappen
dersom Node ligger et annet sted. Ikke installer eller endre repoavhengigheter
for rendering. Bruk nye fil-/katalognavn, også ved gjentakelse.

## Filansvar og API

- `innlesning/forlopspilot_model.py` og `innlesning/forlopspilot.py`: egen
  regel, begrensede registre, råbevaring, eksakte oppskrifter, strukturering og
  rekonstruksjon. Kan kjøres uten analyse. Ingen T2-/315-original kreves.
- `analyse/forlopspilot.py`: validert gammel T1, ID-union i minnet,
  konto-/års- og dokumentvalg/retur, avgrenset lokal regning, streng JSON og
  eksplisitt modul-CLI. `import_basis`, `build_report`, `open_document`,
  `open_accounts`, `go_back`, `read_json` og `calculate_path` er testgrensene.
- `analyse/forlopspilot_excel.py`: egen T3-skriver/leser etter T2-profilen,
  fem hovedfaner, full global kontroll, én offlinekapsel og kontroll av faktisk
  synlig presentasjon. `export_pair`, `read_excel` og `export_originals`.
- `tests/test_forlopspilot.py`, `ops/forlopspilot_proeve.py` og
  `ops/render_forlopspilot.mjs`: høye akseptgrenser, reproduserbare fil-/kjerne-
  og kompatibilitetsprøver, rendering av allerede lagrede bøker.
- `docs/forlopspilot.md`, denne rapportmappen og små kontekstpekere i
  AGENTS/krav/pilotplan/datakontrakt/kildefunn; `.gitattributes` bevarer journalbyte.

Gamle produktmoduler, schema5, B5, ID-er, parser-/tolkningsbetydning,
`legacy_html`, standardvalg, kilder og arkivfixtures er urørt. Nye T3-regler
har egne navn; 210s 18 T1-felt er ikke kopiert til den nye basisen.

## Bevisgrenser

857s gamle 554e-fullrespons mangler i det tilgjengelige grunnlaget. Bare
gammel fixture/sidevogn og dens byteidentiske objekt mot ny 66aa er kontrollert.
Selvstendig gammel frozen-v1-rapport-JSON er fortsatt ikke tilgjengelig;
ekte gammel B6-bok og uendrede innebygde B6-kjerner prøves separat. Gamle A/B-
og T2-kopier er faktiske tidligere leveranser, ikke omgenererte layoutprøver.
Én gammel B-fil er en tidligere merket syntetisk forslagsprøve; den er ingen
positiv K1-fasit. Native Excel er ikke kjørt.

Ingen fullårsdekning, godkjent årsbalanse, faglig kontrollavgjørelse,
kontokontinuitet, historisk produksjonsimport eller drift er levert. Hele
341/857-inventaret er bevart, men bare de fem nye 1429-feltene er strukturert.
Andre poster, herunder /60-beløp, kan ikke tolkes som null fordi utvalgstelleren
er null. Ukjent/dekningshull består også i tomme filer.

## Anbefalt neste økt etter bekreftet merge

Anbefal T4s smale, separate årsforløp: 201/40034038s to bevarte 2025-nivåer,
med ukjent kontinuitet. K2 må avklares før positiv kontinuitet og K3 før positiv
helårsdekning. T4 er ikke bestilt eller bygget i denne leveransen.

> Fortsett fra fersk main etter bekreftet T3/#46-merge i depmartin/budsjetthistorikk.
> Les AGENTS, #37 og siste T3-overlevering, kontraktene og konto-år/testmatrisen.
> Undersøk og legg frem ett konkret T4-snitt: 1429/1 og /22 i 2024 og opprinnelig
> 2025-vedtak 201/40034038 som separate årsforløp med synlig ukjent kontinuitet.
> Bruk originale byte og bevar gamle ID-er, én kompatibilitetskapsel og samme
> kildegrunnlag i begge innganger/faktisk gjenlest JSON/Excel. Ingen automatisk
> kontinuitet, årsbalansegodkjenning, full årsdekning eller drift. #10 åpen.
> Dette bestiller undersøkelse og ticketforslag; bygg/publiser/merge først ved
> mitt uttrykkelige mandat til akkurat T4.
