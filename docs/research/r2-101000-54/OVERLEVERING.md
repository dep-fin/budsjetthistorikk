# Overlevering – #54 og CI-retting

Leveransen gjelder «R2: Kildeundersøk sak 101000 – lønnsoppgjøret 2024 og
1429/1, /22». Base er `6b2441ee5e859d103ab44d78f12d33c374a89171`, branch
`codex/r2-101000`, isolert checkout `work/r2-101000`. Tidligere arbeidsflater
og pinnede K3/P1-filer er bevart.

[Hovedrapporten](README.md) og [behandlingsledgeren](treatment-ledger.json)
har resultatet: 230 gjelder 1560/71, 231 er generell lønnsregel. Den fulgte
FIN-henvisningen gir et selvstendig /1-kompensasjonsanslag på 2 796 000 i
Prop. 36 vedlegg 4 og overføringsfullmakt 429. Dette er henholdsvis forslag
og fullmakt, uten ny monetær 1429-hendelse. Faktisk fullmaktsbruk og
personell-/avtaleanvendelse er uavklart. /22 arver ingen lønnsforklaring.

Kilde- og bevisgrunnlaget er komplett bevart for det oppgitte hovedsaksutvalget,
med transportmetadata, kilde-/arkivhasher, eksakte lokatorer, egen
[kryssreferansejournal](cross-reference-journal.json) og åpne primærkildegrenser.
Juni-datokonflikten 20./21. juni står synlig. Forskningsledgere er separate
fra produktregisteret; ingen av de øvrige indekskandidatene undersøkes.

## Utført av byggeren

- [Offlinekildekontroll og reproduksjon](reproduksjon.md), med
  [resultat](verification.json) og [manifest](delivery-manifest.json).
- Kontroll mot base av alle endrede sporede filer: bare den nye forskningsmappen
  og korte pekere i AGENTS/kildefunn var tillatt i forskningskandidaten.
  CI-rettingen nedenfor tillater i tillegg bare `checks.timeout-minutes`
  fra 60 til 90 i `.github/workflows/check.yml`. K3/P1, produktkode, tester,
  avhengigheter og P1-kontrakt er uendret. Fem/elleve følger av bevart
  produktgrunnlag; de er ikke nye observerte hendelser fra denne undersøkelsen.
- PDF har fire sider og er tekstkontrollert. Ingen ny PDF-utgivelse,
  native Excel-prøve eller visuell PDF-kontroll påstås.

Byggerens filer inneholder ingen kjørbare forskningsskript eller
produktkode. Engangshjelpere under ignorert `.local/` er bevart lokalt.
Kodeblokken i reproduksjonen er en offlinekommando for fil-/kildekontroll.
Ingen staging, commit, push, PR eller GitHub-mutasjon er gjort av byggeren.

## Retting etter kildekontroll

F1 i [kildekontrollens rapport](reviews/source-control/RAPPORT.md), som gjelder
kandidat `c61dcc7c9221aa485a764c954323e0aac25b9e82`, er rettet i README og
ledgerens `FIN-1429-1`. Begge gjengir nå den faktiske overskriften
«4 Endring av utgifter som følge av lønnsoppgjøret for statsansatte», lest
direkte i `prop36-ch11.html`, `//*[@id='ved4']/h1`. Råkilden, postcellen,
anslagsrollen og tallkonklusjonen er uendret. Kildekontrollens signerte
rapport og tilhørende filer er bevart. På dette byggetrinnet var rettingen
ikke uavhengig etterkontrollert; den senere Spec-kontrollen nedenfor lukker
F1. Byggerens offlinekontroll er kjørt på nytt med oppdatert
resultat og manifest. Full Ruff check og formatkontroll omfatter også
`reviews/source-control/verify_sources.py` og består.

## Orkestratorens leveringsporter

Portene og sluttmanifestet i dette avsnittet beskriver før-PR-trinnet
28. oktober. De beholdes som historikk; CI-rettingen har eget manifest.

Alle kontrollporter før PR er bestått. De tre rapportene gjelder hele den
faste forskningskandidaten `7af3153bda95726ac93d0780b918ae95440bae2d`
mot oppgitt base, inkludert kildekontrollens skript og alle 64 kandidatfiler:

- [Standards](reviews/standards/RAPPORT.md): 0 dokumenterte standardbrudd,
  én valgfri navneheuristikk. Publisert kildekontroll: 204 bestått;
  publisert reproduksjon: 818 bestått, med 59 Git-blobkontroller.
- [Spec og F1-etterkontroll](reviews/spec/RAPPORT.md): 0 nødvendige og
  0 valgfrie funn; F1 lukket mot hashbundet råoverskrift. Egen etterkontroll:
  274 bestått. Hovedsak, presisjon, roller og restgrenser er kontrollert.
- [Separat sikkerhetsaudit](reviews/security/REPORT.md): 0 nødvendige
  rettinger, to valgfrie forbedringer om generell dekomprimeringsherding
  og dataminimering ved senere innhenting. 696 beståtte kontrollpunkter.

De nye reviewartefaktene er deretter kontrollert særskilt for standarder,
sikkerhet, referanser og kandidatbinding. Ruff check/format består for alle
fem nye Python-filer. Gjenkjøringer skriver til separat lokal resultatmappe;
de opprinnelige rapportene og resultatene er bevart. En ufarlig aliasering
i sikkerhetskontrollens detaljfelt er presisert i
[sluttkontrollen](reviews/final-artifacts/RAPPORT.md), uten endret auditutfall.

[Publikasjonsmanifestet](reviews/final-artifacts/publication-manifest.json)
binder samlet filinventar, inkludert `reviews/**` og AGENTS/kildefunn i
Git-LF-representasjon. Manifestet og sluttkontrollrapporten er uttrykkelig
utelatt fra egen filliste for å unngå sirkulær binding; rapporten oppgir
manifestets SHA-256. `delivery-manifest.json` gjaldt bare byggerens filer og
ble i før-PR-trinnet oppdatert kun for overleveringen og samlet byteantall.
Det historiske `verification.json` og alle kildebevis er uendret.

Før-PR-tillegget består av denne statusoppdateringen, byggermanifestet,
de tre reviewmappene og sluttkontrollen. Det endrer ingen kilde, faglig
påstand eller produktfil i den kontrollerte forskningskandidaten. Manifestet
angir filbyte før commit; faktiske Git-blobbyte for hele den endelige
publikasjonsrevisjonen må kontrolleres etter commit.

PR #55 er opprettet på head `a5cb97cb4f825e1ce338f4d698a6b4425e9ed0c1`.
Den første fulle Linux-CI-en fikk tidsavbrudd. Ny full CI med bare den
avgrensede timeoutendringen og bekreftet merge gjenstår hos orkestratoren.
Lokale forskningskontroller er ikke full produkttestsuite eller CI.
Faktisk PR-/CI-/mergestatus lagres i GitHub før #54 lukkes.

Positiv M21, full årsdekning, kontokontinuitet, faglig årsbalanse,
produktadopsjon og drift inngår ikke. #10/#32/#37 står åpne.
Avslutt etter denne ticketen; ingen neste ticket er bestilt.

## CI-retting 29. oktober 2026

[Recoverygrunnlaget](ci-recovery/README.md) binder serverannotasjon,
jobbstatus, loggutdrag, URL-er, head/merge-SHA-er og historiske filhasher.
Jobb 123114666144 i run 40772943242 ble avbrutt ved 60-minuttersgrensen;
1105 av 1201 tester hadde bestått uten registrert testfeil. De siste 96
har ingen sluttstatus. Ruff check/format og mypy bestod på den gamle headen.

Den eneste endringen i workflowen er `timeout-minutes: 60` til `90`.
Alle kontrollsteg og hele `python -m pytest -vv --durations=20` beholdes.
Ingen lokal full pytest-kjøring, ny review/audit, staging, commit, push,
GitHub-mutasjon eller merge er utført i denne rettingsrunden. Implement-
filinstruksjonen er lest; review-/commit-trinnene er uttrykkelig overlatt
eller utelatt etter rettingsmandatet. Full CI må bestå på ny publisert head.

`reviews/**` og det gamle `verification.json` beholdes som historiske
bevis for deres oppgitte kandidater. De attesterer ikke timeoutendringen.
Nye/endrede filer bindes av [recoverymanifestet](ci-recovery/recovery-manifest.json).
Byggermanifestet oppdateres for README, denne overleveringen og reproduksjonen;
tidligere manifesthash og tidligere filhasher bevares i recoverygrunnlaget.
