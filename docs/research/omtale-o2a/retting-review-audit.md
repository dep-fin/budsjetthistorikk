# O2a: retting av samlet review og separat sikkerhetsaudit

Rettingen gjelder lokale endringer over fast kandidat `5887e180dcdfa85b16dea4cf8a79b91e7b2bdada`, tree `b0b25e41a071b2d63690a42e657ccd056a2738fe`, med sammenligningsbase main `d74d2cb`, på `codex/34-omtale-post1`. De tidligere portfunnene er gitt av orkestratoren og er bevart i [maskinlesbart retterbevis](retting-review-audit.json). Dette dokumentet erklærer ingen ny samlet review, sikkerhetsaudit, commit, PR, CI eller merge. Orkestratoren håndterer de gjenstående leveringsportene.

## Rettet atferd og faktisk gjenlesing

| Tidligere portfunn | Rettet kontroll | Faktisk filbevis |
| --- | --- | --- |
| P1: oppdiktet `step_id` og lokator ga seks verifiserte relasjoner etter omberegnede ID-er | Valgte og globale rader må svare til samme valgte uttrekk og eksakt revisjon, tolkning og originalartefakt. Lokator, råfelt og hendelsesgruppe kontrolleres også mot originalens lokale post 1-rader. | Begge `forged-event-canonical`-filene fra audit avvises. Ny eksport fra samme bevarte angrepsgrunnlag får synlig grunnlagsavvik og **0 relasjoner**, gjenlest fra JSON og XLSX. Tester prøver i tillegg endring av både uttrekk og rader, og endring av bare det synlige utvalget. |
| P1/P2: kapittel i KT/Vs beløpstabell kunne være feil mens 1429 stod i annen kontekst | PT, KT og V binder kapittel, post, delta og fra/til innen samme lokale trippel av tabellrader. | Begge gamle `wrong-kt-chapter`-filer avvises. Ny eksport viser `konto_eller_forslagsbelop_motstrid:KT` og seks `uavklart`-relasjoner. KT og V prøves separat; PT med feil lokal kapittelcelle og KT/V med lånte før/etter-beløp fra nabotekst prøves også i faktiske filer. |
| P2: KS kunne gi samlet komitérolle til én navngitt representant | Den navngitte samlede avsenderen og selve støtteutsagnet må begge være bevart i KS-avsnittet. | Begge gamle `wrong-ks-actor`-filer avvises. Ny eksport viser KS som `ukjent` / `ukjent_rolle` og seks `uavklart`-relasjoner, kontrollert i JSON og XLSX. |
| P2: 200 000 ubundne Excel-celler ble lastet og godtatt | Avgrenset ZIP-/XML-kontroll og fullstendig ark-/dimensjonsbinding kommer før full innlasting av input. Hele senere celleinnholdet og lenkene kontrolleres mot rekonstruert eksport. | Den eksakte gamle `padded-extra-sheet.xlsx` avvises med **0** kall til openpyxls `load_workbook` for inputfilen. En separat Windows-prosess brukte 57 937 920 byte maksimalt arbeidssett og 0,016 s i denne lokale prøven. Dette er et retterbevis, ikke en ytelsesgaranti. Nye prøver dekker ubundet ark, celleområde, celleverdi og XML-element. |
| P3: duplisert kildekatalog og magisk antall | Én konkret `SOURCE_CATALOG` brukes ved import og validering; antallet avledes fra den. | Autentisk grunnlags-ID er fortsatt `4fb6187784cfe233a89ce5d7180b4d76b3de669125d70c8eead7d70e9a0986a1`. Ingen generell adapter eller ny kilde ble innført. |

Alle angrepsfiler er **syntetiske feilprøver**, selv om de inneholder ellers autentiske originaler. Eksakte filhasher, feilmeldinger, nye rapport-ID-er og nye gjenleste feiluttrekk ligger i retterbeviset. De nye lokale feilparene er i `work/omtale-retterbevis/`; ingen tidligere eksport er overskrevet.

## Kontroller

TDD ble gjennomført ved den godkjente grensen original → seksjon → dokumentert relasjon → faktisk lagret og gjenlest JSON/XLSX. Før retting feilet ny hendelsesprøve med seks verifiserte relasjoner, begge lokale KT/V-kapittelprøver, den endrede KS-avsenderen og begge opprinnelige paddingprøver. Utvidelsen med samtidig endret uttrekk og rader og med bare endret valgt utvalg feilet også før kildebindingen ble strammet inn. De samme prøvene bestod etter retting. ZIP-/XML-ressursgrenser ble deretter prøvd særskilt.

Utførte kommandoer fra reporoten, med de pinnede repoavhengighetene og `lxml 6.1.3`:

```powershell
python -m pytest -q tests/test_omtale.py --basetemp work/fix-focused-final
python -m pytest -q tests/test_omtale.py -k synthetic_xlsx_resource_limits --basetemp work/fix-resource-boundaries
python -m pytest -q tests/test_b6_authentic.py tests/test_b6_cli.py tests/test_b8.py tests/test_b9.py --basetemp work/fix-compatibility-final
python -m ops.omtale_proeve --output work/omtale-post1-rettet-leveranse
ruff check .
ruff format --check .
python -m mypy
git diff --check
```

Den første fokuserte kjøringen bestod med **30 prøver på 154,54 s**. Fire etterfølgende ressursprøver bestod på **13,91 s** og dekker 70 000 celler i et eksisterende tillatt ark, forfalsket stor dimensjon, for mange ZIP-medlemmer og for stor XML-metadatadel. B6/B8/B9-kompatibilitetskjøringen bestod med **128 prøver på 49,70 s**. Fullsuite ble ikke gjentatt: resultatet **814 bestått, 2 hoppet over** gjelder den tidligere kandidaten `5887e18`, og final fullsuite hører til CI. Ruff check/format og mypy er kjørt på den rettede kandidaten. Eksakte endelige resultater står i [verification.json](verification.json).

En syntetisk, sterkt komprimerbar HTML-original på over 5 MiB bevares komplett i base64, eksporteres og gjenleses fra begge filer etter at kildekatalogen er fjernet. Den eksisterende prøven med lang formellignende P1-tekst og faktisk fortsettelsesark består. Verken store legitime originaler, tidligere B8/B9-filer eller uavhengig ordinær innlesning av den autentiske vedtaksprøven 40034229 er erstattet med interne objektprøver.

## Ny autentisk leveranse og grenser

`work/omtale-post1-rettet-leveranse/` er produsert på den rettede kandidaten og faktisk gjenlest fra JSON og Excel, også som offline reeksport med SQLite-filen utilgjengelig. Rapport-ID er `6021e1344038b6727f76cb09e77e382b4b5b1a48948acd977df0849eba391eb3`; basis-ID er uendret. Inventaret har seks observasjoner, to eksisterende hendelsesgrupper, åtte seksjoner og seks kildeverifiserte, ikke faglig godkjente post 1-relasjoner. De nye base-/rapport-ID-ene skyldes et nytt datert B8-snapshot; gamle filer og ID-er beholdes. Eksakte filhasher finnes i leveransens `kontroll.json` og i verification-filen.

Ressursgrensene og Excel-gjenlesingens behov for en midlertidig underkatalog ved inputfilen er dokumentert i [pilotkontrakten](../../omtale-pilot.md). Ressursvernet gjelder O2a-leseren; gamle B8/B9-lesere er ikke endret. Ingen ny visuell layout er innført eller ny native Excel-kontroll hevdet. #35 bygges ikke, #10 står åpen, og ingen faglig godkjenning eller årsdekning gis.

## Andre etterkontroll

Den uavhengige etterkontrollen av `d45dee7` fant ytterligere kilde-/råfeltbinding og et uavgrenset hyperlenkeområde. Den separate sikkerhetskontrollen ble stoppet av verktøyets automatiske risikofilter og er ikke et pass. Andre retting med nye filer, eksakt Python-eksekverbar og dependency-target er dokumentert i [etterkontrollens retterrapport](retting-etterkontroll2.md) og [maskinlesbart bevis](retting-etterkontroll2.json). Resultatene ovenfor er bevart som kontrollhistorikk.
