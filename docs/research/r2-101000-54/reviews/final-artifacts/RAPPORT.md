# Sluttkontroll av kontrollartefakter og publikasjonsbinding – #54

Målrettet kontroll av kontrollartefaktene før PR, 28. oktober 2026.
Forskningskandidaten er `7af3153bda95726ac93d0780b918ae95440bae2d`,
mot base `6b2441ee5e859d103ab44d78f12d33c374a89171`.
Denne kontrollen endrer ingen kildetolkning eller produktfil.

**Resultat: ingen nødvendige standard- eller sikkerhetsrettinger i de nye
kontrollartefaktene. Alle kontrollporter før PR består.** Én ufarlig
inkonsistens i et detaljfelt er presisert nedenfor. PR, Linux-CI og merge
er fortsatt ikke utført.

## Omfang og kandidatbinding

Kontrollen omfatter de 18 nye filene under `reviews/standards`,
`reviews/spec` og `reviews/security`, og deres bindinger til de fire
historiske `reviews/source-control`-filene. Alle 22 kontrollartefakter er
lest, inkludert 12 JSON-filer og fem Python-filer. Ingen av disse 22
filene er endret under sluttkontrollen.

De tre uavhengige vurderingene er
[Standards](../standards/RAPPORT.md), [Spec](../spec/RAPPORT.md) og
[sikkerhetsaudit](../security/REPORT.md). Alle tre inventarene dekker de
samme 64 filene. Størrelse og SHA-256 i hvert inventar er kontrollert mot
faktiske Git-blober i `7af3153`; base, HEAD og kandidatens tre
`ab1ff41bb3c9ea7ee310418abec82efcbe6d00c0` stemmer. De eksplisitte
skripthashene i Standards-, sikkerhets- og kildekontrollresultatene
samsvarer med de publiserte skriptene. Historisk kildekontroll mot
`c61dcc7` og senere F1-lukking beholdes som separate kontrolltrinn.

Alle JSON-filer i kontrollartefaktene har unike nøkler og kan leses.
Relative dokumentlenker løser til eksisterende filer. Spec-sporets
formaterte `replay_builder_check.py` har identisk Python-AST med den
publiserte kodeblokken i `reproduksjon.md`. Ingen lenke eller rapport
brukes som bevis på gjennomført CI eller merge.

## Sikkerhets- og standardkontroll

Alle fem skript er gjennomgått for filbaner, skriving, parserbruk,
prosesskall, nettverk og dynamisk kjøring. De leser det frosne offentlige
grunnlaget og bruker argumentlister til Git-lesekommandoer. Standards
kjører den faste, blobkontrollerte reproduksjonsblokken med `exec`;
sikkerhetssporet laster det faste kildekontrollskriptet med `runpy`.
Dette er kjøring av den kontrollerte lokale koden, ikke kjøring av tekst
fra råkildene. HTML/XML/PDF-innhold går til parsere og sammenligninger.
Ingen produktimport, ny nettinnhenting eller manifeststyrt skrivebane er
funnet i disse inngangene. De nye skriptenes resultatbaner ligger i egne
kontrollmapper; reproduksjonsskriptet skriver bare til standard output.

De tre nye kontrollinngangene er faktisk kjørt på nytt før statusendringen,
med bare resultatkonstanten `HERE` omdirigert til hver sin katalog under
ignorert `.local/final-artifacts-replay/`. Spec-sporets tre lagrede
kontrollinnganger ble kopiert dit uten endring. Den kontrollerte
skriptkoden og forskningskandidatens filer var uendret under kjøringen.
Sikkerhetsauditens prosess- og nettverkssperrer var aktive i sin gjenkjøring.

- Standards-gjenkjøring: 64 kandidatfiler, 204 kildekontroller og 818
  reproduksjonskontroller, inkludert 59 faktiske Git-blobkontroller.
- Spec-gjenkjøring: 274 beståtte kontroller, F1 fortsatt lukket.
- Sikkerhetsgjenkjøring: 696 beståtte kontrollpunkter, ingen feil.
- Egen artefaktkontroll: 271 beståtte kontroller av inventarer, tre
  kandidatbindinger, skripthasher, referanser, JSON og resultatkonsistens.
- Ruff 0.11.0 check og formatkontroll: alle fem Python-filer består.
  `git diff --check` mot basen består. Ingen formattering var nødvendig.

Ruff ble kjørt fra P1s eksisterende `.local/python/bin/ruff.exe`.
Første forsøk gjennom P1s venv uten modulsti fant ikke Ruff og er ikke
telt som bestått. Parserkjøringene brukte bundlet Python 3.12.14,
lxml 6.1.1 og pypdf 6.10.0. Ingen installasjon eller oppgradering er gjort.

## C1 – presisering av sikkerhetskontrollens detaljfelt

I `reviews/security/checks.json` viser detaljfeltet for
`rerun only writes redirected results` både `results.json` og
`candidate.json`. Dette er en referanse til den samme mutable listen
`io_events`: testen kjøres mens listen bare inneholder `results.json`,
og auditens senere egen skriving av `candidate.json` utvider listen før
den serialiseres. Detaljfeltet er derfor ikke et tidsavgrenset snapshot.

Det separate feltet `source_control_rerun_writes` inneholder korrekt bare
`results.json`. Den ferske gjenkjøringen bekreftet begge observasjonene.
Dette endrer ingen kontrollbetingelse, kandidatbinding eller auditutfall.
Denne sluttrapporten og overleveringen presiserer den riktige lesningen;
originalskriptet og de historiske, signerte resultatene er bevart. Ved en
senere redigering kan detaljfeltet fryses med `io_events.copy()`.

Standards-sporets ene valgfrie navneheuristikk og sikkerhetssporets to
valgfrie forbedringer om generell dekomprimeringsherding og dataminimering
beholder sine opprinnelige statuser. Ingen av dem er gjort om til en
nødvendig retting av denne kildeundersøkelsen.

## Endelig status og publikasjonsmanifest

Etter kontrollene ble bare `OVERLEVERING.md` oppdatert for faktisk
før-PR-status og tydelige rapportlenker. `delivery-manifest.json` ble
oppdatert bare i overleveringens filrad og `total_bytes`. Alle øvrige
byggermanifestfelt, de 44 nye original-/metadatafilene, kildebevisene,
alle 22 kontrollartefakter, K3/P1, produkt/test/CI og pinnefiler er uendret.

Den publiserte reproduksjonsblokken ble deretter hentet direkte fra
`reproduksjon.md` og kjørt mot de endelige arbeidsfilene uten revisjonsargument:
**764 beståtte kontroller, 0 feil**, inkludert 59 byggermanifestfiler og
128 lokale lenkemål. Den er også tilgjengelig som AST-identisk publisert
skript:

```powershell
python -B -X utf8 docs/research/r2-101000-54/reviews/spec/replay_builder_check.py
```

764 gjelder arbeidsfilene etter denne statusoppdateringen. Historiske
818 gjelder forskningskandidaten og inkluderer 59 Git-blobkontroller.
Den endelige publikasjonsrevisjonen er ennå ikke committet; kontroll av
dens faktiske Git-blober må kjøres etter commit med full revisjons-SHA.

[publication-manifest.json](publication-manifest.json) binder **82 filer**,
samlet **3 444 869 byte** i oppgitte representasjoner. Hele det endrede og
nye publikasjonsinventaret mot basen er med, inkludert `reviews/**` og
AGENTS/kildefunn i uttrykkelig UTF-8/LF. Resten bindes som eksakte filbyte.
Ingen råkilde er normalisert. Alle 82 forventede Git-blob-ID-er er også
kontrollert med `git hash-object --path=... --stdin`, uten `-w`; dette
skriver ingen Git-objekter og viser hvilke byte gjeldende Git-filtre ville
publisere. Det erstatter ikke kontrollen av den senere committen.

Bare manifestet selv og denne rapporten er uttrykkelig utelatt fra
manifestets filliste for å unngå sirkulær binding. Manifestets SHA-256 er:

```text
81f49a1671d706a32130180c509c369ff6539e87bbe51c1fb0ccfe67328d0c92
```

Første etterkjøring av reproduksjonen skjedde før rapportfilen var opprettet
og stoppet korrekt på et manglende lenkemål. Det forsøket er ikke telt som
bestått; kjøringen med alle endelige lenkemål ga resultatet ovenfor.

Ingen staging, commit, push, PR eller GitHub-mutasjon er gjort her. Ingen
ny produkttestsuite, visuell PDF-kontroll, native Excel-prøve, kildeautentisering
gjennom ny HTTP, generell parserfuzzing eller isolasjon av native bibliotek
er utført. Faktisk 231/429-anvendelse, juni-datokonflikten, øvrige R1–R7,
positiv M21, årsdekning, kontokontinuitet, faglig årsbalanse og drift
beholder de dokumenterte grensene. Full Linux-CI og bekreftet merge gjenstår.
