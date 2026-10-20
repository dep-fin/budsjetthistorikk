# Issue 2 – gjentakelsen av 1860/01 og 4860/01 i desember 2024

Kontrollert 20. oktober 2026. Undersøkelsen gjelder bare de to postene. [Årsrapporten](../aar/README.md) og relevante ferdige kontrollfiler er brukt som inngående grunnlag. Nye kilder er offentlige primærkilder fra Stortinget og Energidepartementet. Ingen utgiver er kontaktet. GitHub og produksjonskode er ikke endret. Research-skillen og FINs språkprofil er brukt; PDF-ene er også kontrollert visuelt der rettelsesmerking og tabellutforming har betydning.

## Publisert kontrollgrunnlag

[Fasit og observasjoner](controls.json) · [Hentemanifest](fetch-manifest.json) · [Tildelingsbrevet som nettobservasjon](tildelingsbrev-nettobservasjon.json) · [Årsavstemming](../aar/README.md). Originale PDF-/HTTP-filer er mellomlagret lokalt. Anbefalt økonomisk opptelling nedenfor er en faglig analyseanbefaling; den gir ingen generell automatisk dedupliseringsregel. I første leveranse skal formelt uavklarte kjeder fortsatt ha synlig avvik og holdes utenfor automatisk godkjente historikksummer til en sporbar kontrollavgjørelse foreligger.

## Konklusjon

**De to endringene skal telles én gang i den økonomiske bevilgningshistorikken. Det er samtidig dokumentert at begge innstillingers publiserte forslag, voteringsgrunnlag og vedtak gjengir endringene.** Konflikten kan derfor ikke forklares som en isolert feil i vedtaks-API-et eller ved at det andre forslaget ble forkastet.

Stortingets publiserte behandling viser at romertall I i Innst. 99 S ble enstemmig vedtatt 17. desember, og at romertall I i Innst. 93 S ble enstemmig vedtatt 18. desember. Begge inneholder samme overgang på 1860/01 og 4860/01. Den andre tilrådingen bryter med sin egen uttrykkelige komitéavgrensning og gjenbruker det tidligere førbeløpet. Det er ikke funnet et nytt økonomisk formål, et nytt før-/etterpar eller en uttrykkelig beslutning om å øke/redusere de samme postene ytterligere. [Votering 17. desember](https://data.stortinget.no/eksport/voteringer?sakid=100898), [votering 18. desember](https://data.stortinget.no/eksport/voteringer?sakid=100894), [Innst. 93 S](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-093s/?all=true).

Energidepartementets supplerende tildelingsbrev 2, datert 19. desember 2024, henviser samlet til begge datoene og begge innstillingene. Brevet gjennomfører +10 988 000 og −2 400 000 kroner én gang. Dette gir en konkret administrativ forklaring på hvordan departementet la vedtakene til grunn, uavhengig av sluttsamsvaret mellom DFØ og statsregnskapet. Brevet er lest gjennom nettsøkets gjengivelse av den offisielle PDF-en; rånedlasting ga 403, jf. begrensningen nedenfor. [Supplerende tildelingsbrev 2](https://www.regjeringen.no/contentassets/7734a4d009ed4df9be8e055862c7a3e2/supplerende-tildelingsbrev-til-havindustritilsynet-for-2024-1640841.pdf).

**Juridisk tolkningsgrense:** Det er ikke dokumentert en særskilt rettelse som fjerner disse to radene fra vedtaket 18. desember. Rapporten fastslår derfor ikke at vedtak 365 rettslig er opphevet, ugyldig eller aldri vedtatt. Den anbefaler en etterprøvbar, avgrenset regel for økonomisk opptelling, med begge formelle observasjoner bevart. En ubetinget påstand om at bare arbeids- og sosialkomiteens tekst ble vedtatt, ville stride mot de leste voteringskildene.

## Hva kildene viser

### 1. Saken ble uttrykkelig delt mellom komiteene

Innst. 99 S gjelder blant annet Prop. 17 S kap. 1860 og 4860. Innst. 93 S gjelder samme proposisjon med disse kapitlene unntatt. I avsnittet om komiteens behandling opplyser energi- og miljøkomiteen at Stortinget 26. november sendte de to kapitlene til arbeids- og sosialkomiteen. Avgrensningen er dermed dokumentert i behandlingsbeskrivelsen, og ikke bare i en kort sakstittel. Den særskilte energisaken under Innst. 99 S har saks-ID 100929; den felles behandlingen er også knyttet til sak 100898. [Innst. 99 S](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-099s/?all=true), [Innst. 93 S](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-093s/?all=true), [sak 100929](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=100929).

Dette dokumenterer hvilken komité som fikk oppgaven. Det dokumenterer ikke alene at avvikende rader i en senere vedtatt tilråding kan slettes rettslig.

### 2. Begge fullstendige innstillinger inneholder de to postene i tilrådingen

Begge innstillingene er lest i full HTML og full PDF, inklusive merknader, mindretallsforslag, tilråding og vedlegg. Innst. 99 S har de to radene på trykte sider 4 og 6. Den eneste mindretallsteksten gjelder rapportering om arbeidsavklaringspenger; den gir ingen alternativ endring på disse postene. [Innst. 99 S, PDF](https://www.stortinget.no/globalassets/pdf/innstillinger/stortinget/2024-2025/inns-202425-099s.pdf).

Innst. 93 S har tilsvarende rader på trykte sider 2–3. Tilrådingen fremmes av en samlet komité. Vedlegget gjelder andre spørsmål og inneholder ingen forklaring som avgrenser eller reverserer de to Havindustritilsynet-radene. Følgende beløpspar er identiske i begge innstillingene:

| Post | Før, kroner | Endring, kroner | Etter, kroner |
|---|---:|---:|---:|
| 1860/01 | 349 324 000 | +10 988 000 | 360 312 000 |
| 4860/01 | 85 800 000 | −2 400 000 | 83 400 000 |

Dette er kildeobservasjoner. Den gjentatte forekomsten er også synlig i PDF-ene og skyldes verken HTML-parsing eller feil lesing av et sideskifte. [Innst. 93 S, PDF](https://www.stortinget.no/globalassets/pdf/innstillinger/stortinget/2024-2025/inns-202425-093s.pdf).

### 3. Voteringsforslagene og avstemningene bekrefter begge forekomstene

Voterings-API-et er kontrollert mot de fullstendige møte-/voteringsreferatene. Det er skilt mellom voteringens tema og forslagstekst, fordi ett voteringsuttrekk kan inneholde flere romertall.

| Dato og dagsordenssak | Voterings-ID | Forslag med de to postene | Tema og resultat |
|---|---|---|---|
| 17. desember, sak 3 | 23880 | 40077095, komiteens tilråding I | I, II og III; enstemmig vedtatt |
| 18. desember, sak 14 | 23976 | 40077047, komiteens tilråding I | I og III; enstemmig vedtatt |

17. desember ble Høyres forslag 1 forkastet i en egen votering, 23879. Det endrer ikke at bevilgningstilrådingen ble vedtatt. 18. desember gjaldt votering 23975 romertall II; motstemmene der gjelder ikke romertall I. Voteringsforslagene 40077095 og 40077047 inneholder begge nøyaktig de to aktuelle før-/etterparene. [Forslag under 23880](https://data.stortinget.no/eksport/voteringsforslag?voteringid=23880), [forslag under 23976](https://data.stortinget.no/eksport/voteringsforslag?voteringid=23976), [voteringer i sak 100898](https://data.stortinget.no/eksport/voteringer?sakid=100898), [voteringer i sak 100894](https://data.stortinget.no/eksport/voteringer?sakid=100894).

Referatet 17. desember sier «Tilrådinga frå komiteen blei samrøystes vedteken». Referatet 18. desember gjengir de to radene under sak 14 og avslutter avstemningen over I og III med «Komiteens innstilling ble enstemmig vedtatt». Det er ikke funnet noe muntlig uttak av de to kapitlene i debatt- eller voteringsdelen av disse møtene. Den bevarte PDF-en for 18. desember viser begge radene på trykt side 1784, PDF-side 158. [Voteringsreferat 17. desember, sak 3](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-17/voteringer#2024-12-17-3), [voteringsreferat 18. desember, sak 14](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-18/voteringer#2024-12-18-14).

**Kildeobservasjon:** Offentlig publisert vedtak 221 / 40034064 og vedtak 365 / 40034226 svarer på dette punktet til forslag og referat. Samme overgang har to vedtaks-ID-er. **Vurdering:** API-et viderefører en gjentakelse som allerede finnes i parlamentariske publikasjoner. En løsning som bare retter parseren, vil ikke løse opptellingen. [Vedtak 221](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034064&p=100898), [vedtak 365](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40034226&p=100894).

### 4. «Beriktiget» løser ikke denne konflikten

Den tilgjengelige PDF-en av Innst. 93 S er tydelig merket «Beriktiget». PDF-metadata oppgir endringstid 19. desember 2024 kl. 14.57.20 +01.00. Dette er filmetadata, ikke et selvstendig bevis på rettelsens rettslige dato eller innhold. Visuell kontroll av forside og sider 2–3 viser at de to radene fortsatt står som vanlig tabelltekst, uten strykning eller merknad om bortfall. Hele dokumentet har ingen rettelsesforklaring som gjelder disse radene. Det er derfor ikke grunnlag for å bruke ordet «Beriktiget» som dokumentasjon på at gjentakelsen er fjernet. [Beriktiget Innst. 93 S](https://www.stortinget.no/globalassets/pdf/innstillinger/stortinget/2024-2025/inns-202425-093s.pdf).

Søk etter kombinasjoner av de to kapitlene, Innst. 93 S, rettelse og beriktiget ga ingen særskilt rettelse som løser postkonflikten. Dette er en avgrenset søkeobservasjon, ikke en garanti om alle historiske utgaver. Ingen versjon før beriktigelsen er hentet, og rapporten tilskriver derfor ikke beriktigelsen en bestemt endring.

### 5. Departementets gjennomføring og sluttkildene har én endring

Tildelingsbrevet 19. desember omtaler begge stortingsdatoene og begge innstillingene sammen. Tabellen har én økning på 10 988 000 kroner og én reduksjon på 2 400 000 kroner. For 1860/01 viser brevet tidligere tildelt 366 487 000 og ny tildeling 377 475 000 kroner. Dette er disponibel tildeling med overføringen fra 2023, og må holdes adskilt fra årets bevilgning. Differansen på 17 163 000 kroner stemmer med overføringen i det ferdige årsgrunnlaget: 349 324 000 + 17 163 000 = 366 487 000, og 360 312 000 + 17 163 000 = 377 475 000. For 4860/01 viser brevet 85 800 000 → 83 400 000. [Tildelingsbrevet](https://www.regjeringen.no/contentassets/7734a4d009ed4df9be8e055862c7a3e2/supplerende-tildelingsbrev-til-havindustritilsynet-for-2024-1640841.pdf).

Det ferdige DFØ-kontrollgrunnlaget har de to endringene bare under i99/24–25: råfilrad 52379 og 38609. Gruppene i93/24–25 mangler DFØ-motpart for disse postene. Årets sluttbevilgninger stemmer med statsregnskapet, jf. årsrapporten og de arvede post-/kildekontrollene. Dette er støtte for økonomisk behandling, og erstatter ikke voteringsdokumentasjonen.

## Presis anbefalt kontrakt før bygging

1. **Bevar fire kildeobservasjoner.** Nøkkelen er minst budsjettår, sesjon, vedtaks-ID, kapittel, post og radlokator. Originalt delta, førbeløp, etterbeløp, dato, sak og dokumentreferanse bevares. To observasjoner har samme post, men ulike vedtaks-ID-er; ingen råobservasjon slettes.
2. **Skill formell vedtakshistorikk fra økonomisk effekt.** Vis begge vedtak og begge voteringene som dokumenterte publikasjoner. For økonomisk årsbevilgning brukes én overgang per post, først dokumentert 17. desember gjennom 40034064. Knytt 40034226 til samme økonomiske overgang med rollen `repeated_transition_non_additive`, avgrenset uttrykkelig til 2024, 1860/01 og 4860/01. Rollen er en dokumentert analysebeslutning, ikke påstand om opphevelse.
3. **Begrunn regelen med flere primærspor.** Registrer identisk før/delta/etter, den uttrykkelige komitéfordelingen, begge faktisk vedtatte forslag, departementets felles gjennomføring og sluttkontrollen. Like beløp alene er ikke dedupliseringsgrunnlag. En annen kildeversjon eller annet før-/etterpar må utløse ny vurdering.
4. **Bevar kildebeløpet ved ikke-additiv opptelling.** For 40034226 lagres fortsatt +10 988 000 og −2 400 000 som publiserte deltaer. En teknisk opptellingsvekt på null betyr at den gjentatte overgangen ikke legges til på nytt. Den betyr ikke at kilden vedtok null eller at en DFØ-rad med null er observert.
5. **Ha to eksplisitte statuser.** `economic_effect=verified_once` kan gis på dette kildegrunnlaget. `formal_publication_conflict=unresolved` beholdes fordi den publiserte tilrådingen går ut over sin uttrykkelige saksavgrensning og ingen konkret uttaksrettelse er funnet. Brukeren skal kunne se begge deler. Unngå et felles «alle kilder feilfrie»-stempel.
6. **Sperr bokstavelig dobbel summering i godkjente analysetall.** 1860/01 skal ende på 360 312 000; 4860/01 på 83 400 000 kroner. En rå rekonstruksjon kan vise hva dobbelt tillegg gir, henholdsvis 371 300 000 og 81 000 000, men skal da merkes med kjedebrudd og avvik. Dersom systemets datamodell krever rettslig entydig hendelseskjede før godkjenning, må disse to kjedene forbli sperret i den visningen, mens sluttbeløp og dokumentert økonomisk behandling kan godkjennes separat.

Denne kontrakten gir to formelt dokumenterte vedtaksforekomster og én økonomisk overgang per post. Den oppfinner ingen mellomliggende økning, reduksjon eller reversering for å få sluttsaldoen til å stemme.

## Kontroller, råspor og begrensninger

`fetch-manifest.json` oppgir alle nye rå-URL-er, endelige URL-er, faktisk hentetid, HTTP-status, byteantall og SHA256. `raw/` inneholder de vellykkede originale svarene. `controls.json` inneholder de to voteringstemaene, forslag-ID-er, korte postutdrag, de fire relevante API-postobservasjonene, arvede inputhash og aritmetikk. Tekstfilene og PNG-ene er avledede kontrollfiler. Det er ikke skrevet mellomrapporter.

| Kontroll | Resultat |
|---|---|
| Begge innstillinger, alle sider/avsnitt | Lest; begge har postene i tilråding I |
| Forslag 40077095 og 40077047 | Samme to før-/etterpar i begge |
| Votering 23880 og 23976 | Begge relevante romertall enstemmig vedtatt |
| Referater 17. og 18. desember | Samme posttekst; intet uttak funnet |
| Beriktiget PDF, visuell kontroll | Postene står fortsatt på sider 2–3 |
| Lokal aritmetikk, begge poster | Før + delta = etter i begge forekomster |
| Sammenheng ved nytt tillegg 18. desember | Bryter med foregående etterbeløp på begge poster |
| DFØ og statsregnskap, ferdig årsgrunnlag | Én endring; sluttbeløp 360 312 000 og 83 400 000 |

Sentrale nye råhash:

| Råfil | SHA256 |
|---|---|
| `raw/inns-093.pdf` | `d1d414ee95142bfd0e4390134bbcfcba052015f341b9f792ceb7408517ebf978` |
| `raw/inns-099.pdf` | `8418baf1baa92454195ac145578b5af867066e2183a16cad3071339209bdd43b` |
| `raw/voteringer-100898.xml` | `24a2b8b8626c482e497878c6d5f89d6a5ac0646325d67fb8dc3ddf61c5d16e83` |
| `raw/voteringer-100894.xml` | `de7448e69f942f0d8f7a02224017654049463e28a155231967134500143ef82b` |
| `raw/voteringsforslag-23880.xml` | `842d4b207627e3f1d3ba8a05b35666c3f2371fd55e09071f3ab2370824992405` |
| `raw/voteringsforslag-23976.xml` | `bb3ed0f40f3943152fe8eb9504459b593cc96bb76da8dafa4c70323c9096a810` |
| `raw/ref-1217.html` | `61cc7b0a3ac67bd9c1e3637d843ebabe2e4dbc9d7ac78a224dcacea70fac8696` |
| `raw/ref-1218.html` | `30c3b9d3d1fb09980702bc526b4dcc97afb5b7b6819c1d2add6e800f275e28f2` |
| `raw/ref-1218.pdf` | `81dc43c8146464c448b4e6ddcd9200d9157a56f7e35fe16d948967685d1b4cfd` |

De to direkte vedtakssidene er gjenbrukt fra ferdig årsgrunnlag. Hashene er verifisert på nytt: 40034064 = `b0c02a2deda99ea0d1bdd8bd1a808d6a76290fdacb74fb01ed30e08a935bee79`; 40034226 = `4dd3027adee4a1b615166f8cf6325fb8d76330be3bbef5b2a2c4d56462fa5d7b`. API-sesjonsfilens inngående hash står i årsrapporten og er ikke erstattet med en ny versjon.

**Tilgangsbegrensning:** Direkte nedlasting av tildelingsbrevet ga HTTP 403. Ingen alternativ tilgang til denne PDF-en er forsøkt etter avslaget. Brevets tekst, dato og tabell var allerede synlig i offentlig nettsøk mot den samme offisielle URL-en. Den observasjonen har ingen bevart originalbytehash og skal ikke fremstilles som en råfil kontrollert mot originalbytes. En separat sidecar bevarer søkegjengivelsen som nettobservasjon, med tydelig skille mellom gjengivelsens egen hash og manglende originalhash. Den forespurte PDF-adressen for referatet 17. desember ga 404; fullt HTML-referat og voterings-API er bevart. Vanlig direkte nettbruk ble kjørt med nettverkstilgang etter DNS-feil i sandkassen. Ingen 403-omgåelse er brukt.

Undersøkelsen dokumenterer dermed hvordan den offentlige behandlingen og den faktiske administrative opptellingen henger sammen. Årsaken til at begge postene ble beholdt i energi- og miljøkomiteens tilråding, og den eksakte rettslige virkningen av denne publiserte motsetningen, er fortsatt ikke uttrykkelig forklart i en funnet rettelse. Dette restpunktet skal avgrenses til formell kildekonsistens; det gir ikke grunnlag for å doble de økonomiske endringene.
