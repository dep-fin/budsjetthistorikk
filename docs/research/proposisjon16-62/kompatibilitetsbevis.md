# Kompatibilitetsbevis

T5 er nye separate modell-/adapter-/analyse-/Excel-moduler og en egen CLI.
Bare korte additive AGENTS-/kildefunnpekere endres i eksisterende basefiler.
Ingen gamle T1/T2/T3/T4/P1/P2-moduler, gamle fixtures, kildeoriginaler,
K3/P1/R2/P2/U1/C06-filer, schema5/B5, CLI-standarder, avhengigheter eller CI
er endret. Bevaring skal etterkontrolleres mot den publiserte basen på fast
kandidat; byggeren har ikke opprettet noen commit.

Autentisk eldre T1-fixture gjenleses med uendret `analyse.visningspilot`.
T1-rapporten og basisens alle felter beholdes; T5 serialiserer én typet
`t1_basis`. De seks Prop.-feltene, seks Innst.-feltene og seks 210-feltene
er ikke kopiert eller omskrevet utenfor kapselen. Full objektlikhet prøves
gjennom alle faktiske nye filpar. Gamle dokument-ID-er inkluderer fortsatt
`structured_coverage=delvis_1429`, og gamle vedtaksfelt har uendret
`round=uavklart`, revisjon, tolkning, step_id og kontrollstatus.

Fire reelle tilleggstilstander er prøvd: manglende fil, feilet filåpning
(sti er katalog), korrupt HTML og motstridende kontotekst. De gir synlig
mangler/motstrid i T5. I hver tilstand kjører ordinær autentisk 40034229
gjennom synkronisering, råbevaring, tolkning, SQLite, analyse og Excel:
222 observasjoner / 74 hendelser, original-SHA-256
`66208daf51111356ad73c26985819870ab9c2f97ec7b070024d89e150cd772b9`.

Innlesning er prøvd i egen prosess hvor alle analyseimporter er sperret.
Typed PilotInput/PilotBasis og de samme råkildeobjektene gir identisk T5-ID.
Offline JSON/XLSX-gjenlesing er prøvd med både nett og SQLite sperret og
med en kilde-rot som ikke finnes. Både `--t1` og `--frosset` er prøvd via
den nye offentlige CLI-en. Originalfiler og eksisterende output overskrives
ikke; no-clobber-prøven kontrollerer uendrede filhasher etter avvisning.

Hele tidligere testutvalg og 90-minuttersgrensen beholdes. Lokal ny testsuite
og hele Ruff/format/mypy er kontrollert. Full Linux-CI er en separat port
hos orkestrator; ingen lokal fullsuite eller CI-resultat påstås her.
