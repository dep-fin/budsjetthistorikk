# Kildebinding, gjenbruk og faglige roller

P2 adopterer bare de allerede kontrollerte funnene fra R2-merge c041ad8.
Ingen ny HTTP-innhenting eller utvidet kildeundersøkelse er gjennomført.
Gjeldende R2-sluttstatus er #54s siste overlevering, ikke de eldre
kandidatrapportenes «gjenstår»-tekster. De gamle rapportene bevares.

Den nye kodekatalogen pinner 69 eksakte eksisterende filer: seks
register-/bevisfiler, 22 arkiv-/metadatapar og 19 gjenbruksfiler. Hash,
byteantall og dekomprimert representasjon kontrolleres separat før parsing.
Alle 74 belegg rekonstrueres med opprinnelig XPath, navnerom, eventuell
indre HTML-feltlokator, whitespace-regel, tekst og tabellceller.
De 11 funnene og C01–C12 rekonstrueres fra de kodepinnede journalene og
belegg som faktisk er gjenfunnet i de hashbundne originalene.

Den første DNS-feilen for sak 101000 har tom capture og ufullstendig
status. Den er ikke et komplett dokument eller fraværsbevis. Det vellykkede
retry-forsøket har egen identitet, original, tid og metadata. De to
HTTP-representasjonene av vedtak 230/231 beholder egne arkiver; hele
XML-objekters kanoniske samsvar rekonstrueres fra begge originalene.

P1/T4/T1s eksisterende kilde-ID-er og payloads løses gjennom referanser.
Identiske gamle råbyte legges ikke inn som en ny fysisk payload. De nye
gzip-originalene lagres én gang; visningene lagrer ingen full dekomprimert
råkopi hver. Gamle immutable kapslers arvede duplisering oppgis separat.
`.gitattributes` bevarer R2s eksisterende byte også ved Windows-checkout;
ingen gammel kilde eller manifest er normalisert eller omskrevet.

Den faktiske fysiske målingen i `physical-reuse.json` teller base64-kildefelt
og rekursivt dekodede `*_json`-kapsler per lagret forekomst. P2 har 50 nye
fysiske payloads, 50 unike digester, null dupliserte byte og null overlapp
med arvede råfelt. Den uendrede P1-basis har 141 slike fysiske felt med
139 unike digester og 226 088 dupliserte dekodede byte. Dette er et mål på
den erklærte lagringsrepresentasjonen, ikke dekomprimert kildeomfang eller
antall faglige objekter. T1-kapselen er også målt separat og bevart ordrett.

Prop. 36 beholder sitt gamle dokument-ID og sin gamle dokumentpost.
R2s ekstra rårepresentasjoner, konkrete 1429/1-celle og fullmaktsgren er
additive utsagn og inventarrader. Den kildeobserverte anslagscellen er
`/html/body/main/div/div[3]/div[3]/div/div/table/tbody/tr[293]/td[4]`.
Kapittelraden tr292, postcelle td2, enhet «Kroner» og neste kapittel 1471
avgrenser lesingen. Den vises i egen verdi-/rollekontekst, aldri i
1429s vedtatte endringskolonne. 1560/71s før/delta/etter er forskningsverdier
for annen konto; 231/429 har uttrykkelig null beløp.

Hele Prop. 34s fem HTML-kapitler og PDF er råbevart. Hovedinnholdet i de
fem kapitlene og Innst. 91s komplette relevante seksjoner er tilgjengelig
som kildebundet tekst. Ulike merknadsavsendere står separat fra samlet
tilråding og Stortingets vedtak. Innst. 90 er hel råkilde, men bare
fullmaktsgren II er strukturert. Ingen hel Prop. 36-adapter hevdes.

Voterings-APIets −1 bevares som rå sentinel. Samtykkedatokonflikten
20./21. juni og alle tolv kryssreferansers delomfang/uavklarte rest består.
Felles sak, tittel, ordfravær eller beløpslikhet oppretter ingen postkobling.
