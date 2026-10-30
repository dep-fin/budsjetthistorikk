# T6: hele beriktiget Innst. 95 S og vedtak 359–364

Før-kode-kontrakt fastsatt 30. oktober 2026 for publisert [#64](https://github.com/depmartin/budsjetthistorikk/issues/64), fra main `9616fbe6a8ab15eec696f34de76888565a784f8f`. Bygging gjelder hele det faste snittet, ikke generell komitéparser. Ingen nødvendig oppdeling er påvist. T5/T1, observasjon-1, schema 5, B5 og tidligere filer/standarder består.

## Lukket felt- og identitetskontrakt

Alle nye modeller er immutable. Konvolutt: nøyaktig `format,report`, format `innstilling95-1`. Report: `id,basis,selection,return_selection,view,version`. PilotSelection/PilotView og StageComparison har uendrede felter som dokumentert i [T1](visningspilot.md). View rekonstrueres og sammenholdes; lagrede avledninger er ingen autoritet.

Basis: nøyaktig `id,rule,t5_basis,sources,recipes,documents,inventory,statements,observations,contexts,relations,bindings,coverage,authorizations,issues,version`. Regel `innst95-tabell-1`, versjon `innstillingsgrunnlag95-1`. `t5_basis` er én uendret typet [T5 Basis](proposisjon16.md), med dens ene uendrede typede T1-kapsel. Minneunionen serialiseres aldri som en ekstra kapsel. Bare nødvendige tidligere ikke-innlemmede original-/metadatarepresentasjoner er nye payloads. Eksisterende 95-HTML/PDF, begge beriktigede representasjoner og c5f3-forelderen gjenbrukes.

| Type | Eksakte felter |
| --- | --- |
| SourceRecipe | `id,document_key,parent_source_id,sidecar_source_id,object_start,object_end,prefix_bytes,suffix_start,separator_base64,expected_sha256,expected_bytes,status`; posisjoner/størrelse int, øvrige str |
| CoverageOverlay | `id,document_id,table_groups,table_fields,accounts,status,scope,historical_issue`; grupper/felt int, accounts tuple[str], øvrige str |
| PilotSource | `id,name,document_key,media_type,expected_sha256,content_base64,sha256,byte_count,status,metadata_json`; T1-felttyper |
| PilotDocument | `id,key,title,kind,session,date,raw_coverage,structured_coverage,professional_status,source_ids,accounts`; T1-felttyper |
| InventoryItem | `id,document_id,source_id,locator,chapter,post,role,structure_status,text,budget_year,observation_ids`; T1-felttyper |
| Statement | `id,document_id,source_id,locator,text,html,role,actor,period,status,accounts,hierarchy`; T1-felttyper |
| TreatmentContext | `id,observation_id,document_id,round,stage,actor,status,evidence_ids`; T1-felttyper |
| PilotRelation | `id,from_id,to_id,role,scope,status,accounts,evidence_ids,budget_year`; T1-felttyper |
| FieldBinding | `id,inventory_id,observation_ids`; T5-felttyper |
| Authorization | `id,document_id,source_id,locator,roman,point,role,period,accounts,frame_kr,text,html,status`; T5-felttyper |
| AmountObservation | Eksisterende observasjon-1 med SourcePointer og separat Interpretation; ingen nye felter |

Nye objekter bruker `identity(navnerom, asdict(objekt med tom id))` gjennom identified, med egne `innstilling95-*`-navnerom. Beløps-ID følger observasjon-1. Ukjente felter, feil typer, dangling refs og semantisk endring av rehashede objekter avvises ved full rekonstruksjon. Gamle ID-er/step_id/revisjoner/tolkninger/round=uavklart/status/råbyte beregnes aldri om.

Seks recipes rekonstruerer API 40034220–40034225 fra riktig c5f3-forelder og validerte sidevogner; ingen ekstra forelder/utdragspayload eller oppfunnet HTTP. 359: `parent[:317] + parent[2172545:2237039] + parent[7479886:7479943]`, 64868 byte, SHA256 `d4c473bf1ee95ec3edacce490586c0df5ec233d356e4c236fd9d765704b00490`. Øvrige grenser følger sidevognene. Metadata og faktisk forelder kontrolleres. Kilder/bindingspeker binder artifact-hash, eksakt lokator, råfelt og dokument/rolle. Ny faktisk saksrepresentasjon fra 23.10 erstatter ingen gammel B8-respons.

Lokatorpresisering fra den lokale originalkontrollen: 95-feltenes XPath gjelder hele HTML-representasjonen. 359-feltenes XPath gjelder HTML-verdien i XML-feltet `stortingsvedtak_tekst` i det rekonstruerte XML-artifactet. `field` skiller før/endring/etter der samme HTML-celle brukes. Source-unit, kilde-/tolkningsversjon, recipe og behandlingskontekst binder dokument/rolle; det er ikke en XPath direkte i XML-treet.

Gamle inns95 beholder `ikke_strukturert` og bred kontoliste i sin ID. Ny aktiv dekning følger eksakte bindings-/inventar-/relasjons-/coverage-objekter. 1533/45 og 1429 arver ingen T6-beløpsgren. T5s `ikke_strukturert_T6` og gamle avvik vises historisk; aktuelle T6-overlays vises separat. Vedtak359–364 binder API-ID, formelt nummer, sesjon, dato, recipe/source og faktisk kontoomfang.

## Faste faglige grenser

216 nye beløpsobservasjoner: 108 tilrådingsfelt fra 95 I og 108 vedtaksfelt fra 359 I, 36 kontoer/14 kapitler. Kildesystem `innstilling95`, NOK/heltall/multiplikator 1; hvert dokuments før/endring/etter deler step_id. Vedtaksstep binder sesjon/API40034220/kilde-/tolkningsversjon/konto, uavhengig av utvalg/navigasjon/støtte-HTML. 95 bruker komiteforslag/tilraading/samlet_komite; 359 stortingsvedtak, dokumentert nysaldering og enstemmig vedtakelse. Kontrollrepresentasjoner skaper ingen ekstra hendelser.

Ap/Sp/SV-, H- og FrP-merknader får egne Statement-objekter med avsender, periode, hierarki, tekst-/kontoomfang og tolkningsstatus. De blir ingen tallfestede alternativer eller Stortingets begrunnelse. Hele dokumentets seksjoner, tilråding I–VI og sluttopplysninger inventeres; fullteksten er bevart selv når nærmere faglig tolkning/postkobling mangler. Uberiktiget 95/rettelsesmelding er fortsatt globalt hull.

35 felles Prop.-trioer gir 105 beregnede nullforskjeller; 95→359 gir 108; T1s 12 består. Samme konto/år/NOK/enhet/betydning/runde/rolle/detalj/omfang og dokumentert relasjon kreves. 1420/32 mangler tre Prop.-felt: difference_kr=null, ingen nullpåfylling. 1420/32 = 812765000/+270000000/1082765000 i begge nye stadier. 4400/2 = 518000/-518000/0; observert null har ingen manglendegrunn.

| Frisk full T5-utvalg | Tabellfelt / vedtaksfelt / monetære hendelser |
| --- | --- |
| Hele unionen | 339 / 114 / 38 |
| Prop16 / inns95 / vedtak359 | 111/0/0; 108/0/0; 108/108/36 |
| Felles tabellkonto | 9/3/1 |
| 1420/32 | 6/3/1 |
| 1429/1 eller /22; begge | 9/3/1; 18/6/2 |
| Tekst/fullmakt/tomt/feil år | 0/0/0 med globale hull/inventar |

Fullmaktene har åtte atomiske inventarpunkter per nytt stadium (1+2+1+2+2). 95II→360: 8mill1420/21; III→361: separate 601mill1420/61 og266,3mill1420/62; IV→362: én delt16,3mill1420/39,/69,/79; V→363: stikkord1420/66,/87; VI→364: 25mill1471/1 mot4471/3 og separat regnskapsregel, samlede vilkår. Punkt/romertall er lokale dokumentidentiteter. PropV3→81II→211 består adskilt. Fem nye formelle fullmaktsvedtak pluss bevart211 er seks, uten monetær økning.

## Offentlige porter og avtalte tester

Analyse validerer gammel konvolutt og gir typed T5-basis til innlesningen uten analyseimport i kildeadapter. Offentlige porter: import_basis/structure_basis/validate_basis; build_report/open_document/open_accounts/go_back; read/export_json; read/export_excel/export_pair/export_originals. CLI `python -m analyse.innstilling95 --t5 FIL | --frosset FIL`, etablerte filtre/outputflagg. Dokumentåpning viser hele dokumentet, retur eksakt forrige utvalg; konto-/år er union av kapitler og eksakte par uten kryssprodukt. Begge innganger deler basis/observasjoner/hendelser og globale hull også ved tomt/feil årsvalg.

TDD ved #64s allerede avtalte offentlige grenser original→typed basis→begge innganger→faktisk skrevet/lukket/gjenlest JSON/XLSX, autentisk legacy og uavhengig ordinær vedtaksinnlesning. M01/M06–M08/M13/M15/M22–M28 prøves med hele95/359/360–364,32,felles utgift,4400/2,fullmakt/delt ramme,1429/1,/22,/60,1533/45,flere/kapitler,tomt/mangler/feilår og begge returer. Uavhengig originalfasit, semantisk rehashede negative filer og faktisk presentasjonskontroll inngår. Sikkerhet omfatter streng JSON, celletyper/formelvern/sikre lenker, tema/stiler/synlighet, ZIP/XML/gzip/chunks, tapsfri kilde og atomisk no-clobber.

Egen T6-ressursprofil: 512 beløpsfelt,16 dokumenter,64 kilder,4096 inventarposter,1024 utsagn,4096 relasjoner,64MiB JSON,16MiB råpayload,32MiB utpakket gzip,128MiB XLSX-utpakking. Gamle profiler forblir uendret. Konkrete grensetall og overgrensene prøves. Separate visuelle runtime/render-kontroller av faktiske produktfiler; native Excel påstås bare ved faktisk kjøring. Reproduksjonsbevis/skrevne filer og rå-/LF-/Git-binding skilles. Orkestrator eier fast kandidat, uavhengige review/audit/CI/Gitporter. Byggeren committer/pusher/merger ikke. Full lokal suite én gang til slutt; uendret CI-utvalg og90min beholdes. Ingen neste ticket. #10/#32/#37 står åpne.
