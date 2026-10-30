# T5-review: historiske porter og avventet ny kandidat

Kilde-/feltport, Standards, Spec og sikkerhetsaudit her gjelder historisk
kandidat `d46589cb9e99338e44fc805ee9882006ba657fd0`, tre
`df0eed6d6e8a0b2a07962e641ae05d1194a3304d`, mot base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b`.
Kilde/Spec hadde null funn; Standards hadde null regelbrudd og én valgfri P3.
[Sikkerhetsauditen](security/rapport.md) var ikke bestått: ett P2-temafunn.

[Den lokale P2-rettingen](../security-fix/README.md) binder hele temadelen.
Dens tre regresjonsvarianter og 38 T5-tester er dokumentert separat.
Denne rettingen ligger i arbeidsflaten og inngår ikke i d465-kandidaten.
Ny uavhengig audit av en ny fast kandidat er fortsatt avventet.

[Kontrollintegrasjonen](integration/README.md) gjør fire nye reviewhjelpere
Ruff-/formatklare. Eksakte originalbyte ligger ved siden av hver hjelper
med `.original`-suffiks; [hash-/pathkartet](integration/original-helper-map.json)
knytter historiske manifeststier til disse. Opprinnelige rapporter, resultater
og hele security-fix-pakken er uendret. Historiske security-fix-bindinger
beskriver tilstanden før denne integrasjonen.

Orkestrator fryser neste kandidat og bestiller relevante nye uavhengige porter
før publisering. Historiske godkjenninger eller helper-replay er ingen ny
sikkerhetsgodkjenning, full Linux-CI eller merge.
