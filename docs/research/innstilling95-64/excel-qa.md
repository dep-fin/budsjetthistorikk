# Faktiske T6-filer og avgrenset visuell kontroll

30. oktober 2026. Produktets eksisterende openpyxl-eksport er brukt som
bestilt i #64; ingen alternativ regnearkskriver eller endring av gamle
profiler er innført. Faktisk skrevne, lukkede XLSX-filer er importert og
rendret med loaderens `@oai/artifact-tool`, bundle26.1026.10807.
Native Excel og norsk Excel-lokalisering er ikke prøvd.

## Utført kontroll

De tre CLI-parene `inns95`, `vedtak359` og `null` ligger lokalt i
`.local/reviewable-cli`. [Kilde-/filjournalen](source-control.json) binder
de faktiske JSON/XLSX-bytene, rapport-ID-ene og basis
`3c10e042ad953e3ad9e47e6eee4c41ffe0d4744e36ef126538cb4b109396eccb`.
Første inngang brukte `--t5`; de neste brukte `--frosset` med en fraværende
originalrot. Alle tre par er gjenlest og sammenholdt gjennom begge leserne.

[16 rendringsområder](visual/results.json) dekker alle16 ark i den faktiske
hele95-boken. Hvert område er visuelt inspisert. De
[seks tilleggsområdene](visual-extra/results.json) er også rendret og
inspisert: hele 4400/2-trioen i alle tre stadier, Utvalgs9/3/1 og339/114/38,
separate5+1=6 fullmaktsvedtak, post32s tre hull mot tre nullforskjeller,
alle åtte vedtatte fullmaktspunkter, dokumentlenker/Valgt og359s hovedfelt.

Hovedbeløp, fortegn, datoer, kilde-/talltype, tilrådingsrolle og tellere er
lesbare i de inspiserte områdene. Observert null er synlig som et tall i
Forløp; manglende Prop.-felt er tomme forskjellsceller med uttrykkelig
`hull`/`manglende stadium`. En delt16,3millioners ramme vises én gang per
stadium for de tre kontoene. Regnskapsregelen har egen rad uten beløp.
Nye dokumentlenker går til samme dokumentversjoner som JSON refererer.

Rå IDs kunne i første kontroll flyte visuelt inn i tomme forskjellsceller.
T6s sammenligningsark har derfor egne bredder, tekstbryting og høyder;
den faktiske nye post32-rendringen viser nå de tomme cellene tydelig.
Gamle T1/T5-skrivere er uendret. De øvrige fysiske metadataene er kontrollert
mot forventet bok ved lesing: alle celler/typer, tallformat, lenker,
tema/skrift, dimensjoner, synlighet, flette- og filterområder.

Bevarte PDF-renderinger av trykt side3–5 er inspisert mot tabell/null,
post32 og fullmaktene II–VI. Dette er kontroll av de bevarte
PDF-representasjonene, ingen ny kilderettelse eller ny HTTP-henting.

## Praktiske grenser

Fulltekst/HTML, base64, lange kontolister og enkelte kontroll-ID-er er
celleforhåndsvisninger. Hele verdien ligger i cellen, ordnede tekststykker
og de byteeksakte originalene. Disse kontrollarkene er ingen trykksatt
gjengivelse av fullteksten. Alle rader er kontrollert maskinelt av den
strenge leseren; visuell kontroll er et uttrykkelig utvalg fra hvert ark.
Rendererens tallgruppering er ikke bevis for norsk Excel-lokalisering.

Kontrollen er byggerens fil-/presentasjonsprøve. Orkestratorens uavhengige
samlede review, separate audit, publiserte kandidat, fersk-klon og CI-/
mergeporter er egne kontroller.
