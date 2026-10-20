# Issue #2 – selvstendig bevilgningsvedtak fra presidentskapet

Kildekontroll 20. oktober 2026. Rapporten bygger utelukkende på Stortingets primærkilder. Det er ikke gjort GitHub-endringer eller endringer i produksjonskode.

## Konklusjon

**En reell positiv prøve er funnet:** Stortinget bevilget **7 000 000 kroner på kap. 41 post 21 i statsbudsjettet for 2003** til granskingskommisjonen for Mehamn-ulykken. Bevilgningen ble fastsatt i **vedtak 249, ID 40005719, sak 26250, 6. februar 2003**, etter **Innst. S. nr. 114 (2002–2003)** fra presidentskapet. Det er en selvstendig innstillingssak. Vedtaks-API-et klassifiserer vedtaket som `BUDSJETT`; vedtaksteksten fastsetter selv beløp, kapittel, post og budsjettår. [Endelig vedtak](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did=40005719&p=26250), [offisielt vedtaks-API for sesjonen](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2002-2003).

Det er ikke funnet proposisjonsgrunnlag i den undersøkte relevante dokumentkjeden: representantforslaget, den opprinnelige komitéinnstillingen, presidentskapets bevilgningsinnstilling eller den parallelle lovinnstillingen. Saksmetadata for de tre tilhørende sakene inneholder heller ingen proposisjon eller relasjonskant til en proposisjon. Denne avgrensede påstanden er underbygget både med metadata og fulltekst. Den er ikke en påstand om fravær av enhver proposisjon i all forhistorie til ulykken, tidligere granskinger eller statsbudsjettet.

## Endelig bevilgning og kontroll

Fasit for den historiske positive prøven:

- Sesjon: **2002–2003**. Budsjettår: **2003**. Vedtaksdato: **6. februar 2003**.
- Sak: **26250**. Vedtak: **249**. API-ID: **40005719**.
- Kapittel: **41 Stortinget**. Post: **21 (ny)**.
- Formål: **Spesielle driftsutgifter, Granskingskommisjonen for Mehamn-ulykken**.
- Stikkord: **kan overføres**. Operasjon: **bevilges med**. Beløp: **7 000 000 kroner**.
- Side: utgift. Vedtaket angir ingen fra-/til-beløp; slike skal ikke tilføyes som om de var kildeopplysninger.

Kapittelnummeret står på en egen rad, mens post og beløp følger på neste rad. Den lagrede API-teksten inneholder eldre HTML med `FONT`, `DIR`, tabellceller og HTML-entiteter. Bevilgningen er også kontrollert mot den separate vedtakssiden. [Vedtaks-API](https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2002-2003), [vedtakssiden for saken](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?p=26250).

Referatet gjengir bevilgningstabellen under voteringen i sak nr. 5 og opplyser at presidentskapets innstilling ble enstemmig bifalt. Dermed er det kontrollert at tabellen ble vedtatt. [Referat og votering 6. februar 2003, sak nr. 5](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2002-2003/030206/5/).

## Undersøkt initiativ- og dokumentkjede

1. **Representantinitiativ, sak 25782:** Odd Roger Enoksen fremmet Dokument nr. **8:27 (2002–2003)** om stortingsoppnevnte granskingskommisjoner. Originalforslaget er hentet og lest. Det inneholder ingen konkret kapittel-/postbevilgning. [Forslaget](https://data.stortinget.no/eksport/publikasjon?publikasjonid=dok8-200203-027), [saksmetadata](https://data.stortinget.no/eksport/sak?sakid=25782).
2. **Opprinnelig komitébehandling:** Innst. S. nr. **74 (2002–2003)** har representantforslaget som kildedokument. Vedtak **184**, ID **40005595**, 16. desember 2002, ber presidentskapet oppnevne kommisjonen og fastsette mandat. Dette etablerer initiativet, men gir ingen bevilgning. Vedtak 183/40005594 vedlegger forslaget protokollen; vedtak 185/40005596 gjelder rapporten om «Utvik Senior». [Hele innstillingen](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-200203-074), [de endelige vedtakene](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?p=25782).
3. **Selvstendig presidentskapssak, 26250:** Innst. S. nr. **114 (2002–2003)** viser uttrykkelig tilbake til vedtaket 16. desember og Innst. S. nr. 74. Presidentskapet fastsetter mandatet og fremmer selv forslag om finansiering i 2003. Forslaget munner ut i den konkrete bevilgningen i vedtak 249. [Hele innstillingen](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-200203-114), [saksmetadata](https://data.stortinget.no/eksport/sak?sakid=26250).
4. **Uttrykkelig henvist parallellsak, 26251:** Innst. O. nr. **61 (2002–2003)** gjelder kommisjonens adgang til å innhente bevis. Den viser tilbake til Innst. S. nr. 74 og til den parallelle bevilgningsinnstillingen nr. 114. Hele lovinnstillingen og sakens metadata er hentet. Det fremkommer ikke en proposisjon som grunnlag for bevilgningen. [Lovinnstillingen](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inno-200203-061), [saksmetadata](https://data.stortinget.no/eksport/sak?sakid=26251).

Alle tre saksdetaljer har tom `sak_relasjon_liste`. De tekstlige forbindelsene ovenfor er derfor nødvendige tillegg til API-relasjonene. [saksgraph](selvstendig-saksgraph.json) bevarer alle publikasjonspointere og skiller dem fra de kontrollerte teksthenvisningene. Lovsakens senere lovvedtak og Odelstings-/Lagtingsreferater er registrerte pointere, men deres fulltekst er ikke hentet; de er ikke brukt som bevilgningsbevis. Eldre særlover og tidligere ulykkesgranskinger som omtales i lovinnstillingen, er ikke gransket bakover.

**Metadataavvik må bevares:** Sak 26250 oppgir `eksport_id=inno-200203-114`, mens lenke-URL og dokumenttittel gjelder Stortingets **inns-200203-114**. Tilsvarende oppgir sak 25782 `inno-200203-074` for **inns-200203-074**. De riktige publikasjonene er valgt etter dokumenttittel, forsamling og kanonisk URL, og kontrollert mot innholdet. Råverdiene er bevart. En ukritisk bruk av eksport-ID alene kan gi feil kilde. [26250](https://data.stortinget.no/eksport/sak?sakid=26250), [25782](https://data.stortinget.no/eksport/sak?sakid=25782).

## Andre undersøkte identifikatorer og avgrensning

Det målrettede nettsøket identifiserte også **Innst. S. nr. 10 (2002–2003), sak 25502, vedtak 24/40005350**, 12. november 2002. Den endelige teksten bevilger 800 000 kroner på kap. 41 post 21 og øker post 1 og 45. Forslaget kommer fra presidentskapet, og referatet dokumenterer enstemmig tilslutning. [Vedtaket](https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?p=25502), [voteringen](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2002-2003/021112/1/Votering-i-sak-nr-1).

Denne kandidaten er svakere for den strengeste fraværspåstanden: innstillingen omtaler byggeprosjektets plass i forslaget til statsbudsjett for 2003. Den er derfor beholdt som ekstra kontroll på selvstendig bevilgningsbehandling, uten å være hovedbevis for en kjede uten proposisjonsgrunnlag. Den henviste **Innst. S. nr. 175 (1999–2000)** er hentet og lest som bakgrunn for post 21; dens endelige vedtak er ikke undersøkt. Sak 25502 har dessuten eksport-ID `innb-200203-010` samtidig som URL og innhold gjelder **inns-200203-010**. [Hele Innst. S. nr. 10](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-200203-010), [sak 25502](https://data.stortinget.no/eksport/sak?sakid=25502), [Innst. S. nr. 175](https://data.stortinget.no/eksport/publikasjon?publikasjonid=inns-199900-175).

Søket var målrettet mot presidentskaps- og representantinitiativer. Det ble brukt presise nettsøk avgrenset til `stortinget.no`, blant annet kombinasjoner av «representantforslag», «bevilges», «kap.», «presidentskapet» og «tilleggsbevilgning». Søkeresultatene er bevart lokalt i `search1.json`–`search4.json`; søkeresultaters sammendrag er ikke fasit. Etter at kandidaten var identifisert, ble vedtakslisten for **bare sesjonen 2002–2003** hentet for å kontrollere nøyaktige API-ID-er. Listen er ikke brukt som en ny generell screening. Ingen andre komplette eldre vedtaksår er hentet. Innst. 197 S (2019–2020) er ikke undersøkt på nytt.

## Betydning for gate og testkontrakt

**Kildegaten for et faktisk selvstendig bevilgningsvedtak uten funnet proposisjonsgrunnlag i relevant undersøkt kjede kan bestås.** Vedtak 249/40005719 er en historisk positiv fasit. Resultatet sier ikke hvor ofte slike vedtak forekommer, og verifiserer ikke produktets faktiske innhenting eller klassifisering.

Følgende kontrakt bør inngå i implementeringskravet:

- Alle vedtak er kandidater uavhengig av dokumentgruppe, forslagsstiller og tilstedeværelse av Prop.-metadata. Manglende proposisjon gir ingen eksklusjon.
- Den autentiske prøven **40005719** skal gi én bevilgningslinje: budsjettår 2003, kap. 41, post 21, 7 000 000 kroner, `bevilges med`, `kan overføres`, med sporbar kobling til endelig vedtak.
- Proposisjonsmetadata er opprinnelsesinformasjon. Dersom de mangler, kan øvrige opplysninger og bevilgningen fortsatt valideres. Eventuelle konstruerte variasjoner av metadata merkes som kontrakttester, atskilt fra historisk kildebevis.
- **40005595**, **40005716** og **40005718** skal ikke skape bevilgningslinjer: de gjelder henholdsvis oppnevning, taushetsplikt og tilgang til materiale. Samme sak kan inneholde både bevilgning og andre vedtak.
- Innsamleren må håndtere tekstlige sakshenvisninger og dokumentere avvik mellom eksport-ID og kanonisk URL. Tom relasjonsliste skal ikke tolkes som bevis for fravær av relevant kildegrunnlag.

## Råfiler og kontrollresultat

[hentemanifest](selvstendig-hentinger.json) inneholder URL, hentetid, responsstatus, størrelse og SHA-256 for **17 råsvar**, alle med HTTP 200 og kontrollert filhash. Råfiler har endelsen `.raw`; `.text`, `.html` og `*.decisions.json` er avledede inspeksjonsfiler. [utvalgte API-vedtak](selvstendig-api-vedtak.json) inneholder bare de syv kontrollerte API-vedtakene fra sakene 25502, 25782 og 26250.

[fasit og kontroller](selvstendig-fasit.json) inneholder normalisert positiv prøve og **17 beståtte kildekontroller**. Det lokale inspeksjonsskriptet er ikke produksjonskode og følger ikke repoet. Hentemanifest, fasit og utvalgte API-vedtak er versjonert. Kontrollen dekker vedtaksidentitet, dato, API-type, beløp, budsjettår, kapittel/post, vedtatt votering og fravær av proposisjonshenvisning i de fire sentrale publikasjonsfulltekstene. Dette er kildekontroll; produktets tester er ikke kjørt.
