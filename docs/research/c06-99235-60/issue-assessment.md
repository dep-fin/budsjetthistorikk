# Vurdering av ticketoppdeling og issue-rydding

Observasjon: 29. oktober 2026. Denne lesebaserte vurderingen inngår i #60;
den publiserer eller starter ingen annen ticket. Den følger delegate-tickets,
ticket-orchestrator og prosjektets arbeidsflyt/issue-tracker.

## Kontrollert startfront

GitHub-listene for åpne issues og PR-er ble lest med `per_page=100&page=1`
og side 2. Før opprettelsen av #60 var fem issues og én PR åpne; side 2
var tom. Krav, kommentarer og relasjoner for aktuelle foreldre og leveranser
ble lest. Ingen åpne issues hadde assignees eller etiketter. Native
sub-issue-/avhengighetslister var tomme; tekstlige krav og eierporter gjelder
likevel. Native skriving er ikke eksponert i den tilgjengelige koblingen.

| Arbeid | Gjeldende status og konsekvens |
| --- | --- |
| [P2/#56](https://github.com/depmartin/budsjetthistorikk/issues/56#issuecomment-6497638291) | Levert i PR #57, merge `59485e6bb6e45dacf348451b380cf6ba3b5d8321`. CI 40868223336 er bekreftet completed/success. Ikke bestill på nytt. |
| [U1/#58](https://github.com/depmartin/budsjetthistorikk/issues/58#issuecomment-6501722374) | Levert i PR #59, merge `49cc6e44851cf74e0aaea4eb333419e5598bfd95`. CI 40894686973 er bekreftet completed/success. Dette er #60s base. |
| [#37](https://github.com/depmartin/budsjetthistorikk/issues/37) | Åpen produktforelder. T1–T4/K3/P1/R2/P2/U1 er levert; bredere dekning og senere produktutvidelser består. |
| [#32](https://github.com/depmartin/budsjetthistorikk/issues/32) | Åpen omtale-/temaforelder. O1/O2a/O2b og senere avgrensede piloter skal ikke bestilles på nytt. |
| [#13](https://github.com/depmartin/budsjetthistorikk/issues/13) | Åpen historikkforelder. 2024-pilot/kontrollmatrise er levert; øvrige år og faglige porter består. |
| [#10](https://github.com/depmartin/budsjetthistorikk/issues/10) | Åpen for utsatt faktisk driftsaksept: vert/konto/lager/bakgrunnstilgang, kl. 06-kjøring og backup/restore. Mer generell kodeleveranse er ikke denne aksepten. |
| [#1](https://github.com/depmartin/budsjetthistorikk/issues/1) | Åpen overordnet spesifikasjon, ingen startklar byggeticket. |
| [PR #14](https://github.com/depmartin/budsjetthistorikk/pull/14) | Eneste åpne PR, utkast på feature/historisk-excel-2013-2025, head da720e9. Bevar originaler/arbeid; ingen tillatelse til merge. |

Bare C06/99235 er valgt og autorisert nå. Ingen eksisterende åpen issue
er bekreftet som en ny ledig byggeticket for parallell gjennomføring.
Det er derfor ikke grunnlag for fem parallelle sessions.

## Oppdeling som anbefales ved senere mandat

C06 beholdes som **én** komplett kunnskapsticket. Behandlingskjeden,
datokonflikten og post-/årsvurderingen må kunne kontrolleres samlet.
Separate hente-, parser- og rapporttickets ville ikke gi selvstendig aksept.
99235 ligger utenfor K3s 67 historiske kandidatforekomster; oppfølging via
R2/C06 reduserer ikke historiske 60 åpne forekomster eller R1–R7.

- #37 beholdes som forelder. T5/T6 er allerede separate komplette utkast;
  T1-forutsetningen for T5 er levert, mens T6 fortsatt trenger T5. Hver
  trenger eget mandat og størrelseskontroll mot dagens kode. En uttrykkelig
  delvis leveranse trenger ikke positiv K1/K2/M21, men må bevare sine hull.
- K1 må vurderes mot K3s allerede leverte autentiske alternativer og sju
  forkastede RNB-pakker før ny undersøkelse bestilles. Positiv alternativaksept
  krever fortsatt behandlings-/utfallsbinding og eventuell produktaksept.
- K2 beholdes som egen positiv kunnskapsport. Separate årsforløp kan leveres
  med ukjent kontinuitet; dokumentert sammenkobling krever andre bevis.
- M21 bør følges gjennom navngitte saker eller konkrete bevisporter,
  ikke én stor ticket for å «lukke alle R1–R7». C06 gir ingen positiv årsaksept.
- #32 bør få ett kilde-/årsutvalg og én observerbar søke-/omtaleoppgave per
  senere leveranse. #13 bør deles etter ett år eller én faglig kontrollhypotese.
  Ikke opprett nye tickets som gjentar leverte piloter.
- #10 trenger miljøbeslutning og faktisk driftsaksept. U1-produktadopsjon
  er en mulig egen senere leveranse og ingen blokkering for C06.

Dette er vurderinger, ikke publiserte oppgaver eller byggemandat.

## Rydding: kort gjeldende inngang, bevart historikk

#37s body var omtrent 55 600 tegn og åpnet med foreldet P2-status samt
anbefaling om allerede levert oppfølging. #32 beholdt O1-startprompt selv om
kommentarene dokumenterte senere leveranser. Dette kan utløse dobbeltarbeid.

Ved et eget oppryddingsmandat anbefales følgende:

1. Bevar før-versjonen av hver body med issue-ID, observasjonstid og hash
   i en versjonert dokumentasjonsleveranse.
2. Kort ned foreldrebody til formål, bindende krav/aksept, levertabell med
   ticket/PR/merge, gjenstående porter og lenke til gjeldende overlevering.
3. Erstatt gjentatte historiske overleveringer og lange startprompter i body
   med lenker til bevarte kommentarer og rapportrevisjoner. Behold kommentarene.
4. Ha høyst én aktuell startprompt på maksimalt tre setninger som peker til
   ticketkontrakten, AGENTS og arbeidsflyten. Merk hva som erstattet eldre forslag.
5. Skill uttrykkelig mellom foreslått, autorisert, pågår og levert. En
   anbefaling gir ingen tillatelse til neste ticket.

Det er fornuftig å kutte gjentatte promter fra den **gjeldende inngangen**,
men først etter at den unike krav-/beslutningsinformasjonen er bevart og
erstattet med presise pekere. Ingen eksisterende issuehistorikk er omskrevet
eller slettet i #60. Parent #37 får bare additive statuspekere for leveransen.

## Bevisgrense

Merge, CI-status og main ble kontrollert live. Detaljerte testantall og
faglige akseptbevis er lest i leverte overleveringer; de er ikke kjørt på nytt
som del av denne planvurderingen. Ingen positiv års-, kontinuitets- eller
driftsaksept er gitt. #10/#32/#37 står åpne. Ingen neste ticket er startet.
