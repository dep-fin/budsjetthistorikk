# Endelig uavhengig kildekontroll av U1 / #58

**Resultat: bestått innen undersøkelsens uttrykkelige kilde- og postgrense.
Ingen rettingskrevende funn (P0–P3).** Konklusjonen om ingen ny dokumentert
direkte eller indirekte postvirkning på 1429/1 eller /22 i 2024 er støttet
av de undersøkte originalene. Den er ikke bevis for null faktisk virkning,
full årsdekning eller fullstendig ekstern versjonshistorikk.

Kontrollen gjelder bare kandidat
`e34b2fae67df6417807109e36eaeadc4c40c89fc` mot base
`59485e6bb6e45dacf348451b380cf6ba3b5d8321` i `work/u1-100895`.
Utført 29. oktober 2026. [Issue #58](https://github.com/depmartin/budsjetthistorikk/issues/58)
ble lest direkte gjennom GitHub-koblingen, inkludert komplett kommentarhenting
(ingen kommentarer). Kontrakten, AGENTS, arbeidsflyten, issue-tracker,
begrepsreglene og GLOSSARY er lest. Denne rapporten og kontrollfilene er
etterfølgende reviewartefakter utenfor den faste kandidatens tre.

## Uavhengighet og utført kontroll

Jeg har lest hovedinnholdet i alle fire bevarte HTML-kapitlene til Prop. 21,
hele Innst. 87, hele sak 5s korte debatt, hele sak 5s voteringsblokk,
forslags- og voteringsvedtaksresponsene og alle fire komplette endelige
vedtaksobjekter. Saksresponsene for 100895/100932/100933 og K3-indeksens
ordinal 616 er kontrollert særskilt. C05s komplette Prop. 34-kapittel 3,
den nødvendige lokale motpostomtalen i Prop. 16 og den gjenbrukte
lønnskonteksten i Prop. 36 er lest fra de bevarte originalene.

[Det selvstendige kontrollskriptet](independent_check.py) importerer eller
kjører ikke byggerens verifier. Det finner selv pengepostene ved å gå
gjennom originalenes tabellrader, kapittelkontekst, postnummer, retning,
endringsbeløp og neste før-/etterrad. Først deretter sammenlignes resultatet
med den leverte tabellkontrollen. Alle 163 leverte belegg er dessuten
kontrollert mot kildehash, navnerom, eksakt XPath, eventuelt indre HTML-felt
og avledet tekst. Den faglige vurderingen nedenfor bygger også på manuell
lesing av originaltekstene, ikke bare maskinelle treff.

| Kontroll | Selvstendig resultat |
| --- | --- |
| Fast kandidat/base og arbeidsflate | Riktige commit-ID-er; base er merge-base; ingen endring i kandidatens sporede filer. |
| Nye transporter | 15 metadataobjekter, 14 komplette 200-responser og én bevart DNS-feil uten oppdiktede responsbyte. Alle metadata-, arkiv- og kildehasher/byteantall består; innbyrdes metadata samsvarer med manifestet. |
| Representasjoner og konvolutter | 6 XML-responser parser komplett, 7 HTML-responser har avsluttende HTML-konvolutt, PDF har filstart/EOF. Content-Length kontrolleres der headeren finnes (9 responser). |
| Tid og kontrakt | Alle 15 forsøk starter etter issuepublisering 13:45:35 UTC; start/slutt har riktig rekkefølge. Første forsøk 13:47:47 UTC. |
| Gjenbruk | Alle 16 filer har riktige hasher og byteantall og er identiske med baseblobben; de 7 gzip-originalenes innholdshasher består. Ingen ny observasjonsdato er tillagt dem. |
| Lokatorer | Alle 163 belegg har unik lokator og eksakt gjengitt avledet tekst. |
| Hele pengetabellen | 32 selvstendig funne trioer i Prop. 21; 21 til hovedsaken og 11 til søstersakene. Alle 116 radforekomster i fem representasjoner består før + endring = etter. De fire hovedsakrepresentasjonene samsvarer med de 21 relevante regjeringsforslagene. |
| Endelige originalobjekter | Samtlige 226–229 er C14N-like i de to eldre, separat hashfestede sesjonsoriginalene. Alle fire komplette objekters hasher og byteantall samsvarer med source-comparison.json. Ulike rårepresentasjoner skjules ikke. |
| Journaler | 13 ledgerfunn og 12 kryssreferanser er lest; samtlige beleggreferanser finnes. Den faglige begrunnelsen er vurdert nedenfor. |
| Beskyttet grunnlag | 627 Git-blobber er uendret mellom base og kandidat; 464 checkout-filer består eksakt bytekontroll og 163 tekstfiler består deklarert LF-kontroll. |

[results.json](results.json) inneholder **2 908 beståtte selvstendige
assertasjoner**, sist kjørt `2026-10-29T14:26:24.908121+00:00`.
Byggerens offlinekommando ble også reprodusert separat fra den faglige
vurderingen: [builder-reproduction.json](builder-reproduction.json) har
**2 874 kontroller og 0 feil**, inkludert leveransemanifestets 51 filer.
Det selvstendige skriptet består Ruff check og Ruff format --check.

## Faglig kontroll av behandlingskjeden

K3s `/s:saker_oversikt/s:saker_liste/s:sak[616]` binder sesjon 2024–2025
til 100895 og innstilling-ID 16627. Den nye saksresponsen og Innst. 87s
innledning bekrefter Prop. 21 → Innst. 87 og unntakene 1541, 1542, 1543,
1565, 4565, 5579 og 5607. 100932 gjelder 1541/1542/1543/5579 → Innst. 88;
100933 gjelder 1565/4565/5607 → Innst. 99. De 11 søstertrioene er bevart
i den komplette proposisjonstabellen og tilskrives ikke vedtak 226.
Søstrenes videre behandling er uttrykkelig utenfor undersøkelsen.

Innst. 87 `#m2` og `#m3` uttrykker samlet komités støtte og tilråding.
Debatten 17. desember har presidentens opplysning kl. 13:40:13 om at ingen
har bedt om ordet. Den komplette voteringsblokken viser I–IV og samrøystes
vedtak. APIet har én votering, 23886, kl. 19:29:01.44, og fire tilrådinger:

| Romertall | Forslag | Vedtak/API-ID | Kontrollert rolle og år |
| --- | --- | --- | --- |
| I | 40077034 | 226 / 40034094 | 21 bevilgningsendringer på navngitte andre konti i 2024. |
| II | 40077035 | 227 / 40034095 | Forpliktelsesfullmakt for byggetrinn 2 del I fra 2025 og senere år; kostnadsramme 8 531 mill. kroner i prisnivå 1. juli 2025. |
| III | 40077036 | 228 / 40034096 | Tilsvarende fullmakt for brukerutstyr, ramme 627 mill. kroner. |
| IV | 40077037 | 229 / 40034097 | DFD kan i 2024 føye «kan overførast» til 1560/71. Ikke en beløpsendring eller generell FIN-fullmakt. |

Voteringsvedtaksresponsen binder romertallene til vedtaksnumrene; de
komplette sesjonsobjektene binder nummer, API-ID, dato og sak. Dette er
separate bevisledd. APIets −1-stemmetall beholdes som rå sentineler og
omtolkes ikke til faktiske antall. Det er forsvarlig å rapportere at ingen
ytterligere fremsatt/endret forslag er funnet i dette komplette lokale
behandlingsgrunnlaget. Kandidaten hevder ikke absolutt forslags- eller
versjonsfullstendighet utenfor grunnlaget.

De små språklige forskjellene mellom regjeringens og Stortingets fullmakter
er bevart. Tabellkontrollen gjelder konto-/beløpstrioer, ikke identiske
dokumentbyte. Innst. 87s innledende «kap. 510» er en bevart kildetekst;
selve pengetabellen og de etterfølgende representasjonene har 1510.

## Postgrense og nødvendige indirekte henvisninger

C05 er fulgt fra hele Prop. 34 kapittel 3 til Prop. 21s OU-avsnitt,
forslag IV, Innst. 87 IV, 40077037, votering 23886 og endelig 229.
1560/71 gjelder opplæring og utvikling av tillitsvalgte og mulig senere
utbetaling til hovedsammenslutningene i 2025 etter tariffoppgjørstvistene.
Fullmakten har dette konkrete post-/formålsomfanget. Den fordeler ikke
Riksantikvarens lønnskompensasjon. Prop. 34s separate +14,2 mill.-forslag
på samme post adopteres ikke som en ny beløpshendelse fra 100895.
1560/72s +7 mill. til pensjonskostnader og 1551/1s eget stikkord i tabellen
er korrekt holdt fra C05 og 229. Faktisk overføring, OU-utbetaling og
eventuell virksomhetsvirkning hos Riksantikvaren er fortsatt uavklart.

Den konkrete kulturminnerelaterte kandidaten 1533/45 er undersøkt:
Prop. 21 navngir Statsbygg som utfører, KLD som oppdragsgiver og
1400/21 som motpost til +10,8 mill. til rassikring på Øvre Storwartz.
Prop. 16 `#kap2-p2`, sammenholdt med kapittel- og postoverskriften,
bekrefter denne lokale relasjonen. Postens samlede −8,8 mill. inneholder
også +2 mill. fra 1400/76. Det foreligger derfor en konkret annen
postrelasjon; KLD, Røros og kulturminneformål etablerer ikke en 1429/1-
eller /22-kobling. Kandidaten påstår ingen ny full kontroll av Prop. 16s
behandling eller faktisk ressursbruk.

Innst. 87s generelle Prop. 36-henvisning er kontrollert mot det gjenbrukte
kapittel 5 og vedlegg 4s lokale 1429-blokk. 2 796 000 kroner på 1429/1
er det allerede kjente selvstendige kompensasjonsanslaget. Det er ikke
en ny C05-verdi eller en /22-fordeling. Undersøkelsen trenger ikke
gjenåpne 101000 eller faktisk bruk av 231/429 for denne konklusjonen.

De øvrige postomtalene er lest med konkrete mottakere/formål/motposter:
DFDs og etatenes drift, interne husleie- og brukerbetalingsoverføringer,
Statsforvalterne/Husbanken, byggeprosjekter, KORO, kongelige eiendommer,
Statsbyggs utstyr/renter/vedlikehold og personvern. Ingen gir dokumentert
ny 1429-postkobling i det valgte grunnlaget. Kryssreferansejournalens
J05–J12 beholder faktiske tjeneste-/prosjekt-/avtalevirkninger og eksterne
bakgrunnskilder som avgrenset rest. Dette støtter formuleringen
«ingen ny dokumentert»; det støtter ikke en generell nullvirkning.

## Reproduksjon og bevisgrense

Fra repoets rot:

```powershell
$u1Python = 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONPATH = (Resolve-Path '../p1-perioderegister/.local/python').Path
& $u1Python docs/research/u1-100895-58/reviews/source-control/independent_check.py
& $u1Python docs/research/u1-100895-58/verify.py
```

Skriptene skriver til standard output. Ingen primærkilde ble hentet på
nytt i denne kontrollen; attestasjonen gjelder de frosne, hashbundne
observasjonene og bevarte transportmetadataene. PDF er kun kontrollert for
filkonvolutt, ikke tekst eller layout. Den faglige kontrollen bruker de
komplette HTML-/XML-originalene. Ingen produktkode, historisk pinning,
B5, beløpsadopsjon, fem/elleve, helårsdekning eller faglig årsbalanse er
endret eller godkjent av denne rapporten. Standards/Spec, sikkerhetsaudit,
full Linux-CI, publiserte Git-blobber og merge er egne etterfølgende porter.

| Kontrollartefakt | SHA-256 |
| --- | --- |
| independent_check.py | `ca73e5f08dab4508d6ceb061f533f7cc7cdb4528b500eda55075db8b8039c0d4` |
| results.json | `9fead42126be27f5e802adb20e176037eeae67bc1db840fb76780300c8507db2` |
| builder-reproduction.json | `b585873d3ec8d670a8ebe7f92846507897e98d40201ff6f8ae254d04a1251e05` |
