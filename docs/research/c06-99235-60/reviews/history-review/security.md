# Separat sikkerhetsaudit av C06-kandidaten med transportabel historikk

**Sikkerhetsport: klar på den faste kandidaten nedenfor. Ingen nødvendige
sikkerhetsrettinger.** Antall funn: P0 = 0, P1 = 0, P2 = 0, P3 = 0.
Dette er en selvstendig vurdering av hele endringen fra U1-basen, med egne
kjøringer av portabilitetsdeltaet og relevante tidligere sikkerhetskontroller.

Kontrollert 29. oktober 2026:

| Binding | Eksakt verdi |
| --- | --- |
| Base | `49cc6e44851cf74e0aaea4eb333419e5598bfd95` |
| Fast kandidat | `6204702d5da0ade04f368a6fb4a7b39b73df011a` |
| Kandidatens Git-tre | `79ea3e464984d7ad0aaca55669a68ab0fd0ad96c` |
| Opprinnelig sikkerhetskandidat | `9eb27cebf7ca4a99aeb30fa32245e41314e0d295` |
| Etterkontrollert kandidat | `d241ad8f36f70718dbc54d3093c151d301d04f30` |
| Lokal sluttkandidat før portabilitetsrettingen | `9efa1f7b67e4ad5b2722b6a6604591af281e4e9c` |
| Publisert forutsetning | `92b43c2ce7ec350e10639bd0c75540da0d83ee72` |

AGENTS, arbeidsflyten, issue-tracker, [kontrakten](../../contract.md), live
[#60 med begge kommentarer](https://github.com/depmartin/budsjetthistorikk/issues/60),
U1s S1, de fire opprinnelige C06-portene, integrasjonsbeviset,
[etterkontrollen](../final-check.md) og [historikkpakken](../history/README.md)
er lest som mandat og bevisgrunnlag. Historiske attester er ikke tatt som
automatisk attest på 620-kandidaten.

## Hele endringen og bevarte forutsetninger

Hele basediffen omfatter 109 vanlige filer: to tillatte dokumentpekere og
C06-pakken. Alle 109 arbeidsfiler er sammenlignet med kandidatens faktiske
Git-blobbyte, før og etter prøvene. Bare AGENTS/kildefunn bruker uttrykkelig
LF-representasjon i denne sammenligningen. Alle 1 070 beskyttede basefiler
har uendret Git-blob og filmodus. Det omfatter pinnede K3/P1/R2/P2/U1,
produktkode, tester, CI med 90 minutter, schema 5/B5, gamle lesere,
formater, ID-er og standardvalg. Fem monetære hendelser/elleve vedtaksfelt,
67/66, 60/59, 25 vedtakskandidater og R1–R7 påvirkes ikke av rettingen.

Mot 9eb er 1 138 filer uendret. Den eneste endringen i
`cross-reference-journal.json` er den eksakte J02-erstatningen 14 → 18.
Standards-helperens AST er sammenlignet med den bevarte originalen og er
identisk. Mot 9efa har portabilitetsrettingen nøyaktig 19 stier: seks
dokument-/manifestfiler og 13 nye historikkfiler. De øvrige 1 160 filene
er uendret. Fire dokumenter bevarer hele den tidligere byteprefiksen.
Kildeoriginaler, OCR, bildeinventar, øvrige faglige avledninger og
opprinnelige review-/etterkontrollbevis er bevart.

## Bundle og objektlukning

Bundlen er uavhengig kontrollert til **22 554 byte**, SHA-256
`051ca0279fb61b5ddd3b77a83c09f172c8ac142e1cd2240dfac6fdca2ab7074d`.
Headeren har nøyaktig versjon 2, prerequisites 49cc og 92b, og bare refen
`refs/c06-history/candidates` med verdien 9efa. Pack-delen har versjon 2,
18 objekter, korrekt avsluttende Git-SHA-1 og SHA-256
`a6dfa0c03889cffbbcc4d858ceb55fa7a1c10c8f2a75be5d191e806d308ad4ad`.

En egen disponibel Git-repo under ignorert `.local` fikk først bare
objektene som er nåbare fra base 49cc. `git bundle verify` avviste da
bundlen med den manglende 92b-forutsetningen. Etter tilførsel av bare
92bs nåbare tillegg manglet fortsatt alle tre historiske commitobjekter.
Ingen alternates var konfigurert. Bundleimport gjenopprettet de tre
eksakte rå commitobjektene og trærne; HEAD var uendret, bare den oppgitte
administrative refen ble tilført, og full `git fsck --full --no-reflogs`
bestod.

Den faktiske pack-inventaren er dekodet med Git, og alle 18 objekter er
sammenlignet med `object-inventory.json`, type, gjenopprettet størrelse og
egen rå objekt-SHA-1. Resultatet er tre committer, ni trær og seks små
UTF-8-tekstblobber, største 17 399 byte. Objektsettet er identisk med
`git rev-list --objects 9efa... ^92b... ^92b...^{tree}`. Ingen ekstra
PDF- eller kjørbar blob følger med; de seks tekstblobbene er eldre
versjoner av de oppgitte C06-dokumentene og manifestene.

Dette er en thin pack: enkelte deltaer trenger allerede tilgjengelige
baseobjekter. Den separate strenge pack-kontrollen brukte derfor
`index-pack --strict --stdin --fix-thin`; størrelser ble lest fra de
gjenopprettede objektene, ikke fra deltaprogrammenes lengder.
Den opprinnelige bundlefilens pack-byte ble ikke endret. Den håndskrevne
ekstra prerequisite-linjen endrer dermed ingen Git-objektidentitet;
den gjør en reell ekstern objektforutsetning uttrykkelig.

## Ny helper, referanser og utdata

[create_bundle.py:36–60](../history/create_bundle.py#L36) kontrollerer de
fire faste committenes trær/foreldre og oppretter en manglende lokal ref
med forventet gammel nullverdi. Opprydding i `finally` krever den forventede
kandidatverdien. En eksisterende ref med samme verdi beholdes, mens en
annen verdi avvises før bundleoppretting. Egne kjøringer i den disponible
repoen viste:

- Identisk eksisterende ref: identiske bundlebyte og uendret refsett.
- Manglende ref: identiske bundlebyte; midlertidig ref ryddet bort.
- Avvikende eksisterende ref: avvisning; refsett og bundlebyte uendret.
- Simulert feil i native bundleoppretting: feilen videreføres, riktig
  oppryddingskommando kjøres og ingen tidligere bundlebyte endres.

[Linje 16–17/38–39](../history/create_bundle.py#L16) bruker Git-argv uten
shell. Committer, ref, kommandoer og utfil er faste lokale verdier;
HTTP-/OCR-tekst, bundleheader eller manifestfelt blir ikke shellkode,
Git-opsjoner eller valgte utstier. [Linje 47–56](../history/create_bundle.py#L47)
skriver bare den avtalte bundlefilen under repoets historikkmappe.
[Linje 61–72](../history/create_bundle.py#L61) sjekker den native headeren,
bevarer pack-delen og verifiserer resultatet med Git.

Regenerering er et uttrykkelig lokalt vedlikeholdssteg som overskriver
denne ene bundlefilen. Det er fortsatt reviewet lokal repo-/operatørinput,
uten en ny tjeneste for vilkårlige angriperstyrte manifester, utstier eller
Git-konfigurasjoner. De prøvde refverdiene er vanlige direkte refs i den
avtalte lokale arbeidsflyten. Kildecheckoutens HEAD, refsett og indeks
var uendret gjennom prøvene; ingen branch ble flyttet der.

## Tidligere sikkerhetsgrenser, manifester og hemmeligheter

Den uendrede historiske sikkerhetshelperen ble kjørt på nytt på fast 9eb
i den disponible repoen: **3 776 kontroller, 0 feil**. Hele resultatobjektet
er identisk med den bevarte attesten bortsett fra `checked_utc`.
Det gjentar blant annet negative start-/redirectprøver, urllibs faktiske
redirect-stack med falsk HTTPS-transport og blokkerte sockets, feil- og
delbytebevaring, XML-entitetsvern, bilde-/PDF-kontroll, manifestmanipulasjon,
utstier og regenerering i minnet. Dette er mekanisk reproduksjon av
sikkerhetskontroller; det er ingen ny manuell tarifflesing.

[acquire.py:31–43/139–145](../../acquire.py#L31) er uendret og håndhever
de tre eksakte HTTPS-vertene før første forespørsel og hvert redirectmål.
U1s S1 er fortsatt håndtert i C06-helperen. De ni egne transporttestene
bestod også ved separat kjøring i den aktuelle checkouten.

Alle 39 bindinger i historikkmanifestets tre fillister er kontrollert mot
faste kandidatblobber; alle 21 oppgitte gamle review-blob-ID-er stemmer.
Relative stier holder seg innen sine oppgitte røtter. Historikkinventaret
har nøyaktig 12 filer, 153 861 byte, og utelater seg selv. De fire originale
resultatobjektenes kanoniske hasher i `replay-comparison.json` er beregnet
på nytt og stemmer. Command-loggen bevarer både feilforsøk og etterfølgende
vellykkede kjøringer; den behandles som data, ikke som kjørbare instruksjoner.

Leveransemanifestet utelater fortsatt `reviews/**`. Den nye rapporten
inngår derfor ikke i eldre attester eller selvhashbindinger. Kandidat-SHA
og uavhengig blobkontroll skiller denne bindingen fra en selvkonsekvent
senere omskriving av filer og manifester.

Sterke avgrensede mønstre for GitHub-token, AWS-nøkkel, privat nøkkel og
Authorization/Bearer ga ingen treff i alle 109 kandidatfiler og de 18
gjenopprettede pack-objektene. Den gjentatte gamle auditen dekker også
dekomprimerte originaler/OCR. Ingen ny nettforespørsel, opplasting,
utsending, produktdatabase eller ekstern autentisering er innført.
Mønstersøk er ingen uttømmende hemmelighetsdetektor.

## Egne kjøringer og bevisgrense

| Utført kontroll | Resultat |
| --- | --- |
| Eget supplerende probeprogram, inkludert hele blob-/bevaringsgrensen, objektlukning, import og negative helperprøver | 4 126 kontroller, 0 feil |
| Uendret historisk sikkerhetshelper i disponibel 9eb-checkout | 3 776 kontroller, resultat identisk utenom tidspunkt |
| `verify.py 6204702d5da0ade04f368a6fb4a7b39b73df011a` | 3 349 kontroller, 0 feil, inklusive alle 73 leveranseblobber |
| `test_acquire.py` | Ni offlineprøver, bestått |
| `reviews/integration/verify_integration.py`, uten utdataargument | 15 originalfiler, identisk Standards-AST/-utfall, 1 138 uendrede filer, 0 feil |
| Historikkmanifestets fullstendighet/total og fire kanoniske opprinnelige resultathasher | Bestått |

Kjøringene brukte Python 3.12.14 fra oppgitt Codex-runtime,
`PYTHONPATH=.local/python-tools`, `PYTHONDONTWRITEBYTECODE=1` og
`PYTHONIOENCODING=utf-8`, samt Git 2.55.0.windows.3.
Eget probeprogram og råresultater ligger bare i ignorert `.local`.
Ingen ny executable, kandidatendring eller manifestendring er levert.

Et første forsøk på lokal Git-fetch ble stanset av sandboxens MSYS-
objekttilgang. Den egne disponible repoen ble derfor forsynt med native
`pack-objects --revs --stdout` og `index-pack --strict --stdin` for bare
de oppgitte prerequisite-committenes nåbare objekter. Den faktiske
bundleimporten brukte den dokumenterte `git fetch --no-tags`-refspecen.
Denne auditen har ikke utført en ny GitHub-kloning. Det tidligere
GitHub-fersk-klon-beviset er lest, hashkontrollert og avgrenset som en
tidligere kjøreobservasjon; egen objektisolasjon/import er et separat bevis.

Kommandoene for historisk reproduksjon står i
[historikkpakken](../history/README.md#kontroll-og-gjenoppretting-fra-en-vilkårlig-klonrot).
Regenereringsprøver og historiske hjelpere som skriver reviewutdata må
fortsatt kjøres i en disponibel klon. Ordinær nåtidskontroll av denne
kandidaten kan gjentas fra repoets rot med `verify.py <SHA>`,
`test_acquire.py` og integrasjonshelperen uten utdataargument.

Git-kontroll viser at **92b ikke er ancestor til lokal 620**; 620 har
9efa som forelder. Den kommende publiserte headen må derfor fortsatt
bevare 92b som faktisk ancestor, slik historikkpakken krever. Dette er
en uttrykkelig gjenstående publiseringsforutsetning, ingen påstand om
at den er oppfylt av denne lokale kandidaten.

Ingen full produkttestsuite, Linux-CI, ny kildehenting, WinRT-OCR, ny visuell
lesing, generell bibliotek-/OS-sårbarhetsskann, publisering eller merge er
utført eller godkjent her. Tidligere grenser for lokale hashbundne arkiver,
reviewede manifester og lokal operatørtilgang består. **Sikkerhetsporten
for den eksakte 620-kandidaten er klar**; faktisk publisert head/ancestry,
øvrige porter og full uendret CI ligger fortsatt hos orkestratoren.
