# Reproduksjon og kontrollgrense

Kjørt med Python 3.12.14 og lxml 6.1.1 på Windows. Kontroller er utført på
faktiske filer i kandidaten. Engangshjelpere/netthenting ligger lokalt under
`.local/k3/`, utenfor den sporede leveransen; ingen kjørbar fil eller
produktkode inngår. Dokumentasjonens kodeblokker er reproduksjonskommandoer.

`source-manifest.json` binder hver bevart ny HTTP-respons til tapsfri gzip,
ukomprimert og komprimert SHA-256/byte, transportmetadata og fullstendighets-
status. Ufullstendige svar og feilkropp er ekte mottatte byte, ikke ønsket
dokumenthash. `reused-sources.json` binder tidligere filer med repo-relative
stier og hasher; deres originale transportmetadata/avledningsoppskrifter
beholdes i de opprinnelige manifestene. Forsknings-JSON er avledede ledgere,
ikke kildeoriginaler eller produktfiler.

Den lokale `.gitattributes`-filen setter `-text` for denne forskningsmappen,
slik at hashfestet JSON/transportmetadata beholder faktiske linjeskift i nye
Windows-/Linux-checkouter. Dette er filattributter, ingen kjørbar konfigurasjon.

## Råbyte, gzip, metadata og gjenbruk

Kjør fra repoets rot. Python kan være prosjektets eget miljø; bunten er brukt
her for lxml og kildekontroller. Kommandoen skriver ikke til originalene.

```powershell
$k3Python = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
@'
import gzip, hashlib, json, pathlib
root = pathlib.Path.cwd()
base = root / 'docs/research/k3-arsinventar-50'
digest = lambda b: hashlib.sha256(b).hexdigest()
sources = json.loads((base/'source-manifest.json').read_text('utf-8'))['sources']
for item in sources:
    packed = (base/item['archive']).read_bytes()
    raw = gzip.decompress(packed)
    assert len(raw) == item['bytes']
    assert digest(raw) == item['sha256']
    assert digest(packed) == item['archive_sha256']
    assert digest((base/item['metadata']).read_bytes()) == item['metadata_sha256']
for item in json.loads((base/'reused-sources.json').read_text('utf-8')):
    data = (root/item['path']).read_bytes()
    assert len(data) == item['bytes'] and digest(data) == item['sha256']
    if 'uncompressed_sha256' in item:
        assert digest(gzip.decompress(data)) == item['uncompressed_sha256']
for path in base.rglob('*.json'):
    json.loads(path.read_text('utf-8'))
print('Kildebyte, transportmetadata, gjenbruk og JSON bestått')
'@ | & $k3Python -
```

## Lokatorer og opptelling

HTML dekodes uttrykkelig som UTF-8 før lxml. En DOM-lokator er knyttet til
én representasjons hash. `table-locators.json` har tabellhode, avsenderattributt,
rad-XPath og råceller. Hver rad kan gjenleses slik:

```powershell
@'
import gzip, hashlib, json, pathlib
from lxml import html
base = pathlib.Path('docs/research/k3-arsinventar-50')
sources = {x['id']: x for x in json.loads((base/'source-manifest.json').read_text('utf-8'))['sources']}
normalize = lambda text: ' '.join(text.split())
count = 0
for block in json.loads((base/'table-locators.json').read_text('utf-8')):
    source = sources[block['source']]
    raw = gzip.decompress((base/source['archive']).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == block['body_sha256']
    document = html.fromstring(raw.decode('utf-8'))
    for row in block['rows']:
        matches = document.xpath(row['xpath'])
        assert len(matches) == 1
        cells = [normalize(x.text_content()) for x in matches[0].xpath('./td|./th')]
        assert cells == row['cells']
        count += 1
print(count, 'tabellrader gjenlest')
'@ | & $k3Python -
```

Vedtaksregisteret er avledet fra begge komplette foreldresvar, uten typefilter.
For hvert `s:stortingsvedtak` hentes ID, sak, dato, nummer, tittel og
`stortingsvedtak_type/id`. `stortingsvedtak_tekst` HTML-dekodes av XML-parseren,
HTML-parses, og tekstinnholdet søkes etter `1429`, `Riksantikvar`, `kulturminne`,
`kulturmiljø` uten hensyn til store/små bokstaver. Ingen treff er en åpen
screeningstatus, ikke en eksklusjonsregel. 25 konkrete kandidater vurderes
med årsinnledning, lokale kontoblokker og fullmaktsinnhold.

For saksindeksene undersøkes metadatafeltene med mønsteret
`1429|Riksantikvar|kulturminn|kulturmiljø|statsbudsjettet 2024|nasjonalbudsjett 2024|Prop. 36 S`,
uten hensyn til store/små bokstaver. Dette gir 67 kandidatposter, og
representerer et lokaliseringstrinn. Det er ingen generell nettinnhenter
eller ny produksjonsklassifisering.

`source-comparison.json` omberegnes ved å parse gamle og nye komplette
vedtaksresponser og sammenligne ID-sett samt lxml C14N for hvert komplett
vedtaksobjekt. 2 183 objekter er uendret; responskonvoluttene har egne hasher.
For 447 er bare hovedteksten sammenholdt etter uttrykkelig UTF-8-dekoding
og kollaps av mellomrom. Dette er ikke full HTML-byteidentitet eller bevis
for en tidligere urettet dokumentversjon.

`voting-evidence.json` kontrolleres mot faktiske `sak_votering`,
`voteringsvedtak` og `voteringsforslag` med navngitte ID-er/XPaths.
Forslagets HTML-blokker har egne lokatorer. Sju avviste forslag, en vedtatt
RNB-tilråding og de separate341-/346-/210-/211-koblingene må stemme før
utfall kan presenteres. Dato, sesjon, budsjettår og forslagsrolle er ulike felt.

## Leveransemanifest

`verification.json` oppsummerer de faktisk utførte kontrollene og feilfrie
tellingene; den påstår ikke produktaksept eller full semantisk årsdekning.
`delivery-manifest.json` har SHA-256 og byte for alle filer i denne
forskningsmappen unntatt seg selv, samt den endrede `docs/kildefunn.md`.
Manifestet er en leveransekontroll, ikke hash for kilden som en forskningsledger
omtaler. Schema `k3-delivery-manifest-2` erklærer følgende bytegrunnlag:

- Standard `exact-file-bytes`: alle forskningsfiler, inkludert råoriginaler,
  gzip, metadata og kontrollrapporter, hasher faktiske byte uten normalisering.
  Forskningsmappens `-text`-attributt gjør disse identiske i Git og checkout.
- Eneste unntak er `docs/kildefunn.md`, representasjon `utf-8-lf`: valider UTF-8
  uten BOM, erstatt hvert CRLF med LF og avvis eventuelle gjenværende CR.
  Ingen annen endring er tillatt. Dette er Git-blobens LF-byte; en lokal
  Windows-checkout kan ha CRLF. Filens innhold og råkildene endres ikke.
- `bytes`, `sha256` og `total_bytes` gjelder de erklærte representasjonene,
  ikke nødvendigvis summen av checkoutens filstørrelser.

Kontroller arbeidsfilene med tom `$k3Revision`. Etter at en ny kandidat er
fryst i Git, sett variabelen til dens fulle commit-ID: samme kontroll leser da
**faktiske Git-blobbyte** med `git show` i Python, uten PowerShell-tekstkoding.
Den krever også at manifestets egne byte er identiske med valgt Git-revisjon.
Et arbeidsmanifest før commit er ingen kontroll av en senere commit.

```powershell
$k3Revision = '' # sett full fast commit-ID for kontroll av Git-leveransen
@'
import hashlib, json, pathlib, subprocess, sys
root = pathlib.Path.cwd()
base = root / 'docs/research/k3-arsinventar-50'
manifest_path = base / 'delivery-manifest.json'
manifest_raw = manifest_path.read_bytes()
manifest = json.loads(manifest_raw)
assert manifest['schema'] == 'k3-delivery-manifest-2'
assert manifest['byte_representation'] == {
    'default': 'exact-file-bytes',
    'overrides': {'docs/kildefunn.md': 'utf-8-lf'},
}
revision = sys.argv[1] if len(sys.argv) > 1 else ''
def representation(path, data):
    if path == 'docs/kildefunn.md':
        data.decode('utf-8')
        assert not data.startswith(b'\xef\xbb\xbf')
        data = data.replace(b'\r\n', b'\n')
        assert b'\r' not in data
    return data
paths = {p.relative_to(root).as_posix() for p in base.rglob('*')
         if p.is_file() and p != manifest_path} | {'docs/kildefunn.md'}
assert len(manifest['files']) == len(paths) == manifest['file_count']
assert {item['path'] for item in manifest['files']} == paths
assert sum(item['bytes'] for item in manifest['files']) == manifest['total_bytes']
if revision:
    assert subprocess.check_output(['git', 'show',
        f'{revision}:{manifest_path.relative_to(root).as_posix()}']) == manifest_raw
for item in manifest['files']:
    path = item['path']
    data = representation(path, (root/path).read_bytes())
    assert len(data) == item['bytes']
    assert hashlib.sha256(data).hexdigest() == item['sha256'], path
    if revision:
        blob = subprocess.check_output(['git', 'show', f'{revision}:{path}'])
        assert blob == data, path
print(manifest['file_count'], 'manifestposter bestått; Git:', revision or 'ikke valgt')
'@ | & $k3Python - $k3Revision
```

Etter dokumentendringer må manifestet genereres på nytt med denne regelen
før fast review. Den uavhengige kontrollen av opprinnelig kandidat og den
målrettede F1-etterkontrollen er skilt i [faktakontrollen](faktakontroll.md).
Ingen produkttestsuite er kjørt av byggeren for denne rene kildeleveransen.
Orkestratoren fører PR-/CI-/mergestatus og eventuell kontroll av en ny fast
kandidat separat. Ingen kontroll her gir faglig godkjenning av en årsbalanse.
