# Arkivert utforskergrunnlag for #46

Dette er utforskerens sluttgrunnlag fra 27. oktober 2026, bevart varig før
produktaksepten. Det beskriver kildekontroll og foreslått fasit; senere
produktbevis og deres kandidatbinding finnes i README/verification.json.
Den opprinnelige teksten følger uendret nedenfor.

---

# T3: utforskerens sluttgrunnlag

Undersøkt 27.10.2026 i `work/t3-forlop`, branch `codex/t3-2024-forlop`.
HEAD `c1cb156d50fb986794e2af8b20a131209e4707a7`, tre
`ae70d77b07662bb0e01276237c8d802d98e00117`. Arbeidsflaten var ren.
Kun denne filen og `work/t3-ticket-draft.md` opprettes, begge ignorert.
Ingen produktkode, commit, push, issues eller andre agenters filer er endret.

## Mandat og lest kontekst

Mandatet i `work/ticket-context/parent37.json` gir publisering av T3 under #37,
bygging, CI til grønt og merge. Det utvider det eldre planutkastets status;
T3–T6 var tidligere bare forslag. #37/#32 er foreldrekrav, #10 er åpen drift.

AGENTS, arbeidsflyt, issue tracker, domain, ansvarsdeling, GLOSSARY, målbildet,
pilotplanen, T3-/T4-utkastene, konto-/årsrapporten og testmatrisen er lest.
T1-kontrakt/ADR 0011/kildekontroll, T2-kontrakt/kildekontroll/overlevering,
fanevurderingen og CI-newlines-notatet er lest. GitHub-pluginen leste #1/#32/
#41/#44 og deres kommentarer. #1/#41 har ingen kommentarer. #32s O2b-kommentar
bevarer seks vedtaksfelt/to hendelser; #44s avslutning bekrefter merge #45 og
grønn Linux-CI. Ingen CLI-fallback eller ny HTTP-kildehenting var nødvendig.

## Verifisert fra faktiske kildebyte

Bundlet Python 3.12 og lxml leste filene uten å skrive. Hash- og bytekontroller
er utført nå; tallene nedenfor er ikke bare sitater fra gammel rapport.

| Objekt | Identitet/dato/år og kontrollert innhold |
| --- | --- |
| 341 / 40032928 | Sak 95776, 19.12.2023. Tittel og vedtakstekst sier statsbudsjett **2024**. `table[1]/tr[101]` er 1429; `tr[102]/td[4]` er /1-nivå 161 243 000; `tr[104]/td[4]` er /22-nivå 32 185 000. |
| 857 / 40033719 | Sak 98919, 21.06.2024. Tittel/tekst sier RNB 2024. 1429 er `tr[822]`; /1 `tr[823]/td[5]` har rå 1 000 000 og «reduseres med», altså delta −1 000 000. `tr[824]/td[3]` har før 161 243 000 og etter 160 243 000. |
| 857s fraværsgrense | Hele `tr[822–830]` lest; poster /1,/60,/70,/71. Neste kapittel 1432 starter i `tr[831]`. Ingen /22-beløpsrad i akkurat denne blokken; ingen nullhendelse eller helårs-/hele-RNB-påstand. |
| 210 / 40034048 | Sak 100927, 16.12.2024. Tekst/tittel sier statsbudsjett 2024. /1 `tr[3–4]`: +5 796 000, før 160 243 000, etter 166 039 000. /22 `tr[5–6]`: −3 000 000, før 32 185 000, etter 29 185 000. Gammel T1/O2b eier identiteter og seks felt. |

### 341s eksakte avledning

`docs/research/to-visninger-37/originals/aar/40032928.xml`:
117 054 byte, SHA-256
`73bbcdc1d83a539ab4f3c2fad7b2b2972e003e742a5391a003d19c38149b6e71`.
Forelderens gzip: 342 281 byte,
`d083055643de38008fa373e54ea556cb06f5348f5d7d4978a323bba25e3f303f`.
Utpakket HTTP-respons: 6 816 165 byte,
`66aa3ac5e93598fbbf2c02577c025395ea43a6bb7148e83a79f639bac9b09a57`.
Faktisk byteidentisk rekonstruksjon fra manifestet bestod:

```text
parent[0:317] + parent[6092492:6209173] + LF + parent[6816110:]
```

Objektintervallets SHA er
`5c753687510813c4f4241705670764b4e9903e87343d61ee71e55c872ae53857`.
Dette er original konvolutt + uendrede objektbyte + uttrykkelig innsatt LF,
ikke et eget HTTP-svar. Bevar manifest/transportmetadata og oppskrift.

### 857: to foreldre må ikke forveksles

Den eksisterende B3-fixturen er 1 265 833 byte, SHA
`4113b987c8f939256d30ef6a4401cda358d9da90b5af19cbbbc37d0ec9d312b0`.
Sidevognens oppgitte opprinnelige fullresponshash er
`554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf`,
hentet 20.10.2026 11:35:51 UTC. Denne gamle fullresponsen finnes ikke i
T3-repoets bevarte originaler. Den oppgitte eldre banen under hovedrepoets
`work/issue2/kontroll/raw` finnes heller ikke. Dette er en konkret bevisgrense,
ikke grunnlag for å omskrive sidevognen eller påstå at gammel forelder er lest.

Det finnes likevel et fullt reproduserbart T3-grunnlag: samme komplette objekt
er kontrollert byteidentisk mellom gammel fixture og den bevarte nyere
66aa-forelderen. Intervallet er `[2552391:3817852]`, 1 265 461 byte,
objekt-SHA `a22a2fe3ae4e26f57d1570b27a0f962ddfda9937944b1204262cf8759ef4f392`.
Ny avledet konvolutt kan rekonstrueres uten ny råkopi:

```text
parent[0:317] + parent[2552391:3817852] + parent[6816110:]
```

Denne er 1 265 833 byte med SHA
`252544da8756b038d54f6e935323fb33227b7ef16ee4c540a1badb7c5245517f`.
Det er en **annen konvolutt/kildeobservasjon**, ikke ny faglig vedtakshendelse.
Anbefaling: T3s nye adapter kan bruke denne uttrykkelig nye avledningen som
valgt beløpsrepresentasjon, og kontrollere objektlikheten mot den uendrede
B3-fixturen. Bevar original fixture/sidevogn som selvstendig kontrollgrunnlag;
ikke kall 66aa for 554e og ikke kopier B3-ID-er til nye kildehashbindinger.
Nye T3-observasjoner har eget navnerom; gamle B3-resultater/ID-er er urørt.
Alternativt kan fixturen være valgt beløpsrepresentasjon med synlig manglende
opprinnelig forelder. Valget må dokumenteres før kode; anbefalt første variant
gir fullt repo-reproduserbar ny avledning uten å endre gamle påstander.

### 210 og gammel kapsel

`tests/fixtures/b6/40034048.xml`: 6 058 byte,
`2a540261f110b761a0213516c8ad72844d0285744ca0f1cdd4cb1afce06f0850`.
Den bevarte **gamle** 9cfe-forelderen ble dekomprimert og hashkontrollert:
7 479 943 byte,
`9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680`.
`prefix317 + parent[1249812:1255498] + suffix55` rekonstruerte fixturen eksakt.
Den nyere c5f3-forelderen ble også hash-/størrelseskontrollert, men er ingen
erstatning for 210s gamle proveniens.

`tests/fixtures/t2/authentic-t1.json.gz` ble lest og kontrollert:
gzip-SHA `629c3561cca6f0ab2a5644958c7ae6590dd70775d688f40e134bda449e8982a6`,
utpakket 7 732 250 byte/SHA
`99e871e0ab780cbb548e15699f3093621d0f25229e3fa06c29cfdb5552803f53`.
Rapport-ID `4d27c1e83524102cb29ff8b429fb262bb9861d4b024718e1edca90d457c6f17e`,
basis-ID `e1a32cd17ebe3d96bff66a4c302e72fc95af28d6d3fa6d8f09d07ff84b06ba5c`.
Basis har 18 observasjoner, fem dokumenter, 57 inventarrader.
Dette er et ekte tidligere arkiv, ikke en regenerert gammel fil. Dagens strenge
offentlige `analyse.visningspilot.report_from_json` leste arkivet og bestod
full rekonstruksjon på 1,031 s med samme rapport-/basis-ID og 18 observasjoner.
Dette er en gammel-leser-kontroll, ingen ny T3-funksjonsaksept.

## Minste komplette implementeringssnitt

Anbefal nytt eksplisitt `visningspilot-3`, egen T3-regel/leser og kort kontrakt
før kode. Gjenbruk T2s *mønster* for payloadregister, kilde-ID-er,
derivasjonsmetadata, én gammel T1-kapsel og ID-referanser. T2s faglige
315/78-data, basis og obligatoriske katalog skal ikke trekkes inn i T3.

Det komplette T3-forløpet bygger på én uttrykkelig validert T1-kapsel som kilde
for de gamle 210-/Prop16-/Innst81-observasjonene. Den kan leses fra en faktisk
tidligere leveranse; repoets autentiske arkiv gjør akseptprøven reproduserbar.
Den er ikke en avhengighet for ordinær ny vedtaksinnlesning. Ikke bygg en T2-kapsel
rundt en T1-kapsel og legg så begge i T3. Ingen ny strukturering/lagring av 210.

Nye T3-beløpsobjekter: fem, fra to 341-nivåer og én 857-trio. Gamle 18 T1-felt
refereres uendret og skal ikke serialiseres en ekstra gang i ny basis. Hele
grunnlaget har dermed 23 valgbare tabellfelt på de to kontoene, men bare elleve
vedtaksfelt/fem monetære hendelser. Nye beregninger er separate avledede objekter.

| Utvalg 2024 | Alle kildefelt inkl. forslag/tilråding | Vedtaksfelt | Vedtatte hendelser |
| --- | ---: | ---: | ---: |
| /1 | 13 | 7 | 3 |
| /22 | 10 | 4 | 2 |
| Begge | 23 | 11 | 5 |
| Tomt / ustrukturert /60 | 0 | 0 | 0 |
| Dokument 341 | 2 | 2 | 2 |
| Dokument 857 | 3 | 3 | 1 |
| Dokument 210 | 6 | 6 | 2 |

Dokumentenes øvrige beløp/inventar er fortsatt i råkilden og synlig som
ustrukturert. Null i tellekolonnen betyr ingen **strukturerte utvalgsobjekter**,
ikke en nullbevilgning eller fravær av tekst/fullmakt/øvrige kildeposter.

### Viktig størrelsesfunn før kontrakt

Faktisk kilde: 341 har én tabell med **153 rader**; 857 én tabell med
**1 488 rader**. En enkel telling av numeriske postceller ga 116 og 603;
dette er ingen sertifisert full beløps-/hendelsesopptelling. Ikke kopier en
historisk rapportetikett som om den var en ny utført full inventaravstemming.
Vis hele råtabellens radinventar, kapittel-/postkontekst, total-/kontekstrader og
ustrukturerte deler, heller enn å importere hele RNBs monetære beløp.

T1/T2s **512 inventarrader er for lite allerede for 857**. Bevar gamle grenser;
fastsett en separat, begrenset T3-inventargrense basert på dette kildebehovet,
f.eks. 4 096 rader, og prøv overskridelse i ny leser. Dette er nødvendig ny
kontrakt, ikke å svekke gamle valideringer for å få tester grønne. Bevar øvrige
JSON-/payload-/gzip-/ZIP-/tekstgrenser der de faktisk rommer snittet.
Ikke skjul inventar bak bare en base64-/råfilreferanse.

## Hull og regnegrense

Synlige og navngitte hull: opprinnelig 2024-forslag/tilleggsforslag,
Innst.14/postvis vedtakelsesbevis, RNBs Prop104/kapittel5-original og postkobling,
gjenlesbar avgrenset Innst447-tilråding/rolle, konkret RNB-vedtakelsesbevis,
øvrige endringer/ukjent kontoomfang, vedtak uten proposisjon (ikke undersøkt),
uttømmende periodeinventar og årsavslutningsavstemming. Nysalderingsbeviset
lukker kun sin egen dokumenterte gren. 341/857 har autoritativt vedtaksobjekt,
men ingen her utført full forslag→tilråding→votering-kjede.

Lokal aritmetikk er kontrollert nå: 161 243 000 − 1 000 000 + 5 796 000 =
166 039 000; 32 185 000 − 3 000 000 = 29 185 000. Byggerens resultat skal binde
eksakte inngangs-ID-er og kontroll mot observerte før-/etterfelt. Manglende
inngang/konflikt sperrer beregning. Dette gir ingen godkjent årsbalanse,
ny B5-avgjørelse eller helårsdekning; mulige utlignende mangler er ikke utelukket.

## Påkrevde porter for byggeren

- M16/M17/M21/M22–M27 ved virkelig lukket/gjenlest JSON og XLSX. /1,/22,begge,
  tomt, kapittel, feil år, tekst/fullmaktskonto og alle valgte dokumenter.
  Begge navigasjonsretninger/retur og offline uten kildekatalog/nett/database.
- Faktisk serialiserte payload-/observasjonsforekomster i JSON og Excelpakke;
  én ny payload per eksakt hash, gamle råbyte som referanser når de finnes i
  kapselen, høyst én gammel kapsel og separat oppgitt arvet duplisering.
- Streng rekonstruksjon fra hashankre/byteoppskrifter. Muterte beløp, år,
  fortegn, runde, rolle, lokator, forelder, relasjoner, ID-er eller skjulte hull
  avvises også etter rehash, i begge faktiske filformater. Ingen dangling refs.
- Fem synlige hovedfaner som T2; globalt helinventar/fulltekst og kontrollark
  ved tomt utvalg. Tall/datoer/lenker og gruppenivåer må faktisk vises riktig.
  Lange felter deles tapsfritt; formeltegn er tekst; endret/falsk/skjult Excel-
  presentasjon skal avvises. Render allerede skrevet XLSX med Artifact Tool og
  inspiser forløp, stort dokumentinventar og tomt/globalt. Native Excel er et
  separat bevis og må ikke hevdes uten kjøring.
- Gjenles ekte gamle A/B/B6/B8/B9/T1/T2-filer fra hashkontrollerte kopier uten
  omskriving. Bruk repoets ekte T1-arkiv; øvrige lokale gamle outputs er omtalt
  i T2-overleveringen. Oppgi eksplisitt hvis selvstendig gammel frozen-v1-JSON
  fortsatt mangler; nygenererte gamle layoutprøver erstatter ikke den.
- Fire separate autentiske 368-prøver gjennom offentlig ordinær
  synkronisering→råbevaring→lagring→tolkning→Excel ved manglende, feilet, korrupt
  og motstridende T3-adapter, også med tomt T3-utvalg og uten historisk Excel.
- Innlesning kjører uten analyseimport. Bevar schema5, B5, gamle ID-er,
  parserbetydning/standarder og `legacy_html`-hjelper/streng historisk kontroll.
- TDD/implement ved eksisterende godkjente høye testgrenser; samlet Standards,
  Spec og separat defensiv audit på samme faste kandidat. Full statikk og
  Linux-CI hele pakken, 30-minuttersrammen/parserversjonslogging beholdes.
  Ikke fjern/skip tester eller svekk strenge kontroller for å få grønt.
- Varig kontrakt, kildebevis, akseptledger, hasher, faktiske artefakter,
  reproduksjonskommandoer og bevisgrenser i repo/GitHub. #37/#32/#10 åpne.

Ingen nye T3-produkttester, filrundturer, rendering eller ny CI er kjørt av utforskeren.
Sluttgrunnlaget og issueutkastet er kilde-/scopeleveranser, ikke levert T3.

## Neste prioritet etter T3

Anbefal **T4s smale separate årsforløp** først: legg til de to kildebevarte
201/40034038-nivåene for 2025 med ukjent kontinuitet. Det er neste lille komplette
snitt med råkilde allerede i repoet; ingen nett-/kontinuitetsport blokkerer
negativt kontinuitetsvern. Først etter T3-merge og nytt eiermandat/publisert
ticket: fersk main, samme filgrense, 2024 og 2025 hver for seg, 7 hendelser/
13 vedtaksfelt, ingen årsunion som samlet saldo. T4 er ikke bestilt her.

K2 før positiv kontokontinuitet og K3 før positiv helårsdekning er fortsatt
egne kildeporter. K1 før autentisk tallfestet parallellvariant, T5/T6 og generell
gammel normalisering/fanerydding er separate oppgaver. Velger eier i stedet å
prioritere en faktisk godkjent årsbalanse, er K3 neste kunnskapsoppgave; T4
gir ikke slik godkjenning. #10s vert/konto/drift er fortsatt separat.

Forslag til startprompt neste økt, tilpass T3-issue/PR/SHA etter faktisk merge:

> Fortsett fra fersk main etter bekreftet T3-merge i depmartin/budsjetthistorikk.
> Les AGENTS, #37 og siste T3-overlevering, kontraktene og konto-år/testmatrisen.
> Undersøk og legg frem ett konkret T4-snitt: 1429/1 og /22 i 2024 og opprinnelig
> 2025-vedtak 201/40034038 som separate årsforløp med synlig ukjent kontinuitet.
> Bruk originale byte og bevar gamle ID-er, én kompatibilitetskapsel og samme
> kildegrunnlag i begge innganger/faktisk gjenlest JSON/Excel. Ingen automatisk
> kontinuitet, årsbalansegodkjenning, full årsdekning eller drift. #10 åpen.
> Dette bestiller undersøkelse og ticketforslag; bygg/publiser/merge først ved
> mitt uttrykkelige mandat til akkurat T4.
