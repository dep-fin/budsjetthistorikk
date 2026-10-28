# Akseptledger P1 / #52

Denne ledgeren skiller lokal bygging fra orkestratorens senere leveringsporter.
Gjeldende utfall og faktiske hasher står i verification.json og
delivery-manifest.json når kontrollarkivet er ferdig. Gamle journaler gjelder
sine egne kandidater, ikke automatisk denne kandidaten.

| Krav | Lokal bevisinngang | Grense |
| --- | --- | --- |
| Før-kode-kontrakt | docs/perioderegister.md, commit 407fdbc | Ingen stille modellutvidelse av gamle formater |
| Fullmakt og roller | source-findings.md; kildeavstemming av alle 130 katalogfiler | 346 gir ingen ny AmountObservation eller monetær hendelse |
| To innganger og tellerfasit | Faktiske par i kontrollarkivet; utvalgsjournal | /1 7/3, /22 4/2, begge 11/5; feil år/tomt/fullmakt 0/0 |
| Globale kandidater/hull | 67/25/7 i alle komplette utvalg | 60 åpne forekomster, ingen positiv M21 |
| Filgjenlesing/offline | JSON/XLSX-par og offentlig CLI med sperret nett/SQLite fra tom mappe | Kode og pinned runtime er nødvendige; originalrot er unødvendig |
| Semantiske negativer | negative_pairs i verification.json | Samme forgiftede kapsel passerer containerporten før semantisk avvisning |
| Presentasjon og ressursvern | Faktiske celletyper/tallformat/lenker/synlighet, renderinger og målte størrelser | Arvede ZIP/XML-/base64-vern og gamle grenser beholdes |
| Kompatibilitet og nye vedtak | Hashkontrollerte eldre kopier; fire separate ordinære 368-forløp | Ingen regenerert fil omtales som en gammel original |
| Full lokal suite og statikk | checks/ | Faktisk kjøring, ingen påstand om Linux-CI |
| Standards/Spec/sikkerhetsaudit | Orkestratorens etterfølgende porter | Ikke utført av byggeren |
| PR/full CI/merge | Orkestratorens etterfølgende publisering | Ingen commit/push/PR/GitHub-mutasjon av byggeren |

Native Excel, selvstendig gammel frozen-v1-JSON og den gamle 554e-fullresponsen
er fortsatt egne bevisgrenser. Uendret 2024-regneport gir bare avgrenset
kontroll, 166 039 000 og 29 185 000 kroner. Ingen årsbalansegodkjenning,
kontokontinuitet, ny B5-avgjørelse, drift eller neste ticket er levert.
#10/#32/#37 holdes åpne.

Den avsluttede filkontrollen tok 1 106,234 sekunder. De 36 ordinære utvalgs-/
navigasjonsparene, en offentlig offline-CLI og fire separate tomme P1-par
gir 41 faktiske par. 23 negative par er kontrollert etter vellykket
containerpassasje med eksakt forgiftet kapsel. Åtte presentasjons-/DOCTYPE-
prøver og elleve ekstra container-/JSON-/ressursprøver er avvist.
De fire 368-databasene har hver 222 observasjoner / 74 hendelser og schema 5;
B5-seedregisteret og råkilden er uendret. 14 gamle par og én B6-bok gir
29 uendrede originalfiler. Rendererens 34 bilder er et separat, skrivebeskyttet
visningsbevis fra faktiske bøker, med native Excel uttrykkelig uprøvd.

Den endelige fulle lokale kjøringen bestod: **1 179 bestått, to eksisterende
Windows-rettighetsskips, 2 600,31 sekunder**. Målt prosessveggtid var
2 601,133 sekunder. Alle 24 P1-prøver bestod; JUnit summerer 177,631 sekunder
for disse tilfellene, inkludert deres tilordnede fixturetid. De åtte kjørbare
kandidatfilene hadde identiske SHA-256 før/etter hele fullsuiten.
Ruff check, Ruff format (131 filer) og mypy (76 kildefiler) består.

De to skipene gjelder symbolsk databasealias/OS-lås og hardlink til
kontrollreferanse, der Windows-kontoen svarte manglende rettighet/Access
denied. De er ikke godskrevet som beståtte plattformprøver. Full Linux-CI
og dens faktiske kjøretidsmargin gjenstår; ingen tester, parserversjonslogging,
gamle ressursgrenser eller CI-grenser er fjernet eller redusert.
