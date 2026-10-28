# Uavhengig faktakontroll og samlet dokument-/spec-kontroll av K3/#50

Kontrollert 28. oktober 2026. Fast kandidat `5b6e86c13411ac703976447c5c21fc005f83b6a2`, sammenlignet med `37c6ad4572c030a6b3309201d836bb0c0c51f9c6`, i `work/k3-arsinventar`.

**Portutfall: Kunnskapsinnholdet består som presist avgrenset restusikkerhet. Samlet dokument-/leveranseport består ikke på denne kandidaten: ett nødvendig manifestfunn må rettes. Positiv M21/helårsaksept er fortsatt åpen.**

## Nødvendig retting

**F1 [P2] Leveransemanifestet hasher lokale Windows-byte av kildefunn.md, ikke den fastfryste Git-leveransen.** Fil `docs/research/k3-arsinventar-50/delivery-manifest.json:569–571` oppgir `docs/kildefunn.md` som 59 854 byte og SHA-256 `4491b4f28415d12441c199cc88c6f6a5ddafb1dcf537c447e51e906c5eb1c37c`. Dette stemmer med nåværende CRLF-arbeidsfil, men kandidaten har en Git-blob på 59 469 byte og SHA-256 `b80c0d294f7c0a801cb80305b2394c40c885116ed108bfc27bc7089e65ce09c6`. `git show 5b6e86c13411ac703976447c5c21fc005f83b6a2:docs/kildefunn.md` beviser forskjellen; LF-normalisering av arbeidsfilen gir Git-bloben nøyaktig. Lokal `.gitattributes` gjelder bare forskningsmappen og omfatter ikke `docs/kildefunn.md`.

En vanlig LF-checkout/Git-arkiv av den publiserte kandidaten vil dermed feile manifestkontrollen, selv om filen er uendret. Dette bryter den varige filbindingen beskrevet i `reproduksjon.md:111–113`; ny generering på samme Windows-maskin alene løser det ikke. Velg og dokumenter en stabil representasjon for denne teksten, for eksempel uttrykkelig Git/LF-normalisering i manifest og kontrolloppskrift, og regenerer oppføring/totalsum. Bevar råoriginalenes eksisterende byte. Kontroller deretter manifestet både mot kandidatens Git-blobber og arbeidsfiler etter den erklærte regelen. Ny revisjon må bindes til sluttporten.

Ingen øvrige nødvendige fakta- eller spec-rettinger er bekreftet innen kontrollgrensen.

## Faktisk kjørte uavhengige kontroller

Kontrollen brukte eget `factcheck.py` i denne eksterne outputkatalogen. Byggerens `verification.json` ble lest som en påstand, ikke brukt som bevis for nye kontroller.

- Kandidatens 114 endrede filer er sammenholdt med Git-blobbene. Omfanget er bare forskningsdokumenter, kildefiler, filattributter og `docs/kildefunn.md`; ingen produktkode. Arbeidstreet har samme uendrede untracked `.local/` og ingen endrede sporede filer. `git diff --check` bestod.
- Alle 113 oppføringer i leveransemanifestet er rehashet; lokalt stemmer alle, mot Git-blobbene stemmer 112 og F1 avviker. Manifestets unike filsett, antall og lokale totalsum stemmer.
- Alle 46 bevarte kilde-/transportforsøk er pakket ut og kontrollert mot råhash, gziphash, størrelse og metadatahash. URL, tidspunkt, status, registrert kropp og fullstendighet er avstemt med sidevognene. 42 er komplette vellykkede svar; tre avbrutte 200-svar og én komplett 500-feilkropp er holdt utenfor innholds-/fraværsbeviset.
- Alle 24 gjenbruksreferanser er rehashet og sammenholdt med basecommitten; begge komprimerte sesjonsforeldres ukomprimerte hasher stemmer. Arvet Innst. 447 er dessuten sammenholdt byteeksakt med den eksisterende lokale originalen og dens faktiske tidligere transportsidevogn. Ny/gammel 447 har samme normaliserte hovedtekst; dette er ingen påstand om full HTML-byteidentitet.
- Hele vedtaksregisterets 2 183 poster er omberegnet fra de autentiske komplette sesjonsoriginalene: ID, sak, nummer, dato, type, tittel, ordinal og de fire søkeordenes treff. Typefordeling og 25 treff/2 158 semantisk åpne uten treff stemmer. Gamle og nye sesjonssvar har identiske ID-sett og C14N for hvert komplett vedtaksobjekt.
- Begge saksindekser er parsede på nytt: 637 + 727 poster. Kandidatutvalget er rekonstruert fra faktiske metadata med det oppgitte mønsteret, inkludert ikke-BUDSJETT-grupper. 67 poster/66 unike saker og 60 åpne poster/59 åpne saker stemmer. Alle 25 vedtakstreff har en egen journalpost.
- Alle 43 tabellblokkers kildehash, tabellhode, radtilhørighet og 390 råcellerekker er kontrollert ved faktiske XPaths; 14 avsenderattributter stemmer. Videre er 77 registerpassasjer, 86 vedtaksrader, fem utvalgte passasjer og to komplette fullmaktstekster kontrollert mot originalene.
- Ti navngitte voteringer, fem vedtakskoblinger, åtte API-forslagsidentiteter/roller/HTML-hasher og 55 forslagsrader er kontrollert direkte i XML/HTML. 37 publikasjonsreferanser og 27 saksrelasjoner er avstemt mot faktiske lokatorer og råfelt.
- Sju RNB-forslagsblokker er også funnet uavhengig av byggerens lokatorliste. H 1, FrP 2, SV 21, R 22, V 29, MDG 49 og KrF 54 har hver /1-reduksjon 1 mill. fra 161 243 000 til 160 243 000 og ingen /22 i den avgrensede blokken. Voteringene 23425–23431 bekrefter hvert nummer, parti, for–mot og forkastet status. H/FrP-API-ene har identiske lokale 1429-rader som sine 447-blokker. Tilråding A.I er særskilt koblet til 857/23457.
- De fem vedtatte monetære posthendelsene og elleve vedtaksbeløpsfeltene er rekonstruert direkte fra 341/857/210. Alle tre før+delta=etter-kontroller stemmer; de er lokal aritmetikk. 341/857s år står i tekstinnledningen; 210s år krever den bevarte Innst. 81/Prop. 16-konteksten og er ikke utledet av datoen.
- Alle 61 JSON-filer, inklusive transportsidevogner, er dekodet med kontroll mot duplikatnøkler/ikke-standard tall. 93 lokale Markdown-lenkemål i leveransen og kildefunn.md eksisterer.

## Faglig/spec-vurdering

346/40032933 er faktisk et ytterligere 2024-vedtak om merinntektsfullmakt for 1429/1 mot 4429/2 og /9. Det inneholder ingen ny fast tallfestet bevilgning og skal ikke øke de fem monetære hendelsene. Innst. 14s H-/FrP-nivåer, avviksparenteser, flertallsmerknad og tilråding er korrekte i leveransen; uavklart separat originalbudsjettvotering er ærlig oppgitt.

Prop. 36 vedlegg 3 har faktisk /1 +5 796 000 og −1 000 000, samt /22 −3 000 000 med de oppgitte proposisjons-/innstillingshenvisningene. Vedlegg 6 har 161 243/32 185 i saldert, +4 796/−3 000 i periodens foreslåtte endringer og 166 039/29 185 i status, i tusen kroner. Begge kildenes overskrifter/kolonner støtter leveransens begrensning: foreslått/vedtatt kildeliste og foreslått status, ingen ekstra vedtatt hendelse eller uttømmende årsbevis. De bevarte svarene viser dessuten «Foreløpig utgave»; dette endrer ikke den eksplisitte statusgrensen.

Årseksklusjonene 334/408 og 201/401/427, andre konti/poster i de øvrige journalpostene, tillegg 1s 1481/25-fullmakt, tillegg 2s konkrete departements-/salderingsomfang og Prop. 106s separate forslag er kontrollert mot råinnhold og lokale tabeller/overskrifter. Ingen av eksklusjonene bygger bare på manglende ordtreff eller departementstittel.

R1–R7 er presise nok til den uttrykkelig autoriserte alternative K3-leveransen: omfangene er tallfestet/navngitt, kildenes øyeblikks- og versjonsgrense er synlig, og hver rest har et senere lukningskrav. Undersøkelsen tilfører faktisk nytt kildemateriale, fullmakt 346, alternative forslag, behandlingsutfall og en annen kontrollinngang. Den er dermed mer enn en ny oppsummering av 341→857→210. Restene lukker ikke positiv M21/full V2 og gir ingen faglig årsbalanse.

P1 er ett senere komplett forslag om å føre et uttrykkelig delvis perioderegister gjennom begge innganger til faktisk JSON/Excel. Teksten holder det som forslag med eget mandat. Ingen T5/T6, kontokontinuitet, drift eller produktfiler er startet. Live GitHub-lesning viste #10/#32/#37 åpne. PR/CI/merge og fullføring av #50 gjenstår hos orkestratoren.

## Kontrollgrense og reproduksjon

AGENTS, arbeidsflyt, kildefunn, hele #50/#37/#48 med kommentarer, siste T4-overlevering, konto-/årsundersøkelsen, M21/K3-utkastet, kandidatdiffen og kunnskapsleveransen er gjennomgått. Ingen kandidatfil, staging, commit eller GitHub-innhold er endret av kontrollen; bare denne outputkatalogen er skrevet.

Kjør med den lokale bundlete Python 3.12/lxml-installasjonen:

```powershell
& 'C:/Users/marti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'C:/Users/marti/Documents/ChatGPT/Budsjetthistorikk/outputs/k3-factcheck/factcheck.py'
```

Maskinresultatet ligger i `results.json`: ett bekreftet leveranseavvik, F1. Innledende harnessantakelser om XML-nil/nestede metadata, ekstra registerpassasjer, 500-transportfullstendighet og 210s manglende egen årsinnledning er korrigert mot originalene; disse var ikke kandidatfeil.

Ingen ny HTTP-autentisering, full semantisk gjennomgang av de 2 158 ikke-treffene/59 åpne sakene, full partipublikasjons-/salsforslagskontroll, produkttestsuite, Linux-CI, native Excel eller produksjonskontroll er utført. Nettlenkemål er ikke testet som nettressurser. Kontrollen er ikke en code review eller sikkerhetsaudit av produktkode. Disse begrensningene gjør ingen positiv helårsaksept mulig; den avgrensede K3-kunnskapsaksepten er faglig oppfylt når F1 og den etterfølgende faktiske leveringsporten er håndtert.
