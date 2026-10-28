# P1 / #52: delvis K3-perioderegister

P1 legger til separat opt-in perioderegister-1 for 1429/1 og /22 i 2024.
Begge innganger bruker én typet T4-basis, gamle identiteter og én ordrett
T1-kapsel. Vedtak 346 er en egen merinntektsfullmakt. Forslag, alternative
standpunkter og Prop. 36-status er registerledd med egne roller og kilder.
Ingen ny AmountObservation opprettes av P1.

Et komplett 2024-utvalg beholder elleve vedtaksfelt og fem monetære
posthendelser. 67 indeksforekomster, alle 25 journalbegrunnelser og R1–R7
står globalt, også ved dokumentvalg, feil år og tomt utvalg. Delvis
årsdekning og manglende faglig årsbalansegodkjenning rekonstrueres som
konstanter. Dato, sesjon og like kontokoder etablerer ingen årsrelasjon.

Dokumentinngangen viser hele det uttrykkelige inventaret. Gamle dokumenter
gjenbruker hele T4/T1-inventaret. 346 har komplett vedtaksobjekt og alle
inventerte kontohenvisninger. Nye registerdokumenter har komplette K3-
registeroppføringer og kildebundne råpassasjer med originalpekere, merket
delvis strukturert. Kandidatene har komplette XML-indeksobjekter og tapsfri
metadata_json; selve publikasjonens ikke-hentede fulltekst er merket manglende.

Kildeimport og strukturering ligger i innlesning/ uten analyseimport. Søk,
navigasjon, 2024-regnekontroll, JSON-gjenlesing og Excel ligger i analyse/.
Fem hovedfaner, Kontroll og én Offlinegrunnlag-kapsel følger eksisterende
profil. En falsk synlig verdi eller skjulte rader/kolonner/faner er ikke en
gyldig bok selv om JSON-kapselen er uendret.

Les [før-kode-kontrakten](../../perioderegister.md),
[kildebeviset](source-findings.md), [akseptledgeren](aksept.md),
[byggejournalen](tdd-journal.md) og [reproduksjonen](reproduksjon.md).
candidate-code.json binder de lokale kjørbare filene til base 29ac220 og
kontrakt 407fdbc. verification.json, rendering.json, checks/ og
delivery-manifest.json dokumenterer de faktisk avsluttede kontrollene.

Byggeren leverer lokale endringer. Ingen staging, commit, push, PR eller
GitHub-mutasjon er gjort. Samlet Standards/Spec, separat sikkerhetsaudit,
full Linux-CI og bekreftet merge er orkestratorens etterfølgende porter.
Ingen neste ticket startes. #10/#32/#37 står åpne.

Native Excel, selvstendig gammel frozen-v1-JSON, den gamle 554e-fullresponsen,
full årsdekning, positiv kontokontinuitet, faglig årssaldo og drift er egne
bevisgrenser. Tidligere immutable kapslers fysiske duplisering beholdes og
måles separat fra nye payloads.

Filkontrollen er avsluttet med 41 faktiske P1-par, 23 rehashede negative
par, åtte presentasjons-/DOCTYPE-prøver og elleve ytterligere container-/
ressursavvisninger. 14 ekte tidligere filpar og én B6-bok er kontrollert.
Full lokal suite og kandidatbinding dokumenteres i checks/ og
akseptledgeren; de er separate fra Linux-CI og de uavhengige portene.

Full lokal suite er grønn med 1 179 bestått og to eksisterende Windows-skips,
på 2 600,31 sekunder. Alle 24 P1-tester og Ruff/format/mypy består. Åtte
kjørbare filer var byteidentiske før/etter kjøringen. [Akseptledgeren](aksept.md)
og checks/ skiller dette fra fortsatt gjenstående Linux-CI, review og audit.

Tellerfasiten 67/25/7 gjelder det bevarte komplette K3-grunnlaget ved alle
utvalg. En helt manglende kildepakke gir synlige mangler og konstruerer
ikke kandidatposter. De fire uavhengige 368-forløpene er derfor spesifisert
enkeltvis i verification.json. Ingen av dem krever historisk Excel.
