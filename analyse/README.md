# Fremstilling av budsjetthistorikk

O2a/#34 har en egen opt-in-kommando `python -m analyse.omtale` for post 1 i 210. Den bevarer uendret B8/B9 og lager selvforsynt `omtale-pilot-1` med originaler, omtale og kontrollerte relasjonsbelegg. [Kontrakten og kommandoene](../docs/omtale-pilot.md) beskriver også offline gjenlesing. Prøven reproduseres fra reporoten med `python -m ops.omtale_proeve --output work/omtale-post1-leveranse`. Ingen ny faglig godkjenning eller drift følger med.

Den [historiske kontrollpakken](../docs/historisk-pilot.md) har egne `export`/`verify`-kommandoer i `python -m analyse.historical_package`. Hele lokalpiloten reproduseres med `python -m analyse.historical_pilot`; det [utførte kontrollomfanget](../docs/research/historisk-excel/pilot2024.md) skiller hele filen fra det avgrensede v2-utvalget.

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

## B4: selvstendig uttrekk og fulltekst

`export_extraction_excel(database, extraction_id, output)` og `--belopsuttrekk` viser hele uttrekket uten å kreve en bevilgningskjede. Observasjoner, cellepekere, hierarki, organisasjonskilde/gyldighet, avvik og full B2-tekst følger med, også ved null beløpsobservasjoner. Tekstopplysninger klassifiseres til kontroll uten normaliserte beløp. Historikkeksporten inkluderer også fulltekst for alle valgte revisjoner. Lange felt videreføres i 30 000-tegnsbiter. Kildetekst er formelsikret, og lagring er atomisk. Post- og underpostutvalg er fortsatt gjensidig utelukkende. Se [B4-kontrakten](../docs/datakontrakt.md#b4--særtilfeller-med-eksplisitt-tolkning-v2).

## B6: samlet sesjon med global dekning

`python -m analyse --database <SQLite-fil> --sesjonsutvalg <JSON-fil> --excel <ny-fil.xlsx>` sammenstiller valgte lagrede inventarjobber, tolkninger, B5-resultater og eventuelle beregninger uten nye kilder eller godkjenninger. Departement/fdep, kapittel og post kan kombineres; uavklarte treff og hele kildeinventaret forblir synlige. Hovedsesjon og supplerende kilder fra andre sesjoner har egen dekning.

Excel viser kronologisk historikk, rå/korrigerte/historiske effektive/gjeldende godkjente enkeltverdier, B5-bindinger, separate summer, avstemming, kilder og fulltekst. Manglende kontroll vises som ikke utført. Eksporten leser faktiske beløpsceller tilbake og avstemmer dem før atomisk publisering uten å overskrive eksisterende filer. Python-grensene er `SessionSelection`, `build_session_report` og `export_session_excel`. Se [JSON-veiledning og kontrollmodell](../docs/b6-sesjonsuttrekk.md).

B7 kan fryse en allerede vurdert `SessionReport` som validert `b6-frozen-1`-JSON og eksportere med `export_built_session_excel`; `export_session_excel` beholder eksisterende API. `verify_built_session_excel` avstemmer en fil etter tapt publiseringskvittering. Ingen ny kilde-/faglig vurdering skjer ved replay av den frosne rapporten. Nyere kildeforsøk før staging vises i nye vurderinger gjennom B2/B5-ferskhetskonteksten. Se [B7-manualen](../docs/b7-drift.md).
