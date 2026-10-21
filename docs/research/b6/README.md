# B6: kontroll av samlet uttrekk

Kontrollert 21. oktober 2026, offline mot bevarte kildebyte og forskningsartefakter. Dette er kontroll av eksport-/dekningsfunksjonen og dokumenterte begrensninger, ingen ny faglig godkjenning av hele sesjoner eller budsjettår.

## Hele inventarer gjennom SQLite og Excel

Originalresponsene for 2023–2024 og 2024–2025 ble lest på nytt gjennom offentlig `sync_saved(..., historical_sample=True)` i en separat prøvedatabase. Rå SHA-256 var henholdsvis `554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf` (6 816 165 byte) og `9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680` (7 479 943 byte). Hentetidene 20. oktober 2026 kl. 11.35.51 og 11.36.10 UTC og kilde-URL-ene følger [inputmanifestet](../issue-2/aar/input_manifest.json) og [årsrapporten](../issue-2/aar/README.md). Originalene ble ikke endret.

De 50 uttrykkelig valgte vedtaks-ID-ene i [decision_inventory.csv](../issue-2/aar/decision_inventory.csv) fikk separate v2-uttrekk fra sine eksakte B2-revisjoner. B6 valgte 2024–2025 som hovedsesjon og 2023–2024 som eksplisitt supplement, og eksporterte:

- Alle **2 183** inventar-ID-er: **1 260** i hovedsesjonen og **923** i supplementet. Alle API-typene ANMOD, ANNET, BUDSJETT, GRUNNLOV og RO var med.
- Alle **5 492 beløpsobservasjoner** fra de 50 valgte uttrekkene, med separat beløpsbetydning og komponentnivå. Dette er ikke samme antallsenhet som forskningsrapportens 2 935 posthendelser; før/delta/etter og underkomponenter kan gi flere observasjoner per hendelse.
- Fulltekst også for de **2 133** inventar-ID-ene uten valgt beløpsuttrekk, med synlig manglende strukturering. Globalt kildeinnhold var komplett for de valgte bevarte originalinventarene; struktur og faglig dekning var ufullstendig.
- Ingen faglig godkjente enkeltbeløp eller komplette summer ble konstruert. Ingen B5-resultater var valgt i denne inventarprøven. Regneberegninger med hele de 50 uttrekkene beholdt uavklarte tabell-/kontoavvik og ga ufullstendig kjedegrunnlag.

Den lokale prøven brukte omtrent 42 sekunder fra ny B2-database til ferdig arbeidsbok på 4 648 442 byte. Databasens SHA-256 var uendret før/etter B6-lesing og eksport. Dette er en konkret prøve, ingen generell ytelsesgaranti. Arbeidsboken var mellomlagret lokalt; verken den eller prøvedatabasen er produksjonsgrunnlag eller versjonerte kildeartefakter.

**Konsekvens:** Et helt kildeinventar og et stort Excel-uttrekk kan produseres uten å skjule kilder som ikke er tolket. De 50 kandidatene gir ikke uttømmende strukturering, og uavklarte tabeller/kontoer i et bredt uttrekk må fortsatt sperre berørte kjeder. Det er ikke innført noen ny parserregel for å få en grønn sum. De smale autentiske konfliktprøvene i B3–B6 viser dessuten de konkrete Havtil-/5999-konfliktene separat; de er ikke løst av et kontrollert sluttbeløp.

## Uavhengig 2024-kontroll beregnet på nytt

`audit_preserved_2024` leser seks hashfestede artefakter under [#2](../issue-2/aar/README.md), ikke `verification.json` eller gamle kontrollsummer. Alle 4 268 DFØ-rader rekonstrueres fra `Bevilgning_beløp` minus `Bevilgning_overført_beløp`, med eksakt desimalaritmetikk og dokumentert inntektsfortegn for 2024. Statsrekneskapens `loyving_1000kr` multipliseres med 1 000. Regnskap og samlet tilgjengelig bevilgning blandes ikke inn.

Resultatet var **1 638 DFØ-poster**, **1 655 PDF-poster**, **1 625 felles poster uten beløpsavvik** og **43 forklarte omfangsforskjeller**. De 30 PDF-unike og 13 DFØ-unike nøklene beholder manglende side som `None`; den eksisterende siden har 0. Alle 1 574 opprinnelige API-bevilgninger stemte mot Blå bok. Årets utgifter og inntekter var hver 2 951 906 811 000 kroner. De 2 183 inventarradene og typefordelingen ble telt fra selve inventaret. Hashene som håndheves finnes i `analyse/preserved_controls.py` og følger eksportens kontrollgrunnlag.

**Begrensning og konsekvens:** Dette gjentar kontrollen av bevarte, avledede felt; det leser ikke original-PDF-en på nytt og avstemmer ikke et vilkårlig nytt B6-utvalg. Eksportens egne godkjente verdier kontrolleres separat mot valgte lagrede B5-rader, faktiske Excel-celler og uttrykkelige kildeprøver. Manglende avstemming vises som ikke utført.

## Nye smale kildeprøver og automatisk regresjonskontroll

De komplette, byteidentiske enkeltobjektene 40034048 og 40034229 er avledet fra originalresponsen ovenfor. [B6-fixturene](../../../tests/fixtures/b6/README.md) dokumenterer egen/foreldrehash, byteposisjon og reproduksjon. De bevarer **2 + 74 = 76 posthendelser** uten standardinnledning, gjennom B2, v2-uttrekk og samlet rapport. Begge er ANNET. Dette krever ingen endring av v1 eller ny live forespørsel.

De deterministiske testene bruker offentlige grenser for globalt inventar/filtre, to budsjettår og supplerende sesjon, ukjent konto/år/departement, ny post uten start, post 24/90, tre kildekonflikter, kontrollert rå `I 615 833`, numerisk godkjent 0, begrensede B5-resultater, nyere avvisning/til kontroll, ventende kilde og A → B → A ved kilde/tolkning/register/kontrollgrunnlag, også uten observasjoner. Gyldige og uforenlige avstemmingsomfang, uttrykkelig fravær og manglende rader kontrolleres. CLI-, Excel-/ID-/beløpsrundtur og vern mot overskriving inngår. Ingen test henter nett eller endrer originalfixturene fra B1–B5.
