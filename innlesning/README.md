# Innlesning av endelige stortingsvedtak

Den separate [historiske 2024-adapteren](../docs/historisk-pilot.md) kjøres med `python -m innlesning.historical_excel`. Den bruker datasett `historisk`, eget celleinventar og immutable importforsøk. Offisiell innlesning nedenfor har ingen avhengighet til historiske arbeidsbøker, register eller startsaldo.

Første leveranse skal hente, bevare og strukturere endelige vedtak fra sesjonen 2026–2027. Nye og endrede vedtak skal kontrolleres daglig kl. 06.00 i Europe/Oslo. Første import omfatter også vedtak som gjelder inneværende budsjettår. Nye sesjoner følges videre automatisk. Bevilgningsendringer på både inntekts- og utgiftskapitler inngår, også når saken ikke bygger på en regjeringsproposisjon.

Innlesningen skal kunne kjøres uavhengig av analysegrensesnittet. Senere forslag og andre kilder får adskilte adaptere. Regjeringsforslag er bare en mulig tidlig utvidelse dersom kildeveien er enkel.

Første leveranse gir kildebevaring, strukturerte vedtaksdata, kontrollrapport og Excel-uttrekk. Fullmakts- og vedtakstekst, stikkord og kildehierarki bevares; avansert strukturering av fullmakter kommer ved behov senere.

Se [krav](../docs/krav.md), [ansvarsdeling](../docs/ansvarsdeling.md) og [kildeundersøkelser](../docs/kilder.md).

## Implementert grense i B1

`python -m innlesning hent` velger ett vedtak i en sesjonsrespons, bevarer responsbytene og strukturerer den dokumenterte originaltabellen. [README](../README.md#kjør-b1-lokalt) viser oppstart og offline-prøve. [Datakontrakt v1](../docs/datakontrakt.md) beskriver lesegrensen for analyse og eksport.

HTTP-adapteren bruker bare det faste offentlige sesjonsendepunktet, validerer sesjonsformat, avviser omdirigering, har 1–120 sekunders socket-timeout og grense på 32 MiB. Det gjøres ett kall per eksplisitt oppstart, uten automatisk retry eller parallell innhenting. Lagret respons med hentemetadata kan brukes uten nett. XML-DTD og entitetsoppløsning tillates ikke. HTML tolkes som data og utføres ikke.

lxml er pinnet til [6.1.3](https://pypi.org/project/lxml/6.1.3/), som retter standardbehandlingen av eksterne parameterentiteter. Innlesningen beholder i tillegg eksplisitt `resolve_entities=False`, `no_network=True` og `load_dtd=False`, og avviser alle DOCTYPE-er.

Den autentiske prøven er opprinnelig vedtak 40033944 fra 2024–2025, med alle åtte postlinjene. Dette er en uttrykkelig historisk demonstrasjon. Ukjente mønstre og tvetydige beløp bevares med synlig kontrollbehov. Daglig kjøring, generell parserbredde, registervedlikehold og full faglig sesjonsdekning gjenstår i senere tickets.

## Implementert grense i B2

`synkroniser` bevarer råbyte og sammenligner alle ID-er i full sesjon, med immutable vedtaksrevisjoner og én atomisk publisering. En ny ID er et eget vedtak også ved gammel dato eller like beløp. Nytt innhold under samme ID er en rettelse. Bare ny responstid gir ny kildeobservasjon med samme revisjon og samme postrader. Fravær gir avvik, ikke sletting.

`stage_sync`/`--forbered` bevarer en ventende jobb og returnerer ID før publisering. `resume_sync`/`gjenoppta` trenger bare den ID-en og databasen; feil ved publisering rulles tilbake. Én ventende jobb per datasett/sesjon og kontroll av kilde-/hentetid hindrer at eldre arbeid overstyrer nyere vellykket observasjon. Den lokale rekkefølgen er ingen utgivergaranti om ferskhet.

`read_sync` gir kjørerapport. `read_revision` gir valgt revisjon og separat ferskhetskontekst. `record_control_reference` bevarer en begrunnet henvisning uten å endre analysetall. Nye kildeversjoner gjør gamle henvisninger utdaterte, også ved A → B → A. Filimport og faglig kontrollvirkning kommer i B5.

Se [kommandoer og prøver](../README.md#kjør-b2-lokalt), [B2-kontrakten](../docs/datakontrakt.md#b2--kildeinventar-observasjoner-og-revisjoner) og [ADR 0002](../docs/adr/0002-kildeobservasjoner.md). Alle typer bevares, men B1-parserbredden består. B2 er ikke B6s samlede sesjonseksport.

## Separat beløpstolkning i B3

`innlesning.observations` gir immutable, kildeuavhengige beløpsobservasjoner og en avgrenset Storting-adapter. `extract_revision` leser én eksplisitt valgt B2-revisjon, bevarer første rågrunnlag og gjenbruker identiteter ved ny lesing. Før/endring/etter er egne observasjoner i samme ledd. Råverdier, enhet, akser, lokator og proveniens bevares; B1s `structure_node`, parseridentitet og resultater endres ikke.

`save_extraction` og `read_extraction` er den generiske lagringsgrensen. API-ID og dato kan mangle med nullgrunn; underpost, historisk organisasjon og flere dokumentreferanser kan representeres. Dette er ingen historisk Excel-adapter. Additiv skjemaversjon 3 beholder B1/B2 og ventende jobber. Se [B3-kontrakten](../docs/datakontrakt.md#b3--beløpsobservasjoner-og-valgt-historikk) og [CLI-eksempelet](../README.md#kjør-b3-lokalt).

## Eksplisitt B4-tolkning

B7s [daglige runner](../docs/b7-drift.md) bruker fullt kildeinventar, alle API-typer/ID-er og eksplisitt v2/registersnapshot. Nyere kildeforsøk før staging blir synlige i ferskhetskonteksten. Tidligere v1-standarder og immutable resultater består. Faktisk Windows-installasjon/driftsprøve gjenstår etter eierens avklaring 21. oktober 2026.

`Interpretation(adapter_version="storting-belop-v2")` velger nummererte post-24-spesifikasjoner og observerte totalceller, med eksakt komponentkontroll og registersnapshot. V1 forblir standard og uendret. Nye nivåoppstillinger uten delta gir etterbeløp. Kontoklassifikasjon følger kapittel, mens organisasjonen bygger på ni eksplisitte oppslag med gyldighet bare 2027. Ukjent oppslag beholder beløpet. Se [B4-kontrakten](../docs/datakontrakt.md#b4--særtilfeller-med-eksplisitt-tolkning-v2).
