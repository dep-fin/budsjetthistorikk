# T3: valgt 2024-forløp

Kontrakt fastsatt 27. oktober 2026 **før produktkode** under #46, del av #37.
Opt-in `visningspilot-3`, regel `forlop1429-2024-1`, har egen adapter/leser.
De avtalte testgrensene er original → kildebundet felt/tekst → dokumentert
relasjon → begge innganger → faktisk skrevet, lukket og gjenlest JSON/XLSX.
TDD utføres ved disse allerede godkjente offentlige grensene (#1/#46).

## Kilder og identitet

341 og 857 avledes fra den bevarte 66aa-fullresponsen, 6 816 165 byte:
`prefix[:317]+object+separator+suffix[6816110:]`. 341 bruker intervallet
`[6092492:6209173]`, separator LF og konvolutt-SHA
`73bbcdc1d83a539ab4f3c2fad7b2b2972e003e742a5391a003d19c38149b6e71`.
857 bruker `[2552391:3817852]`, tom separator og konvolutt-SHA
`252544da8756b038d54f6e935323fb33227b7ef16ee4c540a1badb7c5245517f`.
Dette er avledninger, ingen nye HTTP-svar. Gzip, transportmetadata og
forskningsmanifest bevares. Den gamle 857-fixturen/sidevognen bevares som
selvstendig kontroll: objektbyte er like, men dens oppgitte 554e-forelder
mangler. 66aa ommerkes aldri til 554e. Ingen ekstra beløpshendelse opprettes.

Helinventaret skiller uttrykkelig postkolonne/tilgrensende før-/etterrad fra
totaler, SDØE-spesifikasjoner og øvrig kontekst. Total-/komponentrader arver
ingen postkode. Dokumentets kontoliste består av faktisk observerte
tabellreferanser; avgrenset /22-fravær gir ingen positiv /22-medlemskap i 857.
Ved kilde-/transportfeil skilles bevart forelder fra manglende strukturering.

Komplett 341→857→210 krever én validert, ordrett T1-kapsel. Dens 18 felt,
seks vedtaksfelt/to hendelser og 9cfe-proveniens gjenbrukes med gamle ID-er.
Ingen T2-pakke/315-data kreves. Innlesningsadapteren mottar typet tidligere
grunnlag fra analyse; den importerer ikke analyse. Standalone bevarer de fem
nye feltene og viser manglende 210-grunnlag som hull. Ny vedtaksinnlesning
kjører uavhengig av T3, T1-kapsel og historisk Excel.

Konvolutt/basis/kilde/payload/utvalg følger T2s dokumenterte feltmønster med
egne versjoner `forlopsgrunnlag-1` og `visningspilot-3`. Nye objekter får eget
navnerom `forlop*`; observasjoner bruker `observasjon-1`/`source_system=forlopspilot`.
Identiske byte lagres én gang per hash, eller som peker til eksisterende
T1-kilde. Avledede kilder peker til forelderens payload og eksakt oppskrift.
Gamle objekter serialiseres bare inne i én uendret `legacy_json`, ikke i ny basis.
Rapportens eksakte felter er `id,basis,selection,return_selection,view,
calculations,version`; ytterkonvolutten har bare `format,report`.

## Utvalg og kontroll

341/19.12.2023 gjelder budsjett **2024**, med nivå 161 243 000 (/1) og
32 185 000 (/22). RNB 857/21.06.2024 gir /1 før 161 243 000, delta −1 000 000,
etter 160 243 000. Hele 1429-blokken `tr[822–830]` før 1432 i `tr[831]`
mangler /22-beløpsrad; dette er avgrenset kildefravær, ingen nullhendelse.
210/16.12.2024 beholder +5 796 000/−3 000 000 og gamle før-/etterfelt.

Fasit tabellfelt/vedtaksfelt/hendelser: /1 **13/7/3**, /22 **10/4/2**,
begge **23/11/5**, tomt **0/0/0**, dokument341 **2/2/2**, dokument857 **3/3/1**,
dokument210 **6/6/2**. Tekst/fullmakter er ikke monetære hendelser.

Rapporten har separat `calculations`: ID, konto, budsjettår, regel, status,
begrunnelse, eksakte `input_ids` og `check_ids`, beregnet og observert kroneverdi.
Kun ett kildebelagt startnivå og vedtatte deltaer i dokumentert rekkefølge
adderes. Før-/etterfelt kontrollerer lokale trioer og overganger. /22 bruker
det eksplisitt avgrensede RNB-fraværsbeviset. Resultat 166 039 000 og
29 185 000 merkes **avgrenset kontroll**; manglende inngang/konflikt sperrer
og gir null resultat. Ingen faglig godkjenning, B5-avgjørelse, årsbalanse eller
helårsdekning. Beregningen oppretter ingen kildefelt/hendelse.

Utvalg bruker union av konkrete par/kapitler innen eksplisitte år.
Dokumentåpning viser hele dokumentinventaret og bevarer returvalg. Alle
globale kilder, fulltekster og navngitte hull består ved tomt valg. Arvede
T1-avvik merkes `T1-kapsel:` i den nye projeksjonen; originalkapselen er uendret.
Hullene
omfatter opprinnelige forslag/tillegg/Innst14/postvis vedtakelse,
Prop104/kapittel5/Innst447/postvis RNB-vedtakelse, øvrige endringer/ukjent
omfang, vedtak uten proposisjon, periodeinventar og årsavslutningsavstemming.

## Streng filgrense og Excel

Alle objekter og visninger rekonstrueres fra faste uavhengige bytehashankre,
typet validert T1 og oppskrifter. Rehash legitimerer ikke endrede felt,
roller, år, fortegn, runder, relasjoner, foreldre eller skjulte hull.
Duplikatnøkler, NaN, dangling refs og ekstra felter avvises. T3 setter egen
inventargrense **4096**: 341 har 153 tabellrader og 857 1488, i tillegg til
tekstkontekst. Gamle 512-grenser beholdes. Øvrige vern: 64 MiB JSON,
16 MiB/payload, 32 MiB utpakket gzip, 64 payloads/kilder, 16 dokumenter,
512 utsagn, 256 beløp og 1024 relasjoner. Excel har 128 MiB ZIP-utpakkingsvern.

Fem hovedfaner: **Forløp, Dokumenter, Omtale, Sammenligninger, Dekning og avvik**.
Tilgjengelige kontrollark og én selvforsynt Offlinegrunnlag-kapsel følger T2.
Forløp viser nivå separat fra før/endring/etter, runde og kildebelagt kronologi.
Sammenligninger viser også de avgrensede regnekontrollene med inngangs-ID-er.
Globalt helinventar og fulltekst er tilgjengelig også ved null treff.
Tekst/JSON deles tapsfritt i 30 000 tegn; formeltegn lagres som tekst.
Den faktiske presentasjonen (celler, typer, stil, lenker, dimensjoner, synlighet)
avstemmes mot rekonstruert bok, med samme strenge ZIP/XML-vern som T2.
Repoets etablerte openpyxl-skriver videreføres; Artifact Tool brukes til
rendering av de allerede skrevne filene. Native Excel er separat bevis.

Schema 5, B5, gamle formater/ID-er/parserbetydninger, `round='uavklart'`,
legacy_html og standardvalg består. #10/#32/#37 forblir åpne.

## CI-ramme før samlet review

27. oktober 2026 økes jobbgrensen fra 30 til **40 minutter** med grunnlag i
[målt tidsbruk og dokumentert bevisgrense](research/forlopspilot-46/ci-budget.md).
Hele Linux-workflowen, fullsuiten, de statiske kontrollene og
parserversjonslogging beholdes. Full grønn Linux-CI på den endelige kandidaten
er fortsatt en leveringsport. Eldre hashfestede T3-rapporter beskriver den
tidligere 30-minuttersrammen og bevares uendret som historiske byggebevis.
