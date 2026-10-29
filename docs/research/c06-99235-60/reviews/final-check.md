# Målrettet uavhengig etterkontroll av C06 / #60

Kontrollert 29. oktober 2026, uavhengig av byggeren og integrasjonen.
**Etterkontrollport: bestått. Ingen nødvendige eller sperrende funn.**
Kildekontrollens P3 og Specs SP1 er samme presisjonsfeil i J02; rettingen
er bekreftet på den faste kandidaten nedenfor. De fire tidligere portene
beholder sine opprinnelige kandidatbindinger og kontrollgrenser.

| Fast punkt | Full commit-SHA | Git-tre |
| --- | --- | --- |
| Etterkontrollert kandidat | `d241ad8f36f70718dbc54d3093c151d301d04f30` | `afd35a9f4bf98c8b2e69bd3373464a9661811b7b` |
| Tidligere forskningskandidat | `9eb27cebf7ca4a99aeb30fa32245e41314e0d295` | `60dfabaec4e7c022e30c6a6389a622790fad11f5` |
| Base etter U1 | `49cc6e44851cf74e0aaea4eb333419e5598bfd95` | `6dcc9a203a895fa4206a8ef9041bdbccb0b9b580` |

`HEAD`, trær og begge ancestry-forhold er kontrollert direkte med Git.
Arbeidsflaten var ren før kontrollen. Alle 27 endrede/tilførte arbeidsfiler
ble sammenlignet med kandidatens faktiske Git-blobbyte. Denne rapporten
er et etterfølgende dokument og inngår ikke i treet `afd35a9f…`.

## Mandat og nøyaktig endringsgrense

AGENTS, arbeidsflyt, issue-tracker, begrepsregler/GLOSSARY,
ansvarsdeling, C06-kontrakten, den bevarte komplette #60-teksten med
returnerte kommentarer, pakkerapporten og [reviewinngangen](README.md)
er lest. Mandatet er denne avgrensede etterkontrollen. Ingen ny
GitHub-status eller kildeobservasjon er hentet.

Den eksakte Git-diffen `9eb27ce…d241ad8` er gjennomgått. Den inneholder
**seks modifiserte byggerfiler og 21 nye review-/integrasjonsfiler**,
ingen sletting eller filmodusendring. Alle nye filer er vanlige
`100644`-filer under `reviews/`.

- `cross-reference-journal.json` er byteidentisk med 9eb etter nøyaktig
  én utskifting: «14 nøkkelsider er lest visuelt» til «18 nøkkelsider
  er lest visuelt». Ingen annen byte i journalen er endret.
- README, OVERLEVERING og reproduksjon beholder hver hele sin gamle
  tekst som uendret byteprefiks. Tilleggene beskriver de fire historiske
  portene, rettingen og nye kontroller med fortsatt åpne leveringsporter.
- `delivery-manifest.json` har samme 73 filstier og representasjoner.
  Bare fem berørte filrader har nye hash-/størrelsesfelt; samlet størrelse
  er 22 742 994 byte. Alle 73 rader stemmer med faktiske kandidatblobber.
- `verification.json` endrer bare kontrolltidspunkt, antall lokale
  Markdown-lenker fra 161 til 172 og total fra 3 262 til 3 273.
  De øvrige feltene er identiske. Dette er ny arbeidsfilkontroll,
  adskilt fra reviewernes opprinnelige resultater.

Alle **1 138 øvrige filer fra 9eb** har uendret Git-blob og filmodus.
Alle **1 070 beskyttede basefiler** har samme blob og modus i base,
9eb og d241; deres bevarte checkout-byte består også offlinekontrollen.
Produktkode, tester, CI, schema 5/B5 og pinnede K3/P1/R2/P2/U1-filer
er derfor uendret. AGENTS/kildefunn har heller ingen endring etter 9eb.

De historiske tallene er dessuten telt direkte på nytt: **67/66**
kandidatforekomster/unike saker, herav **60/59** åpne; fem monetære
hendelser og elleve vedtaksfelt. `candidate-followup.json` beholder
R1–R7 og `product_adoption=false`. Den bevarte, hashkontrollerte
runtimeattesten har fortsatt 25 vedtakskandidater, delvis årsdekning og
`professional_annual_balance_approval=false`; JSON/Excel-testene er
ikke kjørt på nytt i denne etterkontrollen.

## J02 og kildeforutsetningene

Sidejournalen er uendret og har 130 sider, hvorav nøyaktig disse 18 har
`visual_review=true`: **11, 12, 13, 14, 16, 39, 40, 50, 69, 77, 78,
79, 80, 82, 105, 106, 116 og 135**. De stemmer med lesejournalen,
kildereviewerens opprinnelige sideliste og alle 18 visuelle belegg.
Hvert visuelt belegg har samme side og bildehash som sidejournalen.
Offlinekontrollen gjentok PDF-/bilde-, OCR-/journal- og lokatorbindingene.

J02s endrede tall beskriver dermed det allerede dokumenterte omfanget.
Original-PDF, bilder/OCR, belegg, sidejournal, behandlingsledger,
leddsammenligning, kildemanifest og gjenbruksmanifest er uendret.
Ingen ny visuell lesing eller utvidet semantisk bevisgrense følger av
rettingen eller denne etterkontrollen.

Kildeportens tidligere forutsetninger holder: debatt 20. juni og
votering/vedtak 21. juni skilles fortsatt fra de senere motstridende
20. juni-utsagnene. Riksantikvarens positive institusjonskobling
bevares uten ny postvis bevilgningshendelse eller dokumentert faktisk
anvendelse. /22 arver ingen /1-forklaring. Restene, OCR-begrensningene,
den avgrensede lesedybden og manglende årsaksept består.

## Historiske attester, helper og nye bevis

Alle **15 opprinnelige reviewfiler** er kontrollert byte for byte mot
[original-review-files.json](integration/original-review-files.json),
inkludert størrelse og SHA-256. De fire rapportene og resultatene
beholder 9eb/base-bindingene, sine opprinnelige funn og historiske
«gjenstår». Kildeportens 1 786 kontroller, Specs 50, Standards' 74
kandidatfiler og sikkerhetsauditens 3 776 er tidligere observasjoner;
de er ikke omskrevet til nye kjøringer på d241.

Standards-helperens originalbyte finnes i
[check_candidate.py.original](integration/check_candidate.py.original),
SHA-256 `3be9e5b97ee774b635dc563150deaf79c2a51bd59b4544cd8632086ba0649950`.
Den formaterte helperen har identisk AST uten posisjonsattributter.
Endringene er formattering og oppdeling av én strenglitteral; faste
SHA-er, sammenligninger, tellere og kontrollsemantikk er uendret.

Jeg kjørte også originalhelperens kode separat i minnet, med korrekt
`__file__` og resultatfilskriving avskåret. Resultatet var identisk med
den bevarte `candidate-checks.json`, bortsett fra tidspunkt: 74 endrede
filer, 1 070 bevarte basefiler, seks Python-filer, 37 JSON-filer og null
feil. Den formaterte helperens tilsvarende resultat ble reprodusert
gjennom integrasjonskontrollen. Ingen original rapport eller resultatfil
ble skrevet om.

[result.json](integration/result.json) binder 19 reviewbevisfiler;
alle deres hasher er kontrollert på nytt. Resultatet fra en ny
lesebasert integrasjonskjøring var identisk med dette resultatet utenom
tidspunkt. [checks.json](integration/checks.json) har gyldige bindinger
til sine tre produserte artefakter; alle tolv registrerte råutdatahasher
stemmer med de bevarte UTF-8-utdataene. Det registrerte
integrasjonsutdataobjektet er likt `result.json`.

Kontrollerte SHA-256-bindinger:

| Artefakt | SHA-256 |
| --- | --- |
| `integration/original-review-files.json` | `b9f9f32b030dbe8db06c851177d2873ed8bb98e19591a7015b844de535031702` |
| `integration/result.json` | `a29bd40027f4c3852f99c7faa90b645ed69d0afb7a795c48ac0ee492228b935f` |
| `integration/checks.json` | `2fab4fd0f2f6931a5713acdc26935953b7bec05df1c2c8ed3285398daa948ad2` |
| `../delivery-manifest.json` | `181eab2a56f2b8ec2931977afde4207646ee8d559c7c239361e427bd1080c2b3` |

Disse er bytebindinger til den faste kandidaten, ingen signatur fra en
kildeutgiver. Leveransemanifestets avtalte utelatelse av `reviews/**`
og integrasjonsresultatets utelatelse av seg selv/checks unngår
hashsykler; de er ikke en påstand om at denne senere rapporten inngår
i tidligere manifestevidens.

## Nye hjelpers Standards- og sikkerhetsflate

De fem tilførte Python-helperne er syntaksparset og gjennomgått for
relevant kjøring, filskriving, input og bevisbinding. Git-kall bruker
argumentlister uten `shell=True`. Integrasjonshelperen leser den lokale
hashbundne originalmanifesten, sammenligner AST før import og avskjærer
Standards-resultatets eneste skriving. Uten utdataargument skriver den
bare til stdout. Et uttrykkelig lokalt utdataargument er et operatørvalg,
ikke innhold fra HTTP eller primærtekst.

De historiske reviewhelperne beholder faste kandidatgrenser og kan ved
direkte kjøring skrive egne reviewresultater. De er ikke kjørt direkte
som nye porter her. Sikkerhetshelperens `exec(compile(...))` gjelder
eksplisitt navngitte, faste lokale Git-blobber; det kjører ingen fjerntekst.
Nettprober bruker falsk transport og socketblokkering. Bildeutfilnavn
konstrueres fra side-/bildeordinaler. Ingen ny produkt-, nettjeneste-,
opplastings- eller meldingsflate er innført av integrasjonen.

Sikkerhetsauditens forutsetninger holder: hentehjelperen og dens
verts-/redirectvern er uendret, og de ni offline transportprøvene
består. Lokale reviewede manifester og hashbundne arkiver er fortsatt
den avtalte inputgrensen. Dette gir ingen generell sikkerhetsgodkjenning
av vilkårlige fremtidige manifester, arkiver, tredjepartsbiblioteker eller
uovervåket drift.

## Egen reproduksjon og observerte begrensninger

Kontrollene brukte oppgitt Python 3.12.14 med
`PYTHONPATH=.local/python-tools`, `PYTHONDONTWRITEBYTECODE=1` og
`PYTHONIOENCODING=utf-8`. Ingen ny executable eller resultatfil er laget.

| Utført kontroll | Faktisk resultat |
| --- | --- |
| `reviews/integration/verify_integration.py`, uten utdataargument | Exit 0; 15 originale reviewfiler, identisk helper-AST/-utfall, 18 sider, 1 138 uendrede filer; resultat likt bevart integrasjonsresultat utenom tidspunkt |
| `verify.py d241ad8f36f70718dbc54d3093c151d301d04f30` | Exit 0; **3 346 kontroller, 0 feil**, herunder alle 73 faktiske kandidatblobber |
| `test_acquire.py` | Exit 0; **9 prøver bestått**, ingen reell nettforespørsel |
| Ruff check og Ruff format `--check`, begge `--no-cache`, på `reviews/` | Exit 0; alle fem Python-filer består |
| Mypy på den nye integrasjonshelperen | Exit 0; én kildefil, ingen feil; midlertidig cache under `.local` fjernet |
| Egne Git-/manifest-/journal-/reviewbindinger beskrevet ovenfor | Bestått; alle 27 arbeidsfiler mot faste blobber, fem manifesteendringer og 29 lokale lenkemål i de nye Markdown-filene kontrollert |
| Git diff `--check` med `core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol` | Exit 0 |

Standard `git diff --check 9eb…d241` returnerer derimot 2 fordi fem
opprinnelige reviewutdatafiler bevarer CRLF under pakkens `-text`.
Alle 10 640 meldinger gjelder disse linjesluttene; ingen ordinære
etterfølgende mellomrom/tabulatorer ble funnet. CR-bevisst kontroll
består. Originalbyte er med hensikt ikke normalisert. Integrasjonens
eldre `git diff --check`-observasjon gjaldt arbeidsfilene før staging;
den er ingen attest på denne senere komplette commitdiffen.

En første midlertidig mypy-cache i sandboxens systemtemp ga
`AccessDenied` ved opprydding etter bestått mypy. Gjentatt kjøring med
cache under `.local` bestod og ryddet opp. Ingen pakke- eller
manifestbyte ble endret av forsøkene.

Full produkttestsuite, ny kompatibilitetstest med skrevet JSON/Excel,
WinRT-OCR, ny visuell tarifflesing og ny kildehenting er ikke utført.
De fire tidligere generelle reviewene er heller ikke gjentatt; ingen
endrede forutsetninger som krever dette er funnet. Ingen PR, full
Linux-CI, publisering, merge eller GitHub-ancestry er bekreftet her.

## Publiseringsport

**Den rettede d241-kandidaten kan tas videre til publiseringsløpet.**
Grunnlaget er de fire faste 9eb-portene sammen med denne uavhengige
kontrollen av den eksakte etterfølgende endringen. Ingen nødvendig
retting står igjen i det kontrollerte innholdet.

Orkestratoren må binde en eventuell neste kandidat med bare denne
dokumentariske rapporten til d241, kontrollere den faktiske publiserte
kandidaten/treet og opprette den ene avtalte PR-en. Fullt uendret
Linux-CI-utvalg med 90-minuttersgrensen må bestå før den autoriserte
mergen; merge/ancestry og faktisk GitHub-sluttoverlevering gjenstår.
Andre innholdsendringer krever relevante nye etterkontroller. Ingen
neste ticket eller utvidet faglig aksept følger av denne porten.
