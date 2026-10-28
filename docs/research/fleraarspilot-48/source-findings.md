# T4: kildebevis for separate 2024- og 2025-forløp

Kontrollert 28. oktober 2026 under #48 fra main
`e374bdcad3bf18c44ccd7b813ce67b8f97327ee2`. Kontrakten ble fastsatt før kode
i `fc2b629`, [fleraarspilot.md](../../fleraarspilot.md). Dette er gjenlesing av
bevarte originalbyte; ingen ny HTTP-henting er utført.

201/40034038, sak 100184, 16.12.2024, sesjon 2024–2025, sier uttrykkelig
«På statsbudsjettet for 2025 bevilges under:». Dato/sesjon blir ikke budsjettår.
Kapittel 1429 står i tabellrad 100. Post 1, rad 101/kolonne 4, har observert
nivå 163 173 000 kroner. Post 22, rad 103/kolonne 4, har 33 408 000 kroner,
med råformålet «Flerårige prosjekt kulturmiljøforvaltning, kan overføres».
Hele tabellen har 153 inventarrader. Bare disse to beløpsfeltene struktureres;
øvrige rader forblir tilgjengelige med ustrukturert status.

Den bevarte komprimerte fullresponsen
`../to-visninger-37/originals/aar/session-2024-2025.xml.gz` har SHA-256
`1ea276a5730a5196f4def7471e0bf6ae51a7878a4eac86922cc87a9a71200a6b`.
Dekomprimert: 7 479 943 byte, SHA-256
`c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42`.
Transportmetadata har SHA-256
`4ccc151e0ddd84c11b9c5e973c67762a6470a7bb5f2cd59a542d2847e6c5cd28`.
Byteoppskriften er `parent[:317]+parent[5662496:5779401]+LF+parent[7479888:]`.
Resultatet er byteidentisk med det bevarte komplette 201-utdraget:
117 278 byte, SHA-256
`bd2d50e044e7bbfe1284a8b0dffb5a42ed12412e5b462c61c72614c2d000ee50`.
Oppskriften er en avledning, ikke et nytt HTTP-svar. Metadata viser den
tidligere hentingen 22.10.2026 07:04:03.260568 UTC og den offisielle API-URL-en.

Ved komplett input peker de to nye payloadregistrene til de eksisterende
T1-kildene `8df02a830c028bc0162f87f2504dabc7f3b4b7000144c33afeae0deafe258af4`
og `b73e5076694be94783f9fc34fc8045f5f547578b3247440ca7ac88e7dac3276c`.
Ingen ekstra base64kopi av c5f3, metadata eller ferdig 201-utdrag legges til.
Forskningsmanifestet og T3s fem nye 341-/857-felt gjenbrukes. Alle tilhørende
T3-objektfelt og ID-er består etter de opprinnelige rekonstruksjonsreglene.
T1s 18 observasjoner serialiseres bare i én ordrett kapsel; den gamle kapselen
har egne arvede immutable kopier, som telles separat i kontrollmanifestet.

210 og 201 har samme dato, men gjelder henholdsvis 2024 og 2025. Ingen
behandlingsrelasjon mellom årene er etablert. Like kapittel-/postnumre eller
navn er ingen kildeavgjørelse om kontinuitet eller uendret oppgaveomfang.
Begge kontoene har derfor globalt, navngitt kontinuitetsbrudd/ukjent omfang,
også når filteret gir null treff. 2025s originale forslag/tillegg,
Innst.14/postvis vedtakelse, senere RNB/nysaldering/øvrige endringer,
vedtak uten proposisjon, periodeinventar og årsavstemming har egne hull.
2024s verifiserte ledd fyller ingen av disse hullene. 1149s andre poster gir
ingen helårsfraværspåstand på /1 eller /22.

Praktisk konsekvens: velg opt-in T4 for separat flerårsfiltrering. Positiv
kontinuitet, full årsdekning, faglig årsbalanse og drift er egne porter.
T3s 66aa-avledning og gammel 857/554e-kontroll er fortsatt forskjellige
representasjoner. Gammel 554e-fullrespons er ikke funnet eller ommerket.
