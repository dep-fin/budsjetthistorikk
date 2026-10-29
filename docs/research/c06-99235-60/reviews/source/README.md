# Uavhengig kildekontroll av C06 / #60

Kontrollert 29. oktober 2026. Fast kandidat er
`9eb27cebf7ca4a99aeb30fa32245e41314e0d295`; fast base er
`49cc6e44851cf74e0aaea4eb333419e5598bfd95`. Kontrollarbeidet er separat
fra byggeren. Kandidaten og tidligere originaler er ikke endret.

**Kildeport: BESTÅTT MED ÉN IKKE-BLOKKERENDE P3-MERKNAD.** Ingen
kildefaglig feil som endrer konklusjonen er funnet. Dette er bare
kildeporten; rapporten bekrefter ingen PR, full CI, merge, positiv
årsdekning eller produktadopsjon.

## Funn

**[P3] J02 har et foreldet antall visuelt leste sider.**
[cross-reference-journal.json](../../cross-reference-journal.json#L34),
`references[id=J02].investigated_scope`, sier «14 nøkkelsider».
Sidejournalen har 18 `visual_review=true`, og README/lesejournalen oppgir
de samme 18 sidene. Jeg har selv lest disse 18 originale bildene.
Det faktiske lesebeviset er derfor til stede; den korte beskrivelsen i
J02 er inkonsistent. Rett tallet til 18 og oppdater berørt manifest i en
eventuell ny kandidat. Ingen original, tolkning eller kildekonklusjon
behøver å endres. Funnet er også lagret i `result.json` under
`nonblocking_findings`.

## Utført kontroll og uavhengighet

AGENTS, arbeidsflyt, issue-tracker, begrepsregler/GLOSSARY,
perioderegisterkontraktene og relevant K3/R2/U1-kontekst er lest.
Hele #60 og kommentaren er hentet direkte gjennom GitHub-koblingen;
ticketens avgrensning og akseptporter er kontrollgrunnlaget.

[independent_check.py](independent_check.py) er skrevet for denne
kontrollen. Den importerer ingen C06-bygger eller C06-verifier. Den
rekonstruerer arkiv-/entity-hasher, metadata, redirectbindinger,
lokatorer, kildetekst, hele vedtaksobjekter, figur-/bildeinventar,
OCR-/sidejournalbindinger, historiske tellinger og Git-bevaring direkte.
Prosessidentiteter/datoer gjenfinnes dessuten gjennom semantiske XML-felt,
uavhengig av kandidatens oppgitte XPath-lokatorer.

Sluttkjøringen i [result.json](result.json) har **1 786 beståtte
maskinelle kontroller**, null feil i disse kontrollene og P3-merknaden
separat. Maskinkontroll av hasher/lokatorer er supplert med egen lesing
av primærinnholdet og originalbildene; bestått hash er ikke kalt en
selvstendig faglig godkjenning.

Følgende er konkret kontrollert:

- Alle 16 nye transportforsøk og 20 mottatte HTTP-hopp. Femten forsøk
  ender med komplett 200-svar; DNS-feilen har ingen fabrikkert respons.
  Arkivbyte, dekomprimerte entity-byte, metadatahash, størrelser,
  Content-Length/Content-Encoding og hver observerte redirectbinding
  stemmer. De oppgitte HTTPS-vertene er beholdt gjennom hvert hopp.
  Ingen ny primærhenting var nødvendig eller utført.
- Alle 18 refererte gjenbruksfiler er kontrollert med egne hasher,
  inkludert entity-hashene der de finnes. K3/R2s gamle transportspor,
  feilforsøk og representasjoner er bevart.
- Alle **87 belegg**: **69** maskinelle tekstbelegg har riktig kildehash,
  én eksakt lokator og samme tekst etter den dokumenterte
  whitespace-avledningen. De øvrige **18** er egne visuelle belegg,
  kontrollert mot originalbildene uten å kreve OCR-/XPath-tekstlikhet.
- Full Prop. 108-PDF har **144 sider**, hash
  `8fc583f4a20882d95ada3c36359a19c29ceb22cee51c6c572d948e63dbb8a419`.
  PDF-ens tekstlige innledning/forslag, innholdsfortegnelse,
  vedleggsoverskrifter og sluttsider er undersøkt. Egne HTML-vedlegg
  har hver nøyaktig 65 figurer, og PDF-en har 65+65 innlagte
  vedleggsbilder på side 11–75 og 77–141. Alle 130 bilder er
  ekstrahert og hashkontrollert på nytt.
- Alle 130 OCR-/sidejournalposter er bundet tilbake til sitt faktiske
  bilde og den bevarte OCR-teksten. En egen gjennomgang av sidestarter,
  seksjoner og relevante søkekontekster finnes i `appendix_screening`
  i kontrollresultatet. Dette er screeningsbevis, ingen feilfri
  transkripsjon eller ordfraværsbasert eksklusjon.
- Jeg leste selv originalbildene på PDF-side
  **11/12/13/14/16/39/40/50/69 og 77/78/79/80/82/105/106/116/135**
  i original oppløsning. Jeg leste i tillegg **17 og 83** visuelt for
  å kontrollere den lokale fordelingsregelen i § 2.5.1 direkte.
  De midlertidige JPEG-uttrekkene er fjernet etter kontrollen og kan
  reproduseres fra original-PDF-en.

## Egne primærfunn

Hele nødvendig lokal hovedkjede er lest: Prop. 108 hovedtekst og egne
vedlegg med angitt lesedybde, Innst. 442 `#m1`–`#m3`, komplett lokal
debatt i sak 15, voterings-/forslags-/vedtaksresponsene for 99235/23490,
sakens voteringsblokk i det komplette 21. juni-referatet og alle fire
hele endelige sesjonsobjekter. Komitémerknadenes ulike avsendere er
holdt adskilt fra samlet tilråding.

| Spørsmål | Uavhengig kontrollert belegg og vurdering |
| --- | --- |
| Debatt og votering | Saksoriginalens BEHS er 20.06.2024 og VOT er 21.06.2024. Debattreferatet avslutter med fremoverlenken «Votering, se fredag 21. juni». 21. juni-referatets `#2024-06-20-15` sier uttrykkelig at saken ble debattert 20. juni. ID-en daterer debatten; referatets møtedato er 21. juni. |
| Eksakt voteringsidentitet | Originalens `votering_id=23490`, `sak_id=99235`, `votering_tid=2024-06-21T14:11:27.147`, I–IV og `enstemmig_vedtatt` stemmer. Ingen tidssone er lagt til. −1-feltene er rå sentineler, ikke stemmetall. Møtestart 14:01:04 er et annet felt. |
| Forslag og endelig tekst | 40075780–40075783 er de fire tilrådingene. Tilråding, voteringsforslag, referat og sluttvedtak har lik normalisert tekst for hvert romertall. Regjeringsforslagets I og III har de dokumenterte ordlydsforskjellene; II og IV er like. Ingen ny endring er funnet i den komplette lokale debatten. |
| 853–856 | Hele objektene 40033712–40033715 i begge eldre sesjonsoriginaler er C14N-like. Nummer, sak, tekst og 21. juni-dato stemmer. Voteringsvedtaksresponsen binder I–IV til 853–856; den manglende vedtaksteksten der er ikke oppfunnet. |
| Senere datoutsagn | Prop. 34 kapittel 2 p2/p8/p9 og Innst. 91 `#m2_1` er kontrollert direkte i de gjenbrukte originalene. De oppgir 20. juni som samtykkedato. Dette er reell bevart motstrid mot primærbehandlingens voterings-/vedtaksdato. Ingen årsaksforklaring eller kilderettelse er dokumentert. Kandidatens ukjente årsak er riktig grense. |
| Riksantikvaren | PDF 69/135, figur 1.59/2.59, intern tariffside 56, har Riksantikvaren i både virksomhets- og forhandlingsstedskolonnen under KLD. § 2.2 på 16/82 viser til denne listen. Dette er positiv institusjons-/forhandlingsrelevans. |
| Lokal lønnsfordeling | PDF 17/83, intern tariffside 4, § 2.5.1, beskriver DFD-beregning og forholdsmessig fordeling etter årslønnsmasse, 2,15 % lokalt fra 1. mai og forhandlingsfrist 31. oktober. Det er en generell regel med eget beregningsgrunnlag; ingen konkret 1429-postfordeling er observert. |
| Talltreffet 1429 | PDF 50/116, intern tariffside 37, plan 90.910, viser Stillingskode 1429, Aspirant, minstelønn 357 000. Kolonne, rad og kontekst er lest visuelt. Koden er ikke et observert budsjettkapittel, og minstelønnen er ingen bevilgning. |
| Øvrige tariffstørrelser | 5,2/0,8/2,5 %, 75/25 og 0,75 % på 13/79 er tariffpremisser. På 39/105 står OU 0,24 %, arbeidstakertrekk 400 og 7 mill. til felles tiltak. På 40/106 står 26 mill. til kompetanse, søknads-/DFØ-roller og 4 mill. til omstilling. Disse har egne finansieringsroller og dokumenterer ingen faktisk Riksantikvaren-tildeling eller ny 1429-bevilgning. |

Den positive operative forskjellen mellom utbetalingssamtykke og
postvis budsjettbevilgning er avgjørende: Prop. 108 kapittel 2 p7 og
Innst. 442 omtaler uttrykkelig nødvendige bevilgningsforslag i
høstsesjonen. 853 er nemndshjemmel; 854 er utbetalingssamtykke;
855 og 856 har de dokumenterte betingelsene. De er ikke dokumenterte
nye bevilgningsendringer på 1429/1 eller /22.

For **1429/1 i 2024** står den gamle, selvstendige Prop. 36 vedlegg
4-observasjonen på **2 796 000 kroner** fortsatt som foreslått
kompensasjonsanslag. Originalens kapittelrad tr292, post-/beløpsrad
tr293 og neste kapittel tr294 er kontrollert. Dette er ikke en ny
C06-fordeling eller vedtatt monetær hendelse. Den gamle metodeomtalen
i Prop. 36 kapittel 5 beholder sin rolle.

For **1429/22 i 2024** foreligger ingen selvstendig dokumentert
C06-fordeling. Virksomhetsnavnet og /1-raden beviser heller ikke null
faktisk virkning på /22. Ingen /1-forklaring er arvet. For begge poster
er faktisk avtaleanvendelse, ansatte, lønnsmasse, lokale protokoller,
kostnader og kontoføring uttrykkelig uavklart.

## Bevaring og kompatibilitet

Git-trærne er sammenlignet direkte: alle **1 070** tidligere filer
utenom AGENTS/kildefunn har uendrede Git-blob-ID-er. De to pekerne er
additive; alle øvrige nye kandidatfiler ligger under C06. Det komplette
bevaringsmanifestets checkout-hasher er dessuten kontrollert på nytt,
og leveransemanifestets hasher er prøvd mot kandidatens faktiske
Git-blobbyte. Produktkode, tester, CI-konfigurasjon, schema 5, B5,
gamle formater/ID-er/lesere/standardvalg og pinnede K3/P1/R2/P2/U1-filer
har dermed samme versjonerte innhold som i basen.

K3-indeksen er lest direkte: 99235 er ordinal 114, innstilling 16526.
Hele den gamle kandidatlisten er telt uavhengig: **67 forekomster /
66 unike**, hvorav **60 åpne / 59 unike**. 99235 finnes ikke i denne
listen. C06-oppfølgingen er derfor additiv uten å lukke historiske
kandidater. K3s gamle ledger har fortsatt **fem monetære hendelser /
elleve vedtaksfelt**, delvis årsdekning og ingen faglig årsaksept.

Jeg kjørte også tre uendrede P1/P2-kompatibilitetstester selv:
**3 bestått på 55,10 sekunder**. De omfatter faktisk skriving,
lukking og gjenlesing av et JSON-/Excel-par. Deretter telte jeg den
skrevne JSON-filen direkte, uten produktleseren: **5/11**, **67**
globale sakskandidater, **25** vedtakskandidater, åpne **R1–R7**,
`partial` og `professional_annual_balance_approval=false`.
[runtime-result.json](runtime-result.json) bevarer kommando,
testresultat, filstørrelser og SHA-256 for det faktiske filparet.
Store midlertidige testfiler er fjernet etter kontrollen.

## Reproduksjon og grenser

Kjør fra checkoutens rot med oppgitt Python og `PYTHONPATH=.local/python-tools`:

```powershell
$sourcePython = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = '.local/python-tools'
$env:PYTHONDONTWRITEBYTECODE = '1'
& $sourcePython docs/research/c06-99235-60/reviews/source/independent_check.py
```

`--images` ekstraherer de 18 journalførte kontrollbildene i denne
kontrollmappen. Visuell lesing er et menneskelig/agentutført kontrollsteg;
skriptets hasher beviser ikke at noen har lest bildet. Runtimekommandoen
finnes i `runtime-result.json`; kjør den med samme Python og en ny
`--basetemp` under denne kontrollmappen.

Originalene er frosne observerte HTTP-entity-byte. Ingen uavhengig ny
liveobservasjon, TLS-/wirebevaring eller garanti for senere nettilstand
påstås. Dette er full råbevaring og dokumentert avgrenset innholdslesing;
jeg har ikke manuelt transkribert alle 130 bilder eller utført
uttømmende rettslig/personellmessig anvendelseskontroll. Feilfri OCR,
alle eksterne avtaleversjoner, nemndskjennelser, 2022-behandling og
faktisk bruk av 231/429 er ikke akseptert gjennom denne porten.
De nødvendige lokale krysshenvisningene har undersøkt delomfang og
uttrykkelig rest i J01–J12; eksterne/operative rester er ikke kalt
ekskludert. Restene og K3s globale R1–R7 består.

Ingen produktadopsjon, ny monetær hendelse, kontokontinuitet,
positiv M21, faglig årsbalanse, drift, fullsuite eller Linux-CI er
bekreftet av denne rapporten. Bare denne faste kandidaten er vurdert;
en senere innholdsendring krever ny kandidatbinding og relevante
etterkontroller.
