# T1/#41: begge innganger fra original til gjenlest fil

Lokal kandidat 27. oktober 2026, fra base
`62a54a22ce1d3267c7a0dfbc53bfe23af8cfe5fd` på `codex/41-visningspilot`.
Eierens mandat gjelder T1. Samlet Standards-/Spec-review og separat audit av
fryst head `4cfccb4534b818fb922cd3dac0a713d6c5a2c188` fant fire nødvendige
rettelser. De er rettet i arbeidsflaten med bevisene nedenfor. Ny uavhengig
verifikasjon, GitHub/CI og eventuell merge er orkestratorens egne porter;
retteren har ikke utført dem.

[Kontrakten](../../visningspilot.md) og [ADR 0011](../../adr/0011-filbasert-visningspilot.md)
fastsetter separat opt-in `visningspilot-1`. Kontrakten ble skrevet før
produktkode. Videreføringen har presisert de to nye numeriske adapterinngangene
før sin endring av dem, og prøvd at manglende stadium gir hull i faktiske filer.
De tidligere O2b-originalene/tekstene er bevart; de er ingen skjult reserve for
en feilet ny numerisk adapter. Ingen nye avhengigheter eller databasemigrering
inngår.

## Resultat og avgrenset fasit

Det autentiske grunnlaget fra den ekte tidligere B-leveransen gir 13 nye
kildeobjekter og ti uendrede O2b-kildeobjekter, fem dokumentversjoner, 57
inventarrader, 54 tekstutsagn, 18 eksakte tabellfelt, 18 nye relasjoner og 18
separate behandlingskontekster. O2bs elleve seksjoner/tretten relasjoner ligger
fortsatt ordrett i sitt eget grunnlag. Flere tekster og lenker øker ikke antall
vedtatte hendelser.

| Valg i 2024 | Tabellfelt | Vedtaksfelt | Vedtatte beløpshendelser |
| --- | ---: | ---: | ---: |
| 1429/1 | 9 | 3 | 1 |
| 1429/22 | 9 | 3 | 1 |
| Begge | 18 | 6 | 2 |
| 1429/60 eller tomt kontoutvalg | 0 | 0 | 0 |

Prop. 16 S har synlig helinventar: 37 endringsgrupper og 45 ulike uttrykkelige
kontoangivelser, med særskilte fullmakts-/kontekstroller og II–VI. Bare 1429s
seks forslagstabellfelt er importert. Hele 81 S har /1, /22 og /60, alle
sammendrag, samlet komité, tilråding I–II og sluttunderskrift i full PDF.
211 har bare stikkordsfullmakt. Fullmaktskjeden Prop. V nr. 3 → 81 II → 211
har separate bevis og gir ingen ekstra bevilgningshendelse. Avrundet lønn,
historisk RNB, fondets 10 mill. og 2024/2025-kontekst beholdes som tekst med
egne roller/perioder.

De tre stadiene har egne kilder/ID-er. Begge innganger bruker samme basis,
unionen av hele kapitler og konkrete kontopar gir intet kryssprodukt, og
dokumentåpning viser hele dokumentinventaret. Retur bevarer opprinnelig valg.
De to saksgrenene beholder sine forskjellige omfang; 95 S er synlig ustrukturert.
Gamle seks vedtaksfelt, UUID, `step_id`, tolkning, `round='uavklart'`, B5-status,
schema 5, tidligere formater og standardvalg er uendret.

## Proveniens som kan etterprøves offline

[Gzip-originalen](originals/session-2024-2025-9cfe.xml.gz) er en tapsfri bevaring
av nøyaktig gammel fullrespons, SHA-256
`9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680`,
7 479 943 byte. [Metadata](originals/session-2024-2025-9cfe.meta.json) bevarer
den faktisk gjenfunne transportposten: henting 20. oktober 2026
11:36:10.455138 UTC/HTTP 200. Dette er ingen ny HTTP-henting.

`python docs/research/visningspilot-41/kontroller-forelder.py` leser uten å
skrive. Prefix 317 og suffix 55 byte, objektene ved 1 249 812/5 686 byte (210)
og 2 298 491/132 911 byte (368), rekonstruerer de gamle fixturene byteidentisk.
210/368s gamle sidevogner er uendret. 211 rekonstrueres separat fra sin nyere
c5f3b900-forelder under #37; disse to responsversjonene blandes aldri.

## Faktiske filer og kompatibilitet

Siste kontrollleveranse ligger i checkoutets `work/t1-fixed-delivery/`.
`kontroll.json` har filhasher, rapport-/basis-ID-er, valg, fire uavhengighetsprøver,
manglende nytt tilrådingsstadium og gamle kompatibilitetsprøver. Den samme
leveransen har 19 vanlige JSON-/Excel-par: post1, post22, begge, post60, tomt,
kapittel, to unioner, 2025-kontekst, fem dokumentvalg, fire navigasjonsvalg
og offline. I tillegg finnes særskilt merkede feilpar og to offentlige CLI-par.
Alle er faktisk lukket og gjenlest. `gjenfunne-originaler/` og CLI-originalene
gjenfinner råbyte fra de selvforsynte filene.

Tidligere `work/t1-review-delivery/` og alle dens 201 manifestførte filhasher er
kontrollert uten omskriving. Den tidligere kontrolljournalen er bevart byteidentisk
som `prior-candidate-verification.json` i den nye katalogen. Nye T1-kandidatfiler
har nytt grunnlags-/rapport-ID fordi nye utsagns hierarki er rettet; de gamle
O2-observasjonene, seksjonene og kildebytene er uendret.

De ekte tidligere A/B-filene er lest fra hashkontrollerte kopier: to A-par og
seks B-par. To ekte gamle B8/B9-par er også lest, med henholdsvis 39 og 13
Historikk-kolonner. Deres uendrede innebygde B6-kjerner er lest med frozen-v1-
leseren. Originalenes hasher er like før/etter, og filene er ikke omskrevet.

Den ekstra ekte eldre `accept-b6.xlsx` (4 648 442 byte, SHA-256
`8487909b5e7b2b7498c9ab78de9fb88966be926202df89388ef3f31871ac1f39`)
er en tidligere lokal B6-akseptbok, ikke en nygenerert layouttest. En kontrollert
kopi har 21 ark, 2 183 inventarrader, 5 492 unike observasjonsrader/36 kolonner
og 33 Historikk-kolonner. Alle 5 492 gamle observasjonsobjekter er dekodet med
eksisterende modell og avstemt mot faktiske ID-, beløps-, betydnings- og
kildepekerceller. 50 uttrekk er valgt, 47 har beløpsrader; B5-valg er tomt.
Rapport-ID er `3ff5698de68eaad7f200d08fb73d83c150adea56ae49ccc2b1bd2efa305a9cfc`.
Selvstendig gammel frozen-v1-rapport-JSON og eksakt historisk writercommit
er ikke funnet. Utvalgs-/bevis-JSON er ikke SessionReport. Ingen 92 MB gammel
database er kopiert inn i repoet eller brukt som inngang.

## Uavhengighet og sikker filgrense

Hver av manglende, faktisk feilet filåpning, korrupt og motstridende ny kilde
gir et separat globalt avvik i et faktisk gjenlest tomt visningspar. Deretter
oppdages autentisk 40034229/formelt 368 som ny i hver ferske testdatabase via
ordinær synkroniser → tolk → analyse/Excel. Ny råbevaring, lagring, 74 posthendelser
og de faktiske 700/1-cellene 304 351 000 / 6 324 000 / 310 675 000 kontrolleres.
Historisk Excel, start eller register inngår ikke. Prøven er en autentisk
lagret offisiell respons, ikke et nylig livevedtak.

Nytt bortfalt tilrådingsstadium prøves separat gjennom faktisk JSON/Excel:
/1 har seks gjenværende felt, én vedtatt hendelse og seks hull, alle med
`difference_kr=null`. Den normale prøven har tolv beregnede nullforskjeller
med to faktiske sammenlignbare inngangs-ID-er hver. År, konto, enhet, betydning,
detalj, scope, rolle og runde sperrer inkompatible sammenligninger.

Leserne rekonstruerer alle avledede felt fra de innebygde hashfestede kildene,
og kontrollerer faktiske Excel-celler, typer, lokale lenker, tekststykker og
arkstruktur. Ny hash på manipulert tekst/rolle/kilde/binding godtas ikke som
kildefasit. Gamle ZIP/XML-grenser er parametrert med uendrede standardverdier,
slik at T1 kan gjenbruke samme ressursvern med egne arknavn/snapshot og strengere
128 MiB-grense. Gamle lesere får samme grammatikk/grenser som før.

## Rettede review- og auditfunn

Analyseorkestreringen validerer nå tidligere analysekonvolutter til den typede,
immutable `PilotInput`-kontrakten. Kildeadapteren har ingen analyseimport og
rekonstruerer fortsatt kildegrunnlaget. En separat prosess med alle
`analyse`-importer blokkert har importert og rekonstruert det autentiske grunnlaget.
Se [adaptergrensen](../../visningspilot.md#adaptergrense-og-kontroll-av-tidligere-grunnlag).

Nye HTML-utsagn følger logiske seksjoner. Post 60 har kjeden Sammendrag →
Kap. 1429 Riksantikvaren → Post 60 Kulturminnekompetanse i kommunene, kan overføres.
Alle sju nye 81-seksjoner, tilråding II, Prop.-fullmaktene II–VI og V nr. 3 er
kontrollert mot originaloverskrifter, begge innganger og faktiske JSON-/Excel-celler.
`review-probes/hierarchy-all.json` avstemmer alle tjue nye HTML-utsagns
hierarkier mot originalene, også delrepresentasjoner og hele dokumenter.
Ingen gammel O2-seksjon eller dens hierarki er omskrevet.

Alle seks gamle vedtaksobjekter gjenskapes fra pinnet 210-original, kjent
`storting-belop-v2`-tolkning og samme bundne uttrekk/revisjon før de får verifisert
T1-kontekst. Hele objektene sammenholdes, inkludert kroneverdi, råfelt, konto,
år, betydning, enhet, kildepeker og ID-grunnlag. Tretti negative varianter
dekker begge poster og alle seks felt, også når uttrekk og ytre konvolutter
endres konsistent. Den konkrete P1-manipulasjonen av 5 796 000 til 999 999 999
avvises både ved import og i faktisk skrevet JSON/Excel. Gamle O2-lesere kan
fortsatt lese samme advarselsrapport; T1s strengere grense er separat.

T1-Excel-leseren sammenholder tallformat, effektiv skrift/fill/ramme/justering,
ark-/arbeidsbokvisning, rad-/kolonnedimensjoner og filter-/fletteoppsett med sin
egen forventede bok. Sytten negative visningsprøver dekker blant annet fast
falskt beløp, tomt format, skjult Dekning, skjulte/små rader og kolonner,
usynlig skrift/fill og uventede formateringsregler. Kilde-JSON er uendret i
disse prøvene. `review-probes/results.json` og de særskilt merkede feilfilene
bevarer lokale reproduksjoner fra den ekte nye leveransen. Gammelt O2/B8-guard
er uendret. Hashfestet `verification.json` har målrettet `-text` i
`.gitattributes`, slik at publiseringsnormalisering ikke endrer kontrollbytene.

## Reproduksjon og bevis

Kjør fra reporoten med pinnede `requirements-dev.txt`-pakker og ferske output-
og basetemp-navn. Den lokale prøven brukte bundlet Python 3.12.14 og allerede
pinnede pakker via `PYTHONPATH` i lokal kontrollkatalog, uten installasjon eller
pakkeendring. Vanlig Windows `python` er et WindowsApps-alias i dette miljøet.

```powershell
python -m ops.visningspilot_proeve --previous-root <hovedarbeidsområde> --output work/t1-ny --legacy-b6 <ekte-eldre-accept-b6.xlsx>
python -m analyse.visningspilot --o2b <ekte-begge.json> --aar 2024 --konto 1429/22 --json work/ny.json --excel work/ny.xlsx
python -m analyse.visningspilot --frosset work/ny.json --json work/offline.json --excel work/offline.xlsx --originaler work/originaler
python -m pytest tests/test_visningspilot.py -q --basetemp work/t1-tester-ny
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pytest -q --durations=20 --basetemp work/alle-tester-ny
```

[verification.json](verification.json) registrerer utførte kommandoer, utfall,
faktiske filhasher, kildeoppskrift og akseptledger M01–M09/M13/M22–M27.
Maskinloggen skiller kjørte kontroller fra senere review-/CI-porter.

Utførte lokale sluttkontroller etter retting: **92 T1-tester bestått** og ny
fullsuite med **1 019 bestått, to hoppet over**, uten feil. Fullsuite startet
etter alle produktrettingene og dekker også O2a/O2b/B6/B8/B9 og gamle guardprøver.
Hoppene gjelder vertens manglende symlink-/hardlinkrettigheter i to eksisterende
tester. Alle 26 nye gyldige JSON-/Excel-par er dessuten gjenlest igjen.
Ruff check/format (**104 Python-filer**), mypy (**58 produktmoduler**) og
`git diff --check` består. Eksakte varigheter, filhasher og kommandoer finnes
i den oppdaterte kontrolljournalen; tidligere resultater er bevart separat.

Tolv representative områder, ett per ark i den lagrede siste arbeidsboken,
er rendret med bundlet Artifact Tool. År vises uten tusenskille og globale
dekningsforhold kan leses. Lange tekst-/HTML-/ID-/base64-felt er kontrollceller
som åpnes for hele innholdet; dette er ingen trykksatt dokumentgjengivelse.
Ingen native Excel-applikasjon er prøvd. T2–T6, K1–K3, årsdekning,
kontokontinuitet, tallfestet mindretall og produksjonsdrift er fortsatt utenfor.
#10 står åpen.
