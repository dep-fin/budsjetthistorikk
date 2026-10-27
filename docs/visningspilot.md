# T1: separat dokument- og konto-/årspilot

Kontrakt fastsatt 27. oktober 2026 **før produktkode** innen eiergodkjent #41.
Dette er et separat filformat og en lokal opt-in-kommando. Hovedschema 5,
B1–B9, frozen-v1/v2, O2a/O2b, B5 og standardvalg beholder sin betydning.
Se [ADR 0011](adr/0011-filbasert-visningspilot.md) og [observasjonsformatet](observasjonsformat.md).

## Frossen akseptledger

Testgrensen er original → kildebundet beløp/tekst → dokumentert relasjon → begge
innganger → **skrevet og faktisk gjenlest JSON og Excel**. Fasiten er
[testmatrisen](research/to-visninger-37/testmatrise.md):

| Matrise | T1-forpliktelse |
| --- | --- |
| M01 | Originalbyte/hash, lokator, tekst/hierarki, bevart sidevogn og reell forelderbinding. Manglende eldre forelder vises som gap. |
| M02 | Hele 81 S: sammendrag /1,/22,/60, samlet komité, I/II og sluttunderskrift. |
| M03 | /1 og /22: 9/3/1 hver; begge 18/6/2; tomt 0/0/0 (tabellfelt/vedtaksfelt/vedtatte hendelser). |
| M04 | Prop. V nr. 3 → 81 II → 211, fullmakt uten beløp; avrundet/historisk/fremtidig tekst med egne perioder. |
| M05 | Prop. har 37 tabellgrupper, 45 ulike kontoangivelser, II–VI og full PDF; bare 1429-beløp strukturert. |
| M06–M07 | Eksakt dokumentversjon og union av hele kapitler/konkrete par innen år; retur bevarer opprinnelig utvalg. |
| M08–M09 | Nullforskjell krever to sammenlignbare felt; manglende stadium gir hull. Gamle ID-er og round='uavklart' består. |
| M13 | 100927/81/210–211 gjelder 1429; 100889/95/359–364 gjelder unntatt 1429. Referanser med lik eksport-ID beholdes separat. |
| M22 | O2b-P1, relasjoner, gamle observasjoner og hendelser kopieres ikke ved filtre/navigasjon/eksport. |
| M23–M24 | Streng offline-gjenlesing, synlige celler/lenker og tapsfrie tekststykker kontrolleres mot rekonstruert kildegrunnlag. |
| M25 | Ekte tidligere A/B og B8/B9 leses uten omskriving; innebygd B6 fryses uendret. Separat gammel B6-leveranse er en uttrykkelig bevisgrense dersom den ikke finnes. |
| M26 | Autentisk 40034229 gjennom ordinær synkronisering, tolkning, analyse, lagring og eksport ved manglende/feilet/korrupt/motstridende tillegg; ingen historisk Excel. |
| M27 | Ulike år, kontoer, valuta/enhet, betydning, detalj, omfang, runde eller stadium/rolle sperrer sammenligning med navngitt grunn. |

Ingen positiv komitéendrings-, mindretalls-, helårs-, kontinuitets- eller driftsaksept følger.

## Adaptergrense og kontroll av tidligere grunnlag

`analyse.visningspilot.source_input(o2b_json)` validerer de tidligere analysekonvoluttene
og deres kilde-/uttrekksbinding og leverer et immutable `PilotInput` med OmtaleBasis,
uttrekk, de seks overførte observasjonene og tidligere avvik. Den offentlige
analyseinngangen `import_basis(o2b_json, root)` orkestrerer deretter adapteren.
`innlesning.visningspilot.import_basis(prepared, root)`,
`structure_basis(prepared, sources)` og `validate_basis(basis, prepared)` bruker
den typede kontrakten uten å importere analysepakken. Adapteren kontrollerer selv
omtalegrunnlaget, kildeankrene og hele de seks observasjonsobjektene mot originalen
og den kjente gamle v2-tolkningen. Analysekonvoluttens ID eller tidligere
advarselsstatus er ingen erstatning for denne kontrollen.

Avvik i overførte beløp, konti, år, betydning, enhet, kildepeker, hendelse,
uttrekks-/tolkningsbinding eller øvrige observasjonsfelt avviser T1-grunnlaget
før kildeverifisering og sammenligning. Den gamle O2-leseren og dens videre
advarselskontrakt er uendret. Offline-leseren validerer analysekonvoluttene på
nytt og rekonstruerer adapterresultatet fra samme innhold; ingen database/nett.

## Felt og identitet

JSON-konvolutten har nøyaktig `format='visningspilot-1'`, `report`. Rapporten har
`id`, `basis`, `selection`, `return_selection`, `view`, `version`. `view` er avledet;
leseren beregner den på nytt og avviser forskjell. Alle nye modeller er immutable.

`basis` har `id`, `rule='innst81-visning-1'`, `o2b_json` (uendret, full tidligere
O2b-rapport), `sources`, `documents`, `inventory`, `statements`, `observations`,
`relations`, `contexts`, `issues`, `version='visningsgrunnlag-1'`.

| Modell | Felter og typer |
| --- | --- |
| Kilde | `id,name,document_key,media_type,expected_sha256,status,metadata_json: str`; `content_base64,sha256: str|null`, `byte_count: int|null`. O2b-kilder beholdes i O2b-konvolutten; nye kilder har eget navnerom. |
| Dokument | `id,key,title,kind,session,date,raw_coverage,structured_coverage,professional_status: str`; `source_ids,accounts: tuple[str]`. Dato er ISO-dato. Versjonen binder alle kilde-ID-er. |
| Inventarpost | `id,document_id,source_id,locator,chapter,post,role,structure_status,text: str`; `budget_year: int`; `observation_ids: tuple[str]`. Kanoniske kontokoder er desimal tekst uten ledende nuller; rå tekst beholdes. |
| Tekstutsagn | `id,document_id,source_id,locator,text,html,role,actor,period,status: str`; `accounts,hierarchy: tuple[str]`. Periode er en kildeavgrenset tekst (2024,2025,historisk RNB,aggregat,fremtidig kontekst); ingen beløpsobservasjon av avrundet omtale. |
| Relasjon | `id,from_id,to_id,role,scope,status: str`; `accounts,evidence_ids: tuple[str]`; `budget_year: int`. Scope er kapittel_1429 eller unntatt_1429; postvise relasjoner har konkrete par. |
| Kontekst | `id,observation_id,document_id,round,stage,actor,status: str`; `evidence_ids: tuple[str]`. Separat nysalderingskontekst endrer ikke gamle AmountObservation-felt. |
| Beløp | Eksisterende AmountObservation, SourcePointer, Interpretation; 12 nye forslag-/tilrådingsfelt i separat navnerom og seks nøyaktig uendrede vedtaksfelt fra O2b. |
| Sammenligning | `id,meaning,account,status,reason,rule: str`; `left_id,right_id,null_reason: str|null`; `difference_kr: int|null`. |

Nye objekt-ID-er er SHA-256 via `identity(navnerom, asdict(objekt med tom id))`.
De to nye numeriske adapterinngangene leser Prop.-forslagets og Innst. 81s
HTML som egne, hashfestede `PilotSource`-objekter. O2b beholder samtidig sitt
tidligere rå-/tekstgrunnlag ordrett. Manglende, feilet eller endret ny inngang
gir ingen nye beløpsfelt for det stadiet, synlig globalt avvik og hull i
stadiesammenligningen. Den tidligere innebygde teksten brukes ikke som en
usynlig reserve for en feilet ny adapter. Inventaret fra den bevarte O2b-kilden
består med `ikke_strukturert` der den nye adapteren mangler beløp.
Dokument-ID er en eksakt versjon bundet til kilde-ID-er. Beløps-ID følger
observasjon-1 med kildesystem visningspilot, kildehash, lokator, felt og ny
tolknings-ID. Gamle seks objekter, step_id, ID-er, rånavn, tolkninger og B5-status
gjenbrukes ordrett. Kildeverifisert er adskilt fra ikke_faglig_godkjent.
Nullable kildebyte/hash/størrelse forekommer samlet ved mangler, med grunn i
status/avvik. Manglende inngang gir `difference_kr=null` med årsaken manglende stadium;
sperre gir konkret grunn. AmountObservation beholder sine eksisterende nullgrunner.

## Utvalg, navigasjon og sammenligning

Selection har `mode: str`, `document_id: str|null`, `years: tuple[int]`,
`chapters: tuple[str]`, `accounts: tuple[tuple[str,str]]`. Dokumentvalg krever én
eksakt kjent dokument-ID og tomme andre filtre; konto-/årsvalg krever null
dokument-ID. År avgrenser unionen av hele kapitler og konkrete konto-par. Tomme
år eller tom kontounion gir null treff. Ingen kryssproduktsemantikk.

Dokumentvalg viser hele dokumentets inventar og tekst uansett forrige filter.
open_document/open_accounts lagrer forrige selection; go_back gjenoppretter
startutvalget og tømmer returpekeren. Begge valg serialiseres og valideres. Globale dokumenter, inventar,
kildeavvik og periodehull beholdes alltid i basis og egne Excel-ark.

Regelen stadieforskjell-1 krever begge felt, dokumentert relasjon, samme
år/konto/valuta/multiplikator/betydning/detalj/omfang og separat kildebundet samme
behandlingsrunde. Bare regjering → samlet tilråding → vedtak er tillatt i T1.
Uavklarte roller eller manglende kontekst gir sperre. Resultat peker til begge
observasjons-ID-er; det er ingen ny kildeobservasjon eller hendelse.

## Offline kontroll og grenser

Leseren godtar bare eksakt versjon/felt/type, ingen duplikatnøkler, NaN/Infinity,
ukjente felt eller ID-er. Maksimum 64 MiB JSON, 16 MiB per råkilde, 32 MiB
dekomprimert gzip, 64 kilder, 16 dokumenter, 512 inventarrader, 512 tekstutsagn,
256 beløpsfelt og 1024 relasjoner. ZIP begrenses til 256 medlemmer/128 MiB
utpakket, ingen makroer, eksterne arbeidsboklenker eller uventede ark. Tekst og
base64 lagres i ordnede stykker på høyst 30 000 tegn.

Alle avledede felt rekonstrueres fra kildebyte. Originalene har versjonsfestede
forventede hasher i adapteren; endret rolle/tekst/hash oppgraderes ikke ved å
beregne ytre ID-er på nytt. Manglende/feilet, korrupt eller motstridende ny kilde
bevares som globalt avvik og brukes ikke som verifisert grunnlag.

Nye HTML-utsagn følger kildens logiske seksjoner. Innst. 81s `m1_1_3` har
overskriftskjeden Sammendrag → Kap. 1429 Riksantikvaren → Post 60
Kulturminnekompetanse i kommunene, kan overføres, selv om seksjonene er
DOM-søsken. Tilrådingens II og proposisjonens II–VI bruker sine egne
romertalls-/fullmaktsoverskrifter. Gamle O2-seksjoner og deres hierarki/ID-er
kopieres fortsatt uendret.

210s gamle utdrag/sidevogn har forelder 9cfeaef5…; den nøyaktige originale
HTTP-responsen ble gjenfunnet 27. oktober i det eldre lokale kildearkivet og
bevares tapsfritt som gzip med original transportmetadata under
research/visningspilot-41/originals. #37s gzip har fullresponshash c5f3b900….
Dette er forskjellige kildeobservasjoner. 210 rekonstrueres bare fra sin gamle
forelder (prefix 317 byte, objekt 5686 byte, suffix 55 byte), 211 bare fra sin
egen nye forelder og dokumenterte bytegrenser. Fravær eller motstrid i forelderen
gir synlig avvik; den eldre sidevognen omskrives aldri.

Excel har egne ark for valgt forløp, dokumenter, globalt inventar, fulltekst,
relasjoner, sammenligninger, dekning/avvik, originaler og kontrollgrunnlag.
Lokale lenker binder konto-, dokument- og tekst-/observasjonsrader. Leseren
gjenbygger forventede ark fra validert JSON og sammenholder alle faktiske celler,
typer, lenker og ordnede tekststykker. T1 krever også samme tallformat,
effektive celleskrift, fill, ramme, justering og beskyttelse, synlige ark,
arbeidsbok-/arkvisning, rad-/kolonnedimensjoner og filter-/fletteoppsett som
sin egen forventede bok. Skjulte eller minimert viste verdier og globale
avvik godtas ikke som en identisk eksport. Det eksisterende ressurs-/XML-vernet
avviser også uventede formateringsregler/overlegg. Innebygd JSON alene er ikke aksept.
Inventararket viser en kompakt tekstgjengivelse med normaliserte mellomrom;
originalens komplette tegn/linjeskift ligger i grunnlaget og fulltekstarkene.
Fulltekst, HTML, ID-er og base64 er kontrollfelt: hele feltet åpnes i cellen
eller gjenfinnes med `--originaler`, og er ingen trykksatt PDF-gjengivelse.
Formeltegn i kildetekst lagres uttrykkelig som tekst. Publisering bruker nye
filnavn og atomisk no-clobber. Gjenlesing åpner ingen database eller nett.
