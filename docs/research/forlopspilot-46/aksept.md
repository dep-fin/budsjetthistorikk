# #46: lokal akseptledger

Omfang: M16–M17, M21s navngitte helårshull og M22–M27, ved den avtalte
original→kildebundet felt/tekst→relasjon→begge innganger→faktisk JSON/XLSX-grensen.
Den hashfestede `verification.json` binder sluttkandidat, kjørt kontroll,
faktiske manifestfiler og bevisgrenser. Tabellen er lokal funksjonsaksept;
orkestratorens uavhengige review/audit og Linux-CI må avklares separat.

| #46-punkt | Kontrollgrunnlag og observerbart resultat |
| --- | --- |
| 1 Før-kode-kontrakt | `docs/forlopspilot.md`, [byggerekkefølge](tdd-journal.md), egen opt-in-regel og leser. Gamle formater beholder betydning. |
| 2 Én gammel kapsel | Faktiske snapshot har ett `legacy_json`, fem nye objekter og 18 gamle unike felt i uendret T1. Ingen T2-/ekstra gammel basis. |
| 3 Ansvarsdeling / kompatibilitet | Offentlig innlesningsadapter kjøres i separat prosess med alle analyseimporter blokkert. Gamle ID-er, schema5, B5, standarder og `round='uavklart'` gjenleses gjennom eksisterende tester/ekte filer. |
| 4 Eget inventartak | 153 og 1488 nye tabellrader; T3-tak 4096. Faktisk rehashet JSON/XLSX over tak avvises. Gamle 512-tak er urørt. |
| 5 Råbyte/proveniens/helinventar | `source-audit.json`, payloadregister, kildeindeks, fulltekst og alle tabellrader i Dokumenter/Omtale også ved tomt utvalg. Andre kontoer, totaler og komponenter merkes ustrukturert. |
| 6 341-oppskrift | 66aa-prefix317 + `[6092492:6209173]` + LF + suffix6816110 rekonstruerer repoets SHA73bb-utdrag eksakt. Budsjettår 2024, dato 2023. |
| 7 857-representasjoner | Ny 252544-konvolutt fra 66aa. Gammel 4113-fixture/sidevogn uendret; objektbyte like. 554e-original ikke gjenlest eller ommerket; ingen ekstra hendelse. |
| 8 210-proveniens | Autentisk tidligere T1-arkiv, verifisert av gammel streng leser, bevarer 9cfe/210 og gamle seks vedtaksfelt. Rehashet gammelt beløp avvises i ny faktisk filpakke; eksisterende koordinerte T1-negativer består. |
| 9 Nivå/runder/fortegn | Originalnivåer 161 243 000/32 185 000, RNB −1 000 000 og nysaldering +5 796 000/−3 000 000 i separate behandlingsrunder. Typede dato-/kroneceller og synlig nivåkolonne. |
| 10 Avgrenset fravær | Eget utsagn binder tr822–830 og kapittelgrense tr831. /22 er ingen 857-beløpsobservasjon eller positiv konto i dokumentets tabellreferanser. |
| 11 Tellerfasit | Faktiske par for /1=13/7/3, /22=10/4/2, begge/kapittel=23/11/5, tomt/feil år/fullmakt=0/0/0, 341=2/2/2, 857=3/3/1, 210=6/6/2. |
| 12 Lokal regning | To avledede objekter med eksakte input-/kontroll-ID-er, 166 039 000/29 185 000 og status avgrenset kontroll. Manglende/inkompatible felt, konflikt eller rekkefølge sperrer. Ingen ny kildeobservasjon/hendelse. |
| 13 Navigasjon / union | Faktiske dokument→konto→retur og konto→dokument→retur. Samme basis, rånavn og ID-er; alle 1488 RNB-rader ved dokumentåpning. Konkrete par med kryssproduktfare beholder bare tilsiktede felt. |
| 14 Navngitte hull | Alle opprinnelig-/RNB-/øvrig-/periodehull er i global basis og Dekning og avvik også ved null treff. Nysaldering fyller ingen annen rundes hull. |
| 15 Faktiske filer / offline | Ops-manifestets navngitte par og offentlig frozen-CLI med ikke-eksisterende originalrot; JSON/XLSX lukkes og gjenleses. Gjentatt offline-JSON er byteidentisk med begge-utvalget. Alle sju dokumenter prøves. |
| 16 Faktisk kildegjenbruk | JSON og gjenlest Excel-snapshot har fem nye payload/unik hash og fem nye observasjonsobjekter, én forekomst hver. Én gammel kapsel arver 23 råforekomster/21 hasher og 36 observasjonsobjekter/18 unike; dette normaliseres ikke stilltiende. Ingen ekstra råbase64-fane. |
| 17 Streng gjenlesing | Faktiske rehashede JSON/XLSX for verdi/fortegn/år/rolle/runde/lokator/forelder/ID-ref/relasjon/utvalg/fravær/hull/regneresultat/status/input, også rehashet gammel kapsel. Inkompatible år/enheter/kontoer/betydninger/omfang og rekkefølge sperrer beregning. |
| 18 Excel | Fem hovedfaner + tilgjengelig kontroll/offline. Tapsfrie 30 000-tegnsstykker, formeltegn som tekst, reell helinventar-/fullteksttilgang, gruppetrioer/nivåer og interne lenker. Falsk verdi/format/lenke/skjult rad/kolonne/ark/filter/DOCTYPE avvises. Artifact Tool-rendering av faktisk bok og tomt/globalt utvalg er separat journalført. |
| 19 Ekte gammel kompatibilitet | Hashkopier av tidligere A/B/B8/B9/T1/T2-filer, innebygde gamle B6-kjerner og én ekte separat B6-bok. Originaler kontrolleres før/etter. Selvstendig gammel frozen-v1-rapport-JSON er fortsatt ikke i tilgjengelig kontrollgrunnlag. |
| 20 Uavhengig ny 368 | Fire separate ferske databaser: offentlig synkronisering→råbevaring→lagring→tolkning→Excel ved manglende, feilet, korrupt eller motstridende T3. Hver 222 felt/74 ledd og faktisk 700/1-trio, også sammen med gjenlest tomt T3-utvalg, uten historisk Excel. |

Resultatet gir teknisk kilde-/filaksept for dette snittet. Native Excel,
fullårsdekning, faglig godkjenning, kontokontinuitet, T4–T6/K1–K3 og drift er
egne bevis/mandater. #10/#32/#37 forblir åpne.
