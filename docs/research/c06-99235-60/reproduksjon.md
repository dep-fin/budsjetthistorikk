# Reproduksjon, byteformer og kontrollgrenser

Kjør fra repoets rot med Python 3.12, lxml 6.1.3 og pypdf 6.10.0. De pinnede
verktøyene finnes i checkoutens ignorerte `.local/python-tools`; de er
installert fra uendret `requirements-dev.txt`. Ingen produktdatabase eller
nettjeneste kreves av offlinekontrollen.

```powershell
$c06Python = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = (Resolve-Path '.local/python-tools').Path
$env:PYTHONDONTWRITEBYTECODE = '1'
& $c06Python docs/research/c06-99235-60/test_acquire.py
& $c06Python docs/research/c06-99235-60/verify.py
```

`verify.py` leser originaler og alle manifester. Den rekonstruerer SHA-256,
størrelser, komplette HTTP-hopp, vertsgrenser, rekkefølgen kontrakt→forsøk,
XML/HTML-/PDF-konvolutter, alle nøyaktige lokatorer/tekster, 130 bildehasher,
visuelle sidereferanser, OCR-/sidejournalbindinger, fire C14N-sammenligninger,
tekstsammenligning i behandlingsleddene, datoavklaringen, kandidatfravær i
historisk 67-liste og bevaring av 1 070 basefiler. Den skiller dette fra faglig
årsaksept, feilfriOCR og uavhengig kildekontroll.

Etter at orkestratoren har laget en kandidatcommit kan dens faktiske Git-
blobbyte prøves med `verify.py <full-kandidat-SHA>`. Det krever at alle
manifestførte filer finnes i kandidaten. Uten argument kontrolleres
arbeidsfilene; det er ingen påstand om commit/publisering.

## Originaler og avledet tekst

Alle nye forskningsfiler har `-text` gjennom lokal `.gitattributes`.
Rå entity-byte endres ikke. HTTP transfer-framing, TLS og wire-headerbyte
er ikke bevart. `urllib` leser entity-byte uten automatisk Content-Encoding-
dekomprimering; Accept-Encoding er identity. Alle observerte svar er
kontrollert for dette. Lokal gzip har `mtime=0`; arkivhash og dekomprimert
entity-hash er forskjellige, eksplisitte felt.

Hvert redirect-hopp har egen entity-capture og original responsmetadata.
Den eneste nye transportfeilen er DNS-feilen før noe HTTP-svar; den har
ingen konstruert tom original. Samme identifikator kan ikke overskrives.
Alle forsøk finnes i [source-manifest.json](source-manifest.json).

Den nye [acquire.py](acquire.py) bruker eksplisitt engangshenting:

```powershell
& $c06Python docs/research/c06-99235-60/acquire.py NY-UNIK-ID 'https://data.stortinget.no/eksport/sak?sakid=99235'
```

En ny kjøring er en ny kildeobservasjon og inngår ikke automatisk i denne
frosne leveransen. Eksakte HTTPS-verter er data.stortinget.no,
www.stortinget.no og www.regjeringen.no. Andre scheme/verter/porter og
credentials avvises før nett. Relative redirectmål løses og valideres før
neste forespørsel. Automatisk redirectfølging er deaktivert. Maksimalt åtte
redirects og 80 MiB per body; socket-timeout 55 sekunder. Ingen samlet
wall-clock-frist eller generell uovervåket innhentingstjeneste påstås.

Saks-APIets gamle http-/protokollrelative dokumentlenker beholdes i kilden.
Ved henting er de eksplisitt oversatt til HTTPS på samme avtalte vert;
den faktisk forespurte URL-en og hver videre redirect står i metadata.

HTML avledes fra UTF-8-dekodet kildesvar og lxml HTML; XML bruker
`resolve_entities=False,no_network=True`. `itertext` joines og Unicode-
whitespace kollapses. Originalenes mellomrom/linjeskift bevares i råbyte.
XML-belegg kan i tillegg parse ett navngitt indreHTML-felt. Hvert belegg
har egen hash, absolutt XPath, navnerom og eventuell indre feltlokator.
Visuelle belegg er egne manuelle observasjoner/parafraser og har ikke
en påstått eksakt maskintranskripsjon.

De gamle kildene gjenbrukes ved referanse. 853–856 er sammenlignet som
hele XML-objekter med lxml C14N uten kommentarer fra begge autentiske
sesjonsoriginaler. Ulike HTTP-konvolutter og responsdatoer beholdes; det
påstås ingen ny HTTP-observasjon av dem. Gamle K3-delforsøk og 500-siden
for referatet endres ikke eller brukes som fraværsbevis.

## Hele egne vedlegg og OCR

FullPDF er den autoritative råbevaringen av 130 vedleggsbilder. Den leses
fra gzip; det lagres ingen ekstra full dekomprimert PDF per visning.
Reproduser alle innlagte JPEG-er lokalt slik:

```powershell
& $c06Python docs/research/c06-99235-60/extract_appendices.py --images .local/c06-images
```

`pypdf6.10.0 page.images[].data` brukes. Navn, PDF-side, bildeindeks,
SHA-256, antall byte og figurordinal kontrolleres mot
[appendix-image-inventory.json](appendix-image-inventory.json).
Dette er avledede lokale bildeuttrekk, ingen ekstra HTTP-originaler eller
påstand om at HTML-JPEG-er har samme byte. OriginalPDF-en bevares uendret.

[OCR-skriptet](ocr-appendices.ps1) ble kjørt i Windows PowerShell 5.1 mot
de lokale bildene med Windows.Media.Ocr, en-US. Det bevarte gzip-materialet
har motor, operativsystemversjon, tidspunkt, full tekst og ordkoordinater
for alle 130 bilder. Ingen andre språkpakker ble installert. OCR kan avvike
ved ny kjøring/annenOS-versjon; derfor hasher sidejournalen den faktisk
bevarte avledningen, ikke en antatt universell OCR-fasit.

Skriptet skriver til valgfri lokal utdatafil. En kjøring med `-File` ble
avvist av maskinens scriptpolicy før OCR; deretter ble den lokale
scriptblokken kjørt med `-Command`, uten å endre system-/brukerpolicy.
Sandboxens WinRT-fillesing ga AccessDenied; godkjent kjøring med ordinær
lokal tilgang fullførte alle 130 bilder. Første `test_acquire.py`-forsøk
traff tilsvarende en utilgjengelig sandbox-tempmappe; prøvene bruker nå
automatisk ryddede midlertidige mapper inne i forskningspakken.
Disse er lokale verktøyforsøk, ingen ekstra HTTP-forsøk.

Visuelle belegg kan kontrolleres ved å åpne de angitte bildeuttrekkene
eller rendre de tilsvarende PDF-sidene med bundlet `pdftoppm`. Byggeren
leste de 18 angitte bildene i originaloppløsning; ingen ny PDF er utgitt og
ingen generell layoutgodkjenning av dokumentet påstås.

## Regenerering og manifesteierskap

`build_evidence.py` kan gjenoppbygge kildemanifest, gjenbruk, 87 belegg,
sidejournal, C14N-/leddsammenligninger og bevaringsmanifest fra de
eksisterende råoriginalene. Den skriver ikke originaler eller produktfiler.
`extract_appendices.py --write-inventory` regenererer bildeinventaret.
Kjør bare disse ved en bevisst ny forskningsrevisjon; ordinær kontroll er
lesebasert `verify.py`.

[preserved-files.json](preserved-files.json) binder alle 1 070 basefiler
utenom AGENTS/kildefunn. Checkout-byte er denne Windows-observasjonen;
Git-blob-ID er den plattformuavhengige bindingen. En del eldreCSV-blobber
har selvCRLF; de sammenlignes rått. Ellers brukes Git clean-filter ved
behov for checkout-linjeskift. Ingen kilde normaliseres eller omskrives.
De to additive pekerne hasher uttrykkelig UTF-8/LF i leveransemanifestet.

[delivery-manifest.json](delivery-manifest.json) omfatter alle byggerfiler,
den administrative issuevurderingen og begge pekere, men ikke seg selv,
`__pycache__` eller senere `reviews/**`. Ingen selvhashsyklus lages.
[verification.json](verification.json) lagres fra en avsluttet kjøring,
manifestet oppdateres etterpå, og kontrollen gjentas lesebasert. Den siste
reproduksjonen får flere manifestkontroller enn en første kjøring uten
manifest; de lagrede resultatene skal leses med denne konteksten.

`local-checks.json` binder de faktisk kjørte lokale kommandoene, klokkeslett,
exitkoder og utdata. Full Linux-CI med alle tester, uavhengig kildekontroll,
Standards/Spec og separat audit utføres av orkestratoren på fast kandidat.
Ingen historisk reviewattest eller pinnedfil skrives om til ny portstatus.

## Additiv kontroll etter de fire faste 9eb-portene

[Reviewoversikten](reviews/README.md) og
[originalmanifestet](reviews/integration/original-review-files.json)
binder de 15 opprinnelige reviewfilene til forskningskandidat
`9eb27cebf7ca4a99aeb30fa32245e41314e0d295`. Rapporter og resultater er
uendrede historiske attester. Standards-helperens originalbyte er bevart
separat; bare formattering og linjedeling av én strenglitteral er gjort.

Kjør [integrasjonskontrollen](reviews/integration/verify_integration.py)
uten utdataargument for en lesebasert kontroll:

```powershell
& $c06Python docs/research/c06-99235-60/reviews/integration/verify_integration.py
```

Den kontrollerer originalreviewhasher, helperens identiske AST og dens
faste Git-kontroller med resultatfilskriving avskåret. Alle resultatfelt
utenom kjøretidspunkt må være identiske med originalresultatet. J02 skal
ha nøyaktig én byteutskifting fra «14 nøkkelsider» til «18 nøkkelsider»,
som skal stemme med de 18 uendrede visuelle sideflaggene. Øvrige kandidatfiler
kontrolleres mot 9eb, med bare de uttrykkelige dokument-/kontrollunntakene.
De tre statusdokumentene må ha bevart originalteksten og bare additive
tillegg. Ingen kildehenting eller ny faglig lesing inngår.

[Integrasjonsresultatet](reviews/integration/result.json) hashbinder
reviewinngangen, originalmanifestet, helperne og de historiske bevisene.
Det utelater seg selv og [nye kontrollutdata](reviews/integration/checks.json)
for å unngå hashsykler. Leveransemanifestets avtalte avgrensning består:
det binder de reviderte byggerfilene, mens `reviews/**` har egen binding.
`verification.json` er ny byggerkontroll av arbeidsfilene; 9eb-versjonen
består i Git og reviewernes opprinnelige resultater er uendret.

Full uavhengig nykandidatattest følger ikke av denne integrasjonen.
Orkestratoren committer og bestiller målrettet etterkontroll før PR/full
Linux-CI og bekreftet merge. Hele testutvalget og 90-minuttersgrensen består.

## Flyttbar gjenoppretting av de historiske kandidatene

Før kontroller som bruker eksakte 9eb-/d241-/9efa-SHA-er i en fersk klon,
følg [historikkpakkens kontroll og import](reviews/history/README.md).
Treidentitet alene leverer ikke de opprinnelige commitobjektene.
Bundleforutsetningene er U1-base 49cc og publisert C06-kandidat 92b;
begge må finnes lokalt. Importen skriver bare den særskilte lokale referansen
`refs/c06-history/candidates`, og endrer ingen arbeidsbranch.

Kjør videre fra den aktuelle klonens rot med en Python 3.12 som har
avhengighetene fra `requirements-dev.txt`. Den eksisterende `$c06Python`
kan erstattes med `(Get-Command python).Source`; ved bruk av lokale
verktøypakker settes `PYTHONPATH` til denne klonens `.local/python-tools`.
Helperne finner selv repoets rot fra sin plassering. Ingen gammel checkout
eller delt Git-objektlager kreves. Den nye dokumentasjonen erstatter ikke
de historiske kjøreobservasjonene ovenfor.
