# T6/#64: bygge- og reproduksjonsgrunnlag

30. oktober 2026, fast base `9616fbe6a8ab15eec696f34de76888565a784f8f`,
branch `codex/t6-innstilling95`. Dette er lokal bygging; uavhengig samlet
review/audit, publisert kandidat, CI og merge er orkestratorens porter.

[Før-kode-kontrakten](../../innstilling95.md) fastsetter lukkede felt,
identiteter, kilder, roller og ressursprofil. Den ble skrevet før produktkode.
Alle 216 nye felt og seks rekonstruerte vedtaksobjekter er additive til én
uendret typet T5-kapsel med én uendret T1-kapsel. Gamle produktmoduler,
fixtures, kildeoriginaler, formater, ID-er, schema 5, B5 og standarder er bevart.

## Reproduksjon fra klon

Installer prosjektets uendrede `requirements-dev.txt` og kjør fra repo-roten:

```console
node docs/research/innstilling95-64/independent/oracle.cjs --check
python -m pytest tests/test_innstilling95.py -q --basetemp work/t6-test
python ops/innstilling95_proeve.py --output work/t6-reproduksjon
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pytest -vv --durations=20
```

`work` må finnes før eksplisitt pytest-basetemp brukes. Velg nye outputnavn.
Prøven bruker bare repoets autentiske T1-fixture og bevarte originaler;
ingen utilgjengelig lokal commit, nett, database eller historisk Excel kreves.
Den skriver og gjenleser 28 JSON/XLSX-par og seks byteeksakte XML-utdrag.
Pytest-matrisen har 25 par; reproduksjonsprøven har i tillegg et autentisk
kryssproduktvern (1400/1 +1420/21), bare begge1429 og hele unionen.
`--existing KATALOG` gjenleser allerede skrevne testpar; ingen testfixture
eller eksport påvirkes. `--legacy-t5 FIL` prøver en ekte eldre T5-fil med
gammel leser og verifiserer at dens typede basis er uendret i T6.

CLI velger eksplisitt `python -m analyse.innstilling95 --t5 FIL` eller
`--frosset FIL`; dokument, konto/år og outputflagg følger kontrakten.
`--originaler NY_KATALOG` gjenfinner også rekonstruerte 359–364 offline.

## Kontrollgrense

[Lokalt kontrollutfall](kontrollutfall.md) og [maskinelt utfall](checks.json)
angir hele sluttkjøringens faktiske resultat, hopp, tidsbruk og loggbinding.
[Akseptbeviset](acceptance.json) binder de28 gjenleste filparene.

[Kilde-/filjournal](source-control.json), [avgrenset visuell Excel-QA](excel-qa.md),
[TDD-journal](tdd-journal.json) og [lokalt kandidatgrunnlag](local-candidate.json)
gir konkrete innganger til kontrollene. Kandidatgrunnlaget binder15 produkt-,
kontrakt-, test-/reproduksjons- og legacy-/oracle-filer med rå SHA-256,
LF-representasjon og faktisk Git-filtrert blob-ID. Det er ikke et commit eller
et komplett kandidat-tre; orkestratorens frosne Git-kandidat er en egen port.
Nye kontrollbyte har skopede Git-attributter; gamle manifester er uendret.
[Originalgjenfinningen](original-retrieval.json) avstemmer alle35 lagrede
rårepresentasjoner byteeksakt; seks ytterligere XML-filer er rekonstruert
fra samme kapsel. Med indeks gir det42 faktiske originaleksportfiler.

Den [uavhengige originalfasiten](independent/README.md) er skrevet uten å
lese produktparseren. Produktet bruker aldri fasiten som adapterinput.
Testene sammenholder samtlige 216 nye felt med denne separate kilden og
prøver 35 Prop.-trioer, tre manglende post32-felt, ekte inntektsnull,
separate partimerknader, åtte fullmaktspunkter per stadium og fem nye
formelle fullmaktsvedtak. 339/114/38 skilles fra 216 nye felt og 36 nye hendelser.

M01/M06–M08/M13/M15/M22–M28 omfatter hele 95/359/360–364, post32, felles
utgift, inntekt/null, fullmakt, delt ramme, søstergrenen1429,1533, unions-
og kapittelvalg, tomt/manglende/feil år og begge returer. Semantiske
forfalskninger får nye ytre ID-er og faktisk XLSX med konsistent snapshot;
containerkontrollen består før de semantiske leserne avviser dem.
Presentasjon, tema, ZIP/XML, celletyper, lenker, chunks og no-clobber har
egne negative prøver. Eksakte grense- og overgrenseprøver gjelder T6;
gamle profiler er uendret. Fire syntetiske T6-feiltilstander prøves ved
siden av autentisk ny 40034229-oppdagelse/lagring/tolkning/ordinær eksport:
222 felt,74 hendelser uten historisk Excel.

Native Excel, helårsdekning, kontokontinuitet, faglig årsbalanse og all
tekst faglig avklart er ikke etablert. Uberiktiget95/rettelsesmeldingen
mangler fortsatt. Ulike beriktigede HTML-byte betyr ingen oppfunnet
semantisk rettelseshistorikk. #10/#32/#37 står åpne; ingen neste ticket.
