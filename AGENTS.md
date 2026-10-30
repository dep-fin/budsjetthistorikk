# Budsjetthistorikk

## Arbeidsmetode

Ved planlegging, ticketarbeid og review: les [arbeidsflyten](docs/arbeidsflyt.md) og følg trinnet oppgaven gjelder. Bekreftede krav og åpne produktbeslutninger finnes i [kravgrunnlaget](docs/krav.md).

Ved planlegging, svar fra prosjekteier/systemansvarlig eller funn av nye tekniske forutsetninger: les [avklaringslisten #65](https://github.com/depmartin/budsjetthistorikk/issues/65) med kommentarer. Oppdater beslutninger og avkryssing i samme økt, legg til nye nødvendige avklaringer og kontroller listen før overlevering etter [vedlikeholdsreglene](docs/arbeidsflyt.md#løpende-tekniske-avklaringer).

Før dokumentvisning, sammenligning av behandlingsledd eller konto-/årsvisning: les [målbildet og akseptkravene for de to inngangene](docs/to-visninger.md), [konkretiseringsforslaget under #37](docs/visningspilot-plan.md) og dets kildegrunnlag/testmatrise. Forslag til nye byggetickets er ikke byggemandat.

Ved videre arbeid med T1/#41: les [den separate visningspilotkontrakten](docs/visningspilot.md), [ADR 0011](docs/adr/0011-filbasert-visningspilot.md) og [T1-kontrollen](docs/research/visningspilot-41/README.md). Begge innganger bruker samme frosne grunnlag; nye adapterfeil skal være synlige uten å blokkere ordinær vedtaksinnlesning. Gamle formater, ID-er og schema 5 beholdes.

Før T2/315/78, kildegjenbruk eller lesing av visningspilot-2: les [T2-kontrakten](docs/komitepilot.md) og [kilde-/filkontrollen](docs/research/komitepilot-44/README.md). Standalone krever ingen T1-data; valgfri T1-union bevarer én gammel kapsel og gjenbruker ID-er/payloadreferanser.

Før 341→857→210, lokal 2024-regning eller visningspilot-3: les [T3-kontrakten](docs/forlopspilot.md) og [kilde-/filkontrollen](docs/research/forlopspilot-46/README.md). 857s nye 66aa-avledning og gamle 554e-kontroll er separate representasjoner. Avgrenset regning er ingen årsdekning eller årsbalansegodkjenning.

Før 201/2025, flerårsutvalg eller visningspilot-4: les [T4-kontrakten](docs/fleraarspilot.md) og [kilde-/filkontrollen](docs/research/fleraarspilot-48/README.md). 210 og 201 har samme dato, men separate budsjettår. Ukjent kontinuitet gir ingen videreføring eller sum mellom år; T3s regneport får bare eksplisitt 2024-grunnlag.

Før K3-perioderegister eller perioderegister-1: les [P1-kontrakten](docs/perioderegister.md) og [P1-kontrollen](docs/research/perioderegister-52/README.md). Fullmakt, registerstruktur, monetære hendelser og faglig årsdekning holdes adskilt. Gamle objekter gjenbrukes gjennom én uendret T4-basis.

Før sak 101000, 2024-lønnskompensasjon for 1429 eller overføringsfullmakt 429: les [R2-kildeundersøkelsen](docs/research/r2-101000-54/README.md). Prop. 36 vedlegg 4 har et eget /1-anslag; faktisk fullmaktsbruk og personellvirkning er uavklart. K3/P1s pinnede registre beholdes.

Før perioderegister-r2-1: les [P2-kontrakten](docs/perioderegister-r2.md) og [P2-kilde-/filkontrollen](docs/research/perioderegister-r2-56/README.md). Tre avgrensede R2-grener legges til én uendret P1-basis; historisk kandidatstatus og ny 101000-oppfølging vises separat. Gjeldende leveringsstatus står i #56.

Før sak 100895 eller R2s C05: les [U1-kildeundersøkelsen](docs/research/u1-100895-58/README.md). 229 gjelder stikkord på 1560/71; ingen ny dokumentert 1429-postvirkning. Søstersakene og faktisk fullmaktsbruk har egne bevisgrenser. Pinnede registre beholdes.

Før sak 99235, vedtak 853–856 eller R2s C06: les [C06-undersøkelsen](docs/research/c06-99235-60/README.md). Debatt 20. juni og votering 21. juni er dokumentert separat; senere motstridende datoutsagn beholdes. Egne tariffvedlegg navngir Riksantikvaren som forhandlingssted, uten postvis bevilgningsbevis. /22 arver ingen /1-forklaring; historiske kandidater og pinnede registre beholdes.

Før proposisjon16-1 eller hele Prop. 16 S-tabellen: les [T5-kontrakten](docs/proposisjon16.md) og [T5-kontrollen](docs/research/proposisjon16-62/README.md). 105 nye forslagfelt legges til én uendret T1-basis. Gammel dokument-ID/dekning bevares; gjeldende tabellstatus er eget overlay. Delt fullmaktsramme er ikke bevilgningsdelta. Innst. 95-beløp venter T6; gjeldende levering står i #62.

## Agent skills

### Issue tracker

Arbeid og spesifikasjoner ligger i GitHub Issues for depmartin/budsjetthistorikk. Før issue- eller PR-arbeid: les [issue tracker](docs/agents/issue-tracker.md).

### Domain docs

Prosjektet har én felles begrepsliste. Før faglig modellering eller kodeendringer: les [begrepsreglene](docs/agents/domain.md).

## Ansvarsdeling

Ved endringer i innlesning, analyse eller felles datakontrakt: les [ansvarsdelingen](docs/ansvarsdeling.md). Dokumentasjon og issues skrives på norsk.

## Varige kildefunn

Ved innlesning, kildevalg eller dekningskontroll: les [kildefunnene](docs/kildefunn.md). Bevilgningsendringer finnes også som ANNET; BUDSJETT alene er et utilstrekkelig filter.

Før økten avsluttes: lagre nye varige funn med kildebevis og praktisk konsekvens etter [reglene for kunnskapsoverføring](docs/arbeidsflyt.md#kunnskap-mellom-agentøkter).

## Kildeversjoner og gjenopptak

Før endringer i synkronisering, kontrollhenvisninger eller versjonseksport: les [B2-kontrakten](docs/datakontrakt.md#b2--kildeinventar-observasjoner-og-revisjoner) og [lagringsvalget](docs/adr/0002-kildeobservasjoner.md). B1-kjøringer er et historisk prøvearkiv og adopteres ikke automatisk som B2s vedtaksregister.

## Historisk Excel og felles historikkmodell

Før #6, historisk Excel-import eller utvidelse av den felles historikkmodellen: les [observasjonsformatet](docs/observasjonsformat.md) og [filkontrollen 2013–2025](docs/research/historisk-excel/modellvurdering.md). Formatet er besluttet som spesifikasjon; kildeundersøkelsens åpne tolkninger er fortsatt åpne.

Ved videre historisk import eller pakkeendringer: les [pilotgrensen](docs/historisk-pilot.md), [ADR 0009](docs/adr/0009-historisk-pilotpakke.md) og [hele 2024-kontrollen](docs/research/historisk-excel/pilot2024.md). Bruk implement/TDD og regnearkskill ved eksportendringer. Fullt råinventar og kandidater beholdes lokalt; ny offisiell innlesning er uavhengig av historikken.

Før kontrollmatrise, presisjonsregel eller faglig bruk av historiske 2024-kolonner: les [P2-matrisens omfang og kildebevis](docs/research/historisk-excel/p13-p2/README.md). Verifisert kildekontroll, foreslått normalisering og faglig godkjenning er separate statuser; matrisen aktiveres ikke i innlesningen.

Før endringer i B3: les [B3-kontrakten](docs/datakontrakt.md#b3--beløpsobservasjoner-og-valgt-historikk), [ADR 0004](docs/adr/0004-b3-lagring-og-utvalg.md) og B3-prøvene i [kildefunnene](docs/kildefunn.md#b3-prøver-tabellvariasjon-lokatorer-og-sperrede-kjeder). B1/B2-parser og lagrede resultater er uforanderlige; bruk separat tolkning. Avstemt utvalg er ingen faglig godkjenning eller årsdekning.

Før endringer i samlet sesjonsuttrekk: les [B6-veiledningen](docs/b6-sesjonsuttrekk.md), [ADR 0007](docs/adr/0007-b6-eksplisitt-sesjonseksport.md), [B5-kontrakten](docs/datakontrakt.md#b5--registervedlikehold-og-faglige-avgjørelser) og [B6-kontrollfunnene](docs/research/b6/README.md). Globalt inventar må ikke skjules av beløpsfiltre. Kildeinnhold, struktur, aktuelle godkjente enkeltverdier og uttømmende faglig dekning er ulike opplysninger. Den dokumenterte 2024-kontrollen må beregnes fra hashfestede kildefelt; tidligere kontrollprosent er ingen utført avstemming av en ny eksport.

Før endringer i daglig drift, forsøksferskhet, schema 5 eller GitHub-outbox: les [B7-veiledningen](docs/b7-drift.md) og [ADR 0008](docs/adr/0008-b7-varig-datojobb-og-outbox.md). Windows-plattform er valgt, men konkret vert/konto/lager/bakgrunnstilgang og faktisk driftsaksept er utsatt av eieren 21. oktober 2026. Ingen kode-/testleveranse alene lukker #10. Gamle skrivere skal bevare schema 5; uavklart GitHub-POST skal avstemmes før ny opprettelse.

Før saksdokumenter, stikkordvisning eller frosset v2: les [B8-veiledningen](docs/b8-saksdokumenter.md), [kildeprøven](docs/research/b8/README.md) og [ADR 0010](docs/adr/0010-saksdokumenter-og-frosset-v2.md). Saksrelasjon er ingen postvis forslagstilknytning. B8 er separat berikelse; gamle observasjoner, B5-bindinger og B7s frosset-v1-standard beholdes.

Før endringer i B8-Excel-visningen: les [B9-veiledningen](docs/b9-historikk.md) og [formatkontrollen](docs/research/b9/README.md). Historikk er en avledet hovedvisning med 13 kolonner; Historikkdetaljer bevarer tidligere felt. Kildenavn, beløpsbetydning, alternative grunnlag og globale avvik skal bevares uten ny faglig tolkning eller endret frosset JSON.

Før omtalestrukturering eller post-/hendelseskobling under #32: les [O1-kildebevisene](docs/research/omtale-o1/README.md), [godkjent O2-oppdeling](docs/research/omtale-o1/o2-forslag.md) og [O2a-kontrakten](docs/omtale-pilot.md). #34/O2a er flettet i PR #36 og #35/O2b i PR #39; les også [O2b-kontrollen](docs/research/omtale-o2b/README.md) før utvidelse. A-uttrekksversjonens betydning og gamle filer beholdes; B velges eksplisitt. 210-prøven har samlet komité, avrundet lønnsomtale og to posthendelser. Omtale lagres separat, er et frivillig supplement til uavhengig vedtaksinnlesning og endrer ikke hovedschema 5 eller gamle formater/ID-er. #10 står åpen.
