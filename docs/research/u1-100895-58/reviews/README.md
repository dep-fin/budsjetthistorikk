# Uavhengige porter for U1 / #58

Alle fire porter vurderer forskningskandidat
`e34b2fae67df6417807109e36eaeadc4c40c89fc` mot
`59485e6bb6e45dacf348451b380cf6ba3b5d8321`.
Rapportene er etterfølgende bevis; kandidatens forskningsfiler er uendret.

| Port | Resultat og bevis |
| --- | --- |
| [Uavhengig kildekontroll](source-control/REPORT.md) | Ingen P0–P3-funn; 2 908 selvstendige kontroller og separat reproduksjon av 2 874 byggerkontroller. |
| [Standards](standards/REPORT.md) | Ingen dokumenterte standardbrudd eller begrunnede kode-luktfunn; statikk og 2 874 offlinekontroller består. |
| [Spec](spec/REPORT.md) | Ingen nødvendige eller valgfrie funn; 1 765 selvstendige kontroller består. |
| [Separat sikkerhetsaudit](security/README.md) | Ingen sperrende funn; 775 sikkerhetskontroller og 2 874 offlinekontroller består. S1 er en lav/P3-observasjon om omdirigering ved senere bruk av hentehjelperen. |

S1 beholdes som uttrykkelig begrensning: de faktiske kildehentingene har
avtalte forespurte og endelige HTTPS-verter. Undersøkelsen krever ingen
ytterligere henting. Eventuell senere gjenbruk må vurdere vertsgrensen
på nytt; denne leveransen påstår ingen generell sikker innhentingstjeneste.

Reviewhjelpernes formatering kontrolleres separat før publisering.
Forskningskandidaten og dens kilde-/leveransemanifest endres ikke av dette.
Publisert tre, full CI og bekreftet merge er egne porter. Faktisk sluttstatus
og overlevering registreres i [#58](https://github.com/depmartin/budsjetthistorikk/issues/58)
og PR-en. Ingen historisk «gjenstår»-tekst omskrives til mergebevis.
