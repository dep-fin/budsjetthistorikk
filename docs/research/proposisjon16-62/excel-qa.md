# Faktisk visuell Excel-QA

Produkteksporten bruker det uttrykkelig bestilte eksisterende openpyxl-laget.
Regnearkskillen, stilguiden og hele API-hurtigstarten er lest for separat QA.
Loader-bundlet Node og `@oai/artifact-tool` importerte de **faktisk skrevne
XLSX-filene**, og rendret dem; ingen alternativ håndlaget regnearkmodell ble
brukt som visuell fasit. Produktruntime og avhengigheter ble ikke endret.

## Utført

Alle 15 ark ble rendret og bildene inspisert. Etter visningsretting ble
17 områder i sluttens `inntekt-null.xlsx` rendret: alle ark samt separate
inventar-overlay-/fullmaktsvalg-områder. Representativ utgift, tekstkonto og
tomt utvalg ble også rendret fra sine egne sluttfiler (Forløp og Utvalg).
PNG-er under `visual/` er faktiske import-/renderutdata fra filene med hasher
i `source-control.json`. Lokale øvrige inspeksjoner og renderlogger er bevart
i `.local/visual-final-*`.

| Prøve | Faktisk område / observasjon |
| --- | --- |
| Utgift 1400/1 | Forløp B1:K5: 322816000 / 5937000 / 328753000 og forslagsrolle. |
| Inntekt/null 4400/2 | Forløp B1:K5: 518000 / -518000 / synlig 0. Ingen tom celle eller ####. |
| Tekstkonto 1420/66 | Utvalg A1:B12: eksplisitt valgt konto, 0/0/0 valgt, 123/6/2 globalt. Tomt Forløp er forventet. Fullmaktsvalget er i tillegg kontrollert i faktisk fil. |
| Delt ramme | Fullmakter A1:F10: IV er én rad med 1420/39,/69,/79 og 16300000. V og VI er adskilte punkter. |
| Grenstatus | Grenbevis A1:G9: 1429/81 og øvrige tabellkontoer/95 adskilt, V.1–2/V.3 ulike lokale romertall, synlig ikke_strukturert_T6. |
| Tomt valg | Utvalg A1:B12: tom kontounion og 0/0/0 valgt, 123/6/2 globalt; tomt Forløp. |
| Historisk/gjeldende | Kontoer A1:H6 og Inventar B1:H6/L1:N6: historisk T1-status er merket; aktiv T5-status står separat. |

Rendringen avdekket at historisk inventarstatus trengte eksplisitt etikett
ved siden av gjeldende T5-status. Bare den nye Excel-modulen ble rettet.
Den avdekket også unødvendig høye nye fullmakts-/grenrader; de ble gjort
mer kompakte, mens 35-kontolisten beholder nødvendig høyde. Nye headerceller
har samme stil som de etablerte tabellene. Rettingene er faktisk rendret på
nytt og de berørte bildene inspisert.

## Forsøk og bevisgrenser

Første forsøk på lokal node_modules-junction fikk «Access is denied».
Direkte navneimport ga deretter `ERR_MODULE_NOT_FOUND`. Standard Node-
moduloppløsning mot loaderpakken løste dette; en Windows-sti måtte først
gjøres til file-URL etter `ERR_UNSUPPORTED_ESM_URL_SCHEME`. Selve import- og
render-API-ene var tilgjengelige og virket. Ingen ny installasjon, endring
av runtime eller omgåelse av et autorisasjonsavslag var nødvendig.

Primære verdier, null, kontoomfang, telleenheter og statusoverskrifter er
visuelt lest. Lange ID-er, råtekst og kapsel-JSON vises som avgrensede
celleforhåndsvisninger; hele teksten finnes i cellene/ordnede tekststykker
og kontrolleres tapsfritt av leseren. Disse store kontrollfeltene påstås ikke
fullt lesbare samtidig i en PNG. Slike forhåndsvisninger er en dokumentert
visningsgrense, ikke tapt data eller skjult databaseavhengighet.

Rendererens tusenskille er engelsk. Den faktiske filen bruker invariant
`#,##0`; native norsk Excel/lokalisering, interaktiv klikking og utskrift er
ikke prøvd. Visuell QA gjelder de faktisk inspiserte importerte områdene,
ikke native Excel-aksept eller en påstand om at hver fulltekstcelle er vist
uten klipping.
