# Godkjent O2-pilot fra original til gjenlest omtaleuttrekk

Godkjent av prosjekteieren 22. oktober 2026 under #32. **Oppdelingen er publisert som #34/O2a og #35/O2b. O2a har gjennomføringsmandat; O2b krever eget senere mandat etter A.** O1s [rapport og kildepakke](README.md) er grunnlaget. Hver ticket skal levere et komplett snitt gjennom innlesning, analyse og faktiske filer. [O2a-kontrakten](../../omtale-pilot.md) fastsetter konkret format før produktkode. O3–O5 er ikke inkludert.

## Konkret pilot og observerbar atferd

Brukeren velger de bevarte originalversjonene til Prop. 16 S/Innst. 81 S, plenumsbeviset og 210-revisjonen. Fra kap. 1429 post 1 eller 22 får brukeren vedtaksendringen, full relevant omtale, overskriftshierarki, originalhenvisning, avsender og den dokumenterte behandlingskjeden. Regjeringens forklaring, innstillingens sammendrag, samlet komités støtte og Stortingets vedtakelse er ulike roller/relasjoner.

O2 avgrenses til disse to posthendelsene i budsjettåret 2024. Ikke generell import av regjerings-/komitébeløp: eksakte forslagsrader kan brukes som relasjonsbelegg uten nye beløpsobservasjoner. Omtalen skal ikke kreve historisk startsaldo, registergodkjenning eller årsavstemming. Post 60 bevares som nabokontekst uten beløpsrelasjon til 210. O2 trenger ingen annen prøvesak; flertall/mindretall og faktisk komitéendring krever senere O3-kildevalg.

## Godkjent kompatibilitetsgrense

- Et separat, lokalt omtalegrunnlag brukes i første pilot. Det binder uforanderlige originalartefakter, dokument-/representasjonsidentiteter, uttrekksversjon, seksjoner og eksplisitte relasjoner til eksisterende eksakte vedtaks-/observasjons-ID-er. Ingen omtaletabeller skrives i hovedschema 5. Eventuell felles databaselagring vurderes senere.
- Det eksplisitte eksportformatet `omtale-pilot-1` inneholder det uendrede valgte B8/B6-grunnlaget og omtalegrunnlaget. Ingen omtalenøkler legges inn i `b6-frozen-1`/`b6-frozen-2` eller deres lesere/skrivere. Formatnavn og [feltkontrakt](../../omtale-pilot.md) er fastsatt i O2a før produktkode.
- Et eget opt-in analysevalg skriver til nye JSON-/Excel-filnavn. Gamle CLI-standarder, B7s frosset-v1, rapport-ID-er, B1/B2-parser og B3-tolkninger, B5-avgjørelser og B8/B9-resultater beholder betydningen. Gamle Excel-filer gjenleses uten omskriving. B9s Historikk beholder sine 13 kolonner; egne Omtale-, Relasjoner- og Omtalekilder-ark inngår i det nye uttrekket.
- Hver seksjon binder dokumentidentitet, eksakt representasjonshash, uttrekksversjon, lokator, full tekst og hierarki/kontekst. PDF og HTML er forskjellige representasjoner av samme identifiserte dokument, med kontrollert representasjonsrelasjon. Manglende kilde eller ukjent rolle er synlige statuser, aldri et oppdiktet kildebevis.
- Relasjoner har egen identitet, kildebelegg, rolle, omfang og avklaringsstatus. Konto-, forslag-, støtte- og vedtakelsesbevis skal kunne etterprøves hver for seg. Et synlig «ikke koblet til 210» må ikke forveksles med mislykket henting eller feil lokator. Faglig kontroll er separat fra teknisk verifisert relasjon.
- Omtalegrunnlaget er et frivillig supplement etter vedtaksinnlesning. Manglende/korrupt/motstridende omtale gir avvik i omtaleuttrekket, uten å hindre registrering og ordinær eksport av nye offisielle vedtak. Historisk Excel er ingen avhengighet. #10 står åpen.

Dette er den godkjente byggegrensen for O2a. Den konkrete kontrakten og kandidatkontrollene beskrives i pilotveiledningen; review, sikkerhetsaudit, CI og merge er egne leveringsporter. Ingen søketjeneste, modell eller skyressurs inngår.

## Felles aksept for begge byggetickets

Den bekreftede testgrensen skal gjennomføres i hver ticket: **bevart original → omtaleseksjon med kildepeker → dokumentert relasjon til faktisk vedtak/hendelse og kapittel/post → skrevet og faktisk gjenlest JSON og Excel**. Intern objektkontroll, en rapport om at skriving lyktes eller fil-eksistens er utilstrekkelig.

1. Deterministisk CI starter med O1s autentiske, hashkontrollerte originaler, eksisterende 210- og saksprøver. Bare lokale kildeprøver brukes i CI. Live kontroll er separat og loggføres med faktisk respons/feil.
2. Kilden lagres/åpnes på nytt før analyse. JSON leses fra disk, Excel åpnes med uavhengig lesing av faktiske celleverdier, tekster, fortsettelsesrader og henvisninger. Eksporten må kunne gjenleses og kontrolleres uten nett eller tilgjengelig opprinnelig database.
3. For hver eksportert tekst kontrolleres identitet, eksakt tekst, hash/lokator, dokumentversjon, hierarki, avsender, relasjonsbevis og status mot originalen. Full tekst bevares selv ved lange felt; ingen stille Excel-avkutting. Kildetekst som begynner med formeltegn skal fortsatt være tekst.
4. Samme kilde/uttak to ganger gir stabile ID-er, ingen nye beløpshendelser og ingen tap av råtekst. Dokumentendring og ny uttrekksversjon gir separate grunnlag, med bevart tidligere resultat. Tekstendring med gammel hash eller feil lokator skal oppdages ved gjenlesing, ikke godtas som kontrollert relasjon.
5. Eksisterende B6/B8/B9-prøver gjenleses uendret. Hele 210-grunnlaget har fortsatt seks beløpsobservasjoner og to posthendelser; forslagsrader/omtale gir null ekstra hendelser. Et postfilter begrenser visningen, ikke det globale inventaret eller avvikene.
6. Med manglende, feilet, korrupt eller motstridende omtalegrunnlag og uten historisk Excel skal en autentisk ny offisiell vedtaksprøve fortsatt oppdages, lagres og ordinært eksporteres gjennom eksisterende inngang. Syntetiske feil er tydelig merket. Tomt kontoresultat skal fortsatt vise globale omtaleavvik i den nye eksporten.

## Byggeticket A: post 1 med dokumentert behandlingskjede

**Publisert:** [#34 – O2a: Les 210/1429/1 fra originalomtale til kontrollert JSON og Excel](https://github.com/depmartin/budsjetthistorikk/issues/34).

**Del av:** #32. **Status:** autorisert og under gjennomføring. Ingen gjenstående faglig/teknisk blokkering. O1 er godkjent kildegrunnlag; #32, #10 og #13 behøver ikke lukkes først.

**Leveranse:** Ett kjørbart lokalt opt-in snitt for post 1. Bevar originaler, strukturer P1/K1/KS/KT/V og bind dem med PT og eksisterende 210-revisjon. Definer og dokumenter den minste versjonerte pilotkontrakten og ID-regelen. Lever et ekte JSON-/Excel-par som kan kontrolleres fra kildene ved gjenlesing. Fullstendige dokumenter bevares selv om bare denne postens relevante seksjoner struktureres.

**Aksept i tillegg til fellesgrensen:**

- Fra post 1 vises +5 796 000, før 160 243 000 og etter 166 039 000 som uendrede vedtaksobservasjoner. Den fullstendige regjeringsomtalen har både 3 mill. omdisponering og avrundet lønnsanslag. Lønnsanslaget lagres ikke som eksakt 2 796 000 eller ny vedtaksendring.
- Koblingen til post 22 i P1 er synlig som utsagn om finansieringen, selv om full post 22-visning kommer i B. Ikke opprett en falsk enkeltpostseksjon av avsnittet som navngir begge poster.
- Komiteens sammendrag står som gjengivelse av regjeringen, KS som samlet støtte, KT som tilråding og V som vedtakelse. «Mindretall kontrollert fraværende i Innst. 81 S» skilles fra ukjent rolle i en syntetisk prøve.
- Bevar PDF-side 3 og hele HTML-P1, kapitteloverskrift fra søskenstrukturen, samt representasjonsforbindelsen. Feil kildeversjon/lokator eller konto, endret tekst og ukjent rolle skal oppdages/synliggjøres gjennom de faktisk gjenleste filene.
- Gjenles første leveranses frosne resultat uten kilde-/databasetilgang og demonstrer gamle JSON-/Excel-resultater og ordinær ny vedtaksinnlesning etter fellesgrensen. Ingen automatisk faglig godkjenning.

**Utenfor:** Generell forslagsbeløpsimport, full post 22-relasjonseksport, andre proposisjoner/innstillinger, søk og drift. Ticketen er likevel komplett for post 1 gjennom alle lag; den er ikke en ren lager-/parserleveranse.

## Byggeticket B: post 22 og felles omdisponeringsomtale

**Publisert:** [#35 – O2b: Gjenles begge 210-postene og felles omtalerelasjoner uten dobbelttelling](https://github.com/depmartin/budsjetthistorikk/issues/35).

**Del av:** #32. **Blokkert av:** A levert og kontrollert, samt eget byggemandat. Har ingen avhengighet til O3, historisk import eller #10.

**Leveranse:** Utvid samme komplette snitt til P22/K22 og begge postenes relasjoner. Bevar P1 som én seksjon med uttrykkelige omfang/belegg til begge postene; lønnsdelen gjelder bare post 1. Ta med PN/post 60 som autentisk tekst uten beløpsrelasjon til 210. Skriv og gjenles reelle nye JSON-/Excel-filer for begge poster og separate filtre.

**Aksept i tillegg til fellesgrensen:**

- Post 22 viser −3 000 000, før 32 185 000 og etter 29 185 000, med tilbakepekingen til post 1 i originalene og den komplette kjeden til 210. Omtalens «kulturmiljøforvaltning» og tabellens «kulturminneforvaltning» gjenleses uendret som ulike rånavn.
- Både post 1- og post 22-utvalg finner felles omdisponeringsomtale, uten kopiert seksjonsidentitet eller flere beløpsobservasjoner. Lønnsforklaringen blir ikke en begrunnelse for reduksjonen på post 22. Etter gjenlesing er det fortsatt nøyaktig to posthendelser og seks vedtaksbeløpsobservasjoner totalt.
- Post 60/Vega-tekst bevares med nabokontekst/fullmaktsrolle og ingen 210-beløpskobling. Den blir ikke en tredje hendelse. Et syntetisk uavklart relasjonsforslag bevares som uavklart med belegg/grunn, og skal ikke erstatte dokumentert kobling eller bli godkjent automatisk.
- Reell mange-til-mange-struktur, tomme postfiltre med globale avvik, syntetisk feilaktig postkobling og motstridende omtale prøves ved faktisk JSON-/Excel-gjenlesing. Ingen join på bare konto/beløp får opprette en ny dokumentert relasjon.
- A-formatets tidligere pilotresultat kan fortsatt leses uendret. Om kontrakten må utvides utover dokumenterte utvidelsesregler, kreves ny eksplisitt pilotformatversjon med egen leser; ingen stilltiende endring av tidligere ID-er/feltbetydning.

## Beslutning og etterfølgende arbeid

Prosjekteieren har godkjent **to komplette tickets A → B**, separat omtalegrunnlag og eksplisitt ny piloteksport med uendret fellesgrense. #34 gjennomføres nå; #35 har ikke gjennomføringsmandat. Eksakt lønnsberegning er et synlig kunnskapshull som fortsatt står åpent; den blokkerer ikke dokumentasjon av den vedtatte postendringen.

O3 skal først undersøke og bevare en faktisk komitéendring med autentiske flertalls-/mindretallsroller. O4 krever eget konto-/årsvalg og kildeinventar; O5 krever eget søkeomfang og regler for kontokontinuitet. Disse er ikke ferdige byggetickets og er ikke gitt et skjult byggemandat her. #10s driftsaksept står fortsatt åpen.
