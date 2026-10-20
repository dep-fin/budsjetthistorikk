# Datakontrakt v1 – ett valgt originalvedtak

Kontrakten ligger i `innlesning/model.py`. Innlesningens offentlige grense er `import_saved(database, raw_response, metadata, decision_id, historical_sample=False)`, `read_report(database, run_id)` og `read_source(database, sha256)`. Nettadapteren `fetch_session(session, timeout=30)` leverer råbyte og hentemetadata. Eksportgrensen er `analyse.export_excel(database, run_id, output)`.

## Kilde, identitet og struktur

SQLite-tabellen `sources` lagrer faktisk innlest respons som BLOB, identifisert med SHA-256. `runs` lagrer kjørings-ID, kildehash, komplette medsendte hentemetadata, kontrollstatus, full vedtakstekst og metadata for valgt vedtak. `allocations` lagrer postrader med kobling til kjøringen. Råbyte og resultat skrives i samme transaksjon. `read_source` returnerer de samme bytene som faktisk ble lest inn.

Hentemetadata krever `url`, `retrieved_utc` med tidssone, HTTP-`status=200`, `sha256` og `bytes`. Hash og byteantall valideres før import. `headers` bevares når de er oppgitt. `fixture_kind=http_original` betegner en hel HTTP-respons; eldre metadata uten dette feltet behandles som originalrespons. `derived_excerpt` og `synthetic_test` er uttrykkelige prøveslag. Proveniens og foreldrehash for den autentiske fixturen finnes i sidevognen. Prøvens hash erstattes aldri av foreldrefilens hash.

Valgt vedtak har original ID, nummer, sak-ID, sesjon fra XML-responsen, rå datoverdi, vedtaksdato, API-type, tittel, rå og normalisert kildelenke og hele HTML-feltet. Datoen viser en kalenderdato; kildens midnattstid tolkes ikke som faktisk vedtakstidspunkt. Budsjettår leses fra den uttrykkelige innledningen og holdes adskilt fra sesjon.

Hver postrad har rå kapittel-/postidentitet, kapittelnavn, formål, beløpstekst, heltall i kroner eller `None`, retning, beløpsbetydning, kilderad, kontrollstatus, begrunnelse og radens HTML. Kildepekeren `table[1]/tr[n]` teller fra 1 og inkluderer overskriftsraden. Linjens øvrige vedtaksmetadata følger fra det tilhørende vedtaket i rapporten.

Beløpsbetydningen i denne grensen er **opprinnelig bevilgning**, et nivå for budsjettåret. Endringsbeløp, førbeløp og etterbeløp er ikke relevante og eksporteres som tomme felt. Retning følger kapittel: 1–2999 utgift og 3000–5999 inntekt. Ukjent kapittel gir kontrollbehov. Departement og Gul bok-gruppe utledes ikke; departementstilknytning står uttrykkelig som uavklart i Excel.

## Status og summer

- `strukturert`: det avgrensede originaltabellmønsteret er gjenkjent, postbeløpene er entydige, alle innholdsrader er klassifisert og de to kilde-totalene stemmer.
- `til kontroll`: valgt vedtak og råtekst er bevart, men mønster, beløp eller kontrollgrunnlag er uavklart. Entydige delrader kan bevares. Rapportens `approved_totals` er `None` for begge retninger, og Excel viser ufullstendig grunnlag.
- `innlesningsfeil`: valgt vedtak mangler, XML er ugyldig, tekst mangler eller identitet/sesjon ikke stemmer. Mottatte råbyte og kontrollgrunnen bevares når proveniensen er gyldig. Ugyldig proveniens, transportfeil og for stor respons avvises før import og gir CLI-feil.

`strukturert` gjelder struktureringen av valgt vedtak. Statusen godkjenner verken departementstilknytning, andre vedtak eller en additiv historikk. Kildens totalrader er kontrollopplysninger i `source_totals`; de blir aldri ekstra postbevilgninger. Manglende og tvetydige beløp er `None`, mens et uttrykkelig tall 0 er null kroner.

## Bruksgrense

Eksporten leser bare én eksplisitt kjørings-ID. Hver ny import får en ny kjøring; gjentatte importer skal ikke summeres sammen. B2 skal håndtere løpende synkronisering og kilderettelser før et samlet uttrekk tilbys. Det finnes ingen automatisk «siste gyldige versjon» i B1.

Bare den dokumenterte originaltabellen er kontrollert. Ukjent tabelloppsett, flere tabeller, uklassifisert innhold eller manglende enhet gir kontrollbehov. Generell behandling av underposter, fullmakter, regjerings-/komitéforslag og senere endringsvedtak er ikke implementert. Produksjonsgrensen er fortsatt sesjon 2026–2027; historiske prøver krever et uttrykkelig valg.
