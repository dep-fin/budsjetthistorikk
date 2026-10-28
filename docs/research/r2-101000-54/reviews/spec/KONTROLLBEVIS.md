# Kontrollbevis og reproduksjon

Kontrollen gjelder bare kandidat `7af3153bda95726ac93d0780b918ae95440bae2d`
mot `6b2441ee5e859d103ab44d78f12d33c374a89171`. Egne filer er skrevet bare
i denne katalogen. Ingen original, byggerfil eller tidligere kontrollrapport
er endret; ingen Git-/GitHub-mutasjon er utført.

- [independent-results.json](independent-results.json) binder alle 64
  kandidatfiler med størrelse/SHA-256, 274 kontroller, målrettet F1-belegg,
  alle 60 opprinnelige kontrollpassasjer, transportfelt, 12 kryssreferanser
  og uendrede produkt-/K3-/P1-trær.
- [live-context-comparison.json](live-context-comparison.json) dokumenterer
  samsvar med GitHub-koblingens ferske, komplette issue-/kommentarlesinger.
  #37/#54 var åpne; #50/#52 var lukket. Tidligere P1-fullføring er kontekst,
  ikke CI-bevis for #54.
- [builder-replay.json](builder-replay.json) er faktisk ny kjøring av
  reproduksjonens kodeblokk med kandidat-SHA: 818 bestått/0 feil.
  [replay_builder_check.py](replay_builder_check.py) er den samme logikken,
  kun formatert for at kontrollartefakten skal følge repoets Ruff-regler.
- [source-replay.json](source-replay.json) er ny kjøring av kandidatens
  `../source-control/verify_sources.py`, med output omdirigert hit i minnet.
  Skriptet selv og den tidligere kontrollens `results.json` er uendret.
  Ny kjøring: 204 bestått, 27 kildebindinger, to O1-originaler, 60 passasjer,
  fire PDF-sider. Dette er gjenkjøring av en publisert kontroll, ikke en
  påstand om en ny, uavhengig implementert full kildekontroll.
- [verify_spec.py](verify_spec.py) er egen implementert etterkontroll.
  Den gjenleser originaloverskrift/råcelle, sammenholder rettede påstander,
  kontrollerer komplett publisert Prop.34-kapittelliste, kandidatblobber,
  tidligere kontrollbevis og eksplisitte rollegjerder.

Fra reporoten med Python/lxml/pypdf:

```powershell
python -X utf8 docs/research/r2-101000-54/reviews/spec/replay_builder_check.py 7af3153bda95726ac93d0780b918ae95440bae2d
python -X utf8 docs/research/r2-101000-54/reviews/spec/verify_spec.py
```

`verify_spec.py` leser de lagrede gjenkjøringsresultatene og skriver bare
`independent-results.json` i egen katalog. Følgende Python-kode gjentar
den publiserte kildekontrollen uten å overskrive dens opprinnelige resultat:

```python
import importlib.util
import sys
from pathlib import Path

path = Path("docs/research/r2-101000-54/reviews/source-control/verify_sources.py")
spec = importlib.util.spec_from_file_location("r2_source_replay", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = Path("docs/research/r2-101000-54/reviews/spec").resolve()
sys.argv = [str(path), "--raw-root", "docs/research/r2-101000-54/originals"]
module.main()
(module.HERE / "results.json").replace(module.HERE / "source-replay.json")
```

Kjørt med bundlet Python 3.12.14, lxml 6.1.1 og pypdf 6.10.0. Ruff 0.11.0
ble brukt fra P1s eksisterende lokale modulmappe; ingen installasjon eller
oppgradering. Egen kode ble formatert og kontrollert etter kjøringen.

Tre innledende kontrollselefeil ble rettet i egne filer: råcellen har
kantmellomrom som må strippes uten å normalisere det indre harde
mellomrommet; full kapittelliste ligger på `prop34-ch1.html` snarere enn
inngangssiden; Python-output måtte kjøres med UTF-8. Disse var ingen
kandidatfeil og er ikke telt som beståtte kontrollkjøringer.

Kontrollen autentiserer ikke råkildene mot en ny HTTP-henting. Dokumentenes
bevarte transportopplysninger og observerte versjoner er grunnlaget. Den
visuelle PDF-presentasjonen, faktiske ansatte, FINs konkrete fullmaktsbruk,
andre R2-saker, årsdekning, faglig saldo og drift er utenfor.
