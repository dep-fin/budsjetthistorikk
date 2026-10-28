# Separat sikkerhetsaudit av R2/#54

Det er ikke funnet nødvendige sikkerhetsrettinger i den undersøkte kandidaten.
Konklusjonen gjelder den avgrensede forskningsleveransen og de bevarte,
hashkontrollerte kildefilene. To valgfrie forbedringer er omtalt nedenfor.

## Kandidat og mandat

Auditten gjelder hele forskjellen
`6b2441ee5e859d103ab44d78f12d33c374a89171...7af3153bda95726ac93d0780b918ae95440bae2d`,
inkludert committene `c61dcc7c9221aa485a764c954323e0aac25b9e82` og
`7af3153bda95726ac93d0780b918ae95440bae2d`. Kandidatens tre er
`ab1ff41bb3c9ea7ee310418abec82efcbe6d00c0`.

Alle 64 endrede filer er bundet til Git-blobben med SHA-256 og byteantall i
[candidate.json](candidate.json). Forskningsfilene er kontrollert byteidentisk;
de to pekerdokumentene er sammenlignet som UTF-8/LF, som angitt i leveransen.
Alle filene har Git-modus `100644`. Ingen symlenker eller kjørbare filmoduser
inngår. Auditens egne filer er senere tilført dokumentasjon og inngår derfor
ikke i kandidatens 64 filer.

Grunnlaget er gjeldende AGENTS, arbeidsflyten, issue-tracker-reglene og hele
[#54 med kommentarer](https://github.com/depmartin/budsjetthistorikk/issues/54),
lest 28. oktober 2026. Issuet hadde ingen kommentarer ved kontrollen.
Forskningsrapporten, manifestene, transportfilene, reproduksjonskoden og hele
`reviews/source-control/verify_sources.py` er gjennomgått. Kildeagentens
rapport eller byggerens kontrollresultat er ikke lagt til grunn som utført
sikkerhetsaudit.

## Kontroller og resultat

[audit_checks.py](audit_checks.py) og [checks.json](checks.json) dokumenterer
696 beståtte kontrollpunkter og ingen feil. Kontrollene ble kjørt offline på
Windows med Python 3.12.14, lxml 6.1.1, libxml 2.11.9 og pypdf 6.10.0.

- Alle 22 nye gzip-arkiver, tilhørende transportfiler og dekomprimerte
  innhold er kontrollert mot manifestets SHA-256 og byteantall. Hvert arkiv
  ble først kontrollert med begrenset dekomprimering, maksimalt 32 MiB,
  og krav om ett fullført gzip-medlem. Totalt innhold er 6 229 295 byte;
  største nye innhold er 2 735 346 byte. De 19 gjenbruksfilene har også
  riktige hasher og størrelser; største gjenbrukte innhold er 7 479 943 byte.
- Alle faktiske filreferanser i kilde-, gjenbruks-, leveranse- og
  sammenligningsmanifestene samt evidensens kildekart holder seg innenfor
  repoet. Manifestfeltene brukes til lesing og sammenligning. Ingen
  manifestverdi styrer en skrivebane eller shellkommando.
- Alle nye kilde-URL-er bruker HTTPS til `www.regjeringen.no`,
  `www.stortinget.no` eller `data.stortinget.no`. De komplette svarene har
  registrert GET, HTTP 200, TLS-verifikasjonsresultat 0 og ingen opplasting.
  DNS-feilen har tomt innhold og blir ikke behandlet som et dokument.
- De 22 transportfilene har ingen cookie-, autorisasjons-, token- eller
  hemmelighetshenvisende headernavn. URL-brukernavn og URL-passord er tomme.
  URL-parametrene beskriver dokument-, kapittel-, saks- eller voteringsvalg.
  Responsenes `Request-Context`-app-ID-er og relative CSP-rapportmål er også
  gjennomgått. Ingen autentiseringsopplysning er påvist. Søk i alle
  kandidatfiler, også dekomprimerte kilder, fant ingen av de kontrollerte
  mønstrene for private nøkler, GitHub-/Slack-token eller AWS-tilgangsnøkler.
- XML-parsing bruker uttrykkelig `resolve_entities=False` og
  `no_network=True`, jf. kildekontrollskriptets linje 98–101 og
  reproduksjonskodens `parse_xml`. De nye XML-kildene har ingen DTD- eller
  entitetsdeklarasjoner. En liten prøve med en intern entitet bekreftet at
  entiteten beholdes uløst. Ingen ekstern ressurs ble brukt i prøven.
- HTML, også indre HTML fra XML-felt, behandles som trær av lxml. Bibliotekets
  tilgjengelige parserdokumentasjon angir `no_network=True` som standard.
  Ingen browser, JavaScript-motor, XSLT, eksterne XPath-funksjoner eller
  innlasting av lenkede ressurser brukes. HTML-fragmenter skrives som
  JSON-strenger; kandidaten har ingen visningsflate som setter dem inn som
  aktiv HTML. Råkildenes script- og ressurslenker blir liggende i gzip-arkivene.
- PDF-en er lest fra minne med pypdf. Alle 76 registrerte PDF-objekter er
  inspisert for de oppgitte aktive dictionary-nøklene. Ingen JavaScript-,
  tilleggshandlings-, Launch-, EmbeddedFiles- eller RichMedia-nøkkel ble
  funnet. Dokumentets `OpenAction` er en lokal `/GoTo` med `/Fit`.
  Fire sider gir tekstuttrekk. Ingen PDF-handling eller lenke ble aktivert.
- Begge publiserte kodeinnganger er kontrollert for dynamisk kodekjøring,
  utrygg deserialisering, shellbruk og produktimport. Ingen slik inngang er
  funnet. Kildeinnhold går til parserne og sammenligninger. `subprocess`
  brukes med argumentlister til Git-lesekommandoer. Reproduksjonskoden
  skriver resultatet til standard output; kildekontrollskriptet skriver
  én fast `results.json` ved siden av seg selv, jf. linje 623–625.
- Hele kildekontrollskriptet er kjørt på nytt mot kandidatens publiserte
  `originals/`. Bare konstanten for resultatmappen ble omdirigert til denne
  auditmappen etter innlasting; skriptets fil og kontrollfunksjoner er
  uendret. Python-socketoperasjoner var sperret, subprocess-kall var
  begrenset til Git-lesekommandoer, og filskriving utenfor auditmappen ble
  avvist. Kjøringen skrev bare `results.json` og bestod alle 204 egne
  kontroller. [Det nye resultatet](results.json) binder kandidatens HEAD,
  skripthash, 27 kilderepresentasjoner, to O1-kontekstkilder og 60 passasjer.
- Produktkode, tester, CI, avhengighetsfiler og K3/P1-trær er uendret mot
  basen. De nye kunnskapspekerne innfører ingen import eller produktadopsjon.
  Ingen installasjon, dependency hook, nettjeneste eller automatisk
  oppdateringsmekanisme er tilført. Ruff 0.11.0-kontroll og formatkontroll
  består for auditens eget skript.

## Nødvendige funn

Ingen. Det er ikke påvist en realistisk vei fra kandidatens faste kildeinnhold
til kodekjøring, vilkårlig filskriving, nettinnhenting eller utlevering av
autentiseringsopplysninger i denne forskningsleveransen.

## Valgfrie forbedringer

**V1 – Avgrens dekomprimeringen før eventuell generell gjenbruk.**
`verify_sources.py` linje 46–55 dekomprimerer hele filen før arkivhash og
størrelse blir kontrollert. Reproduksjonskodens `body()` og gzip-løkker har
samme ressursbegrensning. De faktiske arkivene i kandidaten er uavhengig
hashkontrollert og små, og verktøyene er dokumentert som offlinekontroll av
denne leveransen. Dette krever derfor ingen retting av #54. Dersom kode eller
`--raw-root` senere brukes mot vilkårlige filer, bør arkivbinding kontrolleres
før parsing, og dekomprimering bør ha en fast bytegrense. Leseomfang og
PDF-ressursbruk bør da også begrenses. Manifeststier og revisjonsargumentet i
reproduksjonen forutsetter tilsvarende et betrodd lokalt kontrollgrunnlag.

**V2 – Vurder dataminimering av maskinfelt ved senere innhenting.**
`transport.filename_effective` forekommer i alle 22 nye sidevogner og
`transport.local_ip` i 21. Eksempel er `prop34-ch1.html.meta.json` linje 14
og 19. Disse feltene røper lokal katalog-/brukerkontekst og intern
nettverksadresse, men gir ingen påvist autentiseringstilgang. En fremtidig
innhenter kan skille rå transportbevis fra et publiserbart utvalg av
proveniensfelter. Bevarte sidevogner og deres hashbindinger bør ikke
overskrives som en udokumentert opprydding.

## Reproduksjon og bevisgrenser

Fra reporoten med ovennevnte bibliotekversjoner:

```powershell
python docs/research/r2-101000-54/reviews/security/audit_checks.py
```

Kommandoen krever at HEAD fortsatt er den fastlåste kandidaten. Den skriver
bare kontrollbevis i denne mappen. [candidate.json](candidate.json) binder
hele kandidatdifferansen; [checks.json](checks.json) binder auditens skript
og faktiske kjøring. Kontrollresultatet fra kildeagenten er bevart uendret
i `reviews/source-control/`.

Dette er en defensiv gjennomgang av en konkret forskningsleveranse. Den
omfatter ingen destruktive prøver, nye HTTP-hentinger av råkilder, generell fuzzing,
operativsystemisolasjon av native parserkode eller uttømmende søk etter
hemmeligheter. Python-sperrene er observasjons- og avgrensningskontroller;
de er ikke en generell sandbox for vilkårlig kode. Engangshjelpere i ignorert
`.local/` inngår ikke i den publiserte kandidaten og er ikke revidert her.

Avhengighetsfiler er uendret og pinner blant annet lxml 6.1.3 og pypdf 6.10.0.
Den bundlete kontrollkjøringen brukte lxml 6.1.1, som dokumentert i
leveransen. Auditten har ikke installert avhengigheter eller gjennomført
en fullstendig, aktuell sårbarhetskartlegging av de eksterne bibliotekene.
Konklusjonen innebærer derfor ingen generell sikkerhetsgodkjenning av dem.

Ingen visuell PDF-kontroll, produktadopsjon, faglig årsaksept, Linux-CI,
publisering, GitHub-mutasjon eller merge er utført av denne auditten.
Nye kandidatendringer må bindes og vurderes særskilt før denne rapporten
brukes som leveringsport.
