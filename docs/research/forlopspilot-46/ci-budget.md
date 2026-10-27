# T3/#46: CI-tidsmargin før samlet review

27. oktober 2026, fra base `c1cb156d50fb986794e2af8b20a131209e4707a7`.
Jobbgrensen i [Python-kontroller](../../../.github/workflows/check.yml)
økes fra **30 til 40 minutter**. Hele fullsuiten, de statiske kontrollene,
testutvalget, skipreglene og parserversjonslogging er uendret.

## Målegrunnlag

| Kontroll | Faktisk målt tid | Kilde og avgrensning |
| --- | ---: | --- |
| T2 fullsuite, Windows | 1 283,40 s | [Historisk logg](../komitepilot-44/checks/t2-resume-full.log): 1069 bestått, to rettighetsskips. |
| T2 full Linux-CI | 1 599 s | [Kjøring 40528226605](https://github.com/depmartin/budsjetthistorikk/actions/runs/40528226605), start 15:09:47, slutt 15:36:26, inkludert oppsett; tidene er lest av orkestratoren. |
| T3 fullsuite, Windows | 1 512,57 s | [Ny byggersluttlogg](checks/t3-full-final.log): 1118 bestått, to eksisterende Windows-rettighetsskips; alle 46 T3-prøver bestod. |

Den lokale økningen er `1 512,57 − 1 283,40 = 229,17 s`. Lagt til den
historiske Linux-jobben gir dette `1 599 + 229,17 = 1 828,17 s`, altså
30 min 28,17 s før variasjon. Den tidligere 30-minuttersgrensen var
1 800 s. En 40-minuttersgrense gir 2 400 s, med 571,83 s margin over denne
indikasjonen.

Dette er en tidsindikasjon på tvers av plattformer og kandidater, ingen
utført T3-Linux-måling eller garanti om kjøretid. Jobbgrensen gjelder også
oppsett og statiske kontroller; Windows-loggene måler pytest. Faktisk full
grønn Linux-CI på endelig T3-kandidat gjenstår og er fortsatt påkrevd.

## Historikk og kontrollgrense

T2s tidligere [CI-notat](../komitepilot-44/ci-newlines.md) begrunnet økningen
fra 20 til 30 minutter. T3s [utforskergrunnlag](source-findings.md),
[byggeroverlevering](OVERLEVERING.md), [README](README.md) og
`verification.json` beskriver byggetilstanden før denne avgrensede endringen.
De hashfestede rapportene, journalene og leveransefilene bevares uendret.
[Gjeldende T3-kontrakt](../../forlopspilot.md#ci-ramme-før-samlet-review) viser
den nye 40-minuttersrammen og peker til dette tillegget.

Denne endringen kjører ingen produkttester på nytt. Relevant kontroll er
whitespace, YAML-struktur og at workflowdiffen bare endrer timeoutverdien.
