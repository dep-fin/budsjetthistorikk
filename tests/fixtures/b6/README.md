# B6: vedtak uten standardinnledning

Avledet 21. oktober 2026 fra den allerede bevarte komplette offentlige responsen for 2024–2025. Originalen er lest uten endring og har 7 479 943 byte, SHA-256 `9cfeaef59510a54ff8b2a695e0be368e67cfbab574f8d3f466c0c2f0c3c92680`, hentet 20. oktober 2026 kl. 11.36.10 UTC fra [Stortingets API](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025). Bevaringsmanifest: [#2](../../../docs/research/issue-2/aar/input_manifest.json).

`create_b6_fixtures.py <original.xml>` validerer foreldrehash/byteantall før det avleder original konvoluttprefix, ett komplett byteidentisk vedtaksobjekt og original suffix. Sidevognene bevarer egen hash/byteantall og nullbasert objektposisjon i forelderen. Dette er delvise enkeltvedtaksprøver, ingen fullsesjonsfixturer.

| Vedtak | Objektstart (byte, 0-basert) | Objektbyte | Utdragsbyte | Utdragets SHA-256 | Posthendelser |
| --- | ---: | ---: | ---: | --- | ---: |
| 40034048 | 1 249 812 | 5 686 | 6 058 | `2a540261f110b761a0213516c8ad72844d0285744ca0f1cdd4cb1afce06f0850` | 2 |
| 40034229 | 2 298 491 | 132 911 | 133 283 | `66208daf51111356ad73c26985819870ab9c2f97ec7b070024d89e150cd772b9` | 74 |

Begge API-objektene er ANNET og har bevilgningstabell uten standardinnledningen om statsbudsjettet. B2/B4/B6 leser dem gjennom valgte offentlige grenser og bevarer alle 76 posthendelser med original lokator. Ingen ny parserregel eller beløpstolkning er innført. Eksemplene beviser ikke generell uttømmende dekning. Øvrige autentiske ANNET-, Havtil-, 5999-, post-24-, 90-, ny-post- og direktevedtaksprøver gjenbrukes uendret fra B3–B5. Syntetiske testmutasjoner ligger i tester og merkes der.
