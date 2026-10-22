# B8: kontroll av Stortingets saksdokumentmetadata

Kontrollert 22. oktober 2026 for #28. Kilde: Stortinget. To avgrensede, komplette API-responser er hentet uten innlogging og bevart som faktiske HTTP-responsbyte. Nettsidene nedenfor er supplerende kontroll; de erstatter ikke API-originalene. Dette er ingen årsdekning eller beløpskontroll.

## Dokumentert grensesnitt og innhenting

[Stortingets dokumentasjon for sak](https://data.stortinget.no/dokumentasjon-og-hjelp/sak/) angir `GET https://data.stortinget.no/eksport/sak?sakid=<ID>` og rot `detaljert_sak`. Den beskriver `publikasjon_referanse_liste` og `sak_relasjon_liste`; en publikasjons `eksport_id` er bare utfylt når eksport finnes. Publikasjonstype og undertype er egne felt. Sakens `status=behandlet` beskriver komitébehandling; `ferdigbehandlet` må leses separat. Dokumentasjonen ble kontrollert før API-hentingen.

[Dokumentasjonen for publikasjon](https://data.stortinget.no/dokumentasjon-og-hjelp/publikasjon/) beskriver et eget endepunkt som tar `publikasjonid`, og skiller XML fra HTML-representasjonen. B8-prøven henter bare saksmetadata; den har ikke hentet eller tolket selve proposisjonen, innstillingen eller referatene.

Første nettleseforsøk fra den begrensede shellen feilet med DNS-feilen `No such host is known`. Begge vellykkede API-hentinger brukte godkjent utvidet nettverkstilgang. Feilforsøket ga ingen rårespons og ingen oppfunnet hash.

| Sak og API-kilde | Byte | SHA-256 | HTTP-status |
| --- | ---: | --- | ---: |
| [100927](https://data.stortinget.no/eksport/sak?sakid=100927) | 12 383 | `2ee25b327b78772523d56317c752e35f5134eef60db9536f6dea3c94ad8fed27` | 200 |
| [100889](https://data.stortinget.no/eksport/sak?sakid=100889) | 15 888 | `3a8f0918a3fcce90bf2c93f3ce972c3de7277c76e27e5ef563d6c43384cf2af2` | 200 |

Originaler og transportmetadata finnes i [fixturmappen](../../../tests/fixtures/b8/README.md). Begge er UTF-8 XML med CRLF, navnerom `http://data.stortinget.no`, XSI-navnerom `http://www.w3.org/2001/XMLSchema-instance` og `versjon=1.6`. Ingen DOCTYPE er observert. `Content-Type` var `text/xml; charset=utf-8`. SHA-256 er beregnet på de lagrede responsbytene, ikke på gjenserialisert XML.

100927 har rotens `respons_dato_tid=2026-10-22T11:04:47.6066742+02:00`; HTTP `Date` er `Thu, 22 Oct 2026 09:04:48 GMT`. Sidevognens lokale `retrieved_utc=2026-10-22T09:04:48.0511379+00:00` ble registrert umiddelbart **før** forespørselen; `timestamp_basis` oppgir dette. 100889 har rotens `respons_dato_tid=2026-10-22T11:05:44.6588969+02:00`; HTTP `Date` er `Thu, 22 Oct 2026 09:05:44 GMT`; lokal ferdigregistrering er `2026-10-22T09:05:45.4812557+00:00`, med separat starttid i sidevognen. Disse tidene er observasjonsmetadata, ikke dokumentenes publiseringsdatoer eller bevis for en faglig rettelse.

## Observert dokumentkjede

Det maskinlesbare [kontrolluttrekket](source-observations.json) er beregnet direkte fra de to hashkontrollerte originalene. Det bevarer tekst, nil-attributt og 1-baserte lokatorer for alle publikasjoner og relasjoner. Lokatorenes elementnavn står i det eksakte navnerommet ovenfor; prefiks er utelatt i visningen.

100927 har `id=100927`, `sak_sesjon=2024-2025`, `sak_nummer=16`, sakstype `budsjett`, dokumentgruppe `proposisjon`, `status=behandlet` og `ferdigbehandlet=true`. Den har fem referanser under `/detaljert_sak/publikasjon_referanse_liste`:

| Nr. | Rå dokumentetikett | type / undertype | eksport_id |
| ---: | --- | --- | --- |
| 1 | Prop. 16 S (2024-2025) | regjering / proposisjon | element til stede, `i:nil="true"`, ingen tekst |
| 2 | Stortingsreferat 26.11.2024 | referat / storting | `refs-202425-11-26` |
| 3 | Innst. 81 S (2024-2025) | innstilling / storting | `inns-202425-081s` |
| 4 | Stortingsreferat 16.12.2024 | referat / storting | `refs-202425-12-16` |
| 5 | Stortingsreferat 16.12.2024 | referat / storting | `refs-202425-12-16` |

Referanse 1 har den rå URL-en `http://www.regjeringen.no/id/PRP202420250016000DDDEPIS`. Referansene til Stortinget er protokollrelative `//www.stortinget.no/...`. Referanse 4 ender `/25`, mens 5 ender `/voteringer#161224-25`: samme eksport-ID peker til to ulike steder i samme referat. Begge referanser må kunne bevares; eksport-ID alene er ingen unik referanseidentitet. Ingen referanse av typen `vedtak` forekommer i akkurat dette svaret. Det beviser ikke at saken mangler endelige vedtak.

Den eksisterende autentiske [B6-prøven 40034048](../../../tests/fixtures/b6/40034048.xml) angir `sak_id=100927`, vedtaksnummer 210 og dato 16. desember 2024. Saks-ID-en gir dermed en direkte forbindelse fra vedtaksobjektet til disse saksmetadataene uten å tolke dokumentnummeret fra fritekst. B8 har ikke hentet dette vedtaket på nytt eller endret B6-originalen.

100927 har én relasjon: `relasjon_type=sammekilde`, `relatert_sak_id=100889`. Den relaterte originalen 100889 viser motsatt relasjon tilbake til 100927. Begge bruker samme Prop. 16 S og regjerings-URL, men 100927s `henvisning` gjelder `kap. 1429` og Innst. 81 S. 100889s `henvisning` sier `unntatt kap. 1429` og Innst. 95 S. Den andre saken har også fem referanser, men bruker `inns-202425-095s` og referatet `refs-202425-12-18` med egne debatt-/voteringslokatorer. En felles proposisjon innebærer altså ikke felles innstilling eller ett felles vedtak. Relasjonens rå retning og type må beholdes.

## Uavhengig sidekontroll

[Sakssiden 100927](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=100927) viser kapittelavgrensningen, Prop. 16 S, Innst. 81 S, innstillingsdato 9. desember 2024, debatt/votering 16. desember og lenke til den andre saken som sak fra samme kildedokument. [Innstillingens offisielle inngang](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-081s/) oppgir Prop. 16 S, kap. 1429, som kildedokument og familie- og kulturkomiteen som utgiver. [Vedtaksoversikten](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?p=100927) og [den relaterte sakssiden](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=100889) ble åpnet som kontroll av lenkekjeden.

Regjeringslenken fra sakssiden ble forsøkt åpnet i nettverktøyet, men ga `Cache miss`; proposisjonens faktiske innhold og eventuelle omdirigering er derfor **ikke kontrollert** i B8. Regjeringslenken bevares som oppgitt metadata. Den gjøres ikke til et vellykket dokumentinnholdsfunn. Nettsidene er kontrollert via nettverktøyet 22. oktober; bare de to API-svarene er bevart med bytehash.

## Publiseringsgrense og videre bruk

De to originalene utgjør samlet 28 271 byte fra to offentlige parlamentariske saker. De inneholder i tillegg til saksdokumentfeltene offentlige saksordføreropplysninger: navn, representant-ID, fødselsdato, kjønn, fylke og partitilhørighet for to politikere. Ingen private kontaktopplysninger, innloggingsinformasjon, tokens, cookies eller ikke-offentlige dokumenter ble funnet i responsene eller sidevognene. Partitilhørighet er personinformasjon og er her uttrykkelig knyttet til offentlig parlamentarisk rolle. Prøven er avgrenset til disse to allerede identifiserte sakene, uten representantkartlegging eller masseinnhenting. Det avledede kontrolluttrekket inkluderer bare saks-, publikasjons- og relasjonsmetadata. Råoriginalen er bevart komplett for etterprøvbarhet og skal ikke beskrives som anonymisert.

[Stortingets bruksvilkår](https://data.stortinget.no/om-datatjenesten/bruksvilkar/) viser til NLOD, krever kildeangivelse og korrekt fremstilling. Kildefeltene her stammer fra Stortinget; mulige parservalg nedenfor er prosjektets anbefalinger. Bruksvilkårene oppgir også 100 API-kall per minutt. Det er bare utført to vellykkede API-hentinger i denne undersøkelsen.

Anbefalt tolkningsgrense: behold rå `lenke_tekst`, `lenke_url`, `type`, `undertype`, `eksport_id` og relasjoner uendret med kildehash/lokator; legg eventuell normalisert HTTPS-lenke og dokumentklassifikasjon i separate felt. Nil eksport-ID er forventet for denne regjering/proposisjon-referansen og betyr ikke manglende dokument. Ikke utled beløp, budsjettår eller endelig vedtaksstatus fra dokumentetiketten eller sakstype. Ukjente typer/undertyper og uavklarte lenker må synes som metadata til kontroll fremfor å bli kastet.

Responstider forekommer også inne i emner, publikasjonsreferanser, relasjoner og saksgang. En ny B8-fingeravtrykksregel må derfor skille disse tidsfeltene fra dokumentmetadata hvis bare en ny henting skal gi uendret innhold. Dette er en designanbefaling ut fra observerte felt, ikke en målt gjenhentings-/rettelsesprøve. B2s eksisterende `xml-object-v1`, tidligere resultater og parseridentiteter skal beholde sin betydning. Generell sesjonsdekning, ukjente faktiske XML-varianter og korrekthet over tid er ikke demonstrert av to originaler. Feil-/nil-/grensemutasjoner må merkes som syntetiske tester.

## Utført kilde–SQLite–CLI–Excel–JSON-prøve

Den nye offentlige grensen er prøvd offline på de hashkontrollerte originalene gjennom `tests/test_b8.py`. B2s `sync_saved` og uttrykkelig `storting-belop-v2` bruker den uendrede B6-originalen 40034048. Den faktiske innlesnings-CLI-en `python -m innlesning saksdokumenter` leser 100927 og returnerer en immutable berikelses-ID. Databasen gjenåpnes; `python -m analyse --saksutvalg ... --excel ... --json ...` skriver faktiske filer. Arbeidsbok og `b6-frozen-2` leses tilbake med samme ID-er/verdier. Det er seks før-/delta-/etterobservasjoner, to posthendelser og to historikkrader, uten nye beløpsrader fra de fem dokumenthenvisningene.

Kontrollverdiene er 1429/1 +5 796 000 fra 160 243 000 til 166 039 000 og 1429/22 −3 000 000 fra 32 185 000 til 29 185 000. Vedtaket vises som 210 (2024–2025), mens API-ID-en heter 40034048. Innst. 81 S og Prop. 16 S har klikkbare metadatahenvisninger. `Stikkord` står rett etter `Post`; 1429/22 viser «kan overføres» med rå formåls-/HTML-felt og lokator `table[1]/tr[5]/td[3]`.

Et supplerende byteidentisk utdrag for 40034049/211 er laget fra en allerede lokalt bevart offentlig sesjonsrespons, uten ny HTTP: forelder 7 479 943 byte, SHA-256 `c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42`, hentet 22. oktober 2026 kl. 07.04.03 UTC. Objekt ved byte 1 255 498 (0-basert), 1 318 byte, beholdes mellom originalprefix og suffix. Utdraget er 1 692 byte, SHA-256 `5f253a556d2ac512570899252b396bc38f068de5f4bd6820178e7de8ce41f3eb`. [Sidevogn og uttak](../../../tests/fixtures/b8/README.md) beskriver proveniensen. 211s stikkordsfullmakt om 1429/60 bevares i faktisk fulltekstark, uten beløpsobservasjon. Det er et vedtaksutdrag, ingen tredje komplett saks-API-original.

Separate syntetiske tester prøver gjentatt henting, volatil responstid, A → B → A med overgang 1 → 2 → 3, eldre kilde-/hentetid, timeout før respons, HTTP-feil, proveniens-/XML-feil med bevart rårespons, nil/fravær, ukjent/motstridende identitet, S/L/LS, flere dokumenter, utrygge URL-er og uavklart/flere stikkord. Korrigert vedtaksrevisjon erstatter ikke valgt gammelt beløp eller berikelse. Ny saksfeil gir historiske referanser med feilgrunn, uten å endre gamle B5-avgjørelser/kontrollerte verdier. Globale dokumentavvik består når alle beløp filtreres bort. En relatert sak kan ikke brukes som vedtakets direkte saksgrunnlag. Manglende, korrupt og motstridende historisk arbeidsbok hindrer ikke den nye offisielle kilden.

Frosset v2 er gjenlest og faktisk reeksportert etter at databasefilen er gjort utilgjengelig. Endret konvolutt/felttype/innhold avvises. Gamle frosset-v1-rapporter gjenleses uendret. Gamle skrivere bevarer schema 5 og tidligere v1/v2-resultater; schema 6 avvises. Ingen av prøvene omtolker gamle råkilder, aktiverer historisk normalisering eller godkjenner sesjon/år.

Excel er også importert med den bundne Artifact Tool-leseren og rendret ved normal målestokk for beløps-/stikkord-/dokumentkolonner, historikk, dokumenter, relasjoner, avvik og stikkordgrunnlag. Kontrollen viste lesbare kjerneetiketter, numre, lenker og stikkord. Lange rå JSON-/HTML-felt er bevart og kan kreve utvidet radhøyde. Ingen native Excel-app eller live lenketilgjengelighet er påstått kontrollert. Produksjonsdrift og #10s driftsaksept inngår ikke.

Kommandoer og format ligger i [B8-veiledningen](../../b8-saksdokumenter.md). Samlet Standards-/Spec-review, separat sikkerhetsaudit, CI og merge utføres av orkestratoren etter denne lokale kandidaten.

Fire funn fra den første kandidatgjennomgangen er rettet og prøvd med separate syntetiske regresjoner gjennom offentlige grenser. PRP-kodens nummer, sesjon og serie kontrolleres mot etiketten, også med nil eksport-ID; motstridende dokumenttype blir motstrid og ukjent lenkekode blir uavklart. De tre seriene S/L/LS i kodeformatet er prøvd syntetisk; bare originalens S-kode er et autentisk kildebevis. Stikkordkontrollen undersøker teksten utenfor kursivmarkørene også når markører finnes, og faktisk Excel viser kjente ord sammen med uavklart status ved et annet umerket/ukjent/ufullstendig uttrykk. Ingen råfelt eller kildepekere forkortes.

En liten deterministisk samtidighetsprøve stopper første lagring etter SQLite-commit av råbyte, uten å holde en databaselås. Et annet offentlig lagringskall med andre byte eller bare endret metadata avvises; den første lagringen publiserer fortsatt et resultat bundet til sine egne råbyte og metadata. En separat avbruddsprøve viser identisk gjenopptak. HTTP-portprøver gir `HTTPError` med lesefeil, timeout, tilgjengelige delbyte, tomt eller komplett feilinnhold. Alle avsluttes som feilforsøk som kan berikes og brukes i et kontrolluttrekk med de seks eksisterende beløpsobservasjonene. Responsen lukkes. Tilgjengelige delbyte bevares med faktisk hash og eksplisitt delstatus; lesefeil uten tilgjengelige byte gir bare kjente transportmetadata og feilgrunn, uten oppfunnet hash/byteantall. Ingen nettinnhenting eller endring av autentiske fixtures inngår i rettingene. Ny uavhengig gjennomgang, CI og merge gjenstår hos orkestratoren.

Lokalt kontrollresultat etter rettingene 22. oktober 2026 med Python 3.12.14: fullsuite `python -m pytest -q --basetemp ../t8fixfull` ga **738 beståtte, to hoppet over** på 253,63 sekunder. De to er eksisterende Windows-vertsrettighetsprøver. Den målrettede `python -m pytest tests/test_b8.py -q --basetemp ../t8fixall` ga **51 beståtte** på 10,10 sekunder. Regresjonene ble lagt til før de tilhørende rettingene og viste feil ved proposisjonskode, umerket stikkord, konkurrerende lagring og lesing av HTTP-feilinnhold. `python -m ruff check .`, `python -m ruff format --check .` og `python -m mypy` bestod; formatkontrollen omfattet 82 filer og mypy 47 kildefiler. Dette er lokale kontroller av `67fad4e` med ikke-committede rettinger, ingen påstand om at ny uavhengig gjennomgang eller CI er utført.
