# Separat sikkerhetsaudit av T5/#62

**Portstatus: IKKE BESTÅTT på denne kandidaten. Ett P2-funn må rettes og etterkontrolleres.**

| Binding | Fast verdi |
| --- | --- |
| Kandidat | `d46589cb9e99338e44fc805ee9882006ba657fd0` |
| Kandidattre | `df0eed6d6e8a0b2a07962e641ae05d1194a3304d` |
| Base | `2f4ee30c9d8074076fc8042e208c4a4b6345db6b` |
| Checkout | `work/t5-prop16` |

Auditen omfatter hele faste diffen: modell, adapter, analyse, Excel-leser/-skriver,
kontrollhjelper, tester, dokumentasjon og nye kontrollartefakter. AGENTS,
arbeidsflyten, ansvarsdelingen, issue-reglene, hele publiserte #62 (ingen
kommentarer), T5-kontrakten, T1-kontrakten og relevante JSON/Excel-/kildegrenser
er lest. Andre kontrollørers nye reviewfiler er ikke vurderingsgrunnlag.
Sporede arbeidsfiler ble kontrollert mot den faste kandidaten før probene og
igjen etterpå. Ingen produktretting, staging, commit eller GitHub-mutasjon er utført.

## P2: Temafargen kan skjule gjeldende T5-status uten at Excel-leseren avviser filen

**Sted:** `analyse/proposisjon16_excel.py:290–291`, sammen med nye celler på
linje 59–60 og 69–73. `_style_profile` kontrollerer `xl/styles.xml`, mens
`read_excel` ikke binder `xl/theme/theme1.xml` til forventet presentasjon.

De nye datacellene i `Inventar!M:N` og `Kontoer!H` opprettes uten `put` eller
eksplisitt skriftfarge. De bruker standardfontens `color theme="1"`. En angriper
kan endre bare temaets `a:clrScheme/a:dk1` fra svart `windowText` til
`<a:srgbClr val="FFFFFF"/>`. De aktuelle status-/bindingscellene får da hvit
skrift på vanlig hvit, ufylt bakgrunn. Alle JSON-data, kildereferanser,
beløp, celleverdier, stilindekser, `styles.xml` og relasjoner kan beholdes.

Egen konkret prøve skrev og lukket en ekte produkteksport og endret bare dette
ene ZIP-medlemmet. `read_excel(accepted-theme-white.xlsx) == clean_report`
returnerte **True**. Leseren godkjenner dermed en bok som skjuler den synlige
forskjellen mellom historisk T1-status og gjeldende T5-status. Dette bryter #62s
krav om at faktisk presentasjon/synlighet kontrolleres, også når snapshotet er korrekt.

| Kontrollcelle i den aksepterte filen | Verdi | Faktisk font | Fyll |
| --- | --- | --- | --- |
| `Inventar!N2` | `strukturert_T5` | `theme=1` → hvit | Ingen |
| `Kontoer!H2` | `strukturert_T5` | `theme=1` → hvit | Ingen |
| `Inventar!M2` | Tre observasjons-ID-er | `theme=1` → hvit | Ingen |

Beviset er faktisk OOXML og leserutfall. Native Excel-rendering av angrepsfilen
er ikke utført; skjulingen følger den konkrete temareferansen/fargen i OOXML.
Det er ikke funnet makro- eller kodekjøring i denne prøven.

Anbefalt retting er å binde temaet til skriverens forventede profil og/eller
gi alle nye status-/bindingsceller eksplisitt kontrollert font/farge. Legg til
en offentlig leserprøve som endrer bare temaet. Den forgiftede filen må avvises,
eller alle relevante celler må beviselig beholde sin effektive presentasjon.
Gamle guardmoduler trenger ikke endres; vernet kan legges i T5-modulen.

## Egne prøveutfall

Endelig ledger er [results-final.json](results-final.json): **70 konkrete prober,
69 bestått, ett akseptert angrep (`theme_integrity`)**. Dette er egne prober,
ikke en ny kjøring av fullsuiten eller byggerens 35 tester.

- Faktisk JSON/XLSX-par ble skrevet, lukket og gjenlest. Gammel typet T1-basis
  er lik den autentiske fixturens basis. Nye felt er 105; full union er
  **123/6/2** gjennom offentlig visning. Gammel gzip-fixturs SHA-256 er fortsatt
  `629c3561cca6f0ab2a5644958c7ae6590dd70775d688f40e134bda449e8982a6`.
- 14 ulike semantiske forgiftninger ga 28 avvisninger gjennom faktiske JSON-
  og Excel-lesere: feil nullbeløp/null, rolle, år, betydning, step-ID, forfatter,
  råverdi, gammel vedtaks-step-ID, 1533-grenlekkasje, oppdelt felles ramme,
  falsk dekning, skjulte globale hull og feil binding. Nye identifiserte
  omslag/objekter ble rehashet. Hvert XLSX-arkiv hadde snapshot og presentasjon
  generert fra samme forgiftede rapport og passerte containerkontrollen;
  avvisningen kom fra semantisk original-/basisrekonstruksjon.
- JSON avviste duplikatnøkkel, ekstra felt, bool og desimaltall i heltallsfelt,
  NaN, Infinity og -Infinity. Over 64 MiB fil ble avvist før parsing.
- Typed adapter rekonstruerte identisk basis og avviste rehashet falskt beløp,
  falskt kildeverifisert innhold, ugyldig base64 og base64 over 16 MiB-grensen.
  En ny gzip på over 32 MiB utpakket ble merket motstrid og ikke dekomprimert;
  forsøk på å oppgradere den til kildeverifisert ble avvist. Katalogpinner,
  hash/størrelse og canonical kildeobjekt stopper dette før XML-parsing.
- Faktiske ZIP-/XML-prøver avviste ekstern relasjon, DOCTYPE, skjult ark,
  uventet/traverserende medlem, rå skriftendring, formel, numerisk null som
  tekst, duplisert celle/ZIP-medlem og over 128 MiB deklarert utpakket størrelse.
- Offentlig manuell relasjon tok inn mer enn 60 000 tegn med formellignende
  `HYPERLINK`-tekst. Faktisk lagrede/gjenleste Excel-celler var tekst, uten
  formelceller; dekodet relasjonsgrunn og ordnede videreføringer var tapsfrie.
- Begge offline-lesere bestod med cache tømt og `socket.socket` samt
  `sqlite3.connect` sperret. Egen `--frosset`-CLI bestod med kilde-rot som ikke
  finnes. Ingen kildehenting eller database åpnes av denne leserstien.
- No-clobber beholdt eksisterende JSON-/XLSX-hasher og avviste eksisterende
  originalkatalog. En faktisk Windows-publiseringsrace opprettet målfila
  umiddelbart før atomisk publisering; eksporten avviste, vinnerens byte bestod,
  og midlertidig JSON ble fjernet.
- Alle **25** eksporterte originalpayloads ble sammenholdt byte for byte med
  den validerte selvforsynte kapselen. 21 ble også sammenholdt med direkte
  eksisterende repositoryfiler. Det øvrige eksporterte elementet er `index.json`.
- Fire reelle manglende/feilede/korrupte/motstridende T5-importer ble fulgt av
  ordinær 40034229-synkronisering, rålagring, v2-tolkning, SQLite, analyse og
  Excel. Alle bestod med **222 observasjoner / 74 hendelser**.

[artifact-checks.json](artifact-checks.json) binder dessuten alle 35 oppføringer
i leveransemanifestet til faktiske kandidatblobber (størrelse, SHA-256,
Git-blob-ID og oppgitt LF-representasjon). Alle åtte nye JSON-artefakter bestod
streng syntakskontroll; åtte PNG-er bestod signatur-/CRC-/størrelseskontroll.
PNG-kontrollen er ingen visuell QA eller full billeddekoding.

Baseinventaret har 1183 filer. **1181 har identiske Git-objekter**; bare de to
additive kontekstpekerne i AGENTS/kildefunn er endret. Dette omfatter gamle
produktmoduler, CLI-standarder, schema 5/B5, fixtures, kildeoriginaler,
registerfiler og CI-konfigurasjon. T5s nye kildekatalog er eksplisitt og pinnet,
og originalstier kontrolleres mot valgt rot. Ingen ny primærkilde er hentet.

## Reproduksjon og bevisgrenser

[probes.py](probes.py) tar eksplisitt rot, kandidat, base og nytt outputnavn.
Publiserte tilsvarende commit-ID-er med samme tre kan brukes; ingen utilgjengelig
lokal SHA er eneste replaymodus. Fra en checkout med kandidatens sporede filer:

```powershell
python docs/research/proposisjon16-62/reviews/security/probes.py --root . --candidate KANDIDAT --base BASE --output .local/security/replay
python docs/research/proposisjon16-62/reviews/security/artifact_checks.py --root . --candidate KANDIDAT --base BASE --output .local/security/artifact-checks.json
```

Det er forventet at `theme_integrity` viser akseptert angrep på dette faste treet.
Filer som gir det konkrete funnet ligger i den utførte kjøringen under
`.local/security/audit-2`; deres hasher er ført i endelig ledger.

Første harnesskjøring stoppet på forventet `FileExistsError` som harnesset bare
fanget som `ValueError`. Harnesset ble rettet, og komplett kjøring gjennomført.
To kontrolluttrykk i komplett kjøring ble deretter etterkontrollert med
[verify_outcomes.py](verify_outcomes.py): gamle monetære hendelser skal telles
i offentlig visning, og relasjonsgrunn med anførselstegn/linjeskift skal
sammenlignes etter JSON-dekoding. Begge produktutfall var riktige. Korreksjonene
og de tidligere harnessverdiene står eksplisitt i ledgeren. Kun disse
etterkontrollene og den cachetømte offline-prøven ble gjentatt; fullsuiten er
ikke kjørt. De korrigerte uttrykkene inngår nå i replayprogrammet.

Audit av `ops/proposisjon16_proeve.py` omfatter kilde-/artefaktlesing,
originaleksport, prosessargumenter og refbinding. Hjelperen er et lokalt
repositorykontrollprogram som kjøres fra en valgt checkout, ikke en generell
leser for ubetrodde arkiver. Denne auditen er bundet til programmets og de
lokale fixturefilenes faste Git-objekter. Ingen generell infrastruktur eller
nytt kildeinnsamlingssystem er krevd.

Ingen full Linux-CI, native Excel-aksept, helårsdekning, nye monetære vedtak,
merge eller driftsaksept er dokumentert av denne auditen. Atomisk publisering
er kontrollert per fil; det er ikke påstått en transaksjon over begge filer i
`export_pair`. POSIX-publisering og Windows-junction-racer er vurdert ved
kodelesing, ikke kjørt i dette Windows-miljøet. Uavhengig kilde-/Excel-QA og
Standards/Spec er andre kontrollporter.

**Neste nødvendige steg:** rett temafunnet og kjør målrettet negativ Excel-prøve
og sikkerhetsetterkontroll på ny fast kandidat før porten kan godkjennes.
