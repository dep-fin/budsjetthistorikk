# K3 – overlevering av kunnskapskandidat

Undersøkelsen er gjort 28.10.2026 på `codex/k3-arsinventar` i isolert checkout
`work/k3-arsinventar`, fra main `37c6ad4572c030a6b3309201d836bb0c0c51f9c6`.
Siste T4-overlevering er gjeldende; eldre statusavsnitt i planer/issues er
historikk. Ingen produktkode, gammel råkilde eller gammel identitet er endret.

## Leveranse

[Hovedrapport](README.md), [M21 med restusikkerhet](m21.md),
[dekningsjournal](coverage-journal.json), [vedtaksregister](decision-register.json),
[sakskandidater](case-candidates.json), [saksrelasjoner](case-relations.json),
[nye/tidligere råoriginaler](source-manifest.json), [gjenbruk](reused-sources.json),
[tabellokatorer](table-locators.json), [vedtaksbevis](decision-evidence.json),
[voteringsbevis](voting-evidence.json), [versjonskontroll](source-comparison.json),
[avgrenset perioderegister](known-period-ledger.json),
[snittforslag/startprompt](neste-snitt.md) og [reproduksjon](reproduksjon.md).

Nytt sikkert berørende vedtak er 346/40032933, merinntektsfullmakt for 1429/1
i 2024. Originale H-/FrP-alternativer er belagt i Innst. 14. Hele tidligere
Innst. 447 er nå tapsfritt bevart med tidligere transportmetadata; dens sju
primærpakker holdes adskilt fra tilråding og 857. Prop. 36s års-/kildeliste
gir en annen kontrollinngang enn tekstsøk og den lokale trevedtaksregningen.
Tillegg 1/2 og Prop. 106 er undersøkt med konkrete omfangsgrunner.

2 183 vedtaksobjekter er registrert uten type-/proposisjonsfilter; 25 funn har
egne grunner. 2 158 uten søkeordtreff er fortsatt semantisk åpne.
1 364 saksindeksposter gir 67 kandidatposter/66 unike saker, hvorav 60/59 står
åpne for fulltekstkontroll. R1–R7 angir ytterligere referanse-/voterings-/
versjons-/strukturgrenser. Positiv M21/helårsdekning er ikke hevdet lukket.

## Porter og bevisgrense

Byggerens faktiske kilde-/dokumentkontroller står i `verification.json`;
leveransefilenes hasher står i `delivery-manifest.json`. De er forsknings-
og dokumentkontroller. Ingen ny produkt-JSON/Excel, native Excel-test,
produksjonsdrift, faglig årssaldo eller positiv kontokontinuitet er levert.
Avbrutte HTTP 200-svar er uttrykkelig ufullstendige; HTTP 500 er feilkropp.

Byggerens kontroller omfatter 46 kilde-/transportforsøk (42 komplette vellykkede,
fire ufullstendige/feilsvar), 24 uendrede gjenbruksfiler, 390 gjenleste tabellrader,
fem eksakte passasjer, 64 saksreferanser/-relasjoner og samtlige 2 183 gamle/nye
kanoniserte vedtaksobjekter. Ti navngitte voteringer/fem vedtakskoblinger,
åtte API-forslag og alle sju RNB-pakkenes nummer/avsender/beløpsblokker/utfall
er kontrollert mot de bevarte kildene. Ingen av disse kontrollene har feil.
Uavhengig kildeutforskning er integrert og gjenkontrollert her; dette erstatter
ikke orkestratorens senere faktakontroll av en fastfryst samlet kandidat.

[Den uavhengige faktakontrollen](faktakontroll.md) gjelder fast kandidat
`5b6e86c13411ac703976447c5c21fc005f83b6a2` og fant ett nødvendig
manifestavvik, F1. Opprinnelig rapport/måleresultater er bevart uendret.
F1 er rettet med en uttrykkelig Git/LF-regel bare for `docs/kildefunn.md`,
kontrollert mot den faktiske originalbloben; øvrige filer er byteeksakte.
Dette er ikke samlet review eller sluttport av en senere commit.

Orkestratoren fyller inn ny fast revisjon, faktisk etterfølgende leveringsport,
PR/CI/merge og siste status før ekstern avslutning. Rettingen er ikke staget,
committet eller skrevet til GitHub av retteragenten. #10/#32/#37 skal stå åpne.

Anbefalt neste arbeid er P1-snittet i [neste-snitt.md](neste-snitt.md), etter
nytt mandat. Alternativt kan en egen kildeøkt lukke ett konkret R-hull først.
Ingen neste ticket starter automatisk.
