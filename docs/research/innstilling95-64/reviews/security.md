# Separat sikkerhetsaudit av T6/#64

**Portstatus: BESTÅTT for den faste kandidaten. Ingen åpne P1-/P2-sikkerhetsfunn. Én ikke-blokkerende observasjon om utskriftsprofil er angitt nedenfor.**

30. oktober 2026. Auditen omfatter hele `git diff base...HEAD`, inkludert produktmodeller, adapter, analyse/CLI, Excel, prøveskript, tester, dokumentasjon og data-/bevisfiler. Dette er en uavhengig sikkerhetsport; andre nye reviewrapporter er ikke brukt som fasit.

| Binding | Fast verdi |
| --- | --- |
| Base | `9616fbe6a8ab15eec696f34de76888565a784f8f` |
| Kandidat | `fc9b676ce6e2f361433f2562bcdf91930302c21e` |
| Kandidattre | `93fee86f5b117c076136dd95d8d48b32fe1d1316` |
| Checkout | `work/t6-innstilling95` |
| T6-basis | `3c10e042ad953e3ad9e47e6eee4c41ffe0d4744e36ef126538cb4b109396eccb` |
| Beholdt T5-basis | `f5a7a071d35e58642c5872cc658eb2abd4b37c266227e2fb2c2f0df21a7713c7` |

AGENTS, arbeidsflyt, issue-regler, ansvarsdeling, kravkontekst, hele publiserte #64 og dets tomme kommentarliste er lest. Før-kode-kontrakten, T6-kontrollpakken, relevante eldre JSON-/kilde-/Excel-guardmoduler og T5s opprinnelige temafunn, security-fix og sluttetterkontroll inngår. Vurderingen bygger på aktuelle kode-/Git-objekter og egne faktisk skrevne filer.

## Resultat og avgrenset observasjon

Ingen prøvd forfalskning av beløp, kilde, behandlingsrolle, konto, år, fullmakt, gammel hendelsesidentitet, aktiv gren eller dekningsstatus ble akseptert. Originalrekonstruksjon og full basisrekonstruksjon er autoritet; rehashing av objekter og konvolutt gir ingen godkjenning av nye faglige påstander.

**P3, ikke-blokkerende: utskriftsmarger er ikke bundet til skriveren.** `analyse/innstilling95_excel.py:443–460` sammenholder arkvisning, arkformat, filtre, dimensjoner og synlighet, men ikke `page_margins` eller `sheet_properties`. Egen fil med bare `Forløp`-arkets `<pageMargins left="1000">` endret ble akseptert som samme rapport. En endring av `outlinePr.summaryBelow` ble også akseptert; eksporten har ingen grupper som dette kan skjule. Verdier, cellefarger, feltbindinger, hull og navigasjon på skjermen var uendret i disse prøvene. Utskrift er ikke rendret eller prøvd i native Excel. Det er derfor ikke dokumentert et angrep som skjuler faglige opplysninger i den avtalte cellevisningen. Dersom «all fysisk presentasjon» også skal omfatte utskriftsprofilen, bør leseren sammenholde disse egenskapene eller kontrakten presisere grensen. De to akseptene er registrerte observasjoner, ikke negative tester rapportert som avvist.

T5s tidligere P2 om temastyrt skjuling er **ikke gjenåpnet i T6**. Den nye leseren binder hele temaets størrelse og byte til skriverens faste `theme_xml` på linje 422–428, etter lokal pakke-/relasjonskontroll. Hvit systemfarge-fallback, Wingdings-font og UTF-8-BOM ble faktisk avvist. Rå stilprofil og hver celles type, verdi, tallformat, font, fyll, kant, justering, beskyttelse og lenke sammenholdes etterpå.

## Egne kontroller

[Hovedledger](security/results.json) har **99 navngitte kontrollutfall**: 87 forventede avvisninger, ti positive kontroller og de to uttrykkelige observasjonene ovenfor. [Tillegget](security/extra.json) har én ny vellykket offentlig filpareksport og åtte forventede avvisninger. [Grense-/bytekontrollen](security/supplement.json) har tolv ressurskanter, 15 kandidatbindinger og 35 byteeksakte råoriginaler. Tallene er konkrete kontrollutfall, ikke uavhengige sikkerhetsegenskaper eller en fullsuite.

| Kontrollgrense | Faktisk resultat |
| --- | --- |
| Rehashet JSON og faktisk XLSX | 25 hovedvarianter og fire tilleggsvarianter ga **58 avvisninger**. Alle 29 Excel-filer hadde snapshot og presentasjon skrevet fra samme forgiftede rapport og passerte beholderuttrekket før offentlig leser avviste dem. Nye objekter, relevante referanser, basis og rapport ble rehashet. |
| Semantiske varianter | Falskt beløp; samtidig endret før/etter med bevart lokal aritmetikk; rolle/avsender/år/konto/betydning/valuta/multiplikator/runde/omfang; falsk råverdi og kildepeker; fullmakt som monetært felt; nullutfylt post32; oppdelt delt ramme; feil romertall/fullmaktsrolle; 1429-/1533-grenlekkasje; falsk helårsdekning; skjulte globale hull; oppfunnet rettelseshistorikk; endret gammel kapsel; feil recipe og nye/gamle step-ID-er. |
| Kildepinner | Endret saks-XML med oppdatert faktisk hash/størrelse/base64, både med beholdt og forfalsket forventet hash og påstått kildeverifisert status, ble avvist gjennom begge formater. |
| Celler og presentasjon | Formel, tall som tekst, feil intern lenke, ekstern lenke, skjult ark/rad, null radhøyde, hvit font, skjulende tallformat, rå `applyFont`-flagg, uventet celleattributt og overstor koordinat ble avvist. Snapshotets delindeks ble også avvist ved endring. |
| ZIP/XML | Traverseringsmedlem, ekstra makrodel, duplikatmedlem, ekstern temarelasjon og DOCTYPE/ekstern entitet i metadata eller ark ble avvist. Deklarert utpakking over 128 MiB ble avvist før XML-lesing. Den faktiske arkivstørrelsen passerte utpakkingsporten ved eksakt faktisk total; én byte lavere tillatt total ble avvist. |
| JSON | Duplikatnøkkel, NaN, Infinity, ekstra konvoluttfelt, bool i heltallsfelt og dyp nesting ble avvist. Eksakt 64 MiB blanktekst nådde syntaksavvisning; 64 MiB + 1 ble stoppet av størrelsesporten. Dette er størrelsegrenser, ikke påstand om en faglig gyldig rapport på 64 MiB. |
| Payload/gzip | Eksakt 16 MiB råpayload passerte `raw_source`; én byte over og ugyldig base64 ble avvist. Den faktiske avgrensede gzip-leseren avviste en syntetisk forelder på 32 MiB + 1. Den direkte gzip-prøven omgår bevisst den tidligere offentlige kildepinnen for å nå denne ressursporten; ingen slik falsk forelder ble godkjent gjennom offentlig rapportleser. |
| Objektgrenser | For 64 kilder, 16 dokumenter, 4096 inventarposter, 1024 utsagn, 512 observasjoner og 4096 relasjoner nådde gjentatte syntetiske objekter eksakt grense og ble avvist semantisk. Ved grense + 1 kom ressursavvisningen først. Ingen gammel profil er utvidet. |
| Skriving og no-clobber | Et nytt offentlig JSON/XLSX-par ble skrevet, lukket og gjenlest likt. Eksisterende JSON/XLSX og originalkatalog ble avvist. Simulert kollisjon rett før faktisk `_publish` lot eksisterende byte stå urørt for begge filtyper. Traverserende kildeeksport ble avvist før målkatalogen ble opprettet. |
| Offline | Kald offentlig JSON-/Excel-gjenlesing med tømte relevante cacher og sperret `socket.socket`/`sqlite3.connect` bestod. Ingen nett- eller databaseport ble åpnet. |

## Gamle grenser, originaler og bevis

Egen Git-tresammenligning viste at **1409 av basens 1410 filer** har samme blob. Eneste gamle avvik er to additive T6-pekerlinjer i AGENTS. Dette omfatter de gamle guardprofilene, T1–T5, schema 5/B5, pinnede registre, primærkilder, fixtures, standardvalg og CI. Ingen gammel sikkerhetskontroll er svekket eller omgått for union339.

Autentisk gammel T5 ble lest med gammel T5-leser; dens T1-kapsel ble lest med gammel T1-leser. Hele typede basisobjekter var like kapslene i den nye rapporten. Unionen var 339 felt, 114 vedtaksfelt og 38 monetære hendelser. Begge inns95-representasjoners gamle identiteter og statuser består.

Egen originaleksport ga 42 filer: 35 lagrede rårepresentasjoner, seks rekonstruerte XML og indeks. Alle 35 rårepresentasjoner ble sammenholdt byteeksakt med den validerte kapselen og dens SHA-256. Alle seks API-utdrag ble sammenholdt med de bevarte XML-filene; 359 beholdt den fastsatte c5f3-forelderen, grensene, 64 868 byte og forventet hash. Ingen ekstra forelder-/utdragspayload eller oppfunnet HTTP-henting ble innført. Den separate Node-originalfasiten ble kjørt med `--check` og traff lagret SHA-256 `6fd8f0c2fb119771fccff1f61e22785fb9e4ac01fe706723934d2f7d07e473b1`.

Alle 15 bindingene i byggerens `local-candidate.json` traff faktisk råbyte, relevante LF-byte og Git-filtrert blob. Binær gzip har bevisst ingen LF-hash; råhash og Git-binding ble kontrollert. De nye `.gitattributes` gjelder bare nye kontroll-/fixturemapper og inneholder ingen kjørbare filtre, encodingdriver eller kommandoinngang. Prøveskript og oracle bruker faste lokale kildevalg; ingen ny shell-, nettverks- eller databasekjøreinngang er funnet.

## Reproduksjon og bevisbinding

Kontrollprogrammene ligger i [security/](security/). Fra en isolert checkout av den faste kandidaten med denne additive reviewmappen materialisert kan de kjøres slik. Alle outputkataloger må være nye. Dersom filparene mangler, lager repoets prøveskript dem først:

```console
python ops/innstilling95_proeve.py --output .local/full-acceptance/t6-files0
python -m docs.research.innstilling95-64.reviews.security.audit_checks --output .local/t6-security-replay
python -m docs.research.innstilling95-64.reviews.security.supplement --audit .local/t6-security-replay
python -m docs.research.innstilling95-64.reviews.security.extra_checks --audit .local/t6-security-replay
```

Denne kjøringen brukte Windows, bundled Python 3.12.14 og det oppgitte `c06-99235/.local/python-tools`-miljøet. Ruff og formatkontroll for de tre nye kontrollprogrammene bestod. [Bevisindeksen](security/evidence.json) binder programmene og alle 135 lokale utdatafiler under `.local/t6-security-audit02`; store angrepsfiler legges ikke i Git. De maskinelle ledgerne er bevart her:

| Fil | SHA-256 |
| --- | --- |
| `results.json` | `6dc3c7db451147e811f33d1de06adcc645a2cbdfe3901d00fe91869080702f85` |
| `summary.json` | `07acb50a7470126ebb63f55126ad1c175a1b3c8b88927c5a2a755829304c5937` |
| `supplement.json` | `31efb207a91d022b5e0a2a2a38d21980a426dc908f200050b87e4ad7373f650a` |
| `extra.json` | `bacd1fd0b0acd8ce276d8d9af42270a66ded6a58d8b71fcbe874ee481c422221` |
| `evidence.json` | `194e6538992c2114a94c6e5c3296033e940c761577a6a4ef5bafc461fdc80abc` |

Første direkte skriptinvokasjon manglet repoet i Python-søkestien og startet ingen prober. Første samlede audit kjørte de semantiske probene, men stoppet i auditens egen tallmutator fordi tomt Forløp-ark bare har tekstoverskrift. Den ble rettet til en faktisk tallcelle i Kontoer, og den andre kjøringen startet helt på nytt og fullførte. Første program er bevart lokalt. En separat første metadatahjelper forsøkte å sammenligne gzip med en bevisst null LF-hash; den endelige supplementkontrollen håndterer binærgrensen eksplisitt. Ingen av disse kontrollhjelperfeilene er ført som produktfunn eller beståtte prober.

## Begrensninger og overlevering

Ingen ny fullsuite er kjørt; oppgitt 1305 bestått/to eksisterende hopp er byggerens tidligere bevis. Ordinær vedtaksinnlesnings fire T6-feiltilstander er gjennomgått i kandidatens tester og er bevart ved blob-/grensekontrollen, men er ikke kjørt på nytt i denne auditen. Ingen ny primærkildehenting, native Excel, utskriftsrendering, ny visuell QA, Linux-kjøring, junction-/symlinkløp eller samtidig ondsinnet lokal katalogskriver er prøvd. Den simulerte publiseringskollisjonen beviser per-fil no-clobber; `export_pair` er fortsatt ingen transaksjon over begge filer.

Kandidatens head/tre og sporede produktflate var uendret før og etter. Bare denne rapporten, egne kontrollprogrammer/maskinelle bevis og ignorerte lokale prøvefiler er skrevet av auditen. Ingen produktretting, staging, commit eller GitHub-mutasjon er utført. Publisert-klon-kontroll, øvrige reviewer, full CI og merge er orkestratorens egne porter.
