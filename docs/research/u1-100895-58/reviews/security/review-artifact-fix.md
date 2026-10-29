# Rettet reviewartefakt før CI

29. oktober 2026: bare sikkerhetsreviewets eget kontrollskript er rettet.
Forskningskandidaten er fortsatt
`e34b2fae67df6417807109e36eaeadc4c40c89fc`, med base
`59485e6bb6e45dacf348451b380cf6ba3b5d8321`. Ingen commit er laget.

`security_checks.py` er formatert med Ruff. Den lokale funksjonen
`altered` binder nå `data=data, name=name` ved definisjon. Den brukes
fortsatt synkront innen samme løkkerunde. AST-sammenligning bekrefter
at dette er eneste endring i kjørbar struktur; øvrige endringer er
formatering og linjedeling av kommentar/streng. Auditens omfang, funn,
kontroller og observasjoner er uendret. Dette er ingen ny substansiell audit.

## Testattest og filbinding

Det opprinnelige reviewresultatet mot forskningskandidaten var
**775 kontroller, 0 feil**, datert `2026-10-29T14:38:08.176904+00:00`.
Etter rettingen ble skriptet kjørt på nytt mot samme kandidat:
**775 kontroller, 0 feil**, datert `2026-10-29T14:40:42.777138+00:00`.
JSON-sammenligning viser at bare `checked_utc` er endret.
Alle 52 kandidatfiler og 627 beskyttede base-/kandidatblobber består
skriptets kontroller. Byggerens eksisterende attest på 2874 kontroller
er bevart; byggerkontrollen er ikke kjørt på nytt i dette rettingssteget.

SHA-256 gjelder eksakte lokale filbyte:

| Fil | Før retting | Etter retting |
| --- | --- | --- |
| `security_checks.py` | `f96f88b5fd1e3398efa4ed45764ec5af121cbd3d017e0891a55e4787904539a0` | `ccd5bcc7be7383200532c0eb097bf50997871473e584b50c70ce8a11e9c7a5b9` |
| `security-results.json` | `414b9796935c8a47f4d99a47f226b1af3b1f56208d2062c83a4eae2b3604db3f` | `7fbee3cbeef01f6617d8856512f6b76107d703657d46e33843e7a7b7becd83fd` |
| `builder-verify-current.json` | `502b9dc2650b8c559b29242d2554fa743861134cc2b494883f561af45fad7f1e` | Uendret |

## Reproduksjon og grenser

Fra checkoutens rot:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = (Resolve-Path '../p1-perioderegister/.local/python').Path
$auditPython = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $auditPython docs/research/u1-100895-58/reviews/security/security_checks.py
& $auditPython -m ruff check .
& $auditPython -m ruff format --check .
& $auditPython -m mypy
```

Alle kommandoene besto: Ruff-kontroll for hele checkouten, 152 formaterte
Python-filer og mypy uten funn i de 81 konfigurerte kildefilene.
Full produkttestsuite og Linux-CI er ikke kjørt i dette rettingssteget.
Ingen primærkilder er hentet, og ingen forskningsoriginaler,
`acquire.py`, `verify.py`, produktkode eller CI-filer er endret.
