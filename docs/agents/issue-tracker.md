# Issue tracker

## Plassering

Spesifikasjoner, undersøkelser og byggetickets ligger i GitHub Issues i `depmartin/budsjetthistorikk`. GitHub er kilde for status, akseptansekriterier og blokkeringer. Les hele issuet og relevante kommentarer før arbeid.

Bruk tilgjengelig GitHub-kobling eller en autentisert GitHub CLI. Verktøyvalget endrer ikke arbeidsmetoden. I oppsettsøkten var GitHub-koblingen tilgjengelig, mens CLI-en gh ikke var installert.

## Relasjoner og status

Bruk native sub-issues og avhengigheter når tilgjengelige verktøy støtter dem. Ellers angis `Del av #N` og `Blokkert av #N` i issue-teksten. Opplys om at slike referanser er tekstlige; de er ikke native GitHub-relasjoner.

GitHub-koblingen i oppsettsøkten eksponerte ikke skriving av sub-issue- eller blokkeringsrelasjoner. Dette må kontrolleres ved publisering av byggetickets. En foreldreissue er kravkontekst, ikke en blokkering som må lukkes før barn kan starte.

Bruk status i teksten: under avklaring, foreslått, startklar, pågår eller ferdig. Oppdater status og kontrollresultat ved overlevering. Det er ikke opprettet triage-etiketter fordi triage-skillen ikke er tilgjengelig.

## Publisering

Følg [arbeidsflyten](../arbeidsflyt.md) ved oppdeling og publisering av byggetickets. Bevar eksisterende krav og kommentarer når et issue oppdateres. Pull requests brukes til kodeendringer; de er ikke en egen inngang for nye behov.
