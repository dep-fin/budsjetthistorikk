# T6/#64: lokalt kontrollutfall

Hele sluttkjøringen bestod: **1305 passed, 2 skipped** av1307 prøver,
3596.85sekunder (59.95minutter). Alle43 nye T6-prøver bestod.
De to eksisterende hoppene gjelder Windows-vertens symlink-/hardlinkrettigheter.
Ingen tester, konfigurasjon eller CI-grense er lettet. Linux-CI er en egen port.

Ruff bestod,185 filer var ferdig formatert, og mypy bestod for89 kildefiler.
[Maskinelt utfall](checks.json) binder [hele pytest-loggen](checks/pytest-full.log)
og statiske/logger med rå SHA-256. Tre tidligere delkjøringer ble avbrutt mens
kandidaten ble ferdigstilt; ingen av dem er rapportert som en bestått sluttport.
Den siste visuelle rettingen var på disk før T6-importen i sluttkjøringen.

[Akseptbeviset](acceptance.json) binder28 faktisk skrevne, lukkede og gjenleste
JSON/XLSX-par.25 kommer fra sluttkjøringens filfixture; tre ekstra prøver
dekker kryssparvern, bare1429 og hele unionen. Den selvstendige
[reproduksjonsprøven](../../../ops/innstilling95_proeve.py) avstemte216 nye felt
mot uavhengig originalfasit,339/114/38, begge innganger og returer, post32s hull,
ekte inntektsnuller og separate fullmakter. Den autentiske eldre T5-filen er
lest med gammel leser; samme ene T5/T1-basis er bevart i T6.

[Kilde-/filjournalen](source-control.json) binder tre ekstra faktiske CLI-par.
[Originalkontrollen](original-retrieval.json) gjenleste35 rå originaler byteeksakt,
med seks rekonstruerte XML-filer og én indeks:42 filer.
[Excel-QA](excel-qa.md) viser22 inspiserte rendringsområder fra alle16 ark og
tilleggsutvalg. Native Excel og norsk Excel-lokalisering er ikke prøvd.

Fast base er `9616fbe6a8ab15eec696f34de76888565a784f8f`, tre `13caacd265a9a53ba0d077a65e488224d2d1b992`,
branch `codex/t6-innstilling95`. [Lokalt kandidatgrunnlag](local-candidate.json)
binder15 produkt-/kontrakt-/kontrollinnganger med kernel
`07515de3553d22f8fc7795ee265625d76c0caa94336569c777396011d2b0b8fa`. T6-basis er
`3c10e042ad953e3ad9e47e6eee4c41ffe0d4744e36ef126538cb4b109396eccb`. Dette er filgrunnlag, ingen ny commit eller nytt Git-tre.
Av1410 eksisterende sporede filer er bare en kort tilleggshenvisning i AGENTS.md
endret; gamle produktfiler, fixtures, schema5, B5 og CI er uendret.
Byggeren har ikke staget, committet, pushet, opprettet PR eller merget.

Uberiktiget95/rettelsesmelding, faglig årsbalanse, helårsdekning,
kontokontinuitet og all tekst faglig avklart er fortsatt uavklart.
#10/#32/#37 berøres ikke; ingen neste ticket er startet.

Orkestratoren må fryse en konkret Git-kandidat og gjennomføre uavhengig samlet
review, separat sikkerhetsaudit, offentlig fersk-klon-reproduksjon og hele
uendrede Linux-CI-utvalget innen90minutter før godkjent PR/merge.
