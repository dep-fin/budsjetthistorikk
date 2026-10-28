# Forslag til neste lille komplette snitt

**P1: vis det avgrensede K3-perioderegisteret for 1429/1 og /22 i 2024 gjennom
begge innganger og faktisk gjenlest JSON/Excel.** Dette er et forslag, ingen
publisert eller startet byggeticket.

Snittet bygger på levertT 4 og dette K3-grunnlaget. Bruk en separat opt-in
format-/identitetskontrakt fastsatt før kode. Gjenbruk T1/T3/T4s uendrede
kilder, observasjoner, ID-er og nødvendige kompatibilitetskapsel med referanser.
Ikke kopier de store råoriginalene inn flere ganger bare for å vise dem fra
flere innganger. Selvstendig ny vedtaksinnlesning består.

Det nye komplette brukersnittet er et **perioderegister med synlige hull**,
ikke generell fullstrukturering av Prop. 1/104/447 eller en ny årsimport:

1. Les et kildebundet frosset register med dokument-/vedtaks-/saks-ID,
   budsjettår eller ukjent år, rolle, runde, kjent postomfang eller ukjent
   postkobling, originalreferanse, lokator og egen dekningsstatus.
2. Vis de kjente monetære leddene og 346/40032933 som særskilt fullmakt.
   Det skal være fem kjente monetære hendelser/elleve vedtaksfelt, ingen
   ny beløpshendelse for 346, partiforslag eller Prop. 36-status.
3. Vis 67 indekskandidatposter med undersøkt/åpen status, 25 begrunnede
   vedtakskandidater og R1–R7 som globalt dekningsgrunnlag. Dokumentet kan
   åpnes fra konto/år; retur bevarer utvalget. Dokumentvalg må beholde hele
   det uttrykkelige dokumentinventaret og markere delvis strukturering.
4. Skriv, lukk og gjenles JSON og Excel, også offline uten originalrot/nett/
   database. Samme kilde-/dokument-/hendelsesreferanser og hull skal bestå
   i begge innganger. Prøv post 1, post 22, begge, fullmakt 346, ukjent kandidat,
   feil år og tomt utvalg.
5. Prøv rehashet feil på kildehash/år/post/rolle/346-beløp/positiv årsdekning
   og skjulte globale hull. Bevar gamle lesere, schema 5, B5, standardvalg og
   uavhengig ordinær registrering/eksport av nye vedtak.

Enheten trenger ikke full RNB-/originalbudsjettadapter, ny nettinnhenter,
positiv kontinuitet, T5/T6 eller faglig årsbalanse. Hvis et byggemandat heller
skal lukke positiv M21, må først R1–R7 avklares i en egen avgrenset kunnskapsøkt.

## Kopierbar startprompt – krever nytt eiermandat

```text
Publiser og gjennomfør ett lite P1-byggesnitt under #37 fra fersk main etter
K3/#50: vis det uttrykkelig delvise K3-perioderegisteret for 1429/1 og /22,
budsjettåret 2024, gjennom begge innganger og faktisk gjenlest JSON/Excel.

Les AGENTS.md, hele #37/#50 med kommentarer, siste K3-overlevering,
docs/research/k3-arsinventar-50/README.md, m21.md, coverage-journal.json,
case-candidates.json, source-manifest.json, reused-sources.json og
neste-snitt.md samt T4-kontrakten/kildekontrollen. Bevar tidligere arbeid
og bruk isolert checkout/egen branch fra fersk origin/main.

Fastsett en egen opt-in felt-/identitetskontrakt før kode. Gjenbruk gamle
objekter/ID-er/kilder med referanser. Vis 346/40032933 som egen 2024-fullmakt
på /1, uten ny monetær hendelse. De fem kjente monetære hendelsene/elleve
vedtaksfelt består. Forslag/alternativer/Prop.36-status er egne roller.
Behold de 67 indekskandidatpostene med status og globale R1–R7-hull også
ved tomt valg. Ingen positiv helårsdekning eller faglig årssaldo.

Lever original -> kildebundet register/fullmakt -> dokumentert relasjon ->
begge innganger -> faktisk skrevet, lukket og gjenlest JSON/Excel/offline,
med negative prøver og kompatibilitetsbevis. Nye offisielle vedtak skal
registreres uavhengig av registeret/berikelse/historikk. Følg uavhengige
Standards/Spec-porter, separat audit, relevant full CI til grønt og faktisk
autorisert merge. Denne bestillingen autoriserer akkurat P1, ikke neste ticket.
Ingen T5/T6, kontinuitet, faglig godkjenning, generell årsimport eller drift.
La #10/#32/#37 stå åpne. Lagre sluttstatus/kildebevis/overlevering og ny
startprompt i GitHub, og avslutt økten etter P1.
```
