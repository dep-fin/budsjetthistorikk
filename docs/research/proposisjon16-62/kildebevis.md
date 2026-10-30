# Kildebevis og bevaring

Ingen primærkilder er hentet på nytt. Alle kilder kommer fra tidligere bevarte,
hashfestede originaler i basen. Kontrollinventarer er avledninger, ikke
primærkilder. [source-manifest.json](source-manifest.json) fører navn,
kildeversionens ID, SHA-256, byteantall, status og bevart metadata.

## Forslagstabell og kontoer

Autoritet er O1s uendrede `originals/prop16s-ch4.html`, SHA-256
`ff1c53688a155c2cb9d8d37a8d40550e56b5c5c1d2d171c30519ef49227eca5e`.
Full PDF har SHA-256
`677716056269c07b8ec81bcae91d814b975123791635548281038d9beb3aa5db`.
Kapittel 2s separate del-HTML har SHA-256
`258d26e6d324bde709bf3d1cb660d7eb6f4248f537d4b0c77e095f17697cf8df`.
Ingen del-HTML gis full HTML-dekning.

`source-control.json` avstemmer alle 111 felt mot den eldre uavhengige
forgreningsundersøkelsens `inventory.json`, og kontrollerer i tillegg de
konkrete cellene i original-HTML uten produktparseren. Konto, betydning,
eksakt kroneverdi, råfelt, felt-ID og XPath følger hver kontrollrad.
Tre felter er én trio; de er ikke tre hendelser. 37/15 gjelder tabellen,
mens 45-kontoinventaret også har stikkord og kontekst, herunder 1533/45.

4400/2s før/endring/etter er 518000/-518000/0. Null er til stede og har
ingen nullgrunn for `amount_kr`. 1429s seks Prop.-felt gjenbrukes; bare
35 andre trioer blir nye beløpsobjekter.

## Fullmakter og grener

Originalankrene `kap2-p57`–`kap2-p61` dekker II–VI. Ni atomiske punkter
bevarer seksjonens råtekst, vilkår og struktur samt punktets egen XPath.
Den separate originalkontrollen kontrollerer romertall, råtekst og de fem
tallfestede rammene direkte mot kilden: 8 / 601,0 / 266,3 / 16,3 / 25 mill.
IV er ett objekt med tre kontoer, ikke tre rammer eller bevilgningsdeltaer.
VI har en forskutteringsramme og en separat regnskapsregel.

Grenene bruker gamle dokument-/kilde-ID-er og lokatorer i den bevarte
c5f3b900-forelderen. `raw-source-controls.json` kontrollerer alle åtte
formelle forbindelser mot faktiske XML-objekters saks-ID og lokale romertall.
Dette importerer ingen nye 95/359-beløp. T1s historiske videre referanseomfang
beholdes inne i kapselen og merkes historisk i Excel. Gjeldende T5-grener
avgrenser tabellkontoer og uttrykkelige fullmaktspunkter. Et 1533/45-utvalg
viser proposisjonen uten automatisk Innst. 95-tilknytning.

## Representasjoner og ukjent rettelseshistorikk

T1s 23.10-HTML av beriktiget Innst. 95 har SHA-256
`ae61227fa83adf04fb45956b1bd714a75592bbc1d6c70da300e554afef806aa6`.
22.10-representasjonen, som ikke lå i T1-kapselen, legges til én gang med
SHA-256 `1f159a3ca1df3e0bc35617644d0b36f7c92fd5684947f6eca5510595af533a03`
og sitt uendrede gjenbruksmanifest. De to HTML-responsenes hovedseksjoner
m1–m4 har lik normalisert tekst. Begge er merket beriktiget. PDF-en har egen
hash `7a78167c7eafc500938e4ac39d8ed9febec1f6e7e6ce337acc4b7a58d0d14635`.

22.10-kilden har bare datopresisjon i transportmetadata. Verken uberiktiget
utgave, rettelsesmelding eller semantisk rettelseshistorikk er rekonstruert.
Forskjellige råhasher er ikke i seg selv en faglig dokumentrettelse.

Originalene kan gjenfinnes tapsfritt med `export_originals`, også uten kilde-
rot, nett eller database. Gamle foreldre, transportmetadata og utdragsidentiteter
ligger fortsatt i én T1-kapsel. Nye råpayload er bare 22.10-HTML og dens
gjenbruksmanifest; gamle råpayload og beløpsobjekter kopieres ikke til et nytt
modellag. Synlig originalark peker til den selvforsynte kapselen.
