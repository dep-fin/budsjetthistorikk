# B8: saksdokumenter og stikkord ved vedtaksbeløp

B8/#28 bruker Stortingets saks-ID fra en eksakt B2-revisjon. Saks-API-ets publikasjoner er metadata på saksnivå. Proposisjonen og innstillingen leses ikke inn som forslagstekst eller beløp. En lenke er en bevart metadatahenvisning, ikke dokumentert tilgjengelighet eller bevist postvis forslagstilknytning. Se [kildeprøven](research/b8/README.md), [kontrakten](datakontrakt.md#b8--separat-saksberikelse-og-frosset-v2) og [lagringsvalget](adr/0010-saksdokumenter-og-frosset-v2.md).

## Hent eller les en lagret saksrespons

Velg først vedtaksrevisjonen fra en B2-kjøring. Tolkningen av beløp velges fortsatt uttrykkelig, for eksempel:

```powershell
python -m innlesning synkroniser --database work/b8.sqlite --sesjon 2024-2025 --historisk-proeve --vedtak-id 40034048 --response tests/fixtures/b6/40034048.xml --metadata tests/fixtures/b6/40034048.json
python -m innlesning tolk --database work/b8.sqlite --revisjon <B2-revisjon> --tolkning storting-belop-v2
python -m innlesning saksdokumenter --database work/b8.sqlite --revisjon <B2-revisjon> --response tests/fixtures/b8/sak-100927.xml --metadata tests/fixtures/b8/sak-100927.json
```

Uten `--response`/`--metadata` henter siste kommando bare det faste offisielle endepunktet `https://data.stortinget.no/eksport/sak?sakid=<sak_id>`. `--timeout 30` er standard; 1–120 sekunder er tillatt. Ingen omdirigering eller automatisk gjenhenting skjer. Saks-ID-en kan ikke brukes som vilkårlig URL. Store responser avvises ved 32 MiB. Mottatt HTTP-feilinnhold innen grensen bevares med faktisk hash; timeout uten respons har ingen hash.

CLI returnerer `saksforsok` og immutable `saksberikelse`. Status `observert` gir returkode 0. Et lagret avvik/feilet forsøk gir 2 med feilgrunn og berikelses-ID, slik at et kontrolluttrekk fortsatt kan velge resultatet. Fil-/argument-/databasefeil gir 1. En saksfeil ruller ikke tilbake vedtak eller beløpsuttrekk. Det finnes ingen avhengighet til historisk Excel, historisk register eller startsaldo.

## Eksporter med uttrykkelig dokumentgrunnlag

En saksutvalgsfil inneholder `base` i eksisterende B6-format og `enrichment_ids`. Bruk de faktiske ID-ene fra kommandoene ovenfor:

```json
{
  "base": {
    "dataset": "prove",
    "session": "2024-2025",
    "inventory_job_ids": ["<B2-jobb>"],
    "extraction_ids": ["<v2-beløpsuttrekk>"]
  },
  "enrichment_ids": ["<saksberikelse>"]
}
```

```powershell
python -m analyse --database work/b8.sqlite --saksutvalg work/saksutvalg.json --excel work/sak.xlsx --json work/sak.json
```

Velg nye filnavn. `--json` er valgfri og skriver `b6-frozen-2`. Eksporten henter ingenting fra nettet og velger ingen nyeste berikelse automatisk. Hele inventaret vurderes før konto-/beløpsfiltre. Ikke valgt saksberikelse og nyere feil/forsøk blir synlige i dokumentavvik. Identitet, dokumentlenke, saksferskhet og vedtaksferskhet er separate felt. Historiske referanser forsvinner ikke etter en nyere feil.

Excel viser «Stikkord» rett etter «Post», formelt vedtak med sesjon, «Teknisk API-ID» og klikkbare innstillings-/proposisjonsnumre ved beløp og historikk. Flere dokumenter gir flere dokumentkolonner og relasjonsrader, aldri flere beløpsrader. `Saksdokumenter`, `Dokumentrelasjoner`, `Dokumentavvik` og `Stikkordgrunnlag` viser det separate grunnlaget. Lange råfelt følger eksisterende tekst-/videreføringsregler; utvid radhøyden for å lese lange JSON-/HTML-felt i Excel.

Det autentiske eksemplet viser 210 (2024–2025), API-ID 40034048, Innst. 81 S og Prop. 16 S. Kapittel/post 1429/1 har +5 796 000, fra 160 243 000 til 166 039 000; 1429/22 har −3 000 000, fra 32 185 000 til 29 185 000. Den siste har «kan overføres» i kursiv kildemarkering. 211 er en separat fullmakt om 1429/60 og gir ingen ekstra beløpsrad.

## Offentlige Python-grenser og gjenlesing

`innlesning.saksdokumenter` tilbyr `import_case_response`, `begin_case_attempt`, `save_case_response`, `fail_case_attempt`, `fetch_case_attempt`, `read_case_attempt`, `read_case_source`, `read_case_context`, `enrich_revision` og `read_enrichment`. Importen bruker `dataset` og `session` eksplisitt; en berikelse må ha samme datasett/sesjon/saks-ID som vedtaksrevisjonen. Et ventende forsøk med lagrede byte kan ferdigstilles med samme `save_case_response`-kall og identiske byte/metadata; det krever ikke ny HTTP. Andre byte eller metadata krever et nytt forsøk. Lesefeil i HTTP-feilinnhold gir et avsluttet feilforsøk som kan berikes. Tilgjengelige delbyte er eksplisitt merket som delrespons med faktisk hash; uten tilgjengelige byte finnes bare transportmetadata og feilgrunn.

`analyse.saksdokumenter` tilbyr `SaksSelection`, `saks_selection_from_dict`, `build_saks_report`, `report_to_json`, `report_from_json`, `export_saks_json`, `export_built_saks_excel` og `verify_saks_excel`. Et gjenlest v2-snapshot kan eksporteres selv når databasen er utilgjengelig. Eksportens databaseargument beskytter filbanen, men det frosne grunnlaget leses bare fra rapporten. Gamle `analyse.session_serialization` leser/skriver fortsatt bare `b6-frozen-1`; B7 beholder dette standardvalget.

Ingen ny aktivering eller faglig godkjenning utføres. Manglende start og de dokumenterte historiske kjedekonfliktene består. #10s utsatte driftsaksept er uendret.
