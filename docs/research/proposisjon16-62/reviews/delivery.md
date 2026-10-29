# Gjeldende kontrollporter og publiseringsbindinger

Denne inngangen skiller de historiske kontrollene fra den rettede, samlet
godkjente T5-kandidaten. Faktisk CI-/mergestatus føres i
[#62](https://github.com/depmartin/budsjetthistorikk/issues/62) og dens PR.
Dette dokumenttillegget endrer ingen produktkode, test, kilde eller manifest.

## Kandidater tilgjengelige fra GitHub

De publiserte committene har de samme komplette trærne som de lokale
kandidatene. De danner en direkte foreldrekjede fra base
`2f4ee30c9d8074076fc8042e208c4a4b6345db6b`.

| Lokal kandidat | Publisert tilsvar | Identisk tre | Tilstand |
| --- | --- | --- | --- |
| `d46589cb9e99338e44fc805ee9882006ba657fd0` | `4ddda7953431ac9f6ae861d800a33229121e54db` | `df0eed6d6e8a0b2a07962e641ae05d1194a3304d` | Historisk kandidat før temaretting. |
| `95ed8e60052d7731bb99386db572ba607c6b36a2` | `ea91dc9c7a30c55e7a5f9c75b7381fc7a2d33d11` | `225382d23bf776a8c9ee1a81a8d27de90e1b8620` | Temavern rettet; historisk feil i Git-binding av kontrollbyte. |
| `cd240e3b2f4846081d1f658faf0caec9cf4a7186` | `a08fc28dc33fa4244814dc29fbeeb5b87d4e804d` | `1f32d2e81f8ff76fb3365d9c0fa6592fbb64eb39` | Rettet produkt og råbytebevaring; gjeldende godkjente kontrollkandidat. |

Ulike lokale/publiserte foreldre og author-/committermetadata gir ulike
commit-ID-er. Bruk de publiserte tilsvarene som kandidatargument ved
fersk-klon-reproduksjon. Kontrollene krever ikke at upubliserte lokale
commitobjekter importeres. Blob-ID-er og hele trær er kontrollert før
publisering; tomme trediffer etter ny fetch bekrefter alle tre bindingene.

## Uavhengig kilde-/feltkontroll og visuell QA

[Kildekontrollen](source/report.md) bekrefter 37 trioer/111 felt, 45
kontoangivelser, ni fullmaktspunkter og åtte grener mot originalene.
18 egne filpar, 25 originalrepresentasjoner, 13 faktiske Excel-renderinger
og åtte PDF-sider inngår. Produktets feltgrunnlag, identiteter og skriver
er uendret gjennom de etterfølgende sikkerhets-/bytebevaringsrettingene.
Native Excel er ikke prøvd. Forhåndsvisningsgrenser er dokumentert.

## Standards

[Gjeldende rapport](byte-final/standards.md): bestått. Det tidligere P2 om
49 råbytebindinger er lukket direkte mot de endelige Git-blobene. En
valgfri P3 om duplisert kontopredikat består som skjønnsmerknad uten
påvist atferdsfeil; den er ikke endret i denne avgrensede leveransen.

## Spec

[Gjeldende rapport](byte-final/spec.md): bestått, 0 funn. Alle tidligere
funksjonsforutsetninger består. Det konkrete feilede kontrollreplayet er
gjennomført på nytt med eksplisitt retargeting og består.

## Separat sikkerhetsaudit

[Gjeldende rapport](byte-final/security.md): bestått, ingen åpne P1/P2.
Temavernet består. 16 bevaringskontroller og 25 leserprober inngår;
den tidligere separate auditen av rettet temavern hadde 122 kontroller.

[Temarettingen](../security-fix/README.md) binder hele temadelens størrelse
og byte til skriverens faste forventning. Tre regresjonsvarianter avvises,
og alle 38 T5-tester består. Gamle guardprofiler og eksportskriveren er
uendret.

[Råbytebevaringen](../byte-preservation/README.md) retter 49 manifestavvik
ved å bevare de allerede observerte bytene. Gamle manifester og bevis er
uendret. Scoped Git-attributter, faktiske filtre og fire ferske
utsjekkinger er prøvd; den opprinnelige 35-filers kontrakten består.
344 historiske arbeidsrepresentasjoner materialiseres bare i en isolert
replaykopi. Dette gir ingen generell tillatelse til å normalisere kilder.

## Faktisk fersk GitHub-klon

[Fersk-klon-rapporten](fresh-clone/README.md) dokumenterer nettverksklon
uten lokale kandidatobjekter, alternates eller gamle eksportdata.

- Alle tre publiserte SHA-er/trær og foreldrekjeden er bekreftet; alle
  tre upubliserte lokale kandidat-SHA-er manglet.
- 14 nye JSON/XLSX-par, begge CLI-inputveier og 25 byteeksakte originaler
  er prøvd på den rettede publiserte kandidaten.
- Separat historisk feltkontroll bekrefter 111 felt/45 kontoer og
  16 gjenleste filpar.
- 35/18/54 manifestbindinger, 49 rettede avvik og 47 historiske
  bevaringsbindinger består.
- Åtte ferske hjelperprosesser og det uendrede sammenligningsprogrammet
  består med 1270 bindinger og fire like ledgerutfall.
- Historisk kandidat beholder sitt dokumenterte temaakseptutfall;
  den rettede publiserte leseren avviser alle tre temaangrepene.

Feilforsøk og krav til isolert materialisering er bevart i rapporten.
Etter dette følger bare dokumentariske kontrollrapporter/publiserings-
bindinger. Full Linux-CI med hele testutvalget og 90-minuttersgrensen,
bekreftet merge og betinget lokal hovedsynkronisering er egne sluttporter.
