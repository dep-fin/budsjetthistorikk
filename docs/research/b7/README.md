# B7: deterministisk driftskontroll, 21. oktober 2026

Kontrollen gjelder kandidatkode for #10 på grunnlag av B6-merge `2633d8a92633dc9fb63c7413620f297b99efe6f4`. Den er utført lokalt på Windows, med Python 3.12, bevarte fixturer og fake kilde-/GitHub-porter. Ingen faktisk scheduleroppgave er registrert, ingen ny live vedtaks-/sesjonsrespons er brukt som prøve, og ingen GitHub-varslingsissue er opprettet. Plattformvalg og gjenstående faktisk driftsaksept er dokumentert i [manualen](../../b7-drift.md).

## Resultat og reproduksjon

Sluttkjøringen etter reviewretting ga **482 beståtte, 1 hoppet over**, av 483 innsamlede tester, på 229,68 sekunder. Basen hadde 423 tester; kandidaten tilfører 60, hvorav tre kom med reviewrettingen. Det hoppede tilfellet trenger rett til å opprette en symbolsk filkobling på Windows. Den separate prøven med to faktiske prosesser, avvist overlapp og frigjort OS-lås etter prosessdød er bestått. POSIX-grenen er implementert og hører til CI-/Linux-kontrollen; den er ikke utført i denne Windows-økten.

Ruff check, Ruff format check (68 Python-filer), strict mypy (39 kildemoduler) og `git diff --check` er bestått. Windows-adapteren er kontrollert med PowerShells AST-parser og deterministisk lesing av generert task XML. Ingen registrering eller faktisk CIM-/schedulerprøve inngår. En eldre B5-test som brukte skjemaversjon 5 som ukjent fremtid, er oppdatert til 6 fordi 5 nå er en støttet additiv versjon; prøvens avvisningskrav er bevart.

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q --basetemp=work/pytest-b7-reviewfix-final
python -m ruff check .
python -m ruff format --check .
python -m mypy
git diff --check
```

Det lokale delte B1-testmiljøet manglet `tzdata` og pip. Testene brukte derfor dette miljøets eksisterende biblioteker med `PYTHONTZPATH` satt til den allerede installerte, bundlete `tzdata/zoneinfo`-mappen. Den delte runtime-en ble ikke endret. Pakken er verifisert som `tzdata 2026.5`/IANA `2026e`, og [PyPI-versjonen](https://pypi.org/project/tzdata/2026.5/) er låst i kravfilen for ordinær installasjon. En ny ordinær installasjon trenger ikke denne testspesifikke miljøvariabelen.

## Offentlig vertikalsnitt og avbrudd

Prøvene går gjennom `run_daily` til lagret B2-kilde, eksplisitt v2, B5-lesing/eksakt aktivert nybehandling, frosset B6-JSON, virkelige Excel-filer/celler og fake GitHub. De omfatter vinter/sommer og begge DST-overganger, før kl. 06, gjentatt dato, uteblitt dato, neste/fremtidig sesjon, gammel ID med sen innkomst, rettelse, timeout, HTTP-feil, ugyldig XML, tomt inventar, feil i sesjonslisten og videre kontroll av kjente sesjoner.

Prosessavbrudd etter staging før kvittering, etter rapportfrysing, etter filpublisering før kvittering og før outboxlevering gjenopptas uten ny kildehenting. Tvetydig GitHub-POST avstemmes uten blind ny opprettelse, også over datogrenser og etter databasegjenoppretting. Lukket issue og menneskeskrevet innhold beholdes. En nyere ventende dagstatus erstatter eldre ikke-leverte dagkopier; usikker POST bevares særskilt. Faglige avgjørelser gjenopplives ikke etter kilde-/aktiverings-A → B → A eller en nyere avvisning. Nyere prestagingfeil sperrer gamle aktuelle godkjente verdier. Ingen automatisk aktivering er utført. En uttrykkelig godkjent, uendret numerisk null gir bare rapport og ingen issue.

## Regresjoner etter reviewfunn

Tre nye testtilfeller dekker to driftsfeil gjennom offentlig `run_daily`, med faktiske SQLite-/Excel-artefakter og fake GitHub. Begge feilene ble først reprodusert med røde tester mot kandidaten: En ikke-tom katalog som utelot 2026–2027, førte til at denne sesjonen ikke ble hentet. En OS-feil bare ved JSON-publisering ga `kjorerapport_fil_feilet`, men `control_needs=0` og intet varsel i et ellers godkjent nulltilfelle.

[Sesjonsprøven](../../../tests/test_b7_sessions.py) beholder 2026–2027 og 2027–2028 i daglig HTTP, frosne rapporter og Excel selv når katalogen bare beholder den siste av dem. En rettelse og en forsinket ID fra den utelatte sesjonen blir med. En katalogoppført 2028–2029 med fremtidig start blir ikke hentet. Katalogfraværet gir `outcome=partial`, eksplisitt feil i kjørerapporten og én stabil issue over gjentatt forsøk samme dato og neste dato. B6 viser fortsatt separat kildeinnholdsdekning for inventarene som faktisk ble hentet.

[Filfeilprøvene](../../../tests/test_b7_controlled.py) bruker et ellers godkjent numerisk nullbeløp. Ved avvist JSON-publisering bevares feil, ett kontrollbehov og outbox før levering. Med GitHub-port leveres varselet samme start; uten eksisterende bakgrunnstilgang blir det stående i kø. Gjentatt forsøk og neste dato bruker samme issue. Hvert forsøk gjør bare ett publiseringsforsøk, og senere vellykket publisering gjenbruker det bevarte kilde-/Excel-grunnlaget samme dato. Rå unntakstekst lagres ikke. Det eksisterende nulltilfellet uten filfeil gir fortsatt null varsler.

JSON-kjørerapporten publiseres nå før den ene GitHub-leveringsrunden. Den immutable filens `delivery` er et snapshot før levering, mens returverdien og `read_daily` viser kvitteringen etterpå. Dette gjør også filfeilen varslingsbar og beholder grensen på 100 outbox-rader per start. Manual, datakontrakt, ADR og varige funn dokumenterer denne rekkefølgen.

Den interne ferskhetskonteksten er samlet for B2s revisjons- og inventarlesere. Offentlige ID-er, feltformer, liste-/tuppeltyper og tidligere resultater er bevart. Offentlige prøver kontrollerer samme forsøks-ID, feilstatus, tom råhash og feilklasse ved prestagingfeil. B5/B6-prøvene viser fortsatt sperret aktuell godkjenning etter et nyere slikt forsøk. Schema 5 er uendret.

## Bevarte autentiske objekter i syntetiske testkonvolutter

Ni eksisterende, komplette vedtaksobjekter brukes fra B3-/B6-fixturene: 40032850, 40033025, 40033719, 40034064, 40034226, 40034287, 40034048, 40034229 og 40036289. Originalfixturene er uendret. Testporten bygger tre syntetiske fullistekonvolutter, med de opprinnelige fixturhashene i proveniensen. Dette er ikke komplette ekte sesjoner eller nye live kildefunn.

Gjennom hele runneren beholdes **9 inventar-ID-er**, **2 663 beløpsobservasjoner**, to eksplisitte supplerende sesjoner og tre nye Excel-filer på omtrent 2,04 MB hver. ANNET 40033719/40034287, de **76 posthendelsene** uten standardfrase i 40034048/40034229, rå `I 615 833` i 40036289 og konfliktene på 1860/1, 4860/1 og 5999/90 bevares. Aktuelle godkjente konfliktbeløp og helsesjonsgodkjenning konstrueres ikke.

Prøvens bevisst uavklarte historiske register-/kontrollgrunnlag ga **10 136 stabile avviksnøkler**. Dette er per klasse/vedtak/lokator/felt, ikke antall vedtak eller feilfrie analysetall. GitHub-porten er feilet med vilje i denne store prøven; hele køen bevares uten eksterne issues. Arbeideren leverer høyst 100 rader per start, slik at store førstegangs-/kontrollrestanser må følges opp og dreneres etter manualen. Tallet er ingen måling av den faktiske produksjonssesjonens varslingsvolum.

## Eksterne kontrakter

Den offisielle [sesjonsdokumentasjonen](https://data.stortinget.no/dokumentasjon-og-hjelp/sesjoner/) er kontrollert for felt, lokaltid og advarsel om fremtidige sesjoner. Microsofts [StartBoundary-skjema](https://learn.microsoft.com/en-us/windows/win32/taskschd/taskschedulerschema-startboundary-triggerbasetype-element) viser lokal dato/tid i XML; generert oppgave krever en vert med avtalt norsk tidssone og må fortsatt prøves der. GitHubs [issues-API](https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues) dokumenterer åpne/lukkede/all, paginering og PR-er i issue-listen; klienten filtrerer PR-er og oppdaterer bare body. Disse dokumentkontrollene erstatter ikke faktisk bakgrunnstilgang eller driftsaksept.
