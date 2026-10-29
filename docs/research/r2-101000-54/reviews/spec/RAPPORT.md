# Spec – samlet review og kildeetterkontroll for #54

**Resultat: ingen nødvendige eller valgfrie funn. F1 er lukket.**

Fast base er `6b2441ee5e859d103ab44d78f12d33c374a89171`; kandidaten er
`7af3153bda95726ac93d0780b918ae95440bae2d` (commitene `c61dcc7`, `7af3153`).
Hele `git diff <base>...<kandidat>` er vurdert: 64 filer, inkludert
råarkiver, sidevogner, forskningsdata og kildekontrollens Python-skript.
Alle 64 er bundet til faktiske kandidatblobber; to pekerdokumenter bruker
uttrykkelig LF-representasjon.

Mandatet er [hele #54](https://github.com/depmartin/budsjetthistorikk/issues/54),
med gjeldende #37/#50/#52 og alle kommentarer. Kandidatens kontekst-snapshot
samsvarer med ferske GitHub-lesinger av samtlige fire issue-tekster og
15 kommentarer. AGENTS/arbeidsflyt, P1-kontrakt, K3-restgrenser og O1/O2b
er kontrollert som kravkontekst.

Kravet «sakens komplette proposisjon, innstilling, forslag/endringer,
relevante referat/voteringer og endelige vedtak» er oppfylt for hovedsaken:
fem Prop.34-kapitler og firesiders PDF, komplett Innst.91, hele sak-6-debatten,
voteringsblokken, forslag 40077003/40077004 og 23887→230/231. Ulike
komitéavsendere og APIets −1-sentineler er bevart. Kontrollert tabellomfang
1560/71 og generell lønnsregel gir ingen oppdiktet 1429-hendelse.

Kravene om post/år/rolle/fullmaktsomfang og separat presisjon er oppfylt.
Vedlegg4 har selvstendig råcelle `2 796 000` kroner på 1429/1; den beholder
forslags-/anslagsrollen. O1s avrunding og beregnede rest omklassifiseres ikke.
429-kjeden er dokumentert som overføringsfullmakt til 2025, med faktisk
anvendelse uavklart. Tolv kryssreferanser angir undersøkt delomfang eller
uttrykkelig rest. Ingen positiv M21 eller generell posteksklusjon utledes.

**F1 etterkontroll:** Jeg leste `//*[@id='ved4']/h1` direkte i den hashbundne
originalen. Overskriften «4 Endring av utgifter som følge av lønnsoppgjøret
for statsansatte» står korrekt i rettet README og `FIN-1429-1`. Alle 44
original-/metadatafiler er uendret fra første kandidat.

**Kontroller:** publisert reproduksjon ga 818 beståtte kontroller, inkludert
59 Git-blobkontroller. Kildekontrollskriptet ble kjørt separat på kandidaten:
204 bestått. Egen etterkontroll ga 274 bestått; detaljer og skript ligger her.
Pinnede K3/P1-trær, produkt/test/CI og fem/elleve er uendret.

Forskningsaksepten består. Faktisk 231/429-anvendelse, juni-datokonflikten
og øvrige R1–R7 består som grenser. Dette er ingen ny HTTP-autentisering,
visuell PDF-kontroll, native Excel-prøve eller full produkttestsuite.
Full Linux-CI, GitHub-overlevering og bekreftet merge er senere leveringsporter;
denne rapporten erklærer dem ikke gjennomført.
