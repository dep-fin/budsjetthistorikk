# CI-tidsavbrudd og avgrenset retting – #54/PR #55

Dokumentert 29. oktober 2026. R2s første fulle CI ble avbrutt ved jobbens
eksplisitte 60-minuttersgrense. Rettingen endrer bare
`checks.timeout-minutes` fra **60 til 90** i
[workflowen](../../../../.github/workflows/check.yml). Alle kontrollsteg,
hele `python -m pytest -vv --durations=20`, avhengigheter og produktkode
beholdes. Dette er en CI-retting innen det autoriserte leveringsløpet for
#54, uten utvidelse av undersøkelsen eller produktadopsjon.

## Direkte GitHub-bevis

[Run 40772943242](https://github.com/depmartin/budsjetthistorikk/actions/runs/40772943242),
[jobb 123114666144](https://github.com/depmartin/budsjetthistorikk/actions/runs/40772943242/job/123114666144),
har status `completed/cancelled`. Check-APIets eksplisitte failureannotasjon er:

> The job has exceeded the maximum execution time of 1h0m0s

[github-evidence.json](github-evidence.json) bevarer alle fire annotasjoner,
de små jobbresponsene, publisert workflowinnhold og kildehenvisninger.
[log-excerpts.json](log-excerpts.json) har korte, eksakte utdrag med
opprinnelige UTC-tider og linjenumre i de lagrede loggene.

- Publisert head: `a5cb97cb4f825e1ce338f4d698a6b4425e9ed0c1`.
- Faktisk checkout i CI: PR-merge `39eedcbfc099dbb9550f706cf3294a9d58ff3d4d`,
  som fletter head inn i P1-base `6b2441ee5e859d103ab44d78f12d33c374a89171`.
- Lokal kandidat før retting: `a8dff45df3db66e4ef340ee3bc3c312b7a2743f9`,
  samme tre som publisert head: `ea6b68f728f6bd0442c920e55b05e76b68a9de24`.
- Gammel workflowblob: `f04fadd1f24b64171f540a708a9e9f5a72695a43`,
  SHA-256 `b34723f78680f98d644f02593090bbbee7f532444f8766b37ff01ddf3cdbe6e0`
  av 727 UTF-8/LF-byte. Den angir `timeout-minutes: 60`.
- Ruff check, Ruff format og mypy fullførte med `success`.
  1201 tester ble samlet; loggen har 1105 `PASSED` og ingen
  `FAILED`/`ERROR`-teststatus. De siste 96 har ingen registrert sluttstatus.
- Siste beståtte test er `test_false_hidden_or_active_excel_content_is_rejected[hidden-sheet]`,
  92 %, `2026-10-28T22:33:22.6873726Z`. Avbruddet kommer
  `22:33:55.4376710Z`, 32,75 sekunder senere. Første runnerlinje er
  `21:33:38.6416380Z`. Ingen sluttlinje med `1201 passed` finnes.

Maskert fullogg og de opprinnelige API-capturene er lokalt bevart under
ignorert `.local/ci-diagnose/`; komplette logger og miljøutskrifter er ikke
kopiert hit. `local_capture_bindings` i bevisfilen oppgir byte/SHA-256 for
alle disse filene. Logghashene gjelder de lagrede UTF-8-capturene med
GitHubs maskerte verdier erstattet av `<REDACTED>`, ikke uendrede
oppstrømsbyte. API-dataene ble innhentet 29. oktober. Filenes mtime er
merket som filsystemtid; en eksakt HTTP-mottakstid ble ikke registrert.

## Hvorfor 90 minutter

[P1-run 40732500584](https://github.com/depmartin/budsjetthistorikk/actions/runs/40732500584),
jobb 122972242554, bestod alle 1201 tester på **2765,30 sekunder**.
Begge kjøringer viser Ubuntu 26.04.1, image `ubuntu-26.04` versjon
`20261025.179.1`, provisioner `20261021.618`, Python 3.12.15, pytest 8.3.5,
pluggy 1.7.0, lxml 6.1.3 og libxml2 2.14.6, både runtime og compiled.

Fra første testresultat til samme navngitte siste 1105. test brukte R2
3555,023 sekunder mot P1s 2426,445 sekunder, en faktor på 1,465.
En grov skalering av P1s fulle tid gir **67,5 minutter**. Dette er et
anslag, ikke R2s målte sluttid. Fem genererte ZIP-parameter-ID-er varierer
bytevis mellom kjøringene; sammenligningen bygger på faktisk uendret
testkode og den samme navngitte testen, ikke identiske rå-ID-lister.

90 minutter gir margin over anslaget og adresserer den dokumenterte
avbruddsgrensen. Samme suite bestod tidligere innen 60 minutter; den
underliggende årsaken til R2s langsommere kjøring er **uavklart**.
Loggene har ingen ressursprofil. Varierende vertskapasitet er en hypotese.
Node-/Ubuntu-varslene er ikke påvist som årsak; setup-stegene fullførte.
Ingen ytelsesforbedring eller garanti for ny fullføring påstås.

## Filbinding og historikk

[prior-bindings.json](prior-bindings.json) bevarer gamle byte/SHA-256 og
Git-blob-ID-er for de fem endrede sporede filene, samt alle 24 historiske
reviewfiler. Gammelt byggermanifest har SHA-256
`a4c4e56019d467ca392a7f970948cbe6268a5a5aa2fa54bb845ba2ab73589b00`;
det kan hentes fra den oppgitte lokale eller publiserte revisjonen.
Ingen historisk reviewrapport, kontrollkode eller signert resultatfil
omskrives. [Det oppdaterte byggermanifestet](../delivery-manifest.json)
binder fortsatt 59 byggerfiler og oppdateres bare for README,
OVERLEVERING og reproduksjon samt samlet byteantall.

[recovery-manifest.json](recovery-manifest.json) binder alle nye/endrede
filer i denne rettingsrunden, inkludert workflowen, byggermanifestet og
recoveryfiler. Bare manifestet selv er utelatt for å unngå sirkulær hash.
Forskningsfiler hasher eksakte byte; workflowen hasher Git-LF-byte.
K3/P1, råoriginaler, faglige ledgere, produktkode, tester, formater/ID-er,
avhengigheter og fem/elleve-tellerne er uendret.

Følgende historiske utsagn og låser beholdes uttrykkelig for sine gamle
kandidater og skal ikke leses som attester for denne rettingen:

| Historisk fil | Beholdt utsagn eller lås |
| --- | --- |
| `reviews/spec/RAPPORT.md:40` | «produkt/test/CI og fem/elleve er uendret» gjelder `7af3153`. |
| `reviews/final-artifacts/RAPPORT.md:98` | «produkt/test/CI og pinnefiler er uendret» gjelder før recovery. |
| `reviews/final-artifacts/RAPPORT.md:33–34, 105–107` | AST-likhet og gammel `replay_builder_check.py`-kommando gjelder daværende reproduksjon. |
| `reviews/spec/KONTROLLBEVIS.md:18–20` | Påstanden om samme logikk i replay og kodeblokk gjelder gammel kodeblokk. |
| `reviews/spec/replay_builder_check.py:228–248, 265–272` | Gammel tillatt filliste, `.github`-sperre og byggermanifestinventar tillater ikke recovery. |
| `reviews/spec/verify_spec.py:20, 72–112` | Låser HEAD til `7af3153`, 64 filer og uendret `.github`. |
| `reviews/security/audit_checks.py:33, 69–135` | Låser HEAD/filliste til samme kandidat og uendret `.github`. |
| `reviews/standards/review_checks.py:22, 47–59, 111–122` | Låser HEAD/filbyte og kjører gammel kandidatbinding; er ingen recoverykontroll. |
| `reviews/final-artifacts/publication-manifest.json` og historiske reviewresultater | Binder gamle filbyte/kandidater; rehashes ikke for recovery. |
| `../verification.json:50–51` | Gammel scopekontroll og åtte beskyttede trær gjaldt før timeoutunntaket. |

Issuekommentaren fra 28. oktober om «full uendret Linux-CI» er også
historisk: [kommentar 6481221999](https://github.com/depmartin/budsjetthistorikk/issues/54#issuecomment-6481221999).
Den er ikke endret av denne lokale rettingsrunden.

## Kontrollkommandoer og restgrense

Den oppdaterte Python-blokken i [reproduksjon.md](../reproduksjon.md)
kontrollerer kilder, lokatorer, registre og byggermanifest. Den tillater
bare det eksakte timeoutbyttet og sperrer andre `.github`-endringer.
[reproduction-results.json](reproduction-results.json) er rundens nye
offlinekjøring. [local-checks.json](local-checks.json) bevarer kommandoer,
utdata, tid og exitkode for forskningskontroll og Ruff/format/mypy.

Kjør fra reporoten. Bundlet Python brukes for lxml/pypdf; P1s eksisterende
venv med sin lokale modulmappe brukes for Ruff/mypy, uten installasjon:

```powershell
$ciPython = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = (Resolve-Path '../p1-perioderegister/.local/python').Path
& '../p1-perioderegister/.venv/Scripts/python.exe' -m ruff check .
& '../p1-perioderegister/.venv/Scripts/python.exe' -m ruff format --check .
& '../p1-perioderegister/.venv/Scripts/python.exe' -m mypy
```

Reproduksjonsblokken skriver kun til standard output og kan trekkes ut og
kjøres slik, uten å kjøre historiske review-/auditskript:

```powershell
@'
from pathlib import Path
text = Path('docs/research/r2-101000-54/reproduksjon.md').read_text('utf-8')
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'reproduksjon.md:python', 'exec'), {})
'@ | & $ciPython -
```

Recoverymanifestets filhasher og alle historiske reviewbyte kan
kontrolleres uten nett og uten å kjøre reviewlogikk:

```python
import hashlib
import json
from pathlib import Path

root = Path.cwd()
pack = root / "docs/research/r2-101000-54/ci-recovery"
manifest = json.loads((pack / "recovery-manifest.json").read_text("utf-8"))
for row in manifest["files"]:
    data = (root / row["path"]).read_bytes()
    if row["representation"] == "utf-8-lf":
        data = data.replace(b"\r\n", b"\n")
    assert len(data) == row["bytes"], row["path"]
    assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
prior = json.loads((pack / "prior-bindings.json").read_text("utf-8"))
for row in prior["historical_review_files"]:
    data = (root / row["path"]).read_bytes()
    assert len(data) == row["bytes"], row["path"]
    assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
print("Recoverymanifest og historiske reviewbyte stemmer.")
```

Ingen lokal full pytest-duplisering, ny review/audit eller Git-/GitHub-
mutasjon inngår i denne runden. Full CI er fortsatt **ikke bestått for
rettingen**. Orkestratoren må publisere ny head, verifisere faktiske
Git-blober og få alle ordinære kontroller og alle 1201 tester bestått på
den nye headen før merge. Senere testfeil eller et nytt tidsavbrudd må
undersøkes ut fra den nye kjøringens bevis. Ingen testfilter, skip eller
`continue-on-error` er lagt til. #10/#32/#37 og de faglige restgrensene
fra R2-undersøkelsen står åpne.
