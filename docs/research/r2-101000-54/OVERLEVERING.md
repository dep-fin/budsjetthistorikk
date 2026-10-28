# Overlevering – byggerens kandidat for #54

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
  og korte pekere i AGENTS/kildefunn er tillatt. K3/P1, produktkode, tester,
  CI-konfigurasjon og P1-kontrakt er uendret. Fem/elleve følger av bevart
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
rapport og tilhørende filer er bevart; rettingen er ingen ny uavhengig
etterkontroll. Byggerens offlinekontroll er kjørt på nytt med oppdatert
resultat og manifest. Full Ruff check og formatkontroll omfatter også
`reviews/source-control/verify_sources.py` og består.

## Orkestratorens leveringsporter

Uavhengig kildekontroll og endelig vurdering av dokument-/kildedata skal
bindes til samlet fast kandidat. Kontrollagentens `reviews/source-control/`
eies av den agenten; byggeren har ikke endret disse filene.
`delivery-manifest.json` gjelder byggerens filer og utelater `reviews/**`.
Eventuelle publiserte kontrollskript i `reviews/**` må inngå i orkestratorens
vurdering av samlet review-/auditplikt for hele kandidaten.
Etter eventuelle rettinger/rapporter oppdaterer orkestratoren manifestet
og kontrollerer faktiske Git-blobbyte på den publiserte revisjonen.

Full uendret Linux-CI og bekreftet merge gjenstår hos orkestratoren.
Lokale forskningskontroller er ikke full produkttestsuite eller CI.
Faktisk PR-/CI-/mergestatus lagres i GitHub før #54 lukkes.

Positiv M21, full årsdekning, kontokontinuitet, faglig årsbalanse,
produktadopsjon og drift inngår ikke. #10/#32/#37 står åpne.
Avslutt etter denne ticketen; ingen neste ticket er bestilt.
