# Samlet Spec-review av T5/#62

**Ett P2-funn; Spec-porten er ikke bestått.** Ingen annen påvist kravmangel,
feilimplementering eller scope creep.

Fast kandidat `95ed8e60052d7731bb99386db572ba607c6b36a2`, tre
`225382d23bf776a8c9ee1a81a8d27de90e1b8620`, base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b`. Hele diffen, begge commits,
AGENTS, hele #62 med kommentar, T5-kontrakt, akseptmatrise og reproduksjon er
gjennomgått. Gamle reviewrapporter er historiske.

**[P2] Gjør manifestbindinger og replay uavhengige av lokal linjeskiftblanding.**
Krav #62: «Kontrollgrunnlaget må være tilgjengelig fra publisert historie eller
hashfestet kandidatarkiv; prøv reproduksjon i fersk klon.»
`reviews/integration/manifest.json:27–31` og øvrige oppføringer erklærer
`raw bytes`/Git-blob-hasher, men **40 av 54** bindinger avviker fra faktisk
kandidatblob; **9 av 18** i `security-fix/manifest.json` avviker også.
Eksempelvis normaliseres CRLF i `baseline-files.json` og `tests-38.log` til LF
i Git, mens manifestene binder lokale CRLF-byte. Kjerneleveransemanifestets
**35 av 35** bindinger stemmer med uttrykkelig angitt representasjon.
Det historiske stikartets fire originalarkiver stemmer; dette forklarer ikke
linjeskiftavvikene. `compare_evidence.py:125–137` sammenligner dessuten rå
arbeidsfiler mot historiske lokale byte: 365 av 1270 baselinebindinger avviker
fra Git-blobber. Egen `git -c core.autocrlf=false archive` av kandidaten og
replay med korrekt historisk d465-binding stopper konkret på
`AssertionError: .gitattributes`. Dette er en utført reproduksjonsfeil,
ikke ventestatusen for senere publisert-klon-port. Bevar historiske byte,
men gi eksporterte bevis og replay en eksplisitt etterprøvbar representasjon.

Egne kontroller bekreftet alle **111** felt mot bevart HTML, **105** nye,
**37/15**, **45** kontoangivelser, **123/6/2**, ekte 4400/2-null, identisk
T1-kapsel, separat historisk/gjeldende dekning, ni fullmaktspunkter, én IV-ramme,
åtte grenbevis og fortsatt ustrukturert 95/ukjent rettelseshistorikk.
Alle 45 kontoutvalg med begge returveier bestod. **14** eksisterende par ble
gjenlest; **tre** nye JSON/XLSX-par, begge CLI-opphav og offline bestod.
Tre endrede temaer passerte kapselkontrollen og ble avvist av T5-leseren.
**15 målrettede tester bestod**, inklusive ti rehashede semantikkangrep,
fire ordinære registreringsforløp og uavhengig typed innlesning.

Bevis: `.local/final-spec/{manifest-results,replay-representation,api-results}.json`
og `pytest.log`. Ingen ny primærkildehenting, rendering, fullsuite, GitHub-mutasjon
eller CI-/mergepåstand. Publisert fersk klon, øvrige uavhengige porter, full CI
og merge gjenstår hos orkestrator.
