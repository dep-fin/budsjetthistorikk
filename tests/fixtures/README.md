# Autentisk XML-prøve for B1

`40033944.derived.xml` er et bytekopiert utdrag fra sesjonsresponsen 2024–2025, hentet 20. oktober 2026. Prøven inneholder konvolutten og det ene komplette vedtaksobjektet 40033944, nr. 113, sak 100215, datert 13. desember 2024. Budsjettåret er 2025. Den er et historisk testgrunnlag; produksjonsstarten 2026–2027 består.

Dette er et **avledet utdrag**, ikke en komplett HTTP-originalrespons. Sidevognen `40033944.metadata.json` skiller inngangens hash og byteantall fra foreldrekildens. HTTP-headerne i sidevognen kommer fra foreldrefilen og beskriver den komplette HTTP-responsen. Ingen test hevder å ha lagret de 1 259 utelatte vedtakene. Kjøring med en komplett respons bevarer hele responsen i SQLite.

- Kilde: https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025
- Hentet: `2026-10-20T11:34:46.321003+00:00`, HTTP 200.
- Original: 7 479 943 byte, SHA-256 `6d7859369de69105c957cb8dbc520a077355b4c9d4452f1605f7954deccea2ac`.
- Utdrag: 15 214 byte, SHA-256 `043012d31683fb98d53f3c94b649af6d05ef738bdf4cd6bce7e6558103600512`.
- Metode: originalt konvoluttprefiks (317 byte), uendret objektblokk (14 842 byte) og originalt suffix (55 byte), med CRLF og tabulatorer før enkelte linjeslutt. `.gitattributes` beskytter fixturebytene med `-text` og et avgrenset whitespace-unntak for denne filen. Metadatafilen er vanlig UTF-8-tekst med LF.

Med den opprinnelige råfilen og dens `.meta.json` tilgjengelig kan utdraget gjenskapes med `python tests/create_fixture.py <original.raw>`. Skriptet kontrollerer begge hashverdiene og byteantallet før det skriver. Ingen nett- eller forskningsimport utføres.

Den litterale fasiten i `test_b1.py` kommer fra den direkte kontrollerte tabellen og [U1s publiserte API-rapport](../../docs/research/issue-2/api.md#opprinnelig-budsjett-2025). Sju utgiftsposter gir 910 097 000 kroner; én inntektspost gir 300 000 kroner. Totale utgifter/inntekter står i to separate totalrader. Prøven har ingen underposter eller stikkordsfullmakter. Nummerering av `tr` inkluderer tabellhodet.

Avledningene med manglende/tvetydig beløp, ugyldig struktur, XML-entitet og Excel-formel er **syntetiske robusthetsprøver**. De dokumenterer ingen historisk kilderettelse eller feil hos Stortinget.
