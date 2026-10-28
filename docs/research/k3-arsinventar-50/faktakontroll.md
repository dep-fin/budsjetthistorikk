# Uavhengig faktakontroll og målrettet F1-etterkontroll

Den uavhengige dokument-/spec- og faktakontrollen 28. oktober 2026 gjelder
**bare kandidat `5b6e86c13411ac703976447c5c21fc005f83b6a2`**, mot
`37c6ad4572c030a6b3309201d836bb0c0c51f9c6`. Den fant ett nødvendig
leveranseavvik, F1. Kunnskapsinnholdet bestod som presist avgrenset
restusikkerhet; positiv M21/helårsaksept er fortsatt åpen.

Full [opprinnelig rapport](faktakontroll/rapport-5b6e86c.md) og
[opprinnelige måleresultater](faktakontroll/resultater-5b6e86c.json) er bevart
byteeksakt fra `outputs/k3-factcheck/rapport.md` og `results.json` utenfor repoet.
Rapport: 9000 byte, SHA-256 `51e5df33412bebaac36447a5c9e27e4e5b8f5659ab0a8339ddac9ecc0f3fe9d7`.
Resultater: 3551 byte, SHA-256 `740c52072366bd34791bedfb3d92fdee615e72172097445830d2adf8c977e822`.
De opprinnelige filene er historisk bevis og beholder derfor F1 som funn;
de er ikke omskrevet til å beskrive en senere kandidat som kontrollert.
Kontrollhjelperen `outputs/k3-factcheck/factcheck.py` er ekstern og inngår
ikke i leveransen.

## F1 og konkret etterkontroll

F1 bandt `docs/kildefunn.md` til lokale CRLF-byte (59 854 byte,
SHA-256 `4491b4f28415d12441c199cc88c6f6a5ddafb1dcf537c447e51e906c5eb1c37c`).
Den faktiske Git-bloben i opprinnelig kandidat er **59 469 byte**,
SHA-256 `b80c0d294f7c0a801cb80305b2394c40c885116ed108bfc27bc7089e65ce09c6`,
Git-blob-ID `2405cf3c41661d104f0e5443dcb6b962bdfd67f8`.

Etterkontrollen leste denne bloben med `git show` som binær prosessoutput.
Nøyaktig 385 CRLF-par i arbeidsfilen blir LF; resultatet er byteidentisk
med Git-bloben. Med bare den korrigerte oppføringen stemmer samtlige
**113/113 opprinnelige manifestposter** mot de faktiske Git-blobbene;
den korrigerte summen for dette opprinnelige filsettet er **7 224 692 byte**.
Ingen forskningskilde eller kildehash er normalisert.

F1 er rettet i arbeidsleveransen ved schema `k3-delivery-manifest-2` og en
uttrykkelig `utf-8-lf`-regel bare for `docs/kildefunn.md`. Alle øvrige filer
følger `exact-file-bytes`. Oppskriften og Git-kontrollen står i
[reproduksjon](reproduksjon.md#leveransemanifest). Manifestet er regenerert
etter dokumentendringene; dets aktuelle antall og sum omfatter også de
bevarte kontrollfilene ovenfor.

## Grense for utfallet

Dette er målrettet lukking av F1 med faktisk Git-bytebevis for den berørte
originalbloben, og kontroll av det oppdaterte arbeidsmanifestet. Det er
**ingen ny uavhengig faktakontroll eller samlet sluttport for en senere
commit**. En ny fast kandidat må bindes til den faktisk etterfølgende
leveringskontrollen; PR/CI/merge føres separat av orkestratoren.
Opprinnelig rapports begrensninger gjelder fortsatt, herunder åpne
semantiske årsrester, ingen produkt-/native Excel-/produksjonsaksept og
ingen faglig årsbalanse. Ingen senere byggesnitt er startet.
