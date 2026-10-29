# Separat sikkerhetsaudit – C06 / #60

**Sikkerhetsport: klar for denne faste kunnskapskandidaten. Ingen sperrende
sikkerhetsfunn.** U1-auditens S1 er håndtert i den nye hentehjelperen:
vertsgrensen håndheves før første forespørsel og før hvert videre HTTP-hopp.
Ingen retting i pinnede U1-hjelpere eller tidligere forskningspakker er nødvendig.

Kontrollert uavhengig av byggeren, 29. oktober 2026:

- Base: `49cc6e44851cf74e0aaea4eb333419e5598bfd95`.
- Fast kandidat: `9eb27cebf7ca4a99aeb30fa32245e41314e0d295`.
- Hele diffen: 74 vanlige filer, ny forskningspakke og to additive pekere.
  Alle 74 arbeidsfiler er sammenlignet med kandidatens faktiske Git-blobbyte,
  med eksplisitt LF-representasjon bare for AGENTS/kildefunn. Sammenligningen
  er gjentatt etter de kjørte prøvene.
- Alle 1 070 beskyttede basefiler har uendret Git-blob og filmodus i kandidaten.
  Produktkode, produkttester, CI, schema 5/B5, gamle lesere/standardvalg og
  pinnede K3/P1/R2/P2/U1-filer inngår i denne kontrollen.
- Mandat: AGENTS, arbeidsflyt, issue-tracker, lokal kontrakt, U1s S1-rapport
  og live lest [#60 med kommentar](https://github.com/depmartin/budsjetthistorikk/issues/60).
  Auditen gjelder sak 99235/C06, uten produktadopsjon eller ny ticket.

## Funn og rådgivende grenser

Ingen kritiske, høye eller middels alvorlige sikkerhetsfunn er identifisert.
Det er heller ingen ny lav observasjon som krever retting før denne leveransen.

De lokale forskningshjelperne har et bevisst begrenset driftsomfang. Dette
er rådgivende bruksgrenser, ikke sperrende funn:

- [acquire.py:103–111](../../acquire.py#L103) begrenser vanlig lesing til
  80 MiB med høyst én ekstra 65 536-byte blokk før avvisning. Socket-timeout
  er 55 sekunder, og høyst åtte omdirigeringer følges. Det finnes ingen samlet
  tidsfrist; en langsom respons innen hver socket-timeout kan ta lengre tid.
- [extract_appendices.py:17](../../extract_appendices.py#L17),
  [build_evidence.py:37](../../build_evidence.py#L37) og
  [verify.py:46](../../verify.py#L46) dekomprimerer lokale arkiver uten en
  generell applikasjonsgrense. PDF/bildedekoding og WinRT-OCR har heller ingen
  egen prosessisolasjon eller samlet tidsfrist i disse skriptene. De konkrete
  hashbundne arkivene og alle 130 innlagte bilder er kontrollert; dette er
  ingen godkjenning av vilkårlige fremtidige arkiver eller en nettjeneste.
- Manifestene og operatørens lokale utdataargumenter er reviewede lokale
  inndata. `verify`/`build` er ingen sikker innlesningsport for et vilkårlig
  angriperlevert manifest. Ingen HTTP-kropp brukes som manifest, utdataargument
  eller shell-kode i kandidaten. Vernet for et nytt forsøksnavn er kontrollert
  ved sekvensiell bruk og eksklusiv opprettelse av metadata; det er ingen
  garanti mot en lokal angriper som samtidig erstatter filer eller kataloger.

## S1: hver omdirigering kontrolleres før nett

[acquire.py:31–43](../../acquire.py#L31) validerer eksakt HTTPS-hostname,
port 443/standardport, fravær av brukerinfo og fravær av kontrolltegn,
whitespace, backslash og ikke-tomt fragment. Bare `data.stortinget.no`,
`www.stortinget.no` og `www.regjeringen.no` er tillatt.
[Linje 46–56](../../acquire.py#L46) slår av urllibs automatiske
redirectfølging. [Linje 62/92](../../acquire.py#L62) validerer før forespørselen;
[linje 139–145](../../acquire.py#L139) løser og validerer hvert neste mål.

Egne negative prøver dekker 22 ugyldige start-URL-er og 100 redirectmål
fordelt på 301/302/303/307/308: fremmed vert, prefiks-/suffixforveksling,
lokal IP, HTTP/FTP/file, uventet/ugyldig port, credentials, trailing dot,
backslash, fragment og kontrolltegn. Ingen avviste mål utløser neste
forespørsel. En relativ redirect, et tillatt vertsskifte og deretter et
ondsinnet tredje mål prøver grensen gjennom flere ledd. Normalisering av
ledende whitespace i Location kan gi en gyldig URL; det faktisk forespurte
målet oppfyller fortsatt den eksakte grensen.

Fem andre prøver kjører **urllibs faktiske redirect-/HTTPError-stack** med
en falsk HTTPS-transport. De viser at `request_once` ikke følger fremmed
vert automatisk, heller ikke etter en gyldig første redirect. Vanlige
socketforbindelser er eksplisitt blokkert under hele auditkjøringen.

Alle fem virkelig observerte redirecthopp er kontrollert fra de bevarte
Location-headerne til neste hashbundne hopp: to i debattreferatet, ett på
proposisjonsforsiden og to i voteringsreferatet. Samtlige holder seg på
avtalte HTTPS-verter. Fullstendige URL-er/status finnes i
[maskinresultatet](security-results.json). Ingen ny HTTP-henting er gjort.

## Kontroller og faktiske resultater

[security_checks.py](security_checks.py) kjørte **3 776 kontroller, 0 feil**.
[security-results.json](security-results.json) angir fast SHA/base,
kontrollnavn, målinger og observerte redirecthopp. Byggerens uendrede
`verify.py <kandidat-SHA>` består **3 335 kontroller, 0 feil**, bevart i
[builder-verify-current.json](builder-verify-current.json). De ni eksisterende
transporttestene består også; bare midlertidig mappe ble omdirigert til denne
review-mappen. [Faktisk testutdata](builder-transport-tests.txt) er bevart.

| Flate | Kontroll og resultat |
| --- | --- |
| Filstier og overskriving | Ni ugyldige identifikatorer avvises før nett/filskriving. Et brukt forsøksnavn avvises uten endrede byte. Alle 1 320 kontrollerte stifelt er relative og uten traversal/drive/backslash. Alle kandidatfiler er vanlige filer. Kildekontrollerte PDF-bildenavn brukes bare som metadata; en egen `../../outside.jpg`-prøve gir utfil `page-001-0.jpg` innen operatørens utmappe. |
| Originaler og feil | 16 forsøk, 15 komplette sluttsvar og 20 komplette HTTP-responskropper inklusive redirects; én DNS-feil uten fabrikkert responsarkiv. Alle sidevogn-/entity-/arkivbindinger og originalinventaret består. Største body er 25 471 530 byte; høyeste gzip-forhold er 38,0044. HTTP 404/500, manglende Location, feil Content-Length, pre-response-feil, IncompleteRead og bytegrensen er negativt prøvd. Delbyte bevares med feilstatus og `body_complete=false`; HTTP-feil får egen status. CRLF/NUL/UTF-8 bevares uendret. |
| XML/HTML | Begge kandidatparserne bruker `resolve_entities=False,no_network=True`. Intern entitet, ekstern fil-entitet og ekstern HTTPS-entitet forblir uekspandert i egne prøver. HTML avledes som data; ingen JavaScript, bildehenting, XSLT eller XInclude kjøres. XPath kommer fra lokale reviewede skript/belegg. |
| PDF/bilder/OCR | Hele PDF-inventaret er regenerert og stemmer: 144 sider, 130 bilder. Alle 130 JPEG-er er dekodet/kontrollert; hvert bilde er 1 339 × 1 893 piksler, maksimalt 245 283 JPEG-byte. PDF-katalogens OpenAction er `/GoTo` for sidenavigasjon. Pypdf-uttrekket kjører ingen PDF-handlinger. OCR-skriptet leser eksplisitt valgt lokal JPG-mappe med `-LiteralPath`, bruker Windows.Media.Ocr og serialiserer resultatet som JSON; kilde-/OCR-tekst blir aldri kommandoer. Lokal OutputPath er et operatørvalg som kan overskrive utfilen. |
| Avledninger og manifester | Hele `build_evidence.main` er kjørt med utdata fanget i minnet: alle sju genererte artefakter stemmer byte for byte med kandidaten. `refresh_manifest.main` er kjørt med bare den ene manifestskrivingen avskåret; resultatet er byteidentisk med kandidatmanifestet og utelater senere reviews som avtalt. Manipulert metadatahash, entityhash og beleggtekst avvises i tre egne negative prøver. Hashene binder byte, uten påstand om kildeutgiversignatur. |
| Kjøring og rettigheter | Ingen eval/exec, shell-kjøring av fjerntekst, produktdatabase, opplasting eller utsending i kandidatens hjelpere. Subprocess-bruk er argv-basert Git uten `shell=True`. Ref/filnavn fra reviewet lokal kontekst settes ikke inn i en shell-streng. Bygg-/refreshskriptene skriver avledninger i egen pakke; de er dokumentert som bevisste regenereringskommandoer. |
| Hemmeligheter og lenker | Avgrensede sterke mønstre for GitHub-token, AWS-nøkkel, privat nøkkel og Authorization/Bearer ga ingen treff i de 74 kandidatfilene, inklusive dekomprimerte nye arkiver/OCR. De registrerte forespørslene bruker bare User-Agent og Accept-Encoding. Ingen innlogget nettlesersesjon eller cookies videresendes av koden. Ingen aktive/lokale javascript/data/file/vbscript-lenker er funnet i de kontrollerte forfattede Markdown-lenkene. Byggerkontrollen bekrefter også lokale lenkemål. Bevarte primærkildelenker er data og følges ikke automatisk av parserne. |

Auditprobenes egne syntetiske referanser til `evil.example`, lokal
fil-entitet og traversal er testdata i denne mappen, uten nettaktivitet
eller endringer i kildepakken. Ruff og Ruff-format består for auditverktøyet.

## Reproduksjon og begrensninger

Fra checkoutens rot:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = (Resolve-Path '.local/python-tools').Path
& 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' docs/research/c06-99235-60/reviews/security/security_checks.py
```

Prøven bruker Python 3.12.14, lxml 6.1.3, pypdf 6.10.0 og Pillow 12.3.0.
Den leser de auditerte skriptene fra **fast kandidatblob**, bruker de
blobkontrollerte arbeidsfilene som lokale kilder og skriver bare egne
resultater og automatisk ryddede syntetiske prøver under denne mappen.
Andre agenters reviewfiler inngår ikke i auditen. Ingen kandidatfil,
leveransemanifest eller eldre hjelpe-/pinnefil er endret.

HTTPS/TLS/wire-transport er ikke replayet. WinRT-OCR er statisk gjennomgått,
og den bevarte OCR-avledningen er hash-/sidekontrollert; selve motoren er
ikke kjørt på nytt i denne auditen. Dekodede bilder er ingen uavhengig
visuell/faglig kontroll av alle tarifftekster. Ingen generell sårbarhetsskann
av operativsystem eller tredjepartsbiblioteker er gjennomført. Mønstersøket
er ingen uttømmende hemmelighetsdetektor. Selvkonsekvente, senere endrede
filer/manifester er ikke denne kandidaten; ny kandidat krever ny binding.

**Denne sikkerhetsporten er klar.** Rapporten bekrefter ingen PR,
full produkttestsuite, Linux-CI, publisering eller merge. Øvrige uavhengige
porter og faktisk leveringsstatus ligger hos orkestratoren.
