# B5: register og kontrollfiler

Kommandoene kjøres med `python -m innlesning.maintenance --database budsjett.sqlite <kommando>`. `--help` viser alle argumenter. Ingen kommando henter nett, godkjenner automatisk eller endrer gamle råobservasjoner. En import returnerer JSON med varig `id`, `new_ids`, `reused_ids`, `errors` og eventuelt `snapshot_id`. Feil har ark, fysisk rad og felt. Returkode 0 betyr vellykket operasjon, 1 betyr bevart import med valideringsfeil og 2 betyr feil før operasjonen kunne fullføres.

## Vedlikehold registeret

1. Kjør `register-seed` én gang. Svaret gir startgrunnlagets `snapshot_id`. `register-head` leser gjeldende publiserte snapshot senere; `register-read --snapshot <ID>` leser et historisk snapshot.
2. Kjør `register-export --snapshot <ID> --output register.xlsx`, eller velg `.csv`.
3. Rediger den eksporterte filen. Behold kolonnenavnene og grunnlagsraden. Hele filen er neste komplette kandidat, ikke en liste med delvise oppdateringer.
4. Kjør `register-import --input register.xlsx`. Rett eventuelle feil og importer igjen. Etter en annen gyldig publisering må en ny arbeidsfil eksporteres fra gjeldende base.

Excel har ett ark `Register`. CSV har samme kolonner og radtyper, semikolon, UTF-8 og valgfri BOM. CSV-eksport beskytter tekst som Excel ellers kunne tolket som formler med en innledende apostrof; importen fjerner bare denne beskyttelsen. XLSX-tekst er reelle tekstceller, og beløpskorreksjoner skal skrives som heltall eller desimal heltallstekst, aldri som formler.

Kolonnene er `radtype`, `eksport_id`, `forventet_base`, `nummer`, `navn`, `forkortelse`, `kildenavn`, `kategori`, `kapittel`, `fdep`, `gdep`, `gruppenavn`, `post`, `fra_ar`, `til_ar`, `presisjon`, `kilde`, `referanse`, `begrunnelse`.

- `grunnlag`: Første datarad. Eksport-ID og forventet base kopieres uendret fra eksporten.
- `departement`: Nummer, brukerens navn og forkortelse, separat kildenavn og kategori `ordinær` eller `særkategori`. Kode 23 er særkategori. Nummer 10 og 12 er ledige i starten, men kan tildeles med periode og proveniens. KUDs navnevariant er ett departement med ett nummer. En forkortelse trenger ikke være unik på tvers av tidsperioder.
- `kapittel`: Eksakt kapittel, administrativ kode `fdep`, separat `gdep` og gruppenavn. Når grupperingen er uavklart, la `gdep` stå tom og skriv `uavklart` i `gruppenavn`. Ingen intervaller eller +3000 godkjenner en kobling. Departementet må dekke hele koblingsperioden.
- `post`: Eksakt kapittel/post med periode og kildebevis. Denne katalogen er adskilt fra departementstilknytningen. En kapittelkobling alene godkjenner ikke post 32 i kapittel 900.

Alle faglige rader krever `fra_ar`, `til_ar`, `presisjon=år`, kilde, referanse og begrunnelse. Gyldighet er inklusiv og kan ikke overlappe for samme departementsnummer, kapittel eller kapittel/post. Et startregister kan eksporteres og importeres uendret; innholdet gjenbrukes. Endret radrekkefølge, filnavn og importtid gir ingen ny snapshot-ID. Tidligere snapshots og resultater beholdes.

For 900/32 må både departementets 2025-periode, eksplisitt administrativ kapittelkobling og katalogposten oppgis kildebegrunnet for 2025. Startgrunnlagets 2027-poster kan ikke brukes som 2025-bevis. Vedtak 40034443 dokumenterer +454 000 000 kroner og ny post, men oppretter ingen inngående nullbevilgning.

## Tolk og velg kontrollgrunnlag

```powershell
python -m innlesning.maintenance --database budsjett.sqlite reinterpret --revision <B2-revisjon> --register <snapshot-ID>
python -m innlesning.maintenance --database budsjett.sqlite basis-define --description "Kildeavstemming av valgt uttrekk og avgrenset bruk"
python -m innlesning.maintenance --database budsjett.sqlite basis-activate --extraction <uttrekks-ID> --register <snapshot-ID> --control <kontrollgrunnlag-ID>
```

Ny tolkning returnerer ny uttrekks-ID og bevarer den gamle. `basis-activate` er en uttrykkelig administrativ overgang som velger uttrekk/tolkning, register og kontrollgrunnlag per kildeenhet. Flere ulike kildeenheter kan oppgis med gjentatt `--extraction`. Registerimport alene aktiverer ikke et nytt analysegrunnlag. Historisk lesing, alternativ tolkning og eksport aktiverer heller ingenting. Ny aktivering gjør tidligere berørte vurderinger utdaterte, også etter A → B → A. Kildeendring bruker i tillegg B2s overgangsteller.

## Bevar beviset og behandle kontrollfilen

```powershell
python -m innlesning.maintenance --database budsjett.sqlite evidence-add --input referat.xml --version refs-202526-03-26 --locator "<presis lokator i denne filen>" --url "https://data.stortinget.no/eksport/publikasjon?publikasjonid=refs-202526-03-26"
python -m innlesning.maintenance --database budsjett.sqlite control-export --extraction <uttrekks-ID> --register <snapshot-ID> --control <kontrollgrunnlag-ID> --output kontroll.xlsx
python -m innlesning.maintenance --database budsjett.sqlite control-import --input kontroll.xlsx
```

`evidence-add` lagrer faktiske lokale filbyte, hash, versjon, lokator, URL og rolle `kontrollkilde`. For et avledet utdrag brukes `--parent-sha256 <originalens hash>` i tillegg. Utdraget får alltid sin egen hash. Velg eksakt lokator i filen som faktisk legges inn. `evidence-read --id <ID>` viser bevisets metadata. Funksjonen verifiserer ikke at kontrollørens faglige vurdering er riktig.

Kontrollfilens ark heter `Kontroll`; `.csv` gir samme kolonner/validator. `--observation <observasjons-ID>` kan gjentas for å avgrense kontrollarbeidet. Hver eksportert observasjon skal beholdes nøyaktig én gang. Alle kilde-, revisjons-, tolknings-, register-, overgangs- og forgjengerfelt, råverdi, status og avvik kontrolleres mot en bevart eksport i databasen. År/kapittel/post er beskrivende felt, aldri en tilstrekkelig identitet. Beløpsfeltet følger lokatoren også når før- og etterbeløpet kommer fra samme fysiske celle.

Bare disse feltene fylles ut:

| Felt | Innhold |
| --- | --- |
| `status` | Tomt betyr ingen ny avgjørelse. Ellers `til_kontroll`, `godkjent` eller `avvist`. |
| `godkjente_felter` | Ved godkjenning: kommaseparert `amount_kr`, `organization` og/eller `catalogue`. Metadata må finnes i valgt register og ha gyldighet for året. |
| `godkjent_bruk` | Ved godkjenning: `analysebelop`, `kjedegrunnlag` eller `metadata`. |
| `korrigert_belop_kr` | Valgfri separat godkjent heltallsverdi i kroner. Ukjent råbeløp krever en eksplisitt verdi for å kunne godkjenne `amount_kr`. Originalen beholdes. |
| `begrunnelse` | Påkrevd for enhver ny avgjørelse. |
| `kontrollor` | Navnet på den som tar avgjørelsen, påkrevd. Ingen automatisk autentisering. |
| `bevis_id` | ID fra `evidence-add`; påkrevd ved godkjenning. Metadata binder artefakt, versjon, hash, lokator og rolle. |

Avvist/til kontroll har ingen godkjent bruk eller korreksjonsvirkning. En ugyldig rad avviser hele importen. Feil og råfil bevares. `import-read --id <import-ID>` viser diagnostikken igjen. En fil eksportert før en nyere avgjørelse kan ikke overskrive den. Identisk filreplay returnerer opprinnelig resultat uten å reaktivere gamle avgjørelser. Etter ny kilde, aktivering eller nyere avgjørelse må berørte rader eksporteres og vurderes på nytt.

For vedtak 599, 5538/70, skal bare observasjonen `etter_belop` med råtekst `I 615 833` få eventuell korreksjon 1 615 833 000. Referatets fulle tall er kontrollbevis; differansen mellom førbeløp og endring er støtte, ikke erstatning. Det finnes ingen generell I→1-regel eller automatisk nullpåfylling. Representasjonsavviket beholdes. Andre observasjoner påvirkes ikke.

## Ny behandling og rapport

```powershell
python -m innlesning.maintenance --database budsjett.sqlite control-read --id <avgjørelses-ID>
python -m innlesning.maintenance --database budsjett.sqlite control-report --extraction <uttrekks-ID>
python -m innlesning.maintenance --database budsjett.sqlite reprocess --extraction <uttrekks-ID> --register <snapshot-ID> --control <kontrollgrunnlag-ID> --output godkjente-belop.xlsx
python -m innlesning.maintenance --database budsjett.sqlite controlled-read --id <resultat-ID>
python -m innlesning.maintenance --database budsjett.sqlite controlled-export --id <resultat-ID> --output godkjente-belop-igjen.xlsx
```

Resultatet lagrer råobservasjons-ID-er og de faktisk anvendte avgjørelsene. Godkjent effektiv verdi vises adskilt fra råverdien og fra en historisk verdi som senere har blitt utdatert. Rapporten viser ferskhet, godkjent bruk, begrunnelse, bevis og gjenstående avvik. Siste kildeforsøksstatus vises selv når ingen faglig avgjørelse finnes. Ventende/feilet forsøk, fravær eller et siste kildeforsøk som bare omfattet et annet vedtak, gir ikke vurderbart grunnlag når innholdet ellers er gjeldende. Ingen eldre godkjenning tas i bruk som reserve etter en nyere avvisning eller ny markering til kontroll.

For et avgrenset kjedeutvalg kan `reprocess` i tillegg få `--selection utvalg.json` med samme `HistorySelection`-format som B3. Database, utvalgsfil og utfil må ha forskjellige normaliserte baner. `reprocess --output` og `controlled-export --output` krever `.xlsx`; bane og utformat kontrolleres før behandling eller eksport. En slik kommandofeil gir returkode 2 og bevarer utvalgsfil og tidligere resultat. Valgte uttrekks-ID-er må stemme eksakt. Eksisterende teknisk kjedekontroll må bestå, og alle aktuelle beløp må ha gjeldende godkjenning for `kjedegrunnlag` og kjent organisasjon/katalog. Manuelle korreksjoner vises som egne godkjente enkeltbeløp og skriver ikke om den eksisterende råkjeden. En ny post får ingen nullstart. Havtil-/5999-konflikter, manglende start og ufullstendig kjede forblir sperret. Det lages ingen sum på tvers av før-/endrings-/etterbeløp. Resultatet erklærer ingen årsdekning.

Arbeidsfiler over 8 MiB avvises før innlesning og får varig feilmelding, uten lagret råfil eller påstått filhash. Innleste filer, også ugyldige, bevares ellers med faktiske byte. Filgrensen tillater høyst 10 000 datarader, 30 000 tegn per celle, 128 XLSX ZIP-medlemmer og 64 MiB deklarert utpakket innhold. XLSX-arket kontrolleres dessuten løpende i blokker på høyst 64 KiB før celleverdiene leses med begrenset strømlesing. Faktiske rad- og cellekoordinater bestemmer grensene: høyst 10 001 fysiske rader med overskriften, formatets kolonneantall og tilsvarende antall celler. Uordnede eller gjentatte koordinater avvises. Arket kan ikke overskride 64 MiB ved strømlesing. Manglende, for liten eller for stor deklarert arkdimensjon skjuler ingen celler og er ikke alene en importfeil. En feil i faktisk innhold avviser hele importen med bevarte råbyte og diagnostikk. Formler evalueres ikke. Eksport er atomisk og kan ikke overskrive database eller bevarte import-/kildefiler; bruk nytt filnavn etter en import. Dette er ikke en historisk Excel-adapter.
