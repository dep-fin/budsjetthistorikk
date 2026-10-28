# Akseptledger T4/#48

Fasiten er fastsatt før kode i [kontrakten](../../fleraarspilot.md), issue #48
og [testmatrisen](../to-visninger-37/testmatrise.md). Faktiske lokale resultater
føres i `verification.json` og loggene; orkestratorens porter står separat.

| Port | Forpliktelse og kontroll |
| --- | --- |
| Kontrakt | `visningspilot-4`, `fleraar1429-2024-2025-1`, `fleraarsgrunnlag-1`; eksakte felter. Før-kode-commit fc2b629. |
| Kilde 201 | c5f3/metadata/manifest er hashbundet. Oppskriften rekonstruerer komplett 117 278-byte-objekt; budsjettåret er uttrykkelig 2025. |
| Beløp/tekst | 163 173 000 og 33 408 000 nivå; tr101/td4 og tr103/td4. Rånavn/stikkord, fulltekst, statuser og 153-raders helinventar. |
| Gjenbruk | T3s fem felt/objekter og gamle ID-er består. T1-kapselen er ordrett og validert; to parent-/metadatapayloads er legacy-referanser. |
| M18 | 2024/2025/årsunion, hver post og begge/kapittel, alle tellerfasiter og dokumentvalg gjennom faktiske JSON-/Excel-par. |
| M19 | Ukjent kontinuitet/oppgaveomfang på begge konti, separate årsgrupper, ingen relasjon eller aritmetikk på tvers av år. Syntetisk positiv kontinuitet avvises. |
| M06–M07 | Begge navigasjonsretninger/retur, dokument201s hele inventar, eksplisitte par uten kryssprodukt, union av kapittel/par, feil år, tomt flerårsvalg og fullmakt. |
| M16–M17/M21 | T3s lokale 2024-regning og avgrensede 857-/22-fraværsbevis består. Ingen 2025-inngang i regneporten; ingen helårspåstand. |
| M22 | Gjentatt eksport/lesing og bytte av inngang bevarer basis/ID-er og tellerantall. JSON-byte ved gjentakelse er identiske. |
| Fysisk lagring | Serialiserte objekter/payloads telles fra faktisk JSON og skrevet Excel-snapshot; én offlinekapsel. Arvede immutable kopier telles separat. |
| M23 | Skrevet/lukket/gjenlest JSON. Offentlig offline CLI med nett-/databaseforbud og fraværende originalrot. Originalene rekonstrueres fra pakken. |
| Negative filpar | Rehash av feil år/verdi/betydning/dato/rolle/rånavn/lokator/forelder/oppskrift/ref/hull/kontinuitet/utvalg/beregning, gammel verdi, referanse og inventartak avvises. |
| M24 | Skrevet/lukket/gjenlest Excel, alle synlige celler/typer/formater/stiler/lenker/visninger/filtre avstemmes. Årslenker er kontrollerte. |
| Skjult presentasjon | Falskt 2025-beløp, tallformat, skjult rad/kolonne/ark, feil lenke/filter og DOCTYPE avvises i faktisk lagret XLSX. |
| Rendering | Artifact Tool leser skrevne bøker for flerår, dokument201 og tomt/globalt. Forløp, nivåer, år, avgrenset regning, helinventar og globale hull inspiseres visuelt. |
| M25 | Ekte tidligere A/B/B6/B8/B9/T1/T2/T3 fra hovedmappens outputs eller hashfestet gammel B6-bok leses fra kontrollerte kopier. Originaler bevares. |
| M26 | Fire separate autentiske 368-forløp gjennom offentlig ordinær synkronisering/råbevaring/lagring/tolkning/Excel ved manglende, feilet, korrupt og motstridende T4. Tomt flerårsvalg uten historisk Excel. |
| M27/ressursvern | Analysefri adapter, uendret T3-årsvern, duplikatnøkkel/NaN/ukjent felt, JSON/payload/gzip/objekt/inventar/ZIP/XML-vern. Gamle 512-tak bevares; T3/T4 har 4096. |
| Statikk/fullsuite | Ruff check/format, mypy og hele testutvalget. Ingen testutvalg, gamle parser-/linjeskiftregler eller vern er redusert. Workflowens 40 minutter og parserversjonslogging består. |
| Orkestrator | Samlet Standards/Spec, separat audit på samme fryste kandidat, faktisk grønn full Linux-CI, autorisert publisering/merge og GitHub-overlevering gjenstår hos orkestratoren. |

Ingen lokal port lukker #10, #32 eller #37. Ingen neste ticket er startet.
