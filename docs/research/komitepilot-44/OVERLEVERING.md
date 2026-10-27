# Overlevering T2/#44

Byggerens lokale leveranse, 27. oktober 2026. Base main `3d76677`, branch
`codex/t2-komiteendring`. Ingen commit, push, egen review/audit eller merge fra
byggeren. Orkestratoren fryser kandidaten og gjennomfører de uavhengige portene,
PR, CI-løkke og eierens allerede autoriserte merge. #10, #32 og #37 beholdes åpne.

## Kjør fra en fersk checkout

Bruk Python3.12 og pinnede `requirements-dev.txt`. Lokal kontroll brukte bundlet
Python3.12.14 og allerede pinnede pakker via `PYTHONPATH` i en separat kontrollrot.
Ingen avhengighets-, database- eller standardvalg er endret.

Den lokale pakkekatalogen er
`C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a/work/spec-verify-deps`.
På denne verten kan kontrollene kjøres slik (fra T2-checkouten):

```powershell
$env:PYTHONPATH='C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a/work/spec-verify-deps'
$t2Python='C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $t2Python -m pytest tests/test_komitepilot.py -q --durations=8 --basetemp work/t2-ny-test
& $t2Python -m ruff check .
& $t2Python -m ruff format --check .
& $t2Python -m mypy
```

Pakkekatalogen er en lokal kontrollressurs, ingen avhengighet i produktet eller i
GitHub CI. En fersk vert installerer repoets pinnede `requirements-dev.txt`.
Bruk et nytt `--basetemp`-navn ved gjentakelse.

```powershell
python -m ops.komitepilot_proeve --output work/t2-ny-kontroll
python -m analyse.komitepilot --rot . --aar 2024 --konto 315/78 --json work/t2-cli/post.json --excel work/t2-cli/post.xlsx
python -m analyse.komitepilot --frosset work/t2-cli/post.json --rot work/ingen-originaler --json work/t2-cli/offline.json --excel work/t2-cli/offline.xlsx --originaler work/t2-cli/originaler
```

Velg nye fil-/katalognavn. Skrivere bruker no-clobber og kontrollerer filene etter
lukking. Første kommando bruker repoets hashfestede T2-originaler og det tapsfrie,
autentiske gamle T1-JSON-testarkivet. Standalone trenger bare T2-originalene.
Frozen-leserne bruker ingen originalrot, database eller nett.

Ekstra reell historisk kontroll ble kjørt med følgende lokale, bevarte kilder:

```powershell
python -m ops.komitepilot_proeve --output work/t2-delivery-readable --previous-root C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk --legacy-b6 C:/Users/marti/Documents/Codex/2026-10-20/fortsett-med-6-i-depmartin-budsjetthistorikk/work/b6/work/accept-b6.xlsx
node ops/render_komitepilot.mjs work/t2-delivery-readable/standalone.xlsx work/t2-render-readable
```

Renderkommandoen bruker bundlet Node fra `load_workspace_dependencies` og
`@oai/artifact-tool` fra runtimepakken. `BUDSJETT_NODE_MODULES` kan peke til den
oppgitte `node_modules`-roten. Den importerer og rendrer den allerede lagrede
XLSX-filen uten å skrive den om. Kontroll av tomt/unionvalg har egne renderbaner.

## Offentlig API og filkontrakt

`innlesning.komitepilot.import_basis(root)` og `validate_basis(basis)` kjører
uten analysepakken. Faste kildeankre, byte-/lokatorkontroll og kildebasert
rekonstruksjon eies der. Ingen B2-UUID-er konstrueres fra hash.

`analyse.komitepilot.import_basis(root,t1_json="")` validerer høyst én gammel
T1-kapsel og klargjør eventuelle råreferanser. `build_report`, `open_document`,
`open_accounts` og `go_back` eier utvalget. `read_json/report_from_json` og
`komitepilot_excel.read_excel` er strenge offline-lesere. `export_pair` skriver
og gjenleser begge filer. `export_originals` gjenfinner kanoniske råbyte ved hash
og de to oppskriftsbundne API-konvoluttene med særskilt avledningsmerking.

`contents(basis)` er en midlertidig sammenstillingsvisning i minnet; den skrives
aldri som en ekstra gammel basis i T2. Nye observasjoner, kilder og tekster har
egne registre, og utvalget refererer til ID-er. T1s leser/sammenligner er uendret;
T2s egen flertallsport krever Ap/Sp/SV- og postvist voteringsbevis.

## Kontrollbevis og bevarte begrensninger

[verification.json](verification.json) binder faktiske manifestfiler, loggfiler,
kode-/kildehash, rapport-/basis-ID-er, forventet/observert aksept og renderbilder.
Ferdige filer ligger i egen ignorert kontrollkatalog; orkestratoren kan kopiere
den til hovedrepoets outputs uten å skrive over eldre leveranser. Tidligere
kontrollkataloger er bevart. Faneanalysen #43 følger kandidaten uendret.

Gjenopptak etter byggeravbruddet er dokumentert i [resumption.json](resumption.json).
De sju registrerte kode-/testfilene og alle 159 leveransefiler stemte med den
bevarte kontrolljournalen. Ny T2-kjøring med bare pakkekatalogen i `PYTHONPATH`
avdekket én prøvefeil: adapterskriptet i en tempmappe fant ikke repoets
`innlesning`-pakke. Prøven starter nå samme skript med Python `-c` fra reporoten,
som den eksisterende T1-prøven. Analyseblokkeringen er fortsatt aktiv. Dette
endrer bare testoppstart, ingen produktfil, kilde eller leveranseartefakt.
Rød logg, rettet enkeltprøve og avsluttende fullsuite bevares i `checks/`.

16 positive JSON-/Excel-par dekker standalone, union, tomt, kapittel, årsunion,
alle seks nye dokumenter, begge navigasjonsretninger, retur og offline. JSON
bevarer nøyaktig samme grunnlag/ID-er mellom valgene. Serialiserte payload- og
observasjonsforekomster telles også fra den faktisk gjenleste Excel-kapselen.
Særskilt merkede faktiske negative JSON/XLSX-filer prøver rehash og falsk visning.
Enhetstester dekker ytterligere rolle/år/enhet/betydning/omfang, kilde/aktør/vote,
sak/lokator/relasjon, ukjent parallellvariant og ZIP/XML/presentasjonsgrenser.

Fire nye, uavhengige testdatabaser synkroniserer autentisk 40034229/368, bevarer
råbyte, tolker og eksporterer ordinær Excel ved manglende, feilet, korrupt eller
motstridende ny tilrådingsadapter. Hver gir 222 beløpsfelt og 74 monetære ledd,
også sammen med tomt T2-utvalg og uten historisk Excel.

Reell kompatibilitet er kontrollert fra hashkontrollerte kopier: to gamle A-par,
seks gamle B-par, to gamle B8/B9-par med innebygd B6-kjerne, ett gammelt T1-par og
én ekte eldre B6-bok. Det er **11 par og én separat bok**, ikke tolv par. Et av
B-parene er en tidligere merket syntetisk forslagsprøve, ikke positiv K1-fasit.
Originalenes SHA er like før/etter. B6-boken har 5 492 observasjoner fra 47 uttrekk
med beløpsrader, i et eksplisitt utvalg på 50 uttrekk. Selvstendig gammel
frozen-v1-rapport-JSON er fortsatt ikke funnet. Det er ingen native Excel-prøve.

Ingen faglig godkjenning, full årsdekning, kontokontinuitet eller drift. K1s
positive parallelle beløpsforslag mangler fortsatt. T3–T6/K1–K3 og generell
fane-/legacyopprydding krever egne mandater. Gamle schema5/B5/B7/frozen-v1/v2,
B8/B9/O2/T1, kildebyte, ID-er og `round='uavklart'` er bevart.
