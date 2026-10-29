# T5/#62: uavhengig prøve fra fersk GitHub-klon

30. oktober 2026. Prøven består for publisert produktkandidat
`a08fc28dc33fa4244814dc29fbeeb5b87d4e804d`, tre
`1f32d2e81f8ff76fb3365d9c0fa6592fbb64eb39`.
Dette er en avgrenset reproduksjonskontroll før PR/full CI. Den attesterer
ingen CI, merge, ny rendering eller native Excel. Ingen produktretting,
staging, commit eller GitHub-skriving er utført av kontrolløren.

## Uavhengig anskaffelse og objekter

Klonen ble opprettet i en ny mappe:
`work/t5-prop16/.local/fresh-github-20261030`, relativt til hovedarbeidsområdet.
Den eneste Git-kilden var `https://github.com/depmartin/budsjetthistorikk.git`:

```powershell
git -c core.autocrlf=false clone --no-local --single-branch --branch codex/t5-prop16 https://github.com/depmartin/budsjetthistorikk.git .local/fresh-github-20261030
```

Første nettverksforsøk feilet med DNS-feil i sandboxen. Samme kommando med
autorisert nettverksescalering fullførte. Ingen bundle, lokal klonekilde,
references, alternates eller kopierte gamle Git-objekter ble brukt.
`.git/objects/info/alternates` finnes ikke. Ingen gamle `.local`-eksporter,
kontrollprogrammer eller resultatfiler ble importert fra kildearbeidsflaten.
Python og installerte avhengigheter ble lest fra de tillatte runtime-/C06-
mappene; produktkode, hjelpere og originaler kom fra GitHub-klonen.

[identity.json](identity.json) fører faktiske remote-/configverdier, foreldre,
trær og `git cat-file`-utfall. Følgende sammenheng ble kontrollert:

| Historisk lokal kandidat, bare alias | Faktisk publisert commit | Faktisk tre |
| --- | --- | --- |
| `d46589cb9e99338e44fc805ee9882006ba657fd0` | `4ddda7953431ac9f6ae861d800a33229121e54db` | `df0eed6d6e8a0b2a07962e641ae05d1194a3304d` |
| `95ed8e60052d7731bb99386db572ba607c6b36a2` | `ea91dc9c7a30c55e7a5f9c75b7381fc7a2d33d11` | `225382d23bf776a8c9ee1a81a8d27de90e1b8620` |
| `cd240e3b2f4846081d1f658faf0caec9cf4a7186` | `a08fc28dc33fa4244814dc29fbeeb5b87d4e804d` | `1f32d2e81f8ff76fb3365d9c0fa6592fbb64eb39` |

De tre publiserte commitene danner én direkte foreldrekjede fra base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b`. Alle tre ancestry-prøver
bestod. Alle tre lokale kandidat-SHA-er mangler i klonen: hver
`git cat-file -e SHA^{commit}` returnerte 128. Disse lokale navnene ble
aldri hentet eller opprettet som erstatningsobjekter.

Hele #62 med begge kommentarer, AGENTS, arbeidsflyt, T5-kontrakt,
reproduksjonsveiledning og kilde-/integrasjons-/bytebevaringsgrunnlaget ble
lest. Lesingen av publisert materiale ga ingen grunn til ny kildehenting.

## Faktisk produkt- og kildeprøve

Fra kloneroten ble den publiserte leveransehjelperen kjørt med faktisk head
og base:

```powershell
python -m ops.proposisjon16_proeve --root . --output .local/fresh-exports --base 2f4ee30c9d8074076fc8042e208c4a4b6345db6b --candidate a08fc28dc33fa4244814dc29fbeeb5b87d4e804d
```

Returkode 0 etter 117,094 sekunder. Den genererte, lukket og gjenleste
14 nye JSON/XLSX-par: dokument, utgift, inntekt/null, tekst, flere kontoer,
tomt, begge 1429-poster hver for seg og sammen, 1533-kontekst og begge
navigasjons-/returretninger. [fresh-export-control.json](fresh-export-control.json)
fører feltfasit, originalceller, locators, kilder, fullmakter, grenbevis,
utvalg og faktiske filhasher. [core-execution.json](core-execution.json)
fører eksakt kommando/runtime og [core.log](core.log) faktisk utfall.

Offentlig CLI ble deretter kjørt både med utpakket autentisk T1 og med et
nettopp generert T5-frosset dokument. T1-veien valgte `4400/2` i 2024 og
ga tre felt. Frosset-veien åpnet `prop16` med en kilderot som ikke finnes,
ga 111 felt og eksporterte originalene. Begge skrev ekte JSON og XLSX;
en separat kontroll gjenleste begge og bekreftet samme basis. Eksakte
kommandoer ligger i `cli-*-execution.json`; resultatene ligger i
[public-api-checks.json](public-api-checks.json).

Kontrollen bekrefter **111 forslagfelt / 105 nye felt / 37 grupper / 45
kontoangivelser**, global union **123 felt / seks vedtaksfelt / to monetære
hendelser**, full objekt- og JSON-likhet for gammel T1-basis og fortsatt
`delvis_1429` i gammel dokumentpost. `4400/2` har heltallsnull, også som
numerisk Excel-celle G4. IV har én delt 16 300 000-kronersramme, og 1533/45
har ingen ny grenlekkasje. Alle **25 originalpayloads** ble kontrollert med
byteantall/SHA-256 og sammenlignet byte for byte med begge ferske
originaleksportene: API-hjelperens og offline-CLI-ens.

Den publiserte uavhengige `reviews/source/independent_check.py` ble også
kjørt på en ny `git archive` av publisert historisk `4ddda795…` med dette
kandidatnavnet og samme base. Den direkte DOM-/originalkontrollen fullførte
med **111 felt, 45 kontoer, 16 faktiske filpar, 25 originaler og 35
manifestfiler**. [independent-source-control.json](independent-source-control.json)
er denne ferske kontrollens utdata. Første forsøk nådde siste dokumentarskriving,
men den gamle kandidaten manglet `reviews/source`-mappen. Første feil/logg
er bevart; etter opprettelse av bare denne outputmappen fullførte samme
uendrede publiserte hjelper. Andre forsøk brukte bare filene generert i
første ferske forsøk.

## Manifest, historisk replay og tema

[manifest-checks.json](manifest-checks.json) fører kontroll mot både faktiske
publiserte Git-blobber og checkoutbyte:

- **35/35** opprinnelige leveransebindinger består.
- **18/18** security-fix-bindinger og **54/54** integrasjonsbindinger består.
- Alle **49** dokumenterte gamle manifestavvik gjenfinnes i `ea91dc9c…`,
  stemmer med den publiserte førbindingen og er nøyaktig gjenopprettet i `a08fc28d…`.
- Alle **47** historiske `preserved-before`-bindinger består med de fire
  uttrykkelig publiserte `.original`-arkivstiene. Gamle hasher er beholdt.

Den uendrede publiserte `replay_helpers.py` ble kjørt med
`--candidate 4ddda7953431ac9f6ae861d800a33229121e54db`, publisert base,
ny workspace `.local/fresh-helper-work` og ny output
`.local/fresh-helper-ledgers`. Alle **åtte** original-/integrert-prosesser
returnerte 0. [helper-replay/executions.json](helper-replay/executions.json)
har hver kommando, hjelperhash, tid og returkode. De ferske prober og
etterkontroller har begge **70 prober, 69 beståtte og bare dokumentert
historisk `theme_integrity`-aksept**. D465-tilsvarende produkt er dermed
fortsatt historisk sårbart; replayet er ingen ny sikkerhetsaksept.

`compare_evidence.py` mot en uendret a08-arkivkopi feilet som dokumentert på
`.gitattributes`; [compare-before.log](compare-before.log) er bevart.
Den publiserte additive **344-mappen** ble så anvendt bare på den isolerte
kopien. **342** filer trengte LF→CRLF; to CSV-filer hadde allerede riktig
representasjon. Alle 344 sluttbindinger traff historisk råfasit.
[replay-materialization.json](replay-materialization.json) dokumenterer hver sti.

Samme uendrede sammenligner, samme publiserte refs og de **ferske** replay-
ledgerne/XLSX-filene returnerte deretter **0**: **1270** bevarte bindinger,
fire arkiver og like utfall i alle fire ledgertyper. Ingen gamle absolutte
`.local`-filer fra leveransearbeidsflaten ble brukt.
[comparison/replay-comparison.json](comparison/replay-comparison.json) og
[comparison/generated-xlsx-comparison.json](comparison/generated-xlsx-comparison.json)
fører de faktiske sti-/tempnavn-/ZIP-/tidsunntakene. Produktkapsel, tema,
stiler og kontrollutfall er ikke utelatt fra sammenligningen.

Den **eksakte a08-Git-bloben** som aktiv leser avviser alle tre ferske
temaangrep: hvit sRGB, hvit systemfarge og endret minor-font.
[current-theme.json](current-theme.json) binder leserhash og avvisninger.
Den opprinnelige publiserte `security-fix/probe.py` avviste også angrepene,
men stoppet deretter på en historisk hjelperbinding på den gamle stien;
den er ikke tilpasset det senere arkivkartet. Dette feilforsøket er bevart.
Den samme uendrede proben fullførte på en separat a08-arkivkopi med
344-representasjonen og de fire publiserte hjelperoriginalene lagt på sine
historiske stier: ett ferskt gyldig filpar, én ny gyldig eksport, tre
temaavvisninger og alle 47 historiske bevaringsbindinger.
[theme-retargeted-results.json](theme-retargeted-results.json) fører dette.
Produktmodulene ble ikke erstattet; bare historiske kontrollhjelpere og
den eksplisitte arbeidsrepresentasjonen ble materialisert i tempkopien.

## Bevisgrense og videre port

Prøven krevde ingen utilgjengelig lokal kandidat eller gammel eksport.
De konkrete historiske setupkravene og alle reelle feilforsøk er synlige i
[failed-attempts.json](failed-attempts.json) og råloggene. Det gjenstår ingen
blokkering for denne avgrensede ferskklonprøven. Full CI og bekreftet merge
gjenstår hos orkestrator.

Alle sporede filer i den ferske klonen er rene etter kjøringen.
[summary.json](summary.json) fører sluttstatus, runtime, observeringstid og
kontroll av at produkt-/test-/ops-blobber er uendret mellom ea91 og a08.
Midlertidige kontrollprogrammer er bevart som **dokumentarisk JSON-tekst**
i [temporary-control-transcripts.json](temporary-control-transcripts.json);
ingen nye kjørbare filer er levert i kildearbeidsflaten. Bare nye bevis
under denne mappen er skrevet dit. Ingen fullsuite eller rendering er
gjentatt, og denne rapporten påstår ingen utvidet årsdekning, T6 eller drift.
