# Byggeroverlevering: C06 / #60

Lokal kunnskapskandidat for [#60](https://github.com/depmartin/budsjetthistorikk/issues/60),
base `49cc6e44851cf74e0aaea4eb333419e5598bfd95`, gren `codex/c06-99235`.
Byggeren har ikke staged, committet eller mutert GitHub. Denne statusen
er ikke en påstand om uavhengig godkjenning, full CI, PR eller merge.

## Levert lokalt

- [Kontrakt](contract.md), [rapport](README.md), [lesejournal](reading-journal.md),
  [behandlingsledger](treatment-ledger.json),
  [kryssreferanser](cross-reference-journal.json),
  [C06-oppfølging](candidate-followup.json) og administrativ
  [oppdelings-/ryddingsvurdering](issue-assessment.md).
- Komplette nødvendige hovedoriginaler, egne vedlegg i full PDF på 144 sider,
  16 nye transportforsøk med 15 komplette sluttsvar, alle redirectentity-byte,
  én DNS-feil uten svar, 18 gjenbruksfiler og 87 belegg. 130 egne vedleggsbilder
  har inventar/OCR/sidejournal; 18 nøkkelsider er visuelt lest.
- [Reproduksjon](reproduksjon.md), [bevaringsmanifest](preserved-files.json),
  [leveransemanifest](delivery-manifest.json),
  [offlinekontroll](verification.json) og [lokale kontroller](local-checks.json).

## Faglig resultat

Debatten var 20. juni; 23490 vedtok I–IV enstemmig 21. juni 2024 kl 14:11:27.147.
Saksgang, komplett debatt-/voteringsreferat, API og fire endelige vedtak
støtter denne prosessavklaringen. Senere 20. juni-utsagn i Prop. 34/Innst. 91
er bevart; hvorfor de bruker denne datoen er uavklart. Ingen original rettes.

853 er nemndshjemmel; 854 nemndsbasert lønnssamtykke; 855 betinget LO/YS-
møteboksamtykke; 856 alternativt betinget nemndssamtykke. Høstbevilgningene
skal fremmes senere ifølge Prop. 108. Ingen ny postvis 1429-bevilgning er
belagt. Riksantikvaren står uttrykkelig i begge egne forhandlingsstedslister;
det er positiv institusjonsrelevans med uavklart personell-/postanvendelse.
Stillingskode 1429 Aspirant 357 000 er konkret annen tallbetydning. /22 arver
ingen /1-forklaring; det gamle /1-kompensasjonsanslaget beholder sin rolle.

Lesedybden i 130 bildesider er uttrykkelig avgrenset: alle er råbevart,
OCR-behandlet og seksjonsinventert; 18 sider er visuelt lest. Feilfri OCR,
full manuell celletranskripsjon og generell tariff-/retts-/personellaksept
påstås ikke. Ved uavhengig kildekontroll bør bildene på side 69/135,
50/116 og 13/79 prioriteres for de konkrete nye observasjonene.

## Neste nødvendige porter for akkurat denne ticketen

Orkestratoren lager fast kandidat og sørger for uavhengig kildekontroll,
samlet Standards/Spec og separat sikkerhetsaudit på samme kandidat.
Nødvendige funn rettes og kontrolleres. Deretter én PR, faktisk Git-blob-
kontroll, hele uendrede Linux-CI med 90 minutter, eventuell nødvendig
CI-retting, autorisert merge, ancestry og GitHub-sluttoverlevering.
Ingen av disse portene kan utledes bare fra byggerens lokale resultat.

Lokalt består ni offline transportprøver, tre eksisterende kompatibilitets-
tester med faktisk P2-JSON-/Excel-gjenlesing, Ruff/format på 158 filer og
konfigurert mypy på 81 kildefiler. Alle 1 226 eksisterende tester ble
samlet inn; full kjøring gjenstår i Linux-CI. Nøyaktige kommandoer,
tidspunkt og utdata ligger i local-checks.json og checks/.

Alle 1 070 beskyttede basefiler er uendret; AGENTS/kildefunn har bare korte
additive pekere. K3/P1/R2/P2/U1, produkt/tester, schema 5/B5 og gamle
formater/ID-er/lesere/standardvalg består. Fem/elleve og historiske 67/66,
60/59,25 og R1–R7 består. 99235 er utenfor den historiske 67-listen.

Ingen gjenåpning av 101000/100895 eller faktisk 231/429 bruk. Ingen annen
kandidat eller neste ticket. #10/#32/#37 står åpne. Bevar andre branches,
arbeidsflater og historiske manifest-/reviewbindinger; lokal hovedcheckout
synkroniseres bare hvis prosjektets bevaringsvilkår er oppfylt.

## Additiv integrasjon etter uavhengige porter

Kildekontroll, Standards/Spec og separat sikkerhetsaudit er fullført på
forskningskandidat `9eb27cebf7ca4a99aeb30fa32245e41314e0d295`.
[Portoversikten](reviews/README.md) lenker de uendrede attestene med
konkrete resultater og grenser. Ingen sperrende funn står åpent der.
Den felles P3/SP1-presiseringen i J02 er rettet fra 14 til 18 nøkkelsider.
Ingen original, sidejournal, faglig konklusjon eller eldre pinnefil er endret.

Bare den nye Standards-helperen fikk formattering/lintretting. Originalbyte
er bevart, og [integrasjonskontrollen](reviews/integration/result.json)
krever identisk AST og identisk fast kontrollutfall utenom tidspunkt.
Ingen opprinnelig reviewer-rapport/resultatfil er overskrevet.
[Nye kontrollutdata](reviews/integration/checks.json) er separate fra
byggerens og reviewernes historiske observasjoner.

Denne integrasjonen er ikke committet av byggeren. Orkestratoren lager
ny kandidat og bestiller målrettet uavhengig etterkontroll av J02,
manifestoppdateringen og reviewbindingen. Én PR, faktisk Git-blob-kontroll,
full uendret Linux-CI/90 minutter, autorisert merge, ancestry og
GitHub-sluttoverlevering gjenstår. Ingen ny fullsuite eller kildehenting
er utført i integrasjonen. Avsnittet om neste porter ovenfor er den
opprinnelige byggeroverleveringen, bevart som historikk.

## Additiv overlevering av transportabel reviewhistorikk

PR #61s publiserte `92b43c2ce7ec350e10639bd0c75540da0d83ee72` og lokale
`9efa1f7b67e4ad5b2722b6a6604591af281e4e9c` har identisk tre, men forskjellig
commithistorikk. [Portabilitetsrapporten](reviews/history/README.md) bevarer
de eksakte tre kandidatcommittene i en 22 554-byte Git bundle og dokumenterer
gjenoppretting i en fersk, isolert GitHub-klon uten gamle Git-objekter.
De fire 9eb-attestene og d241-etterkontrollen er bevart som historiske porter.
Dette tillegget gir ingen ny faglig aksept eller attest på en ny PR-head.
Kommende publisering må beholde bundleforutsetningen 92b tilgjengelig i
Git-historikken; faktisk ny head/blobkontroll, relevant etterkontroll og
full uendret Linux-CI med 90 minutter gjenstår før merge. Ingen kildehenting,
full lokal suite, GitHub-skriving, staging, commit eller merge er gjort i rettingen.
