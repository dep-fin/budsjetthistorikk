# Syntetisk arkivprøve for beregningsregel v1

`synthetic-history-v1.json` er et lagret beregningsresultat fra den leverte
B3-implementasjonen ved `ac8d4e4c0785a74e77efdf67fef590a798a059c1`, kjørt
20. oktober 2026. Det er ingen autentisk kilde eller importert arbeidsbok.

Reproduksjon: bruk `test_b3.generic` med `date="2013-01-01"`, `subpost=None`
og `detail="post"`. Legg til uttrekksavviket
`Anomaly("mangler_organisasjonsoppslag", "Unresolved mapping", chapter="1",
post="1", budget_year=2013)` og lagre i en ny database. Kjør den uendrede
`analyse/history.py` fra B3-revisjonen over et `HistorySelection` med datasett
`historisk`, dette uttrekket, år 2013, kapittel `1` og post `1`. JSON-filen
inneholder det opprinnelig lagrede resultatet; tidspunktet er bevart.

Fasit er `vedtatt-kjede-v1`, ID
`ad24cc3a988e38f2612e692f1cb2ff6fd17a3e6822f5786af86b9a50a195fc09`,
`ufullstendig` og ingen beregnet saldo. Testen prøver både ny beregning og
gjenåpning/gjentatt beregning med dette resultatet allerede lagret. Dermed kan
ikke `INSERT OR IGNORE` skjule en endret regneregel under samme identitet.
