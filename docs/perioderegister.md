# P1: delvis K3-perioderegister for 1429/1 og /22 i 2024

Før-kode-kontrakt for [#52](https://github.com/depmartin/budsjetthistorikk/issues/52),
del av #37, 28. oktober 2026. Startgrunnlag er fersk main
`29ac220f62b35062fc4203f054e2f757ca795b7c` etter K3/#50/PR #51.
Kontrakten fastsettes før produktkode. Mandatet omfatter akkurat P1 med
PR, uavhengige porter, full CI og merge; #10/#32/#37 forblir åpne.

## Resultat og faglig grense

Én separat opt-in `perioderegister-1`, regel `periode1429-2024-1`, viser
det frosne K3-registeret fra dokumentinngangen og konto-/årsinngangen.
Formatnavnet er ikke T5 og starter ingen T5/T6-leveranse.

Perioden er uttrykkelig delvis. Råkildebevaring, postkobling, strukturering,
faglig kontroll og monetær vedtaksvirkning er separate opplysninger.
`year_coverage='partial'` og `professional_annual_balance_approval=false`
er rekonstruerte konstanter. Ingen positiv M21, årssaldo, kontinuitet eller
ny B5-avgjørelse følger av dette registeret.

341/40032928 → 857/40033719 → 210/40034048 beholder sine gamle objekter,
ID-er, felt og fem monetære posthendelser/elleve vedtaksfelt.
346/40032933, 19.12.2023, er en egen merinntektsfullmakt på 1429/1 for
budsjett 2024 mot 4429/2 og /9. Den har tekst, dokument, postkobling og
voteringsbevis, men ingen ny AmountObservation eller monetær hendelse.
Sak95776/votering22032/forslag40073889 gjelder fullmakten; forslag40073884
gjelder 341. Samme votering erstatter ikke disse separate forbindelsene.

Originalforslag, tilråding, H-/FrP-standpunkter, sju forkastede RNB-pakker
og Prop.36s vedtatt-eller-foreslått-status vises med egne kilder og roller.
Registertekst kan vise deres råtall uten å normalisere dem til nye
beløpsobservasjoner. Originalalternativenes separate primærvotering er
ukjent; ingen forslag-ID, stemmetall eller utfall oppfinnes.

## Lukket filkontrakt

Konvolutten har nøyaktig `format,report`. Alle objekter er immutable,
feltnavn er lukkede, og ukjente felter avvises. Tupler serialiseres som
JSON-arrays; `null` er eksplisitt ukjent og blir aldri 0 eller 2024.

Rapport:

```text
id,basis,selection,return_selection,view,calculations,version
```

`selection` og `return_selection` bruker uendret PilotSelection;
`calculations` bruker uendret Calculation. `version='perioderegister-1'`.

Basis:

```text
id,rule,t4_basis,payloads,sources,evidence,documents,inventory,statements,
relations,entries,case_candidates,decision_candidates,gaps,issues,
year_coverage,professional_annual_balance_approval,version
```

`version='periodegrunnlag-1'`. `t4_basis` er én typet, validert og uendret
T4-Basis, ikke en ekstra serialisert T4-rapport. Den inneholder sin ene
ordrette T1-kapsel. Ingen ekstra T1/T2/T3/T4-kapsel eller kopiert gammel
observasjonsliste legges i nye felter. Nye `payloads,sources` bruker
Payload/Source-kontraktene fra T2; nye `documents,inventory,statements,
relations` bruker PilotDocument/InventoryItem/Statement/PilotRelation.
Gjenbrukte gamle objekter refereres med ID og serialiseres bare i
`t4_basis`/dens opprinnelige kompatibilitetskapsel.

Ny Evidence har nøyaktig:

```text
id,source_id,locator,representation_sha256,role
```

`source_id` kan peke til en ny kilde eller en uendret kilde i T4/T1-unionen.
Lokatoren gjelder den eksakte representasjonen, ikke et vilkårlig senere
HTTP-svar. `representation_sha256` bindes til faktisk rå-/avledet innhold;
arkivhash og dekomprimert hash holdes adskilt i kildens metadata.

Ny PeriodEntry har nøyaktig:

```text
id,key,document_id,decision_api_id,case_id,budget_year,accounts,
post_link,role,round,actor,status,reason,evidence_ids,
observation_ids,event_ids,professional_status
```

`key` er original `rows[].id` fra known-period-ledger.json.
`decision_api_id,case_id` er streng eller null; `budget_year` er heltall
eller null. `accounts` er konkrete kapittel/post-strenger. `post_link` er
`proven_selected`, `proven_other_scope` eller `unknown`. Tom konto betyr
ikke 1429/1 eller /22. `round` er `opprinnelig`, `rnb`, `nysaldering`,
`kontroll` eller `uavklart`, kildebegrunnet og separat fra gamle
observasjoners `round='uavklart'`. `role` bevarer den konkrete K3-rollen;
`actor` angir kjent avsender eller `ukjent`. `status,reason` bevarer den
faktiske undersøkelsesgrensen; `professional_status='ikke_faglig_godkjent'`.
Bare de tre allerede kjente monetære vedtaksleddene kan referere gamle
`observation_ids,event_ids`; andre oppføringer har tomme slike tupler.

Ny CaseCandidate har nøyaktig:

```text
id,index_session,ordinal_1based,case_id,document_id,metadata_json,
budget_year,accounts,post_link,status,reason,evidence_ids
```

Alle 67 indekskandidatposter bevares, herunder de to indeksforekomstene
av samme sak. `metadata_json` er kanonisk, tapsfri JSON av K3s komplette
metadataobjekt. Identitet bruker indeksens sesjon og ordinal samt
kildeversjon; `case_id` alene kan ikke være radnøkkel. Status er de
eksisterende `investigated_case_references` (7) eller
`open_title_candidate` (60). Undersøkte saksreferanser betyr ikke bevist
postkobling. År/konto forblir null/tomt/unknown uten konkret kildebevis.

Ny DecisionCandidate har nøyaktig:

```text
id,session,decision_api_id,number,document_id,budget_year,accounts,
post_link,status,reason,raw_preservation,product_structuring,
professional_approval,monetary_effect,evidence_ids
```

Alle 25 journalposter bevares med egne inkluderings-/ekskluderingsgrunner
fra coverage-journal.json og full autoritativ objektidentitet fra
decision-register.json/den hashbundne sesjonsoriginalen. Kjente andre år
bevares som 2023/2025; ukjent år forblir null. Ekskluderte poster er fortsatt
tilgjengelige i global dekning og som dokumentvalg.

Ny CoverageGap har nøyaktig:

```text
id,key,title,status,reason,evidence_ids
```

Det finnes nøyaktig sju globale poster `R1`–`R7`, alle med `status='open'`,
med faktisk restomfang fra m21.md. De omfatter blant annet de 2 158
ordløse vedtaksobjektene og 60 åpne indekskandidatposter/59 unike saker.
K3s frosne 2 183-vedtaks- og 1 364-indeksunivers beholdes gjennom
kilde-/registerreferanser; 25 treff er ikke hele universet.

View har nøyaktig:

```text
monetary,entry_ids,document_ids,case_candidate_ids,decision_candidate_ids,gap_ids
```

`monetary` er PilotView for gamle monetære objekter innen P1s eksplisitte
2024-omfang. De øvrige ID-listene er nye registerprojekteringer.
`case_candidate_ids,decision_candidate_ids,gap_ids` omfatter alltid alle
67/25/7, også ved dokumentvalg, feil år og tomt utvalg. `entry_ids` avgrenses
av bevist konto/år eller valgt dokument. Ukjente kandidater beholdes i
global dekning, uten å bli konstruerte kontotreff.

## Identitet, rekonstruksjon og kildegjenbruk

Identiteter bruker eksisterende `identified(namespace,obj)` og kanonisk
`encode`; ID-feltet utelates/tømmes etter den eksisterende regelen.
Navnerom er `periodegrunnlag-1`, `periodekilde-1`, `periodebevis-1`,
`periodedokument-1`, `periodeinventar-1`, `periodeutsagn-1`,
`perioderelasjon-1`, `periodeledd-1`, `periodesakskandidat-1`,
`periodevedtakskandidat-1`, `periodehull-1` og `perioderegister-1`.
Payload-ID-regelen gjenbrukes uendret; eksisterende objekt-ID-er beregnes
aldri på nytt med P1-navnerom. Dato/sesjon/navnelikhet etablerer ingen
års-, post- eller kontinuitetsrelasjon.

Innlesning eier kildebevaring og kildebundet registerstrukturering, uten
analyseimport. Analyse eier utvalg, navigasjon, regnekontroll, visning,
streng filgjenlesing og Excel. Forventet basis og rapport rekonstrueres
fra fast kode-/kildekatalog, aldri bare fra innkommende selvhash.
Validering skal finne feil selv etter konsistent rehashing av hele filen.

K3-JSON-filenes eksakte byte/hash og benyttede originalarkiver/metadata
pinnes i den nye adapterens uttrykkelige katalog før produksjon av basis.
coverage-journal, case-candidates, known-period-ledger, decision-register,
decision-evidence, table-locators, voting-evidence og m21 inngår som
register-/bevisgrunnlag med egne roller. source-manifest/reused-sources
bevarer transport- og gjenbruksreferanser. Bevarte indeksoriginaler
binder sesjon/ordinal/metadata; 346 bindes til komplett 66aa-forelder og
fullmaktsteksten. Alle nye statuser og bevisreferanser må kunne gjenfinnes
fra dette selvforsynte grunnlaget offline.

Råpayloads dedupliseres fysisk etter identiske byte, med referanser til
T4/T1-payloads der mulig. Ulike HTTP-forsøk, ulike metadata og ulike
representasjoner beholder egne Source-objekter. Komprimert originalarkiv
bevares én gang; en ny full dekomprimert HTML-kopi skal ikke legges inn
ved siden av arkivet for hver visning. Innst.447s 28,6 MB fulle HTML skal
ikke sendes gjennom den gamle 16 MiB-kildeporten som rå HTML. Bevar gzip,
validert dekomprimering og egne begrensede P1-porter. Manglende nødvendige
kilder gir synlige mangler, aldri verifisert fullstendighet.

P1 beholder 64 MiB rapportgrense, 16 MiB enkelt arkiv-/metadatapayload,
32 MiB dekomprimert original, 4096 inventarrader per dokument og 512 nye
kilder. Nye samlinger har faste tak: 256 registerledd, 67 sakskandidater,
25 vedtakskandidater, 7 hull og 4096 bevisobjekter. Komplette fixturedata
skal måles mot disse takene før fullføring. Gamle 512-/4096-grenser og
ZIP/XML-/base64-vern endres ikke. Ingen generell nettinnhenter innføres.

## Innganger, dokumentinventar og Excel

PilotSelection beholder union av eksplisitte kontopar/kapitler innen valgte
år, uten kryssprodukt. P1s monetære område er bare 1429/1,/22 og 2024;
andre år/tomt valg gir null monetære felt/hendelser. T4s 201/2025-grunnlag
kan bevares uendret som tidligere grunnlag, men oppretter ingen P1-kjede.
Ekskludert 201 er fortsatt en begrunnet journalpost, ikke en 2024-hendelse.

Dokumentvalg viser hele det uttrykkelige dokumentinventaret og dets
rådekning/strukturgrense, uten opprinnelig kontofilter. Eksisterende
T1/T3/T4-dokumenter gjenbruker hele gamle inventar. 346 viser komplett
vedtaksobjekt/fullmaktstekst og alle dets inventerte kontohenvisninger.
En ny indekskandidat er et indeksdokument: komplett indeksobjekt og
kildelokator er inventaret; ikke-hentet publikasjon/fulltekst merkes som
manglende. Øvrige nye registerdokumenter viser komplette kildebundne
registeroppføringer/bevispassasjer og originalreferanser, uttrykkelig
delvis strukturert. De hevder ikke en generell fullstrukturering av
Prop.1/104/447. Dokumentets erklærte inventar kan ikke begrenses av valgt
post; ingen post arver en sammenheng fra felles sak alene.

`open_document`, `open_accounts` og `go_back` bevarer samme basis,
objektidentiteter og opprinnelig utvalg/år. CLI støtter frisk kildeimport
og allerede frosset P1-input, samme to innganger og nye outputnavn.

Excel viderefører fem hovedfaner: Forløp, Dokumenter, Omtale,
Sammenligninger og Dekning og avvik; Kontroll og Offlinegrunnlag er
tilgjengelige. Registerledd/fullmakt vises i Forløp med rolle, år,
postkobling, originalreferanse, lokator og status, uten tall i
bevilgningskolonner for ikke-monetære ledd. Dokumenter viser globale
kandidater og valgt dokumentinventar; Dekning og avvik viser R1–R7,
67/25-statusgrunnlaget og konstant delvis dekning også ved tomt valg.
ID-baserte interne lenker forbinder samme dokument-/kontoårsgrundlag.
Lange tekster deles tapsfritt. Én Offlinegrunnlag-kapsel indeholder de
samme P1-JSON-byte, ikke en kapsel per fane. Synlig presentasjon skal
avstemmes mot kapselen; celleverdi alene er ikke visningsbevis.

## Akseptporter

Faktiske filer skal skrives, lukkes og gjenleses. Intern objektlikhet
eller eksisterende filnavn er ikke tilstrekkelig. Vertikale TDD-prøver
dekker autentisk original → register/fullmakt → dokumentert relasjon →
begge innganger → JSON/XLSX/offline.

| Valg | Vedtaksfelt | Monetære hendelser |
| --- | ---: | ---: |
| 2024 /1 | 7 | 3 |
| 2024 /22 | 4 | 2 |
| 2024 begge eller kapittel1429 | 11 | 5 |
| Dokument341 | 2 | 2 |
| Dokument857 | 3 | 1 |
| Dokument210 | 6 | 2 |
| Fullmakt346, ukjent indekskandidat, feil år eller tomt | 0 | 0 |

Alle tilfeller beholder globalt 67/25/7, rå-/struktur-/faglig status og
samme fem/elleve i ufiltrert 2024-grunnlag. Gamle tabellfelt/observasjoner
og uendret 2024-regneport kontrolleres separat: 166039000 og 29185000,
bare status *avgrenset kontroll* og eksakte gamle inngangs-ID-er.

Nødvendige prøver omfatter:

- Begge navigasjonsretninger og retur for /1,/22,begge,346,åpen kandidat,
  feil år og tomt; hele dokumentinventaret og gjentatt eksport består.
- Alle 67 indeksforekomster/66 unike saker, 7 undersøkte/60 åpne,
  alle 25 begrunnelser og alle R1–R7 avstemmes mot pinnet K3-grunnlag.
- Faktiske JSON-/Excel-par og offentlig CLI leses/eksporteres med sperret
  nett/SQLite og utilgjengelig originalrot. Ingen repositoriefil er en
  skjult avhengighet etter frysning. Kildereferanser kan gjenfinnes offline.
- Rehashede feil i kildehash/forelder/lokator, år, post, rolle, kandidat-
  ordinal, identitet, status, 346-beløp, alternative forslags vedtaksrolle,
  Prop.36 som hendelse, positiv årsdekning og skjulte globale hull avvises.
  Excel-angrep skal nå semantisk kontroll med konsistente kapseldimensjoner.
- Falsk/skjult Excel-presentasjon, formler/eksterne lenker, ZIP/XML-angrep,
  ressursgrenser, dupliserte payloads og ikke-tapsfri tekst avvises.
  Faktisk celle/type/tallformat/lenke/synlighet og rendering kontrolleres.
- Ekte tidligere A/B/B6/B8/B9/T1/T2/T3/T4 gjenleses fra hashkontrollerte
  kopier; gamle originaler bevares. Uforanderlige kapslers gamle fysiske
  duplisering oppgis separat fra nye payload-/objektforekomster.
- Fire separate autentiske 368-forløp gjennom offentlig ordinær
  synkronisering, råbevaring, lagring, tolkning og Excel består ved
  manglende, feilet, korrupt og motstridende P1, med tomt P1-valg og uten
  historisk Excel. Schema5/B5/standardvalg og gammel parserbetydning består.

Samlet Standards/Spec og separat sikkerhetsaudit vurderer samme fryste
kandidat. Relevant fullsuite, Ruff/format/mypy og hele Linux-CI skal bli
grønne; ingen test-/parserversjonslogging fjernes for tidsmargin. Faktiske
manifesthasher, fil-/renderingsbevis, kandidatbinding, reproduksjon og
overlevering lagres. Eksisterende 60-minutters CI-grense er startpunkt,
ikke garanti for ny kjøretid. Native Excel og de tidligere dokumenterte
manglende gamle originalene omtales bare med faktisk bevis. Ingen neste
ticket starter automatisk.
