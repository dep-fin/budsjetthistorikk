# Sak 101000: lønnsoppgjøret 2024 og 1429/1, /22

Kildeundersøkelse for [#54](https://github.com/depmartin/budsjetthistorikk/issues/54),
del av #37, utført 28. oktober 2026 fra P1-main
`6b2441ee5e859d103ab44d78f12d33c374a89171`. Dette er separat forskningsgrunnlag,
uten produktadopsjon, nye beløpsobservasjoner eller faglig årsaksept.

## Resultat

**Sak 101000 gir ingen ny belagt direkte monetær hendelse på 1429/1 eller /22.**
Prop. 34 S → Innst. 91 S → vedtak 230/231 har en annen bevilgningspost og
en generell lønnsregel. Den konkrete krysshenvisningen til nysalderingen
gir derimot selvstendig kildebevis for **1429/1s foreslåtte lønnskompensasjon
på 2 796 000 kroner**, samt en relevant generell overføringsfullmakt.
Faktisk fullmaktsbruk hos Riksantikvaren og lønnsregelens anvendelse på
konkrete ansatte er uavklart.

| Kildeinnhold | Omfang og rolle | Betydning for 1429 |
| --- | --- | --- |
| 230/40034098, 17.12.2024 | Budsjett 2024: **1560/71**, +14 200 000 fra 233 100 000 til 247 300 000 kroner, opplæring og utvikling av tillitsvalgte | Annen post. Kapittelnavnet «Tariffavtalte avsetningar» gjør ikke dette til sentral fordeling av lønnskompensasjon til 1429. |
| 231/40034099, 17.12.2024 | Generell lønnsregel for bestemte embetsmenn/statstilsette utenfor hovedtariffavtalene; administrative kontrakter for stillinger tatt ut av avtalene | Ingen konkret kapittel/post eller beløpsfordeling. Riksantikvarens personell-/avtaleforhold er ikke dokumentert her. |
| Prop. 36 vedlegg 4, tr292–294 | Overskrift «4 Endring av utgifter som følge av lønnsoppgjøret for statsansatte», tabellhode «Kroner»: 1429 Riksantikvaren → post 1 Driftsutgifter → **2 796 000** → neste kapittel 1471 | Selvstendig kildeobservert kompensasjonsanslag med forslagsrolle. Ingen /22-rad i akkurat denne kapittelblokken. |
| Prop. 36 kapittel 5 | Normalt FIN-fullmaktsopplegg omtales separat. I 2024 innarbeides anslag ved nysalderingen, basert på YS Stat-avtalen; postvirkningen vises i departementenes omgrupperinger og vedlegg 4 | Forklarer forbindelsen til Prop. 16. Ingen påstand om at Prop. 34 har en postvis fordelingsfullmakt. |
| 429/40034289, 19.12.2024 | FIN kan øke maksimalgrensen for overføring av ubrukt drift til 2025 tilsvarende lønnskompensasjonen for 2024 og fastsette en minsteoverføring for utsatt etterbetaling | Potensiell /1-relevans gjennom kompensasjonsraden. 429 nevner ikke 1429. Vilkår, konkret bruk og faktisk overført beløp er ukjent; ingen ny 2024-/2025-bevilgningshendelse. |

Vedlegg 4s eksakte felt er **ikke beregnet fra 210**. Belegget er tr293/td4,
rått `2 796 000`, med kapittelrad tr292, postcelle tr293/td2 og enhet i
tabellhodet. Prop. 36 kapittel 5 merker beregningen som et anslag. Det er
et kildeobservert tall for et foreslått anslag, ikke et nytt selvstendig
vedtatt lønnsbeløp. Eksakt XPath er
`/html/body/main/div/div[3]/div[3]/div/div/table/tbody/tr[293]/td[4]`.

O1s Prop. 16 `#kap2-p24` beholder avrundet **2,8 mill.**, og regnestykket
5 796 000 − 3 000 000 beholder rollen **beregnet rest**. Samme tallverdi
i vedlegg 4 gir nytt kildebevis med egen rolle; O1-teksten og beregningen
omklassifiseres ikke. Post 22s `#kap2-p25` gjelder omdisponering til post 1
og arver ingen lønnsforklaring. Ingen tilleggshendelse opprettes utover 210.

## Hovedsak og behandlingskjede

Prop. 34 er bevart med forside, alle fem publiserte HTML-kapitler og full
PDF på fire sider. De dekker innledning, lønnsforhandlinger, generell
lønnsregulering, 1560/71, tilråding og begge vedtaksforslag. Innst. 91 er
bevart både som inngangsside og komplett `?all=true`. Hele debatten i
sak 6 og hele den relevante voteringsblokken 17. desember er bevart.
Saks-API, saks-voteringer, forslag og voteringsvedtak har egne originaler.

| Trinn | Kildebevis og lokalisering |
| --- | --- |
| Identitet | K3 `/s:saker_oversikt/s:saker_liste/s:sak[624]`, sesjon 2024–2025: sak 101000, innstilling 16626. Ny saksrespons har alle dokument-/referatlenker. `IDX624`, `R30`. |
| Regjeringen, 29.11.2024 | Prop. 34 kapittel 5, I-tabell `/html/body/main/div/div[3]/div[3]/div/div/div[1]/div/table`; II samme hoveddel `div[2]/p[1]`. §2.1 viser til de postvise nysalderingsforslagene. `R11`, `R16`, `R36`. |
| Samlet komité, 10.12.2024 | Innst. 91 `#m3` har samlet tilråding I/II, med samme tabellbeløp og regel. `#m2_1` og `#m2_2` har ulike merknadsavsendere. `S-inn91-m3`, `R37`. |
| Forslag/endringer | `voteringsforslag?voteringid=23887`: **40077003 = I**, **40077004 = II**. Én registrert saks-votering; komplett debatt og voteringsblokk har de samme to tilrådingsleddene. Ingen ytterligere fremsatt/endret posttabell er funnet i dette behandlingsgrunnlaget. `S-debatt6`, `R26`, `R31`, `R33`. |
| Votering | **23887**, 17.12.2024 kl. **19:29:21.12**, tema «Romertallene I og II.», `enstemmig_vedtatt`. Referatet sier samrøystes. APIets `antall_for/antall_mot=-1` blir ikke faktiske stemmetall, 0 eller et oppfunnet antall. `R26`, `R31`. |
| Endelig vedtak | Voteringsvedtaks-API binder **I → 230**, **II → 231**. Hele sesjonsobjektene binder nummer, sak, dato, **40034098/40034099** og ordlyd. De er også C14N-like i eldre c5f3-original; begge HTTP-konvolutter beholdes. `R32`, `D40034098`, `D40034099`, [sammenligning](source-comparison.json). |

Ulike merknader om tariffavtaler, uorganiserte og organisasjonsfrihet
tilskrives sine navngitte avsendere. De er ikke tallfestede alternative
tilrådinger. Samlet tilråding og enstemmig vedtak gjør ikke alle
begrunnelsene til Stortingets felles vedtaksordlyd.

Den eneste fulgte sidegrenen er FINs lønns-/overføringshenvisning:
**Prop. 36 forslag II → Innst. 90 tilråding II → forslag 40078386 →
votering 23945, 19.12.2024 kl. 14:39:29.063 → vedtak 429/40034289**.
Temaet er resten av I samt II–IV, enstemmig vedtatt. Vedtaksreferansen
identifiserer 429 særskilt som II; 430/431 arver ingen 1429-kobling.
Hele Innst. 90 er råbevart, men bare denne relevante grenen er strukturert.
De øvrige R2-sakene utvides ikke.

## Krysshenvisninger og restgrense

[Kryssreferansejournalen](cross-reference-journal.json) har tolv begrunnede
oppføringer, med undersøkt delomfang eller uttrykkelig uavklart status.
Postkoblingen bygger på vedlegg 4 og kapittel 5 i Prop. 36, ikke på
felles tittel, sak eller ordfravær.

En kildekonflikt beholdes: Prop. 34 og Innst. 91 omtaler Stortingets
samtykker **20. juni 2024**, mens de komplette API-objektene for
**853–856**, sak 99235, har dato **21. juni 2024**. Hele juni-sakens
proposisjon, innstilling og referat er ikke undersøkt. Ingen dato
korrigeres; de fire vedtakene er ikke nye 1429-beløpsbevis.

Åpne forhold er:

- Personell-/avtalegrunnlag for faktisk anvendelse av 231 hos Riksantikvaren.
- Vilkår, FINs fullmaktsbruk, utsatt utbetaling og faktisk overføring under 429.
- Originalene bak tariff-/nemndskjennelser, Prop. 108/Innst. 442, Prop. 21s
  stikkord, 2022-henvisninger og øvrige navngitte fag-/rettskilder. Grunn og
  undersøkt delomfang står per journalrad; ukjent betyr ikke ekskludert.
- Øvrige indekskandidater og andre deler av R1–R7, produktstrukturering,
  full årsdekning, kontokontinuitet, faglig årsbalanse og drift.

K3/P1s historiske registre beholdes: 67 indeksforekomster, 66 unike saker,
60 åpne indeksforekomster, 25 begrunnede vedtakskandidater og 2 158 objekter
uten ordbokstreff. 230/231 var søkeordfrie; denne undersøkelsen lukker
ikke R1 generelt. Hovedteksten til 101000 er nå undersøkt separat, mens
indirekte faktisk postvirkning fortsatt er uavklart. Ingen ny total eller
positiv M21 beregnes. Fem monetære posthendelser/elleve vedtaksfelt i
341 → 857 → 210 er uendret.

## Proveniens og kontroll

[Kildemanifestet](source-manifest.json) binder **22 nye transportforsøk**:
21 komplette HTTP 200-svar og ett DNS-feilet forsøk uten responsbyte.
Sistnevntes gzip er en tom capture, ikke et dokument. Mottatte byte,
arkivhasher og originale transportmetadata er bevart. Hvert HTML-kapittel
har egen observasjonstid; kapitlene er ikke én samtidig HTTP-observasjon.
[Gjenbruksmanifestet](reused-sources.json) refererer **19 eksisterende filer**
uten kopierte råoriginaler eller ny hentedato.

[Kildebelegg](evidence.json) har kildehash, XML-navnerom, eksakt XPath,
eventuelt eksplisitt indre HTML-felt, tekst og tabellceller. Whitespace i
avledet tekst kollapses etter oppgitt regel; originalene beholder alle byte.
[Behandlingsledgeren](treatment-ledger.json) skiller år, post, rolle,
forslag, generell regel, fullmakt, beregnet rest og uavklart faktisk bruk.
[Issue-snapshotet](context-snapshot.json) bevarer #37/#50/#52/#54 med
kommentarer; siste P1-overlevering er gjeldende.

Byggerens engangshjelpere ligger bare i ignorert `.local/`; byggerfilene
er dokumentasjon og kilde-/kontrolldata. [Reproduksjonen](reproduksjon.md)
har de faktisk kjørte offlinekommandoene. [Kontrollresultatet](verification.json)
og [manifestet](delivery-manifest.json) gjelder byggerens arbeidsfiler og
erstatter ikke uavhengig kildekontroll, full Linux-CI eller bekreftet merge.
PDF er tekstkontrollert, ikke visuelt kontrollert eller nyutgitt.

[Overleveringen](OVERLEVERING.md) angir leveringsportene. #10/#32/#37 står
åpne. Ingen neste ticket startes av denne leveransen.
