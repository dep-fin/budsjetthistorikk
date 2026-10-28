# T4: separate konto-/årsforløp

Kontrakt fastsatt 27. oktober 2026 under #48, del av #37, **før produktkode**.
Startgrunnlag er T3/#46/PR #47, main `e374bdcad3bf18c44ccd7b813ce67b8f97327ee2`.
Eierens mandat omfatter publisering, bygging, full CI og merge av akkurat T4.

## Format og ansvar

Separat opt-in `visningspilot-4`, regel `fleraar1429-2024-2025-1`, basisversjon
`fleraarsgrunnlag-1`. Konvolutten har nøyaktig `format,report`. Rapporten har
`id,basis,selection,return_selection,view,calculations,version`. Basis har
`id,rule,payloads,sources,documents,inventory,statements,observations,contexts,
relations,issues,legacy_json,version`, som T3s feltmønster.

Innlesning eier kildebevaring/strukturering uten analyseimport. Analyse eier
utvalg, årsgruppering, navigasjon, avledede kontroller og streng filgjenlesing.
Ingen migrering eller endring i gamle formater, ID-er, kildebyte, parserbetydning,
schema 5, B5, `round='uavklart'`, legacy HTML-regler eller standardvalg.

Én ordrett validert T1-kapsel i `legacy_json` gjenbrukes som i T3. Ingen ekstra
T3-/T2-kapsel. T3s fem 341-/857-observasjoner og tilhørende objekter gjenbrukes
med identiske ID-er og felt etter eksisterende rekonstruksjonsregler. To nye
201-observasjoner får eget navnerom og `source_system=fleraarspilot`. T1s 18
observasjoner serialiseres bare i kapselen; referanser brukes i nye visninger.
Identiteter følger eksisterende hash-/objektmønster med egne T4-navnerom.

## Kilde og gjenbruk

Vedtak 201/API 40034038, sak 100184, 16.12.2024, sesjon 2024–2025 gjelder
uttrykkelig **budsjett 2025**. /1 nivå 163 173 000 ved
`table[1]/tr[101]/td[4]`; /22 nivå 33 408 000 ved `tr[103]/td[4]`,
kapittelrad `tr[100]`. Rånavn/stikkord og tekst bevares. Hele tabellen har
153 inventarrader; bare disse to nye beløpsfeltene struktureres.

Utdraget har 117 278 byte og SHA-256
`bd2d50e044e7bbfe1284a8b0dffb5a42ed12412e5b462c61c72614c2d000ee50`.
Det rekonstrueres byteeksakt fra bevart c5f3-forelder (7 479 943 byte):

```text
parent[:317] + parent[5662496:5779401] + LF + parent[7479888:]
```

Dette er en avledning, ikke et nytt HTTP-svar. Forelderens gzip og metadata
finnes allerede i autentisk T1-kapsel og refereres med `legacy_source_id`:
`8df02a830c028bc0162f87f2504dabc7f3b4b7000144c33afeae0deafe258af4`
og `b73e5076694be94783f9fc34fc8045f5f547578b3247440ca7ac88e7dac3276c`.
Ingen ekstra base64 av forelder, metadata eller ferdig utdrag ved komplett
input. Forskningsmanifestet gjenbrukes fra T3. Ulike autoritative kilder,
HTTP-forsøk og representasjoner beholder sin egen proveniens.
Manglende T1 gir synlig manglende 210-grunnlag; tilgjengelig nytt grunnlag kan
bevares selvstendig. Ordinær ny vedtaksinnlesning krever aldri T4 eller T1.

## Utvalg, årsgrense og tellerfasit

Eksisterende `PilotSelection` brukes med union av konkrete kontopar/kapitler
innen eksplisitte budsjettår, uten kryssprodukt. Dokumentvalg åpner hele
dokumentinventaret, og retur bevarer valg og år. Grupper etter budsjettår og
konto før kronologi. 210 og 201 har samme dato, men separate årsforløp.
Ingen relasjon gjør 201 til neste runde i 2024.

| Utvalg | Tabellfelt | Vedtaksfelt | Monetære vedtakshendelser |
| --- | ---: | ---: | ---: |
| 2024 /1 | 13 | 7 | 3 |
| 2024 /22 | 10 | 4 | 2 |
| 2024 begge | 23 | 11 | 5 |
| 2025 /1 eller /22 | 1 | 1 | 1 |
| 2025 begge | 2 | 2 | 2 |
| Begge år /1 | 14 | 8 | 4 |
| Begge år /22 | 11 | 5 | 3 |
| Begge år begge / kapittel 1429 | 25 | 13 | 7 |
| Tomt / feil år | 0 | 0 | 0 |
| Dokument 201 eller 341 | 2 | 2 | 2 |
| Dokument 857 | 3 | 3 | 1 |
| Dokument 210 | 6 | 6 | 2 |

Forslag, tilråding, fullmakter, tekst og beregninger øker ikke vedtakstellerne.
T3s lokale 2024-regning bevares med eksakte inngangs-ID-er og status
*avgrenset kontroll*. Beregningsporten får eksplisitt 2024-grunnlag; dens vern
mot andre år svekkes ikke. 2025 viser bare observerte opprinnelige nivåer.
Ingen videreføring, differanse, nivåsum eller saldo på tvers av år.

Globale rekonstruerte avvik navngir ukjent kontinuitet/oppgaveomfang for
1429/1 og /22 mellom 2024 og 2025, også ved tomt valg. Like koder/navn er ingen
kontinuitetsavgjørelse. Egne 2025-hull: originalforslag/tillegg,
Innst.14/postvis vedtakelse, senere RNB/nysaldering/øvrige endringer,
vedtak uten proposisjon, periodeinventar og årsavstemming. 2024-ledd fyller
ingen 2025-hull. 1149s øvrige poster beviser ikke helårsfravær på /1 eller /22.

## Filgrense, kompatibilitet og porter

Akseptgrensen er autentisk original → kildebundet beløp/tekst → dokumentert
relasjon → begge innganger → faktisk skrevet, lukket og gjenlest JSON/XLSX.
M18–M19/M22–M27, M06–M07 og T3-regresjon M16–M17/M21 i
[testmatrisen](research/to-visninger-37/testmatrise.md) gjelder.
Alle tellerutvalg, dokumenter, tekst/fullmakt, kapittel, feil år og tomt
flerårsvalg prøves med faktiske filpar, navigasjon/retur, gjentatt eksport og
offline uten originalrot/nett/database. Fysiske payload-/feltforekomster telles
i JSON og Excelpakken; arvede immutable kopier oppgis separat.

Streng rekonstruksjon avviser også rehashede feil i år, verdi, nivå/delta,
dato, rolle, rånavn, lokator, forelder/oppskrift, referanser, skjulte hull,
falsk kontinuitet, utvalg og beregning. T3s begrensede 4096-inventartak og
øvrige ressurs-/ZIP-/XML-vern videreføres; gamle 512-grenser røres ikke.

Excel viderefører fem hovedfaner, tilgjengelige kontrollark og én selvforsynt
offlinepakke. Separate årsgrupper, budsjettår, nivå/før/endring/etter og hull
skal være tydelige. Faktisk celle-/type-/format-/lenke-/synlighetskontroll og
rendering av skrevne flerårsbøker, dokument201 og tomt/globalt er påkrevd.
Repoets openpyxl-skriver videreføres; Artifact Tool brukes til rendering.

Gjenles ekte tidligere A/B/B6/B8/B9/T1/T2/T3 fra hashkontrollerte kopier og
bevar originalene. Fire separate autentiske 368-prøver gjennom offentlig
ordinær synkronisering/råbevaring/lagring/tolkning/Excel ved manglende,
feilet, korrupt og motstridende T4, også tomt valg uten historisk Excel.

Samlet Standards/Spec og separat audit skal vurdere samme fryste kandidat.
Statikk og full Linux-CI må bli grønn før autorisert merge. Hele testutvalget,
parserversjonslogging og begrunnet 40-minuttersramme beholdes. Varige
kildebevis, akseptledger, filhasher, reproduksjon/rendering og overlevering
lagres i repo/GitHub. Native Excel, gammel selvstendig frozen-v1-JSON og
gammel 554e-fullrespons omtales bare med faktisk bevis.

Utenfor: positiv kontinuitet/K2, full årsdekning/K3, K1, faglig årsbalanse,
T5/T6, generell eldre normalisering/fanerydding, historikkimport og drift.
#10/#32/#37 står åpne. Neste ticket starter ikke automatisk.
