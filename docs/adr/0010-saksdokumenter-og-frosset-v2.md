# ADR 0010: separat saksberikelse og eksplisitt frosset v2

Valgt for B8/#28, etter eierens mandat 22. oktober 2026. Stortingets saks-API gir dokumenthenvisninger på saksnivå. Det gir ikke dokumentenes beløp eller bevis for tilknytning til hver enkelt budsjettpost. [Kildekontrollen](../research/b8/README.md) viser to ulike innstillinger til deler av samme proposisjon, nil eksport-ID for proposisjonen og ulike referatlenker med samme eksport-ID.

## Valg og alternativer

Berikelsen lagres i egne `b8_*`-tabeller med modulversjon `saksdokumenter-1` innen hovedschema 5. Å legge dokumentene inn i gamle `Decision`, `AmountObservation`, v1/v2-tolkninger eller B5-bindinger ville endret betydningen av eksisterende immutable resultater og kontrollavgjørelser. Å øke hovedschema til 6 ville stengt tidligere skrivere unødvendig. De gamle tabellene, ID-reglene og standardvalgene bevares; ukjent hoved-/modulversjon avvises.

Et eget saksforsøk registreres før HTTP, uten å bruke B2/B7s sesjonsforsøk. Mottatte byte bevares før proveniens-/XML-tolkning og binder forsøket til første byte-/metadataforhold. Identisk gjenopptak er tillatt; bindingen kontrolleres atomisk ved publisering. Transportfeil uten tilgjengelige responsbyte har ingen råhash. HTTP-feil med lesefeil avsluttes med kjente transportmetadata; eksplisitt tilgjengelige delbyte bevares som ufullstendige, med faktisk hash. Avviste mottatte byte har faktisk hash og feilgrunn. En vellykket kildeobservasjon binder eksakte byte og metadata. Revisjonen identifiserer bare utvalgte saks-, publikasjons- og relasjonsfelt uten `respons_dato_tid`. Endret biografi, saksgang eller emne ligger fortsatt i råoriginalen, men regnes ikke som ny dokumentrevisjon. Råfelt, nil, lokator og kildehash følger hver referanse.

Gjeldende sakspeker følger monotone kilde- og hentetider. Eldre lagrede kilder bevares som `eldre_kilde`, uten å overta pekeren. A → B → A gjenbruker innholdsrevisjon A, men har tre observasjoner og tre innholdsoverganger. Lik dokumentrevisjon etter ny henting er ingen ny rettelse. En berikelse binder eksakt vedtaksrevisjon, saksforsøk, dokumentrevisjon og tolkningsversjon. Historiske referanser og nytt feilforsøk vises samtidig. Ingen saksfeil blokkerer B2/B3 eller endrer B5-godkjenninger.

Stikkord får en egen versjonert visning `stikkord-1` av den bevarte vedtaksteksten, med rå formålsfelt, HTML, kildehash og lokator. Kjente uttrykk i dokumentert kursiv markering bevares i kilderekkefølge. Ukjent/umerket mulig stikkord blir uavklart; ingen funn i en støttet formålsrad er en annen status. Denne visningen registrerer ingen beløp og omskriver ingen tidligere parser. Vedtak 211s separate stikkordsfullmakt bevares som fulltekst og gir ingen ekstra beløpshendelse.

## Eksport og konsekvenser

Det nye analysevalget består av en uendret `SessionSelection` og eksplisitte berikelses-ID-er. Hele B6-inventaret vurderes før beløpsfiltre. Manglende valg, feil, nyere kilder, historiske vedtak og uavklarte dokumenter vises globalt. Relasjonsnivået er alltid sak; en delt proposisjon arver ikke innstilling eller postkobling fra en annen sak.

`b6-frozen-2` inneholder den uendrede B6-rapporten, berikelser, aktuelle separate ferskhetsakser og frosne kildetekster. Et `data_version`-vern dekker hele lesingen. Filskriving fra snapshot krever ingen nye database- eller nettlesinger. Excel gjenbruker B6s oppsett, men har formelt vedtaksnummer med sesjon, eksplisitt teknisk API-ID, stikkord og klikkbare dokumentetiketter. Egne dokument-, relasjons- og avviksark gir ingen beløpsjoin eller suminflasjon. Faktiske celler leses tilbake før atomisk publisering til nytt navn.

`b6-frozen-1`-leser/-skriver og B7s standardeksport er uendret. Den nye grensen er uttrykkelig opt-in. Ingen dokumentfulltekst, forslagsbeløp, faglig årsdekning eller driftssetting følger av berikelsen. #10 står fortsatt åpen for utsatt faktisk driftsaksept.
