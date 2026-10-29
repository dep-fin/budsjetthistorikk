# Reproduksjon fra publisert historie

Bruk Python 3.12 og pinnede `requirements-dev.txt`. Kjør fra kandidatens
repositoryrot. Hjelperen bruker kildene og den autentiske gamle T1-fixturen
i klonen. Den trenger ingen lokal database, nett eller tidligere arbeidsflate.
Bruk nye outputnavn; eksportene er no-clobber.

```powershell
python -m ops.proposisjon16_proeve --root . --output .local/t5-proeve --base BASE --candidate KANDIDAT
python -m pytest tests/test_proposisjon16.py -q --basetemp .local/t5-test
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

`BASE` er den publiserte base-referansen som kandidaten sammenlignes med.
`KANDIDAT` er kandidatens tilgjengelige publiserte referanse. Begge er valgfrie;
de binder rapporten når gitt, og er ikke hardkodede lokale commits.
Ved kandidatbinding kreves at sporede arbeidsfiler samsvarer med kandidaten.
Første levering bruker basen `2f4ee30c9d8074076fc8042e208c4a4b6345db6b`.
Kildesjekken mot base tillater bare de to korte kontekstpekerne som endrede
basefiler. Nye moduler/dokumenter er egne additive filer; basekontrollen
avgrenser til endring/sletting/type-/rename-forhold, slik at publiserte nye
filer ikke feiltolkes som endrede baseblobber i en fersk kandidatklon.

Hjelperen lager 14 faktiske JSON/XLSX-par, tapsfritt originaluttak og
`kontroll.json` med felt-/kilde-/filhasher. Alle par lukkes og gjenleses via
de faktiske leserne. `source_controls` gir separat kontroll av fullmakter og
formelle grenlokatorer direkte fra bevarte originaler, uten produktparseren.

For en T1-JSON som allerede finnes:

```powershell
python -m analyse.proposisjon16 --t1 .local/t1.json --rot . --aar 2024 --konto 4400/2 --json .local/inntekt.json --excel .local/inntekt.xlsx
python -m analyse.proposisjon16 --frosset .local/t5-proeve/hele-prop.json --rot .local/finnes-ikke --dokument prop16 --json .local/offline.json --excel .local/offline.xlsx --originaler .local/originaler
```

Den autentiske T1-fixturen kan pakkes ut med `gzip.decompress` til en ny
`.local/t1.json`; ikke skriv over fixturen. Konto-/årsåpning bruker union av
hele kapitler og eksakte par. Dokumentvalg bruker én eksakt ID eller en kjent
dokumentnøkkel ved førstegangsvalg og kan ikke kombineres med kontofiltre.

Visuell QA bruker loaderens Node og `@oai/artifact-tool` til å importere de
faktiske produkteksportene og rendre avgrensede områder. Ingen alternativ
regnearkmodell bygges. [excel-qa.md](excel-qa.md) angir faktiske områder,
forsøk og grenser. Lokale runtime-stier er bare miljøoppsett; selve
reproduksjonen og kontrollhjelperen krever ingen utilgjengelige SHA-er.

Hele Linux-suiten skal kjøres én gang av orkestrator på publisert slutt-head,
med tidligere CI-utvalg og 90 minutter. Byggeren kjører ikke den lokale
fullsuiten eller egne samlede review-/auditporter.
