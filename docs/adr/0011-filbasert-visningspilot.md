# ADR 0011: separat filbasert visningspilot

Besluttet 27. oktober 2026 innen eiergodkjent T1/#41, før produktkode.

Vi velger separat opt-in-konvolutt visningspilot-1 med selvforsynt,
innholdsidentifisert grunnlag og avledet dokument-/konto-/årsutvalg. O2b-konvolutten
bevares ordrett; nye forslag-/tilrådingsobservasjoner og behandlingskontekst
ligger utenfor gamle lukkede formater. JSON/Excel kan gjenleses uten database/nett.

Alternativet var å utvide B6/B8/O2 eller innføre nytt databaseskjema. Det ville
endret leverte kontrakter eller koblet et lite snitt til en større plattform.
Separat format krever egen streng leser og kompatibilitetskontroll, men bevarer
gamle ID-er, B5-status, schema 5 og uavhengig vedtaksinnlesning.

[Kontrakten](../visningspilot.md) fastsetter felt, ID-regler, kilde-/rollekontroll,
utvalgssemantikk, sammenligningsporter, grenser og frossen akseptledger.
Ingen generell T2+-plattform, årsdekning, kontinuitet, mindretall eller drift.
#10 står åpen.

Presisert etter review 27. oktober: analyseorkestreringen eier lesing av de
tidligere analysekonvoluttene og leverer typet `PilotInput` til kildeadapteren.
Adapteren validerer råkilder og rekonstruerer alle seks gamle vedtaksobjekter
mot kjent tolkning uten analyseimport. T1s separate leser kontrollerer også
presentasjonsegenskapene som bestemmer synlige verdier; gamle lesere endres ikke.
