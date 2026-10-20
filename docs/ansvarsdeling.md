# Ansvarsdeling

## Innlesning

Innlesningsdelen skal håndtere kildeoppdagelse, henting, kildebevaring, identifikasjon av nye og endrede opplysninger og strukturering. Den skal gi sporbarhet fra hvert strukturert element til kilden og kunne kjøres uten analysegrensesnittet.

Foreslått plassering er `innlesning/`. Detaljert kodeorganisering avklares når teknologistakken er valgt.

## Datagrunnlag

En felles datakontrakt skal beskrive identifikatorer, sesjon, budsjettår, kapittel, post, beløp, beløpets betydning, kilde og forholdet mellom forslag og vedtak. Kontrakten skal skille mellom regjeringens forslag, komitéforslag og endelige vedtak.

Valg av database er åpent. Data skal kunne leveres videre uten å binde innlesningen til et bestemt fremtidig mottakersystem.

## Analyse og fremstilling

Analysedelen skal bruke det dokumenterte datagrunnlaget til søk, sammenligning, fremstilling og eksport. Den skal vise kildehenvisninger og opplyse om datakvalitet og dekningsgrad.

Foreslått plassering er `analyse/`. Visuelle grensesnitt og eksportformater avklares ut fra Finansavdelingens arbeidsoppgaver.

## Endringer på tvers

Endringer i felles datakontrakt skal beskrive konsekvenser for begge deler. Fremtidige byggetickets skal angi hvilke deler de berører. Samlet repo krever ikke samlet driftssetting.
