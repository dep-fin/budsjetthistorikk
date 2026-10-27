# T3/#46: avgrenset 2024-forløp

Lokal byggekandidat fra main `c1cb156d50fb986794e2af8b20a131209e4707a7`, tre
`ae70d77b07662bb0e01276237c8d802d98e00117`, branch `codex/t3-2024-forlop`.
Byggeren gjør lokale endringer og kontroll. Samlet Standards-/Spec-review,
separat defensiv audit, GitHub/CI og merge er orkestratorens porter.

[Kontrakten](../../forlopspilot.md) ble fastsatt før produktkode, med eksplisitt
`visningspilot-3` og egen regel/leser. [Utforskergrunnlaget](source-findings.md)
bevarer kildefunnene og deres opprinnelige status som undersøkelse/forslått
fasit. Produktaksept føres separat i [akseptledgeren](aksept.md) og den
hashfestede kontrolljournalen `verification.json`.

[Sluttmanifestet](delivery-manifest.json) og [kildekontrollen](source-audit.json)
er byteidentiske kopier av de lokale journalene. [Kodehashene](candidate-code.json)
skiller faktiske Windows-byte fra Git-LF. [Rendering og kontrollområder](rendering.json)
og previewbildene er bevart sammen med kontrolloggene.

Avsluttende lokal fullsuite: **1118 bestått, to eksisterende Windows-
rettighetsskips (symbolsk lenke/hardlink), 1512,57 s**. Alle **46 T3-prøver**
bestod, 153,345 s inkludert fixturetid i JUnit. Ruff check/format (118 filer)
og mypy (67 kildefiler) består. Linux-CI er ikke kjørt av byggeren.

Sluttprøven tok 421,579 s og produserte 20 autentiske utvalgspar, ett ekstra
offentlig offline-CLI-par og fire par med tomt utvalg under syntetiske kildefeil.
14 rehashede negative JSON/XLSX-par og fire falske/skjulte presentasjonsbøker
ble avvist. 27 ekte tidligere par og én separat gammel B6-bok ble gjenlest.
Alle **225 manifestførte filer** ble rehashet uten endring. I tillegg finnes
den særskilte fem-filers avhengighetsprøven og fullsuitens JUnit-fil.

## Leveranse

Fem nye 341-/857-kildefelt og én ordrett, validert T1-kapsel gir et valgt
341→857→210-forløp for 1429/1 og /22 i budsjettåret 2024. T1s 18 felt og seks
vedtaksfelt/to hendelser beholder ID-er, råkilder og tolkning. Begge innganger
bruker samme basis. T2/315-data kreves ikke. [Egen avhengighetsprøve](dependency-proof.json)
gir samme basis/rapport fra bare fem T3-kildefiler og én T1-kapsel. Den selvstendige adapteren kan
bevare de fem nye feltene uten tidligere kapsel og vise manglende 210 som hull.

| Utvalg 2024 | Tabellfelt | Vedtaksfelt | Vedtatte monetære hendelser |
| --- | ---: | ---: | ---: |
| /1 | 13 | 7 | 3 |
| /22 | 10 | 4 | 2 |
| Begge / kapittel 1429 | 23 | 11 | 5 |
| Tomt / feil år / tekst-fullmakt /60 | 0 | 0 | 0 |
| Dokument 341 | 2 | 2 | 2 |
| Dokument 857 | 3 | 3 | 1 |
| Dokument 210 | 6 | 6 | 2 |

Null i denne tabellen gjelder strukturerte utvalgsobjekter. /60 har også
andre beløpsrader i 341/857s ustrukturerte råinventar; T1 bevarer tekst/fullmakt.
Ingen av disse nulltellerne er en observert nullbevilgning.

341s 19.12.2023-dato blir ikke budsjettår 2023. Nivå vises separat fra
før/endring/etter; 857s rå positive million med «reduseres med» gir −1 million.
Det avgrensede /22-fraværet i 857s tr822–830 før 1432 i tr831 er et eget
kildebevis. Ingen nullhendelse eller generell RNB-/årsfraværspåstand opprettes.

To separate beregningsobjekter binder startnivå/delta-ID-er og observerte
kontrollfelt: 166 039 000 og 29 185 000 kroner. Status er **avgrenset kontroll**.
Manglende start/delta/kontroll, konflikt, feil år/enhet/omfang/rolle/runde eller
rekkefølge sperrer. Nivåer, før-/etterfelt og forslag adderes ikke som deltaer.
Regningen gir ingen ekstra kildeobservasjon/hendelse, faglig avgjørelse,
godkjent årsbalanse eller uttømmende periode-/årsdekning.

## Bytebevis og synlige rester

341 og 857 avledes fra 66aa-fullresponsen med eksakte bytegrenser. Hele
objekter, original gzip, transportmetadata og kontrollmanifest er innebygd.
341s konvolutt er byteidentisk med bevart utdrag. Den nye 857-konvolutten har
SHA `252544da8756b038d54f6e935323fb33227b7ef16ee4c540a1badb7c5245517f`.
Det gamle 857-objektet er byteidentisk, men gammel fixture/sidevogn beholder
sin egen 554e-forelder; den fullresponsen er ikke gjenlest eller ommerket.
210 beholder 9cfe-forelderen gjennom den gamle strenge T1-leseren.

Hele 341-tabellens 153 og 857-tabellens 1488 rader er tilgjengelige, også ved
tomt utvalg. Uttrykkelige postkolonner, tilgrensende før/etter, totaler og
SDØE-spesifikasjoner har ulike inventarroller. Total-/komponentrader får
ingen arvet postkobling. Dokumentets kontoliste viser observerte
tabellreferanser; /22-fravær i 857 blir ikke positivt dokumentmedlemskap.
Øvrige beløp forblir ustrukturerte; radinventar er ingen sertifisert monetær
fulltelling. T3s begrensede inventartak 4096 rommer dette; gamle 512-tak består.

Navngitte hull består globalt: opprinnelige forslag/tillegg/Innst14/postvis
vedtakelse, RNBs Prop104/kapittel5-original og postkobling, gjenlesbar Innst447-
tilråding/rolle og vedtakelsesbevis, øvrige endringer/ukjent omfang, vedtak uten
proposisjon, uttømmende periodeinventar og årsavslutningsavstemming. Kjent
nysaldering fyller ikke hull i andre runder. #10/#32/#37 er fortsatt åpne.
Arvede T1-dekningsavvik merkes som `T1-kapsel:` i den nye fremstillingen;
de beskriver kapselens opprinnelige snitt, mens T3s nye dekning står separat.
De opprinnelige strengene og statusene forblir uendret inne i T1-kapselen.

## Filgrense og reproduksjon

Nye råpayload lagres én gang per hash og kildefelt én gang per
versjon/tolkning/lokator. Avledede kilder peker til forelderens payload.
Én uendret T1-kapsel bevarer gamle objekter; ingen ekstra gammel basis/T2-kapsel
serialiseres. Faktiske JSON- og Excel-snapshot telles separat, med arvet
immutable duplisering uttrykkelig oppgitt i manifestet.

Excel følger T2s fem hovedfaner og tilgjengelige Kontroll/Offlinegrunnlag.
Hele inventaret, fulltekst, lange felt, kildepekere, runder og globale hull
består ved null treff. Kildetekst med formeltegn lagres som tekst. Leseren
rekonstruerer bok/utvalg/regning og avviser endrede eller skjulte celler,
formater, lenker, dimensjoner og ZIP/XML-objekter. Datoene er ekte datoceller;
escapede punktum i `dd"."mm"."yyyy` gir riktig visning også i Artifact Tool.

Fra fersk checkout med Python3.12 og pinnede `requirements-dev.txt`:

```powershell
python -m pytest tests/test_forlopspilot.py -q --durations=12 --basetemp work/t3-test-ny
python -m ops.forlopspilot_proeve --output work/t3-delivery/ny
python -m analyse.forlopspilot --rot . --t1 work/t3-delivery/ny/authentic-t1.json --aar 2024 --konto 1429/1 --konto 1429/22 --json work/t3-cli/begge.json --excel work/t3-cli/begge.xlsx
python -m analyse.forlopspilot --frosset work/t3-cli/begge.json --rot work/ingen-originaler --json work/t3-cli/offline.json --excel work/t3-cli/offline.xlsx --originaler work/t3-cli/originaler
node ops/render_forlopspilot.mjs work/t3-delivery/ny/both.xlsx work/t3-delivery/ny/render-both
node ops/render_forlopspilot.mjs work/t3-delivery/ny/empty.xlsx work/t3-delivery/ny/render-empty empty
```

Velg nye outputnavn; skriverne kontrollerer begge faktiske filer etter lukking.
Ops-prøven bruker repoets autentiske T1-arkiv, ikke et regenerert gammelt
resultat. `--previous-root` og `--legacy-b6` legger til reell historisk
kompatibilitet fra tilgjengelige gamle originaler, med hashkontrollerte kopier.
Se [overleveringen](OVERLEVERING.md) for lokale runtime-/arkivbaner og siste portutfall.

Native Excel og selvstendig gammel frozen-v1-rapport-JSON er særskilte
bevisgrenser. T4–T6/K1–K3, godkjent årsbalanse, kontokontinuitet, historisk
produksjonsimport og faktisk drift følger ikke av denne leveransen.
De fire 368-prøvene nyregistrerer en bevart autentisk 2024-respons i hver
ferske database; dette er ingen påstand om nylig livevedtak eller ny HTTP-henting.
