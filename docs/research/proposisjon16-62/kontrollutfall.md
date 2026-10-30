# Faktiske lokale kontrollutfall

Byggerkontroll 29. oktober 2026. Ingen samlet egenreview eller sikkerhetsaudit
er utført. Uavhengig kildekontroll/Standards/Spec/audit og full Linux-CI på
publisert slutt-head er orkestratorens porter.

## Tester og statisk kontroll

Samlet sluttkjøring av alle **35 nye tester bestod på 163,86 sekunder**.
Hele Ruff og formatkontrollen bestod (170 filer), og mypy bestod for alle
85 kildefiler. Full tidligere suite er ikke kjørt lokalt.

En tidligere kjøring ga 33 bestått på 148,91 sekunder, fulgt av to nye
grensetester på 19,75 sekunder. Siste typekontroll krevde offentlige font-/
fill-settere i stedet for privat stilkopi og eget variabelnavn for kolonnen.
Dette ga identisk Excel-presentasjon: alle 14 eksisterende kontrollpar ble
gjenlest med sluttleseren uten forskjell, og alle 35 tester ble deretter
kjørt samlet som angitt over. Ingen guardprofil ble endret.

Ti semantiske angrep rehasher ytre objekt-ID-er, bygger konsistent syntetisk
JSON/snapshot OG synlige Excel-tabeller, passerer `inspect_excel`, og avvises
deretter av de faktiske semantiske leserne: beløp, rolle, år, null, konto,
grenlekkasje, oppdelt felles ramme, gammelt step_id, falsk fullstrukturering
og skjulte globale hull. Ni andre angrep prøver tall som tekst, formel,
internlenke, skjult dekningsark, feil tekstdel, rå stilflagg, ekstra ZIP-medlem,
DOCTYPE og feil snapshotrekkefølge.

Fire autentiske 40034229-forløp bestod uavhengig av faktisk manglende, feilet,
korrupt og motstridende T5-fil. Typed innlesning uten analyseimport bestod.
Begge CLI-innganger, nett-/SQLite-fri gjenlesing, originaluttak og no-clobber
bestod. Ekte gammel T1-fixture leses med gammel leser og beholdes uendret.

Hele Ruff/format/mypy er kontrollert; endelig verktøyutfall og filhash står i
`static-checks.log`/leveransemanifest. Tidligere CI-utvalg, avhengigheter og
90-minuttersgrensen er uendret. Ingen full CI er påstått utført av byggeren.

## Rødt til grønt

Implement- og TDD-filinstruksjonene er lest og fulgt ved #62s allerede
bekreftede offentlige grenser. [TDD-journalen](tdd-journal.json) fører faktisk
observerte resultater, ikke en senere simulering av rødt. Hvert snitt ble
implementert etter sin observerte røde test:

| Snitt | Rødt | Grønt |
| --- | --- | --- |
| 1 | Manglende analysemodul | 105 nye/123 union, uendret T1 og ekte null; 1 bestått |
| 2 | Manglende build_report | Begge innganger/retur og skrevet/gjenlest JSON; 2 bestått |
| 3 | 0 fullmaktspunkter mot forventet 9 | Delt ramme og presise V-/tabellgrener; 3 bestått |
| 4 | Manglende sources-felt | To bevarte 95-representasjoner og ukjent rettelseshistorikk; 4 bestått |
| 5 | Manglende Excel-modul | Ekte null i faktisk JSON/XLSX; 5 bestått |
| 6 | 1533/45 arvet historisk søsterreferanse i aktiv visning | Bare eksplisitt kildebelagt T5-grenomfang; 6 bestått |
| 7 | Manglende Valgt-kolonne i fullmaktsarket | Synlig skille valgt/globalt; 1 bestått, 32 deselectert |

Snitt 5s første implementasjonsforsøk ble også avvist av eksisterende
Excel-guard fordi nytt inventarområde ikke var bundet til autofilterets hele
område. Bare ny T5-kode ble rettet; guardprofilen ble ikke endret.
Før snitt 2 ble lokal tempopprettelse korrigert med eksplisitt `.local`-
basetemp. Dette var miljøfeil og godskrives ikke som produktets røde test.

Første bredere kjøring ga 21 bestått og én feil i den syntetiske old_id-
angrepsbyggeren: den endret dokument-ID uten å oppdatere referanser, slik at
Excel ikke nådde semantisk leser. Prøven er korrigert til konsistent forgiftet
gammelt step_id. Alle ti semantiske Excel-angrep passerer nå containerkontroll
før forventet semantisk avvisning. Dette var kontrollretting, ikke et funn som
ble skjult eller godskrevet som bestått produktaksept.

## Faktiske filer og kildefasit

`ops.proposisjon16_proeve` produserte og gjenleste **14 JSON/XLSX-par** i
`.local/delivery-final`, i tillegg til testenes delte eksportgrunnlag og
CLI-/vernprøver. Alle deler samme basis
`f5a7a071d35e58642c5872cc658eb2abd4b37c266227e2fb2c2f0df21a7713c7`.
Kontrollledgeren inneholder hasher, valg, retur, telleenheter og originaluttak.
Den ble skrevet før de to korte kontekstpekerne; `preservation.json` binder
sluttilstanden: 1181 av 1183 basefiler uendret, bare 17 additive pekerlinjer
i AGENTS/kildefunn. Selve kilde-/produkteksportene er etterkontrollert uendret.
111 forslagfelt er kontrollert mot uavhengig eldre feltinventar og faktisk
originalcelle. Separat råkildekontroll bekrefter ni fullmaktspunkter og åtte
formelle grenlokatorer. Dette erstatter ikke uavhengig kontrollør.

[Excel-QA](excel-qa.md) skiller faktisk render-/bildeinspeksjon fra celleassert.
Ingen ny primærkildehenting, endret gammel original, staging, commit,
GitHub-skriving, PR, merge eller neste ticket inngår i byggerens arbeid.
