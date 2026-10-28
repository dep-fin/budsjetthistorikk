# T4: tidsmargin før samlet review

Orkestratoren setter jobbgrensen til **60 minutter** før fast kandidat og
uavhengige porter. T4s lokale fullsuite bestod med 1155 tester og to eksisterende
Windows-rettighetsskips på 2903,14 sekunder (48 minutter 23,14 sekunder).
Ops-prøven kjørte delvis samtidig; dette er derfor ingen isolert ytelsesmåling
eller målt Linux-tid. Den gamle 40-minuttersgrensen gir likevel utilstrekkelig
margin mot den faktisk observerte varigheten. 60 minutter gir omtrent 12
minutters margin for oppsett og variasjon mot denne konservative referansen.

Hele fullsuiten, Ruff, formattering, mypy og parserversjonslogging beholdes.
Ingen tester fjernes/skippes, aksept reduseres eller strenge filvern lempes.
Faktisk grønn full Linux-CI på publisert kandidat er fortsatt obligatorisk.
Eldre hashfestede byggejournaler og overleveringen bevares som opprinnelige
målinger med daværende 40-minuttersramme; dette tillegget angir gjeldende valg.
