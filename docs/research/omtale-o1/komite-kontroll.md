# O1: kontroll av komitéleddet for 210/1429

Kontrollert 22. oktober 2026. Dette er en kildeundersøkelse under #32, ikke implementering eller faglig godkjenning av historikk. Originaler og innhentings-/hashmetadata inngår i denne mappens felles kildepakke. HTML-lokatorene nedenfor er kontrollert i de bevarte originalbytene, ikke bare søkemotorens tekstvisning.

## Originaler og lokatorer

* [Innst. 81 S, full HTML](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2024-2025/inns-202425-081s/?all=true): lokalt `originals/inns81s.html`.
* [Innst. 81 S, offisiell PDF](https://www.stortinget.no/globalassets/pdf/innstillinger/stortinget/2024-2025/inns-202425-081s.pdf): lokalt `originals/inns81s.pdf`. Trykt side 1 inneholder sammendrag og merknader; side 2 inneholder tilrådingen. PDF-sidetall bør brukes sammen med HTML-strukturen; PDF-uttrekkets leserekkefølge mellom spaltene kan være misvisende.
* [Plenumsreferat 16. desember 2024, votering](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/2024-2025/refs-202425-12-16?all=true#2024-12-16-25): lokalt `originals/votering-161224.html`, faktisk HTML-ID `2024-12-16-25`. Dette er et separat behandlingsbevis. Den offisielle [referat-PDF-en](https://www.stortinget.no/globalassets/pdf/referater/stortinget/2024-2025/refs-202425-12-16.pdf) har den relevante voteringen på trykt side 1503.

Alle `nth-of-type`/radnumre nedenfor er 1-baserte. Tekst, mellomrom og markup må fortsatt bindes til representasjonens hash i en senere strukturering.

| Lokator i Innst. 81 S | Hierarki og omfang | Kildeutsagn, parafrasert |
| --- | --- | --- |
| `#m1`, `#m1_1` | Sammendrag → Kap. 1429 Riksantikvaren | Innledningen angir forslag til statsbudsjettet for 2024. |
| `#m1_1_1 > div.krnl_chapter > p` | Sammendrag → kap. 1429 → Post 1 Driftsutgifter | 3 mill. kroner til egne stillinger skal redusere konsulentbruk i digital systemutvikling; finansieres fra post 22. Lønnsoppgjøret gir i tillegg anslått 2,8 mill.; samlet omtales 5,8 mill. |
| `#m1_1_2 > div.krnl_chapter > p` | Samme kapittel → Post 22 | Reduksjon på 3 mill. foreslås omdisponert til post 1. |
| `#m2 > div > p` | Komiteens merknader, hele avsnittet | Medlemmer fra Ap, H, Sp, FrP, SV og V støtter regjeringens forslag. Navnene står i originalen. |
| `#m3 > div > p`, deretter `#m3 div.strtngt_komiteen > p` | Komiteens tilråding | Tilrådingen fremmes samlet, med henvisning til proposisjonen. |
| `#m3 div[data-strtngt-romertallseksjon-romertall='i'] table tbody` | Tilråding → I → kap. 1429 | Rad 1 gir kapittel; rad 2–3 gir post 1 +5 796 000, før 160 243 000, etter 166 039 000; rad 4–5 gir post 22 −3 000 000, før 32 185 000, etter 29 185 000. |

For postomtalen skal `#m1` og `#m1_1` beholdes som forfedrekontekst, selv om HTML-en har seksjonene som søsken. Bevar hele postavsnittet. Post 1-avsnittet gjelder også post 22 og to forskjellige forklaringsledd; en løsrevet første setning mister dette omfanget.

## Roller og dokumentert kobling

Sammendraget er innstillingens gjengivelse av regjeringens forslag. Det er ikke en ny selvstendig komitébegrunnelse. Komiteens uttrykkelige støtte i `#m2` og samlede tilråding i `#m3` skal registreres som egne behandlingsbelegg. Hele innstillingen er kontrollert: ingen mindretallsmerknad, avvikende beløpsforslag eller særskilt flertallskonstellasjon er funnet. Riktig rolle her er **samlet komité**; piloten gir ingen autentisk prøve av uenighet mellom flertall og mindretall.

Voteringsseksjonen `#2024-12-16-25` gjengir I med samme konti, beløp og før-/etterverdier og avsluttes med at innstillingen ble enstemmig vedtatt. Dette dokumenterer komitéforslagets vedtakelse; den bevarte vedtaksoriginalen 40034048/210 identifiserer selve beløpsvedtaket. Koblingen skal bygge på denne kjeden, ikke bare likt beløp eller felles sak. Henvisning til proposisjonen gjør heller ikke samtlige regjeringspremisser til vedtaksordlyd.

## Tolkningsgrenser og negative kontroller

* Avsnittet gir kildebelegg for omdisponeringen mellom postene. Det beviser ikke at hele økningen på post 1 skyldes redusert konsulentbruk.
* Differansen 5 796 000 − 3 000 000 = 2 796 000 er en beregning. Omtalens avrundede 2,8 mill. er ikke et selvstendig eksakt lønnsbeløp på 2 796 000. Henvisningen til Finansdepartementets nysalderingsproposisjon er et videre kontrollspor; detaljgrunnlaget er ikke kontrollert her.
* Omtalen bruker «kulturmiljøforvaltning», mens tilrådingens tabell bruker «kulturminneforvaltning». Bevar begge rånavn; kapittel/post og behandlingsbevis dokumenterer koblingen uten en skjult tekstretting.
* `#m1_1_3` og tilrådingens II gjelder post 60 og stikkordsfullmakt. De er nødvendig nabokontekst, men forklarer ingen ekstra beløpshendelse under 210. Vedtak 211 holdes separat.
* Den felles plenumsdebatten om sakene 23–25 nevner et mindretall i omtalen av Prop. 25 S/Innst. 85 S. Slik debattkontekst gir ikke et mindretall under Innst. 81 S og skal ikke tilordnes post 1/22 uten eget belegg.
* O2 kan bruke denne saken til å prøve full kildekjede, flere forklaringer og mange-til-mange-omtale. O3 trenger en annen autentisk sak for en faktisk komitéendring og flertalls-/mindretallsroller.
