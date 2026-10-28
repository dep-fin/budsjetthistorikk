# T4: lokal tidsmåling og uendret CI-ramme

Full Windows-suite 28. oktober 2026: **1155 bestått, to eksisterende
rettighetsskips, 2903,14 s**. JUnit har 1157 cases og 2902,649 s som
testsuite-attributt. De 37 T4-prøvene summerer **1151,989 s** inkludert
fixturetid. Den største prøven, alle års-/kontoutvalg med faktiske filpar
og navigasjon, tok **903,58 s**. Hele testutvalget ble kjørt.

Den separate ops-filprøven tok **1239,219 s** og kjørte delvis samtidig
med fullsuiten. Den produserte alle avtalte utvalg/filpar, negative filer,
fire offentlige 368-forløp og eldre kompatibilitetskopier. Dens varighet er
ikke en ekstra CI-jobb: workflowen kjører pytest, statikk og versjonslogging.
Samtidigheten og Windows-miljøet gjør at den lokale fullsuitetiden ikke er
et isolert Linux-mål. Ingen målt korreksjonsfaktor er fastslått.

[Python-kontroller](../../../.github/workflows/check.yml) er uendret:
**40 minutter**, hele `pytest -vv --durations=20`, Ruff, format, mypy og
lxml/libxml2-versjonslogging. T3s [begrunnede ramme](../forlopspilot-46/ci-budget.md)
er bevart. Ingen test, skipregel, parserregel eller ressurs-/filvern er
redusert for å få et grønt resultat.

**Faktisk grønn full Linux-CI på endelig kandidat gjenstår.** Den lokale
kjøringen overstiger 40 minutter og er ingen garanti for at Linux-jobben
vil rekke rammen. Orkestratoren må vurdere den faktiske kjøringen og rette
eventuelle ytelsesproblemer innen samme utvalg og vern. Dette notatet
endrer ikke timeout og erklærer ikke CI-porten bestått.
