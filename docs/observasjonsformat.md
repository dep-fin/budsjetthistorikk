# Felles observasjonsformat, versjon 1

Status: besluttet spesifikasjon 20. oktober 2026 etter prosjekteierens mandat om å presisere formatet før #6. Dette dokumentet er den faglige kontrakten. Det avgrensede B3-snittet, konkret API og additiv lagring beskrives nå i [datakontrakten](datakontrakt.md#b3--beløpsobservasjoner-og-valgt-historikk) og [ADR 0004](adr/0004-b3-lagring-og-utvalg.md). Full historisk Excel-adapter og senere kilder er fortsatt egne leveranser.

## Formål og avgrensning

Historiske Excel-data og nye stortingsvedtak skal kunne levere kildeforankrede beløpsobservasjoner til samme analysegrunnlag. Formatet er langt: én observert beløpsverdi per kildecelle eller beløpsfelt, med egne relasjoner til dokumenter, andre beløp og omtale. Et nytt stadium krever dermed ingen ny beløpskolonne. En kilde med før-, endrings- og etterbeløp gir tre observasjoner knyttet til samme vedtaksledd; det gir ikke tre additive hendelser.

Beslutningen bygger på [kontrollen av de faktiske filene 2013–2025](research/historisk-excel/modellvurdering.md), [kravene](krav.md) og kildeprøvene fra #2. Åpne enhets-, stadie- og dokumenttolkninger er fortsatt åpne. Ingen Excel-kolonne får faglig godkjenning bare fordi den passer i formatet. Første implementering i #6 avgrenses til opprinnelig vedtak og senere vedtatte endringer. Historisk adapter, forslag, regnskap og omtale kommer i sine leveranser.

## Identitet og kildegrunnlag

Disse identitetene har ulike oppgaver og skal holdes adskilt:

| Begrep/felt | Innhold og regel |
| --- | --- |
| `formatversjon` | `observasjon-1`. Uavhengig av B1s Report-versjon, B2s kontraktversjon og SQLite-skjemaets versjon. |
| `artefakt_id` | SHA-256 av faktisk originalbyte. Filnavn, kildeart, MIME-type og byteantall følger artefakten. En arbeidsbok og en HTTP-respons er ulike kildearter. Originalene lagres uendret. |
| `kildeenhet_id` | Navneromsavgrenset kildeidentitet, f.eks. et Storting-vedtak. API-ID er valgfri for andre kilder. Manglende faglig identitet bevares som uavklart. |
| `kilderevisjon_id` | Ett innhold i kildeenheten. B2s vedtaksrevisjon gjenbrukes for Storting-kilden; Excel bruker den bestemte arbeidsbokartefakten. Ny arbeidsbok er ikke automatisk nye vedtak. |
| `tolkning_id` | Versjon av adapter og normaliserings-/klassifikasjonsregler som frembrakte observasjonen, med begrunnede kontrollvalg der de brukes. Ny tolkning er ikke kilderettelse. |
| `observasjon_id` | Stabil identitet innen kildegrunnlaget: kilderevisjon, lokator, beløpsfelt, tolkning og formatversjon. Samme grunnlag lest på nytt gjenbruker observasjonen. Ny tolkning/revisjon bevarer tidligere observasjoner. |
| `innlesning_id` | Et konkret forsøk med datasett, tidspunkt, kildegrunnlag og resultat. Flere innlesninger kan vise samme observasjon; deres ID-er er aldri beløpshendelser. |
| `hendelse_id` | Valgfri identitet for en dokumentert faglig hendelse. Kobling krever kildebevis; likt år/kapittel/post/beløp eller dokumentlenke er utilstrekkelig. |

Kilderevisjonen har et uttrykkelig kildesystem/navnerom. For Excel uten varig rad-ID er kildeenheten lokal til arbeidsboken, ikke en påstått stabil rad på tvers av filendringer. Radflytting eller ny fil kobles ikke automatisk til gamle observasjoner.

Hver observasjon har minst én kildepeker til artefakt og lokator. Excel-pekeren inneholder nøyaktig arknavn, 1-basert rad, kolonnenavn og celleadresse; en dokumentrad peker særlig på beløpscellen og bevarer resten av raden. Storting-pekeren inneholder vedtaksidentitet/revisjon og den eksisterende HTML-/tabellokatoren, utvidet med beløpsfelt når raden har flere beløp. Filens inventar og kildens objekter bevares slik at ukjente kolonner, originaltekst, stikkord og metadata kan gjenfinnes uten informasjonstap.

En B2-revisjon kan ha flere råresponspekere. Volatil konvolutttid gir nye kildeobservasjoner, men ikke nye beløpsobservasjoner. Det opprinnelige uttrekksgrunnlaget og senere kildeobservasjoner er separate relasjoner. Nytt innhold A → B → A følger B2s revisjons- og kontrollregler.

Datasett er uttrykkelig adskilt: `produksjon` for ordinære Storting-kilder fra avtalt start, `historisk` for reelle historiske Excel-data og `prove` for kildeprøver/syntetiske kontroller. Dette er formatets datasettbegreper; dagens B2 implementerer bare sine eksisterende datasett. Historisk import skal ikke omgå B2s startgrense ved prøvemerking. Sammenligning på tvers er mulig, men sammenslåing krever en dokumentert beslutning.

## Beløpsobservasjonens felter

Alle feltgrupper nedenfor skal kunne representeres. Nullable opplysninger har `null` og en angitt grunn (`ikke oppgitt`, `ikke relevant` eller `uavklart`); tom tekst skal ikke skjule årsaken. En kildenær observasjon kan beholdes med uavklarte faglige felt og kontrollbehov. Manglende regnskap/stadium gir ingen oppdiktet observasjon.

| Feltgruppe | Kontrakt |
| --- | --- |
| Konto | Rå og normalisert kapittel/post/underpost, kildens kapittel-/postnavn, `detaljnivaa` og eventuelle dokumenterte komponentrelasjoner. Normaliserte kontokoder er tekst med avtalt kanonisk form; rå ledende nuller beholdes separat. Ukjent er ikke kode `0`. |
| Periode | `budsjettar`, kilde for årstolkning, valgfri vedtaksdato og separate dokument-/vedtakssesjoner. Budsjettår gjelder hver observasjon, også hvis ett dokument omtaler flere år. Innlesningstid er ikke vedtaksdato. |
| Verdi | Rå celletype, rå numerisk/leksikalsk verdi og eventuell formel/lagret resultat, original beløpstekst og enhetsangivelse. `belop_kr` er heltall eller null; fortegn bevares. Kildens presisjon og konverteringsregel med kildebevis følger normaliseringen. |
| Faglig klassifikasjon | `talltype`, eventuell forslagsrolle, `behandlingsrunde`, `stadium_original`, `belopsbetydning`, `omfang` og `detaljnivaa`, som definert nedenfor. Hver normalisering har grunnlag; dokumenttypen bestemmer ikke automatisk talltypen. |
| Organisasjon | Kildens Dep, fdep_nr, gdep_nr, gdep_navn, omr_nr og kat_nr bevares hver for seg der de finnes. Tolkede registerkoblinger har kilde, registerversjon og gyldighet fra/til, med årspresisjon når dato ikke er kjent. Manglende kobling skjuler ikke beløpet. |
| Dokumenter | Null eller flere referanser med rolle. Fravær av proposisjon, innstilling eller verifisert URL hindrer ikke kildebevaring. |
| Kontroll | Separate struktureringsstatus, faglig kontrollstatus og liste av avvik med kode, grunnlag, berørte felt og eventuell avklaring. B1 `strukturert` er ikke automatisk godkjent analysetall. |

For kontokoder er normalformen desimal tekst uten ledende nuller (`"01"` → `"1"`); kapittel/post forblir separate felter. Underpost bevarer kildens kode, inkludert `"0"`. `detaljnivaa` kan være `post`, `underpost` eller `uavklart`; kode `0` alene beviser ikke posttotal. Uavklart betydning av underpost i ett ark skal ikke arve et annet arks tolkning. Inntekt/utgift følger dokumentert kapittelregel, aldri beløpsfortegn eller teksten «Driftsinntekter» på en komponent.

Faglige akser er uavhengige:

| Akse | Verdier i versjon 1 | Eksempel på skille |
| --- | --- | --- |
| `talltype` | `regjeringsforslag`, `komiteforslag`, `stortingsvedtak`, `regnskap`, `uavklart` | En innstillingslenke på en historisk rad beviser ikke hvilket beløp regjeringen foreslo. |
| `forslagsrolle` | `tilraading`, `alternativ`, `uavklart` eller null når ikke relevant | Flertallets tilråding og øvrige komitéforslag kan eksistere parallelt. Forslagsidentitet/avsender bevares ved parallelle alternativer. |
| `behandlingsrunde` | `opprinnelig`, `rnb`, `nysaldering`, `ovrig`, `uavklart` | Både forslag og vedtak kan høre til RNB. Kildens egen etikett/kode bevares i `stadium_original`. |
| `belopsbetydning` | `nivaa`, `endring`, `for_belop`, `etter_belop`, `uavklart` | Saldert budsjett er et nivå; «økes med» er en endring. |
| `omfang` | `enkeltledd`, `aggregat`, `uavklart` | En førstehalvårssum er ikke et nytt enkeltvedtak. Aggregatets dekningsperiode/hendelser er egne opplysninger og kan være uavklarte. |

Fullmaktsrammer, satser og overførte midler bevares som egne kildeopplysninger, med en egen opplysningstype, og er ikke bevilgningsobservasjoner som kan tas inn i kjeden. Omtale er beskrevet nedenfor. Dette krever ikke at alle slike kilder detaljstruktureres i #6.

## Beløpsenheter og kvalitet

Enhet oppgis som NOK med multiplikator, f.eks. 1, 1 000 eller 1 000 000, eller som uavklart med rå etikett. Normalisering bruker desimalaritmetikk fra bevart kildeverdi, ikke binære flyttall som pengemodell. Dersom omregningen ikke gir hele kroner, forblir `belop_kr` null frem til en uttrykkelig, kildebegrunnet presisjons-/avrundingsregel er avklart. Det finnes ingen generell regel som runder Excel-spor til nærmeste tusen eller automatisk velger millioner ut fra tallstørrelse.

En matematisk kandidatverdi kan bevares som uavklart normalisering, men brukes ikke som godkjent kroneverdi. Enhetsregelen skal være avgrenset til adapter, år, ark og kolonne der kontrollgrunnlaget gjelder. Én avstemt celle godkjenner ikke alle årganger. Rå null, manglende verdi og uavklart faglig null holdes adskilt: 2015s f150-null bevares som observert 0 med avvik, ikke omgjort til blankt eller godkjent budsjettstilling.

Struktureringen angir om kildefeltet er lest entydig. Faglig kontroll bruker `til_kontroll`, `godkjent` eller `avvist`; godkjenning angir hvilke felter/bruk den dekker og kildegrunnlaget. Vurderinger er egne versjonerte registreringer, med begrunnelse og tidspunkt. Beregninger har dessuten egen deknings- og kjedestatus. Godkjent enkeltbeløp betyr ikke komplett/godkjent historikk. Kilderettelse, ny tolkning eller endret register-/analysegrunnlag gjør berørte vurderinger utdaterte, med B2s innholdsovergang som del av grunnlaget der relevant. Ingen automatisk godkjenning ved A → B → A.

## Dokumentreferanser, sammenhenger og omtale

En dokumentreferanse bevarer `kode_original`, kildekolonne, tolket dokumenttype/nummer/sesjon, eventuell autoritativ ekstern ID/URL, relasjonsrolle og tolkningsstatus. Rolle kan være `forslagsgrunnlag`, `innstilling`, `vedtak`, `kontrollkilde`, `omtale` eller `uavklart`. Budsjettår hører til beløpet, ikke utledet fra referansens sesjon. `VedtakRNB`, `VedtakDok8` og `v1280/20-2` bevares ordrett, med uavklart identifikasjon frem til kildekontroll. En kildestreng kan ikke bli en bekreftet URL ved gjetning.

Relasjoner er mange-til-mange med egne kildebevis. Tre dokumentkoder på én beløpsrad skaper ikke tre beløp. Flere kilder kan belyse samme hendelse, men må først kobles gjennom sporbar avklaring. Andre beløpsrelasjoner kan angi «før/endring/etter i samme ledd», «komponent av» og «kontroll av aggregat». Rollen «komponent av» krever avklart hierarki; en løs kapittel-/postkobling er ikke nok. Summen av komponenter og posttotal kan ikke begge inngå i samme uttrekk.

Fremtidig omtale har egen seksjonsidentitet, dokument/revisjon, nøyaktig lokator og original tekst/struktur, med relasjoner til år, kapittel og eventuelt post. En seksjon kan høre til flere poster og finnes uten beløpsobservasjon. Det opprinnelige dokumentet bevares også. Forslagets omtale og innstillingens omtale har egne dokumentversjoner, selv om de gjelder samme post. Korte kildeutdrag i Excel er ikke erstatning for omtalen.

## Beregnet historikk og dobbelttellingsvern

Analysen leser observasjoner gjennom et uttrykkelig utvalg med datasett, kilderevisjoner, tolkninger, register-/kontrollgrunnlag og tidspunkt. En beregnet verdi har egen ID, regelversjon, inn-observasjoner, periode/konto og kontroll-/dekningsstatus. Den lagres/vises adskilt fra kildens observerte nivåer. En radposisjon eller behandlingsrunde er ikke dokumentert vedtaksrekkefølge; uavklart rekkefølge gir ufullstendig grunnlag.

For en vedtatt bevilgningskjede velges ett avklart opprinnelig nivå og deretter dokumenterte vedtatte enkeltendringer i riktig rekkefølge for samme konto/budsjettår. Regjerings-/komitéforslag, regnskap, aggregater, kontrollsummer, før-/etterbeløp og fullmakter legges ikke til som delta. En ny post får ikke automatisk inngående null. Kontroller `før + endring = etter` der alle finnes, og kontroller kjedens forrige saldo mot neste førbeløp. Manglende grunnlag eller konflikt sperrer godkjent kjedesum. Et separat kontrollert sluttbeløp kan fortsatt vises med sin egen proveniens.

To kilder med like beløp blir verken automatisk slått sammen eller lagt sammen. Valg av representasjon og eventuell ikke-additiv rolle må være dokumentert, og bevare begge observasjoner. En historisk førstehalvårssum kan brukes som separat kontrollaggregat; oppdeling i enkelthendelser krever underliggende bevis. Formatet løser ikke de tre historiske kildekonfliktene fra #2 ved å balansere summer.

## Konkret mapping og kontraktprøver

Eksemplene er faglige mappinger, ikke ferdig import. Kildebevis/celler og begrensninger finnes i [filkontrollen](research/historisk-excel/modellvurdering.md). Vedtaksprøven finnes i `tests/fixtures/40033944.derived.xml` med sidevogn. Eksempel-ID-er i en senere test skal merkes som lokale, ikke utgiver-ID-er.

| Kilde og faktisk verdi | Representasjon og påkrevd kontroll |
| --- | --- |
| B1-vedtak 40033944, 2024–2025, budsjettår 2025, kap. 42/post 1: 10 478 000 kr | `stortingsvedtak` + `opprinnelig` + `nivaa` + `enkeltledd`, postnivå. B2-revisjon og eksisterende lokator bevares. «Opprinnelig bevilgning» i B1 er en kompatibel mapping, ikke et endret B1-felt. Departement forblir uavklart hvis det ikke finnes oppslag. |
| 2013 `Rådata!H2=10.032`, kap. 1/post 1/upost 1 | Én nivåobservasjon med `stadium_original=Saldert (f120)`. Millionfaktoren har ett konkret kontrollanker, ikke blanketgodkjenning. Regjeringsforslaget i G2 er en annen observasjon. API-ID/vedtaksdato kan mangle. |
| 2015 `Rådata!J2=0`, f150, mens H2 er positiv | Bevar rå 0, kildecelle og etikett. Faglig bruk av nivået er `til_kontroll`; ingen godkjent budsjettstilling eller oppdiktet manglendeverdi. |
| 2025 kap. 100/post 21, I36=0, K36=-5; dokumentrad 15 har -5 000 000 og i540/24-25 | Separate observasjoner for kildecellene og dokumentbeløpet. Forslaget er ikke det senere resultatet. Kildenes forbindelse, enhet, omfang og talltype må kontrolleres før beløp brukes i kjeden. Den ene referansen blir ikke flere talltyper. |
| 2025 kap. 20/post 1, rådatarad 6/upost 1 og rad 7/upost 2; dokumentrad 2/upost 0 | Alle tre kildeposisjoner bevares. Ingen duplisering av dokumentbeløpet ved join på kapittel/post og ingen tvungen fordeling på underposter. Nivåkobling er egen kontroll. |
| 2017 dokumentrad 495: p141/16-17, i445/16-17, v963/16-17 | Én beløpsobservasjon med tre referanser. Verken tre additive hendelser eller tre antatt like forslags-/vedtaksbeløp. |
| Kilde uten dato, tvetydig dokumentkode eller manglende regnskap | Null med grunn for ukjent metadata; regnskapsobservasjon opprettes først når regnskapskilden finnes. Ingen dato fra radrekkefølge. |

I #6 skal kilde → lagring → Excel fortsatt være testgrensen. Kontraktprøvene skal vise kildepeker og akser, ett ledd med før/endring/etter uten dobbelttelling, gjenbruk ved gjentatt lesing, kildeversjon adskilt fra ny hendelse og separat beregnet saldo. De eksisterende prøvene for økning, reduksjon, manglende grunnlag og kjedekonflikt består som aksept. Excel-eksemplene her er kompatibilitetskrav til representasjon, ikke krav om full Excel-import i #6. #7/#8 tar avklart hierarki/registerkontroll, #13 tar historisk adapter og enhets-/kolonnekontroll, #9 tar samlet analyseutvalg og dekning.

## Kompatibilitet og videre bygging

`innlesning/` eier adaptere, råkilder, observasjoner og sporbar normalisering. `analyse/` eier eksplisitte utvalg, avledede kjeder og visning. Analysegrensen bruker formatet og krever ikke at kilden er et Storting-API-objekt. [Ansvarsdelingen](ansvarsdeling.md) består.

B1/B2s offentlige funksjoner, kildebyte, kontrollstatus og ID-er beholdes. En separat B3-adapter tolker uttrykkelig valgte revisjoner; gamle rapporter blir ikke automatisk en godkjent samlet historikk. Konkret lagring og additiv migrering med regresjonsbevis er beskrevet i [B3-kontrakten](datakontrakt.md#b3--beløpsobservasjoner-og-valgt-historikk). Den opprinnelige spesifikasjonsleveransen var ingen implementering av #6 eller #13; #13 er fortsatt utenfor B3. Plattform og mottakersystem forblir åpne.
