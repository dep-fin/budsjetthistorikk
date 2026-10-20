# Kildeundersøkelse for bevilgningsvedtak

Del av #2 og spesifikasjon #1. Undersøkelsen er påbegynt etter brukerens godkjenning 20. oktober 2026. Dokumentasjonen er under arbeid og innebærer ikke fullført produksjonsinnlesning.

## Første kontrollerte funn

Vedtakstype BUDSJETT alene dekker ikke alle bevilgningsendringer. RNB-vedtak 857 (2023–2024), ID 40033719, og nysalderingsvedtak 428 (2024–2025), ID 40034287, er observerte ANNET-eksempler med bevilgningsendringer. Se [kontrollrapporten](kontrollkilder.md) for kilder og hentebevis.

DFØs bevilgningshistorikk kan brukes som en egen kontrollkilde. Fire 2024-poster er avstemt mot opprinnelige vedtak, Blå bok, endringsvedtak og statsregnskapets bevilgningskolonne. Dette er et avgrenset bevis på kildevei og beløpstolkning, ikke en fullstendig sesjonskontroll.

## Videre kildeavklaringer

- [Vedtak 599: direktebehandling uten komitéinnstilling og faktisk tallavvik](vedtak599/README.md)
- [Gjentatte overganger på 1860/01 og 4860/01](dobling/README.md)
- [Full årsavstemming 2024 med eksplisitte kildekonflikter](aar/README.md)
- [Selvstendig bevilgning uten proposisjonsgrunnlag i undersøkt kildekjede](selvstendig-bevilgning.md)
- [Stortingsinitiativ, bevilgning, fullmakt og negative prøver](stortingsinitiativ.md)
- [Varig originalkilde, hele regnskapstabellen og endringsregler](varig-kildegrunnlag.md)
- [Alle 2024-posters bevilgningskolonner](statsrekneskap2024-posts.csv)
- [Tabellkontroller](statsrekneskap2024-kontroller.json)

Den offisielle PDF-en for Statsrekneskapen 2024 er hentet med HTTP 200. Alle 1 655 postrader har bevilgning som stemmer mot samtlige 594 kapittelsummer og begge totalsummer. Dette validerer bevilgningskolonnens uttrekk, ikke i seg selv hele vedtakshistorikken.

## Underlag

- [API-prøver, ID-koblinger og tabellvarianter](api.md)
- [API-kontrollresultater](api-kontroller.json)
- [API-hentemanifest](api-hentinger.json)
- [Kontrollkilder og fire avstemminger](kontrollkilder.md)
- [Avledede kontrollrader](kontroll-avstemming.json)
- [Hasher for lokale mellomfiler](kontroll-filhashes.json)

Originale råfiler er mellomlagret lokalt. Kilde-URL-er, hentestatus og SHA-256 er dokumentert. Den første HTML-hentingen ga HTTP 403. Senere ble den uttrykkelig tilbudte offisielle PDF-en hentet normalt med HTTP 200 og bevart lokalt. Versjonerte postrader og hentemanifest følger den videre undersøkelsen.

## Status og gjenstående arbeid

API-prøvene omfatter 24 vedtak i 2026–2027 og 1 260 i 2024–2025. Vedtakstekst finnes i sesjonsoversikten. I de fire undersøkte voteringsvedtak-svarene hadde alle 54 elementer nil-tekst. Sak, sesjon og vedtaksnummer ga en entydig kobling i utvalget, ikke en generell unikhetsgaranti. Gjentatte sesjonssvar var like etter normalisering av responstid; faktisk kilderettelse er ikke observert. Vedtak 249/40005719 fra 2003 gir nå en autentisk positiv prøve på en selvstendig bevilgning uten funnet proposisjonsgrunnlag i relevant undersøkt kildekjede. Hele 2024 er nå avstemt: alle 1 625 felles DFØ-/regnskapsposter stemmer eksakt, og alle 43 nøkkelforskjeller er forklart. Alle 1 574 Blå bok-poster stemmer mot opprinnelige vedtak. Hendelseskjeden har fortsatt tre kildekonflikter som undersøkes nærmere; produksjonsparserens dekning er ikke testet. Originalt rågrunnlag for kontrolltabellene er nå sikret. #2 holdes åpen til akseptansekriteriene er dokumentert eller konkrete gjenstående punkter er avklart.

## Kandidatgrunnlag for byggetickets

Den godkjente B1-ticketen #4 omfatter en opprinnelig bevilgning. Vedtak 40033944, nummer 113, er en liten opprinnelig tabell som kan brukes her. API-utforskerens anbefaling om 40033805 gjelder et enkelt endringsvedtak, som passer som tillegg for B3 (#6); det skal ikke erstatte det godkjente kravet om opprinnelig bevilgning i B1.

Ingen produksjonsteknologi er valgt på grunnlag av denne rapporten. Kildeprøvene viser at XML, HTML-tabeller, versjonering og presis beløpsbehandling må støttes, men de låser ikke programmeringsspråk, database eller Azure.
