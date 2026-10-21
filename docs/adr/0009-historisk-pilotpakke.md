# ADR 0009: separat historisk adapter og kontrollpakke

Valgt for den autoriserte 2024-piloten i #24 under #13, 21. oktober 2026. [Pilotplanen](../pilotplan-historisk-excel.md) fastsetter hele kilde–lagring–eksport–sammenligning-løpet. Åpne faglige tolkninger skal kunne bevares uten godkjent kroneverdi.

## Valg og alternativer

`historisk-excel-2024-v1` leser rå OOXML gjennom en egen adapter. Å lese numeriske verdier gjennom vanlige flyttall ville skjult presisjonsspor, blant annet `Rådata!H2=14.768000000000001`. Å endre Storting-v1/v2 eller bruke B5-aktivering ville bundet historiske kildefelt til feil kildetype og registerkrav. Ingen av disse alternativene er valgt.

Etter nødvendige review-/auditrettinger 21. oktober 2026 fikk v2 rettede navn, eksplisitt formeltilstedeværelse, samlede ressursgrenser og bundne kontrollhypoteser. Nye importer velger nå `historisk-excel-2024-v3` og celleinventar v3: sperren gjelder også celler dekket av et eksplisitt array/shared/dataTable-resultatområde uten eget `<f>`. Dette endrer kandidatinnhold for slike kilder og får derfor ny tolkningsidentitet. Sammenligningsgrunnlag v2 videreføres. V1-/v2-uttrekk, ID-er, JSON og tidligere fullpakker bevares og leses uendret; uferdige eldre forsøk må erstattes av nye v3-forsøk. Det generiske observasjon-1-formatet, B1–B7-standarder og Storting-v1/v2 endres ikke.

Adapteren bruker eksisterende `Artifact`, `SourcePointer`, `AmountObservation`, `Extraction` og samme atomiske lagringsvalidering. Den interne funksjonen `save_extraction_in` gjør det mulig å lagre uttrekk, inventar, kandidater, regler og bindinger i én transaksjon. Den offentlige `save_extraction` beholder signatur, JSON, ID-er og kollisjonskontroll. Nye historiske observasjoner har datasett `historisk` og kildesystem `historisk-excel` uten HTTP-status, API-ID, oppfunnet vedtaksdato eller hendelsesidentitet.

Et særskilt problem i observasjon-1 er den matematiske kronekandidaten. Feltet `amount_kr` betyr normalisert heltall; en eksakt desimalkandidat med uavklart enhet/presisjon kan ikke legges der. Derfor legges `historisk-kandidat-1` til som en versjonert ledsager med observasjons-ID, celle-ID, Decimal-streng, prøvd faktor og separate nullfelter for normalisert/kontrollert verdi. Originalmodellen og gamle JSON-identiteter endres ikke. Alle pilotens normaliserte og kontrollerte verdier er null. Treff i en kontroll opphever ikke dette.

## Identitet, lagring og forsøk

Arbeidsbokhashen er både kildeenhet og kilderevisjon i denne piloten. Observasjons-ID bruker eksisterende identitetsregel med hash, arknavn, celle, beløpskolonne og tolkning. Filnavn, lokal filflytting, nye importtidspunkter og eksportsti endrer ikke beløpsidentitet. Ny fil eller begrunnet tolkning gir nytt uttrekk. En uttrykkelig forgjenger kan angis; radflytting er ingen automatisk hendelseskobling.

Pilottabellene er additive innen kjent SQLite-schema 5 og har egen lagringsversjon `historisk-pilot-1`. Gamle skrivere bevarer schema 5 og de nye tabellene. Ukjent fremtidig hoved- eller pilotversjon avvises. Et nytt forsøk lagres før lesing, med `startet`, `feilet` eller `lagret`. Mottatte byte innen grensen bevares også når arbeidsboken avvises. Uten mottatt full fil finnes ingen oppfunnet fullfilhash. Publisering av kontrollpakken registreres separat.

Originalens byte og det første importgrunnlaget gjenbrukes ved gjentakelse. En ny innlesning må gi samme immutable resultat under samme tolkning. Eksplisitt staging gir forsøks-ID før tolkning; gjenopptak trenger bare SQLite.

## Pakke og analyse

`historisk-pakke-1` er typet UTF-8-JSONL med manifest og faktisk Excel. Decimal er tekst med type og faktor, heltall/null beholder typer. Celleinventar, kandidater, kolonneregler og metadata bindes med hash i artefaktmetadata. Originalen blir liggende i SQLite; pakken identifiserer den med hash og byteantall. Filnavn/hash/størrelse/antall, adapter/tolkning, uttrekk, import, forgjenger, kontrollgrunnlag og nullgrunn for historisk register følger eksporten.

`historisk-sammenligning-1` fryser uavhengige referanser før sammenligning. Hele nøkkelunionen bevares, inklusive manglende rad og observert null. Underposter kan prøves som et uttrykkelig kontrollaggregat uten å bli godkjent hierarki. Beregnede komponentdifferanser er separate kontrollverdier med begge innganger. Forslag og vedtak kan ikke brukes som samme talltype. Ingen kontroll oppretter nye vedtaksdeltaer.

Eksport leser eksplisitte lagrede ID-er og henter ingen kilder. Alle JSONL-filer og faktiske Excel-celler, ID-er og videreføringsdeler kontrolleres mot SQLite før en unik midlertidig katalog gis det nye pakkenavnet. Eksisterende filer eller pakker erstattes ikke. Etter tapt publiseringskvittering verifiseres den allerede synlige pakken før den gjenbrukes.

## Konsekvenser

Full lokal kildebevaring og teknisk kontroll kan leveres med åpne enheter, stadier, hierarki og historisk organisasjon. Godkjenning av enkeltverdier, kjeder og årsdekning er fortsatt egne beslutninger. Kjedekonfliktene 1860/1, 4860/1 og 5999/90 består. Nye offisielle observasjoner har ingen avhengighet til pilottabeller eller Excel. #13 gjelder fortsatt øvrige år, og #10s faktiske driftsaksept gjenstår.

Fullstendig inventar, kandidater, kontrollpakke og original behandles lokalt. Delingsgrunnlaget for ny offentlig kopiering av den historiske originalen er uavklart. Bare kode, syntetiske prøver, begrensede offentlige kontrollreferanser og en aggregert kontrollrapport følger endringen.
