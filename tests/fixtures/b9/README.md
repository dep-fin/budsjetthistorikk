# B9: uforandret arbeidsbok fra den opprinnelige B8-skriveren

Dette er en **syntetisk kompatibilitetsprøve**, ikke en ny Storting-kilde eller et nytt faglig resultat. Arbeidsboken er produsert med hele, uendrede `analyse/saksdokumenter.py` fra commit `a7fc7d9996733dcaa73589c2fa8a3906059b4413`, lastet i minnet med `git show`. Modulens kildebyte har SHA-256 `4c1874cc31dee9f2211d1ef5d999d3a4a0cc6f173717148dd15851ebe7d20b1d`. Originalens offentlige `export_built_saks_excel` og `verify_saks_excel` bestod. Arbeidsboken er ikke laget ved å omdøpe eller redigere en B9-eksport.

Grunnlaget er det tidligere leverte frosset-v2-snapshotet for vedtak 210, SHA-256 `2d855c97abf6af30e6eb64817bfc50778f5f7ffb7deee56362ff8caf1e908cbe`. Bare post 1 beholdes i de valgte radene og de ufiltrerte radene. Hver av de tre beløpsobservasjonenes `pointer.raw_record` erstattes med den uttrykkelig syntetiske teksten `"syntetisk raatekst " * 2500`, globale beløpsavvik tømmes og rapport-ID beregnes på nytt ved den offentlige frosset-v2-grensen. De opprinnelige kildeutdragene og saksmetadataene er allerede dokumentert under [B6](../b6/README.md) og [B8](../b8/README.md).

| Fil | Byte | SHA-256 |
| --- | ---: | --- |
| `legacy-b8.xlsx` | 39 735 | `aff0035fbda3e8ec0ea4b8cc36628c835fed08bf2d0392a17ca5885d66cb597b` |
| `legacy-b8.json.gz` | 17 098 | `aeb256ea3c382cf8532da9587aa9f090d6658d62ee93b9f060e93f7d8070da62` |
| Utpakket JSON, ikke lagret separat | 351 294 | `838aed96d7a4c1a42530e1d788245a838da051c2cdd552acb37d061d404fdd02` |

JSON har konvoluttformat `b6-frozen-2` og rapport-ID `0444f32ef14c71f1cf1eae0ba17c8aa7fff2bf3a402358a4c4fdec82eaef4d7f`. Komprimering bevarer hele snapshotet uten en stor repetert råtekstfil i repoet. [Manifestet](legacy-b8.manifest.json) binder filene og genereringsgrunnlaget. CI leser de uforanderlige filene, kontrollerer byteantall/hash, pakker ut JSON og bruker den offentlige rapportleseren og Excel-kontrollen. Verken Git, nettverk, database eller opprinnelig brukerleveranse trengs under testen.

Original B8 skrev `Historikk!AB2` i videreføringsarket før de seks dokument-/stikkordkolonnene ble satt inn. Selve feltet `Lokatorer` finnes derfor i `Historikk!AH2`. Den nye kontrollen må kjenne akkurat denne gamle pekerregelen når den detaljerte B8-visningen leses. B9s `Historikkdetaljer` skal fortsatt kreve den flyttede pekeren. Begge må avvise endret videreført tekst, delnummer, rekkefølge, peker, arkstruktur og formeltyper.

Generering gjentas bare eksplisitt med et **nytt** målnavn, fra repoets rot. Det innsjekkede komprimerte snapshotet er tilstrekkelig; den opprinnelige brukerleveransen trengs ikke:

```powershell
python -m tests.create_b9_legacy_fixture tests/fixtures/b9/legacy-b8.json.gz work/ny-b8-fixture
```

[Generatoren](../../create_b9_legacy_fixture.py) bruker prosjektets godkjente openpyxl-eksport, ingen nettinnhenting eller binær etterredigering. ZIP-tidsstempler fra openpyxl kan gi andre arbeidsbokbyte ved en ny generering. Hashene ovenfor gjelder den innsjekkede filen; snapshotets innhold og opprinnelige pekerregel er faste. Ingen opprinnelig leveranse eller kildefixture overskrives.
