# Samlet kontroll av portabilitetsrettingen

De tre uavhengige kontrollene vurderer hele kandidaten mot base
`49cc6e44851cf74e0aaea4eb333419e5598bfd95`, med særlig kontroll av
portabilitetsrettingen og at de tidligere faglige attestene fortsatt gjelder.

| Binding | Eksakt verdi |
| --- | --- |
| Lokal fast kandidat | `6204702d5da0ade04f368a6fb4a7b39b73df011a` |
| Tilsvarende publisert kandidat | `d11a55d70e347462e2492a8332feb36e34c06b35` |
| Identisk tre | `79ea3e464984d7ad0aaca55669a68ab0fd0ad96c` |
| Publisert forelder | `92b43c2ce7ec350e10639bd0c75540da0d83ee72` |

GitHub-publiseringen bevarer den gjennomgåtte kandidaten som egen commit
før disse dokumentariske sluttrapportene legges til. Tre- og bloblikhet
gjør det mulig å inspisere den eksakte gjennomgåtte filkandidaten i GitHub.
Den lokale commitens andre author-/committermetadata gir et annet commit-ID.

## Standards

[Uavhengig rapport](standards.md): 0 dokumenterte regelbrudd og 0
vesentlige smells. Kandidatbindinger, historiske attester, manifesthasher
og isolert bundleimport/regenerering er kontrollert.

## Spec

[Uavhengig rapport](spec.md): 0 funn. En separat GitHub-klon bekrefter
manglende historiske committer før import, eksakte objekter og trær etter
import, byteidentisk regenerering og samme resultater fra alle fire
historiske maskinkontroller, bortsett fra tidspunkt.

## Separat sikkerhetsaudit

[Uavhengig rapport](security.md): 0 funn, P0–P3. Bundle/hash,
objektlukning, import, negative ref-/feilprøver og tidligere sikkerhetsporter
er kontrollert. Den publiserte kjeden beholder 92b som ancestor; den lokale
620-committen gjør ikke det. Lokal og publisert historie må derfor ikke
forveksles selv om de gjennomgåtte trærne er identiske.

## Historiske kandidatobjekter og leveringsgrense

De eksakte 9eb-/d241-/9efa-objektene som de opprinnelige maskinkontrollene
bruker, bevares i [kandidatarkivet](../history/README.md). Arkivet har
SHA-256 `051ca0279fb61b5ddd3b77a83c09f172c8ac142e1cd2240dfac6fdca2ab7074d`.
Følg [reproduksjonsveiledningen](../../reproduksjon.md) i en fersk klon.

Dette tillegget omfatter bare reviewrapporter og publiseringsbindinger;
det endrer ikke den gjennomgåtte kjørbare kandidaten eller kildebevisene.
Full CI og faktisk merge er egne leveringsporter. Gjeldende sluttstatus
lagres i [#60](https://github.com/depmartin/budsjetthistorikk/issues/60) og
[PR #61](https://github.com/depmartin/budsjetthistorikk/pull/61).
