# Innlesning av endelige stortingsvedtak

Første leveranse skal hente, bevare og strukturere endelige vedtak fra sesjonen 2026–2027. Nye og endrede vedtak skal kontrolleres daglig kl. 06.00 i Europe/Oslo. Første import omfatter også vedtak som gjelder inneværende budsjettår. Nye sesjoner følges videre automatisk. Bevilgningsendringer på både inntekts- og utgiftskapitler inngår, også når saken ikke bygger på en regjeringsproposisjon.

Innlesningen skal kunne kjøres uavhengig av analysegrensesnittet. Senere forslag og andre kilder får adskilte adaptere. Regjeringsforslag er bare en mulig tidlig utvidelse dersom kildeveien er enkel.

Første leveranse gir kildebevaring, strukturerte vedtaksdata, kontrollrapport og Excel-uttrekk. Fullmakts- og vedtakstekst, stikkord og kildehierarki bevares; avansert strukturering av fullmakter kommer ved behov senere.

Se [krav](../docs/krav.md), [ansvarsdeling](../docs/ansvarsdeling.md) og [kildeundersøkelser](../docs/kilder.md).

## Implementert grense i B1

`python -m innlesning hent` velger ett vedtak i en sesjonsrespons, bevarer responsbytene og strukturerer den dokumenterte originaltabellen. [README](../README.md#kjør-b1-lokalt) viser oppstart og offline-prøve. [Datakontrakt v1](../docs/datakontrakt.md) beskriver lesegrensen for analyse og eksport.

HTTP-adapteren bruker bare det faste offentlige sesjonsendepunktet, validerer sesjonsformat, avviser omdirigering, har 1–120 sekunders socket-timeout og grense på 32 MiB. Det gjøres ett kall per eksplisitt oppstart, uten automatisk retry eller parallell innhenting. Lagret respons med hentemetadata kan brukes uten nett. XML-DTD og entitetsoppløsning tillates ikke. HTML tolkes som data og utføres ikke.

lxml er pinnet til [6.1.3](https://pypi.org/project/lxml/6.1.3/), som retter standardbehandlingen av eksterne parameterentiteter. Innlesningen beholder i tillegg eksplisitt `resolve_entities=False`, `no_network=True` og `load_dtd=False`, og avviser alle DOCTYPE-er.

Den autentiske prøven er opprinnelig vedtak 40033944 fra 2024–2025, med alle åtte postlinjene. Dette er en uttrykkelig historisk demonstrasjon. Ukjente mønstre og tvetydige beløp bevares med synlig kontrollbehov. Daglig kjøring, generell parserbredde, rettelser, registervedlikehold og full sesjonsdekning gjenstår i senere tickets.
