# Fremstilling av budsjetthistorikk

Analysedelen skal gi Finansavdelingen i Finansdepartementet oversikt over historiske budsjettforslag og budsjettvedtak.

Første prioriterte visning skal støtte departement, kapittel, post og kombinasjoner av disse. For utvalget skal regjeringens forslag, komiteens innstilling og endelig vedtak kunne sammenlignes med beløp, dokumentnummer og kildehenvisninger.

Excel er bekreftet som et første uttrekksformat. Første innlesningsleveranse fokuserer på endelige vedtak; forslag og innstillinger blir tilgjengelige etter at deres kilder er integrert. Manglende opplysninger skal fremgå i fremstillingen.

Se [krav](../docs/krav.md) og [ansvarsdeling](../docs/ansvarsdeling.md). Første leveranse gir Excel-uttrekk. Det interaktive grensesnittet kommer senere. Historikken skal vise hvert trinn gjennom året, med regnskap som egen talltype.

## Implementert i B1

`python -m analyse --database <SQLite-fil> --kjoring <ID> --excel <uttrekk.xlsx>` eksporterer én lagret kjøring uten nett eller ny innlesning. Python-grensen er `export_excel(database, run_id, output)` og bruker [datakontrakt v1](../docs/datakontrakt.md). Den leser via innlesningens offentlige lesegrense; den henter ingen kilde selv.

Excel viser numeriske kronebeløp, kilderad, faktisk kildehash, vedtaksidentitet, klikkbar lenke til Stortingets vedtak, råtekst og synlige mangler. Kildetekst skrives som tekstceller. Kildelenker aktiveres bare for det kanoniske vedtaksmålet hos Stortinget. Ved kontrollbehov står usikre beløp og godkjente summer tomme. Departementstilknytning er uavklart i B1. Utvalg, flere kilder og samlet historikk følger senere tickets.

## Versjonsvalgt eksport i B2

`python -m analyse --database <SQLite-fil> --revisjon <revisjons-ID> --excel <uttrekk.xlsx>` velger én bestemt B2-revisjon. Python-grensen er `export_revision_excel(database, revision_id, output)`. `--kjoring` består og er gjensidig utelukkende med `--revisjon`.

Valgte tall, strukturering og råhash er immutable. En historisk A-eksport viser fortsatt As beløp etter rettelse B, med separat historisk status, nåværende revisjon og siste observerte råhash. Ved A → B → A gjenbrukes As innhold, mens tidligere kontrollhenvisninger fortsatt er utdaterte. Arket `Kontrollhenvisninger` viser grunnlag, referanse, begrunnelse, tid og status; det endrer ingen beløp. Feilede eller ufullførte nyere forsøk, fravær og valgt omfang vises som egen observasjonsstatus.

Eksporten henter aldri nett eller velger en nyere revisjon automatisk. B1-kjøringer beholder sitt opprinnelige grunnlag og merkes som prøvearkiv uten valgt B2-registrering. Se [datakontrakten](../docs/datakontrakt.md#b2--kildeinventar-observasjoner-og-revisjoner). Samlet sesjonsbevilgning er fortsatt B6.

## Avgrenset historikk i B3

`HistorySelection` velger datasett, uttreks-ID-er (revisjon + tolkning), budsjettår, konto og detaljeringsnivå. `calculate_history` lagrer beregningen separat fra kildeobservasjonene. `read_history` gir det lagrede resultatet med separat ferskhetskontekst. Én original pluss vedtatte enkeltendringer kan avstemmes; andre talltyper, aggregater og før/etter er ikke additive.

`export_history_excel` leser en beregnings-ID uten ny innlesning og viser arkene `Historikk`, `Beløpsobservasjoner` og `Grunnlag og kontroll`. Avvik gir ingen avstemt saldo; observerte sluttbeløp beholdes. `avstemt_utvalg` er en regnekontroll av et valgt grunnlag, ikke faglig godkjenning eller komplett årsdekning. CLI-ene `--utvalg` og `--beregning` er alternativer til eksisterende `--kjoring` og `--revisjon`. Se [B3-kontrakten](../docs/datakontrakt.md#b3--beløpsobservasjoner-og-valgt-historikk) og [eksempel](../README.md#kjør-b3-lokalt).
