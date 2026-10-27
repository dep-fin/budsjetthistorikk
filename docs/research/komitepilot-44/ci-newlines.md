# T2: CI-retting av historisk HTML-rekonstruksjon

Kontrollert 27. oktober 2026. Avgrenset CI-løkke for #44 / PR #45 over lokal
head `83b659c114cd1456718c28e12b6544e104e47c8c`, tre
`6c2b35a5d561208758814fba20b56bbcbb523ef1`. Publisert head
`1898ef3fbd6a5e9da119ce72a002a06b41b2ef6a` har samme tre. Notatet og nye
kontrollogger supplerer de tidligere hashfestede journalene; gamle journaler
og akseptbevis er uendret og gjelder sine opprinnelige kandidater.

## Faktisk feil og årsak

[CI 40518317553, jobb 122237867165](https://github.com/depmartin/budsjetthistorikk/actions/runs/40518317553/job/122237867165)
sluttet med **1 070 beståtte og én setup-feil etter 1 149,47 sekunder**.
[Det gjenleste loggutdraget](checks/t2-ci-original-failure.log) binder dette til
`test_union_selection_navigation_offline_and_legacy_objects`. Feilen var
`ValueError: Omtalegrunnlaget avviker fra gjenleste originaler/lokatorer/roller`,
fra T1-leseren gjennom O2b til `innlesning.omtale.validate_basis`. Jobben feilet
med exitkode 1, ikke ved timeout.

Loggen viser Linux/Python 3.12.15 og lxml 6.1.3 fra manylinux-hjulet. Den separate
Astra-diagnosen identifiserte hjulets libxml2 2.14.6; den gamle CI-loggen skrev
ikke selv ut denne runtimeversjonen. Her måltes Windows/Python 3.12.14,
lxml 6.1.3 og libxml2 2.11.9. Samme lxml-versjon betyr dermed ikke samme
underliggende HTML-parser. [libxml2 2.14.6s HTML-parser](https://github.com/GNOME/libxml2/blob/v2.14.6/HTMLparser.c#L3117)
normaliserer rå CR/CRLF til LF. Den autentiske T1-kapselen lagrer historisk CR i
O2b-seksjonene K1, KS, KT, V og K22. Streng rekonstruksjon sammenligner også
fulltekst, HTML, overskrifter og de avledede ID-ene.

Den nye regresjonen bruker den offentlige T1-leseren og det autentiske,
uendrede arkivet. Hver parserregel kjøres i en fersk prosess, før noen gammel
basis kan finnes i valideringscachene. På Windows består den opprinnelige
parserregelen; innført CR/CRLF-normalisering ved den eksterne lxml-grensen
gjenskaper den samme exceptionen. Før rettingen: **én bestått / én feilet**,
2,74 sekunder. Etter rettingen: **to beståtte**, 3,37 sekunder. Dette er et
lokalt årsaks-/regresjonsbevis, ikke en kjørt Linux-suite.

## Avgrenset retting

`innlesning.legacy_html.parse_legacy_html` skjermer rå CR med en kollisjonsfri
sekvens av HTML-mellomrom i parserinput. Mellomrom bevarer markupens skilletegn
og plasseringen av head/body. Tekst, hale og attributter tilbakestilles til CR
før seksjoner, HTML, hierarki, lokatorer og ID-er beregnes. Script/style og
kommentarer behandles i samme tre. Markørens reservevalg har begrenset bredde,
også når kilden allerede har lange markørlignende mellomrom eller tegnreferanser.
Innhold uten rå CR gjennomgår vanlig parsing.
Originalkildenes byte og kildehash brukes fortsatt uendret.

Bare de to gamle HTML-inngangene i `innlesning.omtale` og `_doc` i
`innlesning.visningspilot` bruker denne historiske regelen. T2-adapterens
faglige strukturering og samtlige strenge felt-/kilde-/rolle-/ID-sammenligninger
er uendret. Ingen sammenligningskrav er fjernet, og ingen fixture er rehashet.
Regresjonen sammenligner alle gjenleste felt med den gamle JSON-konvolutten og
kontrollerer begge autentiske arkivhashene:

- Gzip: `629c3561cca6f0ab2a5644958c7ae6590dd70775d688f40e134bda449e8982a6`.
- Utpakket: `99e871e0ab780cbb548e15699f3093621d0f25229e3fa06c29cfdb5552803f53`.

En separat lokal sammenligning leste alle fem ulike HTML-originaler fra den
gamle T1/O2b-kapselen. Full HTML-serialisering og hver DOM-lokator var identiske
med libxml2 2.11.9s opprinnelige resultat: Prop.16 ch2/ch4, Innst.81, Innst.95
og plenum. Denne kontrollen gjelder hele disse fem trærne, ikke bare et nytt
egenprodusert snapshot. [Hele kontrolloggen](checks/t2-ci-html-originals.log)
oppgir hvert faktisk kildefilnavn og hash.

Tidligere lokale leveranser er dessuten lest via hashkontrollerte kopier:
åtte O2a/O2b-par, to B8/B9-par, ett T1-par og to tidligere T2-par
(standalone/union). **13 JSON-/Excel-par / 26 originalfiler** er gjenlest med
samme gamle rapport-ID-er, og originalhashene er uendret etterpå.
[Resultat og hasher](ci-old-compatibility.json) og
[kontrollogg](checks/t2-ci-old-compatibility.log) er egne nye bevis. Kontrollen
bruker de tidligere filene under prosjektets lokale `outputs`, ikke regenererte
«gamle» filer. Den er et Windows-bevis; tilgjengeligheten av disse lokale
originalene er en grense for reproduksjon på en fersk vert.

## CI-ramme og videre kontroll

Workflowens fulle testutvalg beholdes. Timeout økes fra 20 til 30 minutter:
den feilende jobben brukte om lag 19 min 31 s uten å kjøre uniontestens innhold;
tidligere lokale bevis målte unionen til 154,18 s og fullsuiten til 1 283,40 s.
Disse historiske tidene begrunner marginen og hevdes ikke som nye målinger på
den rettede kandidaten. En egen CI-step skriver nå ut lxml, kjørt libxml2 og
kompilert libxml2 før de øvrige kontrollene.

Kontrollkommandoer fra T2-checkouten, med Python 3.12 og pinnede
`requirements-dev.txt`:

```powershell
python -m pytest tests/test_legacy_html_newlines.py -q --durations=3 --basetemp work/t2-ci-newline-final
python -m pytest tests/test_legacy_html_newlines.py tests/test_omtale.py tests/test_omtale_o2b.py tests/test_visningspilot.py tests/test_komitepilot.py -q --durations=12 --basetemp work/t2-ci-newline-regression
python -m pytest tests/test_komitepilot.py::test_union_selection_navigation_offline_and_legacy_objects tests/test_visningspilot.py::test_rehashed_json_cannot_change_source_binding tests/test_omtale_o2b.py::test_synthetic_rehashed_false_binding_is_rejected_from_written_json_and_excel -q --durations=4 --basetemp work/t2-ci-newline-final-union
python -m ruff check .
python -m ruff format --check .
python -m mypy
git diff --check
```

Nye basetemp-navn brukes ved gjentakelse. Denne Windows-verten bruker bundlet
Python og samme lokale pakkekatalog som beskrevet i [overleveringen](OVERLEVERING.md).
Den brede, inkrementelle regresjonsrunden lagres i
[egen logg](checks/t2-ci-newline-regression.log): **273 beståtte / 1 058,32
sekunder**, uten feil eller hopp. Den omfatter faktisk
JSON-/Excel-/offline-union, O2a/O2b/T1/T2, rehashede negativer og uavhengig ny
vedtaksinnlesning. Runden startet før markørens reservevalg ble avgrenset og
før den siste syntetiske prøven ble lagt til; den oppskrives ikke alene til
bevis for den avsluttende kandidaten.

Avsluttende ferske prosesser prøver den uendrede historiske kapselen under begge
linjeskiftregler og faktisk skrevet/gjenlest syntetisk O2a med 4 096 mellomrom,
CRLF og tegnreferert markørlignende tekst: **tre beståtte / 11,27 sekunder** i
[siste linjeskiftkontroll](checks/t2-ci-newline-final.log). Deretter består
**14 prøver / 206,00 sekunder**, inkludert hele den faktiske T2-unionen med
JSON/Excel/offline/navigasjon og rehashede O2b-/T1-negativer, i
[siste unionkontroll](checks/t2-ci-newline-final-union.log). Unionens testinnhold
tok **171,11 sekunder** på denne avsluttende kandidaten. Statiske kontroller
består med 112 formatterte Python-filer og 63 typekontrollerte kildefiler.
Kandidatens filhasher og kontrollenes presise rekkevidde finnes i
[den nye CI-journalen](ci-newlines.json); [siste statiske kontroll](checks/t2-ci-newline-static.log)
er lagret separat.

Ny fullsuite på Windows er ikke kjørt i denne CI-løkken. Den nye Linux-headen
må faktisk bestå full CI etter publisering; Windows og simulert normalisering
erstatter ikke dette. Retteren har ikke committet, pushet, reviewet, auditert
eller merget. Schema 5, gamle ID-er, uavhengig vedtaksinnlesning og #10s åpne
driftsgrense består. Ingen ny faglig godkjenning eller helårsdekning følger.
