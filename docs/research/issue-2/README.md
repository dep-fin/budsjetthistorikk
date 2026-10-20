# Kildeundersøkelse for bevilgningsvedtak

Del av #2 og spesifikasjon #1. Undersøkelsen er påbegynt etter brukerens godkjenning 20. oktober 2026. Dokumentasjonen er under arbeid og innebærer ikke fullført produksjonsinnlesning.

## Første kontrollerte funn

Vedtakstype BUDSJETT alene dekker ikke alle bevilgningsendringer. RNB-vedtak 857 (2023–2024), ID 40033719, og nysalderingsvedtak 428 (2024–2025), ID 40034287, er observerte ANNET-eksempler med bevilgningsendringer. Se [kontrollrapporten](kontrollkilder.md) for kilder og hentebevis.

DFØs bevilgningshistorikk kan brukes som en egen kontrollkilde. Fire 2024-poster er avstemt mot opprinnelige vedtak, Blå bok, endringsvedtak og statsregnskapets bevilgningskolonne. Dette er et avgrenset bevis på kildevei og beløpstolkning, ikke en fullstendig sesjonskontroll.

## Underlag

- [API-prøver, ID-koblinger og tabellvarianter](api.md)
- [API-kontrollresultater](api-kontroller.json)
- [API-hentemanifest](api-hentinger.json)
- [Kontrollkilder og fire avstemminger](kontrollkilder.md)
- [Avledede kontrollrader](kontroll-avstemming.json)
- [Hasher for lokale mellomfiler](kontroll-filhashes.json)

Originale råfiler er mellomlagret lokalt. Kilde-URL-er, hentestatus og SHA-256 er dokumentert. Regjeringssidens regnskapstabell ble lest gjennom nettverktøyet, men en direkte henting ga HTTP 403; et originalt råsvar fra denne siden er ikke bevart.

## Status og gjenstående arbeid

API-prøvene omfatter 24 vedtak i 2026–2027 og 1 260 i 2024–2025. Vedtakstekst finnes i sesjonsoversikten. I de fire undersøkte voteringsvedtak-svarene hadde alle 54 elementer nil-tekst. Sak, sesjon og vedtaksnummer ga en entydig kobling i utvalget, ikke en generell unikhetsgaranti. Gjentatte sesjonssvar var like etter normalisering av responstid; faktisk kilderettelse er ikke observert. Full årsavstemming, et bevilgningsvedtak uten proposisjonsgrunnlag, alle parservarianter og en varig råkopi av statsregnskapets kontrolltabeller er ikke ferdig verifisert. #2 holdes åpen til akseptansekriteriene er dokumentert eller konkrete gjenstående punkter er avklart.

## Kandidatgrunnlag for byggetickets

Den godkjente B1-ticketen #4 omfatter en opprinnelig bevilgning. Vedtak 40033944, nummer 113, er en liten opprinnelig tabell som kan brukes her. API-utforskerens anbefaling om 40033805 gjelder et enkelt endringsvedtak, som passer som tillegg for B3 (#6); det skal ikke erstatte det godkjente kravet om opprinnelig bevilgning i B1.

Ingen produksjonsteknologi er valgt på grunnlag av denne rapporten. Kildeprøvene viser at XML, HTML-tabeller, versjonering og presis beløpsbehandling må støttes, men de låser ikke programmeringsspråk, database eller Azure.
