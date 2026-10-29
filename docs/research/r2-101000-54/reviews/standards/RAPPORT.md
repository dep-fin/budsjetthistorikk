# Standards – samlet review av #54

Fast base: `6b2441ee5e859d103ab44d78f12d33c374a89171`.
Fast kandidat: `7af3153bda95726ac93d0780b918ae95440bae2d`.
Diff: `git diff <base>...<kandidat>`, hele **64 filer**; commits
`c61dcc7` og `7af3153`. Reviewet omfatter også alle råarkiver,
metadata, dokumenter, kontrollresultater og `source-control/verify_sources.py`.

**Dokumenterte standardbrudd: 0.** Standardgrunnlag: AGENTS.md,
docs/arbeidsflyt.md, docs/agents/issue-tracker.md, docs/agents/domain.md,
GLOSSARY.md, docs/ansvarsdeling.md, README.md, pyproject.toml,
.gitattributes, lokal .gitattributes og .github/workflows/check.yml.
Ingen CONTRIBUTING.md, CODING_STANDARDS.md eller separat kodestilfil ble
funnet. Dokumentasjonen er norsk; kildeobservasjon, forslag, vedtak,
fullmakt og faglig godkjenning holdes adskilt. Kildeendringen har varige
pekere i AGENTS/kildefunn. K3/P1, produktkode og fem/elleve er bevart.

**Skjønnsmessig heuristikk: 1, valgfri.** Mulig *Mysterious Name* i
[verify_sources.py, linje 376](../source-control/verify_sources.py#L376):
`pp = embedded(...)`, `dd = embedded(...)`, `rr = committee.xpath(...)`
brukes deretter i `norm(pp) == norm(dd)` og sammenligningen av tilrådingen
(linje 404–406). `proposal_html`, `decision_html` og
`recommendation_section` ville gjort behandlingsleddene lettere å følge.
Dette er ingen dokumentert regel eller leveringsblokkering. Alle tolv
baselineheuristikker er vurdert; ingen andre nyttige funn. Den uavhengige
kildekontrollens gjentatte kontrollfakta bør ikke kobles til byggerens
fasit gjennom felles hjelpeabstraksjoner.

**Utførte kontroller:** [review_checks.py](review_checks.py) binder alle
64 Git-blober til checkoutet, leser samtlige 34 JSON-filer og kontrollerer
dupliserte nøkler/dekomprimering. Den publiserte kildekontrollen består
**204 kontroller**, 27 kildebindinger, to O1-originaler og 60 passasjer;
stabile resultatfelter er identiske med den bevarte kontrollrapporten.
Den publiserte reproduksjonskommandoen består **818 kontroller**, inkludert
59 manifestfiler mot kandidatens Git-blober. Ruff 0.11.0 check/format og
`git diff --check` består. [Resultater](results.json).

**Begrensning:** Offline Standards-review på Windows. Ingen ny HTTP,
visuell PDF-kontroll, full produkttestsuite, Linux-CI, produktadopsjon
eller merge er utført her. Kildekontrollens historiske F1 mot `c61dcc7`
er bevart; kandidatens rettede overskrift samsvarer med råkilden.
