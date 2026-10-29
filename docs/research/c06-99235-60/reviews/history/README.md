# Transportabel kandidat- og reviewhistorikk for C06 / #60

Kontrollert 29. oktober 2026 før merge. Publiseringen av PR #61 gjennom
GitHub-blob/tree/commit bevarte slutt-treet, men ikke den lokale
commithistorikken. En ny, isolert GitHub-henting av bare den publiserte
C06-branchen manglet alle tre lokale kandidatcommitter. Historiske attester
kunne derfor ikke reproduseres fra denne klonen alene.

[candidates.bundle](candidates.bundle) bevarer de eksakte commitobjektene
og bare de eldre objektene som mangler i det publiserte treet.
Ingen historisk rapport, resultatfil eller kandidatbinding er omskrevet.
Dette er en administrativ portabilitetsretting, uten ny faglig lesing.

| Rolle | Commit | Git-tre |
| --- | --- | --- |
| U1-base | `49cc6e44851cf74e0aaea4eb333419e5598bfd95` | `6dcc9a203a895fa4206a8ef9041bdbccb0b9b580` |
| Fire historiske reviewporter | `9eb27cebf7ca4a99aeb30fa32245e41314e0d295` | `60dfabaec4e7c022e30c6a6389a622790fad11f5` |
| Målrettet etterkontroll | `d241ad8f36f70718dbc54d3093c151d301d04f30` | `afd35a9f4bf98c8b2e69bd3373464a9661811b7b` |
| Lokal sluttkandidat | `9efa1f7b67e4ad5b2722b6a6604591af281e4e9c` | `4664149a1cbf6c288b741fa502e162746b032e07` |
| Publisert PR-kandidat | `92b43c2ce7ec350e10639bd0c75540da0d83ee72` | `4664149a1cbf6c288b741fa502e162746b032e07` |

Den lokale kjeden er base → 9eb → d241 → 9efa. Publisert 92b har base
som direkte forelder. Treidentiteten 9efa/92b er bekreftet, men innebærer
ikke commitidentitet eller en ny reviewerattest på 92b.

## Bundle, forutsetninger og oppretting

- Filstørrelse: **22 554 byte**.
- SHA-256: `051ca0279fb61b5ddd3b77a83c09f172c8ac142e1cd2240dfac6fdca2ab7074d`.
- Bundle v2, Git SHA-1-objektformat; 18 pakkede objekter: tre committer,
  ni trær og seks eldre tekstblobber. Største blob er 17 399 byte.
- Uttrykkelige prerequisites: `49cc6e44851cf74e0aaea4eb333419e5598bfd95`
  og `92b43c2ce7ec350e10639bd0c75540da0d83ee72`.
- Annonsert ref: `refs/c06-history/candidates` → 9efa. Dette er ingen
  publisert branch eller endring i en eksisterende arbeidsbranch.
- Pack-delens SHA-256:
  `a6dfa0c03889cffbbcc4d858ceb55fa7a1c10c8f2a75be5d191e806d308ad4ad`.

Første native forsøk med `git bundle create ... codex/c06-99235 ^92b...`
lyktes teknisk, men ga **21 581 042 byte** og tok med den allerede
publiserte PDF-blobben på 19 639 345 byte. Det oppfylte ikke størrelseskravet.
[Det faktiske første forsøket](initial-attempt.json) bevarer kommando,
størrelse, hash og avvik. Den store mellomfilen er erstattet av den lille
bundlen; den er ingen ekstra kildeoriginal.

[create_bundle.py](create_bundle.py) bruker i stedet native Git med både
`^92b...` og `^92b...^{tree}`. Den siste eksklusjonen fjerner objekter som
allerede leveres gjennom det publiserte treet. Git skrev bare ancestry-
grensen 49cc som prerequisite. Helperen legger derfor også 92b til i
bundleheaderens prerequisite-liste, uten å endre én byte av pack-delen.
Dette gjør den ekstra objektforutsetningen eksplisitt ved `git bundle verify`.
Ingen commit, tre eller blob endres eller konstrueres på nytt.

Helperen kontrollerer alle faste trær/foreldre og bruker en avgrenset lokal
administrativ ref. En ny ref opprettes med krav om at den mangler, og
fjernes med krav om uendret verdi i `finally`; en eksisterende identisk
ref beholdes. Ingen branch flyttes. Regenerering er et uttrykkelig
vedlikeholdssteg etter at objektene er tilgjengelige:

```powershell
& $c06Python docs/research/c06-99235-60/reviews/history/create_bundle.py
```

## Kontroll og gjenoppretting fra en vilkårlig klonrot

Bruk Python 3.12 med avhengighetene i `requirements-dev.txt`. Sett
`$c06Python` til denne Python-en, eksempelvis `(Get-Command python).Source`.
Kommandoene nedenfor bruker relative repo-stier. Hvis prerequisite 92b
mangler, hent den fra den publiserte historikken først, for eksempel
`git fetch origin 92b43c2ce7ec350e10639bd0c75540da0d83ee72`.
En ny PR-head og den senere mergen må bevare denne forutsetningen
tilgjengelig i Git-historikken.

```powershell
Set-Location (git rev-parse --show-toplevel)
$c06Bundle = 'docs/research/c06-99235-60/reviews/history/candidates.bundle'
$c06Hash = (Get-FileHash $c06Bundle -Algorithm SHA256).Hash.ToLowerInvariant()
if ($c06Hash -ne '051ca0279fb61b5ddd3b77a83c09f172c8ac142e1cd2240dfac6fdca2ab7074d') {
    throw 'Bundlehash stemmer ikke'
}
git bundle verify $c06Bundle
if ($LASTEXITCODE -ne 0) { throw 'Bundleforutsetning eller filkontroll feilet' }
git fetch --no-tags $c06Bundle 'refs/c06-history/candidates:refs/c06-history/candidates'
if ($LASTEXITCODE -ne 0) { throw 'Historikkimport feilet' }
git fsck --full --no-reflogs
git rev-parse '9eb27cebf7ca4a99aeb30fa32245e41314e0d295^{tree}'
git rev-parse 'd241ad8f36f70718dbc54d3093c151d301d04f30^{tree}'
git rev-parse '9efa1f7b67e4ad5b2722b6a6604591af281e4e9c^{tree}'
```

Sammenlign trærne med tabellen. Importen krever ingen checkout eller
endring av HEAD. Den bruker ikke `--force` og flytter ingen arbeidsbranch.
Bundlen beviser Git-objektidentitet, ikke kildeutgivers signatur eller
uavhengig faglig godkjenning.

Ordinære, lesebaserte kontroller etter import er:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
# Bare ved bruk av lokale verktøypakker:
$env:PYTHONPATH = (Resolve-Path '.local/python-tools').Path
& $c06Python docs/research/c06-99235-60/verify.py
& $c06Python docs/research/c06-99235-60/reviews/integration/verify_integration.py
& $c06Python docs/research/c06-99235-60/test_acquire.py
```

`verify.py <SHA>` krever at manifestførte arbeidsfiler også svarer til
den navngitte kandidaten. Bruk en separat, ren checkout av kandidaten
ved slik kontroll. Nye additive dokumenter er ikke del av 92b eller 9efa.
Integrasjonshelperens nye stdout lister også senere reviewfiler; den
overskriver ikke det historiske `integration/result.json`.

De fire historiske reviewhelperne kan skrive resultater. Følgende blokk
gjelder derfor **bare en separat disponibel klon**, etter bundleimport.
Ingen brukerarbeidsflate brukes. Helperfilene leveres fra 92b; de fantes
ikke i 9eb. Python-kopieringen bevarer deres eksakte Git-blobbyte.
Specs helper krever først avledede bilder i **den nye klonens**
`.local/c06-images`:

```powershell
git checkout --detach 9eb27cebf7ca4a99aeb30fa32245e41314e0d295
@'
from pathlib import Path
import subprocess
published = '92b43c2ce7ec350e10639bd0c75540da0d83ee72'
prefix = 'docs/research/c06-99235-60/reviews/'
for name in ('standards/check_candidate.py', 'source/independent_check.py',
             'spec/verify_spec.py', 'security/security_checks.py'):
    relative = prefix + name
    target = Path(relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(subprocess.check_output(['git', 'show', published + ':' + relative]))
'@ | & $c06Python -
& $c06Python docs/research/c06-99235-60/extract_appendices.py --images .local/c06-images
& $c06Python docs/research/c06-99235-60/reviews/standards/check_candidate.py
& $c06Python docs/research/c06-99235-60/reviews/source/independent_check.py
& $c06Python docs/research/c06-99235-60/reviews/spec/verify_spec.py
& $c06Python docs/research/c06-99235-60/reviews/security/security_checks.py
# Bare i den samme disponible klonen: gjenopprett de publiserte attestfilene.
git checkout --force --detach 92b43c2ce7ec350e10639bd0c75540da0d83ee72
git status --porcelain=v1
```

Dette rekonstruerer de 130 JPEG-ene fra den bevarte PDF-en, uten ny
HTTP-observasjon, OCR, visuell lesing eller endring av bildeinventaret.
Det første ferske Spec-forsøkets manglende bilde og den påfølgende
reproduksjonen er bevart; historiske hjelpere er ikke omskrevet.

## Faktisk fersk-klon-bevis og kontrollgrense

[fresh-proof.json](fresh-proof.json), [commands.json](commands.json) og
[replay-summary.json](replay-summary.json) dokumenterer den utførte
gjenopprettingen. [manifest.json](manifest.json) binder bundle og nye
bevisfiler uten selvhashsyklus.

Den nye klonen startet med `git init` i en ny mappe, deretter en vanlig
GitHub-fetch av kun `refs/heads/codex/c06-99235`, uten shallow-historikk.
FETCH_HEAD var eksakt 92b. Ingen objekter, hardlinks, alternates eller
lokal fetch fra den gamle checkouten ble brukt. Git-objektmiljøvariabler
var ikke satt. Alle tre `git cat-file -e <SHA>^{commit}` feilet med 128
før import. Etter import ble de rå commitbytenes SHA-1 regnet på nytt,
alle tre trær kontrollert og full `git fsck` bestått. Bare den lille
bundlefilen ble tilført Git-objektgrunnlaget.

Python-verktøypakkene ble kopiert separat til den nye klonens ignorerte
`.local/python-tools`; dette var bibliotekfiler, ingen Git-objekter eller
kildedata. Python og versjonene av lxml, pypdf, Pillow, Ruff og mypy er
registrert i kommandobeviset. GitHub-fetchens første DNS-feil i sandbox
og et feilnavnet importforsøk for den ignorerte kommandologgeren er også
bevart. Nett-hentingen lyktes deretter med godkjent ordinær lokal tilgang.

| Utført maskinell reproduksjon i fersk klon | Faktisk resultat |
| --- | --- |
| `verify.py 92b...` på ren publisert checkout | 3 346 kontroller, 0 feil, alle 73 kandidatblobber |
| Lesebasert `reviews/integration/verify_integration.py` | Bestått; 15 originalfiler, identisk helper-AST/-utfall, J02 og 18 sideflagg |
| `test_acquire.py` | Ni offlineprøver bestått |
| Historisk Standards-helper på fast 9eb | 74 kandidatfiler / 1 070 beskyttede basefiler, 0 feil |
| Historisk kildehelper på fast 9eb | 1 786 kontroller, ingen feil; historisk P3 består |
| Historisk Spec-helper på fast 9eb, etter bildeekstraksjon | 50 kontroller; historisk SP1 består |
| Historisk sikkerhetshelper på fast 9eb | 3 776 egne kontroller, 0 feil |
| Ny arbeidsfilkontroll etter dokument-/manifestrettingen | 3 276 kontroller, 0 feil, i den flyttede klonen |
| Ny integrasjonskontroll og transportprøver | Bestått; 15 historiske originalfiler og ni transportprøver |
| Ruff / Ruff format `--check`, uten cache | Bestått på alle 12 Python-filer i C06-pakken |
| Mypy på historikkhelperen og integrasjonshelperen | Bestått, to kildefiler |
| Regenerering av bundle i den ferske klonen | Eksakt samme 22 554 byte og SHA-256; importref beholdt |
| CR-bevisst `git diff --check` | Bestått |

[replay-comparison.json](replay-comparison.json) viser at alle fire
reproduserte resultatobjekter er identiske med de bevarte historiske
resultatene bortsett fra kjøringstidspunkt. Skriptenes manuelle
lesebeskrivelser er historikk; de betyr ikke at visuell lesing er gjort
på nytt. Den disponible klonen er deretter satt tilbake til ren 92b.
Full stdout/stderr fra kommandoene er samlet i `commands.json`.
Sammenligningen bevarer resultatbytenes hasher, tidspunktsforskjellene
og en identisk kanonisk hash etter at bare tidsfeltene er utelatt.
De store, ellers identiske historiske resultatobjektene dupliseres ikke.
Deretter er bare de nye rettingsfilene lagt over i samme klon for
arbeidsfilkontrollene i [final-checks.json](final-checks.json). Denne
administrative arbeidsflaten er ingen ny kandidatcommit. Kommandoutdata
er observasjoner ved kjøretidspunkt; den avsluttende manifestbindingen
skrives etter kontrollene og utelater seg selv.

Maskinell reproduksjon er adskilt fra de opprinnelige attestene.
Originale kilde-, Standards-, Spec- og sikkerhetsrapporter/resultater,
integrasjonsbevis og `final-check.md` består. Kildeoriginaler og pinnede
K3/P1/R2/P2/U1, produkt, tester, CI/90 minutter, schema 5/B5, fem/elleve,
67/66, 60/59, 25 og R1–R7 er uendret. Ingen nye kildefunn, faglig årsaksept,
fullsuite, CI-resultat, GitHub-skriving, staging, commit eller merge inngår.
Ny publisert head må ha faktisk blob-/trekontroll og full uendret CI før merge.
