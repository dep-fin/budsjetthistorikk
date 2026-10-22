# Faglig kontrollmatrise 2024, versjon 1

Utført 22. oktober 2026 for [#26](https://github.com/depmartin/budsjetthistorikk/issues/26), etter P13-P1/#24 på `6b19a5c`. [Den maskinlesbare matrisen](control-matrix-2024-v1.json) har identitet `p13-p2-2024-1`. Den binder originalhash, P1-uttrekk, fire bevisfiler og konkrete JSON-/kildelokatorer. [Kontrollkvitteringen](verification.json) angir matrisehash og faktisk utførte prøver.

Matrisen kan brukes til de uttrykkelig avgrensede kilde- og matematikkontrollene nedenfor. Den er et selvstendig dokument ved siden av de lagrede observasjonene. Den aktiverer ingen tolkning, faglig godkjenning eller årsdekning. En faglig godkjenner er ikke oppgitt, fordi ingen slik avgjørelse er tatt. #13, #10 og #1 er fortsatt åpne; #26 kan lukkes etter orkestratorens review, CI og bekreftede merge.

## Tillatt bruk per kolonne

| Kolonne | Verifisert kilde-/kontrollomfang | Grense for bruk |
| --- | --- | --- |
| G | G2 på 1/1 mot faktisk Gul bok-forslag | Ett forslagsnivå med rå presisjonsrest; ingen generell G-godkjenning |
| H | Alle 1 871 celler og unionens 1 694 nøkler. Faktoren 1 000 000 er validert for 1 573 felles kontrollaggregater | 726 råpresisjonsspor beholdes. Separat heltallsforslag treffer 1 573/1 573; generell normalisering og hierarki er åpne |
| I | I70 på 151/70 mot originalt RNB-forslag −20 mill. kroner | Forslag holdes adskilt fra K og dokument-D |
| J | Nivåankeret 2541/70 og full rå `J−H−K` | 1 654 eksakte og 217 ikke-null rester; nivået blir ingen ekstra endringshendelse |
| K | Vårregisterets 613 kontoer: 501 eksakte og 112 råpresisjonsrester | Dokumentutvalg inklusive RNB; K og I er forskjellige på 71 rader |
| L | Alle fire ikke-null celler har konkrete kildeankre | Dokumentavgrenset gruppe; p34 og p36 er begge datert 29. november, så en generell dato før nysaldering er ugyldig |
| M | Alle 1 871 celler er fysisk numerisk 0. Faktisk lønnskilde er Prop. 36 S kapittel 5/vedlegg 4 | Offentlig lønnsfordeling har 165 positive rader og negativ reserve 2309/1. Fortegnssum 0 beviser ingen null lønn eller M-enhet |
| N | Alle 737 ikke-null postkandidater inngår i samtidig offentlig register; tre originale forslagsankre | 738 felles kontrollkontoer inkluderer nullsummen på 2470/24. 509 eksakte + 229 råpresisjonsrester. Alle departementenes originalforslag er ikke individuelt avstemt |
| Dokument-D | Unionen gir 1 354 eksakte kontrollaggregater og fem navngitte rester; tolv offentlige v2-fixtures gir fortsatt 2 894 observasjoner | Kildekontroll, avledet komponentdifferanse, ny adapterforventning og godkjent additiv kjede har separate roller |

Matrisens `subscopes` presiserer blant annet Hs enkeltrader, kontrollaggregater, fysisk null, fravær og post 24, samt dokument-Ds post-/komponentomfang. Tillatte kontroller er ikke avhengige av en generell eiergodkjenning av hele kolonnen. Eventuell videre analysebruk og aktivering av normalisering krever egne, sporbare beslutninger innen berørte omfang.

## Kildebevis, forslag og åpne spørsmål

`VERIFIED_RAW_SOURCE` gjelder den faktisk observerte råverdien. `VERIFIED_SOURCE_CORRESPONDENCE` gjelder det beskrevne samsvaret eller kildefraværet. `CONTROL_HYPOTHESIS` er en uttrykkelig utledning om kolonne-/periode-/aggregatomfang. `PROPOSED_NORMALIZATION` er et forslag uten virkning på tidligere data. `OPEN_QUESTION` angir den konkrete grensen som består. `professional_approval=OPEN` er en egen akse og opphever ikke verifiserte kildefunn.

[Presisjonsrapporten](precision.md) måler alle 726 H-nøkkelrester: 388 negative og 338 positive, absolutt fra `1E-13` til `0.00002` kroner. På cellenivå er det 787 spor; fire oppheves i to eksakte aggregater. Alle 787 er binært kompatible med en referanseuavhengig heltallskandidat delt på 1 000 000. Den frosne regelen bruker heltall i NOK, Decimal `ROUND_HALF_EVEN`, binær likhet og en lokal ULP-grense med bredde under en halv krone. Den gjør ingen skjult tusenavrunding eller referanseavhengig tilpasning. Alle 1 871 numeriske vilkår består; alle 1 573 felles aggregater treffer etter kandidatregelen. Dette er ingen blind holdout-prøve eller aktivert regel.

De 120 H-nullrestene består av 64 offisielle kontoflyttinger, ett uttrykkelig nullomfang på 1530/30 og 55 kontoer med ukjent fraværsårsak. De 55 fordeler seg på 39 poster i eksisterende kapitler og 16 fraværende kapitler. Ingen blir konstruert nullbevilgning. 5999/90 har 101 874 353 000 kroner i Blå bok, men mangler i Excel. Alle 178 to-rads H-nøkler har kode 1/2; 170 er felles med referansen. Dette tillater merkede kontrollsummer, uten å godkjenne en universell komponentrelasjon. Enkeltstående kodede rader og post-24-totaler har egne begrensninger.

[Vedtakskontrollen](decisions.md) forklarer dokument-Ds fem rester mot originaltekster. D43=0 på 151/70 er en dokumentert markering av uendret resultat uten ny nullhendelse. 5999/90 mangler på to dokumentgrupper og har en publisert før-/etterkonflikt. Havtil-overgangene finnes under to formelle vedtaks-ID-er; Excel har bare i99 og mangler i93. Ingen konkret uttaksrettelse er funnet. De tre formelle kjedekonfliktene består. Adaptergrensene på 228/85 og 2440/31 har kildebelagte fremtidige forventninger om henholdsvis +30 mill. og +11,9 mrd. kroner som delta, uten oppdiktet før-/etterfelt eller nullstart. V2 endres ikke.

[Stadiekontrollen](stages.md) skiller nullkolonnen M fra faktisk lønnskompensasjon, som på 20/1 er inkludert i N. Den kildebelegger N og J/K/Ls avgrensede dokumentomfang. Den etterfølgende [seksrestkontrollen](stage-residuals.json) forklarer alle seks rester på minst én krone som forslag mot vedtak: komitétillegg på 5, 215, 270, 10 og 100 mill. kroner, samlet 600 mill. kroner, med tilsvarende økning på 5800/50. Der beholdes dessuten rå presisjonsrest på `−0.0000005` kroner. Énkronegrensen beskriver et stratum og er ingen aksepttoleranse.

De 726 talltekniske H-restene, 55 uavklarte kontoårsaker, tre formelle kjedekonflikter og seks kildebelagte forslag/vedtak-forskjeller kan ikke summeres til ett antall «økonomiske feil».

## Lesing og reproduksjon

Velg filversjonen uttrykkelig fra repoets rot:

```powershell
python -m analyse.control_matrix docs/research/historisk-excel/p13-p2/control-matrix-2024-v1.json
python -m pytest tests/test_control_matrix.py tests/test_historical_controls.py -q
```

`read_control_matrix(path, expected_sha256=...)` kan også binde matrisens byte til hashen i kontrollkvitteringen. Leseren kontrollerer år, ni kolonner, kildefaktor, betydning, talltype, stadium, separate statuser og presisjonsgrunnlag. Den verifiserer alle fire bevisfilenes SHA-256/størrelse og hver JSON-peker. CLI skriver bare resultat til standard ut. Ukjent fremtidig versjon avvises; ingen «gjeldende» versjon velges automatisk. Endret kildegrunnlag eller betydning skal få en ny matriseversjon; eldre versjoner og tolkninger beholdes uendret.

CLI skriver SHA-256 for nøyaktig de matrisebytene som er lest innen bytegrensen, dekodet og validert. En senere endring eller sletting av filbanen endrer ikke dette kontrollresultatet. En forventet hash sammenlignes med den samme bytehashen.

G/I-originalbevis valideres også uten forventet matrisehash. Kilde, referanse, lokator og avstemmingsomfang har lukkede feltsett og eksplisitte typer. Kildens hash og kanoniske URL, konto, celle, beløp og HTML-lokator bindes til de to dokumenterte originalfeltene i v1. Referansens eget år, NOK-faktor 1, talltype, betydning, stadium og postnivå må samsvare. De eksisterende interne kontrollpekerne betegner kontrollens eneste validerte `references/0`-blad og kan bare brukes i tilhørende G-/I-rad og omfang. Manglende bevis erstattes ikke. Matrisens og bevisfilenes opprinnelige byte, identitet og faglige betydning er uendret.

Før noen bevisfil åpnes, kreves nøyaktig de fire tillatte filnavnene uten duplikater, med gyldig metadata og størrelse. Hver fil leses høyst til oppgitt byteantall pluss ett kontrollbyte. Samlet lesebudsjett for de fire filene er 2 MiB, inkludert kontrollbytene; hver fil har samme øvre lesegrense. Selve matrisen har en separat grense på 2 MiB pluss ett kontrollbyte. Overskridelse avvises også hvis filen vokser etter metadatakontrollen.

CI bruker bare den offentlige matrisen, begrensede bevis, syntetiske prøver og tidligere publiserte autentiske fixtures. Prøvene dekker blant annet feil år/enhet/betydning/status, ufullstendig presisjon, bevistampering, fremtidig versjon, meningsfulle tallankre, v2-grenser og ny innlesning med fraværende/korrupt matrise. De krever verken nett, råoriginal eller tidligere pilotpakke.

Full lokal kildekontroll krever den bundne originalen, P1s hashfestede pakke, de tidligere forskningsreferansene og lokale originale responsbyte. Rådata og komplette ledgere forblir lokale. Eksakte algoritmer, skriptnavn/-hasher, kilde-URL-er, lokatorer og begrensninger står i [H-rapporten](precision.md#nye-kildebyte-og-reproduksjon), [vedtaksrapporten](decisions.md#reproduksjon-bevis-og-begrensninger) og [stadierapporten](stages.md#kilderevisjon-reproduksjon-og-videre-ansvar). Integrasjonskjøringen og lokale fullkontroller dokumenteres i kontrollkvitteringen. Den numeriske H-regelen kan reproduseres med den separate `proposed_h2024_integer`-funksjonen; den får ingen referansebeløp som input og brukes ikke i noen adapter.

Kildehashene gjelder faktisk mottatte byte. Opprinnelige HTTP-/PDF-kilder og avledede JSON-/CSV-beløpsreferanser har forskjellige roller. Der vedtakssporet bare fikk nettlesing/HTTP 403, er manglende råhash uttrykkelig oppgitt; stadiesporet har egne vellykkede råhentinger av enkelte samme proposisjoner. Ingen hash fra en annen responsversjon flyttes over. Full fersk v2-sesjonsreplay er ikke utført: to ferske sesjonssvar er brukt til kildefelt-/objektlikhet, og bare det avgrensede fixtureutvalget er kjørt gjennom v2.

Nye offisielle observasjoner har ingen importavhengighet til matrisen, historisk Excel, historisk organisasjonsregister eller startsaldo. Normalisert/kontrollert NOK i de tidligere historiske pakkene er uendret. Ingen ny råoriginal, komplett celleinventar, HTTP-snapshot eller intern metadatafilsti publiseres.
