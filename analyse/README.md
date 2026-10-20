# Fremstilling av budsjetthistorikk

Analysedelen skal gi Finansavdelingen i Finansdepartementet oversikt over historiske budsjettforslag og budsjettvedtak.

Første prioriterte visning skal støtte departement, kapittel, post og kombinasjoner av disse. For utvalget skal regjeringens forslag, komiteens innstilling og endelig vedtak kunne sammenlignes med beløp, dokumentnummer og kildehenvisninger.

Excel er bekreftet som et første uttrekksformat. Første innlesningsleveranse fokuserer på endelige vedtak; forslag og innstillinger blir tilgjengelige etter at deres kilder er integrert. Manglende opplysninger skal fremgå i fremstillingen.

Se [krav](../docs/krav.md) og [ansvarsdeling](../docs/ansvarsdeling.md). Første leveranse gir Excel-uttrekk. Det interaktive grensesnittet kommer senere. Historikken skal vise hvert trinn gjennom året, med regnskap som egen talltype.

## Implementert i B1

`python -m analyse --database <SQLite-fil> --kjoring <ID> --excel <uttrekk.xlsx>` eksporterer én lagret kjøring uten nett eller ny innlesning. Python-grensen er `export_excel(database, run_id, output)` og bruker [datakontrakt v1](../docs/datakontrakt.md). Den leser via innlesningens offentlige lesegrense; den henter ingen kilde selv.

Excel viser numeriske kronebeløp, kilderad, faktisk kildehash, vedtaksidentitet, klikkbar lenke til Stortingets vedtak, råtekst og synlige mangler. Kildetekst skrives som tekstceller. Kildelenker aktiveres bare for det kanoniske vedtaksmålet hos Stortinget. Ved kontrollbehov står usikre beløp og godkjente summer tomme. Departementstilknytning er uavklart i B1. Utvalg, flere kilder og samlet historikk følger senere tickets.
