# Syntetisk arkiv fra historisk adapter v1

`historical-v1.sql` er en lokal SQLite-dump fra den syntetiske `workbook_bytes`-prøven ved pilotkandidat `d6b0ea1f06b30d99d919bbf901f7547c9d1144fb`, før v2-rettingene. Den inneholder ingen autentisk arbeidsbok eller interne filstier. ZIP-originalen i dumpen er utelukkende syntetisk. Arkivet ble opprettet 21. oktober 2026 med v1-koden, ikke beregnet fra forventet v2-resultat.

Den offentlige lese-/importprøven gjenåpner uttrekk `7875b8bafed25b14dd8fe5072ec72ff744168d20e3fa2dc15232032302fffe11`, importerer samme kildebyte med v2 og uttrykkelig forgjenger, og kontrollerer uendret gjenlesing av v1 og idempotent v2. SQL brukes bare til å klargjøre det frosne lagringsgrunnlaget, ikke til å kontrollere produktets utfall.
