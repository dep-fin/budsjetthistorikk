# P1: kildebinding og representasjoner

Kontrollgrunnlaget er K3 i merge 29ac220. Den faste katalogen i
innlesning/perioderegister_catalog.py pinner 130 register-, arkiv-, metadata-
og gjenbruksfiler før rapportbygging. Eksakte byte, inkludert K3s CRLF,
bevares. .gitattributes gjør denne regelen eksplisitt også for nye checkouter.
Ingen eksisterende kildebyte, gammel ID eller uttrekkstolkning er endret.

Arkivhash og dekomprimert representasjon har ulike hasher. P1 bevarer gzip
og de opprinnelige transportmetadataene, inkludert ufullstendige/feilede
forsøk. Full Innst. 447 sendes gjennom en egen begrenset gzip-port på
32 MiB; gammel 16 MiB-port for enkeltpayload eller HTML endres ikke.
Det finnes ingen generell nettinnhenter. Nytt register legger ikke inn en
full dekomprimert 447-kopi for hver inngang.

De 119 nye payloadoppføringene består av 113 fysiske råpayloads og seks
referanser til identiske byte i den uendrede T1-/O2b-kapselen. Gjenbruket
omfatter også råoriginaler som ligger i den nestede eldre kapselen, blant
annet plenum 16.12.2024. T4s egne payloads refereres direkte. Nye Source-
objekter beholder sine metadata og proveniens selv når byte gjenbrukes.

346/40032933 er bundet til den komplette 66aa-forelderen og hele objektet.
Inventaret viser 1429/1, 4429/2, 4429/9 og den uttrykkelige 1633/1-
henvisningen i fullmaktsteksten. Bare 1429/1 er leddets valgte postkobling.
Votering 22032 og tilråding VI/forslag 40073889 holdes adskilt fra
341s tilråding I/forslag 40073884. Ingen ny beløpsobservasjon eller hendelse
opprettes av fullmakten.

K3s 67 indeksforekomster er forskjellige registerobjekter etter sesjon,
ordinal og kildeversjon, også når saks-ID er lik. metadata_json bevarer
hele K3-metadataobjektet. Det komplette underliggende XML-indeksobjektet
bevares også som et kildebundet utsagn i dokumentinventaret. Kandidaten
selv er indeksets inventarprojeksjon. Det opprettes ingen InventoryItem
med et oppdiktet budsjettår 0 eller 2024; den gamle typen har obligatorisk
heltallsår, mens CaseCandidate tillater null etter P1-kontrakten.

Alle 25 begrunnelser beholdes, med full autoritativ identitet og originale
vedtaks-/registerreferanser. Uttrykkelig statsbudsjett, Svalbardbudsjett og
fullmaktens «i 2025» kan gi år; sesjon og dato gjør det aldri alene.
H-/FrP-standpunktene beholder ukjent separat primærvotering. De sju RNB-
pakkene beholder egne forkastede utfall. Prop. 36 er en kontrollkilde for
vedtatt eller foreslått status, ikke en ekstra vedtakshendelse.

208 nye inventarrader omfatter 203 kildebundne råceller fra de uttrykkelige
registerpassasjene og fem fullmaktsrader. De komplette tabellbevisene vises
i Omtale, med råtall og lokatorer. Dette er den erklærte delstrukturen;
det er ingen fulladapter for Prop. 1/104/447. Råkildene og K3s øvrige
bevisarkiv er bevart selv om enkelte passasjer står utenfor denne visningen.

R1–R7 er rekonstruerte globale rester, også ved tomt utvalg. Registeret
gir ingen positiv M21, kontokontinuitet, faglig årsbalanse, B5-avgjørelse
eller driftsaksept. #10/#32/#37 står åpne. De gamle hullene i T4-kapselen
beholdes som historisk grunnlag; P1s nye kilder og status står separat.
