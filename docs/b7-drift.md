# B7: daglig innlesning og senere Windows-drift

Kodeleveransen kan kontrolleres deterministisk og konfigureres for en varig Windows-vert med lokal lagring. Eieren valgte denne plattformen 21. oktober 2026, men utsatte valg av vert, driftskonto, datamappe og eksisterende bakgrunnstilgang. Oppgaveinstallasjon og faktisk driftsprøve er derfor **ikke utført**. Kode, generert scheduler-XML og simulerte tidspunkter oppfyller ikke akseptkravet om demonstrert daglig kjøring i avtalt miljø. #10 skal stå åpen til dette er gjort.

## Konfigurasjon og kjøring

Kopier [eksempelet](../ops/daily.example.json) til en avtalt lokal konfigurasjonsfil. Bytt alle `AVKLARES`-baner. `register_snapshot` er en eksakt, eksisterende tolkning, ikke et automatisk «siste» register. Eksempelet viser det avgrensede innebygde 2027-grunnlaget, med de tidligere dokumenterte kildebegrensningene. Bruk en manuelt vedlikeholdt snapshot-ID når den er avtalt. Et ikke-null `control_basis` bruker bare allerede aktive, eksakt samsvarende B5-bindinger. Det aktiverer eller godkjenner ingenting.

```powershell
python -m pip install -r requirements.txt
python -m drift --config C:\avtalt\daily.json --next-due
python -m drift --config C:\avtalt\daily.json
python -m drift --config C:\avtalt\daily.json --status
```

Kjør fra repoets faste installasjonsmappe med en eksplisitt Python 3.12-runtime. Konfigurasjonen krever absolutte database-/rapportbaner, fast autorisert GitHub-repo `depmartin/budsjetthistorikk`, `dataset=produksjon` og `first_session=2026-2027`. Prøver bruker en separat database og `dataset=prove`; tidligere prøvegrense kan velges der. Ukjente felter og ukjente fremtidige databaseskjema avvises. Konfigurasjonen fryses per dato; endring samme dato krever en uttrykkelig ny pipeline-ID. Samme database har likevel bare én driftsprosess om gangen.

Returkode 0 betyr utført teknisk jobb eller ikke forfalt, med ingen ventende varsling. Kode 1 betyr kilde-/behandlings-/rapportfeil eller ventende levering; kode 2 betyr avvist overlapp. Faglige kontrollbehov fremgår særskilt og gir ikke alene en innlesningsfeil. CLI viser maskinlesbar JSON. Kjørerapporten i SQLite og den nye JSON-filen skiller:

- `source_changes`: ny, rettelse, uendret og mangler i faktisk observerte inventarer.
- `outcome`: full, partial eller failed; «ingen nye» sier ingenting om feil eller kontrollbehov.
- `control_needs`: stabile avviksforhold for denne datojobben, med separat B6-dekning.
- `delivery`: ingen_avvik, levert eller venter; GitHub-feil endrer ikke lagrede kilder.
- Eksakte jobber, frosne rapport-ID-er og nye Excel-filer. Rå, historisk effektive og aktuelle godkjente beløp vises separat. Ingen helsesjons-/årsgodkjenning innføres.

Den opprinnelige JSON-filen er et immutable forsøkssnapshot før GitHub-levering. Leveringskvitteringen vises i returverdien og SQLite/`--status`; den gamle filen overskrives ikke. Feil ved publisering av JSON-filen lagres som `kjorerapport_fil_feilet` og et stabilt outboxvarsel før levering. SQLite bevarer kjørerapporten også når JSON-filen ikke kunne skrives. Filpubliseringen prøves én gang per prosessforsøk, og gjenopptak bruker samme avviksnøkkel.

Datoer før første start rekonstrueres ikke, med mindre `first_date` eksplisitt angir når driftsansvaret begynte. Uteblitte datoer etter dette registreres uten fiktive hentetider. Før kl. 06 gjøres ingen kildehenting. En forsinket start etter kl. 06 henter dagens kilde. Alle startede sesjoner fra 2026–2027 beholdes i den daglige kontrollen, også etter sesjonsslutt. Sesjonslisten hentes fra den faste [offisielle URL-en](https://data.stortinget.no/eksport/sesjoner); [kildedokumentasjonen](https://data.stortinget.no/dokumentasjon-og-hjelp/sesjoner/) sier uttrykkelig at fremtidige sesjoner kan ligge i listen.

Daglig omfang er unionen av katalogens startede sesjoner og tidligere kjente kontrollerte sesjoner i datasettet, fra konfigurert startsesjon. En tidligere kjent sesjon som mangler i en ellers gyldig katalog, hentes fortsatt og beholdes i B6/Excel. Kjørerapporten får `sesjon_mangler_i_katalog:<sesjon>`, `outcome=partial` og et stabilt varsel for den aktuelle sesjonen, også ved gjentatt forsøk samme dato. Katalogfraværet betyr ikke at de separat hentede vedtaksinventarene mangler kildeinnhold; B6-dekningen vurderer disse inventarene på vanlig måte. Fremtidige katalogperioder tas fortsatt ikke inn før de har startet.

## Forbered avtalt Windows-vert

Gjør disse punktene når eieren har valgt vert/konto/lager. De er ikke utført av kodeleveransen:

1. Registrer vertens navn, avtalt driftsansvarlig, eksisterende Windows-konto, fast lokal database-/rapportbane og backupplassering. Én kanonisk databasebane; ingen UNC, nettverksdisk, hardlinkalias, synkronisert mappe eller flere samtidige verter.
2. Bekreft `W. Europe Standard Time`, riktig systemklokke, varig strøm/nettverk og Task Scheduler-tilgang. Skriptet endrer ingen vertsinnstillinger. Tidligere read-only CIM-spørringer i utviklingsmiljøet feilet med tilgang/nettverksadresse; dette beviser ikke at en oppgave mangler eller kan installeres.
3. Installer låste Python-avhengigheter i vertens runtime. Sikre filrettigheter: driftskontoen skal kunne lese kode/konfigurasjon, og skrive database, tilhørende journal-/låsefiler og rapportmappe. Begrens andres skrivetilgang til kode, database og konfigurasjon etter avtalte driftsregler.
4. Bekreft eksisterende bakgrunnstilgang til offentlige Stortings-URL-er og GitHub fra **den faktiske driftskontoen uten innlogget bruker**, inkludert proxy/sertifikat. GitHub-tokenet må ha issues read/write for bare det autoriserte repoet. Vanlige repo-/kontoabonnementer styrer varsler. Ingen credentials opprettes av verktøyet. Ikke send secrets i chat, argumenter, konfigurasjonsfil eller rapport. Miljøvariabelen må finnes i schedulerprosessens miljø; en variabel satt bare i en interaktiv terminal er ikke nok.
5. Gjennomgå frosset konfigurasjon og generert XML før registrering. Bruk den avtalte eksisterende kontoen med batchpåloggingsrett. XML bruker `Password` som Windows-logontype; passordet finnes aldri i XML. Lokalt `Get-Credential` gjelder den eksisterende kontoen, ikke opprettelse av en ny credential.

Generer bare XML, uten installasjon:

```powershell
python -m drift --config C:\avtalt\daily.json --task-xml C:\avtalt\ny-task.xml `
  --python C:\avtalt\venv\Scripts\python.exe --working-directory C:\avtalt\kode `
  --account 'AVTALT\eksisterende-konto' --start-date 2026-10-22
```

Når den konkrete oppgaven er gjennomgått og bakgrunnstilgang er prøvd lokalt, bruker operatøren [Windows-adapteren](../ops/windows-task.ps1) med eksplisitt vert, konto og nye XML-filnavn. `Inspect` er standard og leser eksisterende oppgave; `Install` krever `-BackgroundAccessVerified` og en lokalt oppgitt eksisterende `PSCredential`. Ingen `-Force` brukes, så en eksisterende oppgave erstattes ikke. Skriptets `-WhatIf` registrerer ingenting. Skriptet er et reviewbart oppsett; faktisk registrering må dokumenteres på den avtalte verten.

## Driftsprøve som fortsatt gjenstår

På avtalt vert må operatøren dokumentere generert/registrert task XML, vertens tidssone, konto uten passord, database-/rapportbaner, kilde-/GitHub-rettigheter og Task Scheduler-historikk. Gjennomfør en faktisk 06-start og en forsinket start, les prosessens returkode, `--status`, råkildehash, Excel-rapport-ID og outboxkvitteringer. Prøv omstart, samtidig forsøk, nettfrafall og gjenoppretting på et avtalt prøvegrunnlag. Testene i repoet demonstrerer kalenderberegning ved begge DST-overganger; de erstatter ikke faktisk scheduler-/konto-/nettverkskontroll. Skill bevisene i driftsprotokollen.

Ingen live GitHub-issue opprettes bare som prøve uten uttrykkelig avtalt prøveforhold. Bruk eventuelt allerede autorisert reelt avvik eller en fake GitHub-port i separat prøvedatabase. #10 lukkes først når eieren har akseptert faktisk drift.

## Gjenopptak og levering

Start samme kommando på nytt etter avbrudd. Den tar OS-låsen, avvikler ventende B2-jobber fra lagrede byte før ny HTTP og gjenfinner tapt stagingkvittering via kildeforsøket. En vellykket datojobb gjør ingen ny kildehenting samme dag; ventende GitHub-levering kan likevel prøves igjen. Ved avsluttet prosess frigjør OS låsen; slett ikke den beholdte `.runner.lock`-filen mens en arbeider kan leve.

Outboxen bevares før GitHub-HTTP. Inntil 100 leveringer prøves per start. Restanse gir `delivery=venter` og returkode 1; gjentatt start drenerer restansen uten ny HTTP mot Stortinget. En nyere dags ventende status erstatter eldre, ennå ikke leverte statusrader for samme stabile forhold; den gamle raden bevares som `erstattet` med peker til den nyere. Tvetydig POST beholdes særskilt og avstemmes med markeren, også blant lukkede issues; den gjentas aldri blindt. Vedvarende fravær kan kreve operatøravklaring. Etter dokumentert verifisering kan `issue_binding(database, repository, key, issue_number)` binde en faktisk eksisterende issue gjennom den offentlige driftsgrensen. Ikke slett usikker outbox for å tvinge frem en ny POST. Statusfeltet oppdateres uten daglige kommentarer, automatisk gjenåpning, automatisk løsning eller sletting av menneskeskrevet tekst.

Ta konsistent SQLite-backup med SQLite backup-API mens annen drift er stanset/koordinert; bevar også konfigurasjon, alle Excel-/JSON-artefakter og outbox-/issuebindinger. En løs kopi under skriving kan være inkonsistent. Gjenopprett i separat lokal mappe, verifiser hashene og eksisterende markere/bindinger mot GitHub før gjenstart. Dokumenter kjente datahull; spill ikke gamle kildefiler av som ny nettobservasjon. Nyere ubundne feilforsøk sperrer aktuell faglig bruk selv om det siste bevarte B2-innholdet ser gammelt og feilfritt ut.

## Offentlige Python-grenser

`drift.Config`, `run_daily(..., source=SourcePort, github=GitHubPort, now=...)` og `read_daily` er kjøregrensene. `checkpoint` mottar bare faste livssyklushendelser for observasjon og avbruddsprøver. `drift.store` gir bevarte rapporter, outbox og eksplisitte issuebindinger. `analyse.export_built_session_excel` bruker en ferdig vurdert rapport; `analyse.session_serialization` har validert `b6-frozen-1`-JSON. B2s valgfrie `source_attempt_id` binder staging atomisk. Tidligere API-standarder og immutable ID-/resultat-JSON er bevart. Se [ADR 0008](adr/0008-b7-varig-datojobb-og-outbox.md) og [datakontrakten](datakontrakt.md).

Den utførte [deterministiske kontrollrapporten](research/b7/README.md) viser konkrete bevis og begrensninger, adskilt fra driftsprøven som fortsatt gjenstår.
