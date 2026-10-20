# Departementsregister og kapitteltilknytning

Registeret skal kunne vedlikeholdes manuelt. Departementsnummer, navn, forkortelse og kapitteloppslag skal kunne endres med gyldighetsperiode og kildehenvisning. Det skal ikke være nødvendig å endre programkode for en ordinær endring i registeret.

## Brukerens utgangspunkt

Navn og forkortelser nedenfor er oppgitt av brukeren. De ordinære utgiftsseriene gir et utgangspunkt; særkapitler krever egne oppslag.

| Nummer | Navn | Forkortelse | Ordinære utgiftskapitler |
| --- | --- | --- | --- |
| 1 | Utenriksdepartementet | UD | 100–199 |
| 2 | Kunnskapsdepartementet | KD | 200–299 |
| 3 | Kulturdepartementet | KUD | 300–399 |
| 4 | Justis- og beredskapsdepartementet | JD | 400–499 |
| 5 | Kommunal- og distriktsdepartementet | KDD | 500–599 |
| 6 | Arbeids- og inkluderingsdepartementet | AID | 600–699 |
| 7 | Helse- og omsorgsdepartementet | HOD | 700–799 |
| 8 | Barne- og familiedepartementet | BFD | 800–899 |
| 9 | Nærings- og fiskeridepartementet | NFD | 900–999 |
| 11 | Landbruks- og matdepartementet | LMD | 1100–1199 |
| 13 | Samferdselsdepartementet | SD | 1300–1399 |
| 14 | Klima- og miljødepartementet | KLD | 1400–1499 |
| 15 | Digitaliserings- og forvaltningsdepartementet | DFD | 1500–1599 |
| 16 | Finansdepartementet | FIN | 1600–1699 |
| 17 | Forsvarsdepartementet | FD | 1700–1799 |
| 18 | Energidepartementet | ED | 1800–1899 |

Nummer 10 og 12 er ledige i dette oppsettet. Det skal være mulig å opprette eller endre nummer og navn senere.

Kilden bruker navnet «Kultur- og likestillingsdepartementet» for nummer 3. Kildenavnet bevares sammen med brukerens navn og forkortelse; navnevarianter må ikke gi to forskjellige departementer med samme nummer.

## To forskjellige inndelinger

Forklaringsarket i vedlagt Gul bok-fil definerer fdep_nr som departementsnummer og gdep_nr som Gul bok-departement på nivå 1 i vedtaksliste og vedlegg.

I dataarket avviker kodene på 541 av 1 595 utfylte rader. Bruk fdep_nr som kilde til den administrative koblingen, og bevar gdep_nr som egen presentasjonsgruppering. En Gul bok-gruppe er ikke automatisk et departement.

Kilden har også fdep_nr 23 «Ymse». Dette skal bevares som en særkategori med kildekode, ikke opprettes som et nytt ordinært departement.

## Eksempler på eksplisitte oppslag

Verdiene er kontrollert i vedlagt 2027-fil. Excel-rad viser raden i arket Data.

| Kapittel | Administrativ kildekode | Gul bok-gruppe | Excel-rad |
| --- | --- | --- | --- |
| 1 | 15 DFD | 91 Det kongelige hus | 2 |
| 41 | 16 FIN | 93 Stortinget og eksterne organer | 8 |
| 2309 | 23 Ymse | 23 Ymse | 1077 |
| 2410 | 2 KD | 24 Statsbankene | 1078 |
| 2445 | 15 DFD | 26 Statens forvaltningsbedrifter | 1106 |
| 2650 | 6 AID | 27 Folketrygden | 1129 |
| 5309 | 23 Ymse | 60 Inntekter under departementene | 1453 |
| 5501 | 16 FIN | 30 Skatter og avgifter | 1478 |
| 5700 | 16 FIN | 57 Folketrygden | 1584 |

Inntektskapittel er som hovedregel utgiftskapittel +3000. Dette gir ikke en sikker administrativ kobling for særserier. Kapittel 5531 er for eksempel registrert under FIN, mens kapittel 2531 er registrert under BFD. Dette er to forskjellige kapitler; mekanisk fratrekk av 3000 ville gitt feil departement.

## Krav til vedlikehold

- Kildens opprinnelige koder og navn skal kunne etterprøves.
- Manuelle endringer skal ha gyldighetsperiode og sporbar begrunnelse.
- En oppdatert katalog skal ikke omskrive historisk tilknytning.
- Nye kapitler og poster skal kunne opprettes. Manglende oppslag sendes til kontroll uten at kildedata slettes.
- Eksplisitt kapittelkobling har forrang fremfor intervall- og offsetforslag.
- En 2027-katalog er ikke alene et autoritativt register for alle 2026-vedtak eller fremtidige år.

Første leveranse bruker manuelt redigerbare Excel-/CSV-filer som arbeidsflate for registervedlikehold. Import av endringer skal valideres og være sporbar. Et eget administrasjonsgrensesnitt kommer eventuelt senere.

## Avgrenset B4-grunnlag

B4 bruker bare de ni eksplisitte oppslagene ovenfor, med gyldighet **2027–2027**, i en immutable datatabell med versjon og deterministisk innholdshash. Tolkningsidentiteten bevarer registersnapshotet. Kildeartefaktens SHA-256 er `952757a9964f92a7e2cb1972fcfb6b82b426d4973de641a29fef5ea66d6c1adb`, jf. faggrunnlagets tidligere filkontroll. Originalfilen ble ikke gjenfunnet ved B4-implementeringen; dette er bruk av tidligere kildebelagte oppslag, uten nye påstander om cellekontroll eller filens øvrige kapitler. Intervaller og +3000 brukes ikke som bekreftede koblinger. Registervedlikehold/import og brukerens endringer følger B5.
