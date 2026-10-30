# T5/#62: lokal bygge- og kontrollleveranse

29. oktober 2026. Fra publisert base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b` på isolert `codex/t5-prop16`.
Dette er byggerens lokale leveranse, uten commit, PR, samlet egenreview,
sikkerhetsaudit, full Linux-CI eller merge. Disse portene eies av orkestrator.
Gjeldende leveringsstatus skal føres i [#62](https://github.com/depmartin/budsjetthistorikk/issues/62).

[Kontrakten](../../proposisjon16.md) ble skrevet før produktkode. Formatet
`proposisjon16-1` har én uendret typet T1-kapsel, 105 nye forslagfelt og egne
bindings-, deknings-, fullmakts- og grenobjekter. Gamle inventar-ID-er og
råpayloadreferanser gjenbrukes. Ingen gamle produktmoduler eller fixtures endres.

Hele tabellen har **37 trioer / 111 forslagfelt / 15 kapitler**, fordelt på
27 utgift og 10 inntekt. Unionen har **123 felt / seks vedtaksfelt / to
monetære hendelser**. T5 legger ikke til vedtatte beløpshendelser.
4400/2s etterbeløp er ekte numerisk **0**. Alle 45 kontoangivelsene består,
også tekstkontoer og kapittel 1533 utenfor de 15 tabellkapitlene.

II–VI vises som ni atomiske inventarpunkter. IV har én delt ramme på
16,3 mill. kroner for tre kontoer. De to saksgrenene og V.1–2/V.3 har presist
omfang; 1533/45 får ingen automatisk søstergren. Innst. 95s beløpsstadium
forblir ustrukturert. Begge bevarte beriktigede HTML-representasjoner har
egne råhasher; ukjent rettelseshistorikk beholdes.

T1s `delvis_1429` inngår i gammel dokument-ID og er uendret. Et separat
identifisert overlay angir gjeldende tabellstatus. Excel skiller historisk
T1-status fra gjeldende T5-status, også i konto-/inventararkene.

## Kontrollpakken

- [Kildebevis og bevaringsgrense](kildebevis.md).
- [Akseptmatrise](akseptmatrise.md).
- [Kompatibilitetsbevis](kompatibilitetsbevis.md).
- [Reproduksjon i ny klon](reproduksjon.md).
- [Faktiske kontrollutfall og TDD](kontrollutfall.md), [TDD-journal](tdd-journal.json).
- [111 felt, kilder, fullmakter, grener og 14 faktisk gjenleste filpar](source-control.json).
- [Separat originalkontroll av ni fullmaktspunkter og åtte formelle grenlokatorer](raw-source-controls.json).
- [Kildeinventar](source-manifest.json) og [leveransemanifest](delivery-manifest.json).
- [Visuell Excel-QA](excel-qa.md), med faktiske renderinger i `visual/`.

Kontrollhjelperen [ops/proposisjon16_proeve.py](../../../ops/proposisjon16_proeve.py)
bruker kildemateriale og autentisk T1-fixture i klonen, aldri utilgjengelige
lokale commits. Kandidat/base kan gis som publiserte Git-referanser. Byggerens
kildefasit er separat fra produktparseren, men dette erstatter ikke en
uavhengig kontrollør på fast kandidat.

## Åpne grenser

Native Excel og lokal Excel-lokalisering er ikke prøvd. Kontrolldata, lange
ID-er og råtekst vises som celleforhåndsvisninger; hele verdien finnes i cellen
og ordnede tekststykker. Ingen full semantisk tolkning, T6, U1/C06-adopsjon,
helårsdekning, kontokontinuitet, faglig årssaldo eller drift inngår.
Hele tidligere CI-utvalg og 90-minuttersgrensen består. #10/#32/#37 står åpne.
