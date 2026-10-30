# Uavhengig originalfeltfasit for T6/#64

Kontrollert 30. oktober 2026 mot grunnlaget i main
`9616fbe6a8ab15eec696f34de76888565a784f8f`.
Dette er en separat kildeport, skrevet mens produktet ble bygget.
Ingen T6-produktparser, produktuttrekk, byggerskript eller aktive byggerfiler
er lest eller kalt. Bare denne katalogen er skrevet. Ingen staging, commit
eller GitHub-mutasjon er utført.

## Reproduksjon og fasit

Fra repositoryroten, med Node.js (kontrollert med v24.22.1):

```console
node docs/research/innstilling95-64/independent/oracle.cjs --check
```

`oracle.cjs` bruker bare Nodes standardbibliotek. Det leser bevarte
originaler og deres faktiske forelder/sidevogner; tabellrader hentes med en
egen rad-/celleleser, og romertall avgrenses med balanserte DIV-tagger.
Ingen avhengighet til produktets parser eller datamodeller finnes.
Uten `--check` skriver skriptet bare `original-fields.json` i egen katalog.
Med `--check` beregnes hele fasiten på nytt og sammenlignes byteeksakt med
den lagrede filen, inkludert samtlige kildehasher, feltverdier og lokatorer.
Begge kommandoene er faktisk kjørt med bestått resultat og identisk fasit.

- `original-fields.json`: SHA-256
  `6fd8f0c2fb119771fccff1f61e22785fb9e4ac01fe706723934d2f7d07e473b1`.
- `oracle.cjs`: SHA-256
  `f73567978229eb6e78657b0daedec56b35b996a16a0d4dd1697799d793947c97`.

Fasiten har 36 kontoer i 14 kapitler, 108 tilrådingsfelt og 108 vedtaksfelt.
Alle tre felt er like for hver av de 36 kontoene mellom 95 og 359, og
før + fortegnsbestemt endring = etter er kontrollert på hver originalrad.
35 Prop.-trioer gir 105 identiske felt; Prop.-tabellens to øvrige trioer er
1429/1 og /22 og inngår ikke i 95. Den eneste 95-kontoen uten Prop.-rad er
1420/32. De tre manglende Prop.-feltene har uttrykkelig `null` i
forslagsverdi og differanse, uten oppfunnet nullobservasjon.

`innstilling_rows` og `decision_rows` er den komplette feltfasiten;
`prop_rows` omfatter hele de 37 originale Prop.-trioene.
`common_prop_trios` og `missing_proposal_fields` dokumenterer snittene.
Alle felt har rå talltekst, originalcelle, kildehash, lokator og nullbaserte
UTF-8-byteposisjoner i den faktiske kildefilen. XML-lokatorenes byteposisjoner
peker på det XML-escapede originalinnholdet; `raw_html` er samme innhold
dekodet ett XML-lag. Dette er ikke byteposisjoner i en normalisert tekst.

## Originaler og konkrete kontrollpunkter

Originalene ligger under
`docs/research/to-visninger-37/originals/forgrening/`, med mindre annet er
angitt. Alle brukte originale representasjoner og sidevogner har egen
byteantall/SHA-256 i fasitens `sources`.

| Original | SHA-256 |
| --- | --- |
| `inns95s.html` | `ae61227fa83adf04fb45956b1bd714a75592bbc1d6c70da300e554afef806aa6` |
| `inns95s-20261022-reused.html` | `1f159a3ca1df3e0bc35617644d0b36f7c92fd5684947f6eca5510595af533a03` |
| `docs/research/omtale-o1/originals/prop16s-ch4.html` | `ff1c53688a155c2cb9d8d37a8d40550e56b5c5c1d2d171c30519ef49227eca5e` |
| `vedtak-100889.html` | `f58ec94336da10d04046e09683bf83d6a72d3a2ddbf42a7b106f194472ef72f3` |
| `votering-181224.html` | `88553153fd4011b6b3aa041c7899701bd7f7a938f2ad1984aecd4c441d24a9d9` |

1420/32 er **812 765 000 / +270 000 000 / 1 082 765 000** i begge stadier.
I `inns95s.html` er endringen i `I/table[1]/tr[30]/td[4]`, byte
`[77293,77467)`, og før/etter i `tr[31]/td[3]`, byte `[77610,77811)`.
I `40034220.xml` er de tilsvarende cellene i de samme tabellradene, byte
`[22465,22623)` og `[22752,22938)`.

4400/2 er **518 000 / −518 000 / 0** i Prop., 95 og 359. 95s endringscelle
er `I/table[1]/tr[67]/td[4]`, byte `[105785,105955)`, og før/ettercellen er
`tr[68]/td[3]`, byte `[106290,106475)`. Etterbeløpet er et observert
heltallsnull; det er verken et manglende felt eller en beregnet forskjell.

Plenumsbeviset er avgrenset fra «Votering i sak nr. 13, debattert 18.
desember 2024» til neste sak, nr. 14. Det identifiserer Innst. 95 S,
Prop. 16 S unntatt kap. 1429 og hele I–VI, og avsluttes med at komiteens
innstilling ble enstemmig vedtatt. Hele denne tekstgrenen er bevart i
`plenumEvidence`. Dette sammenholdes med de seks formelle API-objektene og
vedtakssidens seks tilsvarende romertallsseksjoner; likt tabellbeløp alene
brukes ikke som vedtakelsesbevis. API-utdragene har ingen egen rundeopplysning;
fasiten beskriver den dokumenterte voteringen uten å finne opp en API-klasse.

Begge 95-HTML-originalene er merket BERIKTIGET. Hovedseksjonene `m1`–`m4`
er sammenlignet i sin helhet etter whitespace-normalisering, og er identiske.
Hver seksjons normaliserte teksthash ligger i fasiten. Alle seks lokale
romertallsseksjoner er også like. De forskjellige råhashene består;
uberiktiget original eller rettelsesmelding er fortsatt ikke funnet.

## Seks byteeksakte API-utdrag

Forelderen er den bevarte gzip-filen
`docs/research/to-visninger-37/originals/aar/session-2024-2025.xml.gz`.
Utpekt råforelder har **7 479 943 byte**, SHA-256
`c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42`.
Den komprimerte filens hash er
`1ea276a5730a5196f4def7471e0bf6ae51a7878a4eac86922cc87a9a71200a6b`.
Foreldermetadata og hver sidevogns både øverste og nestede forelderopplysning
er kontrollert mot faktiske byte.

For alle seks er oppskriften
`parent[:317] + parent[start:end] + parent[7479886:7479943]`, uten innsatte
byte. Objektgrenser og ordinært objektløpenummer er også funnet uavhengig
direkte i forelderen, før de sammenlignes med sidevognene.

| Vedtak/API-ID | Objektordinal | start:end | Utdragsbyte | SHA-256 |
| --- | --- | --- | --- | --- |
| 359 / 40034220 | 582 | 2172545:2237039 | 64868 | `d4c473bf1ee95ec3edacce490586c0df5ec233d356e4c236fd9d765704b00490` |
| 360 / 40034221 | 583 | 2237041:2238534 | 1867 | `5523b3b70066f58a19c2a57dad37c4b83d601b28cbfbbcc8afb07c99f275cfd1` |
| 361 / 40034222 | 584 | 2238536:2243116 | 4954 | `cdc501f41586cfda1116f280f940c508314556c1e18552a68de842aae53ad162` |
| 362 / 40034223 | 585 | 2243118:2244633 | 1889 | `9225b91c98f49b7b4f3006285848b0ca6021c335a220393be8dbc514787a53eb` |
| 363 / 40034224 | 586 | 2244635:2246531 | 2270 | `216186f2993d0844c81ac3a46f995df2a262a0afb930e2f44da27134aebc0fd6` |
| 364 / 40034225 | 587 | 2246533:2248874 | 2715 | `e41f0de65ee6aeb438005af7b4f1230ad1268e7c5545bc8b027cae20b0e14dcd` |

Alle rekonstruerte utdrag er byteidentiske med de bevarte `.xml`-filene,
og har kontrollert API-ID, formelt nummer, sak **100889**, sesjon
**2024–2025**, dato **18.12.2024**, type **ANNET** og lokalt romertall I–VI.
De er avledede utdrag fra fullsesjonsresponsen; ingen ny HTTP-respons hevdes.

## Fullmakter og roller

Hvert stadium har åtte atomiske detaljer etter **1+2+1+2+2**. Alle
beløpsrammer, tekstvilkår, perioder og kontoomfang følger med i
`authorizations`, med selvstendige bevispekere i 95 og det respektive
API-objektet. Råparagrafene er ikke forkortet.

| 95 → vedtak | Atomisk omfang |
| --- | --- |
| II → 360 | Én bestillingsramme på 8 000 000, 1420/21, 2024 og fremtidige år |
| III → 361 | Separate rammer 601 000 000 for 1420/61 og 266 300 000 for 1420/62; ett formelt vedtak |
| IV → 362 | Én delt ramme 16 300 000 for 1420/39,/69,/79; ingen tredobling |
| V → 363 | To stikkordspunkter, 1420/66 og /87, uten bevilgningsdelta |
| VI → 364 | Forskuttering 25 000 000 for 1471/1 mot 4471/3 med bindende avtale og betryggende sikkerhet; separat regnskapsregel om mellomværendet og rapporteringstidspunkt |

95-punktene er samlet komités tilråding; vedtakspunktene har egne
vedtaksroller. Det er fem nye formelle fullmaktsvedtak, og de tilfører ingen
monetær posthendelse. T6s beløpstabell tilfører 36 posthendelser.
Prop. V har tre stikkordspunkter. De tre originale avsnittene og kontoene
ligger i `prop_keyword_points`; V.3/1429/60 er uttrykkelig utenfor 95 og
de fem nye fullmaktsvedtakene. Gammel 81/211-gren må bevares av produktet;
den er ikke nyverifisert gjennom denne originalfeltfasiten.

95s Ap/Sp/SV-avsnitt begrunner skogvernøkningen på 1420/32. Høyres kritikk
og Fremskrittspartiets merknad til post 74 har egne avsendere og råavsnitt i
`statements`. De gjøres ikke til tallfestede alternativer eller Stortingets
begrunnelse. Samlet komités tilråding har separat bevis fra innledning til
tilrådingen, mens Stortingets vedtakelsesutfall har separat plenumsbevis.

Kildeporten fastsetter originalfelter, kildeidentitet og avgrenset rolle- og
fullmaktsfasit. Den kontrollerer ikke produktets nye identiteter, faktisk
eksport/navigasjon, legacy-bevaring, all omtalesemantikk, faglig årsdekning,
kontokontinuitet, faktisk fullmaktsbruk eller drift.
