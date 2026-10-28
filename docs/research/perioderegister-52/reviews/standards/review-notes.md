# Standards: kontrollnotater

## Omfang og metode

Kun Standards-aksen. Ingen produktskriving, Git-mutasjon, GitHub-skriving
eller ny fullsuite. Egne filer ligger kun i .local/p1-standards.

Kommandoer: `git diff 29ac220f62b35062fc4203f054e2f757ca795b7c 4413a5f21be71ccd2ad5c885560da6bae2e8b885`
og `git log 29ac220f62b35062fc4203f054e2f757ca795b7c..4413a5f21be71ccd2ad5c885560da6bae2e8b885 --oneline`.
Base er direkte forgjenger til kontraktcommitten; to-dot/tre-dot gir samme
endringsomfang. Alle 78 endrede stier er med i evidence-audit.json.

SKILL.md for code-review og writing-for-agents er lest i installert
Matt Pocock-pakke 1.3.1. Dette er delegert Standards-spor; ingen nye
reviewagenter er startet. Komplett issue #52 og den ene kommentaren er
lest gjennom GitHub-koblingen. Memory ble bare brukt til å finne gjeldende
repo-/kildegrenser; alle faktiske reviewkonklusjoner bygger på kandidaten.

## Standardkilder og vurdering

- AGENTS.md: relevante kontekstpekere, norske dokumenter og separate
  faglige statuser. P1s nye peker er kort, har konkrete triggere og peker
  til kontrakt og kontroll. Den kopierer ikke hele kontrakten.
- docs/arbeidsflyt.md: fast kandidat, to uavhengige reviewspor, varige
  kildefunn, dokumentert kontrakt og faktiske testgrenser. Kontrakten har
  egen før-kode-commit; implementeringen utvider den additive grensen.
- docs/agents/issue-tracker.md og docs/agents/domain.md: gjeldende
  issue/kommentarer og felles begrepsapparat. Ingen konkurrerende ordliste
  eller ny etablert definisjon av bevilgningsendring/årsdekning er innført.
- docs/ansvarsdeling.md: nye innlesningsmoduler har ingen analyseimport;
  analyse bruker modellen og adapteren. Ingen nett-/SQLite-avhengighet er
  lagt til i P1-adapteren.
- GLOSSARY.md: regjeringsforslag, komitéforslag, vedtak, fullmakt,
  observasjon og avstemt utvalg beholder separate roller.
- docs/perioderegister.md, docs/fleraarspilot.md og ADR 0011:
  kilde-/objektgjenbruk, immutable modeller, opt-in format, selvforsynt
  rekonstruksjon, analyseansvar og uendret eldre grunnlag.
- K3 README, m21 og neste-snitt samt P1s README, aksept, kildefunn,
  overlevering og reproduksjon: kontrollerbare bevisgrenser. Historiske
  byggestatusformuleringer vurderes på deres oppgitte tidspunkt, ikke som
  påstand om aktuell HEAD eller senere PR-/CI-/mergestatus.
- Søk etter CONTRIBUTING*, CODING_STANDARDS*, AGENTS.md og CLAUDE.md
  fant kun rotens AGENTS.md som ytterligere normativ standardfil.

## Gjennomlest kandidat

Alle linjer i nye produktmoduler, modeller, tester, ops-hjelpere og
supplerende navigasjons-/guardprober er gjennomlest. Katalogens 130
dataoppføringer er kontrollert maskinelt mot kildebyte/baseblobs,
gzip-representasjon og parsebare transportmetadata. Alle endrede JSON-filer
er parsbare og inngår i hashet leveransebevis. JUnit og fullsuiteloggens
slutt er lest, og åtte kjørbare hasher er kontrollert mot den faste Git-
kandidaten. Loggene påstår eksplisitt lokal Windows-kjøring.

Visuelt inspisert eksisterende previews/both/forlop.png,
previews/346/forlop.png og previews/empty/dekning.png. Resterende
renderingsfiler er hashverifisert, ikke individuelt visuelt godkjent her.
Ingen native Excel-aksept påstås.

## Baselineheuristikker

Ett lavt prioritert skjønn er rapportert: Primitive Obsession i den
posisjonsbestemte katalogposten. Navngitt post ville gi tydeligere felt,
men ingen feil eller nødvendig refaktorering er vist.

Ingen andre actionable baselinefunn: navnene uttrykker domene/rolle;
ingen nedarving eller refused bequest; ingen lange fremmede objektkjeder;
ingen ny ubrukt plattformabstraksjon; delegatene utfører kontraktkontroll,
utvalgs- eller filansvar; like JSON-/Excel-prosesser er eksplisitte separate
formatgrenser og gjenbruker eksisterende hjelpere; adapteren strukturerer
ett frosset register. Store struktur-/visningsfunksjoner alene er ikke en
av de pålagte lukteheuristikkene og er ikke gjort til oppfunnet repo-regel.
Data Clumps, Feature Envy, Repeated Switches, Shotgun Surgery og Divergent
Change ga ingen egne funn som forsvarer endring innen dette snittet.

## Egne bevis

`audit_evidence.py` kjøres med den medfølgende Python-runtime; ingen
eksterne Python-avhengigheter trengs. Den skriver bare egne JSON-bevis.
Resultatene er evidence-audit.json, verified-manifest-files.json og
verified-source-catalog.json. Kontrollen viser rent Git-arbeidstre både
før og etter. Fullsuite/statikk er ikke kjørt på nytt, og deres passstatus
er utledet fra de avsluttede, hashverifiserte journalene.
