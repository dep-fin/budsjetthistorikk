# O2a: siste retting av metadata og støttemanifest

Rettingen gjelder to defensive funn over `fbef904943961b926041dc3985a108dff9342320`, tree `131ad5083c01b7affd7a6c6179b4361e7e072209`, på `codex/34-omtale-post1`, sammenligningsbase `d74d2cb`. Standards og Spec var bestått på denne tidligere kandidaten. Dette er byggerens lokale retterbevis; samlet review, separat sikkerhetsaudit, PR, CI og merge håndteres av orkestratoren. Ingen individuell review, commit, push eller PR er utført her.

## Rettet atferd

| Funn | Endring | Faktisk filbevis |
| --- | --- | --- |
| P2: XML-kildens dupliserte metadata kunne avvike fra den bevarte sidevognen uten avvik | Hele `metadata_json` dekodes strengt og avstemmes mot den bevarte JSON-sidevognens objekt før kildebindingen verifiseres. Transportfelt, nøstede felt, ekstra/manglende nøkler og talltyper inngår. Råmetadata beholdes; nøkkelrekkefølge og innrykk kan variere. Dupliserte JSON-felt gir synlig avvik. | Det opprinnelige syntetiske metadatafeilparet i `work/audit-final-defensive-results/` avvises nå uten omskriving. Ny eksport fra eksakt samme feilgrunnlag bevarer rådata, viser `vedtaksbinding_motstrid` og har **0 kildeverifiserte relasjoner**, faktisk gjenlest fra JSON og XLSX. |
| P2: `supporting-manifest.json` ble lest to ganger uten bytegrense | Én felles avgrenset JSON-lesing brukes for begge manifestene og støtte-XML-enes metadata. Den leser høyst 1 MiB + én sentinelbyte før størrelseskontroll og JSON-dekoding. Støttemanifestet leses én gang og må være en liste av objekter før radgjennomløp. | Instrumentert autentisk import viser ett `read(1048577)` og uendret grunnlags-ID. Små 979-/980-byte-prøver tester eksakt grense og én byte over. Feil konvolutt, skalar, blandet liste, manglende peker og duplikater beholder sidevognene med synlig `motstrid` i begge gjenleste filer. |

De nye syntetiske feilfilene ligger i `work/omtale-finalaudit-retterbevis/`. Eksakte filhasher, rapport-ID-er, tidligere feilfiler og kjøringsmiljø står i [maskinlesbart retterbevis](retting-finalaudit.json). De to tidligere auditfunnene og auditens opprinnelige maskinresultat beholdes uendret som førbevis.

## TDD og kontroller

Implement-/TDD-filene er fulgt ved den allerede godkjente testgrensen. Metadata-URL-prøven feilet før retting fordi de faktisk gjenleste filene manglet avvik. Manifestprøven stanset gammel `read(size=-1)` før faktisk uavgrenset lesing. Begge prøvene bestod etter hver retting. Utvidede metadataregresjoner dekker URL, hentetid, nøstet header, vedtaks-ID, talltype, responsstørrelse, ekstra og manglende felt, ekvivalent JSON-representasjon og dupliserte felt.

Kommandoene er kjørt fra `C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a`:

```powershell
$env:PYTHONPATH='C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a/work/spec-verify-deps;C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/work/o2a'
$taskPython='C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $taskPython -m pytest -q tests/test_omtale.py --basetemp work/fix3-omtale-final
& $taskPython -m pytest -q tests/test_b2.py tests/test_b6_authentic.py tests/test_b6_cli.py tests/test_b8.py tests/test_b9.py --basetemp work/fix3-compatibility-final
& $taskPython work/fix3-evidence.py
& $taskPython -m ruff check .
& $taskPython -m ruff format --check .
& $taskPython -m mypy
git diff --check
```

Omtalesuiten bestod med **109 passed in 386.82s (0:06:26)**. B2/B6/B8/B9-kompatibilitet bestod med **193 passed in 54.80s**. Ruff check og format bestod for 92 filer, mypy for 51 produktmoduler, og `git diff --check` bestod. 43 lokale fillenker i fire dokumenter er kontrollert. Faktiske sluttresultater og logghasher står i retterbevisets `checks`. Miljøet bruker Python 3.12.14 og pinnet `lxml 6.1.3`, `openpyxl 3.1.5`, `pypdf 6.10.0` fra det oppgitte dependency-målet. Ingen ny fullsuite er kjørt; endelig fullsuite hører til CI. Ingen nye store filer, storallokeringer eller belastningstester er innført. De eksisterende omtaleprøvene er kjørt som regresjon.

## Bevaring og avgrensning

Alle ti tidligere feilfiler avvises med samme dokumenterte feil. De tre autentiske JSON-/Excel-leveransene og deres offline reeksporter er faktisk gjenlest med uendrede rapport-ID-er:

- `299de472b0c01c64983a7816b178991fa5f76e4737bb33e86fb99d9f1f87de13`
- `6021e1344038b6727f76cb09e77e382b4b5b1a48948acd977df0849eba391eb3`
- `22e216820b2b2d17fd43016d8be437a8cbdfaf4cbd8920b871aec0acd55d7143`

Grunnlags-ID er fortsatt `4fb6187784cfe233a89ce5d7180b4d76b3de669125d70c8eead7d70e9a0986a1`. Alle tre har seks kildeverifiserte, ikke faglig godkjente relasjoner og uendrede seks observasjoner/to posthendelser. Tidligere B8-/B9-par er kontrollert uten omskriving. De ti originale støtte-/omtalefilene og alle tidligere leveranse- og feilfiler i retterbeviset er byteidentiske. Eksisterende autentisk leveranse er derfor beholdt; ingen ny datert rapport eller ny leveransekatalog er nødvendig.

Senere B2-responskonvolutter beholder sin etablerte semantikk: opprinnelig revisjon, artefakt og observasjoner gjenbrukes, mens senere responstider og råhash beholdes separat. Den eksisterende prøven gjenleser dette med seks kildeverifiserte relasjoner. Ny uavhengig offisiell vedtaksinnlesning, gamle schemaer/ID-er/kontrollavgjørelser og CLI-standarder er bevart. Ingen ny nettverkskontroll, kildeadapter, Excel-layout eller native Excel-prøve hevdes. #35 bygges ikke; #10 står åpen.
