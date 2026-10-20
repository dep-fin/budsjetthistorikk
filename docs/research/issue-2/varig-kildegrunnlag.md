# Issue 2 – varig rågrunnlag, rettelser og nye kapittel/post-kombinasjoner

Undersøkt 20. oktober 2026. Dette er en kildeundersøkelse og et lokalt kontrollgrunnlag. Utforskeren endret ikke produksjonskode eller GitHub-innhold. Orkestratoren publiserer rapporten og kontrollunderlaget som dokumentasjon til #2. Rapporten bygger videre på `work/issue2/api/sluttrapport.md` og `work/issue2/kontroll/sluttrapport.md`.

## 1. Et originalt og lovlig hentbart rågrunnlag er sikret

Regjeringens dokumentforside for **Meld. St. 3 (2024–2025), Statsrekneskapen 2024**, tilbyr en ordinær nedlastingslenke merket «Dokumentet i PDF format (6,2 MB)». Den lenken ga HTTP 200 ved direkte nedlasting. Dette er originalfilen som regjeringen tilbyr, ikke nettverktøyets tekstuttrekk. Den tidligere 403-responsen på HTML-vedlegget er ikke omgått. Det er brukt en offentlig, uttrykkelig tilbudt alternativ dokumentrepresentasjon, uten innlogging, endring av informasjonskapsler eller andre tiltak mot beskyttelse. [Offisiell dokumentforside](https://www.regjeringen.no/no/dokumenter/meld.-st.-3-20242025/id3097946/), [PDF-lenken som ble hentet](https://www.regjeringen.no/contentassets/1d45fede74ff4ef18ce06bbd6163c723/nn-no/pdfs/stm202420250003000dddpdfs.pdf).

Første ordinære Python-forsøk kl. **11:55:16.043701 UTC** feilet med `URLError(gaierror(11001, 'getaddrinfo failed'))`. Samme ordinære PDF-forespørsel ble så kjørt med offentlig nettverkstilgang. Ingen andre regjeringsadresser måtte prøves for å få råfilen. Brukeren hadde godkjent offentlig kildeinnhenting. PDF-filen inneholder 311 sider. Hentetid er tidspunktet rett før forespørselen; HTTP Date er bevart separat.

| Råfil | URL | Hentet UTC | HTTP / byte | SHA256 |
|---|---|---|---|---|
| `raw/statsrekneskapen2024.pdf` | [Offisiell PDF](https://www.regjeringen.no/contentassets/1d45fede74ff4ef18ce06bbd6163c723/nn-no/pdfs/stm202420250003000dddpdfs.pdf) | 2026-10-20T11:55:23.257301+00:00 | 200 / 6 491 743 | `f46e7c3613176e064b2d87b07c66608f38c4bd88d980795e51ada42bb52ba9fb` |

HTTP `Last-Modified` var `Wed, 23 Apr 2025 11:18:48 GMT`, ETag var `"1dbb4417ba6d25f"`, og innholdstypen var `application/pdf`. `Last-Modified` beskriver serverens filmetadata og skal ikke behandles som vedtaksdato eller en garanti mot senere endring. `fetch-manifest.json` inneholder URL, status, alle svarhoder, byteantall, hentetid og hash. `fetch-attempts.json` bevarer både DNS-feilen og vellykket henting. `discovery.json` beskriver hvordan den offisielle lenken ble funnet; det er ikke et originalt HTML-råsvar.

Lokal bytebevaring med SHA256 gjør dagens grunnlag etterprøvbart selv om nettfilen senere endres. Det er ingen garanti for at utgiveren vil bevare samme URL eller samme byteinnhold permanent.

## 2. Hele bevilgningskolonnen er trukket ut på postnivå

Vedlegg 2, **tabell 2.1**, står på trykte sider **90–167**, PDF-sider **92–169**. **Tabell 2.2** står på trykte sider **168–197**, PDF-sider **170–199**. Overskriftene i begge tabeller angir **1 000 kroner**. Alle beløp i uttrekket bevarer denne enheten. Konvertering til kroner skjer ved multiplikasjon med 1 000, med den presisjonen originaltabellen gir. [Offisiell PDF, vedlegg 2](https://www.regjeringen.no/contentassets/1d45fede74ff4ef18ce06bbd6163c723/nn-no/pdfs/stm202420250003000dddpdfs.pdf).

| Uttrekk | Poster | Kapitler | Kolonner med beløp |
|---|---:|---:|---|
| Tabell 2.1, utgifter | 1 196 | 364 | Overført frå 2023; Løyving; Samla løyving; Rekneskap; Meirutgift (-) og mindreutgift; Overført til 2025 |
| Tabell 2.2, inntekter | 459 | 230 | Løyving; Rekneskap; Meirinntekt og mindreinntekt (-) |
| Samlet | 1 655 | 594 | Unike nøkler etter del, kapittel og post |

**`Løyving` er årets bevilgningskolonne som skal brukes ved avstemming av bevilgningsvedtak. `Samla løyving` inkluderer overføring fra 2023 og er en separat kontroll. `Rekneskap` er regnskapsutfallet.** Inntektstabellen har ikke egne kolonner for overført beløp eller samlet bevilgning; disse feltene er derfor tomme i CSV-en, ikke satt til null.

Maskinlesbart grunnlag:

- [Alle 1 655 postrader](statsrekneskap2024-posts.csv): UTF-8 med BOM, én rad per kapittel/post, nullutfylte tekstnøkler, tydelig navngitte `*_1000kr`-felt og PDF-sidereferanse.
- `statsrekneskap2024-posts.json`: samme poster, med kildebeløp, tekst og alle tilhørende PDF-linjer. Underposter i netto post 24 er bevart her.
- `pdf-table-lines.json`: alle undersøkte tabellinjer med side, vertikal posisjon, kolonneceller og geometrisk identifisert postnummer.
- `pdf-sums.json`: utskilte summer. Summer er ikke duplisert som bevilgningsposter.
- [Tabellkontroller](statsrekneskap2024-kontroller.json) og lokale kapittelkontroller: dokumenterte kontrollresultater.

`extract_tables.py` bruker pdfplumber og de høyrejusterte beløpskolonnene. Store beløp kan begynne til venstre for vanlige kolonnegrenser; uttrekket bruker derfor kolonnenes høyrekanter og ikke en enkel fast grense for hvert talls venstrekant. Flersidige poster settes sammen, mens innrykkede komponenter i post 24 beholdes som underposter. Nettoresultatet er beløpet på kapittel/post. Eksempelvis er 2445/24 **−334 642**, 2460/24 **102 500**, 2470/24 **−15 000** og 5440/24 **233 300 000**, alle i 1 000 kroner. Underpostene skal ikke legges til en gang til i totalen.

## 3. Kontrollresultater og begrensninger i tabelluttrekket

Kontrollene i `final_table_checks.py` ga følgende:

1. **Alle 1 655 geometrisk identifiserte hovedposter ble satt sammen én gang**, med 1 655 unike del/kapittel/post-nøkler. Ingen uavsluttede poster ble stående igjen.
2. **Summen av Løyving stemmer eksakt med trykt kapittelsum for samtlige 594 kapitler.** Dette er en kontroll mot PDF-ens egne summer, ikke en uavhengig kontroll av det rettslige vedtaksgrunnlaget.
3. **Summen av Løyving er 2 951 906 811 i 1 000 kroner i hver av de to tabellene**, og stemmer eksakt med begge trykte totalsummer. Tabellene inneholder blant annet lånetransaksjoner og fondsoverføringer; totalsummen er derfor ikke et mål på ordinære utgifter uten disse postene.
4. For alle **1 196 utgiftsposter** stemmer `Overført frå 2023 + Løyving = Samla løyving` eksakt. Også kolonnenes samlede summer for overført fra 2023, samlet bevilgning og overført til 2025 stemmer med trykte totalsummer.
5. Det ble først flagget **47 numeriske linjer uten eget postnummer**. Gjennomgang av foregående linjer viser at alle er fortsettelser av summer med ombrutte etiketter. `numeric-warning-classification.json` bevarer klassifiseringen. Ingen slike numeriske linjer står uavklart.
6. Regnskaps- og avvikskolonnene gir små differanser ved summering av publiserte posttall: utgiftsregnskap **−17**, utgiftsavvik **+18** og inntektsregnskap **+2**, i 1 000 kroner, mot trykte totaler. To inntektsrader har også en differanse på 1 ved kontroll av regnskapsbeløp minus bevilgning mot publisert avvik. Dette er forenlig med avrunding av posttall, men årsaken er ikke fastslått for hver rad. Uttrekket endrer ingen tall for å tvinge slike summer til å stemme.
7. Et særskilt avvik gjelder kap. **0702**, kolonnen overført fra 2023: både tekstuttrekket og den kontrollerte sidegjengivelsen viser **`103 0101`** i kapittelsummen. Postene summerer til **103 011**, som også gir samsvar med samlet bevilgning minus årets bevilgning. Dette er bevart som et kilde-/typografiavvik; kapittelsummen er ikke stilletiende rettet. `page123.png` viser den aktuelle trykte side 121. Løyving-kolonnen på samme kapittel stemmer eksakt.

De fire tidligere prøvene er kontrollert mot den lagrede originalfilen:

| Kapittel/post | Løyving | Overført frå 2023 | Samla løyving | Rekneskap |
|---|---:|---:|---:|---:|
| 0020/01 | 109 677 | 3 406 | 113 083 | 108 793 |
| 0021/01 | 201 399 | 6 980 | 208 379 | 201 777 |
| 0024/01 | 125 665 | 3 693 | 129 358 | 122 251 |
| 0041/21 | 1 413 | 619 | 2 032 | 1 037 |

Alle tall i denne tabellen er 1 000 kroner. Verdiene stemmer med de fire prøvene i den tidligere kontrollrapporten etter korrekt enhetskonvertering.

En nøkkelkontroll mot den tidligere lagrede DFØ-filen gir **1 638 unike 2024-nøkler** der, mot **1 655 i PDF-en**. Det finnes 30 PDF-nøkler uten DFØ-nøkkel og 13 DFØ-nøkler uten PDF-nøkkel. Listene ligger i `table-checks.json`. Dette er ikke automatisk manglende stortingsvedtak: kildene kan ha forskjellig omfang, blant annet nullbevilgninger, regnskapsførte poster, fullmakter og radtyper. Forskjellene må avklares ved full avstemming. Det er ikke foretatt en ny full økonomisk avstemming av alle DFØ-beløp mot alle vedtak i denne delundersøkelsen.

Alle relevante PDF-sider er maskinlest. Tre sider er dessuten gjengitt som PNG; side 123 er visuelt inspisert i denne kjøringen. Det er ikke utført manuell linje-for-linje-kontroll av alle 108 tabellsider. De eksakte kontrollsummene underbygger særlig bevilgningskolonnens uttrekk, men beviser ikke at alle mellomliggende vedtak er funnet.

## 4. Regler for kilderettelser, etterslep og sesjonsskifte

Stortingets beskrivelse sier at bare siste versjon av data og dokumentasjon vises. De to virkelige 2024–2025-svarene i den tidligere undersøkelsen hadde ulike responstidspunkter, men identiske vedtaksobjekter. Det er dermed observert en volatil responstid, **ikke en faktisk innholdsrettelse**. Det undersøkte endepunktet er sesjonsbasert. Det er ikke dokumentert en rettelseslogg, et oppdatert-siden-filter, en garanti om uforanderlige gamle vedtak eller en bindende frist for når et vedtak blir synlig. [Om datatjenesten](https://data.stortinget.no/om-datatjenesten/), [vedtaksdokumentasjonen](https://data.stortinget.no/dokumentasjon-og-hjelp/vedtak/).

Følgende er anbefalte, etterprøvbare regler for senere implementering:

- **Bevar råversjoner.** Arkiver hver vellykket full sesjonshenting med URL, hentetid, hash og parserversjon. Bevar også responsens eget tidspunkt. HTTP-feil og ufullstendig parsing må ikke erstatte en tidligere god versjon.
- **Skill transportendring fra kildeinnhold.** En endret `respons_dato_tid` alene skal ikke bli en bevilgningshendelse. Sammenlign hver vedtaks-ID med en hash over objektets innhold, inklusive tekst og relevante metadata. Unngå omfattende tekstnormalisering som kan skjule fortegn eller kolonneendringer.
- **Rettelse av samme ID er en ny kildeversjon.** Ved endret innhold bevares gammel og ny versjon, differansen registreres, og de berørte postenes kjede bygges på nytt. Den reviderte versjonen skal ikke legges til som et ekstra politisk vedtak. Et nytt selvstendig vedtak med egen ID behandles derimot som egen hendelse etter innholdet.
- **Vedtakstid er ikke oppdateringsmarkør.** Nye ID-er med gammel vedtaksdato skal tas inn når de først blir synlige. Full sesjonssammenligning må derfor kunne finne etterslep bak en tidligere største dato.
- **Fravær er et avvik, ikke umiddelbar sletting.** En tidligere kjent ID som mangler i ett senere svar, beholdes i historikken og får et avvik for avklaring. Kilden beskriver ingen tombstone-kontrakt som gjør en enkelt manglende observasjon til sikker sletting. Ved senere bekreftet tilbaketrekking må berørte kjeder behandles uttrykkelig.
- **Sesjonsskifte avslutter ikke et budsjettår.** For budsjettår Y undersøkes minst sesjon Y−1–Y, som inneholder saldert budsjett, og Y–Y+1, som inneholder høstens endringer. Budsjettåret bestemmes fra vedtaksinnholdet og kildekoblingen, ikke bare fra dato eller saksopprettelsens sesjon. Relevante avsluttede sesjoner må kunne leses om igjen.
- **Ingen endelig ferskhetsgaranti kan utledes.** En senere løsning kan hente aktiv og foregående sesjon jevnlig og kontrollere arkiverte år på nytt ved avstemming. Det er et driftsvalg, ikke en kildegaranti. Ingen endelig tidsgrense for gamle rettelser er dokumentert i det undersøkte materialet. Bevar derfor tidspunkt for siste fullkontroll og en uttrykkelig status som «kontrollert per …».

DFØs tidligere dokumenterte månedlige oppdateringsrytme er dessuten en annen tidsdimensjon enn Stortingets vedtaksdato. DFØs `Tildelings_periode` må ikke gjøres om til eksakt vedtaksdato eller brukes som garanti for at alle nylige vedtak allerede er lastet inn. [DFØs nedlastingsside](https://statsregnskapet.dfo.no/last-ned).

## 5. Konkrete og kjørte testgrunnlag

`snapshot_fixture_checks.py` kjørte **sju lokale kontrolltilfeller; alle ga forventet resultat**. Dette er prøver av det foreslåtte deteksjonsgrunnlaget, ikke tester av produksjonssystemet. [Kontrolltilfellene](kildeversjon-kontroller.json) skiller uttrykkelig mellom virkelige kildeobservasjoner og syntetiske variasjoner.

| Tilfelle | Grunnlag | Kontrollert forventning |
|---|---|---|
| Bare responstid endres | To faktisk lagrede 2024–2025-svar | Alle vedtaksobjekter er identiske; ingen ny budsjettendring |
| Samme ID får rettet beløp | **Syntetisk** variant av 40033805 med samme ID/dato og endring fra 400 000 til 401 000 kroner, med tilsvarende endret etterbeløp | Innholdshash endres selv om ID og dato står fast; grunnlag for versjonsbytte og ny kjedeberegning |
| Et gammelt vedtak dukker opp sent | **Syntetisk** fjerning av 40033805 fra første svar, så gjeninnsetting fra virkelig svar | Ny ID med dato 5. november 2024 finnes selv om største tidligere dato er 20. juni 2025 |
| En ID mangler én gang | Samme **syntetiske** utelatelse, betraktet motsatt vei | Konkret fraværssett finnes; dette er ikke dokumentasjon på en reell sletting |
| Budsjettår over to sesjoner | Virkelige vedtak 40032763, 40033719 og 40034287 | Originalt 2024-budsjett og RNB ligger i 2023–2024; nysaldering ligger i 2024–2025; unionen dekker alle tre |
| Sakssesjon og vedtakssesjon er ulike | Virkelig sak 100001 og vedtak 40033805 | Sakssesjon 2023–2024 bevares separat fra vedtakets sesjon 2024–2025 |
| Ny post mangler i opprinnelig katalog | Virkelige opprinnelige 2025-tabeller og vedtak 40034443 | 0900/32 finnes ikke i opprinnelig tabellkatalog, men må tas vare på når ny bevilgning vedtas |

[Den syntetiske rettelsesprøven](syntetisk-rettelse.json) bevarer før-/etterobjekt og er merket syntetisk. Kontrollene dokumenterer at nødvendig input til disse reglene finnes og kan skilles. De dokumenterer ikke at Stortinget faktisk har gjort den kunstige rettelsen, eller at et fremtidig produksjonssystem allerede utfører nyberegning, avviksbehandling og historikk korrekt.

## 6. Etterprøvbart eksempel på en ny katalogpost

Opprinnelig bevilgningsvedtak **40034137**, nummer **284**, **18. desember 2024**, sak **100197**, inneholder kap. 900 med postene **01, 21, 22, 23, 25, 26, 27, 51, 70, 71, 72, 73, 74, 75, 76, 77 og 81**. Post 32 finnes ikke der. Uttrekket av 24 opprinnelige bevilgningstabeller for 2025 gir 1 601 kapittel/post-nøkler, heller ikke med 0900/32. Dette er en katalog av de identifiserte opprinnelige API-tabellene, ikke en ny fullstendighetsgaranti for hele 2025-budsjettet. [Vedtak 284](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034137&p=100197), [lagret sesjonskilde](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025).

Vedtak **40034443**, nummer **526**, **25. mars 2025**, sak **102001**, type `ANNET`, oppretter **(Ny) kap. 900 post 32, Nytt sjøfibersamband til Svalbard og Jan Mayen**, med **454 000 000 kroner**. Samme vedtak reduserer 1760/45 med 227 000 000 kroner. Tabellen har ingen før-/etterbeløp for disse to endringene. Det eksisterende kapittelet får altså en ny postkombinasjon; det er ikke et nytt kapittel. [Vedtak 526](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034443&p=102001).

**Foreslått avviksregel:** nøkkelen er `(utgift/inntekt, budsjettår, kapittel med fire siffer, post med to siffer)`. Når et beløpsvedtak har en nøkkel som ikke finnes i den opprinnelige katalogen, bevares raden med originaltekst, beløp og kilde-ID, og et uttrykkelig avvik «ny nøkkel utenfor opprinnelig katalog» opprettes. `(Ny)` og «bevilges med» er støtte for en ny post; de erstatter ikke en full tolking av tabellen. Katalogen kan utvides med første observerte kilde og virkningsår. Manglende førbeløp må stå som manglende inntil nullstart er underbygd av opprinnelig katalog og vedtakets innhold. Raden skal ikke droppes, kobles til en annen post eller miste beløpet fordi katalogoppslaget feiler.

[Prøven for ny katalogpost](ny-katalogpost.json) bevarer hele vedtaksobjektet, de opprinnelige 900-radene og forventet behandling. `original2025-api-tables.json` bevarer de 24 identifiserte opprinnelige tabellene. API-råfilen fra den tidligere undersøkelsen er originalkilden; disse to filene er avledede kontrolluttrekk.

## 7. Råfilmanifest, reproduksjon og det som fortsatt gjenstår

Den eneste nye nedlastede originalfilen i denne delundersøkelsen er PDF-en i manifestet i punkt 1. Tidligere lagrede originale Stortinget- og DFØ-filer er gjenbrukt med sine opprinnelige hentetider. `inherited-input-hashes.json` oppgir lokale stier, byteantall og SHA256 for disse inputfilene. Deres opprinnelige URL-er og hentetider ligger i `work/issue2/api/manifest.json` og `work/issue2/kontroll/raw/manifest-downloads*.json`. De er ikke fremstilt som hentet på nytt nå. `derived-file-manifest.json` gir SHA256 for de nye avledede datafilene og kontrollresultatene.

Inspeksjons- og kontrollskriptene ble kjørt lokalt og er ikke produksjonskode i repoet. For uavhengig gjentakelse: hent den offisielle PDF-en, verifiser SHA-256, les de angitte sidene i tabell 2.1/2.2, og sammenlign postkolonnen Løyving mot kapittel- og totalsummer. Det versjonerte CSV-uttrekket og kontrollresultatene bevarer fasiten og kildepresisjonen. Den originale PDF-en er beholdt lokalt; dens offentlige kilde-URL og hash er bevart i [hentemanifestet](statsrekneskap2024-henting.json).

Det tidligere manglende varige rågrunnlaget for **alle 2024-posters Løyving** er nå sikret, og hele tabell 2.1/2.2 finnes som maskinlesbare rader med eksakt avstemming av bevilgningskolonnen mot alle kapittel- og totalsummer. Neste økonomiske kontroll er å avstemme dette mot samtlige relevante vedtak og DFØ-radtyper, forklare nøkkelforskjellene, og kontrollere at hele endringskjeden er dekket. Faktiske fremtidige kilderettelser er ikke en forutsetning for å spesifisere og prøve rettelsesreglene: tydelig merkede syntetiske varianter dekker det uobserverte tilfellet. Kildenes manglende historikk- og ferskhetsgarantier må fortsatt være uttrykkelige.
