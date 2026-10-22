# B9: kontroll av hovedvisning og bevarte detaljer

Kontrollert 22. oktober 2026 for #30 mot base `a7fc7d9996733dcaa73589c2fa8a3906059b4413`. Dette er en presentasjonskontroll på eksisterende bevarte kilder, uten ny HTTP, kildeimport eller faglig godkjenning. Samlet Standards-/Spec-review, separat sikkerhetsaudit, CI, merge og brukerens nye uttrekk utføres av orkestratoren etter kandidaten.

## Kildebevis og formatvalg

[B8-kildeprøven](../b8/README.md) og [fixturregisteret](../../../tests/fixtures/b8/README.md) bevarer kilder og begrensninger. 40034048/210s uendrede vedtaksutdrag har SHA-256 `2a540261f110b761a0213516c8ad72844d0285744ca0f1cdd4cb1afce06f0850`. Saksrespons 100927 har SHA-256 `2ee25b327b78772523d56317c752e35f5134eef60db9536f6dea3c94ad8fed27`. Tabellen gir `Riksantikvaren` fra kapittelraden `table[1]/tr[2]/td[3]`, `Driftsutgifter, økes med` på post 1 og `Flerårige prosjekter kulturminneforvaltning, kan overføres , reduseres med` på post 22. Ingen navn er hentet fra dagens register.

Formålsfeltene gir hovednavnene **Driftsutgifter** og **Flerårige prosjekter kulturminneforvaltning**. Den valgte, separate stikkordtolkningen gir «Ingen stikkord funnet» og «kan overføres». Råtekst, HTML, kildehash og lokator bevares. Rensingen er avgrenset til et kjent terminalt handlingsuttrykk og kjente stikkord i den eksakte kildeforankrede formålsraden. Ukjent resttekst, kildekonflikt og manglende navn skjules ikke.

Prøvens to rader har 160 243 000 / +5 796 000 / 166 039 000 og 32 185 000 / −3 000 000 / 29 185 000 kroner. Formelt vedtak vises som 210 (2024–2025), mens API-ID 40034048 beholdes i reservefanen. Innst. 81 S og Prop. 16 S er saksmetadata. Flere dokumenter samles uten økt beløpsradantall; samtlige referanser og URL-er beholdes. Vedtak 211s fullmakt forblir separat fulltekst uten beløpshendelse.

De 13 hovedkolonnene er en visning av den frosne rapporten. Ingen av dem endrer gamle JSON-er, rapport-ID-er, observasjoner, B5-avgjørelser eller hovedschema 5. Et generelt nivåbeløp blir ikke tolket som etterbeløp; det oppgis med verdi i Kontrollstatus og beholdes som `nivaa` i Historikkdetaljer. Ulike omfang, komponenter, revisjoner og tolkninger holdes adskilt. Tvetydige samme-rolle-beløp gir tom hovedcelle med forklaring, aldri automatisk sum eller prioritering. Manglende felt er ikke null.

## Utførte kontroller

`tests/test_b9.py` prøver den offentlige kilde → SQLite → frosset JSON → faktisk Excel-grensen og gjenleser filen. En ny offisiell prøve bygges uten historisk grunnlag; et frosset snapshot eksporteres med utilgjengelig database. B6s tidligere historikk sammenlignes felt for felt med den synlige reservefanen, og B8s seks ekstra felt/dokumentlenker kontrolleres. Råobservasjoner og kildetekst sammenlignes med frosset kildegrunnlag. Tidligere `b6-frozen-1`- og B7-standardkontroller inngår i fullsuite.

Merkede syntetiske snapshot-/kildemutasjoner dekker manglende førbeløp, reell null, nivå og ukjent betydning, gjentatte beløpsroller, komponenter, uavklart omfang og alternative tolkninger, manglende/motstridende navn og dato, uavklart stikkordgrunnlag, flere dokumenter, utrygg/motstridende/manglende dokumentmetadata og manglende berikelsesvalg. En tom filtervisning må fortsatt vise ukjent globalt avvik og saksferskhet. Eksisterende B8-prøver kontrollerer også umerket/ukjent stikkord i den nye hovedvisningen.

Kontrollgrunnlagets ferskhet vises separat fra vedtaks- og saksgrunnlagets ferskhet, også når dokumentkilden er gjeldende i den fryste vurderingen. Tidligere detaljerte B8-arbeidsbøker kan fortsatt verifiseres uten omskriving; en egen faktisk Excel-prøve bevarer dette skillet mellom gammel og ny presentasjon.

Den offentlige `verify_saks_excel` gjenleser alle hovedverdier, typedatoer, kroneformat og dokumentlenker, sammenligner alle tidligere detaljfelter/lenker og lange videreføringer, og beholder B8s eksisterende observasjons-/referansekontroller. Hovedtekst gjenbygges i sin helhet før sammenligning. Hoved- og detaljfanene deler kontroll av videreføringsarkenes navn, form, overskrifter, kildecelle, delnummer, rekkefølge og tekst, med skriverens eksisterende oppdeling som grunnlag. Endret hovedlenke, dato som tekst, endringsbeløp eller detalj-ID avvises. En ny prøve viste at lange detaljfelters cellepeker må flyttes når B8s dokumentkolonner settes inn; pekeren beregnes nå fra opprinnelig kolonnenavn før reservefanen omdøpes. Selve råfeltet endres ikke.

Et tidligere levert 210-snapshot med rapport-ID `d0c677cee11fa8d38677c2afa581c5717145524f25323bc1a334c0a5d831b62c` er reeksportert med faktisk offentlig eksport til en egen mellomfil under `work/b9qa`. Den forrige leveransen er ikke overskrevet. [Maskinlesbar kontroll](verification.json) oppgir aktuelle filhasher, ark-/radantall, kontrollverdier, uendrede kildehasher og testresultater. Ingen mellomfil er den bestilte leveransen etter merge.

Den faktiske tidligere leverte B8-filen er også verifisert med den nye offentlige kontrollfunksjonen. Alle 21 opprinnelige ark, 1 225 rektangulære celler og tilhørende dokumentlenker er sammenlignet med B9-filen, med bare Historikk-navnet flyttet til Historikkdetaljer. Verdier og lenker samsvarer. Tidligere frosset JSON er byteidentisk etter reeksport, og både gammel arbeidsbok, JSON, vedtaks-/saksfixtures og den opprinnelige SQLite-prøvebasen har samme hash før og etter QA-kjøringen.

Arbeidsboken er importert med den bundne Artifact Tool-leseren uten tilbakeføring til XLSX og rendret i utsnitt for navn/stikkord/dato, dokumenter/beløp/kontrollstatus, reservefane og fullstendige dokumentreferanser. Kjerneetiketter, tall, lenkeetiketter og stikkord er lesbare. Excel-datoene er faktiske numeriske datoceller med `dd.mm.yyyy`, bekreftet i den lagrede filen og i Artifact Tools importerte stil. Denne versjonen av Artifact Tools PNG-renderer viser likevel datoen som serienummeret 45642; det er en rendererbegrensning og ingen endring til tekst eller oppfunnet dato i arbeidsboken. Tallseparator i PNG følger rendererens språkinnstilling; celleformatet lar Excel vise lokale tusenskiller. Native Excel-app og live dokumenttilgjengelighet er ikke prøvd.

Lange råfelt kan kreve utvidet radhøyde og finnes også i videreføringsark. Hovedvisningen har filter, frosne konto-/overskriftsfelt, Arial og FINs eksisterende mørkeblå profil. Ingen formler eller Excel-feilceller er innført. Kontrollstatus opprettholder at kildebeløp ikke er faglig godkjent, at førbeløp ikke er historisk startgodkjenning, og at saksrelasjonen ikke beviser postvis forslagstilknytning. Ingen årsdekning eller driftssetting erklæres. #10 forblir åpen.

## Reproduksjon

Kjør fra repoet med prosjektets Python-miljø og en kort, ny midlertidig testbane:

```powershell
python -m pytest tests/test_b8.py tests/test_b9.py -q --basetemp ../t9target
python -m pytest -q --basetemp ../t9full
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

Eksporter deretter et eksplisitt B8-utvalg eller gjenlest `b6-frozen-2` med nytt filnavn etter [veiledningen](../../b9-historikk.md). Bevar den faktiske arbeidsboken uendret under ekstern visuell inspeksjon.

Før videreføringsrettingen ga den lokale kandidaten 22. oktober 2026 med Python 3.12.14 følgende resultat: `python -m pytest -q --basetemp ../t9complete` ga **765 beståtte, to hoppet over** på 269,97 sekunder. De to er eksisterende Windows-vertsrettighetsprøver. Målrettet `python -m pytest tests/test_b8.py tests/test_b9.py -q --basetemp ../t9focused` ga **78 beståtte** på 24,68 sekunder. `ruff check .`, `ruff format --check .` (84 filer), `mypy` (48 kildefiler), lokal dokumentlenkekontroll og `git diff --check` bestod. Dette er lokale kontroller av kandidaten på oppgitt base, ikke gjennomført uavhengig review, audit, CI eller merge.

## Rettet gjenlesing av lange hovedfelt

Standards-funnet ble gjenskapt før rettingen på kandidat `8d24e70a101e494b2e0143dbbaf3882c348dd049`: En gyldig syntetisk frosset v2-rapport med kapittelnavn på 37 500 tegn kunne eksporteres og gjenkontrolleres. Etter sletting av hele **Historikk fortsettelse** godkjente den offentlige kontrollen fortsatt filen. Den nye regresjonen feilet med `DID NOT RAISE ValueError`. Kontrollen sammenlignet bare hovedfeltets første 30 000 tegn. Dette var et hull i gjenlesingen før atomisk publisering, ikke tap av tekst i skriveren.

Kontrollen bruker nå skriverens eksisterende 30 000-tegnsoppdeling for forventede videreføringer, gjenbygger hovedfeltet og sammenligner hele teksten med rapporten. Den delte videreføringskontrollen brukes også for Historikkdetaljer og gammel B8-Historikk. Nye syntetiske prøver med 37 500 og 67 500 tegn gjenleser teksten i sin helhet, bevarer frosset JSON og kontrollerer at formelaktig tekst i hovedcelle og hver videreført del fortsatt er tekst. Separate manipulasjoner av arknavn, overskrift, kildecelle, delnummer, rekkefølge, avsluttende tekst, rader, kolonner og celle-/formeltype avvises. Manglende forventede videreføringsark avvises; ekstra videreføringsark avvises også når det ikke finnes lange hovedfelt. Den første prøven for gammel B8 med lange detaljfelt var laget ved omdøping av en ny B9-fil og dokumenterte derfor ikke den opprinnelige skriverens pekerregel. Den er erstattet av prøven nedenfor.

Den tidligere leverte B8-filen og dens frosne JSON er gjenkontrollert med rettingen. Begge har fortsatt de dokumenterte hashene `64f040412d0d9dabc3c4cec366c918bd8c5442ef5e2cb8f474797d247ec398cb` og `2d855c97abf6af30e6eb64817bfc50778f5f7ffb7deee56362ff8caf1e908cbe`. Skriver, gamle identiteter, kilder og frosne resultater er uendret; ingen ny visuell kontroll er nødvendig for denne rene gjenlesingsrettingen.

Lokalt resultat etter rettingen: `python -m pytest tests/test_b8.py tests/test_b9.py -q --basetemp ../t9fixfocused` ga **96 beståtte** på 37,82 sekunder. Fullsuite `python -m pytest -q --basetemp ../t9fixfull` ga **783 beståtte, to hoppet over** på 283,77 sekunder. De to er de eksisterende Windows-vertsrettighetsprøvene. `ruff check .`, `ruff format --check .` (84 filer), `mypy` (48 kildefiler), seks lokale lenker i de to endrede Markdown-filene og `git diff --check` bestod. Maskinlesbar kontroll bevarer resultatet fra før rettingen separat. Dette er lokale kontroller av ucommittede rettinger; ny samlet gjennomgang, sikkerhetsaudit, CI og merge er fortsatt leveringsporter hos orkestratoren.

## Rettet kompatibilitet med opprinnelige B8-videreføringer

Ny uavhengig gjennomgang fant på kandidat `eca8c671418c4b7d3bbc0de6eff2f20866827177` at den strenge detaljkontrollen avviste en gyldig gammel B8-eksport med lange felt. Den opprinnelige B8-skriveren skrev videreføringspekere før dokumentkolonnene ble satt inn: `Historikk!AB2` stod fortsatt i videreføringen, mens `Lokatorer` var flyttet til `Historikk!AH2`. Den tidligere omdøpte B9-prøven hadde allerede korrigerte pekere og fanget ikke denne forskjellen. Påstanden om prøvd opprinnelig B8 med lange detaljfelt i den forrige maskinlesbare kontrollen er derfor korrigert.

[Kompatibilitetsfixturen](../../../tests/fixtures/b9/README.md) er nå produsert av hele, uendrede B8-modulen fra base `a7fc7d9`, lastet i minnet. Både originalens offentlige eksport og originalens kontroll bestod. Feltet `raw_record` er merket syntetisk og bruker `"syntetisk raatekst " * 2500`; full rapport og faktisk XLSX er bevart komprimert, med schema, ID og hash i manifestet. De felles B6-skriverne er kontrollert uendret fra basen. CI leser disse faste filene uten Git, nettverk eller database. Den nye testen feilet før rettingen med `Historikk har feil videreført tekst, del eller cellepeker` (**én feilet, 43 utelatt**, 0,62 sekunder).

Ved gammel detaljvisning bindes nå hver forventet sluttcelle til den eksakte opprinnelige pekeren fra før dokumentkolonnene. Selve teksten kontrolleres fortsatt fra riktig sluttcelle. Den delte kontrollen av ark, overskrift, rader, kolonner, deler, rekkefølge, tekst og celletyper består. Bare gammel B8-visning bruker denne pekerregelen. B9 krever fortsatt de flyttede pekerne i både hoved- og detaljvisning; en B9-detaljpeker endret til gammel B8-konvensjon avvises. Den opprinnelige fixturen verifiseres uten endring av filbyte. Femten separate ødeleggelser av gammel videreføring avvises, inkludert feil peker utenfor den gamle konvensjonen og tekst lagret som formel.

Den tidligere leverte korte B8-filen og dens JSON er også gjenkontrollert uten omskriving og beholder hashene ovenfor. Ingen skriver, opprinnelig leveranse, kilder, faglige bindinger eller frosset kontrakt er endret av denne kompatibilitetsrettingen. Det er ingen endring i den visuelle leveransen; ny rendring er ikke nødvendig for denne gjenlesingsrettingen.

Målrettet `python -m pytest tests/test_b8.py tests/test_b9.py -q --basetemp ../t9legacyfocused` ga **111 beståtte** på 41,82 sekunder. Fullsuite `python -m pytest -q --basetemp ../t9legacyfull` ga **798 beståtte, to hoppet over** på 289,67 sekunder. De to er de eksisterende Windows-vertsrettighetsprøvene. `ruff check .`, `ruff format --check .` (85 filer), `mypy` (48 kildefiler), 13 lokale lenker i tre endrede Markdown-filer og `git diff --check` bestod. Regenerering fra det innsjekkede komprimerte snapshotet ga byteidentisk komprimert JSON og identiske celleverdier i alle ark, med bestått opprinnelig skriver/kontroll. [Maskinlesbar kontroll](verification.json) bevarer også tidligere kontrollresultater. Samlet ny uavhengig gjennomgang, sikkerhetsaudit, CI og merge gjenstår hos orkestratoren.
