# Byggejournal P1 / #52

Byggemandatet bruker ticket-orchestrator, implement- og TDD-filinstruksjonene
fra den installerte Matt Pocock-pakken 1.3.1. Implement-skillens individuelle
review/commit er uttrykkelig overstyrt: byggeren leverer lokale endringer.
Regnearkskillen brukes med openpyxl etter repoets ansvarsdeling, FIN-farger
og skrivebeskyttet rendering med den medfølgende Artifact Tool-runtime.

Testgrensene er allerede fastsatt i før-kode-kontrakten, commit 407fdbc:
autentisk original, register/fullmakt, kildebundet relasjon, begge offentlige
innganger, faktiske JSON-/XLSX-filer og offline-CLI. De prøver ikke generell
årsimport, native Excel, drift eller faglig årsbalanse.

1. Første vertikale prøve var fullmakt 346 og globale kandidater gjennom
   offentlig kildeimport/rapportbygging. Først manglet pytest i bunten;
   etter lokal installasjon feilet prøven fordi analyse.perioderegister
   manglet. Adapter, immutable typer og rapportgrense ble innført, deretter
   var prøven grønn. En syntaksfeil og en uventet null-henvisning i en ekte
   indeksrad ble rettet under dette steget.
2. Neste prøve skrev/lukket/gjenleste fullmakten som faktisk JSON/Excel og
   krevde tomme bevilgningskolonner. Excel-grensen ble innført etter den
   første registerprøven. Filprøven bestod. Standard midlertidig mappe var
   utilgjengelig i Windows-sandkassen; senere prøver bruker egen basetemp.
3. Etter de to vertikale sporene ble regresjonsmatrisen utvidet med
   tellerfasit, navigasjon/retur, ukjente indeksår, journalbegrunnelser,
   ressursgrenser, rehashede JSON-filer, konsistente negative Excel-kapsler,
   falsk/skjult presentasjon og offentlig offline-CLI. Dette er etterfølgende
   regresjonsarbeid, ikke en påstand om at hver negativregel ble innført i
   en egen rød/grønn syklus. 13 tidlige P1-prøver bestod på 68,10 sekunder.
4. Kildeavstemming fant at saksindeksen har saker_liste som tredje rotfelt.
   Kandidatens kildeordinal beholdes, og lokatoren peker til tredje felt.
   Alle 67 K3-metadataobjekter kontrolleres mot faktisk indeksoriginal.
   Hele indeksobjektet vises dessuten som XML, med uendret null-år.
5. Kontrollhjelperens første voteringsavstemming inkluderte presidentens
   nestede objekt, mens K3s fields har scalarfeltene. Den ble rettet til å
   kontrollere alle scalarfelter eksakt; komplett XML er fortsatt bevart.
   En arvet T4-presentasjonsmutasjon forutsatte tall i G11; P1s egen prøve
   endrer i stedet det faktisk tallførende G2. En testantakelse om at
   kapittelvalg og eksplisitte /1-/22-par har samme tekstinventar ble
   avgrenset til P1s korrekte kontoomfang.
6. Kildepassasjene ble deretter gjort synlige som komplette råceller og
   tabellbevis i de nye registerdokumentene, inkludert begge Prop. 36-
   vedlegg. Dette normaliserer ingen nye beløp. En tidlig fullsuite og
   filkontroll ble avbrutt før fullføring da dette dokumentinventaret ble
   styrket; de ufullstendige loggene er ikke rapportert som beståtte porter.
   Endelig fullsuite og filkontroll ble startet på den ferdige produktkoden.
7. Første faktiske rendering avdekket at de nye registerradene kom etter
   alle gamle beløpsrader. Forløp ble ordnet etter K3-registerets dokumenterte
   behandlingsrekkefølge, slik at originalforslag, fullmakt, RNB og
   nysaldering står i sine runder. En pågående ufullstendig kontrollrunde
   ble stoppet før denne visningsrettingen. Alle 23 P1-tester bestod deretter
   på 199,14 sekunder. Den avsluttende fullsuiten registrerer hashene til de
   åtte kjørbare kandidatfilene før/etter kjøring.
8. Den fysiske bytekontrollen fant seks eldre kilder i den nestede O2b-
   delen som ennå ble kopiert som nye råpayloads. En ny offentlig prøve
   for den autentiske plenumskilden feilet først. P1 bruker deretter T2s
   uendrede legacy_source_id-regel også for disse kildene; 113 nye rå-
   payloads og seks referanser erstatter 119 nye råkopier. En rehashet
   negativ fil prøver dessuten å legge gammel råbyte tilbake som ny kopi.
   Pågående ufullstendige kontroller ble stoppet og ikke godskrevet.

Endelig fullsuite/statikk og faktisk kontrollarkiv dokumenteres separat i
akseptledgeren. Ingen full Linux-CI, samlet review eller audit påstås her.
