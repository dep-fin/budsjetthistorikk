# Vedtak 599 (2025–2026): bevilgningsendring uten komitéinnstilling eller regjeringsproposisjon

Kontrollert 20. oktober 2026 som avgrenset kildeundersøkelse i #2, før bygging. Ingen produksjonskode eller GitHub-innhold er endret. AGENTS.md og dokumentene den viser til er lest fra `main`, herunder kildefunn, arbeidsflyt, krav, ansvarsdeling og begrepsliste. Matt Pococks research-skill er lest; dette er undersøkelsesoppdraget delegert fra hovedagenten.

## Publisert kontrollgrunnlag

[Fasit](fixture-normalized.json) · [Sammenligning av kilderepresentasjoner](source-comparison.json) · [Kontrollutfall](source-checks.json) · [Hentemanifest](fetch-manifest.json) · [Rått API-vedtak 599](vedtak599.json). Alle ti kontrollerte API-objekter fra sakens vedtak 591–600 er versjonert her. Originale store HTTP-svar og undersøkelsesskripter er bare mellomlagret lokalt; fil- og kommandolisten beskriver undersøkelsesøkten.

## Resultat

**Vedtak 599 er en autentisk positiv prøve på endelige kapittel-/postendringer uten komitéinnstilling eller regjeringsproposisjon i den undersøkte behandlingskjeden.** Det ble fattet 26. mars 2026, har vedtaks-ID **40036289**, sak **107811**, og gjelder budsjettåret **2026**. Vedtaket kombinerer midlertidige avgiftssatser med tre uttrykkelige reduksjoner av inntektsbevilgninger på kapittel **5538**, post **70–72**. API-typen er **ANNET**, ikke BUDSJETT. [Endelig vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40036289&p=107811), [sesjons-API](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2025-2026).

Dette er dermed mer presist og nyere enn den tidligere positive prøven fra 2003: her er også fravær av komitébehandling underbygd positivt gjennom et vedtak om direktebehandling, ikke bare gjennom tomme relasjonsfelt. Prøven utvider ikke den avtalte startsesjonen 2026–2027 for produksjonsinnlesning.

## Behandlingskjeden og betydningen av «uten innstilling/proposisjon»

1. **25. mars:** Nikolai Astrup og Trond Helleland fremmet **Dokument 8:222 S (2025–2026)**. Forslag 1 gjaldt nullsatser; forslag 2 ba regjeringen fremme bevilgningsendringer i RNB. Det opprinnelige dokumentet inneholdt derfor ikke de tre vedtatte kapittel-/postbeløpene. Dokumentet er et representantforslag, ikke en proposisjon. [Originaldokument](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Representantforslag/2025-2026/dok8-202526-222s/).
2. **Samme dag, referatsak 329:** Presidenten foreslo oversendelse til finanskomiteen. Astrup foreslo i stedet behandling etter forretningsordenen **§ 39 annet ledd bokstav c**. Ved alternativ votering vant Astrups forslag **52–49**, kl. **13.33.39**. Dermed ble det faktiske behandlingsløpet fastsatt uten komitéforberedelse. [Referat 25. mars](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2025-2026/refs-202526-03-25/referatsaker/).
3. **26. mars, sak 8:** Saken ble debattert og votert over i plenum. Presidenten opplyste at **forslag 23**, fra Ine Eriksen Søreide på vegne av Høyre, erstattet forslagene 1 og 2 i representantforslaget. Innledningen i forslag 23 ble dessuten justert under debatten for ikrafttredelsesperioden. Det er det erstattende, endrede forslaget som ble vedtatt. [Voteringsreferat](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2025-2026/refs-202526-03-26/voteringer).
4. **Vedtak:** Votering **27169** gjaldt forslag 23 og ga **52 for, 49 mot**, vedtatt. API-tiden er `2026-03-26T19:04:17.233`; tidssone er ikke angitt i feltet. `voteringsvedtak` kobler denne voteringen til **vedtak 599**, referanse «nr. 23 på vegne av H». Selve `vedtak_tekst` er `nil`: tekstgrunnlaget kommer fra sesjons-API og vedtakssiden. [Voterings-API](https://data.stortinget.no/eksport/voteringer?sakid=107811), [voteringsvedtak](https://data.stortinget.no/eksport/voteringsvedtak?voteringid=27169), [voteringsforslag](https://data.stortinget.no/eksport/voteringsforslag?voteringid=27169).

§ 39 annet ledd bokstav c innebærer gjennomsyn i minst én dag, deretter oppføring på dagsordenen. Stortingets egen kommentar beskriver dette som et alternativ når det ikke er tid til komitébehandling. Det skal ikke forveksles med straksavgjørelse etter bokstav d. Presidentens muntlige forslag om behandlingsmåte finnes; «uten innstilling» betyr her **uten komitéinnstilling til realitetsbehandlingen**, ikke at presidenten aldri ga noen tilråding. [Forretningsordenen](https://www.stortinget.no/no/Stortinget-og-demokratiet/Lover-og-instrukser/forretningsorden/).

Saks-API støtter kjeden: `dokumentgruppe=representantforslag`, henvisning til Dokument 8:222 S, `innstillingstekst=nil`, `komite=nil`, tom `sak_relasjon_liste` og tom hendelsesliste i trinnet `KOMBEH`. Publikasjonsreferansene er representantforslaget og referatene 25. og 26. mars; ingen Prop.- eller Innst.-referanse. Saksnettsiden har tilsvarende tomt trinn for komitébehandling og beskriver prosedyren uttrykkelig. [Saks-API](https://data.stortinget.no/eksport/sak?sakid=107811), [saksside](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=107811).

Fraværskonklusjonen gjelder denne dokumenterte kilde- og vedtakskjeden. Det opprinnelige avgiftsvedtaket for 2026 som endres, har en tidligere budsjettforhistorie. Prøven påstår ikke at avgiften aldri tidligere har hatt proposisjonsgrunnlag, og tomme API-lister alene er ikke tilstrekkelig bevis.

## Normalisert beløpsfasit

Alle beløp er **kroner**, ikke tusen kroner. Kapittel 5538 er et inntektskapittel; negativ endring skal ikke endre klassifikasjonen til utgift. Før-/til-beløpene gjelder disse linjene i vedtaket, ikke en uavhengig kontrollert helårskjede.

| Budsjettår | Kap. | Post | Før, kr | Endring, kr | Etter, kr |
| --- | --- | --- | ---: | ---: | ---: |
| 2026 | 5538 | 70 | 2 770 000 000 | −1 154 167 000 | 1 615 833 000* |
| 2026 | 5538 | 71 | 5 220 000 000 | −2 175 000 000 | 3 045 000 000 |
| 2026 | 5538 | 72 | 3 000 000 | −1 250 000 | 1 750 000 |
| Sum | | | 7 993 000 000 | **−3 330 417 000** | 4 662 583 000 |

\* Til-beløpet på post 70 er kildeavstemt som beskrevet nedenfor. Endring, førbeløp og øvrige rader stemmer på tvers av representasjonene. [Vedtaks-API](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2025-2026), [referatets XML](https://data.stortinget.no/eksport/publikasjon?publikasjonid=refs-202526-03-26).

### Faktisk kildeavvik på post 70

| Representasjon | Rå til-verdi post 70 | Observasjon |
| --- | --- | --- |
| Endelig vedtak på nettsiden | `I 615 833` | Stor bokstav I og manglende siste tusengruppe |
| `stortingsvedtak_tekst` i sesjons-API | `I 615 833` | Samme avvik som nettsiden |
| `forslag_tekst` for vedtatt forslag 23 | `I 615 833` | Også API-versjonen av forslaget har avviket |
| Voteringsreferat på nettsiden | `1 615 833 000` | Fullstendig tall |
| Voteringsreferatets publikasjons-XML | `1 615 833 000` | Samme tall, med harde mellomrom i originalen |

Nettsiden og vedtaks-API er altså ikke to uavhengige tallbekreftelser. Referatet viser det fullstendige tallet i det vedtatte forslag 23. Dette støttes av regnestykket **2 770 000 000 − 1 154 167 000 = 1 615 833 000**. Fasiten bevarer alle råverdier og oppgir referatet som avklaringsgrunnlag. Dette er en dokumentert avstemming av motstridende representasjoner, ikke en observert rettelse over tid fra Stortinget. Ingen kilde er endret lokalt. [Vedtakssiden](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40036289&p=107811), [forslags-API](https://data.stortinget.no/eksport/voteringsforslag?voteringid=27169), [voteringsreferat](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2025-2026/refs-202526-03-26/voteringer), [referat-XML](https://data.stortinget.no/eksport/publikasjon?publikasjonid=refs-202526-03-26).

En fremtidig innlesning skal finne alle tre beløpslinjene, men markere det ufullstendige til-beløpet som avvik. Verken å oversette I til 1, gange tallet med 1 000 eller erstatte det med regnestykket uten sporbar avklaring er en forsvarlig generell parserregel. Den avklarte prøven kan bruke referatets tall med kildelenke, kildeversjon og begrunnelse. Den må aldri betegne den rå vedtaksverdien som feilfritt uttrukket.

## Positive og negative kontrolltilfeller for #2

`fixture-normalized.json` er en kompakt faglig fasit, ikke en produksjonskontrakt. Den er versjonert sammen med API-objektene og kildeavviket.

| Prøve | Forventet resultat |
| --- | --- |
| Vedtak 599, API-type ANNET, uten Prop./Innst.-kobling | **Tre** endelige inntektsendringer 5538/70–72; behold direktebehandlingskjeden |
| De seks nullsatsene i samme vedtak | Bevar avgiftstekst og virkningsperiode; **ingen ekstra årsbeløpslinjer** |
| Fullmaktsord i originalforslagets bakgrunn | Gir ikke en selvstendig kronebevilgning eller ekstra fullmaktsramme |
| Originalt forslag 2 om senere RNB-bevilgninger | Forslag, erstattet av forslag 23; skal ikke registreres som en ekstra vedtatt endring |
| Vedtak 591–597, ID 40036281–40036287 | Vedtatte satser, **ingen** kapittel-/postendringer |
| Vedtak 600, ID 40036290, også ANNET | Anmodning om tiltak i RNB; **ingen** kapittel-/postendring |
| Vedtak 598, ID 40036288 | Separat positiv hendelse: 5543/70, −3 000 000 000; skal ikke legges inn under vedtak 599 |
| Rå post 70 til-verdi | Synlig kildeavvik; ingen stille korreksjon eller tap av vedtaket |

Saken har ti registrerte vedtak, 591–600, alle klassifisert ANNET. Ut fra dette prøvde saksutsnittet gir 598 og 599 til sammen fire kapittel-/postendringer og −6 330 417 000 kroner. Dette forklarer sakssidens omtrentlige inntektsreduksjon på 6,3 mrd., men denne avrundede omtalen er ikke en ekstra bevilgning eller uavhengig årsavstemming. [Sesjons-API](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2025-2026), [saksside](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=107811).

Konsekvensene for innlesningen er derfor konkrete: bruk alle vedtakstyper som kandidatgrunnlag; krev ikke Prop.- eller Innst.-relasjoner; identifiser beløpslinjene gjennom innhold og proveniens; bevar sats, anmodning og bevilgning som ulike elementer; sammenhold de vedtatte forslagene med endelig vedtak; og hold kildeavvik synlige. Denne prøven beviser ingen fullstendig dekning av en sesjon eller et budsjettår.

## Bevart grunnlag og reproduksjon

Alle **14** offentlige kildesvar ble hentet normalt og ga **HTTP 200**. Et første forsøk i ordinær sandkasse manglet DNS/nettverk; det etterfølgende tillatte nettverkskallet hentet de samme offentlige adressene. Ingen 403 eller 429 er omgått. `retrieved_utc` er tidspunktet rett før forespørselen; API-ets `respons_dato_tid` og HTTP `Date` beholdes som separate kildetider. Råsvarene er bevart under `raw/`; URL, endelig URL, UTC, status, byteantall, SHA-256 og headere uten sessionscookies ligger i `fetch-manifest.json` og per-kilde metadatafiler.

- `fixture-normalized.json`: kompakt fasit, proveniens, behandling, positive/negative prøver og kildeavvik.
- `source-comparison.json`: de faktiske tabellradene fra fem representasjoner, uten å rette feilverdien.
- `source-checks.json`: likhetskontroller, referatets korrekte post 70-verdi og tre aritmetiske kontroller.
- `vedtak591.json`–`vedtak600.json`: komplette vedtaksobjekter fra bevart sesjonsrespons, inkludert rå HTML-tekst og rå API-type.
- `fetch.py`, `fetch_more.py`, `inspect_sources.py`, `normalize.py`: lokale undersøkelsesverktøy. Kjør med bundled Python `C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`. Fra eksisterende råfiler er rekkefølgen `inspect_sources.py`, `normalize.py`; ny nedlasting er ikke nødvendig for å reprodusere tabellkontrollene.

Alle 14 råhashene ble etterkontrollert. Tabelluttrekket fra vedtakssiden, vedtaks-API og forslags-API er likt, inklusive feilen; begge referatversjonene har det fullstendige tallet. Alle tre fasitrader oppfyller før + endring = etter. Dette er kildekontroller, ikke test av en produksjonsparser. GitHub/main er bare lest; hovedagenten overfører funn og prøvehenvisninger til fast kildekontekst og relevante tickets i den samlede publiseringen.

## Kildeinventar med UTC og SHA-256

[Hentemanifest](fetch-manifest.json) bevarer de fulle kildeadressene. UTC-tidene under er gjengitt direkte fra manifestets ISO-tidspunkter.

| Råfil | Hentet UTC | HTTP | SHA-256 |
| --- | --- | --- | --- |
| raw/vedtak599.html | 2026-10-20T12:21:09.059087+00:00 | 200 | `7fb9ac19c0a81495af1e7048a1c4cc74c5fc6c4e562c9d108ccec21373e9939d` |
| raw/sak107811.html | 2026-10-20T12:21:10.314750+00:00 | 200 | `4a1dbb11c7eaa3d449d59f8ef60dde2124aa9953b06e2c3dbf1fa40e1e41b5b5` |
| raw/sak107811.xml | 2026-10-20T12:21:13.174394+00:00 | 200 | `9ba31203ff86494da243ad4992cb50147fb33a7f9d5a9cee1dbf18f53fd8842e` |
| raw/vedtak2025-2026.xml | 2026-10-20T12:21:14.180591+00:00 | 200 | `795afc4202c51a13c4360f1374f3a603aa5d8e803c57195ec48effb60c6aebf6` |
| raw/voteringer107811.xml | 2026-10-20T12:21:25.689340+00:00 | 200 | `22aebf352a3d878089e6862f3ea7f6249f7ab47dc90e2329b00a610587f33162` |
| raw/referat0325.html | 2026-10-20T12:21:26.796673+00:00 | 200 | `57b5d775f3baa699ef439d2bf87c58f2699dd3f3c3215d8d5228eb774fe8ed5c` |
| raw/referat0326.html | 2026-10-20T12:21:28.907639+00:00 | 200 | `b54c7b339089b44e7df89b5424580439205190e89dfc3db65240d4d634751eeb` |
| raw/dok8-222.html | 2026-10-20T12:21:32.233375+00:00 | 200 | `0a5cece62fe1cf78381e9e785a3303de8df721d6853dfa7e24090fdeec260050` |
| raw/publikasjon0326.xml | 2026-10-20T12:21:33.020266+00:00 | 200 | `4eed3a96b705a6bc80f9f7776efbde1c3dab07f36b898ed4722617ff59ea5b56` |
| raw/publikasjon0325.xml | 2026-10-20T12:21:35.164640+00:00 | 200 | `fafd115c98928022d1099b5bd2472b07587890fb3bf5aff8fb604ae5e34db060` |
| raw/voteringsvedtak27169.xml | 2026-10-20T12:22:44.628387+00:00 | 200 | `ae9f6860a6bf5555651b5507fa62a122551a59ef655017a6dad85f6aa7dc0add` |
| raw/voteringsforslag27169.xml | 2026-10-20T12:22:47.035306+00:00 | 200 | `6ed6cd3b1956333799eaa1b459e2c162ac09dad4160e04ce026c6ec9f372a75d` |
| raw/forretningsorden.html | 2026-10-20T12:22:49.486156+00:00 | 200 | `13a1470da0b1de1d41040d0c6107bcdd9b0e55e1d6bd45da6f17b66fdc677853` |
| raw/publikasjon-dok8-222.xml | 2026-10-20T12:23:04.452135+00:00 | 200 | `6abb31e36f19c92a96896754e1cd71c1cda9680249542fc69139ed0f002f322a` |
