# T4/#48: separate konto-/årsforløp

Lokal byggekandidat på `codex/t4-fleraar`, fra main
`e374bdcad3bf18c44ccd7b813ce67b8f97327ee2`. [Kontrakten](../../fleraarspilot.md)
ble fastsatt før kode i `fc2b62966d65147d5d3d2ad5c0670d4d4912399b`.
Byggeren leverer lokale filer; orkestratoren fryser kandidaten, gjennomfører
samlet Standards/Spec, separat audit, publisering og full Linux-CI før merge.
Ingen staging, commit, push, egen review/audit eller GitHub-skriving er gjort
av byggeren. #10/#32/#37 står åpne. Neste ticket starter ikke automatisk.

Lokal fullsuite er grønn: **1155 bestått, to eksisterende Windows-
rettighetsskips, 2903,14 s**. Alle **37 T4-prøver** består; JUnit summerer
1151,989 s for dem inkludert fixturetid. Ruff check/format (124 filer) og
mypy (71 kildefiler) består. Ops-filprøven og fullsuiten kjørte delvis
samtidig. [Tidsmåling og CI-grense](ci-measurement.md) forklarer hvorfor dette
ikke er et Linux-tidsbevis eller en garanti for 40-minuttersjobben.

Den avsluttede ops-prøven tok **1239,219 s** og kontrollerte **30 utvalgspar**,
ett ekstra offentlig offline-CLI-par og fire feil-/tomt-par. **19 rehashede
negative JSON-/Excel-par** og **åtte falske/skjulte presentasjonsbøker** ble
avvist. **66 ekte eldre filpar og én separat B6-bok** ble gjenlest fra
hashkontrollerte kopier; alle **133 originaler** er uendret. Alle **326
manifestførte filer**, de sju kodefilene og **30 renderingsbilder** er
rehashkontrollert. I tillegg er et selvstendig 2025-par uten T1 og en
[syv-filers avhengighetsprøve](dependency-proof.json) kontrollert.

[Kildebeviset](source-findings.md) viser at 201/40034038 gjelder budsjett
2025, med to observerte nivåer på 1429/1 og /22. 210s nysaldering gjelder
2024 selv om vedtakene har samme dato. Ny opt-in `visningspilot-4` bevarer
separate konto-/årsgrupper og globalt ukjent kontinuitet/oppgaveomfang.
Ingen sum, videreføring, differanse eller saldo mellom årene beregnes.

| Års-/kontoutvalg | Tabellfelt | Vedtaksfelt | Monetære vedtakshendelser |
| --- | ---: | ---: | ---: |
| 2024 /1 | 13 | 7 | 3 |
| 2024 /22 | 10 | 4 | 2 |
| 2024 begge | 23 | 11 | 5 |
| 2025 /1 eller /22 | 1 | 1 | 1 |
| 2025 begge | 2 | 2 | 2 |
| Begge år /1 | 14 | 8 | 4 |
| Begge år /22 | 11 | 5 | 3 |
| Begge år begge / kapittel 1429 | 25 | 13 | 7 |
| Tomt / feil år / tekst-fullmakt | 0 | 0 | 0 |
| Dokument 201 eller 341 | 2 | 2 | 2 |
| Dokument 857 | 3 | 3 | 1 |
| Dokument 210 | 6 | 6 | 2 |

T3s fem nye felt og tilhørende objekter beholder ID-er og felt. En ordrett,
validert T1-kapsel gir de 18 tidligere observasjonene og deres kildebevis.
Ingen ekstra T2-/T3-kapsel eller nye kopier av T1-beløp legges i T4-basis.
Ved komplett input er T4s c5f3-forelder og metadata bare to legacy-referanser.
Den nye serialiseringen har sju beløpsobjekter/sju unike og fem nye råpayloads,
én forekomst av hver. Inne i den uendrede T1-kapselen består 36 arvede
beløpsobjekter/18 unike og 23 råpayloadforekomster/21 unike hasher. Dette
arvede forholdet oppgis separat; eldre formater er ikke normalisert på nytt.
Excel har én selvforsynt Offlinegrunnlag-kapsel med samme JSON-byte.

2024-regningen gir fortsatt 166 039 000 og 29 185 000 kroner med status
**avgrenset kontroll**, eksakte inngangs-ID-er og lokale før/etter-kontroller.
Den uendrede T3-porten får bare uttrykkelig 2024-grunnlag. Et rent 2025- eller
201-valg har verken disse beregningene eller arvede 2024-stadiesammenligninger.
2025 viser bare de observerte opprinnelige nivåene. Begge årenes egne hull
består globalt, også ved tomt utvalg.

Fem hovedfaner følger T3-profilen: Forløp, Dokumenter, Omtale,
Sammenligninger, Dekning og avvik. Kontroll og Offlinegrunnlag er tilgjengelige.
Forløp grupperer etter budsjettår/konto før kronologi og viser nivå/før/endring/
etter hver for seg. Lenker fra inventar til konto bruker både år og konto.
Hele 201-tabellens 153 rader, rånavn/stikkord og fulltekst er tilgjengelige;
bare to felt er strukturert. Lange tekster/HTML/JSON deles tapsfritt og kan
åpnes i cellen eller gjenfinnes med `--originaler`.

De faktiske kontrollresultatene, filhashene og bevisgrensene samles i
[akseptledgeren](aksept.md), `verification.json`, `delivery-manifest.json`,
`candidate-code.json`, [renderingen](rendering.json) og [overleveringen](OVERLEVERING.md).
[Byggejournalen](tdd-journal.md) beskriver røde/grønne vertikale prøver og
avgrenser hva som ble utført som senere regresjonskontroll.

Native Excel, en separat gammel frozen-v1-JSON, den gamle 554e-fullresponsen,
positiv kontokontinuitet, helårsdekning, faglig årsbalanse og drift er egne
bevisgrenser. Lokal Windows-kontroll er ingen påstand om grønn Linux-CI.
