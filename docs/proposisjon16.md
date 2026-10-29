# T5: hele den faste Prop. 16 S-tabellen

Felt-, identitets- og testkontrakt fastsatt 29. oktober 2026 før produktkode,
innen den publiserte og eierautoriserte [#62](https://github.com/depmartin/budsjetthistorikk/issues/62).
Opt-in-formatet er `proposisjon16-1`, regelen `prop16-tabell-1`.
T1, ADR 0011, observasjon-1, schema 5, B5 og gamle standardvalg består.

## Lukket modell

Alle modeller er immutable dataclasses. JSON-konvolutten har nøyaktig `format`
og `report`. Rapporten har `id,basis,selection,return_selection,view,version`.
Selection og PilotView beholder T1s felt og semantikk. View rekonstrueres ved
lesing; lagrede avledninger er ingen autoritet.

Basis har nøyaktig `id,rule,t1_basis,sources,observations,contexts,bindings,coverage,
authorizations,branches,issues,version`. `t1_basis` er én uendret typet
`PilotBasis`, ikke en analysekonvoluttstreng. Den inneholder alle gamle
dokumenter, inventar, råpayload, observasjoner, relasjoner og avvik. Nye
observasjoner er bare de resterende 35 trioenes 105 forslagfelt. Ingen gamle
råpayload eller beløpsobjekter serialiseres på nytt utenfor kapselen.
`sources` er tuple[PilotSource] for bare den tidligere bevarte 22.10-
representasjonen av 95 og dens gjenbruksmanifest, som ikke ligger i T1.
23.10-representasjon/PDF og vedtaksforelder gjenbrukes gjennom gamle kilde-ID-er.
Ny katalog har samme 16 MiB/base64-grense, pinnet SHA-256 og eksplisitt
mangler/motstrid; ingen reservehenting. Rekonstruksjon sammenligner hovedtekst
i de to bevarte HTML-representasjonene og hevder ingen rettelseshistorikk.

| Modell | Eksakte felter |
| --- | --- |
| FieldBinding | `id,inventory_id,observation_ids` (str,str,tuple[str]) |
| DocumentCoverage | `id,document_id,table_groups,table_fields,account_count,status,scope,historical_issue` (str,str,int,int,int,str,str,str) |
| Authorization | `id,document_id,source_id,locator,roman,point,role,period,accounts,frame_kr,text,html,status` (str-felt, accounts:tuple[str], frame_kr:int\|null) |
| Branch | `id,from_document_id,to_document_id,case_id,accounts,point,committee_point,decision_ids,evidence_ids,status,amount_stage` (str-felt, tuple[str]-felter: accounts/decision_ids/evidence_ids) |

ID-er bruker `identity(navnerom, asdict(objekt med tom id))` gjennom den
etablerte identified-hjelperen. AmountObservation/SourcePointer/Interpretation
følger observasjon-1, med eget kildesystem proposisjon16 og egen tolkningsregel.
De seks gamle Prop.-feltene, seks Innst.-feltene og seks vedtaksfeltene beholder
alle felter og identiteter, step_id, round og kontrollstatus. Den gamle
Prop.-dokumentpostens `structured_coverage=delvis_1429` inngår i ID og beholdes.
Et identifisert coverage-overlay peker på denne ID-en og angir gjeldende T5-
dekning; det gamle avviket er eksplisitt historisk. Ingen faglig årsdekning følger.

## Faste faglige grenser

37 tabellgrupper / 111 forslagfelt / 15 tabellkapitler: 27 utgift og 10 inntekt.
Frisk union har 123 felt / 6 vedtaksfelt / 2 monetære hendelser. Prop.-valg har
111 felt. 1429/1 og /22 har hver 9/3/1, sammen 18/6/2. Andre tabellkontoer har
3/0/0. Tekst/tomt har 0 felt med global dekning. 4400/2 er
518000, -518000, **0**; ekte heltallsnull får ingen nullgrunn.

De 45 unike kontoangivelsene er 37 tabellkontoer, tre ekstra stikkordkontoer og
fem andre referanser. Hele inventaret omfatter også kapittel 1533. II–VI har
fem romertall og ni atomiske innholdspunkter (1+2+1+3+2). IV er én delt
16300000-kroners ramme for 1420/39,/69,/79; ingen ramme er bevilgningsdelta.
Råtekst, lokator, periode og kontoomfang bevares; formelle vedtak er separate.

Tabellens 1429-grupper går til 100927/81/210–211; øvrige tabellgrupper til
100889/beriktiget 95. Prop. V.3 → 81 II → 211; V.1–2 → 95 V → 363.
Ingen automatisk gren på kontekstreferansen 1533/45. Innst. 95s beløpsstadium
forblir ustrukturert; ingen differanse Prop.→95 beregnes. Separate bevarte
representasjonshasher er ingen rekonstruert rettelseshistorikk.

## Offentlige grenser

Analyse importerer T1-konvolutt og gir typed PilotInput/PilotBasis til
innlesning. Innlesning importerer aldri analyse. Offentlige porter:
`import_basis/structure_basis/validate_basis`, `build_report/open_document/
open_accounts/go_back`, `read_json/export_json/report_from_json/report_to_json`,
`read_excel/export_excel/export_pair/export_originals` og
`python -m analyse.proposisjon16 --t1 FIL | --frosset FIL` med etablerte filtre
og outputflagg. Dokumentåpning viser hele inventaret; retur gjenoppretter
opprinnelig utvalg. År avgrenser unionen av kapitler og eksakte kontopar.

## Avtalte tester og vern

#62 har allerede bekreftet original → typed basis → begge innganger/navigasjon
→ faktisk skrevet/lukket/gjenlest JSON/XLSX, samt autentisk legacy og uavhengig
ordinær vedtaksregistrering. Ett observerbart rødt→grønt snitt av gangen.
Fasit kommer fra originale rader og eksisterende uavhengig kildeinventar,
aldri en ny kjøring av produktparseren alene.

M05, M13–M14, M22–M28 prøves med utgift, inntekt/null, tekst, flere/tomt,
hele Prop. og begge returveier. Semantisk rehashede negative filer skal nå
leseren for rolle/beløp/år/null/konto/gren/ramme/gammelt ID/dekning. Streng JSON,
ekte celletyper, tekst/formelvern, hyperlenker, synlighet/stiler, ordnede chunks,
ZIP/XML/gzip/base64-grenser og atomisk no-clobber beholdes med eksisterende
guardprofiler. Ekte `tests/fixtures/t2/authentic-t1.json.gz` leses med gammel
leser. 40034229 registreres ordinært ved manglende/feilet/korrupt/motstridende
T5. Delte dyre fixture-/eksportgrunnlag begrenser CI-tiden.

T5-leseren binder også hele `xl/theme/theme1.xml` byte for byte til den
eksisterende skriverens faste openpyxl-tema. Pakkprofilen binder temarelasjon
og innholdstype; stil- og cellekontrollene binder bruken. Dette omfatter både
farger og temaskrift, også der cellefonten bruker `theme`/`scheme`. Alternative
temapayloads avvises selv om kapselen og celleverdiene er uendret. Skriveren,
eksportinnholdet og eldre formaters guardprofiler endres ikke.

Excel er bestilt produkteksport med eksisterende openpyxl. Separat visuell QA
av faktiske filer bruker loader-runtime/render der tilgjengelig; celleassert
alene er ingen visuell aksept. Begrensninger og konkrete feilforsøk lagres.
Relevante tester og hele Ruff/format/mypy kjøres lokalt. Orkestrator eier
uavhengige kilde-/Standards/Spec-/sikkerhetsporter, publisering, full uendret
Linux-CI med 90 minutter og autorisert merge. Byggeren gjør ingen GitHub-
mutasjon, staging, commit eller samlet egenreview.

Ingen T6, generell parser/årsimport, GUI, U1/C06-adopsjon, positiv M21,
kontokontinuitet, faglig årssaldo eller drift. Gamle basefiler bevares med
unntak av korte additive AGENTS-/kildefunnpekere.
