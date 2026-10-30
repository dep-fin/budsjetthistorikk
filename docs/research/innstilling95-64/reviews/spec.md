# Uavhengig Spec-review av T6/#64

30. oktober 2026. Base `9616fbe6a8ab15eec696f34de76888565a784f8f`;
HEAD `fc9b676ce6e2f361433f2562bcdf91930302c21e`;
tre `93fee86f5b117c076136dd95d8d48b32fe1d1316`.
Diff: `git diff 9616fbe6a8ab15eec696f34de76888565a784f8f...fc9b676ce6e2f361433f2562bcdf91930302c21e`.
Én commit: «T6: hele Innst. 95 S og vedtak 359–364 gjennom begge innganger (#64)».

**Resultat: 0 bekreftede funn** om manglende/delvis oppfylte byggekrav,
scope creep eller feil implementerte krav. Hele kandidaten er vurdert,
ikke bare post 32. Grunnlag: live hele #64 (ingen kommentarer), #37,
#62 og relevante kommentarer/PR #63, AGENTS/arbeidsflyten, før-kode-kontrakten,
T1/T5-kontraktene, T5s gjeldende leveringsindeks og testmatrisen.

Faktisk etterprøving:

- Originalfasiten er regenerert med `node .../independent/oracle.cjs --check`.
  Alle 216 nye felt er sammenholdt med separat fasit; egne kontroller
  evaluerte hver produkt-XPath mot original HTML eller XML-objektets
  HTML-felt og avstemte råtekst, feltbetydning, kildehash, verdi, år,
  rolle og felles step_id. Alle seks recipes ga byteidentiske bevarte XML.
- Alle 35 Prop.-trioer og 95→359 gir henholdsvis 105 og 108 nullforskjeller;
  T1s 12 består. Tre manglende Prop.-felt for 1420/32 gir hull/null,
  mens 4400/2 beholder numerisk observert 0. Unionen er 339/114/38.
- Åtte fullmaktspunkter per stadium er avstemt mot originalvilkår,
  rammer, roller og kontoomfang. Delt 16,3-millionersramme multipliseres ikke.
  Fem nye formelle vedtak og bevart 211 gir ingen ekstra monetær hendelse.
  Partimerknader, samlet tilråding og plenumsutfall er adskilt;
  1429/1533 får ingen feil T6-beløpsgren.
- Målrettet pytest: **10 bestått, 33 fravalgt, 458,65 s**. Dette omfatter
  25 faktisk skrevne/lukkede/gjenleste JSON/XLSX-par, begge returer,
  offline-CLI, autentisk legacy og fire ordinære 40034229-forløp,
  hvert med 222 observasjoner/74 hendelser. Tre eksisterende CLI-par
  er dessuten gjenlest uavhengig med celle-/lenkekontroll.
- Alle 35 råpayloads samsvarer med bevarte filer og HEAD-blobber;
  seks rekonstruerte originaler og 42 eksportfiler er kontrollert.
  15 kandidatbindinger for rå/LF/Git-filter/HEAD består.
  1409 tidligere sporede filer er identiske; eneste gamle endring er
  den additive AGENTS-pekeren. Hele typede T5/T1-basis er uendret.

Fullsuiten er ikke gjentatt. Dette er lokal Spec-aksept; separat audit,
fersk offentlig klon, publisert head/CI og merge er orkestratorporter.
Native Excel, full teksttolkning, rettelseshistorikk, helårsdekning,
kontinuitet, faglig årsbalanse og drift er ikke etablert.
