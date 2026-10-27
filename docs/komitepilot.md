# T2: komitéendringen 315/78

Kontrakt fastsatt 27. oktober 2026 før produktkode under #44. Opt-in-formatet
`visningspilot-2`, regel `komite315-visning-1`, har egen adapter og leser.
T1, schema 5, gamle kilde-/observasjons-ID-er, tolkninger, B5 og standardvalg består.

## Frosset testgrense og akseptledger

Original → beløp/tekst → kildebelagt relasjon → begge innganger → faktisk skrevet
og gjenlest JSON/XLSX er den avtalte offentlige testgrensen i #44/#1.
M10–M12, M07 og M22–M27 i [matrisen](research/to-visninger-37/testmatrise.md)
fryses med autentisk fasit i [komitéundersøkelsen](research/to-visninger-37/komiteendring.md).
315/78/2024 gir 9 felt / 3 vedtaksfelt / 1 monetær hendelse. Forslag har
29 050 000 / +119 000 000 / 148 050 000; flertallstilråding og vedtak har
29 050 000 / +129 000 000 / 158 050 000. Stadieforskjellene før/endring/etter
er 0/+10 000 000/+10 000 000, deretter 0/0/0. Union med 1429/1 gir 18/6/2,
tomt valg 0/0/0 og samme globale grunnlag. Negativer prøver også rehashede filer.

## Eierskap og filgrense

`innlesning.komitepilot` bevarer og strukturerer det faste kildeutvalget uten
analyseimport. `analyse.komitepilot` eier utvalg, navigasjon, sammenligning og
streng offline-gjenlesing. Excel har egen skriver/leser. Ingen database kreves.
En validert `visningspilot-1` er ett valgfritt, uendret `legacy_json`-felt for
union; gamle objekter refereres med sine gamle ID-er og serialiseres ikke på nytt.

Konvolutten har nøyaktig `format,report`. Rapport har `id,basis,selection,
return_selection,view,version`. Basis har `id,rule,payloads,sources,documents,
inventory,statements,observations,contexts,relations,issues,legacy_json,version`.
De eksisterende immutable dokument-/inventar-/tekst-/kontekst-/relasjonsmodellene
og AmountObservation brukes med sine dokumenterte felt; ny betydning bindes av
T2-regelen, ikke av T1s rolleport. Utvalg og view bruker T1s feltkontrakt og union
av konkrete par/kapitler innen eksplisitte år, uten kryssprodukt. Navigasjon
bevarer returvalg. Globale dokumenter, helinventar og tekst består ved tomt valg.

Payload har `id,sha256,byte_count,content_base64,legacy_source_id`. ID er SHA-256
av de faktiske bytene. Nøyaktig ett av innhold og legacy-peker er satt. Identiske
byte gjenbrukes ved hash; URL/HTTP-forsøk og representasjoner bevares hver for seg.
Kilde har `id,name,document_key,media_type,expected_sha256,payload_id,status,
metadata_json`. Fravær/feil gir null payload og synlig status. Øvrige ID-er følger
`identity(navnerom,asdict(objekt med tom id))`; beløp bruker observasjon-1 med eget
kildesystem `komitepilot`, ikke oppdiktede B2-UUID-er. Ett kildefelt struktureres
én gang per versjon/tolkning/lokator. Kontrollparsing oppretter ingen objekter.

## Kilde- og rolleporter

Alle kildebyte og transportmetadata kontrolleres mot faste uavhengige hashankre.
Vellykket vedtak-HTML med sak 100887 er valgt beløpsrepresentasjon; 500-siden er
bare bevart feilbevis. API-objekt 208 og 209 rekonstrueres fra c5f3-forelderens
eksakte bytegrenser med dokumentert konvoluttoppskrift, uten ny HTTP-proveniens.
209/fullmakt II er eget dokument/tekst og ingen 208-beløpshendelse eller postkobling.

Ap/Sp/SV bindes til både #m2_2_1 og unntaket i #m3. Generell komitéstøtte og
H/V-merknad har egne roller/omfang. Særskilt votering i sak 24 kl. 19.49.48
binder I 315/78 til 63–35 og H/FrP/V-motstand. Enstemmighet for resten arves ikke.
Ingen tallfestet mindretallsvariant utledes. Sammenligning krever kildeverifisert
relasjon og kontekst, samme konto/år/betydning/enhet/omfang/detalj/runde og eksakte
roller. Manglende stadium gir hull; øvrig ukjent/motstrid gir sperre, aldri null.

Leseren rekonstruerer alle nye objekter fra verifiserte byte og avviser felt-,
rolle-, aktør-, lokator-, relasjons- og ID-avvik også etter rehash. JSON har eksakt
feltskjema, duplikatnøkkel-/NaN-vern, 64 MiB total, 16 MiB/payload, 32 MiB gzip,
64 kilder/payloads, 16 dokumenter, 512 inventar/tekst, 256 beløp, 1024 relasjoner.
Legacy valideres med gammel streng leser, høyst én kapsel. Kapselens arvede kopier
telles separat; det gamle formatet omtales ikke som fullt normalisert.

## Excelprofil

Ny profil etter [faneanalysen](research/faner-og-kildedeling/README.md): Forløp,
Dokumenter (inkludert globalt helinventar), Omtale (full tekst/hierarki),
Sammenligninger, Dekning og avvik. Tilgjengelige kontrollark viser bevisrelasjoner,
kildeindeks og én kanonisk offlinepakke. Ingen ekstra base64-originalfane.
Synlige felt er projeksjoner/referanser, ikke nye kildeobjekter. Kildetekst og
JSON deles tapsfritt i ordnede 30 000-tegnsstykker; formeltegn lagres som tekst.
Alle celler, lenker, tallformater, effektiv stil, ark-/rad-/kolonnevisning og
filter kontrolleres mot rekonstruert bok. ZIP/XML/ressursvern før openpyxl
avviser makroer, eksterne lenker, regler/tegninger og uventede ark/objekter.

Ingen faglig godkjenning, full årsdekning, kontokontinuitet eller driftsaksept.
K1s positive parallellforslagsport, T3–T6/K1–K3 og generell faneopprydding er åpne.
#10 står åpen. Nyregistrering av offisielle vedtak kjører uavhengig av T2-feil.
