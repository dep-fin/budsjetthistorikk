# B8: to autentiske saksresponser

Kilde: Stortinget, [dokumentert saksendepunkt](https://data.stortinget.no/dokumentasjon-og-hjelp/sak/). Hentet 22. oktober 2026 uten autentisering. Begge XML-filer er hele, uendrede HTTP-responskropper med CRLF og er **ikke** syntetiske konvolutter eller utdrag. `.json`-sidevognene har URL, HTTP-status/headere, tidsmetadata, byteantall, SHA-256 og `fixture_kind=http_original`.

| Fil | Byte | SHA-256 |
| --- | ---: | --- |
| `sak-100927.xml` | 12 383 | `2ee25b327b78772523d56317c752e35f5134eef60db9536f6dea3c94ad8fed27` |
| `sak-100889.xml` | 15 888 | `3a8f0918a3fcce90bf2c93f3ce972c3de7277c76e27e5ef563d6c43384cf2af2` |

100927 er saken i den eksisterende B6-prøven for vedtak 40034048. 100889 er den ene saken originalen uttrykkelig relaterer til med `sammekilde`. Begge har fem publikasjonsreferanser, nil eksport-ID for regjeringens proposisjon og to ulike lenker til samme debatt-/voteringsreferat. De viser ulike innstillinger for ulike deler av samme proposisjon. Ingen årspåstand følger av prøven.

Originalene inneholder også offentlige saksordførerbiografier, med navn, fødselsdato, kjønn, fylke og partitilhørighet. De er ikke anonymisert. Ingen private kontaktopplysninger, credentials eller ikke-offentlige kilder er lagt til. Det avledede forskningsuttrekket har bare saks-, publikasjons- og relasjonsfelter. Publiseringsavgrensning, feltlokatorer, dokumentasjonskontroll, tidsbegrensninger og tolkningskonsekvenser står i [kilderapporten](../../../docs/research/b8/README.md).

En ny henting kan ha andre responsdatoer og annen råhash selv om saksdokumentene er uendret. Endre aldri originalen eller sidevognens hash for å få en test til å passe. Syntetiske mutasjoner skal lages separat og merkes uttrykkelig.

## Separat byteidentisk fullmaktsutdrag

`40034049.xml` er et avledet vedtaksutdrag, **ikke** en tredje komplett saksrespons. Det har 1 692 byte og SHA-256 `5f253a556d2ac512570899252b396bc38f068de5f4bd6820178e7de8ce41f3eb`. Utdraget bevarer originalprefix, ett uendret vedtaksobjekt og suffix fra den allerede lokalt bevarte offentlige sesjonsresponsen 2024–2025, hentet 22. oktober 2026 kl. 07.04.03 UTC. Forelderen har 7 479 943 byte og SHA-256 `c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42`. Objektet starter ved byte 1 255 498 (0-basert) og er 1 318 byte. `40034049.json` bevarer begge hasher, hentetid, offentlig URL og uttaksgrense. `tests/create_b8_fixtures.py` gjentar byteuttaket fra eksplisitte lokale kilde-/metadatafiler; ingen ny HTTP ble brukt for dette uttaket.

Formelt vedtak 211 (2024–2025) gjelder en stikkordsfullmakt om 1429/60. Originalteksten bevares, men det finnes ingen beløpsrad. Den autentiske beløpsprøven 210/40034048 ligger fortsatt uendret under `../b6/`. `.gitattributes` bevarer alle B8-XML-byte uten tekstnormalisering.
