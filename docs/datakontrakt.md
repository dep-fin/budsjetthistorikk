# Datakontrakt – B1-resultat og B2-kildeversjoner

Dette dokumentet beskriver implementert B1/B2. [Felles observasjonsformat versjon 1](observasjonsformat.md) er den besluttede spesifikasjonen for videre modellering fra #6, med historisk Excel-kompatibilitet. Formatet endrer ikke dagens API eller databaseskjema; se [ADR 0003](adr/0003-felles-belopsobservasjoner.md).

Kontrakten ligger i `innlesning/model.py`. Innlesningens offentlige grense er `import_saved(database, raw_response, metadata, decision_id, historical_sample=False)`, `read_report(database, run_id)` og `read_source(database, sha256)`. Nettadapteren `fetch_session(session, timeout=30)` leverer råbyte og hentemetadata. Eksportgrensen er `analyse.export_excel(database, run_id, output)`.

## Kilde, identitet og struktur

SQLite-tabellen `sources` lagrer faktisk innlest respons som BLOB, identifisert med SHA-256. `runs` lagrer kjørings-ID, kildehash, komplette medsendte hentemetadata, kontrollstatus, full vedtakstekst og metadata for valgt vedtak. `allocations` lagrer postrader med kobling til kjøringen. Råbyte og resultat skrives i samme transaksjon. `read_source` returnerer de samme bytene som faktisk ble lest inn.

Hentemetadata krever `url`, `retrieved_utc` med tidssone, HTTP-`status=200`, `sha256` og `bytes`. URL må ha den kanoniske formen `https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=ÅÅÅÅ-ÅÅÅÅ`, med to påfølgende år fra 2000–2099. URL-format, hash og byteantall valideres før import. En gyldig kilde-URL som avviker fra XML-sesjonen, bevares som en separat identitetsfeil med status `innlesningsfeil`. `headers` bevares når de er oppgitt. `fixture_kind=http_original` betegner en hel HTTP-respons; eldre metadata uten dette feltet behandles som originalrespons. `derived_excerpt` og `synthetic_test` er uttrykkelige prøveslag. Proveniens og foreldrehash for den autentiske fixturen finnes i sidevognen. Prøvens hash erstattes aldri av foreldrefilens hash.

Valgt vedtak har original ID, nummer, sak-ID, sesjon fra XML-responsen, rå datoverdi, vedtaksdato, API-type, tittel, rå og normalisert kildelenke og hele HTML-feltet. Datoen viser en kalenderdato; kildens midnattstid tolkes ikke som faktisk vedtakstidspunkt. Budsjettår leses fra den uttrykkelige innledningen og holdes adskilt fra sesjon.

Hver postrad har rå kapittel-/postidentitet, kapittelnavn, formål, beløpstekst, heltall i kroner eller `None`, retning, beløpsbetydning, kilderad, kontrollstatus, begrunnelse og radens HTML. Kildepekeren `table[1]/tr[n]` teller fra 1 og inkluderer overskriftsraden. Linjens øvrige vedtaksmetadata følger fra det tilhørende vedtaket i rapporten.

Beløpsbetydningen i denne grensen er **opprinnelig bevilgning**, et nivå for budsjettåret. Endringsbeløp, førbeløp og etterbeløp er ikke relevante og eksporteres som tomme felt. Retning følger kapittel: 1–2999 utgift og 3000–5999 inntekt. Ukjent kapittel gir kontrollbehov. Departement og Gul bok-gruppe utledes ikke; departementstilknytning står uttrykkelig som uavklart i Excel.

## Status og summer

- `strukturert`: det avgrensede originaltabellmønsteret er gjenkjent, postbeløpene er entydige, alle innholdsrader er klassifisert og de to kilde-totalene stemmer.
- `til kontroll`: valgt vedtak og råtekst er bevart, men mønster, beløp eller kontrollgrunnlag er uavklart. Entydige delrader kan bevares. Rapportens `approved_totals` er `None` for begge retninger, og Excel viser ufullstendig grunnlag.
- `innlesningsfeil`: valgt vedtak mangler, XML er ugyldig, tekst mangler eller identitet/sesjon ikke stemmer. Mottatte råbyte og kontrollgrunnen bevares når proveniensen er gyldig. Ugyldig proveniens, transportfeil og for stor respons avvises før import og gir CLI-feil.

`strukturert` gjelder struktureringen av valgt vedtak. Statusen godkjenner verken departementstilknytning, andre vedtak eller en additiv historikk. Kildens totalrader er kontrollopplysninger i `source_totals`; de blir aldri ekstra postbevilgninger. Manglende og tvetydige beløp er `None`, mens et uttrykkelig tall 0 er null kroner.

## Bruksgrense

Eksporten leser bare én eksplisitt kjørings-ID. Hver ny import får en ny kjøring; gjentatte importer skal ikke summeres sammen. B2 håndterer løpende synkronisering og kilderettelser; et samlet uttrekk tilhører B6. Det finnes ingen automatisk «siste gyldige versjon» i B1.

Bare den dokumenterte originaltabellen er kontrollert. Ukjent tabelloppsett, flere tabeller, uklassifisert innhold eller manglende enhet gir kontrollbehov. Generell behandling av underposter, fullmakter, regjerings-/komitéforslag og senere endringsvedtak er ikke implementert. Produksjonsgrensen er fortsatt sesjon 2026–2027; historiske prøver krever et uttrykkelig valg.

## B2 – kildeinventar, observasjoner og revisjoner

B2s kontraktversjon er `2`; de bevarte struktureringsresultatene bruker fortsatt B1s `Report` versjon `1`. Parseren er `b1-original-v1`. Dette utvider kildeinventaret og versjonsføringen, uten å utvide hvilke bevilgningstabeller som er faglig strukturert. Alle ID-er og API-typer i hele sesjonssvaret inngår. Verken dato, BUDSJETT, standardtekst, proposisjon eller innstilling er et inngangskrav. Ukjent, velidentifisert tekst blir en bevart revisjon med `til kontroll`, uten godkjente summer. En slik ny revisjon erstatter tidligere innhold som observert kildegrunnlag; gamle godkjente beløp brukes ikke som reserve.

### Offentlige interfaces

- `stage_sync(database, raw_response, metadata, *, historical_sample=False, decision_id=None) -> job_id` validerer proveniens og bevarer råbyte og jobb som `venter`. Kalleren får gjenopptaks-ID før publisering.
- `resume_sync(database, job_id) -> job_id` bruker bare den lagrede jobben. Fullført eller feilet jobb returnerer sitt eksisterende resultat uten nye observasjoner eller beløpsrader.
- `sync_saved(...) -> job_id` er snarveien for de to trinnene. Ved avbrudd som gir Python-unntak følger gjenopptaks-ID som unntaksnotat. Bruk de to uttrykkelige trinnene når ID må sikres før prosessen kan stanses.
- `read_sync(database, job_id) -> SyncReport` viser immutable kjøringsgrunnlag: scope, datasett, kildehash, komplette hentemetadata, kilde-/kjøretider, parser-/hashversjon, feil og observasjoner per ID. `counts` skiller `ny`, `uendret`, `rettelse` og `mangler`; `control_count` og hver observasjons kontrollgrunner viser uavklart strukturering og fravær. «Ingen nye» er ikke det samme som feilfritt.
- `read_revision(database, revision_id) -> RevisionReport` gir eksakt valgt innhold, separat råhash, bevart objekt-XML og immutable struktureringsresultat. Dynamisk ferskhetskontekst og kontrollhenvisninger er merket med vurderingstidspunkt, nåværende revisjon/observasjon og siste forsøksstatus.
- `read_revision_for_run(database, run_id)` knytter bare B2-registrerte resultater til en revisjon. Et B1-resultat returnerer `None`; det blir ikke adoptert gjennom lesing.
- `record_control_reference(database, revision_id, reference, reason, *, locator=None)` bevarer et begrunnet valg eller en ekstern referanse med registreringstid, revisjon og observert innholdsovergang. Valg/referanse, begrunnelse og valgfri locator kan hver ha høyst 32 767 tegn; lengre verdier avvises med `ValueError` før registrering, slik at Excel-eksporten bevarer hele teksten i én celle. Valgfri locator må finnes i revisjonens postrader. Nye henvisninger krever gjeldende observert revisjon. Funksjonen endrer eller godkjenner ingen beløp. Kontrollfilimport og faglig virkning av manuelle endringer tilhører B5.

### Identitet og fingeravtrykk

Råhashen er SHA-256 av faktisk innleste, uendrede byte og beholder B1-betydningen. Vedtakets identitet er `(datasett, vedtakssesjon, original ID)`. Dato, nummer, sak, tekst og like beløp under forskjellige ID-er slår aldri sammen vedtak. Revisjonen er unik på identitet, fingeravtrykksmetode og innholdsfingeravtrykk. Den har egen revisjons-ID og ett uforanderlig struktureringsresultat; senere observasjoner gjenbruker dette resultatet.

`xml-object-v1` hasher UTF-8-kodet kompakt JSON med utvidet XML-elementnavn, sorterte utvidede attributtnavn/verdi-par, elementets tekst og ordnede barn med haletekst. Hele vedtaksobjektet inngår, også ukjente felt, type/navn, sakslenke, attributter og nil. Manglende felt, tomt felt og nil gir forskjellig struktur. XMLs standard normalisering av linjeskift/entiteter skjer ved sikker parsing; namespace-prefikser og attributtrekkefølge har ingen betydning. Kommentarer og prosesseringsinstruksjoner inngår ikke, men omkringliggende tegninnhold, også haleteksten deres, slås sammen og bevares. Bare ren XML-innrykkstekst mellom elementer uten blandet tekstinnhold ignoreres. Løvtekst, HTML-streng, blanktegn i HTML, fortegn og tabellstruktur bevares. `xml:space='preserve'` på elementet eller arvet fra objektets foreldre bevarer også separatorene i undertreet; nærmeste lokale `xml:space='default'` opphever arvet `preserve`. Fingeravtrykket er en konservativ innholdssammenligning, ingen generell semantisk HTML-normalisering.

Konvoluttens `respons_dato_tid`, HTTP-headere og hentetid er observasjonsproveniens og inngår ikke i vedtaksfingeravtrykket. Konvoluttens kildeformat `versjon=1.6` kontrolleres eksplisitt; ukjent versjon gir feil og må kompatibilitetsvurderes. Normaliserings- og parserversjon lagres separat. Ny parser er ikke i seg selv en kilderettelse.

Ved A → B → A gjenbrukes innholdsrevisjon A, og en ny observasjon registreres. Aktiv peker og siste observasjon oppdateres selv om innholdet finnes fra før. Overgangstelleren endres ved hvert innholdsskifte. Kontrollhenvisninger fra første A forblir `utdatert` etter tilbakekomsten. Bare endret konvolutttid gjør dem ikke utdaterte. Et nyere feilet/ventende forsøk, en manglende ID eller et valgt omfang som ikke vurderer vedtaket gir `ikke vurderbar` når henvisningen ellers passer aktivt innhold. Utdatert innhold blir aldri automatisk gjeldende kontrollgrunnlag igjen.

### Fullt og valgt omfang, prøver og feil

Uten `decision_id` sammenlignes hele listen. `derived_excerpt` krever uttrykkelig valgt ID og kan ikke utløse fraværsavstemming. `session_coverage=partial` avvises i full modus. Syntetiske fullsesjonsprøver krever både `fixture_kind=synthetic_test` og `session_coverage=complete`. `http_original` er standard når eldre hentemetadata mangler prøveslag. Ukjente prøveslag avvises.

Datasett `produksjon` brukes bare for ordinære originalresponser. `historical_sample=True`, avledede utdrag og syntetiske prøver bruker `prove`, med adskilte hoder, observasjoner, ventende jobber og tidsrekkefølge. Rå-BLOB-er kan deles fordi de bevarer identiske byte. Eldre sesjoner krever fortsatt eksplisitt historisk prøve. Prøvemerking og proveniens er inngangsdata fra kalleren; løsningen kan ikke autentisere en lokalt redigert sidevogn.

Gyldig proveniens bevares før XML-behandlingen. Feil rot/navnerom/sesjon, trunkert XML, DOCTYPE, manglende/duplisert/nil liste, ukjent listestruktur, gjentatt ID, tvetydige påkrevde objektfelt og motstrid mellom ID, sak-ID og kanonisk vedtakslenke gir `feilet`. Ingen deler av det nye inventaret publiseres. Manglende påkrevd tekst følger B1s feilgrense. En eksplisitt tom, syntaktisk gyldig liste er derimot en faktisk observasjon. Tidligere kjente ID-er som mangler i et gyldig fullt svar får `mangler`; deres siste hode og alle kilder beholdes. Det er ikke en slettings- eller tilbaketrekkingsmelding. Syntaktisk komplett svar beviser ikke faglig fullstendighet.

Kildens responstid og sidevognens hentetid normaliseres til UTC ved gjenopptak, også for første jobb. Et gyldig ISO-tidspunkt som faller utenfor støttet UTC-område, gir en bevart `feilet` jobb med råbyte, metadata og feilgrunn. Jobben blokkerer da ikke en ny synkronisering.

### Atomisk publisering og rekkefølge

Staging lagrer rårespons og jobb i én transaksjon. Publisering bruker `BEGIN IMMEDIATE` og én transaksjon for nye revisjoner/resultater, alle observasjoner, aktive pekere og fullføring. Feil under publisering ruller hele publiseringen tilbake og lar jobben stå `venter`. Ingen delvis oppdatert sesjon blir synlig. Gjenopptak trenger ingen kildefil eller nett; ny kilde kan ikke sendes til samme jobb. Gjenopptak av fullført jobb returnerer samme rapport uten ny skriving. En ny kjøring på samme kilde kan gi ny observasjon, men ingen nye vedtak, revisjoner eller beløpsrader.

SQLite håndhever én ventende jobb per datasett/sesjon med en unik indeks. Den må gjenopptas før ny jobb tillates. I publiseringstransaksjonen avvises eldre jobbsekvens, lavere kilde-responstid eller lavere bevart hentetid enn siste vellykkede jobb. Gamle manuelle HTTP-snapshot kan derfor ikke stille overskrive nyere kilde. Tilbakekomst A er bare en ny aktuell observasjon dersom tidsrekkefølgen tillater den. Dette er en lokal, konservativ regel, ingen påstand om utgivers autoritative revisjonsrekkefølge. For en bevisst historisk replay brukes en separat prøvedatabase; ikke endre tidsmetadata for å få en gammel kilde forbi kontrollen.

### Additiv lagring og B1-kompatibilitet

Før B2-skriving valideres B1-tabeller og kolonner. En tom database eller uversjonert B1-database (`PRAGMA user_version=0`) initialiseres/oppgraderes i samme eksplisitte transaksjon til skjemaversjon `2`. Ingen B1-tabell eller kolonne slettes, bygges om eller renses. Nye tabeller er `sync_jobs`, `decision_revisions`, `decision_heads`, `sync_entries` og `control_references`. SQL-innsettinger navngir kolonnene. Ukjent skjemaversjon avvises ved både lesing og skriving. B1-lesing krever ingen skrivemigrering; B1-skriving fungerer fortsatt etter B2-oppgradering og endrer ikke B2-inventaret.

Gamle B1-kjøringer bevarer sine ID-er, byte, metadata og tall. De er historiske prøverapporter, ikke et kanonisk register over forskjellige vedtak. B2 hevder ikke at gjentatte B1-kjøringer allerede er dublette stortingsvedtak. Automatisk adopsjon eller rekonstruert gjeldende tilstand fra B1 inngår ikke; dette krever en egen, uttrykkelig migreringsregel dersom det senere ønskes.

### Versjonsvalgt Excel

`analyse.export_revision_excel(database, revision_id, output)` og `analyse --revisjon` eksporterer ett valgt innhold. `export_excel` og `analyse --kjoring` består og viser B2-kontekst når resultatet har en B2-kobling, ellers «B1-prøvearkiv». Valgene er gjensidig utelukkende. Eksport leser bare lokalt lagret grunnlag og bytter aldri til latest eller henter nett.

En historisk A-eksport beholder As åtte beløp og As råhash etter B. Revisjons-ID/fingeravtrykk/metode, parser, valgt råhash, nåværende revisjon, siste observasjonsråhash og siste forsøksstatus er separate felt. Historisk/gjeldende innhold og vurderingstid er tilleggskontekst; det gamle resultatets tall og struktureringsstatus endres ikke. Arket `Kontrollhenvisninger` viser opprinnelig grunnlag, valg/referanse, begrunnelse, registreringstid og gjeldende/utdatert/ikke vurderbar status. Dette er ingen samlet sesjonsbevilgning, kontrollfilimport eller additiv historikk.

## B3 – beløpsobservasjoner og valgt historikk

Faglig format er [observasjon-1](observasjonsformat.md). Lagringsvalget er [ADR 0004](adr/0004-b3-lagring-og-utvalg.md). Formatversjon, Storting-adapter `storting-belop-v1`, beregningsregel `vedtatt-kjede-v1` og SQLite-versjon 3 er forskjellige versjoner. B2s `PARSER_VERSION=b1-original-v1`, fingeravtrykk og lagrede resultater er uendret.

### Innlesning

`extract_revision(database, revision_id, *, interpretation=None)` tolker én eksplisitt B2-revisjon offline og gir en immutable `Extraction`. `Interpretation` identifiserer adapter, normaliseringsregel, begrunnelse og eventuelt kildebelagt rundevalg. `Extraction.id` kan leses igjen med `read_extraction(database, extraction_id)`. Samme revisjon/tolkning gjenbruker samme kildegrunnlag og observasjons-ID-er. Første råresponspeker forblir uttrekksgrunnlaget; senere B2-kildeobservasjoner vises separat.

`save_extraction(database, extraction, raw)` er den generiske adaptergrensen. Den kontrollerer artefakthash, byteantall, observasjonenes kilde-/tolkningsgrunnlag, kontoens normalform, heltallsgrense og identitetskollisjoner før atomisk lagring. Dataklassene i `innlesning.observations` representerer rå og normaliserte kontokoder, underpost/nivå/relasjoner, årstolkning, valgfri dato/API-ID, rå celletype/verdi/formel/lagret verdi, enhet/presisjon/normaliseringsbevis, uavhengige faglige akser, historisk organisasjon og flere dokumentreferanser. Nullable observasjonsfelt får navngitt nullgrunn; kildepeker, organisasjon og dokumentreferanser har egen grunn for ikke oppgitte metadata. Ingen Excel-filadapter følger av dette API-et. `Extraction.import_id`/`imported_utc` kan peke til det opprinnelige importgrunnlaget; B3s faktiske lagringstid bevares separat i tabellen.

Storting-adapteren støtter én tabell med de kildekontrollerte 4-, 5- og 6-cellers hodene `Kap./Post/Formål/[tom]/Kroner[/Kroner]`. Den krever ett uttrykkelig budsjettår i vedtakstekst, eller i tittelen når teksten ikke angir år. Flere år eller tabeller, ukjent enhet, tvetydige celler og ukjent nivå/endring gir kontrollbehov. Feil i HTML-behandlingen, også overskredet sikkerhetsgrense, gir synlig adapteravvik og ingen delvis tolkede beløp; fullteksten beholdes i B2. En mulig kapittelrad som ikke kan tolkes opphever arvet konto. Ukjent celleantall, rowspan eller colspan opphever også arvet kapittel og post, selv med blank første celle. Avviket får uavklart konto og sperrer potensielt berørte utvalg fremfor å arve forrige posts filter. I et kjent celleoppsett kan en uavklart, utfylt postcelle avgrenses til det dokumenterte kapittelet, men aldri til forrige post. Fullteksten og radlokatoren bevares for kontroll; ingen kontokode eller beløpsbetydning gjettes fra det ukjente oppsettet. En entydig originalinnledning gir opprinnelig nivå. Retningsord gir fortegn til et eksplisitt delta. «(Ny) … bevilges med» er en endring med ukjent inngående beløp. Fra-/til-raden får to egne observasjoner i samme ledd. Struktureringsstatus i B1 brukes ikke som godkjenningsstempel i B3.

RNB og nysaldering klassifiseres bare ved uttrykkelig vedtakstittel eller eksplisitt `Interpretation(round=..., round_evidence=...)`. Andre runder kan være `uavklart`. Dato bestemmer aldri behandlingsrunden. Uavklart runde alene skjuler ikke et ellers entydig, datert delta. Ukjent talltype, beløpsrolle eller omfang sperrer kjeden. Underpost- og nettoresultatmønstre utover dette snittet har kontrollavvik; modellen bevarer plass, mens generell tolkning følger #7.

### Beregning

`calculate_history(database, HistorySelection(...))` krever datasett, uttreks-ID-er, år og konto. Uttreks-ID-en velger både revisjon og tolkning; ingen latest velges automatisk. Underpostutvalg krever konkret kode og `detail_level="underpost"`. Kode `0` er ikke det samme som ukjent. Ett utvalg kan ikke summere posttotal og underposter. Ukjent konto eller nivå i en valgt kilde som kan berøre utvalget bevares og sperrer avstemming; opplysningen filtreres ikke stille bort. Flere revisjoner/tolkninger av samme kildeenhet gir konflikt.

Regelen krever nøyaktig ett opprinnelig nivå først, deretter daterte, vedtatte enkeltendringer. Kildens dato gir rekkefølge bare når datoene er entydige. Lik eller manglende dato krever eksplisitt `step_order` med hvert valgt ledd og `order_evidence`; valg som strider mot kjente datoer sperres. Motstridende datoer innen samme ledd sperrer også med eksplisitt rekkefølge. En manglende dato på én observasjon opphever ikke andre kjente datoer i leddet. Forslag, regnskap, aggregater og fullmaktsrammer vises blant inn-observasjonene, men inngår ikke i saldoen. Før/etter brukes som kontroller. `før + delta = etter`, forrige saldo mot neste før og beregnet saldo mot etter kontrolleres når feltene finnes, også opprinnelig nivå mot leddets etterbeløp. Ukjent normalisering, manglende start, ukjent ledd eller konflikt gir `ufullstendig` og ingen avstemt saldo. Observerte sluttverdier beholdes også ved sperret kjede.

Resultatet lagres separat med ID, inn-observasjoner, regel, utvalg, tidspunkt, register-/kontrollgrunnlag, status, avvik og begrenset dekningsgrense. `read_history(database, calculation_id)` gjenåpner dette resultatet og føyer til nåværende kilde-/kontrollkontekst. B2-overgangsteller og kontrollhenvisninger inngår i grunnlaget. A → B → A gjør ikke gammel beregning gjeldende igjen. Feilet/ventende siste forsøk og fravær suspenderer avstemt saldo med aktuell kontekst. Et annet siste valgt B2-omfang vises som slik kontekst; det erstatter ikke det eksplisitt valgte historiske grunnlaget.

`status="avstemt_utvalg"` og egenskapen `approved_balance` betyr bare at den dokumenterte regneprøven av det begrensede utvalget består med samme grunnlag. Det er ikke en faglig godkjenning, et kontrollert fullstendig år eller en påstand om komplett sesjonsdekning. Observasjonenes faglige status er fortsatt `til_kontroll` til en særskilt vurdering finnes. Manuell kontrollimport, generelt registervedlikehold og avklaring av de historiske kildekonfliktene er utenfor #6.

### Excel og migrering

`export_history_excel(database, calculation_id, output)` gir arkene `Historikk`, `Beløpsobservasjoner` og `Grunnlag og kontroll`. De viser separate rå/normaliserte verdier, før/delta/etter, avledet saldo, kilderad og beløpsfelt, artefakthash, revisjon/tolkning, dokumentreferanser, organisasjon/nullgrunner, status, avvik og avgrensning. JSON-felt bevarer hele modellen; tekst over cellegrensen fortsetter i grunnlagsarket. Bevart og nåværende kontekst er separate. Kildetekst går gjennom B1s tekstsikre `put()`. Eksporten lagres atomisk og nekter databasen som Excel-mål. CLI-en beskytter også utvalgsfilen.

Første B3-skriving oppgraderer additivt til skjemaversjon 3 i én eksplisitt transaksjon. Ingen B1/B2-tabeller bygges om, råbyte omhashes eller kjøringer adopteres. B1/B2-lesing av versjon 0/2/3 krever ingen skrivemigrering. B2-skriving bevarer versjon 3, og ventende jobber kan gjenopptas etter oppgraderingen. Ukjent versjon avvises fortsatt.
