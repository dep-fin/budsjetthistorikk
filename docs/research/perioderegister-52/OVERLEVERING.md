# Lokal byggeoverlevering P1 / #52

Arbeidsflate: work/p1-perioderegister, branch codex/p1-perioderegister.
HEAD er før-kode-kontrakten 407fdbc, over K3-merge 29ac220. Byggeren har
verken staget, committet, pushet, skrevet til GitHub eller opprettet PR.
candidate-code.json binder de åtte kjørbare filene; delivery-manifest.json
binder kilde-/kontroll-/dokumentasjonsleveransen og de lokale kontrollfilene.

Levert: separat perioderegister-1, begge innganger/navigasjon/retur,
346/fullmakt uten nytt beløp, fem/elleve uendrede vedtakshendelser/-felt,
globale 67/25/7 og delvis årsdekning. Nye registerdokumenter har kildebundne
råpassasjer. T4 og den ene T1-kapselen er uendret. Nye P1-payloads bruker
også eldre byte fra den nestede O2b-delen gjennom seks legacy-referanser.

Det faktiske kontrollarkivet ligger i .local/p1-complete/ og
.local/p1-navigation-complete/. Syntetiske ZIP/XML-/ressursprøver ligger i
.local/p1-guards-complete/. Dette er lokale faktiske filer, ikke bare
filnavn eller interne modellobjekter. De store filene er ikke lagt inn som
et nytt råarkiv i Git; hasher, resultater og reproduksjon er bevart her.
Tidligere forsøk i andre .local/-mapper er ufullstendige historiske forsøk
og inngår ikke som beståtte porter.

Utførte filporter:

- 36 utvalgs-/navigasjons-/returpar, én ekstra offentlig offline-CLI og
  fire separate tomme P1-par: 41 faktiske JSON-/Excel-par.
- 23 rehashede negative par; den eksakte forgiftede JSON-kapselen passerer
  Excel-containerporten før kilde-/kontraktavvisning.
- Åtte presentasjons-/DOCTYPE-prøver og elleve ytterligere merkede
  container-/JSON-/ressursangrep er avvist.
- Fire egne 368-databaser, hver med 222 felt / 74 hendelser, schema 5,
  uendret B5-seedregister, råkilde og gammel round='uavklart'.
- 14 ekte tidligere filpar og én ekte B6-bok er gjenlest fra hashkontrollerte
  kopier. Alle 29 originalfiler er uendret. Dette dekker O2a/O2b, B8/B9 med
  B6-kjerne og representative T1/T2/T3/T4-filer.
- 130 K3-filer stemmer med Git-blobbene i 29ac220. 390 råtabellrader,
  25 vedtaksbevis og alle 67 indeksmetadataobjekter er avstemt mot originalene.
- 34 faktiske renderinger fra de lagrede bøkene er bevart. Native Excel er
  ikke brukt. resources.json viser de målte grensene; gamle porter er uendret.

Full lokal suite/statikk er grønn: 1 179 bestått, to eksisterende Windows-
rettighetsskips, 2 600,31 sekunder; 24 P1-prøver. Ruff/format (131 filer)
og mypy (76 kildefiler) består. Alle åtte kjørbare filhasher var uendret
før/etter fullsuiten. Fullt bevis finnes i checks/ og akseptledgeren.
Standards/Spec, separat sikkerhetsaudit, full Linux-CI og merge gjenstår
hos orkestratoren. Byggerens kontroller erstatter ingen av disse portene.
En lokal kjøretid er ikke en garanti for gjeldende 60-minutters Linux-jobb;
hele testutvalget og parserversjonslogging er beholdt.

Bevisgrense: native Excel, separat gammel frozen-v1-JSON, 554e-fullrespons,
positiv helårsdekning, kontinuitet, faglig årsbalanse og drift er ikke levert.
#10/#32/#37 skal fortsatt stå åpne. Neste ticket starter ikke automatisk.

## Fortsett samme P1

```text
Fortsett P1/#52 i work/p1-perioderegister på codex/p1-perioderegister.
Les docs/perioderegister.md og docs/research/perioderegister-52/README.md,
aksept.md, candidate-code.json og delivery-manifest.json. Kontroller
arbeidsflate/head og alle bundne filhasher før kandidaten fryses.

Gjennomfør samlet Standards/Spec og separat sikkerhetsaudit på samme faste
kandidat etter ticket-orchestrator. Avklar eventuelle funn med målrettede
kontroller, kontroller fersk main/overlapp, og håndter deretter autorisert
PR, full Linux-CI og bekreftet merge av akkurat P1. Bevar hele testutvalget,
gamle format-/ID-/schema5-/B5-grenser og tidligere arbeidsflater.
Rapporter faktisk port-/PR-/CI-/mergestatus og avslutt etter P1.
La #10/#32/#37 stå åpne; start ingen neste ticket.
```
