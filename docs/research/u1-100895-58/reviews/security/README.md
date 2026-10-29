# Separat sikkerhetsaudit – U1 / #58

**Ingen sperrende sikkerhetsfunn på den faste kandidaten.** Én lav
observasjon gjelder omdirigering ved eventuell ny bruk av hentehjelperen.
De bevarte kildene har ikke denne avvikende vertsbruken. Auditresultatet
gjelder den autoriserte kunnskapsleveransen, uten produktadopsjon eller
nye monetære hendelser.

Kontrollert 29. oktober 2026, uavhengig av byggeren og kildekontrollen:

- Base: `59485e6bb6e45dacf348451b380cf6ba3b5d8321`.
- Kandidat: `e34b2fae67df6417807109e36eaeadc4c40c89fc`.
- Hele kandidatdiffen: 52 filer; to additive dokumentpekere og en ny
  forskningspakke. Ingen endret produktkode, tester eller CI-konfigurasjon.
- Mandat: live lest [#58 med kommentar](https://github.com/depmartin/budsjetthistorikk/issues/58),
  [kontrakten](../../contract.md), AGENTS og arbeidsflyten. Sak 100895/C05,
  Prop. 21 → Innst. 87 → 226–229; søstrene bare nødvendig identitetsomfang.

## Funn og alvorlighet

### S1 – lav / P3: vertsgrensen gjelder første URL, ikke omdirigeringer

[acquire.py linje 20](../../acquire.py#L20) godtar bare tre HTTPS-prefikser,
men [linje 54](../../acquire.py#L54) bruker urllib sin ordinære
omdirigeringshåndtering. Den kan følge en ny URL på en annen vert; hjelperen
arkiverer svaret som `complete` og bevarer den avvikende `final_url`.
En offline negativ kontroll med urllib sin faktiske redirect-konstruksjon
og en simulert respons viser dette uten å kontakte en annen vert.

Dette svekker den uttalte vertsgrensen ved senere gjenbruk av hjelperen.
Ved slik gjenbruk bør hver omdirigering avvises utenfor de avtalte
HTTPS-vertene. Observasjonen sperrer ikke denne kandidaten: alle 15
forespurte og alle 14 endelige kilde-URL-er er kontrollert mot de avtalte
vertene, og ingen brukerautentisering eller produktimport inngår.

Ingen kritiske, høye eller middels alvorlige sikkerhetsfunn er identifisert.

## Utførte kontroller

[security_checks.py](security_checks.py) kjørte **775 kontroller, 0 feil**;
[maskinresultatet](security-results.json) bevarer kandidat, runtime,
kontrollnavn og observerte grenser. Testen av omdirigering dokumenterer
S1; et bestått observasjonspunkt hevder ikke at vertsgrensen er håndhevet.
Byggerens offlinekontroll ble også kjørt uendret: **2874 kontroller, 0 feil**,
med separat [faktisk resultat](builder-verify-current.json).

Før publisering ble kontrollskriptets formatering og eksplisitte binding
av løkkevariabler rettet i reviewartefaktet. De samme 775 kontrollene og
observasjonene består mot den uendrede forskningskandidaten. Datering,
filhasher og skillet mellom kandidat og senere reviewartefakt står i
[rettingsattesten](review-artifact-fix.md). Dette endrer ingen auditfunn.

| Flate | Kontroll og resultat |
| --- | --- |
| Kandidat og bevaring | Alle 52 endrede filer er sammenlignet med kandidatens Git-blobbyte. Alle 627 beskyttede filer er i tillegg sammenlignet direkte mellom base og kandidat, med kontroll av manifestets gamle blob-ID-er, størrelser og SHA-256. Produkt/schema 5/B5/lesere/standardvalg, K3/P1/R2/P2 og CI er ikke endret. |
| Filstier og skriving | Alle 886 refererte manifest-/beleggstier, inkludert gjentatte referanser, løser innen avtalt lokal rot. Ingen av kandidatfilene er symlinker. Negative identifikatorer med traversal, absolutte stier, kolon, separatorer og kontrolltegn avvises før nett. Et allerede brukt navn avvises før nett og uten overskriving. Hjelperen skriver bare i den lokale forskningspakkens `originals` ved autorisert, sekvensiell bruk. |
| Forsøk og originaler | 15 sidevogner, 14 komplette arkiver, ingen uregistrerte originalfiler. Sidevogn/manifest-identitet, forespurt/endelig HTTPS-vert, arkiv- og entity-hasher/størrelser er kontrollert. De nye originale entity-størrelsene er maksimalt 765 739 byte; høyeste observerte gzip-forhold er 16,37. XML, HTML-slutt og PDF-konvolutt er kontrollert innen dokumenterte grenser. |
| Feil og avbrudd | Simulert transportfeil og ufullstendig respons gir bevart forsøksmetadata uten fabrikkert komplett arkiv. Simulert HTTP-feil bevarer feilresponsens byte og merker `http_error`, ikke `complete`. Vellykket svar bevarer også CRLF, NUL og UTF-8-byte uendret. |
| XML og HTML | XML bruker `resolve_entities=False, no_network=True`. Både intern og ekstern fil-entitet forblir uekspandert i negative prøver. HTML behandles som data, uten JavaScript-, bilde- eller hendelseskjøring. XPath har ingen `document()`-funksjon i denne bruken; XInclude eller XSLT kjøres ikke. |
| Manipulasjon og proveniens | Negative prøver med endret metadatahash, kildehash og beleggtekst avvises. Beleggene gjenleses fra hashbundne HTML/XML-originaler; ledger/kryssreferanser beholder egne kilde- og tolkningsroller. Manifestene behandles som reviewede lokale repo-inndata. Den uavhengige Git-kandidatsjekken hindrer at en selvkonsistent omskriving av manifest og filer tas som samme reviewkandidat. |
| Hemmeligheter og utgående data | Ingen treff på de avgrensede, sterke mønstrene for GitHub-token, AWS-tilgangsnøkkel, privat nøkkel eller Authorization/Bearer i hele kandidatinnholdet, inkludert dekomprimerte nye originaler. Registrerte kildeforespørsler har bare User-Agent og Accept-Encoding, ingen Authorization eller Cookie. Bevarte Set-Cookie er responsmetadata fra offentlige, ikke innloggede kildehentinger; ingen nettlesersesjon hentes eller videresendes av koden. |
| Kjøring og rettigheter | Ingen eval/exec, shell-kjøring av fjerntekst, produktdatabase, installasjon, opplasting eller melding til andre i hjelperne. Den ene subprocess-kjøringen i verify bruker fast Git-argv uten shell. Fjerntekst, filnavn eller XPath settes ikke inn i en shell-kommando. |

## Reproduksjon og grenser

Fra checkoutens rot, med det oppgitte Python-/lxml-miljøet:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = (Resolve-Path '../p1-perioderegister/.local/python').Path
& 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' docs/research/u1-100895-58/reviews/security/security_checks.py
```

Kontrollskriptet skriver bare resultat og midlertidige, automatisk ryddede
syntetiske prøver i denne review-mappen. Kandidatfiler og tidligere
forskningspakker endres ikke. Ingen commit eller GitHub-mutasjon er utført.

`acquire.py` har socket-timeout på 50 sekunder, men ingen samlet frist eller
bytegrense. `gzip.decompress` har heller ingen egen applikasjonsgrense.
De konkrete arkivene er målt og kontrollert; hjelperne er lokale
forskningsverktøy for eksplisitt valgte kilder, ikke en uovervåket tjeneste
for vilkårlige URL-er, arkiver eller manifester. Sti- og skrivekontrollene
er ingen garanti mot en lokal angriper som samtidig endrer checkouten.
Disse grensene gir ikke et nytt produktkrav i #58.

Ingen nye primærkildehentinger ble gjort i auditen. HTTPS-transporten er
ikke replayet; wire/TLS-byte er ikke bevart. PDF er bare kontrollert som
råfil/konvolutt, ikke rendret eller tekstkontrollert. Mønstersøk er ingen
uttømmende hemmelighetsdetektor. Hashene binder de undersøkte byte til
kandidaten og gir ingen kildeutgiversignatur, faglig årsaksept eller
bekreftelse av faktisk fullmaktsbruk.

Full produkttestsuite og Linux-CI kjøres av orkestratoren; denne auditen
erstatter ikke de portene, samlet Standards/Spec, kildekontroll, publisering
eller bekreftet merge. Fullt CI-utvalg og 90-minuttersgrensen er bevart.
