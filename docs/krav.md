# Krav og åpne beslutninger

## Formål og brukere

Finansavdelingen i Finansdepartementet skal kunne analysere og hente ut historiske budsjettforslag og budsjettvedtak. Hvert beløp skal kunne spores til kilde, dokument og behandlingsledd.

## Første leveranse

- Les inn og bevar endelige stortingsvedtak fra Stortingets kilder. Bevilgningsvedtak gir strukturerte opplysninger om budsjettår, kapittel, post, beløp og kilde.
- Start med sesjonen 2026–2027. Ta med endringer for inneværende budsjettår og vedtak for neste budsjettår. Viderefør innlesningen til nye sesjoner.
- Ta med alle bevilgningsendringer: opprinnelig budsjett, RNB, nysaldering og øvrige vedtak, også uten regjeringsproposisjon.
- Rene lovforslag kan utelates. Bevilgningsendringer i sammensatte lov- og budsjettsaker skal med.
- Oppdag nye og endrede vedtak daglig. Planlagt tidspunkt er kl. 06.00 i Europe/Oslo, med riktig håndtering av sommer- og vintertid.
- Gi en kjørerapport som skiller ingen nye vedtak, innlesningsfeil og uttrekk som krever kontroll.
- Lagre data og lever et kontrollerbart Excel-uttrekk. Interaktivt analysegrensesnitt kommer senere.
- Bevar fullmakter, stikkord og øvrige tekstvedtak med original struktur og kilde. Full detaljstrukturering av fullmaktsrammer er valgfri og skal ikke forsinke bevilgningsinnlesningen.
- Bevar underposter og kildehierarki der de forekommer. Posttotal og underliggende spesifikasjon skal ikke dobbeltelles.

## Historikk og beløp

Prosjekteieren bestilte 20. oktober 2026 presisering av det felles formatet før #6. [Observasjonsformat versjon 1](observasjonsformat.md) og [ADR 0003](adr/0003-felles-belopsobservasjoner.md) fastsetter separate beløpsobservasjoner, dokumentrelasjoner og beregnede verdier, med kompatible kildeadaptere for Excel og Stortinget. Dette er et modellgrunnlag for de eksisterende leveransene; historisk import, forslag, regnskap og omtale er fortsatt egne leveranser. Ingen historisk enhet eller kolonnetolkning er godkjent generelt.

Hvert opprinnelige vedtak og hver senere vedtatte endring skal kunne følges separat på kapittel og post. Bevar endringsbeløp og eventuelle fra-/til-beløp som kilden gir, og skill disse fra beregnet gjeldende bevilgning.

Forslag, vedtak og regnskap er forskjellige talltyper. RNB og nysaldering er behandlingsrunder som kan omfatte flere dokumenter og vedtak. Oppsummeringer av tidligere vedtak skal ikke leses som nye bevilgningsendringer.

Rettelser i en kilde er versjoner av kildeopplysningen. De skal kunne skilles fra et nytt stortingsvedtak om å endre bevilgningen.

Manglende inngående bevilgning skal gi ufullstendig beregningsgrunnlag, ikke et oppdiktet nullbeløp.

## Kontoplan og departementer

Både utgifter og inntekter inngår. Klassifikasjon følger kapittelnummer, ikke beløpets fortegn. Innenfor budsjettkapitlene er 1–2999 utgifter og 3000–5999 inntekter, jf. vedlagt R-101/2024 side 3. Kapitalregnskapets konti 6000–9999 skal holdes utenfor kapittelklassifikasjonen for bevilgningsvedtak.

Departementsnummer, navn, forkortelse og kapitteltilknytning skal kunne vedlikeholdes manuelt. Opplysninger skal ha gyldighetsperiode og kilde. Brukerens departementsoppsett og 2027-filen er utgangspunkt; eldre veiledere skal ikke overstyre nyere opplysninger.

Departementsnummer 10 og 12 er ledige i brukerens oppsett. Særkapitler og inntektskapitler krever eksplisitte oppslag. Hundretallsserier og +3000 er hjelperegler, ikke uttømmende departementskoblinger. Detaljer finnes i [departementsregisteret](departementsregister.md).

## Datakvalitet

Tvetydige uttrekk skal bevares med originalkilden og sendes til manuell kontroll. De skal holdes utenfor godkjente analysetall til de er avklart. Kjøring og uttrekk skal vise uavklarte opplysninger og manglende dekning.

Negative bevilgningsbeløp kan være gyldige, blant annet ved netto driftsresultat. Post 90–99 og særserier skal inngå i dekningskontrollen.

En ny post eller et nytt kapittel skal bevares selv om det mangler i 2027-katalogen. Uavklart departementstilknytning skal synliggjøres og ikke medføre at vedtaket forsvinner.

## Senere kilder og analyse

På sikt skal en post kunne følges gjennom regjeringens opprinnelige forslag, eventuelle tilleggsforslag, stortingsforhandlinger og innstilling, opprinnelig vedtak, alle senere endringer, RNB, nysaldering og regnskap.

Regjeringsforslag, komitéforslag, kapittel- og postomtale og regnskap inngår som egne kildeintegrasjoner. Regnskapstall skal ikke summeres inn som bevilgningsendringer. Overførte midler, fullmaktsrammer og eventuelle overskridelsessamtykker skal også kunne skilles fra årets vedtatte bevilgning.

Visning 1 skal støtte departement, kapittel, post og kombinasjoner av disse. For hvert trinn skal beløp, endring der den kan beregnes, dokumentnummer og kilde fremgå. Manglende kilder skal vises som manglende grunnlag.

Vedlagt Gul bok-fil gir en strukturert kilde til regjeringsforslaget og kapittel-/postmetadata. Katalogbruk kan forberedes uten uthenting fra regjeringen.no. Forslagsbeløp skal ha egen kildetype og skal aldri registreres som vedtak. Automatisk uthenting av regjeringsforslag skal ikke blokkere første leveranse. Brukeren har også eldre historiske data for senere import.

## Fullstendighet og kontroll

Målet er uttømmende dekning av bevilgningsendringer. Kontrollen må skille mellom funnet kildeinnhold, strukturerte opplysninger og godkjente analysetall. Uavklarte linjer er avvik som skal være synlige; de gir ikke grunnlag for å påstå fullstendig strukturering.

Kildeinventar og uavhengige kontrollsummer skal brukes sammen. Blå bok kan være et kontrollgrunnlag for opprinnelige vedtak; senere oppsummeringer og statsregnskapets bevilgningskolonner er mulige kontrollkilder som må prøves i kildeundersøkelsen. Regnskapets utfallsbeløp er ikke fasit for vedtatt bevilgning.

## Drift og mottakersystem

Python, SQLite og openpyxl er godkjent for lokal innlesning og Excel-uttrekk, og byggemandat er gitt for B1 (#4) 20. oktober 2026. Valget er dokumentert i [ADR 0001](adr/0001-lokal-innlesning.md). Eieren valgte 21. oktober 2026 en varig Windows-vert med lokal lagring for B7. Vert, driftskonto, datamappe og eksisterende bakgrunnstilgang er utsatt etter eierens beskjed «Dette vet jeg ikke, så det må vi komme tilbake til». Kodeleveransen omfatter runner og reviewbart Windows-oppsett; faktisk installasjon/driftsprøve gjenstår, og #10 forblir åpen. Ingen skyressurser eller credentials er opprettet. Se [driftsveiledningen](b7-drift.md).

## Manuelt vedlikehold og varsling

Første leveranse bruker Excel-/CSV-filer til vedlikehold av departements-/kapittelregisteret og behandling av uavklarte uttrekk. Endringer kobles til stabile identifikatorer og bevarer originalkilde, gyldighetsperiode og begrunnelse. Kilderevisjoner må gjøre utdaterte korreksjoner synlige før de brukes videre.

Ved innlesningsfeil eller uttrekk som krever kontroll opprettes en GitHub-issue. Gjentakelser av samme forhold oppdaterer samme issue. Vellykkede kjøringer uten slike avvik gir bare kjørerapport. GitHubs vanlige abonnementer styrer hvem som mottar varsler; løsningen skal ikke love en bestemt e-postlevering.

## Gjenstående bekreftelser

Samlet spesifikasjon, testgrenser og ticketoppdeling er godkjent av prosjekteieren 20. oktober 2026. Byggetickets er publisert som #4–#10. Kildeundersøkelsen #2 er levert i PR #11. Teknologiforslaget og byggemandatet for det smale B1-snittet er godkjent med «Gjør som du foreslår».

Gjenstående tekniske avklaringer:
- Konkret kilde- og fullstendighetskontroll etter kildeprøvene.
- Konkret Windows-vert, driftskonto, lokal lagrings-/rapportbane, eksisterende bakgrunnstilgang og faktisk driftsaksept. Endelig mottakersystem for felles bruk er fortsatt åpent.

Tekniske fakta undersøkes av agenten. Brukeren avgjør behov, prioriteringer og faglig aksept.

## Presisering 21. oktober 2026: nye kilder og historisk pilot

Oppfølging samme dag: byggemandat er gitt som #24. Den separate [2024-adapteren og kontrollpakken](historisk-pilot.md) er implementert og [fullt prøvd lokalt](research/historisk-excel/pilot2024.md). Åpne faglige kolonne-/register-/hierarkispørsmål består; samlet review, sikkerhetsaudit, CI og merge følger leveringsløpet. #13 gjelder fortsatt øvrige år og #10s driftsaksept gjenstår. Planbestillingens tidligere mandatgrense nedenfor er historisk kontekst.

Nye offisielle tall skal kunne oppdages, bevares, tolkes, lagres og eksporteres fra sin egen nye offisielle kilde uten historiske Excel-filer, eldre beløp, Excel-startsaldo, historisk register eller en vellykket historisk import. Manglende historisk inngående grunnlag skal gi et synlig analyseavvik når en beregning trenger dette, og skal ikke blokkere innlesning av det nye vedtaket eller gi en oppdiktet nullstart. Dette skal ha en uttrykkelig regresjonsprøve, også ved fraværende, korrupt eller motstridende historisk kilde.

Den historiske modellen skal bevare kilden og betydningen uten å gjøre arbeidsbøkenes kolonner eller dagens API-form styrende for nye kilder. Et bedre felles format kan foreslås og versjoneres ved dokumentert behov, med uttrykkelig kompatibilitetsbeskrivelse. Dagens besluttede observasjonsformat, leverte API-er, ID-er og standardvalg gjelder frem til en slik utvidelse er besluttet. Eksisterende parser-, format- og skjemaidentiteter skal beholde sin betydning. Ingen migrering eller kodebygging følger av bestillingen om en plan.

[Pilotplanen under #13](pilotplan-historisk-excel.md) anbefaler 2024 som én lokal leveranse fra original til historiske observasjoner, lagring, Excel/avviksrapport og uavhengig sammenligning. Årsvalget støttes av den [utførte, avgrensede Excel-/Storting-prøven](research/historisk-excel/pilotkontroll.md). Full historisk filadapter, pilotimport og årsavstemming gjenstår. Uavklarte enheter, kolonnefortolkninger og organisasjonskoblinger blokkerer faglig bruk av berørte verdier; råbevaring, observasjonslagring og kontrolluttrekk kan bygges med synlige avvik. Konkret byggemandat gjenstår. Utsatt driftsaksept i #10 er fortsatt åpen og blokkerer ikke den lokale historikkpiloten.

## Godkjent saksberikelse og stikkord – 22. oktober 2026

Eieren bestilte #28/B8 med kildekontroll, implementering, samlet review, separat sikkerhetsaudit, CI og merge. Saksdokumentenes metadata skal hentes fra Stortingets saks-API og versjoneres separat fra tidligere vedtaks-/beløpsobservasjoner. Formelt vedtaksnummer med sesjon, teknisk API-ID og klikkbare innstillings-/proposisjonsnumre vises ved beløp i Excel og frosset JSON med eksplisitt ny versjon. Saksrelasjoner er ingen bevist postvis forslagstilknytning. Dokumentfulltekst og forslagsbeløp er utenfor omfanget.

Eieren presiserte samme dag at «Stikkord» skal være en egen synlig kolonne. 1429/22 i vedtak 210 skal vise «kan overføres», med bevart råtekst og kildepeker. Ingen stikkord funnet og uavklart tolkning er ulike utfall. Stikkordsvisningen er separat berikelse, uten endring av gamle observasjoner eller ekstra beløpshendelse. Vedtak 211s fullmakt skal fortsatt ikke bli bevilgningsbeløp.

Tidligere ID-er, råbyte, B5-avgjørelser, v1/v2-tolkninger og B7s standardvalg bevares. Manglende eller feilet saksgrunnlag skal synes uten å stoppe nye vedtak eller beløpseksport. Globale dokumentavvik bevares før filtre. Historisk Excel/register/start er ingen avhengighet. [B8-veiledningen](b8-saksdokumenter.md) beskriver den nye opt-in-grensen; orkestratorens review, sikkerhetsaudit, CI og merge er egne leveringsporter. #10s faktiske driftsaksept er fortsatt utsatt, og #1/#10/#13 holdes åpne for sine rester.

## Godkjent hovedvisning for historikk – 22. oktober 2026

Eieren bestilte #30/B9: Historikk skal være første aktive ark i B8-uttrekket, med nøyaktig 13 synlige kolonner i denne rekkefølgen: Kapittelnummer, Postnummer, Kapittelnavn, Postnavn, Stikkord, Dato, Vedtaksnummer, Innstillingsnummer, Proposisjon, Beløp før vedtak, Vedtatt endring, Beløp etter vedtak og Kontrollstatus. Kildenavn skal brukes, med forsiktig skille mellom postnavn, stikkord og handlingsord. Manglende eller motstridende grunnlag skal synes. Før/etter er kildeobserverte beløp, ingen konstruert null eller kjedesaldo.

Tidligere detaljkolonner og full sporbarhet beholdes i en egen synlig reservefane. Flere dokumenter beholder alle henvisninger og klikkbare lenker uten flere beløpsrader eller hovedkolonner. Kontrollstatus skal også synliggjøre globale avvik før filtre, ferskhet og faglige begrensninger. En tom beløpsvisning skjuler ikke disse. Se [B9-veiledningen](b9-historikk.md) og [kontrollrapporten](research/b9/README.md). Eksisterende frosset JSON, ID-er, kilder, B1–B7 og uavhengig ny offisiell registrering bevares. Nytt konkret 210-uttrekk produseres etter review, CI og merge, med eget navn. #10 holdes åpen.
