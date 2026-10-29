# Lesejournal og uttrykkelig restgrense

Utført 29. oktober 2026. [Beleggene](evidence.json) binder HTML/XML til
råhash og eksakt XPath, og visuelle belegg til PDF-/bildehash og side.
Komplett råbevaring, avledet tekst og faktisk lesedybde er forskjellige.

## Hovedtekst og behandling

| Kilde | Lest delomfang og resultat |
| --- | --- |
| K3 komplett indeks | Hele det konkrete objektet på ordinal 114: sak 99235, behandlet sesjon 2023–2024, Prop. 108/Innst. 442, innstilling 16526. Kandidatlisten er kontrollert separat; ingen historisk medlemsstatus oppfinnes. |
| Nytt saks-API | Hele saksobjektet med publikasjoner og saksgang. Fremmet/ref 7. juni, avgitt 13. juni, BEHS20. juni og VOT21. juni er egne felter. Rå0001-datoer for andre steg brukes ikke som faktisk dato. |
| Prop. 108 kapittel 1 | Hele innledningen om utbetaling av nye lønninger i statlig tariffområde våren 2024; forslagets rolle og omfang. |
| Prop. 108 kapittel 2 | Hele åtteavsnittsteksten: fire hovedsammenslutninger, avtaleperiode 1. mai 2024–30. april 2026, forhandlingsbrudd/mekling, møtebok 24. mai og egne vedlegg, medlemsavstemning, streik/nemnd og utsatt utbetaling. Nødvendige bevilgninger skal foreslås høsten 2024. |
| Prop. 108 tilråding/forslag | Hele kongelige tilråding og alle fire operative romertall. Hjemmel, nemndsbasert betaling og de to LO/YS-vilkårsgrenene er skilt. |
| Innst. 442 | Hele `#m1`, `#m2`, `#m3`. Samlet tilråding og ulike merknadsavsendere er lest separat. 2022-/2023-/2016-bakgrunn og medieutsagn brukes som attribuert omtale. Ingen full undersøkelse av bakgrunnskildene påstås. |
| Debatt 20. juni | Hele lokale sak 15: president, Greni, Linnestad, statsrådTung, avslutning og fremoverlenke til 21. juni. LO-nei/YS-ja og nemndsforventning er bevart som talerutsagn. Ingen endret vedtakstekst er funnet fremsatt i dette komplette lokale referatet. |
| Votering 21. juni | Hele lokale blokk `#2024-06-20-15`, med alle fire romertall og enstemmig resultat, samt møtedato/start og overgangen til dagens kart. Hele mottatte 25,47 MB-svar er bevart; øvrige saker er ikke undersøkt. |
| Voterings-/forslags-/vedtaks-API | Hele responsene for 99235/23490, alle fire tilrådingsforslag og vedtaksreferanser. −1-sentineler bevares. De fire bevarte endelige sesjonsobjektene er lest komplett og sammenlignet kanonisk med tidligere sesjonsrepresentasjon. |
| R2 s datoutsagn | Eksakte Prop. 34 p2/p8/p9 og hele Innst. 91`#m2_1` er gjenlest fra gamle originaler for C06/datoformålet. Dette er ikke gjenåpning av 101000. |
| Kjent høstkontekst | Bare eksisterende Prop. 36 kap 5/metode og vedlegg 4s 1429-blokk 292–294 er brukt. Gamle roller og/uavklart faktisk anvendelse består. |

## Egne vedlegg: full bevaring og dokumentert lesedybde

Begge egne vedlegg er komplett bevart i den fulle PDF-en: LO-bilder på
PDF-side 11–75 og YS-bilder på 77–141, 65 bilder hver. Mellomside 76 har
overskrift for YS; den er del av full PDF, uten tariffbilde. Alle 144 PDF-sider
er inventert. Det hevdes ingen identiske JPEG-byte mellom HTML-medier og
PDF-bilder, og ingen unødvendig ekstra HTTP-kopi av 130 bilder er hentet.

Alle 130 innlagte bilder er lokalt ekstrahert og OCR-behandlet. Det fullstendige
avledede OCR-materialet bevares tapsfritt som gzip; motoren har bare en-US
gjenkjennerspråk tilgjengelig. OCR kan særlig forveksle norske bokstaver,
§/5, I/1 og tall. Det er et søke-/seksjonsgrunnlag, ingen feilfri transkripsjon.
[Sidejournalen](appendix-reading-journal.json) fører hver eneste side,
bildehash, OCR-teksthash, emne, visuell kontrollstatus og rest.

| Figurordinal i hvert eget vedlegg | Undersøkt innhold og praktisk grense |
| --- | --- |
| 1–2 | Møteboka 2024-026/027: parter, møtedatoer, fremlagte dokumenter, tilrådd løsning, svarfrist 20. juni, avslutning 08.20 og signatur. Begge møtebøkenes to bilder er visuelt lest. Svarfristen er ikke vedtaksdato. |
| 3 | Økonomiprotokoll: likelydende avtalekrav, 5,2%-ramme, glidning/overheng, 75/25-fordeling, 0,75%-tillegg, minstelønn/virkning og adgang til ny økonomiforhandling ved bedre nemndsresultat. Begge bilder visuelt lest. Ingen virksomhets-/postberegning utledes. |
| 4–5 | Parter og virkeområde, stillinger utenfor avtalen, lønnsplaner/stiger, regulering 2. avtaleår og lokale parter. Figur 4 i begge vedlegg visuelt lest. Generelt omfang etablerer ikke personell-/postanvendelse hos Riksantikvaren. |
| 6–11 | Forhandlingssteder, lokal lønnspolitikk, virkeområde, 2.5.1-avsetning, ledere/særlige grunnlag, virkemidler, ansettelse/permisjon, forhandlingsregler og tvister. § 2.2/figur 6 visuelt lest i begge; resten er OCR-/seksjonsgjennomgått. DFDs forholdsmessige lønnsmasseberegning og lokale budsjettdrift er ikke en observert 1429-fordeling. |
| 12–26 | Fellesbestemmelser om lønn/ansiennitet, arbeidstid/skift, utbetaling, overtid/tillegg, sykdom/permisjon, omsorg, dødsfall og yrkesskade. OCR-/seksjonsgjennomgang; ingen feilfri manuell transkripsjon eller rettslig anvendelseskontroll. |
| 27–28 | Tjenestepensjon/AFP, årskull, inntektsavkortning og variable tillegg. Egne tariffroller, ingen nye 1429-bevilgningshendelser. Faktisk personell-/pensjonsgrunnlag uavklart. |
| 29–34 | Boliglån, OU, fellesopplæring/kompetanse, omstilling, virksomhetsovergang, senior/livsfase, innleie, likestilling, ferie, varighet og protokolltilførsler. OCR-/seksjonsgjennomgang; de konkrete interne ordningene er journalført som bakgrunn/åpen faktisk anvendelse. PDF-side 39/40/105/106 er også visuelt lest for OU-/kompetanse-/omstillingsteksten. Eksterne særavtaler og tildelinger er ikke fulgt. |
| 35–55 | Internt tariffvedlegg 1 med lønnsstiger, stillingskoder, minstelønn og godskriving. Figur 40 i begge er visuelt kontrollert: 1429 Aspirant 357 000 er stillingskode og minstelønn, ikke budsjettkapittel/bevilgning. Hele lønnsplanheftet er ikke manuelt celletranskribert. |
| 56–62 | Internt tariffvedlegg 2 med alle virksomhets-/forhandlingsstedslister. Figur 59 i begge er visuelt lest i sin helhet, inkludert KLD-blokken med Riksantikvaren i begge kolonner og nabogrenser mot Justis/KDD/Kultur. Det gir positiv institusjonsrelevans; ingen arvet kontopost. |
| 63–65 | Interne vedlegg 3–5: omstilling under trygghet og pensjonsgivende variable tillegg for ulike årskull. OCR-/seksjonsgjennomgang. Ingen faktisk omstillings-/tilleggs-/pensjonstildeling eller kontoføring for Riksantikvaren er dokumentert. |

De 18 visuelt leste bildene er PDF-side 11/12/13/14/16/39/40/50/69 og
77/78/79/80/82/105/106/116/135. [Visuelle belegg](evidence.json) er eksplisitte
transkripsjoner eller merkede parafraser, ikke tekster som kan bevises ved
XPath-likhet. En uavhengig kontroll må lese bildene for å kontrollere dem.

Dette oppfyller full råbevaring og dokumenterer den utførte avgrensede
innholdsundersøkelsen. Det er ingen påstand om uttømmende semantisk,
visuell, rettslig eller faktisk postkontroll av hver setning i 130 bilder.
Eventuelle oversette detaljer eller uklar OCR holdes som rest; de er ikke
omgjort til generell 1429-eksklusjon. Det positive institusjonsbelegget og
hovedkjedens operative vedtak er grunnlaget for den begrensede konklusjonen.

## Samlet konklusjonsgrense

Vedtakene har positivt dokumentert samtykke-/hjemmelsinnhold, og kildene
utsetter de nødvendige bevilgningsforslagene til høsten 2024. Derfor er
ingen ny postvis 1429-bevilgning belagt her. Faktisk indirekte lønnsvirkning
for virksomheten er fortsatt uavklart, selv om dens forhandlingssted er
belagt. /22 får ingen forklaring fra/1. Restene i
[kryssreferansejournalen](cross-reference-journal.json) og K3 sR1–R7 består.
