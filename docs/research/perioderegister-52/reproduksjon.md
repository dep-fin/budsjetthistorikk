# Reproduser P1-kontrollen

Kjør fra repoets rot med Python 3.12 og requirements-dev.txt. I Windows-
arbeidsflaten er den medfølgende Python-runtime brukt med avhengigheter
lokalt i .local/python. En mislykket venv-opprettelse skyldtes manglende
ensurepip; bunten er ikke endret. P1s lokale kontrollmiljø er ignorert i Git.

```powershell
$p1Python = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = '.local/python'
& $p1Python -m pip install --target .local/python --upgrade -r requirements-dev.txt
& $p1Python -m pytest tests/test_perioderegister.py -q --basetemp=.local/pytest-p1
& $p1Python -m ops.perioderegister_proeve --output .local/p1-complete `
  --previous-root ../.. `
  --legacy-b6 ../../outputs/t4-48-3f856d8/compatibility/B6/accept-b6.xlsx
```

Den siste kommandoen krever de faktiske tidligere leveransene under
--previous-root/outputs. De regenereres ikke som «gamle» filer. Manglende
gamle originaler skal oppgis som manglende bevis. De nye filene får nye
filnavn; eksisterende filer overskrives ikke.

Frisk import med tidligere autentisk T1-grunnlag:

```powershell
& $p1Python -c "import gzip,pathlib; pathlib.Path('.local/t1.json').write_bytes(gzip.decompress(pathlib.Path('tests/fixtures/t2/authentic-t1.json.gz').read_bytes()))"
& $p1Python -m analyse.perioderegister --rot . --t1 .local/t1.json `
  --aar 2024 --konto 1429/1 --konto 1429/22 `
  --json .local/frisk.json --excel .local/frisk.xlsx
```

--t1 er samme eksplisitte kompatibilitetsinngang som T4. Uten den bevares
tilgjengelig nytt kilde-/registergrunnlag, men 210s gamle beløpsgrunnlag
blir synlig manglende. Ingen ny strukturering av 210 erstatter gamle ID-er.

Frosset P1 trenger ingen originalrot, database eller nett:

```powershell
& $p1Python -m analyse.perioderegister --frosset .local/frisk.json `
  --rot .local/finnes-ikke --dokument vedtak346 `
  --json .local/fullmakt.json --excel .local/fullmakt.xlsx `
  --originaler .local/gjenfunne-originaler
```

Kontrollhjelperen kjører også den offentlige CLI-en fra en tom arbeidsmappe,
med socket/SQLite eksplisitt sperret og en ikke-eksisterende originalrot.
Kildebyte eksporteres én gang per hash; index.json knytter kilde-ID-er,
arkivpayloads, gjenbruksreferanser og representasjonsbevis sammen.

Semantiske negative Excel-filer bygges med konsistente dimensjoner,
filterområder, radhøyder og den eksakte forgiftede P1-kapselen. Den strenge
containerporten må først returnere samme JSON før JSON-/Excel-leserne
avviser kilde-/kontraktbruddet. Resultatene er merket syntetiske.

```powershell
& $p1Python -m ruff check .
& $p1Python -m ruff format --check .
& $p1Python -m mypy
& $p1Python -m pytest -vv --durations=20 --basetemp=.local/full-suite-tmp
$p1Node = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
$env:BUDSJETT_NODE_MODULES = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'
& $p1Node ops/render_perioderegister.mjs .local/p1-complete/both.xlsx .local/render-both-ny
```

De bevarte supplerende prøvene kjøres etter at hovedkontrollen har skrevet
both.json/both.xlsx. De bruker kun det frosne grunnlaget:

```powershell
$env:PYTHONPATH = '.;.local/python'
Copy-Item docs/research/perioderegister-52/navigation-probe.txt .local/navigation_probe.py
Copy-Item docs/research/perioderegister-52/guard-probe.txt .local/guard_probe.py
& $p1Python .local/navigation_probe.py
& $p1Python .local/guard_probe.py
```

Navigasjonsprøven skriver egne faktiske bytte-/returpar for alle de avtalte
tilfellene. Containerprøven lager merkede syntetiske ZIP/XML-/formel-/lenke-
og ressursangrep. De faste lokale utdatafilene må være nye; bruk en fersk
arbeidsflate eller nye uttrykkelige stier ved gjentakelse.

Renderingen leser de lagrede filene og endrer dem ikke. Den er et separat
visningsbevis, ikke native Excel-aksept eller en ny eksportmotor. Fem
hovedfaner og de to tilgjengelige kontrollfanene beholdes.

Den lokale leveransens manifest skiller faktiske bytehasher fra Git-tekst
med LF. De store kontrollfilene ligger i de uttrykkelige .local/-røttene;
manifestet omfatter ikke avbrutte forsøk eller Python-avhengighetene.
Følgende verifiserer alle faktiske filer, fra repoets rot:

```powershell
@'
from pathlib import Path
import hashlib, json
manifest = json.loads(Path('docs/research/perioderegister-52/delivery-manifest.json').read_text(encoding='utf-8'))
for entry in manifest['files']:
    raw = Path(entry['path']).read_bytes()
    assert len(raw) == entry['bytes'], entry['path']
    assert hashlib.sha256(raw).hexdigest() == entry['sha256'], entry['path']
print(len(manifest['files']), 'filer verifisert')
'@ | & $p1Python -
```
