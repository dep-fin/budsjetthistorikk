# Kildeprøver for B3

XML-filene er **avledede enkeltvedtaksutdrag**, ikke fullsesjonssvar. Hvert utdrag er sammensatt av original byteprefix, én komplett uendret objektblokk og original suffix. Sidevognen har utdragets SHA-256/byteantall og foreldresvarets SHA-256/byteantall, kilde-URL, bevart hentetid og `fixture_kind=derived_excerpt`, `session_coverage=partial`. B2 krever eksplisitt valgt ID og historisk prøve. CI henter ingen nettdata.

Foreldregrunnlag kontrollert 20. oktober 2026:

| Sesjon | Original byteantall | Original SHA-256 | Varig proveniens |
| --- | ---: | --- | --- |
| 2023–2024 | 6 816 165 | `554e9960c3e90932594106463cca9c285abb53e9272c1ae391d6fb8093baf0bf` | `docs/research/issue-2/kontrollkilder.md`, `aar/input_manifest.json` |
| 2024–2025 | 7 479 943 | `9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680` | samme |
| 2025–2026 | 7 387 302 | `795afc4202c51a13c4360f1374f3a603aa5d8e803c57195ec48effb60c6aebf6` | `docs/research/issue-2/vedtak599/fetch-manifest.json` |

Reproduksjon fra de lokalt bevarte fullsesjonsoriginalene:

```powershell
python tests/create_b3_fixtures.py <mappe-med-vedtak-2023-2024.xml-og-vedtak-2024-2025.xml> <original-vedtak2025-2026.xml>
```

Prøvene inneholder følgende kontrollgrunnlag:

- 40032850, 40033719, 40033805 og 40034064: 2541/70, budsjettår 2024, opprinnelig 12 818 000 000, delta −608 000 000, +400 000 og +680 000 000, slutt 12 890 400 000 kroner.
- 40034064 og 40034226: begge publiserte Havtil-overganger beholdes. Kjedekonflikt sperrer saldoen, selv om begge lokale kontroller består.
- 40033025, 40033719 og 40034287: 5999/90. RNBs til-beløp 0 og nysalderingens til-beløp 120 371 709 000 beholdes uten en kunstig mellomendring.
- 40034443: 900/32 +454 000 000 og 1760/45 −227 000 000 uten før/etter. «(Ny)» gir ingen nullstart.
- 40034385, 40035422 og 40035429: initiativ, faktisk endring 9 700 000 og separat fullmakt 72 000 000 holdes fra hverandre.
- 40036289: rå til-tekst `I 615 833` bevares med uavklart normalisering. Ingen I→1 eller nullpåfylling.

B1-kontraktprøven 40033944 bruker den eksisterende fixturen ett nivå opp. Denne har et annet faktisk foreldresvar med egen bevart hash; den er ikke ommerket til den nyere hentingen.

Alle beløps-, dato-, metadata-, kontrollrad- og A→B→A-mutasjoner i `tests/test_b3.py` er **syntetiske negative kontroller**, og sidevognene endres til `synthetic_test`. Den generiske Excel-lignende prøven er en syntetisk representasjonsprøve med lokale identiteter og byte som uttrykkelig ikke er en arbeidsbok. Den viser modellkompatibilitet, ingen generell historisk enhets-/kolonnegodkjenning eller full Excel-adapter. Autentiske årsutdrag er heller ingen garanti om generell parser- eller sesjonsdekning.
