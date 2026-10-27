# T2/#44: komitéendringen fra original til begge innganger og fil

Lokal leveranse 27. oktober 2026 fra main
`3d7667762ed1eb00223827761831fdf4dbc309d5`, branch `codex/t2-komiteendring`.
Eier har bestilt T2, grønn CI og merge. Denne kontrollrapporten dokumenterer
byggerens lokale resultat; uavhengige reviewporter, GitHub/CI og merge håndteres
av orkestratoren. #10, #32 og #37 står åpne.

[Kontrakten](../../komitepilot.md) ble fastsatt før produktkode. Testgrensen er
original → beløp/omtale → dokumentert relasjon → begge innganger → faktisk skrevet
og gjenlest JSON/Excel. Implement- og TDD-filene ble fulgt ved de avtalte grensene;
de første to vertikale prøvene var røde før adapter/analyse og skriver fantes.
Regnearkskillen er brukt ved eksportkontrollen. Eksisterende openpyxl-teknologi
er videreført i produktets separate filskriver; Artifact Tool rendrer lagret XLSX.

## Avgrenset resultat

| Utvalg i budsjettåret 2024 | Valgte felt | Vedtaksfelt | Monetære hendelser |
| --- | ---: | ---: | ---: |
| Standalone 315/78 | 9 | 3 | 1 |
| Union 315/78 og 1429/1 med valgfri T1 | 18 | 6 | 2 |
| Tomt utvalg | 0 | 0 | 0 |
| Hele Prop.25 / Innst.85 / vedtak208 | 3 hver | 0 / 0 / 3 | 0 / 0 / 1 |
| Vedtak209, plenum eller sak som dokumentinngang | 0 | 0 | 0 |

Regjeringen: før **29 050 000**, endring **119 000 000**, etter **148 050 000**.
Ap/Sp/SV-tilråding og vedtak208: **29 050 000 / 129 000 000 / 158 050 000**.
Avledede før/endring/etter-forskjeller er **0 / +10 000 000 / +10 000 000** fra
forslag til tilråding, deretter **0 / 0 / 0** til vedtak. Det er ikke nye vedtatte
hendelser. H/Vs generelle merknad, Ap/Sp/SVs LNU-begrunnelse, postunntaket,
H/FrP/Vs varslede motstand og Stortingets vedtakelse har forskjellige roller.
Det finnes ingen autentisk tallfestet parallell mindretallstilråding i denne prøven.

Det nye grunnlaget har seks dokumentversjoner, 90 inventarrader (30 postgrupper
hver i Prop.25s forslag, Innst.85s I og vedtak208), ni beløpsobservasjoner og egne
kontekster/bevisrelasjoner. Bare 315/78 er strukturert. Hele inventaret, relevante
HTML-seksjoner, logisk hierarki, full PDF-tekst og fullmakt II finnes også ved tomt
beløpsvalg. Dokumentvalg, kapittel-/parunion, flere år uten kontinuitetsantakelse,
begge navigasjonsretninger og retur bruker samme grunnlag/ID-er. En manglende
tilrådingsadapter gir reelle hull; bevart PDF/omtale fyller ikke inn beløpet.

## Kildebevis og korrekt 208/209-skille

[Kildeundersøkelsen](../to-visninger-37/komiteendring.md),
[manifestet](../to-visninger-37/originals/komite/manifest.json) og
[passasjene](../to-visninger-37/originals/komite/passages.json) er bevart.
Alle åtte faktiske komitéresponskropper hashkontrolleres; fire DNS-feil uten byte
beholdes i transportmanifestet. Valgt beløpsrepresentasjon er den vellykkede
`vedtak40034045-sak100887.html`, SHA `232e06bc…102c1ab`. Den bevarte
HTTP500-siden `vedtak40034045.html` er et synlig avvik, ikke vedtaksbevis.

Prop.25 ch4 tabellrad 13–14 gir regjeringens trio. Innst.85 #m2_2_1 og unntaket
under #m3 binder Ap/Sp/SV; tilråding I rad 14–15 gir flertallets trio. #m2_1s
generelle støtte og H/V-merknad gis egne roller. Felles plenumsoriginal
`22170a60…85fb2e5`, sak24, binder særskilt I315/78 til 63–35 kl.19.49.48 og
H/FrP/V-motstand. Resten av I og II har en annen votering. Denne enstemmigheten
og fullmakten arver ingen beløps-/postkobling til 315/78.

208/40034045 og **209/40034047** er begge i sak100887. 208 har bare I-tabellen;
209 har II/Narvik. T2 rekonstruerer egne kontrollrepresentasjoner fra den bevarte
fullsesjonsresponsen med SHA
`c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42`,
7 479 943 byte. Konvolutten er eksakt prefix `[0:321]` + objekt + suffix `[-57:]`:

| API-ID | Objektets byteintervall, 0-basert/eksklusiv slutt | Objekt SHA-256 | Konvolutt SHA-256 |
| --- | --- | --- | --- |
| 40034045 / 208 | [1191752:1248367], 56 615 byte | 5f399fc5c9603ea2be74659b40307d31aa7a4b2ce1fa17d053166043f6d33df1 | 9cc1a9b2406f78cfd3e9ec0c0e57b1145813a53c0a2f409d71d6f6069049b8a1 |
| 40034047 / 209 | [1248373:1249810], 1 437 byte | 12850ccf53c91c197562c12e0bdf56f2438621d55aabb0cd47b1eca4711868e4 | b0294d5e20b8ef0d5bd83d33efe0fdd700f831701111261935205824423aa84d |

Disse utdragene lagres som oppskrift/referanse, ikke en ekstra råkopi eller ny
HTTP-respons. Gammel 210/368s 9cfe-forelder og gamle sidevogner er uendret.

## Faktisk kildegjenbruk og ny faneprofil

[Faneanalysen #43](../faner-og-kildedeling/README.md) følger kandidaten uendret.
Standalone har 12 kanoniske payloads med 12 faktiske råhasher, 12 råkilde- og to
avledede kildeobjekter. De ni beløpsobjektene forekommer én gang hver i den
serialiserte JSON-pakken og den faktisk gjenleste Excel-kapselen. Dokument,
inventar, relasjon, sammenligning og utvalg bruker ID-referanser.

Unionen har fortsatt bare ni **nye** serialiserte beløpsobjekter. Felles plenum,
fullsesjons-gzip og dens metadata peker til råbyte som allerede ligger i den ene
uendrede T1-kapselen. Bare ni nye payloads lagrer base64; de tre andre nye
registerpostene er referanser. Inne i den gamle kapselen finnes fortsatt
36 serialiserte observasjonsobjekter/18 unike og 23 råpayloadforekomster/21 hasher.
Dette arvede forholdet oppgis separat. Like beløp slås aldri sammen på tvers av
kilder eller representasjoner. Ingen generell normalisering av legacyformatet
eller gammel faneopprydding er utført.

Den nye Excelprofilen har Forløp, Dokumenter (dokumentoversikt og hele inventaret),
Omtale, Sammenligninger og Dekning og avvik. Forløp grupperer kildefeltenes trio
per ledd. Sammenligninger viser begge dokumentnavn, innbeløp, avledet forskjell og
lenker til de eksakte feltene. Kontroll og Offlinegrunnlag er tilgjengelige
kontrollområder. Det finnes ingen ekstra base64-Originaler-fane. Fulltekst, HTML,
hierarki og lange kontrollfelt åpnes i cellen eller gjenfinnes med `--originaler`;
Excel er ikke en trykksatt PDF. Råregisteret finnes én gang i hver selvforsynte
pakke; samme grunnlag i to eksportformater er ingen ny kildeinnhenting.

## Reproduksjon og videreføring

Se [overleveringen](OVERLEVERING.md) for kommandoer, API, kompatibilitet,
uavhengighetsprøver og begrensninger. [Kontrolljournalen](verification.json)
bevarer manifest, faktiske SHA/byte/ID-er, forventet/observert aksept,
objektforekomster og kontrollresultat. Syntetiske feil er uttrykkelig merket.
Den fullførte fullsuitens [faktiske logg](checks/t2-full-final.log) er bevart
med 1 069 beståtte og to dokumenterte vertsrettighetsskips. Etter byggeravbruddet
ble kode-/artefakthashene, 159 manifestfiler og de lagrede standalone-/union-/tomt-
parene kontrollert på nytt. [Gjenopptakskontrollen](resumption.json) skiller
den tidligere fullsuiten fra testoppstartsrettingen og den avsluttende nye
[fullsuiten](checks/t2-resume-full.log): **1 069 beståtte, to eksisterende
vertsrettighetsskips, 1 283,40 sekunder**. Ruff check/format (110 filer) og mypy
(62 kildefiler) bestod. Alle 23 autentiske gamle kompatibilitetsfiler har
fortsatt sine opprinnelige hasher. Produktkode og leveranseartefakter er uendret
fra den gjenfunne kandidaten; bare adapterskriptets testoppstart ble rettet.
Et [autentisk uendret T1-testarkiv](../../../tests/fixtures/t2/README.md) gjør unionen
reproduserbar fra GitHub uten gamle lokale outputs. Standalone bruker bare
repoets originale T2-kilder og har ingen T1-/O2b-/Excel-/databasekrav.

Ingen faglig godkjenning, helårsdekning, kontinuitet eller drift følger.
T3–T6/K1–K3 og #43s generelle oppfølginger har ikke byggemandat her.
