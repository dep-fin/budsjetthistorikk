# B6: samlet sesjonsuttrekk

B6 sammenstiller uttrykkelig valgte, allerede lagrede B2-inventarer, B3/B4-uttrekk, B5-kontrollresultater og eventuelle historikkberegninger. Eksporten henter ingen kilde, tolker ingen ny revisjon, aktiverer ingen tolkning og velger ingen ny faglig avgjørelse. Et Excel-uttrekk kan derfor også vise historisk grunnlag. Aktuell godkjenning står i en egen kolonne.

## Kjøring og JSON

```powershell
python -m analyse --database vedtak.sqlite --sesjonsutvalg sesjon.json --excel sesjon-kontroll-01.xlsx
```

Excel-filen må være ny. Database, utvalgsfil, bevarte kilde-/importfiler og eksisterende filer overskrives ikke. B1–B5-valgene og standardene deres er uendret; `--sesjonsutvalg` er et nytt gjensidig utelukkende valg. JSON-feil gir `eksportfeil` og returkoden 1. Vellykket eksport gir returkoden 0 også når rapporten viser faglige avvik. Eksportsuksess er ikke godkjenning.

Et minste utvalg kan være:

```json
{
  "dataset": "produksjon",
  "session": "2026-2027",
  "inventory_job_ids": ["erstatt-med-eksakt-B2-jobb-ID"],
  "extraction_ids": [],
  "controlled_result_ids": [],
  "history_calculation_ids": [],
  "supplemental_inventory_job_ids": [],
  "budget_years": [2026, 2027],
  "fdep_nrs": [],
  "chapters": ["900", "1760"],
  "posts": [],
  "reconciliations": [],
  "source_expectations": [],
  "preserved_2024_controls": null
}
```

Erstatt ID-ene med tidligere returnerte ID-er. `prove` velges for historiske/syntetiske prøver. Utvalgsfilen er UTF-8, høyst 8 MiB. Ukjente felter, skalarer i listefelter, gjentatte ID-er, boolske budsjettår og kontokoder med ledende nuller avvises. Fdep er den lagrede administrative koden, ikke Gul bok-grupperingen. Registerkoblingen leses fra observasjonens historiske tolkning, aldri fra dagens registerhode.

Innen hvert filter er verdiene alternativer (OR); mellom budsjettår, fdep, kapittel og post gjelder AND. En tom liste betyr ingen avgrensning i den dimensjonen. Manglende år, konto eller departement i en aktiv filterdimensjon blir `uavklart_treff` dersom ingen annen kjent dimensjon avkrefter treffet. Det blir med i eksporten og sperrer komplett sum. Filtrene påvirker aldri kildeinventaret eller den globale avvikslisten.

Råavvik, gjenstående B5-avvik og kjedesperrer vurderes på alle observasjonene i de valgte uttrekkene før beløpsfiltrering. Rapportens `unfiltered_rows` bevarer dette grunnlaget med `treff`, `uavklart_treff` eller `utenfor`; `rows` inneholder filterutvalget. `Avvik` viser også avvik utenfor filteret med observasjons-ID, år, konto, råverdi, uttrekk og lokator. Et departementsfilter kan derfor utelate en inngående rad fra beløpsvisningen uten å fjerne den fra kjedekontrollen.

Hovedjobbene må gjelde samme valgte sesjon og datasett. Supplerende jobber må uttrykkelig gjelde en annen sesjon. En original for budsjettåret kan dermed tas inn fra forrige sesjon, med egen dekningsrad. Sesjon og budsjettår holdes adskilt. Bare uttrekk for en revisjon i disse valgte inventarene kan velges. Velg én tolkning per revisjon. Flere valgte revisjoner av samme vedtak bevares som et synlig motstridende grunnlag og brukes ikke som gjeldende godkjente verdier.

## Inventar, dekning og kontroll

`Kildeinventar` omfatter alle ID-er i valgte jobber, uansett vedtakstype og filtre. Det viser også tidligere kjente ID-er som ikke finnes i valgt inventar, som eksplisitte avvik. Fullteksten finnes i `Vedtaksfulltekst` for valgte uttrekk og `Inventarfulltekst` for øvrige kilder. Hele HTML-teksten bevares i ordnede 30 000-tegnsbiter. Tekstopplysninger/fullmakter fra valgte uttrekk vises separat til kontroll. Et vedtak uten uttrekk eller beløpsobservasjoner er ikke automatisk faglig klassifisert som uten bevilgningsinnhold.

`Dekning` viser tre ulike nivåer: bevart kildeinnhold, strukturert innhold og antall gjeldende faglig godkjente enkeltbeløp. Fullt kildeinnhold krever et fullført, ikke-tomt inventar med `scope=full`, alle kjente ID-er vurdert, ingen manglende ID og et siste relevant forsøk som inngår i det valgte fulle grunnlaget. Valgt/delvis inventar, historiske alternativer og nyere ventende/feilede forsøk vises. Et tomt HTTP-svar gir aldri full kilde- eller faglig dekning.

`professional_complete` er en sperre mot automatisk erklæring om uttømmende faglig dekning og forblir `False` i B6. Rapporten viser faktisk B5-godkjenning per observasjon og antall godkjente enkeltverdier. Den innfører ingen ny manuell godkjenningsordning for en hel sesjon eller et budsjettår. Slike erklæringer krever relevant kilde-/beløpsavstemming og avklaring av rester utenfor denne eksporten. Dette gjelder særlig sesjonen 2026–2027, som ikke er erklært uttømmende kontrollert.

`Beløpsobservasjoner` viser rå tekst, rå kroneverdi, separat korreksjon, effektiv verdi i det historiske B5-resultatet og gjeldende godkjent verdi. Beløp, godkjente felter/bruk, avgjørelses-ID, bevis og avvik finnes også i de bevarte kontrollfeltene. Bare eksplisitt valgte B5-resultater brukes. Et begrenset B5-resultat godkjenner ikke øvrige observasjoner. Manglende dekning blir synlig per observasjon. Flere valgte kontrollresultater for samme observasjon krever avklaring; eksporten velger ikke et av dem automatisk.

Ferskhet kontrolleres mot kildeovergang, aktivert uttrekk/tolkning/register/kontrollgrunnlag og nyere faglige avgjørelser. En nyere avvisning eller markering til kontroll sperrer et eldre godkjent resultat. A → B → A gjenoppliver aldri den gamle godkjenningen. Dette gjelder også B5-resultater for uttrekk uten beløpsobservasjoner. Historiske verdier beholdes merket, med tom aktuell godkjent kolonne. B3s tekniske saldo vises som teknisk saldo og blir aldri faglig godkjent av eksporten.

## Historikk og summer

`Historikk` ordner vedtak etter uttrykkelig vedtaksdato og viser nivå, før, endring og etter i separate felt, med rå/korrigert/historisk effektiv/gjeldende godkjent verdi. Vedtaks-ID, sesjon, budsjettår, lokator, råhash, revisjon og tolkning følger hver rad. Manglende/samme dato er en synlig rekkefølgesperre, ikke en juridisk rekkefølge utledet fra ID.

`Summer` grupperer bare like budsjettår, beløpsbetydning, detaljeringsnivå, budsjettside, valuta og multiplikator. Før, endring og etter får ingen samlet sum. Posttotaler og komponenter får egne grupper. Alternative nivåer på samme konto summeres ikke. En gjeldende godkjent nullverdi forblir numerisk 0. Ingen verdi for manglende start, ukjent konto, uavklart normalisering eller kildekonflikt konstrueres som null. Godkjent delsum har egne observasjons-ID-er og utelatte ID-er; `None` for komplett sum betyr ufullstendig grunnlag. De dokumenterte Havtil-/5999-konfliktene og post-24-nivå uten delta sperrer komplett sum.

Et aktivt beløpsfilter gir bare en uttrykkelig merket delsum (`filtrert_delsum` og `Sumomfang` i Excel), med tom komplett sum. Globale avvik utenfor filteret beholdes også i sumgruppens avvik. Delsummen omfatter bare feilfrie, gjeldende godkjente rader i gruppen; den godkjenner ikke utelatte rader, øvrige kilder eller årsdekning.

## Avstemming og kildeprøver

Tom `reconciliations`, tom `source_expectations` eller utelatt `preserved_2024_controls` viser **ikke utført** for den aktuelle kontrollen. Kjøring av en annen kontroll erstatter ikke dette.

Hver avstemming er en `Reconciliation` med følgende felter:

- `name`, `actual_scope` og `reference_scope`.
- Begge omfang har `budget_year`, `period_start`, `period_end`, `concept`, `detail_level`, `currency` og `multiplier`.
- `concept` skiller `saldert`, `arets_bevilgning` og `avgrenset_endring` fra `rekneskap` og `samla_loyving`. De to siste er gyldige beskrivelser av et kontrollgrunnlag, men uforenlige med eksportens bevilgningsverdier.
- `observation_ids` velger eksakte eksporterte observasjoner for saldert eller avgrensede endringer. Saldert krever ett originalt nivå per konto; avgrenset endring krever observerte delta innen perioden.
- `controlled_chain_ids` kan brukes for årets bevilgning. De må være valgte, gjeldende B5-kjederesultater med en eksplisitt valgt historikkberegning, riktig budsjettår og hel årsperiode. Et kontrollert etterbeløp alene er ingen godkjent årskjede.
- `references` inneholder én `ReferenceValue` per konto: `chapter`, `post`, valgfri `subpost`, `expected_amount_kr`, `absent`, `reference`, `sha256`, `locator` og `reason`. Oppgi et helt kronebeløp med `absent=false`, eller `expected_amount_kr=null` og `absent=true`. Null og 0 er forskjellige opplysninger.

Perioder og faglig betydning må være forenlige. Kroneverdier sammenlignes i NOK, multiplikator `1`. Om kontrollkilden bruker tusen kroner må den dokumenterte konverteringen være utført før den legges inn som forventet kroneverdi; en mismatchet enhetsmodell passerer ikke. Budsjettår utledes aldri fra DFØs periode eller tildelingsdato. Den valgte datoavgrensningen for en observasjonskontroll gjelder vedtaksdato, mens en hel årsbevilgning har budsjettårets kalenderperiode.

Kontrollen bruker unionen av kontonøklene og viser `samsvar`, `belopsavvik`, `mangler_i_uttrekk`, `mangler_i_kontrollgrunnlag`, `uforenlig_omfang` eller `ikke_vurderbar`. Manglende rader får aldri et oppdiktet nullbeløp. Uttrykkelig fravær i referansen bevares; manglende rad i et begrenset uttrekk er ikke bevis for faktisk fravær gjennom hele perioden.

Den fulle avstemmingsspesifikasjonen bevares én gang per kontroll i utvalgs-JSON på `Sesjonsgrunnlag!B4`, med ordinær videreføring ved lange felt. `Avstemming` har bare de to omfangsbeskrivelsene i hver rads `Omfang`. `Kontrollgrunnlag` peker til kontrollens indeks i JSON-listen `reconciliations`; radens egen kildereferanse vises separat. Flere referansekontoer gjør dermed ikke hver avstemmingsrad større.

En `SourceExpectation` angir `observation_id`, `expected_raw_amount_kr`, `expected_effective_amount_kr`, `sha256`, `locator`, `amount_field`, `reference` og `reason`. Den kontrollerer eksakt observasjon, råbeløp, gjeldende effektiv verdi og kildelokator. JSON-null for forventet råbeløp betyr at prøven uttrykkelig forventer uavklart normalisering, som `I 615 833`; en godkjent referatkorreksjon kan samtidig forventes som effektiv verdi. Kontrollen autentiserer ikke en brukers kildehenvisning eller faglige vurdering.

Før Excel publiseres, leses de faktiske beløpscellene tilbake og sammenlignes eksakt med valgte observasjoner, B5-resultat-/avgjørelses-ID-er, råbeløp, historiske effektive verdier og aktuelle godkjente verdier. En avvikende fil publiseres ikke. Formellignende kildetekst skrives som tekstceller.

## Reproduksjon av #2-kontrollen

`preserved_2024_controls` kan uttrykkelig peke til mappen `docs/research/issue-2`. En relativ bane i CLI-utvalget tolkes relativt til JSON-filen. `audit_preserved_2024(directory)` kontrollerer seks fastfestede artefakthasher og beregner avstemmingen på nytt. Funksjonen bruker DFØs opprinnelige beløps-/overføringsfelt med `Decimal`, kildekontrollert inntektsfortegn for 2024 og PDF-uttrekkets **Løyving × 1 000**. Den leser ikke tidligere kontrollutfall eller normaliserte DFØ-kolonner som fasit.

Avstemmingen viser 1 625 felles poster med eksakt samsvar og 43 separate omfangsforskjeller, med manglende side som nullverdi. Forklaringene valideres mot de faktisk beregnede beløpene. De 1 574 opprinnelige API-postene kontrolleres mot Blå bok. Inventar/typefordeling beregnes fra alle 2 183 bevarte inventarrader. Dette er en reproduksjon fra hashfestede, avledede forskningsartefakter, ingen ny kontroll av original-PDF eller generell regnskapsimport. Den avstemmer ikke automatisk de valgte B6-beløpene; disse trenger sine egne avstemminger og kildeprøver. De tre historiske kjedekonfliktene består.

## Python-grenser og lagring

`SessionSelection`, `selection_from_dict`, `build_session_report(database, selection)` og `export_session_excel(database, selection, output, input_path=None)` er offentlige analysegrenser. Rapporten er en datert lesevurdering med egen ID, ikke et nytt lagret faglig resultat. Ingen databaseskjemaendring eller skjult skrivemigrering innføres. SQLite-versjon 4 og alle tidligere ID-er/resultater beholdes; B6 virker også på B2/B3-grunnlag uten valgte B5-resultater.

`read_inventory(database, job_ids)` gir valgte B2-jobber, kjente ID-er, aktuelle revisjoner, monotone kildeoverganger og siste forsøkskontekst i ett SQLite-snapshot. `read_decisions(database, ids)` leser eksakte valgte avgjørelser med delt kildekontekst. Den ytre B6-leseren følger SQLite `data_version` og avviser sammenstillingen dersom en annen forbindelse endrer databasen mens rapporten bygges. Eksporten bruker deretter bare vurderte data og immutable kildetekster. Se [ADR 0007](adr/0007-b6-eksplisitt-sesjonseksport.md).

B7 legger additivt til schema 5 og kildeforsøk før HTTP. B6 leser dette uten skrivemigrering, og nyere feil/venting inngår i ferskheten. `export_built_session_excel` eksporterer en allerede frosset vurdering; `export_session_excel` beholder sitt eksisterende API. Se [B7-kontrakten](datakontrakt.md#b7--datojobb-kildeforsøk-og-varig-varsling). Eksport fra en frosset vurdering beholder vurderingstidspunktet, selv om en senere vurdering ville ha vist nytt kildegrunnlag.
