# T3: byggerekkefølge og testsløyfer

27. oktober 2026, isolert `work/t3-forlop`, base `c1cb156d`.
Dette er en gjennomføringsjournal, ingen selvstendig review/audit eller CI.
Alle pytest-kall brukte Python3.12 og repoets pinnede pakker. Sluttkandidatens
fullsuite og filhasher dokumenteres separat i `verification.json`.

1. Startgrunnlaget var AGENTS, arbeidsflyt, issue #46/#37 med kommentarer,
   relevante kontrakter/ADR, kilde-/fane-/CI-undersøkelser og utforskerens scope.
   #1/#32/#41/#44 og relevante kommentarer ble også gjenlest direkte fra GitHub
   under byggingen; utforskergrunnlaget hadde allerede deres relevante grenser.
   De eksisterende høye original-/filgrensene er avtalte i #1/#46; ingen ny
   testgrense ble innført. `docs/forlopspilot.md` ble opprettet før første
   produktfil, med valgt 857-representasjon, separat regel og ressursgrenser.
2. Første tracer prøvde offentlig original→basis→konto. `pytest
   tests/test_forlopspilot.py -q --basetemp work/t3-red-01` feilet ved import:
   `ModuleNotFoundError: analyse.forlopspilot`. Produktmodulene ble deretter
   innført. Første grønne grunnlag: **1 bestått / 1,00 s**, `t3-green-02`.
   Den første kontrollparregexen manglet objektets avsluttende CRLF; den ble
   korrigert til nøyaktig kildeintervall, uten endring i fixture/sidevogn.
3. Neste tracer prøvde faktisk skrevet og gjenlest T1-union/JSON/XLSX.
   `t3-red-03`: **1 bestått / 1 feilet**, manglende `analyse.forlopspilot_excel`.
   Egen T3-skriver/leser ble innført etter T2-profilen. `t3-green-03`:
   **2 bestått / 35,24 s**. Dette er en tidligere byggetilstand, ikke endelig aksept.
4. Utvidet samme offentlige grenser til utvalg/navigasjon, rehashede faktiske
   JSON-/XLSX-negativer, falsk/skjult visning, inkompatible regneinnganger,
   analysefri adapter og fire separate autentiske 368-prøver gjennom offentlig
   kjerne-CLI. `t3-slice-04`: **45 bestått / 160,40 s**. Senere ble nivåets kode
   korrigert til observasjon-1s `nivaa`; gamle formater endret seg ikke.
5. Rendering av den første faktiske boken viste datoceller som serienummer
   (45279/45464), selv om openpyxl gjenleste korrekte datoverdier og formatet
   `dd.mm.yyyy`. Et isolert minneforsøk prøvde ISO, escapede punktum og skråstrek.
   `dd"."mm"."yyyy` viste 19.12.2023/21.06.2024 riktig. Produktformatet og en
   faktisk filregresjon ble rettet. Beløp/datoer forble typede; ingen fil ble
   skrevet om gjennom Artifact Tool. CLI-lesing av T1-input ble samtidig
   begrenset til 64 MiB før dekoding.
6. Kildeinventaret ble gjennomgått mot faktiske total-/SDØE-rader. En ny offentlig
   original→basis-prøve var rød: **1 feilet / 1,94 s**, fordi 857 feilaktig listet
   /22 som positivt dokumentmedlem. Totaler arvet også tidligere post. Ny
   inventarregel holder uttrykkelige postkolonner/tilgrensende før-/etter adskilt
   fra total-/komponentkontekst. Rød/grønn-seamen er den samme offentlige
   adaptergrensen. `t3-green-inventory`: **2 bestått / 2,21 s**.
7. De to første lokale artefaktrundene (`builder-01`/`builder-02`) beholdes som
   tidligere, ufullførte byggetilstander. De er ikke sluttaksept: før-kandidatens
   filer var laget med tidligere visnings-/inventarregler og avviker ved den
   senere offentlige CLI-kontrollen. `builder-03` fullførte deretter 20 par og
   gamle kompatibilitetskontroller på den rettede datamodellen (611,14 s).
   Sluttprojeksjonen merker i tillegg arvede dekningsavvik med `T1-kapsel:`:
   den gamle kapselens «opprinnelig/RNB ikke importert» må ha synlig gammelt
   omfang når T3 viser de nye vedtakene. Originalstrengene i kapselen og de
   nye kilde-/rapport-ID-ene er uendret. Den siste fullstendige runden bruker
   **`builder-04`**, med ny eksport/gjenlesing, uten å overskrive eldre runder.
   Ops-journalen fjerner én unødvendig ekstra gjenlesing per par: hver skriver
   har allerede lukket/gjenlest sin fil mot samme rapport, og faktisk Excel-
   snapshot kontrolleres fortsatt mot faktiske JSON-byte. Utvalg/vern er uendret.
8. Avsluttende uendrede produkt-/testfiler: Ruff check/format og mypy består.
   **Hele pakken: 1118 bestått, to eksisterende Windows-rettighetsskips,
   1512,57 s**, med alle 46 T3-prøver bestått. Ny kjørt fullsuite er logget,
   JUnit-tider og kilde-/filhasher er bundet i `verification.json`.

Ingen gammel kilde, arkivfixture, kilde-ID, B5-binding, schema eller gammel
leser er omtolket i sløyfene. Samlet review/audit og Linux-CI er egne porter
hos orkestratoren. Byggeren har ikke staget, committet, pushet eller merget.
