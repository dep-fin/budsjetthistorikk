# Uavhengig kildekontroll for #54 – sak 101000

Sluttrapport, revisjon 1, 28. oktober 2026. Kontrollbase:
`6b2441ee5e859d103ab44d78f12d33c374a89171` (P1-merge). Den selvstendige
førstekontrollen ble gjort på denne basen. Etterfølgende sammenhold og
siste kjøring gjelder den ferdige faglige kandidaten
`c61dcc7c9221aa485a764c954323e0aac25b9e82`.
Arbeidsflate: `work/r2-101000`. Ingen Git-/GitHub-mutasjoner er utført.
Bare filer i denne kontrollkatalogen er skrevet.

**Resultat:** Råhashene og de kontrollerte kildekjedene består. Prop. 34 S
har konkret bevilgningsforslag på **1560/71**, ikke en ny konkret
1429/1- eller /22-bevilgning. Romertall II er en generell lønnsregel.
Den indirekte henvisningen til departementenes omgrupperinger og FIN er
reell og må beholdes. Prop. 36 S vedlegg 4 har en **selvstendig eksakt
primærkildeobservasjon: 1429/1, 2 796 000 kroner**, med rollen anslått
lønnsvirkning foreslått i omgrupperingsproposisjonene. Det er ingen ekstra
vedtatt posthendelse. Vedtak 429 er en fullmakt om **overføring til 2025**;
faktisk bruk på Riksantikvarens poster er ikke belagt her.

**Ett nødvendig dokumentasjonsfunn står åpent mot kandidaten:** F1 nedenfor
gjelder en feilaktig sitert kildeoverskrift. Det endrer ingen tallkonklusjon.

## Uavhengighet og kontrollgrunnlag

Jeg har lest AGENTS/arbeidsflyten, hele #54 og dens tomme kommentarliste,
P1-kontrakten/kildebevisene, K3s README/M21/neste-snitt og O1/O2b-grensene.
Kildekontrollen er gjennomført direkte mot `.local/r2-recon` og repoets
bevarte originaler. Byggerens aktive rapporter, `evidence.py` og
`evidence.json` er ikke brukt som autoritet eller kontrollfasit. Etter at
byggeren var ferdig, er README, behandlingsledger og kryssreferansejournal
sammenholdt med den allerede etablerte kildefasiten. Kandidatens 22
original-/metadatapar er kontrollert byteidentiske med førstegangskontrollens
rårot. Siste kjøring bruker disse publiseringsklare originalene.

Dette er en selvstendig gjenlesing og rehashing av delte innhentede
originaler, **ikke en ny uavhengig HTTP-innhenting**. Transportopplysningene
er bevart fra innhentingen. Et lokalt samsvar med et manifest er ikke i seg
selv et eksternt autentisitetsbevis; kildeinnhold, komplett struktur og
separate API-/publikasjonsrepresentasjoner er kontrollert i tillegg.

[verify_sources.py](verify_sources.py) har ingen nett- eller produktimport.
[results.json](results.json) inneholder 27 gzip-/metadata-/bodybindinger,
to uendrede O1-kontekstoriginaler, 60 selvstendig lokaliserte passasjer,
fullstendige XML-objekter/HTML-fragmenter, PDF-tekst fra alle fire sider,
identitetskontroller og den komplette sjekklisten: **204 beståtte kontroller**.
Alle 27 gzip- og metadatafiler er rehashet; dekomprimert hash og arkivhash
holdes atskilt. Metadataenes eksakte byte/hash er også registrert.

De 27 representasjonene består av 22 nye forsøksrepresentasjoner og fem
gjenbrukte K3-originaler. 26 har status 200; ett DNS-forsøk har status 0,
curl-retur 6 og tom kropp. Tomhashen i sistnevnte er bevis for ingen mottatte
dokumentbyte, ikke fravær av saken eller omtalen. Vellykket ny saksrespons
ligger separat i `sak101000-retry.xml.gz`. Standard-HTML for Innst. 91 S er
bevart, men kontroll av hele innstillingen bruker `inns91-all.html.gz`.

Alle 116 filer under K3s forskningskatalog er sammenholdt byteeksakt med
basens Git-blober og er uendret. P1-katalogen har bare checkoutets eksisterende
CRLF mot Git-blobbens LF; innholdet samsvarer etter denne uttrykkelige
linjeskiftkontrollen. `git diff --name-only <base> -- innlesning analyse tests`
ga ingen endringer ved kontrollen. Ingen produktadopsjon, endring av
pinnede journaler, ny beløpsobservasjon eller ny posthendelse følger av
denne rapporten. Fem monetære hendelser/elleve vedtaksfelt er fortsatt
den eksisterende P1-grensen; ingen ny produktfil er eksportert her.

## Bekreftet forslag → tilråding → votering → vedtak

Alle XML-lokatorer bruker `s=http://data.stortinget.no`. HTML-lokatorer
gjelder bare den angitte representasjonens bodyhash. `results.json` har
både selector, absolutt XPath, full fragmenttekst og hash per passasje.

| Ledd | Selvstendig kontrollert lokator og resultat |
| --- | --- |
| K3-kandidat | `saker-2024-2025.xml`: `/s:saker_oversikt/s:saker_liste/s:sak[624]` er sak 101000, med Prop. 34 S/Innst. 91 S. Hele observerte indeks har 727 poster. Ordinalen beholdes sammen med sesjon og hash. |
| Saksdokumenter | `sak101000-retry.xml`: `/s:detaljert_sak/s:publikasjon_referanse_liste` binder proposisjon, innstilling, debatt og votering. Dette er dokumentrelasjon; postomfanget bevises nedenfor. |
| Regjeringens forslag | `prop34-ch5.html`, `#ch6`, har nøyaktig I og II og én tabell. Tabellen har overskriftene Kap./Post/Føremål/Kroner og nøyaktig tre `tbody/tr`: 1560, post 71, før/etter. Post 71 økes med 14 200 000, fra 233 100 000 til 247 300 000 kroner. PDF side 4 gjengir samme forslag; hele PDF-en har fire sider. |
| Omtale av konkret budsjettforslag | `prop34-ch3.html`, `#kap3_ch1` og `#kap3_ch1_ch1`, angir 1560/71 og opplæring/utvikling for tillitsvalgte. 14,2 mill. er beregnet etter årsverk/lønnsmasse per 1.10.2023. Dette er ikke lønnskompensasjon på 1429/1. |
| Komiteens tilråding | `inns91-all.html`, `#m3`, har nøyaktig romertall I/II, én tabell og samme tre rader/felt som proposisjonen. Tilrådingen fremmes av samlet komité. |
| Faktisk behandling | Hele `.strtngt_sak` i `ref171224-debatt6.html` er lest, til avslutningen «Flere har ikke bedt om ordet til sak nr. 6». `ref171224-votering.html`, `#2024-12-17-6`, identifiserer dokumentene, gjengir hele I/II og fastslår enstemmig vedtakelse. |
| Voterings-API | `voteringer101000.xml` har nøyaktig én `sak_votering`: 23887, tema «Romertallene I og II.», `enstemmig_vedtatt`, 17.12.2024 kl. 19.29.21.12. `antall_for/mot/ikke_tilstede=-1` er beholdt som API-sentinel, ikke null eller oppfunne stemmetall. |
| Forslags-API | `voteringsforslag23887.xml`: de to komplette `voteringsforslag` med `s:forslag_id='40077003'` og `'40077004'` er henholdsvis tilråding I og II. Dekodet `forslag_tekst` er sammenholdt med hele innstillingen og de endelige vedtakstekstene. |
| Vedtaksreferanse | `voteringsvedtak23887.xml`: objektene med `s:vedtak_nummer='230'` og `'231'` viser eksplisitt til tilråding I og II. Dette API-et har tomme vedtakstekstfelt; den faktiske teksten er derfor lest i komplett sesjonsoriginal, ikke utledet fra referansen. |
| Endelig vedtak | `ind-vedtak-2024-2025.xml`: `/s:stortingsvedtak_oversikt/s:stortingsvedtak_liste/s:stortingsvedtak[s:id='40034098']` og tilsvarende `'40034099'`. Sak 101000 har akkurat disse to komplette vedtaksobjektene: 230/231, 17.12.2024. 230 har hele den samme 1560/71-tabellen; 231 har hele den generelle lønnsregelen uten tabell. |

Den komplette strukturen i forslaget, tilrådingen, den særskilte
voteringsblokken, forslags-API-et og de to endelige objektene beviser
**ingen konkret 1429/1- eller /22-beløpsrad i disse vedtaksleddene**.
Dette er ikke en generell eksklusjon av indirekte betydning og bygger
ikke på ordfravær alene.

I romertall II har Prop. 34 formen «medlem av», mens innstilling,
forslags-API og endelig vedtak har «medlemer av». Kontrollskriptet bevarer
den bokstavelige forskjellen; de normaliserte øvrige ordene samsvarer.
I-tabellens normaliserte celler samsvarer gjennom hele kjeden.

Samlet tilråding betyr ikke fravær av politiske forskjeller. Hele Innst. 91 S
er kontrollert gjennom de åtte hovedblokkene `m1`, `m2`, `m2_1`, `m2_2`,
`m2_3`, `m2_3_1`, `m2_3_1_1`, `m3`. `m2_1` har flertallsmerknader fra
Ap/Sp/SV/R, særskilte H/FrP-merknader og R-merknader. `m2_2` har også andre
aktørgrupperinger. Merknadene kan ikke omskrives til alternative vedtatte
1429-beløp. Det kontrollerte saks-API-et og voteringen har de to tilrådingsleddene.

## Indirekte lønnsbevis og presisjon

**Bekreftet:** Prop. 34 S kapittel 2.1, `prop34-ch2.html#kap2-1-p10`, sier
uttrykkelig at virkningen på hver budsjettpost er foreslått i departementenes
omgrupperingsproposisjoner og viser til FINs nysalderingsproposisjon.
Henvisningen er dermed en reell undersøkelsesvei, selv om 34s egen tabell
har annet kontoomfang.

FIN-kilden er kontrollert i `prop36-ch5.html#kap5`, særlig `#kap5-p1`,
`#kap5-p4` og `#kap5-p5`. Den beskriver hva som normalt innarbeides på
Stortingets fullmakt, men sier at det i 2024 er innarbeidet et anslag ved
nysalderingen. Anslaget bygger på YS-avtalen og omfatter også virkningen på
pensjonspremieutgifter. Departementenes omgrupperingsforslag står i vedlegg 4.
Dette dokumenterer ikke at en normal fordelingsfullmakt faktisk er brukt
for 1429/1 med et bestemt beløp.

**Ny eksakt kildeobservasjon:** `prop36-ch11.html` er vedlegg 4, «Endring av
utgifter som følge av lønnsoppgjøret for statsansatte». Den ene komplette
tabellen har 373 kroppsrader og enhet **Kroner**. Eksakt lokator er:

```text
/html/body/main/div/div[3]/div[3]/div/div/table/tbody/tr[292]
  1429 | [tom] | Riksantikvaren: | [tom]
.../tr[293]
  [tom] | 1 | Driftsutgifter | 2 796 000
.../tr[294]
  1471 | [tom] | Norsk Polarinstitutt: | [tom]
```

Hele blokken 1429 er dermed post 1-raden, avgrenset av neste kapittel 1471.
Det finnes ingen /22-rad i denne avgrensede vedleggsblokken. Observasjonen
av 2 796 000 kroner er lest direkte fra råcellen. Den er ikke utledet fra
5 796 000 minus 3 000 000 eller fra avrunding av 2,8 mill.

**Bevart O1-grense:** Uendrede O1-originaler er rehashet og gjenlest.
`prop16s-ch2.html#kap2-p24` bruker fortsatt anslått 2,8 mill. for lønn,
3 mill. for omdisponering og avrundet samlet 5,8 mill.; `#kap2-p25` er
post 22-motposten. Forslagstabellens `tbody/tr[43–47]` har eksakt
1429/01 +5 796 000 og /22 −3 000 000, med neste kapittel i rad 48.
Hele 210/40034048 er i tillegg gjenlest fra komplett sesjonsoriginal.
Den nye vedlegg-4-observasjonen skal ha sin egen kilde/rolle, uten å
endre hva som faktisk var kildeobservert i O1/O2b eller bli en ekstra
vedtatt deltakomponent. Det numeriske samsvaret med den gamle regneresten
er en kontroll, ikke grunnlaget for den nye kildeobservasjonen.

**Sentral avsetning er separat:** `inns90-all.html#m1_3_18_1_1` omtaler
kap. 2309 post 1 som motpost til blant annet lønnsoppgjør og uforutsette
utgifter. Dette må holdes atskilt fra 1560/71, fra vedlegg-4-fordelingen
og fra det konkrete postvedtaket 210. Kapittel 2309-omtalen er et sammendrag
av regjeringens forslag i innstillingens innledning, ikke selv et bevis
for en ekstra 1429-bevilgning eller en utført fordeling.

## Smal kontroll av sak 100289 og fullmakt 429

Sak 100289 er gjenlest med publikasjonshenvisningene til Prop. 36 S og
Innst. 90 S. Følgende faktiske tekstkjede er kontrollert:

| Ledd | Eksakt lokator og rolle |
| --- | --- |
| Regjeringens omtale | `prop36-ch5.html#kap5-p5`: forsinket lønnsoppgjør, mulig etterbetaling i 2025 og forslag om avbøtende overføring. `inns90-all.html#m1_5_1` gjengir dette under lønnsoppgjøret. |
| Forslag | `prop36-ch7.html`: `#kap5-p15` i romertall II under `#ch8`. |
| Tilråding | `inns90-all.html`: `//*[@id='m3']//*[@data-strtngt-romertallseksjon-romertall='ii']`. |
| Faktisk forslagstekst | `voteringsforslag23945.xml`: komplett objekt med `s:forslag_id='40078386'`, dekodet `forslag_tekst`, romertall II. |
| Votering | `voteringer100289.xml`: komplett `sak_votering[s:votering_id='23945']`, 19.12.2024 kl. 14.39.29.063, enstemmig, tema resten av I samt II/III/IV. |
| Vedtaksforbindelse | `voteringsvedtak23945.xml`: `voteringsvedtak[s:vedtak_nummer='429']` viser uttrykkelig til tilråding II. Referansene til 430/431 holdes atskilt. |
| Endelig ordlyd | `ind-vedtak-2024-2025.xml`: komplett `stortingsvedtak[s:id='40034289']`, vedtak 429, sak 100289, 19.12.2024. Hele fullmaktsteksten samsvarer gjennom forslag, tilråding, forslags-API og endelig vedtak. |

**Bekreftet rekkevidde i ordlyden:** Finansdepartementet kan øke maksimalgrensen
for overføring av ubrukte driftsbevilgninger til 2025 tilsvarende kompensasjonen
for lønnsoppgjøret 2024 og fastsette en overføring som minimum tilsvarer
kompensasjonen, slik at virksomhetene har dekning for etterbetaling som skyves
til 2025. Fullmakten inneholder ingen postvis beløpstabell.

**Ikke belagt her:** et faktisk vedtak fra FIN om en bestemt overføring på
1429/1 eller /22, at vilkårene faktisk inntraff hos Riksantikvaren, et faktisk
overført/etterbetalt beløp eller regnskapsføring i 2024/2025.

**Uavklart:** den konkrete anvendelsen på Riksantikvarens poster. At ordlyden
er generell og gjelder driftsbevilgninger, og at vedlegg 4 har en post-1-rad,
er ikke alene bevis for at fullmakten faktisk er anvendt på akkurat denne
posten. Dette er en overføringsfullmakt, ikke belegg for at 429 fordeler
eller øker den vedtatte 2024-bevilgningen med 2 796 000 kroner.

## Datokonflikt som ikke skal glattes over

Prop. 34 S `#kap2-1-p2`, `#kap2-1-p8` og `#kap2-1-p9`, samt Innst. 91 S
`#m2_1`, omtaler samtykker **20. juni 2024**. Den komplette sesjonsoriginalen
for 2023–2024 har derimot:

| Vedtak | API-ID | Sak | Kildens dato |
| --- | --- | --- | --- |
| 853 | 40033712 | 99235 | 2024-06-21 |
| 854 | 40033713 | 99235 | 2024-06-21 |
| 855 | 40033714 | 99235 | 2024-06-21 |
| 856 | 40033715 | 99235 | 2024-06-21 |

De fire komplette objektene og datoene er gjenlest direkte fra XML, ikke
fra K3s avledede register. **Bekreftet kildekonflikt; ikke avklart historisk
samtykkedato i dette snittet.** Hele juni-saken og plenum er ikke undersøkt
her. Bevar begge kildeutsagn og ikke omdater objekter på grunnlag av
senere omtale. Konflikten endrer ikke den kontrollerte desemberkjeden.

## Bindinger og reproduksjon

Fullstendige URL-er, status, UTC-observasjonstid, arkiv-/metadata-/bodyhash,
byteantall og lokatorer finnes i `results.json`. Utvalgte sentrale bodyhasher:

| Representasjon | SHA-256 for dekomprimert kropp |
| --- | --- |
| Prop. 34, forslag HTML | `91af0aa1830d84a125c950dfe010eed11496f8d56767f792adb2aaa4e9e8669b` |
| Hele Prop. 34 PDF | `99c0323aa5250a7a741acf83321136e0ecd3707630632ebdf19d91d72c7acc90` |
| Hele Innst. 91 HTML | `745a24367b3b93979f19b8ef2396cdfed5edf1d80ef887f648b459728e57e8ea` |
| Voteringsreferat 17.12 | `fd3bc47915e760b95c170725e55c4b564b37512f2a813db91b87c66ec1424ab1` |
| Forslag 23887 | `42fe2d3b6d18d10277f31bede9a460829431666acc6785fab041f81044412913` |
| Vedtakssesjon 2024–2025 | `ff5013b2a37220af3254a69b574800f99a3d1fd44f1c6053f07d4b0e846c973c` |
| Prop. 36 vedlegg 4 | `0c88959a60162ed44a9dcf54871e03c8479fd779f5ea5e01948c270b25517586` |
| Innst. 90 komplett HTML | `c75f2df5f4280c3a4b327219f60bb48fda52da8e26ea927f0f6e4d2ba92299cb` |
| Forslag 23945 | `6db2f925711246018c128f581801b70f09313a7c13d921d242f36e349ae82211` |

Kjøring fra reporoten med P1s allerede installerte, pinnede avhengigheter:

```powershell
$env:PYTHONPATH=(Resolve-Path ../p1-perioderegister/.local/python).Path
& ../p1-perioderegister/.venv/Scripts/python.exe docs/research/r2-101000-54/reviews/source-control/verify_sources.py
& ../p1-perioderegister/.venv/Scripts/python.exe -m ruff check docs/research/r2-101000-54/reviews/source-control/verify_sources.py
& ../p1-perioderegister/.venv/Scripts/python.exe -m ruff format --check docs/research/r2-101000-54/reviews/source-control/verify_sources.py
```

Skriptet krever Git, lxml og pypdf; det skriver bare sin egen `results.json`.
Standard rårot er `.local/r2-recon`. Siste kjøring brukte
`--raw-root docs/research/r2-101000-54/originals`. `--raw-root <katalog>` kan
brukes med de 22 byteidentiske gzip-/metadataparene i en publisert originalkatalog.
Gjenbrukte originaler løses fra repoets frosne K3-/O1-kataloger. Alle
basekontroller gjøres fortsatt mot den oppgitte P1-mergen.

Siste kontroll brukte Python 3.12.14, lxml 6.1.3 og pypdf 6.10.0.
Ruff check og formatkontroll av kontrollskriptet består. Ingen native
Excel, visuell PDF-kontroll, produkttest, full CI, ny årsavstemming eller
faglig godkjenning påstås utført av kildekontrolløren.

Frosset kontrollskript: SHA-256
`8629a24f9d19b45630c1948e98ccfa9de5aac5b2ceff24ec39a35ce980b09afc`.
Frosset `results.json`: SHA-256
`d71365a80c4e95d272b497740fc7df287643ac262bede9a497c4878fa5db022b`.
Filer og kopisamsvar ved sammenholdet med ferdig kandidat er bundet i
[candidate-comparison.json](candidate-comparison.json).

## F1 – rett den uriktige kildeoverskriften før levering

Kandidat `c61dcc7` oppgir «Lønnskompensasjon 2024» som kildeinnhold i
[README rad 22](../../README.md) og som «overskrift» i behandlingsledgerens
`FIN-1429-1`, linje 170. Den faktiske overskriften i den hashbundne
`prop36-ch11.html` er:

```text
//*[@id='ved4']/h1
4 Endring av utgifter som følge av lønnsoppgjøret for statsansatte
```

Dette er kontrollert direkte i originalen og som egen passasje
`annex4-actual-heading` i `results.json`. «Lønnskompensasjon 2024» kan være
en passende oppsummerende etikett, men er ikke kildens sitat eller
overskrift. Rett README og ledger til faktisk overskrift, eller merk
etiketten uttrykkelig som en egen oppsummering. Den eksakte postcellen,
enheten, anslagsrollen og konklusjonen om ingen ekstra hendelse består.
Dette er en nødvendig kildepresisjonsretting, ingen ny kildeundersøkelse.

Vedleggssiden har også dokumentmerkingen «Foreløpig utgave» i hovedsidens
presentasjon. Den observerte HTML-versjonen og råhashen beholdes; det er
ingen påstand om at en annen endelig trykkrepresentasjon er kontrollert.

## Nødvendige avgrensninger ved videre levering

Ingen råhash- eller identitetsavvik står åpne i denne kontrollen. F1 over
står åpent mot ferdig kandidat. Ingen andre nødvendige kildefunn ble funnet
ved sammenholdet med README, behandlingsledger og kryssreferansejournal. Den
ferdige forskningsleveransen må likevel bevare alle disse punktene:

1. Direkte 1560/71-vedtak og generell lønnsregel holdes atskilt fra indirekte
   1429-lønnsomtale og postforslag.
2. Den nye eksakte 2 796 000-observasjonen får primærkilde, anslagsrolle og
   egen lokator; den er ingen ekstra vedtatt delta eller en endring av O1s
   historiske presisjonsgrense.
3. Fullmakt 429 gjengis med sin faktiske overføringsrekkevidde. Konkret
   anvendelse på valgt post/virksomhet står uavklart.
4. Samlet tilråding og enstemmig vedtakelse forenes med bevarte særmerknader,
   ikke en påstand om at alle komitéutsagn var enstemmige.
5. Kildenes 20./21. juni-konflikt bevares uten konstruert løsning.
6. Konklusjoner om manglende konkrete rader begrenses til de komplette,
   navngitte strukturene som faktisk er kontrollert.

Dette er kildefasit og bevisgrense for den avgrensede undersøkelsen. Det
etterfølgende sammenholdet gjelder kandidatens uttrykkelige kildepåstander,
ikke hele dens tekniske verifikasjonsopplegg eller full CI. De øvrige R2-
kandidatene, hele juni-saken, faktisk fullmaktsanvendelse, positiv M21,
produktadopsjon og faglig årsbalanse er utenfor denne kontrollen.
