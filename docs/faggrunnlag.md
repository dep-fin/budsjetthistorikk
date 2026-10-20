# Faglige funn fra vedleggene

Vedleggene brukes som faggrunnlag for innlesning og analyse. Kildebeskrivelser og eksempler er atskilt fra prosjektets designvalg. Originalfilene er beholdt lokalt og er ikke lastet opp til repoet.

## Leste kilder

| Kilde | Versjon og kontroll |
| --- | --- |
| r_101_2024.pdf | R-101/2024, Statens kontoplan for statsbudsjettet og statsregnskapet, 9. desember 2024. Gjeldende fra 1. januar 2025 ifølge dokumentet. Alle 20 PDF-sider er lest. |
| statlig-budsjettarbeid.docx | Statlig budsjettarbeid, Finansdepartementet, Finansavdelingen, juni 2023. Relevante kapitler og tabeller er lest. |
| 2027_gulbok_datagrunnlag.xlsx | Brukerlevert datagrunnlag for Gul bok 2027. Begge ark og samtlige utfylte datarader er kontrollert. |

### Identifikasjon av filversjon

SHA-256:

- r_101_2024.pdf: 813b9b0f8dc24f2414387cf32bc1ce4ba16a9e42855ccc4c0ed60d96b0592f92
- statlig-budsjettarbeid.docx: 7e52e8191b5a8f2b18f4ce3d9dcdebce1955148746c38b10a33fdce59324e5c7
- 2027_gulbok_datagrunnlag.xlsx: 952757a9964f92a7e2cb1972fcfb6b82b426d4973de641a29fef5ea66d6c1adb

## Kontoplan og klassifikasjon

R-101/2024 side 3 angir utgiftskapitler 0001–2999 og inntektskapitler 3000–5999. Kapitalregnskapets konti 6000–9999 er en annen inndeling og har ikke bevilgningsvedtak. Klassifikasjon skal derfor avgrenses til budsjettkapitlene.

Samme side beskriver departementsserier og +3000 som hovedregler, med særskilte serier blant annet for statsbankene, forvaltningsbedriftene og folketrygden. Side 4 beskriver felles inntektskapitler. Det støtter eksplisitte administrative kapitteloppslag, jf. [departementsregisteret](departementsregister.md).

R-101 side 4–5 deler postene i 01–29, 30–49, 50–89 og 90–99, med forskjellig betydning på inntekts- og utgiftssiden. Finansielle transaksjoner på 90-poster må inngå i dekningskontrollen.

Side 6–7 og 19 omtaler post 24 og underposter. R-101 beskriver vedtak på postnivå, mens 2023-veilederens vedlegg III også beskriver vedtak med underposter. Før parseren fastsettes, må faktiske kildetabeller prøves. Uansett må hierarki, underliggende spesifikasjon og posttotal bevares uten dobbeltelling.

## Budsjettforløpet

Veilederens punkt 2.2.5 beskriver Gul bok som regjeringens samlede formelle forslag og fagproposisjonene som nærmere forklaring og begrunnelse.

Punkt 2.3 og 5.4.2.1 beskriver postvise vedtak under fagbehandlingen og Blå bok som etterfølgende samlet publikasjon. Modellen skal ikke forutsette én avsluttende avstemning over alle bevilgninger.

Punkt 2.4.3 beskriver Meld. St. 2 og en egen proposisjon med bevilgningsendringer i RNB-runden. Punkt 2.4.4 beskriver fagdepartementenes omgrupperinger og FINs nysaldering. Dokumentene kan oppsummere tidligere endringer og ennå ubehandlede forslag. Slike oppsummeringer er ikke nye vedtak.

Punkt 2.5 og 8.2.2.2 beskriver statsregnskapet som en egen kilde med regnskapsført beløp, overføringer og årets bevilgning. Regnskapstall er en egen observasjon. Veilederens punkt 7.3.2.1 presiserer at overskridelsessamtykke ikke forhøyer selve bevilgningen.

## Fullmakter og postomtale

Veilederens punkt 5.5.2.1 beskriver beløpsrammer i bestillings-, tilsagns- og garantifullmakter som andre opplysninger enn årsbevilgning. Punkt 5.4.2.2–5.4.2.3 beskriver betydningen av blant annet «kan overføres», «kan nyttes under» og «overslagsbevilgning».

Prosjektets valg er å bevare fulltekst, stikkord, identitet og struktur i første leveranse. Full strukturering av alle fullmaktsrammer utsettes dersom det vil forsinke bevilgningsinnlesningen. Fullmaktsbeløp skal ikke legges til årsbevilgningen.

## Analyse av 2027-filen

Arket Data har 16 kolonner. Det finnes 1 595 utfylte datarader fordelt på 579 kapitler: 1 177 utgiftsrader og 418 inntektsrader. Arkets lagrede område strekker seg til rad 2443, men siste utfylte datarad er 1596. Tomme formaterte rader skal ikke behandles som poster.

Det ble ikke funnet dupliserte kapittel-/postnøkler eller manglende kapittel, post eller fdep_nr i de utfylte radene. Dette er kontroll av den vedlagte filen, ikke dokumentasjon av fullstendighet mot hele statsbudsjettet.

Beløpene er lagret som heltall uten formler. To beløp er negative: kapittel 2445 post 24 og kapittel 2470 post 24. Fortegn skal ikke brukes til inntekts-/utgiftsklassifikasjon.

Forklaring A17:B17 definerer beløp som bevilgningsforslag. Data L24:P24 og K24 viser kapittel 100 post 1 med beløpet 4 996 819 000, slik brukerens eksempel angir. Dette er observert i forslagsfilen; det er ikke et kontrollert stortingsvedtak. Beløpsenhet skal valideres mot dokumentkilden før en fremtidig forslagsimport godkjennes.

Filen gir derfor en tilgjengelig strukturert kilde til metadata og regjeringsforslag, uten automatisk uthenting fra regjeringen.no. Den skal ikke brukes som fasit for vedtatte bevilgninger, eller som uttømmende katalog over nye poster som kan komme senere i året.
