# Faner, kildegjenbruk og fysisk dobbellagring

Undersøkt 27. oktober 2026, før T2 bygges, mot main
`3d7667762ed1eb00223827761831fdf4dbc309d5`. Dette er en analyse og et
oppfølgingsforslag, ingen endring av eksportformat, produktkode eller tidligere
filer. Eierens nye føring er at samme kilde skal hentes/struktureres én gang og
gjenbrukes med relasjoner, mens uavhengige kilder bevares for kontroll.

## Konklusjon

Alle dagens faner trenger **ikke** være egne synlige brukerflater. Mange er
avledede detalj-, kontroll- og kompatibilitetsvisninger av de samme objektene.
De er heller ikke alle overflødige: flere dokumenter kan bekrefte samme beløp,
og dekningskontroll, ustrukturert inventar, omtale og originalbevis må bestå.

Anbefal fem synlige brukerfaner i en senere, eksplisitt versjonert eksport:
**Forløp, Dokumenter, Omtale, Sammenligninger og Dekning og avvik**. Dokumenter
må inneholde eller gi umiddelbar tilgang til **hele** konto-/tabellinventaret,
og Omtale må gi hele tekstinventaret, også uten sikker postkobling. Konto er et
utvalg og en navigasjon i dette grunnlaget; det trenger ikke en separat kopi av
alle inventarradene. Behold et tilgjengelig kontrollområde for observasjoner,
relasjoner, proveniens og originaler, med én kanonisk offlinepakke.

Det viktigste lagringsproblemet finnes **bak fanene**: T1 har samme HTML-byte i
to kildeobjekter, hele råbyte både i Originaler og det frosne JSON-snapshotet,
og gjentatte observasjons-/tekstobjekter inne i flere modellag. Å skjule ark
endrer leseropplevelsen, men reduserer ikke denne fysiske lagringen. En ny
versjonert kilde-/observasjonsgrense trengs for faktisk normalisering. Gamle
T1/O2/B8/B9-filer skal fortsatt leses med sin opprinnelige betydning.

T2 bør nå gjenbruke eksisterende kilde- og observasjonsidentiteter, legge til
bare de nye 315/78-kildene og struktureringene, og unngå nye kopier per utvalg,
sak, post eller dokumentinngang. Generell ombygging av gamle eksportformater
bør være en separat, liten ticket. T2s kildebelagte komitéendring kan leveres
før en slik opprydding, med arvet kompatibilitetslagring uttrykkelig oppgitt.

## Hva som faktisk er undersøkt

Primærbevis er lagrede XLSX-celler/ZIP-deler og JSON-objekter, sammenholdt med
koden som eier dem. Følgende lokale leveranser er analysert uten omskriving:

| Leveranse under repoets `outputs/` | Faktisk kontrollerte filer |
| --- | --- |
| `t1-41-608895f/` | JSON og XLSX for `begge`, `dokument-inns81`, `dokument-prop16`, `post1`, `post22`, `tomt` |
| `o2b-210-begge-poster-7e70506/` | `begge.json`, `begge.xlsx`, `uendret-b8-begge.json` |
| `vedtak-210-13-kolonner-2026-10-22/` | `vedtak-210.json`, `vedtak-210.xlsx` |

Alle 17 filer har samme SHA-256 før og etter analysen. Filnavn, absolutte
analysebaner, størrelser, hasher, alle arknavn/overskrifter, rad-/kolonnetall,
lagrede celletyper og kilde-/objektnøkkelkontroller er bevart i
[evidence.json](evidence.json). `data_rows` der teller fysiske rader etter
overskriften; tekststykker og statusrader er ikke kildeobservasjoner eller
hendelser. Alle undersøkte ark er synlige; ingen av de undersøkte bøkene har
formelceller. Oppgitte tall kommer fra cellene, ikke fra arknavnene.

Full foreldre-/kommentarkontekst for #1, #32 og #37 ble lest fra den innhentede
`work/ticket-context/parents.json`. Bindende grenser er [B6][b6], [B8][b8],
[B9][b9], [O2][o2], [T1-kontrakten][t1] og [ADR 0011][adr11]. Den nye
vurderingen skiller derfor ønsket mål fra det som dagens strenge lesere faktisk
godtar. Ingen nye produktfunksjonstester eller ny faglig godkjenning er utført.

## T1: full fanetabell

Tall gjelder faktisk `t1-41-608895f/begge.xlsx`, unntatt der andre valg er nevnt.
Kolonnetyper beskriver semantikken; eksakte overskrifter og XML-celletyper står
i evidensen. [T1s eksportbygger][t1excel] angir eierskapet til hver projeksjon.

| Fane | Rader × kolonner og formål | Faktisk overlapp / nøkkel | Leser | Anbefaling i nytt format |
| --- | --- | --- | --- | --- |
| Forløp | 18 × 20. Kildebeløp, år/konto, betydning/rolle, lokator/hash, behandlingskontekst og status. År/kroner er tall; identiteter/koder er tekst. | De 18 observasjons-ID-ene er nøyaktig samme sett som Beløpsgrunnlag. Dokumentvalget 81 har 6, hvert postvalg 9 og tomt valg 0. | Analytiker | Behold som hovedvisning, projisert fra observasjoner. Vis bare nødvendig teknisk detalj ved oppslag. |
| Dokumenter | 5 × 11. Eksakte dokumentversjoner, dato, kilde-/strukturdekning, konto- og kilde-ID-er, valgt-markør. | Dokument-ID brukes av inventar, tekst og kontekster. Ingen nye beløp. Hele grunnlaget beholdes ved alle undersøkte filtre. | Alle | Behold hovedvisning; bygg inn hele inventaret eller direkte tilgjengelig detaljvisning. |
| Kontoer | 57 × 7. Sortert konto-/årsindeks over dokument, rolle, inventar-ID og strukturstatus. | De 57 inventar-ID-ene er nøyaktig samme sett som Inventar; hver rad peker tilbake dit. Dette er en indeks, ingen egen kilde. | Analytiker/navigasjon | Kan fjernes som separat ark i nytt format og erstattes av filter/sortering/lenker i Dokumenter/inventaret. |
| Inventar | 57 × 12. Hele dokumentenes konto-/rolleinventar, kompakt kildetekst, lokator, kilde-ID og beløps-ID-er. | Samme inventarrader som Kontoer, med flere felt. Noen tekstfelt er også identiske med Fulltekst; inventarets kontokobling har eget formål. | Analytiker/kontrollør | Bevar alle radene. Samle i Dokumenter eller behold tilgjengelig global detalj; må aldri begrenses til Forløps valgte beløp. |
| Fulltekst | 57 × 14 fysiske rader for 54 utsagn. Rolle, avsender, periode, kontoer, hierarki, tekst/HTML og delnummer. | Utsagn-ID + delnummer, ikke én kilde per rad. Tekst/HTML gjentas delvis fra O2 og øvrig T1-strukturering; se måling nedenfor. | Analytiker/kildekontrollør | Behold tilgjengelig som Omtale. Gjenbruk ett tekstobjekt via relasjoner; bevar tekst uten beløpskobling og fullmakter. |
| Beløpsgrunnlag | 18 × 12. Globale observasjoner, alle originalfelt/nullgrunner som JSON og kontekst. | Samme ID-sett som Forløp i begge-utvalget, men globalt 18 også ved tomt filter. Fullt observasjonsobjekt finnes også i snapshot. | Kontrollør/utvikler | Tilgjengelig kontrollvisning. Gjenbruk observasjonsregister via ID; feltene må ikke forsvinne når hovedvisningen forenkles. |
| Relasjoner | 31 × 11. 18 T1-relasjoner og 13 bevarte O2-relasjoner, omfang, aktør-/statusbelegg og fullt originalobjekt. | 31 distinkte relasjons-ID-er og ulike relasjonstyper; flere relasjoner peker til samme observasjon/hendelse. Fullobjektet gjentas i snapshot. | Kontrollør; analytiker via lenke | Behold relasjonene i registeret. En samlet kontrollvisning kan erstatte egen synlig fane, med forståelig oppslag fra hovedfanene. |
| Sammenligninger | 12 × 10. Konto/betydning, venstre/høyre observasjon, beregnet forskjell, regel/status/grunn. | 12 avledede parvise sammenligninger; alle er 0 i begge-utvalget. Ingen nye kilder eller vedtatte hendelser. Tomt valg har 0 rader. | Analytiker | Behold synlig, eventuelt som tydelig særskilt avsnitt i Forløp; inngangs-ID-er og sperregrunn skal være tilgjengelige. |
| Dekning | 7 × 2. Globale forhold før filter. | Samme 7 avvik står også i basis, og består i tomt valg. Dette er nødvendige synlige kontrollopplysninger. | Alle | Behold synlig og samle med øvrige globale avvik. Ikke skjul denne som teknisk kontrollark. |
| Originaler | 247 × 11 tekststykker for 23 kildeobjekter. ID/navn/format/hash/metadata og base64-byte. | 23 objekter, men 21 distinkte råhasher. De samme base64-originalene ligger også i Visningsgrunnlag. | Kildekontrollør/offline-eksport | Gjør til kildeindeks/uthenting fra ett kanonisk råregister. Selve base64-kopien i arket kan fjernes bare i nytt selvforsynt format. |
| Utvalg | 11 × 2. Rapport-/basis-ID, versjon, selection/returvalg og valgte/globale antall. | Avledet fra rapporten; finnes også i snapshot. De ulike utvalgene har samme basis-ID og identiske basisobjekter. | Alle, kort metadata | Flytt nødvendig metadata og filterbeskrivelse til Forløp/Dekning; fjern egen fane i nytt format. |
| Visningsgrunnlag | 258 × 2. Nummererte tekststykker av hele `visningspilot-1`. | Rekonstruert UTF-8 er byteidentisk med `begge.json`, 7 732 250 byte. Inneholder råbyte og hele basis igjen. | Maskin/offline-leser | Behold én offlinekapsel inntil nytt format har likeverdig selvstendig rekonstruksjon. Kan ligge i kontrollområdet; ikke fjern fra gamle bøker. |

Nøkkelkontrollene er gjort fra faktiske celler: `Forløp!A2:A19` mot
`Beløpsgrunnlag!A2:A19`, og `Kontoer!F2:F58` mot `Inventar!A2:A58`.
`Visningsgrunnlag!B2:B259` rekonstruerer den faktiske JSON-filen. I 81-valget
er grunnlagsarkene globale selv om Forløp bare viser tilrådingsstadiets seks
felt. [Utvalgsbyggeren][view] bruker observasjons-/utsagns-ID-er; den oppretter
ingen nye kildeobjekter ved navigasjon.

## B6/B8/B9 og O2b: full fanetabell

De første 22 arkene finnes i både den undersøkte B9-boken og O2b-boken.
De fem siste er O2-tillegg. Radtall er de samme i disse to prøvene, med
metadataforskjeller i rapport-/utvalgsfelt. Dette er **ikke** et forslag om å
endre B6/B8/B9s standardeksport under T2. Bøker med større inventar kan ha
videreføringsark og de valgfrie 2024-kontrollarkene; se siste avsnitt.

| Fane | Faktisk rader × kolonner; felttyper/formål | Overlapp og nødvendig skille | Leser / anbefaling i ny samlet eksport |
| --- | --- | --- | --- |
| Historikk | 2 × 13; konto/navn/dokumenter, datoceller, før/endring/etter i kroner, status. | To postledd projisert fra seks observasjoner; ikke seks ekstra registreringer. | Analytiker. Behold historikkfunksjonen i Forløp; bevart 13-kolonners gammel visning. |
| Sesjonsgrunnlag | 7 × 2; rapport-ID, vurderingstid, utvalg og utført/ikke utført. | Metadata. **Ikke** et innebygd fullstendig B6-JSON-snapshot. | Alle/kontrollør. Samle metadata med Utvalg/Dekning. |
| Kildeinventar | 1 × 28; vedtaksrevisjon, jobber/forsøk, råhash, ferskhet og struktur/dekning. | Eget globalt inventar og senere forsøksstatus; kan ikke erstattes av valgte beløpsrader. | Alle/kontrollør. Bevar globalt i Dokumenter/Dekning. |
| Inventarjobber | 1 × 2; jobb-ID og JSON med alle jobbfelt. | Jobb-/forsøksproveniens; flere hentinger er ikke flere vedtaksrevisjoner. | Kontrollør. Samlet proveniensvisning. |
| Dekning | 1 × 11; inventar-, innholds-, struktur- og faglige dekningsantall/status. | Ulike dekningsakser; avstemt tall er ikke full årsdekning. | Alle. Samle synlig med avvik. |
| Beløpsobservasjoner | 6 × 47; full rå/tolket/effektiv/godkjent verdi, kilde/ID/JSON/kontroll. | Seks ID-er er nøyaktig unionen av ID-listene i Historikkdetaljer. Før/endring/etter er ulike felt i samme posthendelse. | Kontrollør. Behold felt i observasjonsregister; hovedvisningen er projeksjon. |
| Historikkdetaljer | 2 × 39; full historikkgruppe, beløpsvarianter, ID-lister og lokatorer. | Samme to postledd som Historikk; har viktige flere felter og alternative grunnlag. | Kontrollør. Samle som detaljoppslag; fjern aldri feltene fra gammel B9. |
| Summer | 3 × 12; én rad per betydning med inkluderte/utelatte ID-er og dekning. | I denne prøven er alle sumverdier tomme og seks observasjoner utelatt; ingen godkjent total finnes. | Analytiker/kontrollør. Vis bare relevant sum/grunn i Forløp/Dekning; behold semantikken for annet B6-grunnlag. |
| Historikkberegninger | 0 × 5; beregnings-ID, teknisk saldo, status/ferskhet og JSON. | Avledet beregning, ingen original eller ny hendelse. Tomhet gjelder prøven. | Kontrollør. Samle i beregningsdetalj når relevant. |
| Kontrollresultater | 0 × 5; B5-resultat, godkjent kjedesaldo, dekning og JSON. | Faglig vurdering med eget grunnlag og gyldighet; ikke råbeløp. | Faglig kontrollør. Bevar separat vurderingsobjekt, visning ved behov. |
| Avvik | 29 × 11; globalt og radbundet avvik med filterstatus, konto, uttrekk/lokator. | Flere avvik kan gjelde samme observasjon; avviksrad er ikke kilde/hendelse. | Alle. Samle synlig med Dekning og dokumentavvik. |
| Avstemming | 1 × 13; faktisk/forventet/godkjent beløp, omfang og belegg. | Prøvens rad sier `ikke utført`, ikke et bestått kontrollresultat. | Kontrollør. Samlet kontrollområde med synlig status. |
| Kildeprøvekontroll | 1 × 5; observasjon, forventning/rå/effektiv verdi og kildebevis. | Prøvens rad sier `ikke utført`; annen kontroll enn dekning/eksport. | Kontrollør. Samlet kontrollområde. |
| Eksportavstemming | 2 × 3; kontrollnavn, 6 kontrollerte ID-er og 0 godkjente verdier. | Kontroll av selve eksporten, ikke uavhengig bekreftelse av kildebeløpet. | Kontrollør. Samlet kontrollområde. |
| Vedtaksfulltekst | 1 × 5; uttrekk/revisjon/hash/del og HTML. | Avledet dokumenttekst fra originalen, også i B8s `source_text` og O2s V-seksjon. | Analytiker/kildekontrollør. Samle i Omtale med originalpeker. |
| Tekstopplysninger | 0 × 7; lokator/type, tekst/HTML og kontrollgrense. | Kan ha fullmakter og tekst som ikke blir beløp; tom prøve beviser ikke unødvendighet. | Analytiker/kontrollør. Bevar i tekstinventaret. |
| Inventarfulltekst | 0 × 8; fulltekst for inventar uten valgt beløpsuttrekk. | Utfyller Vedtaksfulltekst; B6s brede inventar trenger denne funksjonen. | Alle/kontrollør. Samle fulltekst via dokument-ID, bevar også ustrukturerte dokumenter. |
| Saksdokumenter | 5 × 17; publikasjons-ID, type/nummer/sesjon, URL og rå metadata/hash/lokator. | Fem distinkte publikasjons-ID-er; saksmetadata er ikke innlest dokumenttekst eller postbevis. | Analytiker/kontrollør. Samle i Dokumenter, bevar metadatareferanser separat fra kildeinnhold. |
| Dokumentrelasjoner | 7 × 7; fra/til, sakstype/nivå og kildebelegg/råfelt. | Saksrelasjoner, ikke O2s post-/hendelsesrelasjoner. | Kontrollør/lenker. Ett relasjonsregister med type/omfang; ingen blind sammenslåing. |
| Dokumentavvik | 0 × 8; saksgrunnlag, siste forsøk/status og avvik. | Egen ferskhetsakse; null i dette uttrekket opphever ikke de øvrige 29 avvikene. | Alle. Samle synlig i Dekning og avvik. |
| Stikkordgrunnlag | 2 × 11; stikkord, tolkningsstatus/versjon og råtekst/HTML/hash/lokator. | Samme vedtakskilde, men særskilt `stikkord-1`-tolkning. Fravær og uavklart må skilles. | Kontrollør/analytiker. Gjenbruk kilde; behold tolkningen, vis detalj ved behov. |
| Saksgrunnlag | 11 × 2; rapport/format/saksutvalg, antall og grensefelt. | Metadata. **Ikke** en ekstra full `b6-frozen-2`-kapsel. | Alle/kontrollør. Samle metadata. |
| Omtale | 11 × 14; seksjons-ID, lokator, rolle/avsender, omfang, hierarki, tekst/HTML og uttrekksversjon. | 11 seksjoner, én P1 med to postrelasjoner; ingen ekstra beløpsobservasjoner. | Analytiker/kildekontrollør. Behold funksjonen som Omtale, med gjenbruk via seksjons-ID. |
| Relasjoner | 13 × 12; seksjon→hendelse, revisjon/observasjons-ID-er, kontoer, rolle/belegg/status. | Separate mange-til-mange-bevis; må ikke forveksles med saksrelasjoner. | Kontrollør/lenker. Samlet relasjonsregister. |
| Omtalekilder | 11 × 9; 10 kildemetadataobjekter og én PDF↔HTML-relasjon. | **Ikke 11 originaler**. Her ligger metadata, ikke en base64-kopi av hver original. | Kildekontrollør. Samlet kildeindeks; representasjonsrelasjonen beholdes. |
| Omtaleavvik | 1 × 1; globalt avvik før filter. | Samme rapportavvik finnes i Omtalegrunnlag; nødvendig synlig advarsel. | Alle. Samle med Dekning og avvik. |
| Omtalegrunnlag | 163 × 2; ordnede deler av hele `omtale-pilot-1`. | Rekonstruert tekst er byteidentisk med `begge.json`, 4 866 537 byte. Inneholder O2-originaler og nestet B8/B6. | Maskin/offline-leser. Én kapsel i nytt format; gamle bevares. |

[B6-byggeren][b6excel], [B8-byggeren][b8excel] og [O2-byggeren][o2excel]
underbygger skillene. O2s komplette råbyte ligger i Omtalegrunnlag, mens
Sesjonsgrunnlag og Saksgrunnlag bare er metadata-/kontrollpaneler. Arknavnet
«grunnlag» er derfor ingen pålitelig duplikatindikator.

Videreføringsark er tapsfrie deler av et langt felt, med cellepeker/delnummer,
ikke egne kilder. De skal håndteres som en del av sitt eierfelt. De finnes
ikke i de åtte bøkene undersøkt her. B6s valgfrie `Uavhengig kontroll 2024`
og `Omfangsforskjeller 2024` har et annet, avgrenset avstemmingsgrunnlag og
skal fortsatt kunne åpnes i kontrollområdet når valgt. Ingen konklusjon om
deres faktiske radinnhold trekkes fra disse smale 210-prøvene.

## Konkrete duplikater og nødvendige kildeskiller

### Råbyte: faktiske kopier i T1

Når T1-JSONs nestede O2- og B8-strenger pakkes ut logisk, inneholder den:

| Måling i `begge.json` | Resultat |
| --- | ---: |
| T1-kildeobjekter + bevarte O2-kildeobjekter | 13 + 10 = 23 |
| Distinkte faktiske kildehasher | 21 |
| Sum dekodede råbyte over de 23 objektene | 5 231 039 |
| Sum dekodede råbyte ved én forekomst per hash | 5 004 951 |
| Ekstra råbyte fra to identiske HTML-kopier | 226 088 |
| Tilsvarende ekstra base64-tegn | 301 452 |

Byteantallene gjelder de faktisk lagrede representasjonene etter base64-
dekoding. Gzip-kilder telles her som gzip-byte, ikke som de større
dekomprimerte HTTP-originalene. Gzip/originalhash og -størrelse skilles
uttrykkelig i `session_representations` i evidensen. Ingen størrelse her
likestilles med mengden unik faglig informasjon.

De to presise treffene er:

- `prop16s-ch4.html`: 118 163 byte, SHA-256
  `ff1c53688a155c2cb9d8d37a8d40550e56b5c5c1d2d171c30519ef49227eca5e`,
  både `basis.sources[0]` og nestet O2 `basis.sources[2]`.
- `inns81s.html`: 107 925 byte, SHA-256
  `e7069d74e911fb868812bb34f68b41d210b4e33035c1317cbedd296ac1101e95`,
  både `basis.sources[1]` og nestet O2 `basis.sources[4]`.

Dette er ikke to uavhengige innhentinger som kontrollerer hverandre. T1s nye
adapter leser de samme lokale filene på nytt; metadata for de nye objektene
settes til `repository_path`, mens O2 bevarer sitt eldre proveniensgrunnlag.
Det nye navnerommet og stien gir forskjellige objekt-ID-er for samme byte.
[Importen][sourceimport] og [kildekatalogen][sourcecatalog] dokumenterer dette.
Det er samtidig et **bevisst T1-kontraktsvalg**: en manglende/feilet ny numerisk
adapter skal gi hull, selv om gammel O2-tekst fortsatt finnes. Den kontrollen
kan fremover modelleres som eget adapterforsøk/-resultat som peker til samme
råobjekt; det krever ikke en ny råkopi. Å gjenbruke gamle byte som usynlig
vellykket fallback ville derimot bryte T1-kontrakten.

I selve XLSX-boken kan alle 23 originaler rekonstrueres fra
`Originaler!K2:K248`, gruppert med kilde-ID og delnummer. Alle hasher stemmer.
De samme 23 objektenes base64-byte finnes også i `Visningsgrunnlag!B2:B259`.
Dette gir to fysiske serialiseringer av 5 231 039 dekodede kildebyte i samme
arbeidsbok, før avledet tekst regnes med. De 247 Originaler-radene er
tekststykker, ikke 247 kilder. Metadata gjentas også per tekststykke.

Den faktiske boken er 5 523 111 byte. De to største ZIP-delene er Originaler
(7 738 634 byte XML / 2 753 881 komprimert) og Visningsgrunnlag
(7 822 494 byte XML / 2 673 226 komprimert). Dette viser hvor filvekten ligger,
men gir **ingen garanti** for fremtidig størrelse eller unike datamengder:
ZIP-komprimering, base64, JSON-escaping og metadata har ulike kostnader.
Å gjøre ark skjult vil fortsatt lagre de samme XML-delene.

### Modellobjekter og avledede tekster

T1s globale observasjonsliste har 18 unike ID-er: seks forslag, seks tilråding
og seks tidligere vedtaksfelt. Hele JSON-treet inneholder likevel **36
serialiserte observasjonsobjekter** med 18 unike ID-er. Hvert av de seks gamle
vedtaksobjektene finnes byteidentisk som kanonisk objekt fire steder:

1. nestet B6 `base.rows[*].observation`;
2. nestet B6 `base.unfiltered_rows[*].observation`;
3. nestet B8 `source_text.extractions[0].observations[*]`;
4. T1 `basis.observations[12:18]`.

De 18 overskytende forekomstene utgjør 65 427 byte kanonisk objekt-JSON før
escaping/innpakking. ID er beregnet fra de syv eksisterende identitetsinngangene
i [AmountObservation][obsid]; hele objektinnholdet er hashkontrollert separat.
De undersøkte B9-/O2-grunnlagene alene har 18 objektforekomster av seks unike
observasjoner, altså tre forekomster av hvert objekt allerede før T1.
Dette er serialiserings-/snapshotduplikasjon, ikke 36 kildebeløp eller flere
vedtatte hendelser. Kopiene kan erstattes av ID-referanser i et nytt format.

T1 bevarer O2s elleve seksjoner inne i den gamle konvolutten. Ti kopieres også
til T1-utsagn med nye ID-er; PDF-seksjonen håndteres særskilt. I tillegg er fire
par av T1s egne utsagn identiske i **kilde-ID, lokator, tekst og HTML**. Tre par
har også samme rolle/aktør. Det fjerde har `tilraading` mot `tilrading` i
rollefeltet. Dette er kandidater til ett tekstpayload med flere tolknings-/
kompatibilitetsreferanser, ikke grunnlag for å slette gamle ID-er eller slå
rollene sammen uten versjonert kontrakt. Den konkrete kopieringen fremgår av
[T1s O2-overføring][copysections].

En konservativ eksakt strengkontroll fant 43 grupper av gjentatte lange felt
(over 100 tegn, samme feltnavn), 77 022 overskytende UTF-8-byte. Base64 og de
nestede JSON-strengene er utelatt fra denne målingen. Tekst som er et
underutdrag av annen tekst, eksempelvis lokal tabellrad inne i hel HTML, er
heller ikke målt som eksakt duplikat. Tallet er derfor en snever payloadmåling,
ikke en total spareprognose. Lik tekst alene beviser heller ikke samme rolle,
periode, kildeversjon eller tolkningsobjekt.

De seks T1-utvalgene har samme basis-ID
`e1a32cd17ebe3d96bff66a4c302e72fc95af28d6d3fa6d8f09d07ff84b06ba5c`
og identisk kanonisk basisinnhold. Hvert selvforsynte uttrekk lagrer likevel
hele grunnlaget på nytt. Dette er nyttig ved uavhengig overlevering, men bør
ikke bli primærlagerets måte å registrere et nytt utvalg på. Det logiske
gjenbruket fungerer allerede; fysisk eksportduplisering er en annen akse.

### Det som skal forbli adskilt

- **Prop., Innst. og vedtak:** samme beløp er tre forskjellige kildestadium.
  T1s 12 nullforskjeller er reelle kontrollresultater fra forskjellige
  inngangs-ID-er. Ikke dedupliser på konto/beløp/tekst. I T2 må +119 og +129
  mill. komme fra hver sin kilde, og tilrådingens +129 og vedtakets +129
  bevares separat selv om de er like.
- **Før, endring og etter:** tre kildefelt med ulike beløpsbetydninger og
  lokator-/feltidentiteter. De grupperes til én posthendelse, ikke én
  beløpsverdi og heller ikke tre vedtatte endringer.
- **HTML og PDF:** ulike representasjoner med ulike byte, hasher og lokatorer.
  En HTML-tabell og PDF-sidetekst kan kontrollere hverandre, med uttrykkelig
  representasjonsrelasjon og avgrensning. Normalisert tekst er avledet.
- **Kildeobservasjon og innholdsrevisjon:** samme innhold kan observeres flere
  ganger med ulike HTTP-forsøk og transportmetadata. [ADR 0002][adr2] krever
  én innholdsrevisjon og bevarte observasjoner ved A→B→A. Ny responstid alene
  gir ikke ny faglig vedtakshendelse. HTTP-feil uten byte har ingen råhash.
- **To sesjonsresponser:** T1 har tapsfrie gzip-filer med ulike lagrede hasher.
  Dekompresjon gir henholdsvis `9cfeaef5…` og `c5f3b900…`, begge 7 479 943
  byte, men **ulike originalbyte**. De er ikke duplikater bare fordi de gjelder
  samme sesjon/størrelse. Den gamle 210-forelderen og den nyere 211-forelderen
  må fortsatt holdes riktig bundet. Gzip-hash og originalresponsens hash er
  forskjellige identitetsnivåer; begge står i evidensen.
- **Dokumentreferanse, sak og postbevis:** samme proposisjon kan gjelde flere
  saker. Én original gjenbrukes, mens hver saks-/postrelasjon har eget omfang
  og belegg. B8s publikasjons-ID er ikke en råhash, og samme eksport-ID alene
  kan ikke slå sammen ulike referatlenker. [ADR 0010][adr10] bevarer skillet.
- **Rå, tolket, effektiv og godkjent:** dette er ulike opplysninger om samme
  observasjon og eventuelle separate B5-avgjørelser. Feltene kan presenteres
  mer samlet, men skal ikke erstattes av én udokumentert «verdi».
- **Tekst og hendelsesrelasjon:** P1 er én seksjon med to kontoer og egne
  relasjoner til to hendelser. At bare post 1 får lønnsforklaringen er en
  relasjonsavgrensning. Fullmakter, post 60 og omtale uten beløpskobling skal
  fortsatt kunne bevares og finnes.

## Minste målarkitektur og anbefalt fanesett

Dette er et konkret forslag for en senere versjonert leveranse, ikke en
allerede innført datakontrakt:

1. **Råobjektlager:** ett immutable byteobjekt per faktisk hash, med størrelse
   og medietype. Dokumentversjon/representasjon peker til dette. Samme byte
   kan ha flere proveniens-/URL-/HTTP-observasjoner; de metadataene bevares
   separat og må ikke reduseres til ett vilkårlig felt. Ved like byte kan
   nytt forsøk gjenbruke payload uten å miste forsøket. Nytt innhold får ny
   hash. Gzip/utdrag knyttes eksplisitt til originalen, med bytegrenser.
2. **Kildebundet struktur:** ett beløpsobservasjonsobjekt per eksisterende
   identitetsregel: kildeversjon, parser/tolkning, lokator og beløpsfelt.
   Ett tekstpayload per kildeversjon/lokator/tekstuttrekksversjon, med
   hierarki og HTML; rolle-/periode-/tolkningskontekst kan ha egne objekter.
   Flere dokumenter, saker og poster refererer samme objekt. Gamle ID-er
   bevares og kan ha eksplisitt alias-/kompatibilitetsbinding; ingen omhashing
   av leverte resultater for å «rydde».
3. **Relasjoner og vurderinger:** mange-til-mange med egne ID-er, type,
   avsender, periode/konto-/års-/hendelsesomfang, evidens og status.
   Sammenligninger peker til inngangsobservasjoner og regel; B5-avgjørelser
   forblir separate. Indekser og `view` er avledede, gjenoppbyggbare cacher.
4. **Rapport/utvalg:** referanser til eksakte objekter og utvalg/returvalg;
   ingen ny innlesing eller nye observasjoner ved filterbytte.
5. **Eksport:** brukerfaner er projeksjoner av samme register. Én komplett,
   tapsfri offlinepakke lagrer råobjekter/struktur én gang per pakke.
   Kompatibilitetskapsler for uendrede gamle uttrekk er merket som arkiv/
   backup, ikke en ny kanonisk kopi. Samme pakke kan produsere begge
   inngangene. En eventuell lett visningsbok som trenger en sidefil må være
   et eget tydelig valgt format; den kan ikke erstatte dagens selvforsynte
   bok stilltiende.

| Synlig brukerfane | Innhold som må være lett tilgjengelig |
| --- | --- |
| Forløp | Valgt konto-/dokumentforløp, kildebeløp, rolle/betydning, viktig status, aktive filtre og lenker til detaljer. B9s 13-kolonners uttrekk kan bevares som gammel eksportprofil. |
| Dokumenter | Eksakt versjon og kildeoversikt, hele inventaret også uten beløpstolkning, alle saksgrener, fullmakter og struktur-/rådekning. Konto-/årsnavigasjon bruker dette inventaret. |
| Omtale | Hele tekstinventaret med avsender/rolle/omfang/hierarki og originalpeker, markert utvalg; også urelatert/uavklart tekst og fullmakter. |
| Sammenligninger | Forslag→tilråding→vedtak, avledet differanse, inngangs-ID-er og navngitt sperre/hull. |
| Dekning og avvik | Globale avvik før filter, kilde-/forsøksfeil, ukjente roller/år/omfang, kontrollenes utført-status og delvis dokument-/årsdekning. Skal være synlig også ved tomt valg. |

Kontrollområdet kan samle Beløpsgrunnlag, Relasjoner og Kilde-/eksportkontroll,
med kildeindeks og uttrekking av originaler fra offlinepakken. Det er lov å ha
flere tekniske ark dersom formatet trenger det; fem synlige brukerfaner er
en anbefaling om arbeidsflate, ikke en grense som skal presse bort bevis.
Synlighet må fastsettes i ny versjon: [T1s leser][t1reader] avviser blant annet
endrede arknavn, arksett og synlighet/oppsett. Å skjule tekniske T1-ark i en
eksisterende bok er derfor heller ikke en kompatibel kosmetisk endring.

## Hva T2 bør gjøre nå

T2s [315/78-ticketutkast][t2] skal fortsatt levere ni kildefelt, tre vedtaksfelt
og én vedtatt posthendelse, med kildebelagt +10 mill. sammenligning og
Ap/Sp/SV-/voteringsbelegg. Fanevurderingen endrer følgende antakelser før kode:

- **En kilde per faktisk representasjon/versjon, ikke per bruk:** lag et
  eksplisitt kildeinventar før adapteren. Søk etter råhash i eksisterende
  T1/O2-kilder før ny payload legges inn. Felles plenumsdokument eller
  sesjonsrespons skal ha ett byteobjekt med forskjellige lokatorer og
  saks-/postrelasjoner. Dersom en nyere faktisk HTTP-respons har andre byte,
  bevares den som egen observasjon/versjon med riktig proveniens.
- **Ikke gjenta T1s nye HTML-kopi:** ny parser-/kontrollstatus for samme
  tilgjengelige original skal peke til original-ID/hash. Et bevisst manglende
  adaptergrunnlag gir eget synlig avvik og manglende beløp; gjenbruk av råbyte
  må ikke maskere feilet adapter. Parseren kan kjøres på nytt for uavhengig
  verifisering uten å lagre enda en råkopi eller observasjon med samme ID.
- **Én tilleggsliste for T2-objekter:** eksisterende T1-objekter gjenbrukes
  ved ID. Ikke bygg to komplette 315/78-grunnlag for dokument- og konto-
  inngangen, eller én omtaleseksjon per målpost. Projiser begge inngangene
  fra samme basis. Nye vedtaksfelt skal ikke både opprettes i en ekstra
  normalisert liste og kopieres igjen som T2s egen kildefasit uten behov.
- **Eksplisitt kompatibilitetsgjeld:** gammel `visningspilot-1`/O2-kapsel kan
  måtte beholdes uendret for gamle ID-er og bevis. Den inneholder da fortsatt
  de målte eldre kopiene. T2 skal beskrive dette som arvet lagring, ikke
  hevde at «én gang per kilde» allerede er oppfylt. Hvis T2 trenger ny
  konvolutt, bruk én frosset eldre basis/kapsel og nye tillegg med referanser;
  unngå samtidig å serialisere hele den gamle basisen på nytt som enda et
  fullt T2-register. Felt-/versjonsvalget skal fastsettes før bygging.
- **Ingen generell faneopprydding i T2:** bevar eksisterende lesere,
  standardvalg, schema 5, B5-status og gamle ID-er. Nye T2-kontrollbevis kan
  bruke eksisterende arbeidsflater. Endret fane-/snapshotstruktur som faktisk
  fjerner payload krever et eget versjonert format og testbevis.

T2-aksepten bør suppleres med en faktisk serialiseringskontroll: nye råkilder
grupperes etter hash; samme kilde brukt av flere relasjoner skal ha én ny
payloadforekomst. Gamle kapslers arvede forekomster telles separat.
Antall unike observasjoner/hendelser og nye payloadobjekter skal være
uendret ved gjentatt eksport, filter/navigasjon og unionen 315/78 + 1429/1.
Det gjelder **kanoniske objekter**, ikke antall synlige projeksjonsrader.

Det er fortsatt nødvendig å teste begge inngangene, autentiske kilder og
faktisk JSON-/XLSX-gjenlesing, riktige roller, manglende/sperret sammenligning
og synlige globale avvik. Ordinær innlesning av nye vedtak skal fungere ved
manglende, feilet, korrupt og motstridende berikelse og uten historisk Excel.
Dette er anbefalt testgrense for byggingen; testene er ikke kjørt i analysen.

## Små trygge oppfølginger

**Første separate ticket: versjonert kildegjenbruk i den smale pilotpakken.**
Bruk akkurat de to påviste T1-HTML-duplikatene og de seks gamle observasjonene
som fasit. Ny leser skal kunne importere en ekte gammel T1-fil, bevare gamle
ID-er/objekter, samle råpayload ved eksakt hash og produsere et nytt opt-in-
format med ID-referanser. Ikke endre gammel fil eller gammel leser. Aksept:
gjenfunne originalbyte, metadata-/forsøksbindinger, nullgrunner, roller og
begge innganger er identiske etter faktisk JSON-/XLSX-rundtur; ingen ny
hendelse; endret hash/feil lokator/danglende referanse avvises; ny kilde eller
tolkning skaper separat identitet. Kontroll skal telle faktiske nye payload-
forekomster og observasjonsobjekter, ikke bare Python-objekter i minnet eller
filstørrelse. Ekte gamle A/B/B8/B9/T1-filer skal være uendret før/etter.

**Deretter en presentasjonsticket: fem synlige brukerfaner i den nye profilen.**
Flytt de nevnte projeksjonene inn i hoved-/kontrollområdene, behold ett
selvforsynt offlinegrunnlag og full tekst. Aksept: hele dokumentinventaret
og alle tekst-/kildeavvik finnes også ved tomt utvalg; datoer/beløp har riktige
celletyper; alle ID-er/lenker og lange tekststykker kan gjenleses; faglige
kontrollgrenser består; gammel eksportprofil/standard er uendret. Mål
lagringsreduksjon bare dersom payload faktisk er fjernet, ikke fordi ark er
skjult. Ingen av ticketforslagene er publisert eller startet av denne analysen.

## Kontroll og begrensninger

Analysen brukte regnearkskillens lesebeskyttede arbeidsmåte og research-
skillens primærkildeprinsipp. Bundlet Python og standardbibliotekets ZIP/XML/
JSON/base64/SHA-256 leste de faktiske filene. Originalenes hasher er kontrollert
før/etter; ingen gammel produktleser ble kjørt på originalbanene, og ingen
midlertidig fil ble opprettet ved dem. Alle dekodede kildeobjekter har korrekt
hash; Originaler-fanens rekonstruerte kildebyte stemmer med JSON-kildene.
Seks T1-snapshots og O2b-snapshotet er rekonstruert fra lagrede celler og er
byteidentiske med tilhørende JSON. De sentrale nøkkelsettene er avstemt fra
celler, og nestet objektlikhet er kontrollert uavhengig av ytre rapport-ID.

Ingen native Excel, ny visuell aksept, ny nettinnhenting, CI eller test av
ny funksjonalitet er utført. Bøkene er smale 210-/T1-prøver; konklusjoner om
fullsesjonseksport bygger bare på de dokumenterte kontraktene, ikke en ny
analyse av alle brede B6- eller historiske Excel-bøker. De målte duplikatene
er lokale konkrete funn, ingen generell ytelses-/størrelsesgaranti eller
påstand om feilregistrerte vedtak i databasen. Nye format-/arkvalg er forslag
med eksplisitt akseptgrense. #10 står fortsatt åpen for faktisk driftsaksept.

[b6]: ../../b6-sesjonsuttrekk.md
[b8]: ../../b8-saksdokumenter.md
[b9]: ../../b9-historikk.md
[o2]: ../../omtale-pilot.md
[t1]: ../../visningspilot.md
[adr11]: ../../adr/0011-filbasert-visningspilot.md
[adr2]: ../../adr/0002-kildeobservasjoner.md
[adr10]: ../../adr/0010-saksdokumenter-og-frosset-v2.md
[t2]: ../to-visninger-37/tickets/02-komiteendring-315-78.md
[t1excel]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/analyse/visningspilot_excel.py#L45
[view]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/analyse/visningspilot.py#L197
[b6excel]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/analyse/session_excel.py#L202
[b8excel]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/analyse/saksdokumenter.py#L695
[o2excel]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/analyse/omtale.py#L571
[sourceimport]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/innlesning/visningspilot.py#L178
[sourcecatalog]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/innlesning/visningspilot.py#L56
[obsid]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/innlesning/observations.py#L232
[copysections]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/innlesning/visningspilot.py#L826
[t1reader]: https://github.com/depmartin/budsjetthistorikk/blob/3d7667762ed1eb00223827761831fdf4dbc309d5/analyse/visningspilot_excel.py#L524
