# Reproduksjon

Kjør fra repoets rot med Python 3.12 og lxml. Ingen produktmodul,
produktdatabase eller nett brukes av offlinekontrollen:

```powershell
$u1Python = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = (Resolve-Path '../p1-perioderegister/.local/python').Path
& $u1Python docs/research/u1-100895-58/verify.py
```

`verify.py` skriver bare resultat til standard output. Den kontrollerer
alle nye transportmetadata/arkiver/responsbyte, gjenbrukte originaler,
163 eksakte belegg, samtlige råceller og monetære trioer i fem
behandlingsrepresentasjoner, fire komplette C14N-vedtak, journalreferanser,
627 bevarte checkout-filer, lokalt endringsomfang og Markdown-lenkemål.
Når leveransemanifestet finnes, kontrolleres dets filhasher også.

`preserved-files.json` binder eksakte checkout-byte og gamle Git-blob-ID-er,
byteantall og hasher på base. Bare de 163 radene uttrykkelig merket
`utf-8-lf` sammenligner deklarerte CRLF-/LF-tekstrepresentasjoner, slik at
kontrollen kan gjentas fra både Windows og Linux. De 464 øvrige radene
bruker eksakte byte. K3/P1/R2/P2s eksisterende forskningsbyte normaliseres aldri.
Produktets Git-diff mot base kontrolleres i tillegg. De to additive
pekerdokumentene AGENTS/kildefunn hasher uttrykkelig UTF-8/LF i manifestet;
alle filer under denne mappen har `-text` og eksakte byte. Uavhengige
reviewfiler og manifestet selv er utenfor byggermanifestet.

`verification.json` lagres fra en faktisk fullført kontroll. Etterpå
beregnes manifestet; kontrollen kjøres igjen uten å overskrive den lagrede
rapporten. Dette hindrer en selvsiterende rapport-/manifesthashsyklus.
En senere endring krever ny manifest-/Git-blobkontroll av den endrede filen.
Orkestratoren må kontrollere Git-blobbyte ved publisering; en lokal kontroll
alene beviser ikke publisering eller merge.

## Henting og representasjoner

`acquire.py` ble brukt for én kilde per kall, med et nytt filnavn per
transportforsøk. Et eksempel på selve innhentingsformen er:

```powershell
& $u1Python docs/research/u1-100895-58/acquire.py case100895-new.xml 'https://data.stortinget.no/eksport/sak?sakid=100895'
```

Eksemplet er **en ny henting**, ikke reproduksjon av den bevarte
observasjonen. Den inngår derfor ikke i offlinekommandoen. Alle faktisk
brukte URL-er, start-/sluttider og status finnes i sidevognene og
`source-manifest.json`; første DNS-feil beholdes uten oppdiktet respons.
Vellykkede kall krevde nettverk utenfor standard shell-sandkasse.

Kildehash gjelder responsens entity-byte fra Python urllib med
`Accept-Encoding: identity`, etter fjerning av HTTP-transferframing, før
tekstdekoding og uten linjeskiftnormalisering. TLS/HTTP-wire-framing er ikke
arkivert. Gzip er tapsfri lagring med separat arkivhash; originalen fås
med `gzip.decompress`. HTML-tekst er avledet ved `itertext`, mellomrom
mellom tekstfragmenter og kollaps av Unicode-whitespace. XML bruker
navnerommet `http://data.stortinget.no`; indre HTML hentes først fra
det eksplisitte XML-feltet. C14N er lxml C14N 1.0, inclusive, uten
kommentarer og uten elementets tail. Ingen normalisering omskriver originalen.

## Kontroller og grenser

Ruff check, Ruff format og mypy kjøres med prosjektets eksisterende
oppsett og tilgjengelig P1-verktøymiljø; faktisk resultat bevares i
`local-checks.json`. Ingen avhengigheter installeres eller oppgraderes.
Full lokal produkttestsuite gjentas ikke for denne additive kunnskaps-
leveransen; orkestratoren kjører hele uendrede Linux-CI før merge.

PDF er bare råbevart og kontrollert for filstart/EOF. Den er ikke
tekst- eller visuelt kontrollert. Offlinekontroll er kilde-/filkontroll,
ikke uavhengig semantisk review eller positiv helårsaksept. Historiske
review-/auditskript med eldre kandidatlåser kjøres ikke som nye attester.
