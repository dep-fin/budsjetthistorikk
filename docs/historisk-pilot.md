# Lokal 2024-pilot

Oppfølging 22. oktober 2026: [P13-P2s faglige kontrollmatrise](research/historisk-excel/p13-p2/README.md) dokumenterer kildefunn og tillatt kontrollbruk for alle ni kolonner. Den leses separat og endrer ingen lagret pilotpakke. [P1-rapporten](research/historisk-excel/pilot2024.md) beholder sine faktisk utførte kontroller og historiske åpne spørsmål.

Piloten i #24 bevarer hele 2024-arbeidsboken, lager sporbare historiske observasjoner og leverer en lokal kontrollpakke med uavhengige sammenligninger. [Kontrollrapporten](research/historisk-excel/pilot2024.md) viser faktisk omfang og åpne spørsmål. Teknisk gjennomføring gir ingen faglig godkjenning eller årsdekning. #13 gjelder også øvrige år; #10s driftsprøve berøres ikke.

## Import og gjenopptak

Kjør fra repoet med Python 3.12 og pinnede `requirements.txt`. Bruk en egen lokal database og nye pakkenavn. Originalfilen lagres ikke på nytt.

```powershell
python -m innlesning.historical_excel stage --database work/pilot.sqlite --source work/2024.xlsx --year 2024 --year-evidence 'kilderegister ved da720e9dd4ebfff31d88c14488c5f3217d045786'
python -m innlesning.historical_excel resume --database work/pilot.sqlite --id FORSØKS_ID
python -m innlesning.historical_excel attempt --database work/pilot.sqlite --id FORSØKS_ID
python -m innlesning.historical_excel read --database work/pilot.sqlite --id UTTREKKS_ID
```

`import` gjør staging og gjenopptak i ett kall med samme argumenter som `stage`. Returkoden er 1 ved feil og 0 ved teknisk lagring, også med faglige avvik. Gjenopptak bruker bare mottatte byte i SQLite. Ved filfeil uten byte startes et nytt forsøk. Ny tolkning kan angis med `--interpretation-note`; ny fil/tolkning kan knyttes til et eksakt tidligere uttrekk med `--predecessor`.

Nye forsøk og CLI velger `historisk-excel-2024-v3`, `pilotregler-3` og celleinventar `historisk-celler-3`. Lagrede v1-/v2-uttrekk leses med sine opprinnelige ID-er og JSON. Et uferdig forsøk fra disse versjonene kan ikke fullføres med endret kode under gammel adapter; start et nytt v3-forsøk. En ny tolkning erstatter ingen forgjenger. V2 rettet dokumentarkets navn: J er kapittelnavn, H er postens formål og I er separat rå stikkordstekst i celleinventar og radkontekst. V3 sperrer også resultatceller i et eksplisitt formelområde når bare ankercellen har `<f>`.

De offentlige Python-grensene er `stage_historical_workbook`, `import_historical_workbook`, `resume_historical_import`, `read_historical_attempt` og `read_historical_workbook` i `innlesning.historical_excel`. Tolkningen er avgrenset til 2024. Den krever de to kjente arkene, men arkfilene finnes gjennom arbeidsbokens relasjoner.

## Eksport og kontroll

```powershell
python -m analyse.historical_package export --database work/pilot.sqlite --id UTTREKKS_ID --package work/kontrollpakke-01
python -m analyse.historical_package verify --database work/pilot.sqlite --id UTTREKKS_ID --package work/kontrollpakke-01
```

Oppgi `--comparison SAMMENLIGNINGS_ID` ved eksport og verifikasjon av en valgt lagret kontrollrapport. Uten dette valget er sammenligningen uttrykkelig ikke utført. `export_historical_package` og `verify_historical_package` er de tilsvarende Python-grensene. Verifikasjon leser databasen uten skriving. Eksport registrerer bare en separat publiseringskvittering etter filkontrollen.

Pakken inneholder `manifest.json`, `kontroll.xlsx` og åtte JSONL-filer: observasjoner, celler, kandidater, kolonneregler, avvik, sammenligning, metadata og grunnlag. Originalbyte kan gjenleses gjennom eksisterende `read_source`. Excel har eksplisitte felter og et komplett typet JSON-felt per rad. Lengre tekster videreføres i `Fortsettelser` med ark/rad/kolonne/del. Ark over 50 000 datarader fordeles på nummererte ark. Kildetekst evalueres aldri som formler.

Importforsøk og pakkepublisering er separate. Ved avbrudd etter lagring gjenbrukes uttrekks-ID-en. Ved avbrudd før katalogpublisering er sluttpakken usynlig. Ved tapt kvittering etter publisering kontrolleres den eksisterende pakken mot SQLite. En skadet eller fremmed pakke avvises og erstattes ikke.

## Full lokal reproduksjon

Hent originalbyte binærsikkert fra den festede Git-revisjonen. PowerShell-tekstomdirigering skal ikke brukes for XLSX:

```powershell
python -c "import pathlib,subprocess; p=pathlib.Path('work/2024.xlsx'); p.parent.mkdir(exist_ok=True); p.write_bytes(subprocess.check_output(['git','show','da720e9dd4ebfff31d88c14488c5f3217d045786:data/historisk/original/2024_samlet_inputdata.xlsx']))"
python -m analyse.historical_pilot --source work/2024.xlsx --output work/pilot2024-run --proposal-refs docs/research/historisk-excel/pilot2024/proposal-refs.json
```

Runneren verifiserer originalhash/størrelse, de offentlige kontrollartefaktenes hash, alle tolv autentiske API-fixtures og separat v2-replay. Den fryser referanser og sammenligningsregler før utfallet beregnes, kontrollerer forventningene og verifiserer den faktiske eksportpakken. Ingen nett brukes. Originalen må være tilgjengelig fra den historiske revisjonen; historikkbranchen skal ikke flettes for dette formålet.

Alle utdatafiler, inkludert sammendrag, databaser med sidefiler og pakkeinnhold, kontrolleres mot alle leste originaler og kontrollfiler før første skriving. Baner, symbolske lenker og eksisterende hardlink-aliaser sammenlignes. Et fremmed sammendrag eller en kollisjon avvises uten overskriving. Sammendrag publiseres atomisk uten erstatning. Et identisk eksisterende sammendrag gjenbrukes først etter pakkeverifikasjon. Eldre fullpakker skal beholdes i sine egne kataloger ved ny tolkning.

`historisk-sammenligning-2` krever et lukket omfang med år, NOK, prøvd kildefaktor, talltype, betydning, detaljeringsnivå, budsjettside, stadium, periode og referansegrunnlag. Hypotesen bindes til kolonneregelen og hver valgt kandidat i v2-uttrekket. Referansen har eget omfang og faktisk kildeår. Ukjente felt eller uforenlig innhold avvises før kontrollgrunnlaget fryses. Et talltreff alene kan ikke overstyre disse kontrollene. Dokument-D på kode 0 og avledede komponentdifferanser på kodene 1–6 har separate grunnlag; de sistnevnte krever begge kildeinnganger. G og I krever faktisk regjeringsforslag. M og N står fortsatt `ikke_utfort`.

De bundne profilene er avgrensede matematiske kontrollhypoteser, ikke normaliserte eller faglig godkjente observasjonsakser. D-profilen gjelder bare uttrykkelig valgte dokumentgrupper, uten å tilordne én felles behandlingsrunde til dem. Perioden for K/L gjelder de konkrete prøvde aggregatene; generell periodedekning og overlapp er fortsatt åpne. Eksisterende sammenligningsrapporter i v1 kan fortsatt leses uendret, men nye kontroller krever v2-grunnlaget.

En ny full kjøring på samme lokale database gjenbruker beløpsuttrekket og pakken, mens nye forsøk registreres separat. Lokale uttrekks-/kontroll-ID-er fra API-replayen kan variere mellom ferske databaser, siden B2-revisjoner har sine egne identiteter. Kildehash og lokator er varige kontrollbevis. Ny kode som endrer tolkningsinnhold krever ny adapter-/tolkningsversjon.

## Avgrensninger og ressursgrenser

Rå null, blank celle, fraværende posisjon og uavklart talltype er forskjellige opplysninger. Alle ni kolonneregler er foreløpige. Normalisert og kontrollert NOK er null; eksakte matematiske kandidater bevares som Decimal-strenger. Forslag, aggregater, dokumentreferanser og komponentdifferanser oppretter ingen vedtak. Historisk Dep/fdep/gdep/navn/område/kategori bevares separat; dagens register tilbakeprojiseres ikke.

Standardgrensene er 32 MiB kilde, 128 ZIP-medlemmer, 32 MiB per medlem, 128 MiB samlet utpakket innhold, 1 000 000 XML-noder per dokument, 1 000 000 tegn per tekstfelt, 250 000 fysiske celler og 300 000 inventarposisjoner. Numeriske leksmer har høyst 128 tegn og eksponentens absoluttverdi høyst 100. Grenser kan senkes for et forsøk, men økes bare gjennom en ny adaptervurdering. ZIP/XML-duplikater, usikre interne mål og DTD/entiteter avvises. Eksterne metadatarelasjoner bevares lokalt uten henting; et eksternt ark avvises. Stiler på hele kolonneintervaller utvider ikke rutenettet.

V2 har i tillegg `resolved_chars=16 777 216` for samlet løst celleinnhold, med hver shared-string-bruk telt på nytt, og `serialized_chars=268 435 456` som konservativt budsjett for materialisert/serialisert innhold. Shared strings og inline-tekst telles før sammenføyning, og gjenbruk telles før lagring i inventaret. Hele radkonteksten serialiseres én gang per rad. Alle gjentatte observasjonskontekster, celleinventar, metadata og kandidater reserveres før de store hash-/JSON-kopiene dannes. Overskridelse gir varig mislykket forsøk med mottatte originalbyte, uten delvis uttrekk.

Egen formeltilstedeværelse (`formula_present`), formeltekst, attributter og cache er separate inventarfelt. `formula_result` sperrer både egen formel og alle inventarceller dekket av array-, shared- eller dataTable-formelens `ref`. `formula_region` bevarer anker, rå områdehenvisning og type. En dekket celle uten `<f>` beholder egen formeltekst/attributter som null og får bevart rå cache og et synlig `formelresultat`-avvik. Observasjonens tomme formelstreng markerer formelresultat uten egen tekst. Ingen formel evalueres.

Områder kontrolleres etter at alle fysiske celler og dimensjonsposisjoner er lest. Rekkefølgen i XML og en for liten arkdimensjon skjuler derfor ikke dekkede fysiske celler. Bare enkle A1-adresser og rektangler innen Excel-grensen støttes; blant annet absolutte adresser, flerområder, omvendte/overlappende områder og anker utenfor området avvises konservativt. Array/dataTable uten `ref` og ukjent formeltype avvises. Samlet deklarert formelareal på tvers av ark er begrenset av `positions`, separat fra inventarunionen. Kolonneintervaller og binærsøk kontrollerer eksisterende inventar uten å materialisere områdets celler. Antall intervaller er høyst det begrensede arealet, og intervalldata/resulterende cellemetadata belastes også serialiseringsbudsjettet. Enkeltcelle-array er støttet; områder utvider aldri arkdimensjonen.

Kontroll-Excel kontrolleres innen 128 MiB komprimert, 256 ZIP-medlemmer, 256 MiB per medlem og 1 GiB samlet deklarert utpakket innhold. Dette er eksportens større kontrollflate, ikke importens grenser. Verifikasjon sammenligner dessuten alle celler mot lagret grunnlag og avviser ekstra ark/rader/kolonner/formler.

Originalen, fullstendige råinventarer, kandidater, SQLite og kontrollpakker beholdes lokalt inntil delingsgrunnlaget er avklart. Den offentlige rapporten inneholder antall, hasher og allerede kildebelagte kontrollankere. Interne filstier i arbeidsbokmetadata gjengis ikke der.
