# Syntetisk arkiv fra historisk adapter v2

`historical-v2.sql` er en SQLite-dump fra den syntetiske `workbook_bytes`-prøven ved pilotkandidat `5dd4e295e2940b8bd63546ea47f582438cd51e81`, før v3s områdesperre. Den inneholder ingen autentisk arbeidsbok eller interne filstier. Den ble opprettet 21. oktober 2026 med v2-koden. SHA-256 er `d5fe2d681a51f8f80098955305375c49804ae2bfff5a890aab76f7e607d76b0f`, 207 575 byte.

Den offentlige lese-/importprøven gjenåpner uttrekk `7f1fe49e087fb4760eb96cdf54b0268d2ef5968ae59a1b6860adb96f53743c82`, importerer samme kildebyte med v3 og uttrykkelig forgjenger, og kontrollerer uendret gjenlesing av v2 og idempotent v3. SQL klargjør det frosne lagringsgrunnlaget; utfallene kontrolleres gjennom offentlige funksjoner.
