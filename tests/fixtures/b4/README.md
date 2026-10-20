# B4-kildeprøver

De tre XML-filene er komplette, uendrede enkeltobjekter med originalt byteprefix/suffix fra det offentlige API-svaret [2023–2024](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2023-2024). De er **avledede, delvise prøver**, aldri fullsesjonssvar. Sidevognene bevarer henteproveniens, URL, `derived_excerpt`, `partial`, eget og foreldresvarets byteantall/SHA-256.

Foreldresvaret har 6 816 165 byte og SHA-256 `554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf`, kontrollert før avledning 20. oktober 2026. Hentegrunnlag finnes i `docs/research/issue-2/kontrollkilder.md` og `aar/input_manifest.json`.

| Vedtak | Sak | Utdragsbyte | Utdrags-SHA-256 | Kontrollanker |
| --- | --- | ---: | --- | --- |
| 40032763 | 95780 | 85 042 | `4d5bf0b00dfe40dd73c543bb84b2be6a5bb2fe04e0b0bef08f9641902f907ff5` | 2445/24 total tr[79]/td[5] −334 642 000 |
| 40032791 | 95724 | 140 459 | `96a287159014126a824b61dd3891eb54d5615fbbe2d5078a7077f79e545cae2a` | 2460/24 total tr[101]/td[5] 102 500 000 |
| 40032976 | 95725 | 54 806 | `4c41b5647e65330e938d7bca93582900120c91753744892c826b53e57ddb3c0f` | 5440/24 total tr[62]/td[5] 295 900 000 000 |

Reproduksjon fra uendret foreldresvar:

```powershell
python tests/create_b4_fixtures.py <original-vedtak-2023-2024.xml>
```

Eksisterende [B3-fixturer](../b3/README.md) brukes uendret for øvrige B4-prøver: 2470/24, senere Sum-/tom-formål-oppstillinger, 90–99, nye poster, ANNET, fullmakter og historiske konflikter. [Kildefunnene](../../../docs/kildefunn.md#b4-prøver-post-24-komponenter-og-observerte-nye-nivåer) beskriver lokatorer, faktiske beløp og begrensninger.

Varianter med `1.`, linjeskift, kode 0, ukjent/duplisert/manglende komponent, feilsum, brutte relasjoner, kapitalgrenser, lange tekster, registerår og ukjente tabelloppsett i `test_b4.py` er uttrykkelig **syntetiske**. HTML-mutasjonene får `fixture_kind=synthetic_test` og ny hash. Ingen originalarbeidsbok på historikkbranchen er endret eller importert. CI bruker bare lokale prøver.
