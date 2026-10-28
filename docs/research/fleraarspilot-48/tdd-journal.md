# Byggejournal T4/#48

Den avtalte testgrensen i kontrakt/#48 er autentisk original → kildebundet
felt/tekst → dokumentert relasjon → begge innganger → faktisk skrevet,
lukket og gjenlest JSON/Excel. Implement- og TDD-filene i Matt Pocock-plugin
1.3.1 ble lest og fulgt ved disse allerede godkjente grensene.
Byggermandatet unntar individuell review/commit; orkestratoren eier portene.

Forrige byggers uferdige, utrackede filer ble bevart. Første nye kontroll av
`test_original_201_has_2025_levels_complete_inventory_and_unknown_continuity`
var rød: 2025 ga 0 felt og rapporten var fortsatt `visningspilot-3` fordi
analysefilen var en uendret T3-kopi. Etter separat T4-adapter/analyseimport
og avgrensing av sammenligning/regning ble prøven grønn (1 bestått, 1,56 s).

Neste vertikale prøve skrev/gjenleste flerårsfilpar, kontrollerte arvede ID-er,
lokale 2024-beregninger og sortering. Den var først rød: Excel-kopien brukte
T3s skriver/leser og avviste T4-kildeinventaret. T4-skriveren ble knyttet til
sin egen konvolutt/leser, års-/kontogruppering og årsspesifikke lenker.
Begge prøver bestod deretter (2 bestått, 36,14 s).

To første forsøk på filprøven nådde ikke produktet: pytest hadde ikke skrivbar
standard tempkatalog, deretter manglet overmappen til eksplisitt basetemp.
Det ble opprettet en lokal `work/`-mappe og brukt nye basetempkataloger i
checkoutet. Ingen produktvern ble endret for å løse miljøproblemet.

Deretter ble regresjons-/akseptkontrollen utvidet til tellerutvalg, navigasjon,
faktiske filpar, offline CLI uten nett/database/originalrot, rehashede negative
par, fire uavhengige offentlige 368-forløp, analysefri adapter og uendret
2024-regnevern. Dette er utvidet akseptdekning, ikke en påstand om at hver
enkelt regresjonsprøve ble gjennomført som en separat rød/grønn løkke.
De endelige faktiske kontrollutfallene står i kontrolloggene og ledgeren.

Første komplette ops-prøve nådde alle positive filpar og stanset i
offlineprøvens nettforbud: testharnessen erstattet hele `socket.socket`
før `ssl` var importert, slik at standardbibliotekets klassedefinisjon feilet.
Forbudet ble flyttet til `create_connection`, `socket.connect` og
`socket.connect_ex`; socket-klassen beholdes, og både nett og SQLite-connect
er fortsatt sperret i den særskilte offlineprosessen. Produktkode og
kilde-/filvern ble ikke endret. En offentlig offline-CLI-forprøve bestod.
Den gamle målrettede kjøringen og en tidlig fullsuite ble avbrutt; disse
er ikke grønne sluttbevis. Hele ops-prøven og fullsuiten ble startet på nytt
med nye output-/basetempnavn etter rettingen.
