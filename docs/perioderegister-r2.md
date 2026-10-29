# P2: kildebundet R2-tillegg til perioderegisteret

Før-kode-kontrakt for [#56](https://github.com/depmartin/budsjetthistorikk/issues/56),
del av #37, 29. oktober 2026. Base er R2-merge
`c041ad8ed3e2f8316896b6ff2364d3470024a992`. Kontrakten fastsettes før
produktkode. Mandatet er produktadopsjon av akkurat de kontrollerte
[#54-funnene](research/r2-101000-54/README.md), med begge innganger,
faktisk skrevet/lukket/gjenlest JSON og Excel og selvforsynt offlinebruk.

## Faglig omfang og bevisgrenser

En separat opt-in `perioderegister-r2-1`, regel `periode1429-r2-54-1`,
bygger på én typet, uendret P1-Basis. `perioderegister-1`, gamle lesere,
identiteter, schema 5, B5 og standardvalg beholder sin betydning.
[P1-kontrakten](perioderegister.md) og pinnede K3/P1-filer endres ikke.
Tillegget oppretter ingen nye AmountObservation eller monetære hendelser.

Følgende tre grener utgjør hele det nye faglige omfanget:

1. **101000:** Prop. 34 S → Innst. 91 S → forslag 40077003/I og
   40077004/II → votering 23887 → vedtak 230/40034098 og 231/40034099.
   230 gjelder **1560/71, budsjett 2024**, økning 14 200 000 fra
   233 100 000 til 247 300 000 kroner. Dette er annen konto, vist som
   kilde-/behandlingskontekst uten en ny valgt 1429-hendelse. 231 er en
   generell lønnsregel uten konkret postbeløp. Faktisk anvendelse hos
   Riksantikvaren forblir uavklart. Samlet tilråding/enstemmig vedtak
   gjør ikke alle særmerknader til Stortingets felles begrunnelse.
2. **Prop. 36 S vedlegg 4:** 1429/1, 2024, selvstendig kildeobservert
   kompensasjonsanslag **2 796 000 kroner** med forslags-/anslagsrolle.
   Beløpet leses fra originalens tr293/td4, sammen med kapittelrad tr292,
   postcelle og enhet «Kroner», avgrenset av kapittel 1471 i tr294.
   Eksakt XPath er
   `/html/body/main/div/div[3]/div[3]/div/div/table/tbody/tr[293]/td[4]`.
   O1s `#kap2-p24` beholder avrundet 2,8 mill.; 5 796 000 − 3 000 000
   beholder rollen beregnet rest. Det nye kildebeviset endrer ingen av
   disse bevisrollene. /22 arver ingen lønnsforklaring eller nullverdi.
3. **100289/fullmakt 429:** Prop. 36 forslag II → Innst. 90 tilråding II →
   forslag 40078386 → votering 23945 → 429/40034289. Vedtaket gir FIN
   fullmakt om overføring av ubrukt drift til **2025**, knyttet til
   lønnskompensasjonen for **2024** og utsatt etterbetaling. Det nevner
   ikke 1429. Mulig /1-relevans gjennom vedlegg 4 er **betinget**, mens
   faktisk bruk, vilkårsoppfyllelse og beløp er uavklart. 2025 er et
   overføringsmål, aldri et nytt bevilgningsår eller kontinuitetsbevis.

Voterings-APIets −1 beholdes som rå sentinel, ikke stemmetall. De to
HTTP-representasjonene av 230/231 og deres kanoniske objektsamsvar
bevares hver for seg. 20./21. juni-konflikten og alle tolv
krysshenvisningers undersøkte delomfang/uavklarte rest består.
Ordfravær, tittel, beløpslikhet og felles sak beviser ingen postkobling
eller generell eksklusjon.

`year_coverage='partial'` og `professional_annual_balance_approval=false`
er rekonstruerte konstanter. 341→857→210 beholder **fem monetære
posthendelser/elleve vedtaksfelt**, gamle ID-er, verdier og regneinnganger.
Ingen øvrig R2, generell årsimport, T5/T6, positiv M21, kontokontinuitet,
faglig årsbalanse eller drift inngår. #10/#32/#37 står åpne.

## Lukket feltkontrakt

Konvolutten har nøyaktig `format,report`, med
`format='perioderegister-r2-1'`. Alle typer er immutable. Ukjente felter,
duplikatnøkler, feil typer og ikke-endelige tall avvises. Tupler blir
JSON-arrays. `null`, tom konto og tomt beløp betyr ukjent/ikke relevant;
de konverteres aldri til 0 eller til valgt år/post.

Rapporten har nøyaktig:

```text
id,basis,selection,return_selection,view,calculations,version
```

`selection,return_selection` bruker uendret PilotSelection;
`calculations` bruker P1s uendrede Calculation. `version` er formatnavnet.

Basis har nøyaktig:

```text
id,rule,p1_basis,payloads,sources,evidence,documents,inventory,statements,
relations,findings,status_updates,cross_references,issues,
year_coverage,professional_annual_balance_approval,version
```

`version='periodegrunnlag-r2-1'`; `p1_basis` er **én typet P1-Basis**,
ikke en ekstra P1-rapport/JSON-kapsel. Dens T4-basis og nødvendige
T1-kapsel forblir ordrette. Ingen separat kopi av gamle observasjoner,
dokumenter, kandidater, hull eller hele gamle rapporter lagres i nye felter.
Nye Payload/Source, PilotDocument, InventoryItem, Statement og
PilotRelation bruker de eksisterende typer. Gamle objekter refereres
med deres gamle ID-er. For allerede kjente Prop. 36 brukes det gamle
dokument-ID; nye representasjoner/omtale/inventar refererer dette ID.
Dokumentets ekstra rå-/strukturstatus opplyses additivt i de nye utsagnene,
uten at den gamle dokumentposten endres.

Nyt Evidence har nøyaktig:

```text
id,key,source_id,locator,nested_html_field_xpath,representation_sha256,
kind,role,text,rows_json
```

`key` er belegg-ID fra R2s evidence.json, ikke et nytt vilkårlig nummer.
`nested_html_field_xpath` er den opprinnelige indre HTML-feltlokatoren
eller null. `rows_json` er kanonisk JSON av tabellceller eller `null`.
`kind` bevarer XML/HTML; `role` bevarer beleggets rolle eller null når
forskningsbelegget ikke oppgir en egen rolle. Navnerom er den faste
`s=http://data.stortinget.no`. Tekst og celler kontrolleres mot den
hashbundne originalen med R2s oppgitte whitespace-regel. De 74
forskningsbeleggene beholder nøklene; feltprojeksjonen lager ingen nye
beløpshendelser. Arkivhash, metadatahash og dekomprimert representasjon
er separate bindinger. En lokator uten riktig representasjon er ugyldig.

Nytt Finding har nøyaktig:

```text
id,key,document_id,case_id,decision_api_id,budget_year,accounts,
conditional_accounts,transfer_target_year,post_link,role,actor,status,
reason,evidence_ids,amounts_json,proposal_ids,voting_id
```

`key` er `rows[].id` i treatment-ledger.json. Alle elleve ledgerposter
bevares med deres kildebundne innhold og roller. `accounts` betyr
uttrykkelig kontoomfang, mens `conditional_accounts` bare angir mulig
relevans under uttrykkelig vilkår. `post_link,role,status,reason` følger
ledgeren; aktør hentes fra kildens faktiske avsender. Ukjent aktør er
`ukjent`. Sak/vedtaks-/forslags-/voterings-ID-er er strenger eller
uttrykkelig null/tomt etter deres kardinalitet, aldri utledet fra tittel.
`evidence_ids` peker til nye Evidence-ID-er; ledgerens gamle beleggnøkler
bevares i hvert Evidence.key.

`amounts_json` er kanonisk, tapsfri JSON av ledgerens `amounts` eller
JSON `null`. Dette er en **lukket, kildefestet forskningsverdi**, ikke et
generelt brukerstyrt beløpsfelt. D230 beholder før/delta/etter med
kontoomfang 1560/71; FIN-1429-1 beholder
`source_observed_compensation_estimate=2796000` og
`adopted_new_event=null`; O1-OMDISPONERING beholder avrunding, rest og
formel. D231 og FULLMAKT429 har null beløp. Ingen slik verdi kan delta i
vedtaksteller, regneport eller B5 som en ny observasjon.

Nytt StatusUpdate har nøyaktig:

```text
id,case_candidate_id,case_id,index_session,ordinal_1based,status,reason,
evidence_ids
```

Det finnes én kildebundet oppdatering: sak 101000, sesjon 2024–2025,
ordinal 624, referanse til nøyaktig gammel P1-kandidat-ID.
Status er `hovedsak_undersokt_faktisk_postvirkning_uavklart`. Den viser
at hovedteksten er undersøkt separat, med direkte 230-omfang avklart og
231/429s faktiske anvendelse uavklart. Den gamle kandidatens status og
ID omskrives ikke. Historiske tall er fortsatt **67 indeksforekomster,
66 unike saker, 60 åpne indeksforekomster, 25 vedtakskandidater**; ingen
ny total eller generell lukking av R1/R2 beregnes. Oppdateringen er
globalt synlig også ved feil år, /22 og tomt valg.

Nytt CrossReference har nøyaktig:

```text
id,key,from_text,target,status,result,evidence_ids
```

Alle C01–C12 fra cross-reference-journal.json bevares med uendret
undersøkelsesgrense og beleggreferanser. `from_text` er journalens `from`.
Journalen gir ingen ny generell undersøkelse eller postkobling.

View har nøyaktig:

```text
p1,finding_ids,document_ids,status_update_ids,cross_reference_ids
```

`p1` er P1-View, rekonstruert fra samme basis og gamle beløpsvalg.
Et nytt dokument som ikke finnes i P1, gir tomt P1-beløpsvalg med
P1s globale dekning bevart; ID-en sendes ikke til en gammel leser som
om det var et gammelt dokument.
Gamle calculations gjenbrukes. `status_update_ids,cross_reference_ids`
er globale og ufiltrerte. P1s 67/25/7 og R1–R7 forblir synlige med
de gamle identitetene og historiske begrunnelsene. `finding_ids`
avgrenses etter bevist post/år eller uttrykkelig dokumentvalg.

## Begge innganger og dokumentinventar

Konto-/årsinngangen velger bare direkte 1429/1-anslag og dokumentert
omdisponering etter korrekt år/post. For /1 i 2024 vises dessuten den
avgrensede 101000-kjeden som **uavklart indirekte kontekst** og 429 som
**betinget fullmakt**. Disse vises med sine faktiske konti/år/roller;
1560/71 omskrives ikke til 1429/1. Ingen /22-lønnsbinding opprettes.
/22 beholder omdisponeringen og global oppdatering/restgrense; tomt
eller 2025-valg skaper ingen ny 2024-/2025-hendelse eller lønnsbinding.

Dokumentvalg viser hele det uttrykkelige dokumentinventaret uavhengig
av det tidligere kontofilteret. Prop. 34 og Innst. 91 har komplett bevart
hovedsak; begge romertall, den andre kontoen 1560/71 og generelle regel
må være tilgjengelige. Dokumentinngangen skal kunne åpne disse og de
tre vedtakene 230/231/429 direkte. Hele rårepresentasjoner med kildebevis
bevares offline; full råbevaring og eksplisitt delstrukturering skilles.
Innst. 90s øvrige monetære/mindretallsgrener er råbevart, men ikke
strukturert av denne leveransen. Prop. 36s tidligere inventar beholdes;
tillegget viser vedlegg 4s konkrete 1429-blokk og fullmaktsgren med
uttrykkelig grense. Ingen T5/T6 eller hel Prop. 36-adapter hevdes.

Dokumentrelasjoner er kildebeviste, mange-til-mange og avgrenser år,
rolle og kontoomfang. Generell regel/fullmakt og kildehenvisning får ikke
en falsk `proven_selected`-beløpskobling. Forhold til gamle Prop. 16/O1/
210-objekter bruker ID-referanser. Samme sak er bare saksrelasjon.
`open_document`, `open_accounts` og `go_back` beholder basis,
identiteter og opprinnelig utvalg/år. Ny kildeimport er valgfri;
allerede frosset input krever ikke nett, database eller originalrot.

## Identiteter, rekonstruksjon og kildegjenbruk

ID-er bruker uendret `identified(namespace,obj)` og kanonisk `encode`.
Nye navnerom er `periodegrunnlag-r2-1`, `periodekilde-r2-1`,
`periodebevis-r2-1`, `periodedokument-r2-1`, `periodeinventar-r2-1`,
`periodeutsagn-r2-1`, `perioderelasjon-r2-1`, `periodefunn-r2-1`,
`periodestatus-r2-1`, `periodekryssreferanse-r2-1` og formatnavnet.
Gamle ID-er beregnes aldri på nytt med et nytt navnerom. Nye
fullmakt-/forslags-/omtaleobjekter har ingen gamle event-ID-er som om
de selv var hendelser.

Den separate adapteren pinner de eksakte byte/hashene til R2s
source-manifest, reused-sources, evidence, treatment-ledger,
cross-reference-journal og source-comparison, alle 22 nye arkiv- og
metadata-par samt nødvendig gjenbrukt originalgrunnlag. Metadata
bevarer URL/ID, status, observasjonstid, representasjon og alle hasher.
Det feilede DNS-forsøket er bevart feilstatus/tom capture, aldri en
komplett original eller et fraværsbevis.

Forventet grunnlag rekonstrueres fra **kodepinnede ankere og faktiske
kildebyte**, ikke bare den innkommende filens selvhash. Leseren trenger
ingen repo-/originalfil etter frysning. Gjenbrukte P1/T4/T1-kilder og
payloads løses med ID-/digestreferanser; ingen ny råkopi av identiske
byte legges ved. Ulike HTTP-forsøk eller representasjoner beholder
egne kildeidentiteter. Komprimert original bevares én gang; en ekstra
full dekomprimert kopi lagres ikke per inngang/fane. Tidligere kapslers
arvede duplisering oppgis separat fra nye forekomster.

P1s grenser videreføres: 64 MiB rapport, 16 MiB enkelt arkiv-/metadata-
payload, 32 MiB dekomprimert original og 4096 inventarrader per dokument.
Tillegget har høyst 128 nye kilder/payloads, 128 belegg, 32 funn,
én statusoppdatering og 12 kryssreferanser; faktiske fixturestørrelser
måles før fullføring. Gamle grenser, ZIP/XML-/base64-/formelvern
endres ikke. Filbaner bindes til valgt rot; nye outputnavn og atomisk
publisering bevarer eksisterende filer. Ingen nettinnhenter innføres.

## Excel og kontrollporter

Fem hovedfaner beholdes: Forløp, Dokumenter, Omtale, Sammenligninger,
Dekning og avvik, med tilgjengelig Kontroll og én Offlinegrunnlag-kapsel.
Nye forskningsverdier står med avsender, rolle, år, faktisk/betinget
konto, originalreferanse, representasjonshash, lokator og status.
2 796 000 vises som **foreslått kompensasjonsanslag** i egen tydelig
verdi-/rollekontekst; det fylles ikke i vedtatt endring for 1429.
429 vises uten beløp med overføringsmål 2025 og faktisk bruk uavklart.
Historisk dekning, det separate nye status-tillegget og åpne R1–R7
vises samtidig, også når beløpsutvalget er tomt.

Den ene kapselen inneholder samme nye JSON som filen. Synlige celler,
typer, tallformat, interne ID-lenker, lange tekster og ark-/rad-/kolonne-
synlighet avstemmes mot den rekonstruerte boken. Rå stil-/rotrelasjons-
vern fra P1s auditretting videreføres. Containeraksept alene beviser
ikke semantisk eller synlig riktighet. Rendering dokumenteres med
faktisk verktøygrense; native Excel påstås bare hvis faktisk prøvd.

Faktiske skrevne/lukkede/gjenleste JSON-/Excel-par prøves for /1,
/22, begge, dokument 230/231/429/Prop. 34/Innst. 91/Prop. 36, feil år og
tomt utvalg, navigasjon/retur, gjentatt eksport og offentlig offline-CLI.
Kilder/ID-er/hasher/representasjoner/lokatorer/år/avsender/rolle/
relasjoner avstemmes mellom inngangene og filene. Ufiltrert 2024 beholder
5/11, /1 beholder 3/7 og /22 beholder 2/4; de nye dokumentene har ingen
valgte 1429-vedtaksfelt/hendelser.

Rehashede negative filer skal nå semantisk port og avvises for:

- anslag som vedtak, O1-avrunding/rest som eksakt primærbeløp;
- fullmakt som faktisk overføring eller ny 2025-bevilgning;
- uberettiget /22-binding, feil kilde, rolle, år eller aktør;
- feil forslag/votering/vedtaksrelasjon, lokator eller representasjon;
- skjulte hull/kandidater/statusoppdatering, positiv M21/årsbalanse;
- endrede gamle identiteter, observasjoner, kapsler eller dupliserte payloads.

Excel-negative par får konsistente kapseldimensjoner før semantisk
avvisning. Egne prøver dekker falsk/skjult presentasjon, eksterne lenker,
formler, ZIP/XML, ressurser og ikke-tapsfri tekst. Ekte eldre filpar leses
med gamle lesere fra hashkontrollerte kopier, uten endrede originaler.
Fire separate ordinære 368-forløp prøves gjennom offentlig registrering,
råbevaring, lagring, tolkning og Excel ved manglende, feilet, korrupt og
motstridende tillegg, uten historisk Excel; schema 5/B5/standard består.

Samlet Standards/Spec og separat sikkerhetsaudit vurderer samme faste
kandidat. Relevante tester/statisk kontroll og full uendret Linux-CI
består før merge. Gjeldende 90-minuttersgrense og hele testutvalget
beholdes. Manifest, hasher, kandidatbindinger, faktisk leveringsstatus,
bevisgrenser og overlevering lagres separat for denne nye ticketen.
R2/K3/P1s historiske manifestbindinger og kandidatbundne «gjenstår»-status
omskrives ikke. Ny ticket etter denne leveransen starter ikke automatisk.

## Smal modulgrense

Innlesning eier nye immutable typer, fast katalog, kildebevaring og
kildebundet rekonstruksjon i separate `perioderegister_r2`-moduler,
uten analyseimport. Analyse eier utvalg, navigasjon, streng JSON,
Excel og CLI. P1s offentlige funksjoner gjenbrukes for det uendrede
grunnlaget og regneporten; gamle parser-/skriverbaner utvides ikke.

Den nye offentlige grensen følger de eksisterende pilotene:
`import_basis(root, *, t1_json='')`, `build_report(basis, selection,
return_selection=...)`, `open_document`, `open_accounts`, `go_back`,
`report_to_json`, `report_from_json`, `read_json`, `export_json`, samt
Excelmodulens `read_excel`, `export_excel`, `export_pair` og
`export_originals`. Frosset CLI-input velger eksplisitt det nye formatet.
Dette er et lite tillegg, ikke et nytt generelt import- eller
registerrammeverk.
