# T5: bevaring av kontrollbyte etter Git-normalisering

29. oktober 2026. Avgrenset retting av Standards/Spec-P2 på kandidat
`95ed8e60052d7731bb99386db572ba607c6b36a2`, tre
`225382d23bf776a8c9ee1a81a8d27de90e1b8620`, base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b`.
Dette er nye arbeidsflateregler og utførte isolerte Git-forsøk. Ingen ny
leveransecommit er opprettet, og ingen gammel feilrapport er opphevet.

## Nøyaktig hva som bevares

[raw-bindings.json](raw-bindings.json) fører alle **49** manifestavvik med
sti, opprinnelig manifest, erklært representasjon, byteantall, SHA-256 og
Git-blob-SHA-1 for både manifestets observerte råbyte og kandidatens blob.
Alle 49 er eksakt CRLF→LF; arbeidsfilene stemmer med de gamle manifestene.
Ingen gammel manifesthash, rapport, resultatfil eller `.py.original` er endret.

| Kontroll | Kandidatens Git-blobber før | Råbyte og isolerte nye Git-blobber etter |
| --- | ---: | ---: |
| `security-fix/manifest.json` | 9 avvik av 18 | 0 avvik av 18 |
| `reviews/integration/manifest.json` | 40 avvik av 54 | 0 avvik av 54 |
| Opprinnelig `delivery-manifest.json` | 0 avvik av 35 | 0 avvik av 35 |

Eksempel: `security-fix/tests-38.log` har 724 byte i den gamle Git-bloben,
SHA-256 `afff5668a5849af19705f193aca0e4144016232ff1289da15dc291c32c97e3d5`.
Den observerte, fortsatt uendrede arbeidsfilen og manifestet har 732 byte,
SHA-256 `1c2331f61099931d34685206f969c3fc45820c8253efb6aabeffc8a403c84938`,
Git-blob-ID `d8613cf70e63ac9ca15ff49837ff2061fac7620b`.
Begge faktiske isolerte Git-add-forsøk lagret denne siste representasjonen.

To nye skopede attributtfiler gjelder bare kontrollpakkene:

- [reviews/.gitattributes](../reviews/.gitattributes):
  `** -text whitespace=cr-at-eol`. Bare to historiske `*-probes.log` og
  fire navngitte `integration/*.diff` får i tillegg `-blank-at-eol`.
  Loggene har ekte mellomrom på linjeslutt; diffene har tomme kontekstlinjer
  som består av mellomrom. Ingen generelle whitespace-unntak er lagt til.
- [security-fix/.gitattributes](../security-fix/.gitattributes):
  `** -text whitespace=cr-at-eol`.
- Denne nye mappens [.gitattributes](.gitattributes) bruker samme byteprofil
  for det additive kontrollbeviset.

Reglene gjør at både eksisterende LF og eksisterende CRLF lagres og hentes
uendret. Den gamle rotfilen `.gitattributes` og T5s opprinnelige 35-filers
LF-/råbytekontrakt er urørt. Ingen regel gjelder hele T5-mappen.

Det komplette råinventaret under de to kontrollmappene har **104** allerede
sporede filer. **62** gamle Git-blobber må få tilbake deres observerte råbyte:
de 49 manifestavvikene og **13** øvrige kontrollfiler. De 13 omfatter
integrasjonsmanifestet selv samt gamle kilde-/Spec-/Standards-/sikkerhetsledgere
og prosesslogger. De er ikke nye manifestavvik; også deres originale arbeidsbyte
bevares. Alle 62 har fullstendige før-/etterbindinger i `raw-bindings.json`.

## Faktisk Git-filter og checkout

[git-filter-results.json](git-filter-results.json) dokumenterer følgende:

- `git hash-object --path=STI STI` på hver av de 49 filene med
  `core.autocrlf=true` og `false`: **98 av 98** svar er manifestets rå blob-ID.
- To helt isolerte Git-repositorier fikk samme innhold, reglene og faktisk
  `git add --renormalize`, ett med hver `core.autocrlf`-verdi. Begge ble
  committet bare i sine egne objektlagre under `.local/byte-preservation`.
  De faktiske blobene stemmer med alle 18/54/35 manifestbindingene, og trærne
  er identiske. Prospektiv `git diff --cached --check` består.
- Fire nye utsjekkinger kombinerer begge add-valg med `autocrlf=true/eol=crlf`
  og `autocrlf=false/eol=lf`. **110 filer** er byteidentiske i hver:
  104 gamle kontrollfiler, tre allerede foreliggende sluttreviewrapporter og
  tre nye attributtfiler. Ingen CR-byte tapes eller legges til i disse filene.
  Alle 35 opprinnelige leveransebindinger består med sin erklærte representasjon.

Forsøkene brukte Windows-Git 2.55.0 og ferske, separat initialiserte
repositorier med lesetilgang til eksisterende objekter via Git-alternates.
Lokal `git clone` traff en sandboxfeil i Git-for-Windows' `sh.exe`; initialisering
med eksplisitt alternativt objektlager unngikk dette. Dette beviser faktiske
Git-filtre og nye checkouter, ikke nettverkskloning eller en utført Linux-kjøring.
De isolerte forsøkscommitenes ID-er er bevismetadata, ikke leveransekandidater.

## Det konkrete replayet og den historiske arbeidsrepresentasjonen

`compare_evidence.py` sammenligner **1270 historiske arbeidsfilbindinger**,
ikke bare kontrollpakkenes 49 manifestavvik. Baselinefilen sier eksplisitt
«Actual raw working-file bytes before helper integration, including local
P2 fix; Git index untouched», med historisk head d465. Integrasjonsrapporten
daterer steget til 29. oktober; baseline har ingen mer presis observasjonstid.

Før rettingen avvek **365** av disse bindingene fra Git-blobene. Skopet råbevaring
lukker **21** av dem. De øvrige **344** gjelder historiske CRLF-arbeidsfiler
utenfor de to kontrollmappene, blant annet rotens `.gitattributes`, kode og
eldre dokumentasjon. Å endre deres Git-byte ville bryte bevaringsgrensen.

[replay-representation.json](replay-representation.json) er derfor en
**additiv representasjonsbinding**. Den fører hver av de 344 stiene med lagret
Git-binding, historisk råbinding og én eksakt operasjon: LF→CRLF for alle LF
når input ikke inneholder CR. Utdata må treffe de gamle råbindingene nøyaktig.
Kartets nye observasjonstid står separat fra baselinens historiske tidspunkt.
Gamle hasher er beholdt. Operasjonen brukes bare på en isolert replaykopi;
produkt-/basefiler i repository og arbeidsflate endres ikke.

[replay-results.json](replay-results.json) dokumenterer faktisk før/etter:

1. Ny eksport av 95ed med den historiske d465-replaybindingen stopper igjen
   på `AssertionError: .gitattributes`, returverdi 1.
2. Eksport av det isolerte treet med korrigerte kontrollbyte stopper fortsatt
   samme sted uten representasjonskartet. Råbevaring alene løser ikke en
   historisk arbeidsflaterepresentasjon utenfor skopet.
3. Kartet anvendes på den isolerte kopien. **342** filer materialiseres;
   de to gamle `*_inventory.csv` har allerede historisk CRLF gjennom sine
   eksisterende `eol=crlf`-regler. Alle 344 kontrolleres mot gamle råbindinger.
   Uendret `compare_evidence.py` returnerer **0**, bevarer **1270** bindinger
   med fire opprinnelige hjelpere på arkivstier, og finner like utfall i alle
   fire ledgertyper. Se [replay-preservation.json](replay-preservation.json)
   og [replay-comparison.json](replay-comparison.json).

Den første vellykkede sammenligningen bruker de bevarte historiske XLSX-filene
som `target.json` peker til lokalt. En separat fersk kjøring dokumenteres i
[portable-replay-results.json](portable-replay-results.json): den eksisterende
`replay_helpers.py` regenererer alle åtte original-/integrert-kontroller,
eksporter og målmetadata i en ny isolert mappe. Ingen gamle resultater brukes
som output. Alle åtte prosesser returnerer 0. Samme uendrede sammenligner
returnerer deretter 0 mot disse ferske ledgerne og XLSX-filene.
[portable-replay-comparison.json](portable-replay-comparison.json) fører de
presise sti-/tids-/ZIP-unntakene. Historisk d465 har fortsatt den kjente
temaaksepten; dette er hjelperreplay, ingen ny sikkerhetsaksept av produktet.

## Reproduksjon uten ny leveransehjelper

Bruk en ny klon med publiserte refs som inneholder tilsvarende historisk
d465-tre og base. Kjør fra repositoryroten med nødvendige Python-avhengigheter.
Bruk nye outputnavn. Ingen nye kjørbare filer inngår i leveransen.

```powershell
python docs/research/proposisjon16-62/reviews/integration/replay_helpers.py --root . --candidate d46589cb9e99338e44fc805ee9882006ba657fd0 --base 2f4ee30c9d8074076fc8042e208c4a4b6345db6b --workspace .local/t5-byte-helper-target --output .local/t5-byte-helper-ledgers
git -c core.autocrlf=false archive --format=zip --output=.local/t5-byte-replay.zip HEAD
@'
import hashlib, json
from pathlib import Path
from zipfile import ZipFile
root = Path.cwd()
target = root / '.local/t5-byte-replay-root'
assert not target.exists()
target.mkdir()
with ZipFile(root / '.local/t5-byte-replay.zip') as archive:
    assert all((target / p).resolve().is_relative_to(target) for p in archive.namelist())
    archive.extractall(target)
def bind(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob_sha1': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
doc = target / 'docs/research/proposisjon16-62'
mapping = json.loads((doc / 'byte-preservation/replay-representation.json').read_bytes())
assert bind((doc / 'reviews/integration/baseline-files.json').read_bytes()) == mapping['source_baseline_binding']
for row in mapping['remaining_replay_only_materializations']:
    path = target / row['verified_path']
    raw = path.read_bytes()
    if bind(raw) != row['historical_working_raw']:
        assert bind(raw) == row['stored_git'] and b'\r' not in raw
        path.write_bytes(raw.replace(b'\n', b'\r\n'))
    assert bind(path.read_bytes()) == row['historical_working_raw']
'@ | python -
python docs/research/proposisjon16-62/reviews/integration/compare_evidence.py --root .local/t5-byte-replay-root --candidate d46589cb9e99338e44fc805ee9882006ba657fd0 --base 2f4ee30c9d8074076fc8042e208c4a4b6345db6b --replay .local/t5-byte-helper-ledgers --output .local/t5-byte-helper-comparison
```

## Bevaring og gjenstående porter

[preservation-results.json](preservation-results.json) binder arbeidsflatens
før-/etterkontroll og de avgrensede bevaringsutvalgene. **1181 av 1183** gamle
baseblobber er uendret; de to tidligere additive kontekstfilene er fortsatt de
eneste baseavvikene. Produkt, tester, T5-temavern, gamle pakkprofiler, primærkilder,
autentisk T1-fixture og alle **21 PNG-filer** er urørt. Opprinnelig indeks og
HEAD/tre er uendret. Alle gamle arbeidsfiler og foreliggende sluttreviewer er
byteidentiske. [manifest.json](manifest.json) binder bare dette nye beviset.

Hele Ruff, formatkontroll (**179 filer**) og konfigurert mypy (**85 kildefiler**)
består; [static-results.json](static-results.json) og råloggene fører utfallet.
Ingen ny fullsuite, rendering eller primærkildehenting inngår.

Orkestrator må stage de nye attributtene og eksplisitt gjenbehandle de gamle
kontrollfilene, for eksempel `git add --renormalize --
docs/research/proposisjon16-62/reviews docs/research/proposisjon16-62/security-fix`,
før frysing. Vanlig stat-cache/status alene kan skjule at gamle indeksblobber
fortsatt er LF. Deretter kreves en **ny fast kandidat**, uavhengig kontroll av
de faktiske nye Git-blobene og replay, øvrige relevante porter, publisert-klon-
kontroll, full uendret CI og autorisert merge. Ingen av disse portene attesteres
av isolerte forsøkscommiter eller denne arbeidsflaterettingen.
