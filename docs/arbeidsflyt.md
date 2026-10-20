# Fast arbeidsflyt med issues

Dette er prosjektets arbeidsmetode. Den bygger på Matt Pococks skills og kan brukes som utgangspunkt for en felles metode i Finansavdelingen. Innføring som avdelingsstandard er en egen beslutning.

Metodegrunnlaget er versjonsfestet til [Matt Pococks skills, revisjon 5beb35b](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2), kontrollert 20. oktober 2026. Endringer i prosessgrunnlaget skal gjennomgås og dokumenteres før de tas i bruk.

## 1 Avklar behovet

Bruk grilling i runder. Be om beslutninger som har avklarte forutsetninger, og gi anbefalinger. Agenten undersøker fakta. Oppdater kravgrunnlaget etter brukerens svar. Avslutt intervjuet når brukeren har bekreftet den samlede forståelsen. [Grilling](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/grilling/SKILL.md)

## 2 Samle en spesifikasjon

Sammenfatt avklarte behov med problem, løsning, brukerhistorier, implementeringsbeslutninger, testbeslutninger og avgrensninger. Spesifikasjonen skal beskrive ønsket atferd. Dokumenter hvilke tester og kontrollgrunnlag som er avtalt. En spekulasjon blir ikke et godkjent krav ved at den skrives inn i spesifikasjonen.

Bruk en overordnet GitHub-issue som gjeldende leveransespesifikasjon. Inntil avklaringene er avsluttet, er #1 et kravgrunnlag under arbeid. [To spec](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/to-spec/SKILL.md)

## 3 Del i små komplette leveranser

Hver byggeticket skal gi en smal, komplett og etterprøvbar funksjon gjennom lagene som trengs for den funksjonen. En ticket skal passe i én fersk agentkontekst. Unngå en oppdeling som bare lager database, parser og grensesnitt hver for seg uten et kontrollerbart resultat.

Vis foreslåtte tickets, leveranser og reelle blokkeringer samlet til brukeren før publisering. Etter godkjent oppdeling opprettes tickets i avhengighetsrekkefølge som barn av spesifikasjonen. Bruk native GitHub-relasjoner når verktøyene støtter det; ellers tydelige foreldre- og blokkeringsreferanser.

Undersøkelsesissues er egne avgrensede kunnskapsleveranser. De skal ikke gi inntrykk av ferdig produksjonsfunksjonalitet. [To tickets](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/to-tickets/SKILL.md)

## 4 Gjennomfør startklart arbeid

Les hele ticketen, kommentarer, spesifikasjonen og relevante begreper før start. Velg bare arbeid med avklarte blokkeringer og mandat. Bruk TDD innenfor avtalte testgrenser: test observerbar atferd og gjennomfør små test-/implementeringssteg. Kjør relevante tester og statiske kontroller. Dokumenter konkrete begrensninger.

For innlesningen bør kontrollene blant annet dekke klassifikasjon av kapittel, kildehenvisninger, beløpstolkning, gjentatt kjøring og tvetydige uttrekk. Testgrensene er godkjent i #1. B1 implementerer den smale grensen kilde → lagring → Excel; øvrige kontroller følger ticketoppdelingen. [Implement](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/implement/SKILL.md), [TDD](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd/SKILL.md)

## 5 Gjennomgå samlet

Gjennomgå hele kandidaten mot et fast sammenligningspunkt i to uavhengige spor: dokumenterte kodestandarder og oppfyllelse av spesifikasjonen. Rapportene skal angi konkrete funn og kontrollresultater. Rett nødvendige funn før fullføring. [Code review](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md)

## Prosjektets egne regler for levering

Følgende er lokale prosjektregler, og skal ikke omtales som generelle krav fra Matt Pocock:

- Én byggeticket gjennomføres på egen branch med én pull request.
- Pull requesten knyttes til ticketen og beskriver problem, resultat, kontroller og vesentlige konsekvenser.
- Tester og tilgjengelig CI skal være bestått før sammenslåing.
- Ticketen lukkes når leveransen er flettet og akseptansekriteriene er oppfylt.
- Endringer i kildegrunnlag, datakontrakt eller faglige regler dokumenteres sammen med koden.

Matts [PR-skill](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/pr/SKILL.md) gir veiledning om PR-beskrivelsen. Den fastsetter ikke generelt én PR per ticket.

## Start i en ny agentøkt

Les [AGENTS.md](../AGENTS.md). Oppgi issue-nummeret og om økten gjelder avklaring, undersøkelse, implementering eller review. Se [issue tracker](agents/issue-tracker.md) og [begrepsdokumentasjon](agents/domain.md).

## Tilgjengelige skills og versjoner

Det er et skille mellom denne versjonsfestede metoden og lokalt installerte plugins. I oppsettsøkten var pluginversjon 1.3.1 tilgjengelig med blant annet grilling, TDD, code review, PR og domain modeling. To spec, to tickets, implement og setup var ikke eksponert som kjørbare skills.

Ingen skills er installert eller oppgradert som del av dette arbeidet. Ved senere gjennomføring skal agenten kontrollere faktisk skilltilgjengelighet, bruke denne dokumenterte metoden og opplyse om eventuelle mangler. Ulike versjoner skal ikke blandes eller omtales som kjørt uten faktisk gjennomføring.

Ved B1-start 20. oktober 2026 ble filene for implement, to-spec og to-tickets funnet ved eksplisitt søk i den lokale pluginpakken 1.3.1. De vises fortsatt ikke i den aktive skillkatalogen. Filinstruksjonene kan leses og følges; dette er ingen påstand om en Skill-verktøyinvokasjon. B1 følger implement- og TDD-filene ved de allerede godkjente testgrensene. Det versjonsfestede prosessgrunnlaget ovenfor er bevart, og ingen skills er installert eller oppgradert.

## Kunnskap mellom agentøkter

Før en økt avsluttes, vurder hvilke nye funn som påvirker senere arbeid. Lagre varige kildefunn med observasjonsdato, kilde-ID eller URL, begrensning og konsekvens i [kildefunnene](kildefunn.md). Bruk en kort, oppgavespesifikk inngang fra AGENTS.md når funnet må leses før en bestemt type arbeid.

Begreper hører hjemme i GLOSSARY.md. Krav og avklarte produktvalg oppdateres i kravgrunnlaget og spesifikasjonen. Vesentlige arkitekturvalg dokumenteres som ADR når kriteriene i begrepsreglene er oppfylt. Gjennomføringsstatus og uavklarte punkter oppdateres i issuet.

Et viktig funn som allerede er dokumentert og kontrollert, skal være tilgjengelig fra hovedbranchens faste kontekst selv om den bredere undersøkelsen fortsatt er en utkast-PR. Lenke til en bestemt rapportrevisjon bevarer kildebevisene. En chatmelding eller lenke til en umerget PR alene er ikke tilstrekkelig kunnskapsoverføring.
