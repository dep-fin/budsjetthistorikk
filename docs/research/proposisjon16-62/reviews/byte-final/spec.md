# Spec-etterkontroll av T5/#62

**BESTÅTT: 0 funn. Det tidligere leveranse-P2 er lukket på kandidaten.**

Kandidat `cd240e3b2f4846081d1f658faf0caec9cf4a7186`, tre
`1f32d2e81f8ff76fb3365d9c0fa6592fbb64eb39`, base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b`.
AGENTS, arbeidsflyt, hele #62 med begge kommentarer, T5-kontrakten, tidligere
Spec-/kilde-/sikkerhetsrapporter og byte-preservation/README er gjennomgått.

Egen kontroll av faktiske kandidatblobber bekrefter **35/35** kjernebindinger,
**18/18** security-fix, **54/54** integrasjon, **47/47** historiske
bevaringsbindinger med fire eksplisitte originalarkivsubstitusjoner,
**17/17** nye bevisbindinger og **25/25** kildebindinger.
Alle **49** tidligere manifestavvik er nå eksakte råblobber; alle **104** gamle
kontrollfiler stemmer. De **62** endrede gamle blobene er utelukkende de
dokumenterte CRLF-restaureringene. Egen faktisk `hash-object --path` med
`autocrlf=true/false` bestod **98/98**. Ingen manifest er omskrevet.

Krav #62: «Kontrollgrunnlaget må være tilgjengelig fra publisert historie eller
hashfestet kandidatarkiv; prøv reproduksjon i fersk klon.»
Egen `git -c core.autocrlf=false archive --format=zip cd240e3b2f4846081d1f658faf0caec9cf4a7186`
ga arkiv-SHA-256 `9303b7563561d2db2c0a27ce14dd12989c4e6f234c136ae81ed151b5894c6bf4`.
Replay ble kjørt i separat initialisert repository med privat indeks og
lesende alternates. Ny historisk kandidatidentitet
`3aea348f101b2a132d4c65de1e9fdfe42c8d7c36` har d465-treet; ny baseidentitet
`672feda53a6a0ee7fe8dfadbbad7cdcd82e7d442` har basetreet.

`replay_helpers.py` genererte åtte ferske original-/integrert-ledgere og
XLSX-artefakter; alle prosesser returnerte **0** med disse retargeterte refs.
Umaterialisert `compare_evidence.py` feilet fortsatt på `.gitattributes`.
Det additive kartet verifiserte **344** bindinger og materialiserte **342** filer
bare i replaykopien. Uendret sammenligner returnerte deretter **0**:
**1270** historiske bindinger bevart, fire ledgertyper like etter dokumenterte
sti-/tids-/ZIP-unntak. Ingen gammel lokal XLSX-output ble gjenbrukt.

Kommando: `python .local/byte-final-spec/probe.py`, med mandatets bundled runtime.
Eksakte underkommandoer/utfall finnes i `.local/byte-final-spec/replay-runs.json`
og `fresh-ledgers/executions.json`; øvrige egne bevis er samme sted.

Produkt, tester, kilder, gamle guardprofiler og visuelle bevis er blobidentiske
med 95ed. **1181/1183** basefiler består; bare de to additive kontekstpekerne
avviker. Egen kald gjenlesning bekreftet lik JSON/XLSX, autentisk T1-kapsel,
105 nye/123 samlede felt og ekte 4400/2-null med nett/database sperret;
tre temaangrep ble avvist. Tidligere funksjons-/kilde-/visuell aksept beholder
dermed sine forutsetninger. Ingen ny fullsuite eller rendering.

Kildeindeksen var uendret. Publisert fersk klon med nødvendige historiske
trealiaser, øvrige uavhengige porter, full slutt-CI og bekreftet merge gjenstår.
Denne lokale porten attesterer ingen av disse leveringsportene.
