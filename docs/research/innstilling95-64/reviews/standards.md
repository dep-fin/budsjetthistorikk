# Standards-review av T6/#64

Kontrollert 30. oktober 2026. Hele kandidaten er vurdert mot fast base
`9616fbe6a8ab15eec696f34de76888565a784f8f`, head
`fc9b676ce6e2f361433f2562bcdf91930302c21e`, tree
`93fee86f5b117c076136dd95d8d48b32fe1d1316`.
Sammenligning: `git diff 9616fbe6a8ab15eec696f34de76888565a784f8f...fc9b676ce6e2f361433f2562bcdf91930302c21e`.
Én commit: `fc9b676 T6: hele Innst.95S og vedtak359–364 gjennom begge innganger (#64)`.

## Dokumenterte standarder

**0 harde brudd funnet.** Kildene var `AGENTS.md`, `docs/arbeidsflyt.md`,
`docs/ansvarsdeling.md`, `docs/agents/domain.md`, `GLOSSARY.md`,
`pyproject.toml`, `docs/observasjonsformat.md`, `docs/to-visninger.md`,
`docs/visningspilot-plan.md`, T1/T5/T6-kontraktene og ADR 0011.
Ingen `CODING_STANDARDS` eller `CONTRIBUTING` finnes.

Innlesning beholder egen adapter uten analyseimport; analyse eier utvalg,
sammenligning og eksport. Immutable tillegg og én uendret typet T5/T1-kapsel
følger den dokumenterte kontrakten. Gamle produktmoduler, fixtures, schema 5,
B5 og CI er uendret i diffen. Ny kilde-/rolle-/dekningssemantikk er dokumentert.
Verktøyhåndhevet stil og typing er ikke rapportert som manuelle funn.

## Skjønnsmessig smell

**1 mulig Data Clumps, P3, ikke blokkerende:**
`innlesning/innstilling95.py:227–238,373,408,449`.
`_rows` returnerer en åtteleddet tuple:
`tuple[str, str, str, str, tuple[str, ...], tuple[int, ...], html.HtmlElement, html.HtmlElement]`.
Samme radpakke sendes til flere brukere; kontouttrekk bruker
`r[0] + "/" + r[1]`, mens observasjonsbyggingen må pakke ut alle åtte
posisjonene i riktig rekkefølge. Fire str-felt og to HTML-elementer kan
byttes uten at typen avslører betydningsfeilen. En liten intern frozen
radtype med navngitte felter vil gjøre koblingen tydeligere. Dette er en
vedlikeholdsheuristikk, ingen påvist funksjonsfeil eller kontraktendring.
Repoets uttrykkelig godkjente kapselnesting og separate gamle lesere er
ikke flagget som smells.

## Kontroller og begrensninger

HEAD/tree/base ble bekreftet; arbeidskopien var ren før rapporten.
Alle nye produktmoduler, tester, reproduksjonsskript og originaloracle ble
lest; diffens 58 filer og bevaringsgrense ble kontrollert.
`node docs/research/innstilling95-64/independent/oracle.cjs --check` bestod
byteeksakt, SHA-256 `6fd8f0c2fb119771fccff1f61e22785fb9e4ac01fe706723934d2f7d07e473b1`.
Eksisterende 1305 bestått/2 hopp er lest som byggebevis; full suite er ikke
kjørt på nytt. Denne kontrollen erstatter ikke Spec, sikkerhetsaudit,
native Excel eller fersk Linux-CI. Ingen produktkode, staging, commit eller
GitHub-mutasjon er utført.
