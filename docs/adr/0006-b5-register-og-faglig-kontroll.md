# ADR 0006: Innholdsbestemt register og append-only faglige avgjørelser

Valgt for B5/#8, 21. oktober 2026. Excel og CSV er saksbehandlerens arbeidsflate. B1–B4 har allerede immutable resultater og identiteter. Å skrive en korreksjon inn i samme observasjon, utvide B2s kontrollhenvisning med en skjult beløpsvirkning eller behandle B3s `approved_balance` som faglig godkjenning ville brutt den leverte kontrakten.

## Register og filformat

Et komplett register består av tidsavgrensede departementer, eksplisitte kapittelkoblinger og en egen kapittel/post-katalog. Snapshot-ID bygger på faglig innhold, gyldighet og proveniens i sortert form. Filnavn, importtid, radrekkefølge og eksport-ID inngår ikke. En import starter fra et lagret eksportgrunnlag og sammenligner forventet base med gjeldende register i samme skrivetransaksjon. Samtlige rader valideres før et nytt snapshot publiseres. Identisk faglig innhold gjenbrukes. Eldre snapshots og tolkninger beholdes.

Begge arbeidsformater har de samme navngitte kolonnene og den samme radvalidatoren. Registeret har ett ark `Register`, med radtype `grunnlag`, `departement`, `kapittel` eller `post`; CSV har tilsvarende rader, UTF-8 og semikolon. Dette er valgt fremfor ulike importregler for flere Excel-ark. Det gir en enkel, dokumentert filgrense som kan kontrolleres likt i begge formater. Kontrollfilen har ett ark `Kontroll`, én rad per uttrykkelig valgt beløpsobservasjon.

Startgrunnlaget er brukerens 16 ordinære departementer og særkategori 23, samt de ni dokumenterte 2027-koblingene. Det inneholder ingen bekreftede katalogposter. 2027-koblinger tilbakeprojiseres aldri. B4s innebygde snapshot og standardvalg består uendret. Den samme v2-parseren kan bruke et uttrykkelig lagret snapshot fordi registeret inngår i tolknings-ID-en. `Organization` og gamle v1-feltgrupper får ingen nye standardfelt.

## Kontroll og aktivering

En faglig avgjørelse bevares med egen ID, tid, forgjenger, kontrollør, begrunnelse, godkjente felter/bruk, bevis og eksakt kilde-/tolknings-/registergrunnlag. Korreksjon av normalisert kroneverdi har et eget felt. Den opprinnelige observasjonen, råteksten og struktureringen endres aldri. Bevisfilene lagres med sine faktiske byte, egen hash, versjon, lokator og rolle. Et avledet utdrag har egen hash og separat foreldrehenvisning.

Et aktivt grunnlag velges uttrykkelig per datasett, kildesystem og kildeenhet. Hver endring av valgt uttrekk/tolkning, register eller kontrollgrunnlag får neste aktiveringsovergang. A → B → A kan derfor aldri aktivere første As avgjørelser igjen. B2s egen innholdsovergang håndhever tilsvarende vern ved kildeendring. Alternativ tolkning, historisk lesing og eksport aktiverer ingenting. Et register kan publiseres før det tas i bruk; berørte kontroller blir utdaterte ved den uttrykkelige aktiveringen av den nye tolkningen/registeret.

Kontrollimport validerer alle låste felt mot den bevarte eksporten og revaliderer kildeovergang, aktivering og forgjenger mens `BEGIN IMMEDIATE` hindrer andre skrivere. Ingen del av en ugyldig fil publiseres. Identiske filbyte returnerer det opprinnelige importresultatet uten å flytte noen peker. En nyere avvisning eller markering til kontroll sperrer eldre godkjenninger; det finnes ingen automatisk reserve til dem.

## Kontrollert resultat og avgrensning

En ny, separat resultatmodell viser råverdi, eventuell godkjent effektiv verdi og faktisk brukte avgjørelser. Den har egen regelidentitet og binder kilde- og aktiveringsoverganger også for uttrekk uten beløp. Ferskhet vurderes ved lesing som `gjeldende`, `utdatert` eller `ikke_vurderbar`, adskilt fra faglig status. Siste ventende, feilede eller manglende kildeforsøk vises separat.

Enkeltbeløp kan godkjennes for `analysebelop`. Godkjent kjedesaldo krever et uttrykkelig `HistorySelection`, godkjent bruk `kjedegrunnlag` for alle berørte beløp, kjent organisasjon og katalog, og bestått eksisterende kjedekontroll. Resultatet sier fortsatt ingenting om årsdekning. En manuelt korrigert verdi brukes i den separate kontrollvisningen. Den skriver ikke om B3/B4s regnekjede eller dens råavvik, og løfter ikke alene en sperret kjede. Dette konservative snittet er valgt fremfor å innføre en ny generell kjederegel eller hendelsessammenslåing i B5. Havtil og 5999-konfliktene består.

## Lagring og filgrense

SQLite versjon 4 legger bare til tabeller for register, eksportgrunnlag, importartefakter/diagnostikk, kontrollgrunnlag, aktiveringsoverganger, avgjørelser, bevis og kontrollerte resultater. B1–B4-tabeller og innhold endres ikke. B3-initialisering bruker høyeste kjent versjon og kan ikke nedgradere 4 til 3. B2s ventende jobber og gamle skrivegrenser består. Lesing av gamle resultater krever ingen migrering; ukjente fremtidige versjoner avvises.

Arbeidsfiler begrenses til 8 MiB, 10 000 datarader og 30 000 tegn per celle; XLSX begrenses dessuten til 128 ZIP-medlemmer og 64 MiB deklarert utpakket innhold. Formler evalueres aldri og formel-/feilceller avvises. Råbyte for innleste gyldige og ugyldige filer bevares. Filer over bytegrensen avvises før innlesning med varig diagnostikk og uten påstått råhash; råbyte for disse bevares ikke. Tekst skrives sikkert, og eksport bruker midlertidig fil og atomisk erstatning. Database, bevarte import-/bevisbaner og filer som er byteidentiske med lagrede kilder, kan ikke overskrives av eksport.

Løsningen autentiserer ikke kontrollørens navn eller bevisets faglige relevans. Det er fortsatt saksbehandlerens uttrykkelige ansvar. Rolleforvaltning, historisk Excel-adapter, årsdekning og løsning av historiske kjedekonflikter er utenfor B5.
