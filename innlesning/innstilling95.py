"""Fast beriktiget95/359–364-adapter. Ingen analyse, database eller nett."""

import base64
import gzip
import hashlib
import io
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import cast

from lxml import html

from .innstilling95_model import RULE, Basis, CoverageOverlay, SourceRecipe
from .legacy_html import parse_legacy_html
from .observations import AmountObservation, Interpretation, SourcePointer, encode, identity
from .omtale import compact, identified
from .proposisjon16 import validate_basis as validate_t5
from .proposisjon16_model import Authorization, FieldBinding
from .proposisjon16_model import Basis as T5Basis
from .visningspilot import MAX_PARENT_BYTES, MAX_SOURCE_BYTES, _xml, raw_source
from .visningspilot_model import (
    InventoryItem,
    PilotDocument,
    PilotInput,
    PilotRelation,
    PilotSource,
    Statement,
    TreatmentContext,
)

ROOT = "docs/research/to-visninger-37/originals/forgrening/"
PARENT_SHA = "c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42"
NS = "{http://data.stortinget.no}"
SOURCE_CATALOG = {
    "40034220.json": "51ce336742b445f6fa23945029d7814e51b7e3eb838e65c4f438d3b87524abc5",
    "40034221.json": "4413b8cb072a3a164b8d2572352ff13752e67810cf896f9c5996801f55e3ca31",
    "40034222.json": "698e198a59f7afd29a5f55e6c8dbdeeb796adf00dbe7dc2764324ba66a930804",
    "40034223.json": "7e9b5607935fa4944ae50e9afc3e6bd7daba64f45a5455543d468eddc83031f3",
    "40034224.json": "a61a7e140440bff8ec149b3e862d6d764958f27dc66d88a0a9fc9f7fef401c79",
    "40034225.json": "504bf16ba6184409c17b20b907461b52ec6ef7f3354553b4cefec1b89a6a62cb",
    "sak-100889.xml": "435985bb9cc454d32f4b5c2e0df1e07ef48146dfdb2bf4a456db4df091f00859",
    "sak-100889.html": "279943f8df41d5ae940284c11fd6773b52921f45e093265c046c55b888a2026b",
    "vedtak-100889.html": "f58ec94336da10d04046e09683bf83d6a72d3a2ddbf42a7b106f194472ef72f3",
    "votering-181224.html": "88553153fd4011b6b3aa041c7899701bd7f7a938f2ad1984aecd4c441d24a9d9",
}
MEANINGS = ("for_belop", "endring", "etter_belop")
AUTH_SPECS = (
    ("II", "1", "bestillingsramme", ("1420/21",), 8_000_000),
    ("III", "1", "tilsagnsramme", ("1420/61",), 601_000_000),
    ("III", "2", "tilsagnsramme", ("1420/62",), 266_300_000),
    ("IV", "1", "felles_forpliktelsesramme", ("1420/39", "1420/69", "1420/79"), 16_300_000),
    ("V", "1", "stikkord", ("1420/66",), None),
    ("V", "2", "stikkord", ("1420/87",), None),
    ("VI", "1", "forskutteringsramme", ("1471/1", "4471/3"), 25_000_000),
    ("VI", "2", "regnskapsregel", (), None),
)


def _source(name: str, raw: bytes | None, metadata: str) -> PilotSource:
    meta = json.loads(metadata)
    wanted = {"repository_path"} if raw is not None else {"repository_path", "error_type"}
    if (
        not isinstance(meta, dict)
        or set(meta) != wanted
        or metadata != encode(meta)
        or meta["repository_path"] != ROOT + name
        or raw is None
        and (not isinstance(meta["error_type"], str) or not meta["error_type"])
    ):
        raise ValueError("T6: ugyldig lokal kildemetadata")
    digest = hashlib.sha256(raw).hexdigest() if raw is not None else None
    return identified(
        "innstilling95-source",
        PilotSource(
            "",
            ROOT + name,
            "vedtak" + str(359 + int(name[:8]) - 40034220)
            if name[:8].isdigit()
            else "kontroll100889",
            "application/json"
            if name.endswith(".json")
            else "application/xml"
            if name.endswith(".xml")
            else "text/html",
            SOURCE_CATALOG[name],
            base64.b64encode(raw).decode("ascii") if raw is not None else None,
            digest,
            len(raw) if raw is not None else None,
            "mangler"
            if raw is None
            else "kildeverifisert"
            if digest == SOURCE_CATALOG[name]
            else "motstrid",
            metadata,
        ),
    )


@lru_cache(maxsize=2)
def _parent(t5: T5Basis) -> tuple[PilotSource, bytes | None]:
    parent = next(
        s
        for s in t5.t1_basis.sources
        if s.document_key == "forelder2024" and s.media_type == "application/gzip"
    )
    raw = raw_source(parent)
    if parent.status != "kildeverifisert" or raw is None:
        return parent, None
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as archive:
        expanded = archive.read(MAX_PARENT_BYTES + 1)
    metadata = next(
        s
        for s in t5.t1_basis.sources
        if s.document_key == "forelder2024" and s.media_type == "application/json"
    )
    meta_raw = raw_source(metadata)
    if metadata.status != "kildeverifisert" or meta_raw is None:
        return parent, None
    meta = json.loads(meta_raw)
    if (
        len(expanded) != 7479943
        or len(expanded) > MAX_PARENT_BYTES
        or hashlib.sha256(expanded).hexdigest() != PARENT_SHA
        or meta.get("sha256") != PARENT_SHA
        or meta.get("bytes") != len(expanded)
    ):
        raise ValueError("T6: feil vedtaksforelder eller foreldermetadata")
    return parent, expanded


def reconstruct(
    t5: T5Basis, sources: tuple[PilotSource, ...], recipe: SourceRecipe
) -> bytes | None:
    """Gjenfinn nøyaktige utdragsbyte, uten lagret utdrag eller ekstra forelder."""
    parent_source, parent = _parent(t5)
    sidecar = next(s for s in sources if s.id == recipe.sidecar_source_id)
    raw = raw_source(sidecar)
    if parent is None or sidecar.status != "kildeverifisert" or raw is None:
        return None
    meta = json.loads(raw)
    if recipe.parent_source_id != parent_source.id or (
        meta["source_response_sha256"] != PARENT_SHA
        or meta["source_response_bytes"] != len(parent)
        or meta["source_response"]["sha256"] != PARENT_SHA
        or meta["source_response"]["bytes"] != len(parent)
        or meta["inserted_separator_bytes"] != 0
        or (
            recipe.object_start,
            recipe.object_end,
            recipe.prefix_bytes,
            recipe.suffix_start,
            recipe.expected_sha256,
            recipe.expected_bytes,
        )
        != (
            meta["object_start_byte_0"],
            meta["object_end_byte_exclusive"],
            meta["prefix_bytes"],
            meta["suffix_start_byte_0"],
            meta["sha256"],
            meta["bytes"],
        )
        or recipe.document_key != sidecar.document_key
        or not 0
        <= recipe.prefix_bytes
        <= recipe.object_start
        < recipe.object_end
        <= recipe.suffix_start
        <= len(parent)
    ):
        raise ValueError("T6: ugyldig sidevogn/forelderbinding")
    separator = base64.b64decode(recipe.separator_base64, validate=True)
    result = (
        parent[: recipe.prefix_bytes]
        + separator
        + parent[recipe.object_start : recipe.object_end]
        + parent[recipe.suffix_start :]
    )
    if (
        separator
        or len(result) != recipe.expected_bytes
        or hashlib.sha256(result).hexdigest() != recipe.expected_sha256
    ):
        raise ValueError("T6: rekonstruert vedtaksutdrag avviker")
    return result


def _recipes(t5: T5Basis, sources: tuple[PilotSource, ...]) -> tuple[SourceRecipe, ...]:
    parent, expanded = _parent(t5)
    result = []
    for number in range(359, 365):
        name = str(40034220 + number - 359) + ".json"
        source = next(s for s in sources if s.name == ROOT + name)
        raw = raw_source(source)
        meta = json.loads(raw) if raw is not None and source.status == "kildeverifisert" else {}
        recipe = identified(
            "innstilling95-recipe",
            SourceRecipe(
                "",
                "vedtak" + str(number),
                parent.id,
                source.id,
                meta.get("object_start_byte_0", 0),
                meta.get("object_end_byte_exclusive", 0),
                meta.get("prefix_bytes", 0),
                meta.get("suffix_start_byte_0", 0),
                "",
                meta.get("sha256", ""),
                meta.get("bytes", 0),
                "kildeverifisert" if meta and expanded is not None else "mangler",
            ),
        )
        reconstruct(t5, sources, recipe)
        result.append(recipe)
    return tuple(result)


def _roman(root: html.HtmlElement, roman: str) -> html.HtmlElement:
    nodes = root.xpath(".//*[@data-strtngt-romertallseksjon-romertall=$r]", r=roman.lower())
    if len(nodes) != 1:
        raise ValueError("T6: fast romertall mangler eller gjentas")
    return cast(html.HtmlElement, nodes[0])


def _rows(
    root: html.HtmlElement,
) -> list[
    tuple[str, str, str, str, tuple[str, ...], tuple[int, ...], html.HtmlElement, html.HtmlElement]
]:
    result: list[
        tuple[
            str, str, str, str, tuple[str, ...], tuple[int, ...], html.HtmlElement, html.HtmlElement
        ]
    ] = []
    chapter, chapter_name = "", ""
    for table in root.xpath(".//table"):
        rows = table.xpath("./tbody/tr")
        for index, row in enumerate(rows):
            cells = row.xpath("./td")
            values = [compact(c.text_content()) for c in cells]
            if len(values) != 4:
                continue
            if values[0].isdigit():
                chapter, chapter_name = str(int(values[0])), values[2]
            if not values[1].isdigit() or not (
                "økes med" in values[2] or "reduseres med" in values[2]
            ):
                continue
            levels = rows[index + 1]
            match = re.fullmatch(
                r"fra kr ([\d ]+) til kr ([\d ]+)", compact(levels.xpath("./td")[2].text_content())
            )
            if not chapter or match is None:
                raise ValueError("T6: ufullstendig tabelltrio")
            raw_values = (match[1].strip(), values[3], match[2].strip())
            before, delta, after = (int(v.replace(" ", "")) for v in raw_values)
            if "reduseres med" in values[2]:
                delta = -delta
            if before + delta != after:
                raise ValueError("T6: originalens før/endring/etter avviker")
            result.append(
                (
                    chapter,
                    str(int(values[1])),
                    chapter_name,
                    values[2],
                    raw_values,
                    (before, delta, after),
                    row,
                    levels,
                )
            )
    if len(result) != 36 or len({(r[0], r[1]) for r in result}) != 36:
        raise ValueError("T6: fast tabell er ikke 36 unike kontoer")
    return result


def import_basis(t5_basis: T5Basis, prepared: PilotInput, root: Path = Path(".")) -> Basis:
    sources = []
    for name in SOURCE_CATALOG:
        path = (root / ROOT / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("T6: kildesti utenfor rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(MAX_SOURCE_BYTES + 1)
            if len(raw) > MAX_SOURCE_BYTES:
                raise ValueError("T6: råpayload overstiger16MiB")
            metadata = encode({"repository_path": ROOT + name})
        except (OSError, ValueError) as error:
            raw = None
            metadata = encode({"repository_path": ROOT + name, "error_type": type(error).__name__})
        sources.append(_source(name, raw, metadata))
    return structure_basis(t5_basis, prepared, tuple(sources))


@lru_cache(maxsize=2)
def structure_basis(
    t5_basis: T5Basis, prepared: PilotInput, sources: tuple[PilotSource, ...]
) -> Basis:
    validate_t5(t5_basis, prepared)
    if tuple(s.name for s in sources) != tuple(ROOT + n for n in SOURCE_CATALOG):
        raise ValueError("T6: ukjent eller manglende kildekatalog")
    for s in sources:
        if s != _source(s.name.removeprefix(ROOT), raw_source(s), s.metadata_json):
            raise ValueError("T6: kilderolle/hash/status avviker")
    old = t5_basis.t1_basis
    inns = next(d for d in old.documents if d.key == "inns95")
    original = next(
        s for s in old.sources if s.document_key == "inns95" and s.media_type == "text/html"
    )
    original_raw = raw_source(original)
    recipes = _recipes(t5_basis, sources)
    documents, inventory, statements, observations, contexts, relations, authorizations = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )
    issues = [
        "aarsdekning_delvis",
        "uberiktiget95_og_rettelsesmelding_ikke_funnet",
        "historisk_T5:inns95_belopsstadium_ustrukturert:T6",
        "inns95_to_beriktigede_html:ukjent_rettelseshistorikk",
        "fullt_inventar_og_tabell_ikke_full_faglig_teksttolkning",
    ]
    issues.extend(s.status + ":" + s.name for s in sources if s.status != "kildeverifisert")
    roots: dict[str, tuple[PilotDocument, str, str, html.HtmlElement]] = {}
    if original.status == "kildeverifisert" and original_raw is not None:
        roots["inns95"] = (
            inns,
            original.id,
            original.sha256 or "",
            parse_legacy_html(original_raw),
        )
    support_ok = all(s.status == "kildeverifisert" for s in sources if not s.name.endswith(".json"))
    evidence = tuple(
        s.id for s in sources if not s.name.endswith(".json") and s.status == "kildeverifisert"
    )
    # Plenumsbeviset gjelder konkret sak13, samlet I–VI, enstemmig vedtatt.
    if support_ok:
        voting = next(s for s in sources if s.name.endswith("votering-181224.html"))
        voting_raw = raw_source(voting)
        assert voting_raw is not None
        tree = parse_legacy_html(voting_raw)
        locator = (
            "/html/body/div[2]/div/main/div[2]/div/div[4]/div/div/div/div/div/div/div[1]/div[14]"
        )
        blocks = tree.xpath(locator)
        if len(blocks) != 1:
            raise ValueError("T6: eksakt plenumsblokk mangler")
        text = compact(blocks[0].text_content())
        if not all(v in text for v in ("Innst. 95 S", "enstemmig vedtatt", "1429")):
            raise ValueError("T6: plenumsbeviset avviker")
        voting_statement = identified(
            "innstilling95-statement",
            Statement(
                "",
                inns.id,
                voting.id,
                locator,
                blocks[0].text_content(),
                html.tostring(blocks[0], encoding="unicode", with_tail=False),
                "vedtakelsesbevis_I–VI_ikke_komitegruppenes_begrunnelse",
                "stortinget",
                "2024",
                "kildeverifisert_enstemmig",
                tuple(r[0] + "/" + r[1] for r in _rows(_roman(roots["inns95"][3], "I")))
                if "inns95" in roots
                else (),
                ("Plenum 18.12.2024", "Sak 13", "I–VI"),
            ),
        )
        statements.append(voting_statement)
        evidence += (voting_statement.id,)
    else:
        issues.append("vedtakelsesbevis_mangler")
    for recipe in recipes:
        raw = reconstruct(t5_basis, sources, recipe)
        number = int(recipe.document_key.removeprefix("vedtak"))
        identifier = str(40034220 + number - 359)
        parsed = _xml(raw) if raw is not None else None
        node = parsed.find(".//" + NS + "stortingsvedtak") if parsed is not None else None
        content = None
        accounts: tuple[str, ...] = ()
        if node is not None:
            if (
                node.findtext(NS + "id") != identifier
                or node.findtext(NS + "sak_id") != "100889"
                or node.findtext(NS + "stortingsvedtak_nummer") != str(number)
                or node.findtext(NS + "stortingsvedtak_dato_tid") != "2024-12-18T00:00:00"
                or node.findtext(NS + "stortingsvedtak_type/" + NS + "id") != "ANNET"
                or parsed is None
                or parsed.findtext(NS + "sesjon_id") != "2024-2025"
            ):
                raise ValueError("T6: API-identitet/type/sak/sesjon/dato avviker")
            content = parse_legacy_html(
                (node.findtext(NS + "stortingsvedtak_tekst") or "").encode()
            )
            roman = ("I", "II", "III", "IV", "V", "VI")[number - 359]
            section = _roman(content, roman)
            accounts = (
                tuple(r[0] + "/" + r[1] for r in _rows(section))
                if number == 359
                else tuple(
                    dict.fromkeys(a for spec in AUTH_SPECS if spec[0] == roman for a in spec[3])
                )
            )
        document = identified(
            "innstilling95-document",
            PilotDocument(
                "",
                recipe.document_key,
                f"Vedtak {number} (2024–2025), API {identifier}",
                "stortingsvedtak",
                "2024-2025",
                "2024-12-18",
                "komplett_rekonstruert" if content is not None else "mangler",
                "108_strukturerte_tabellfelt"
                if number == 359 and content is not None and support_ok
                else "fullmaktsinventar"
                if number != 359 and content is not None
                else "ikke_strukturert",
                "ikke_faglig_godkjent",
                (recipe.id,),
                accounts,
            ),
        )
        documents.append(document)
        if content is not None:
            roots[recipe.document_key] = (document, recipe.id, recipe.expected_sha256, content)
        else:
            issues.append("vedtaksutdrag_mangler:" + recipe.document_key)
    for key, (document, source_id, digest, root) in roots.items():
        stage = "tilraading" if key == "inns95" else "vedtak"
        actor = "samlet_komite" if key == "inns95" else "stortinget"
        if key in {"inns95", "vedtak359"} and (key == "inns95" or support_ok):
            interpretation = Interpretation(
                adapter_version=RULE + ":" + key,
                round="nysaldering",
                round_evidence="95 I; sak100889; plenum18.12.2024 sak13; vedtak359",
                reason="T6: eksakte faste før/endring/etter; selvstendig kilde/rolle",
            )
            for chapter, post, chapter_name, purpose, raws, values, row, levels in _rows(
                _roman(root, "I")
            ):
                trio = []
                for meaning, raw_value, value, element, column in zip(
                    MEANINGS, raws, values, (levels, row, levels), (3, 4, 3), strict=True
                ):
                    o = AmountObservation(
                        dataset="prove",
                        source_system="innstilling95",
                        source_unit_id=key,
                        source_revision_id=digest,
                        interpretation_id=interpretation.id,
                        pointer=SourcePointer(
                            digest,
                            element.getroottree().getpath(element) + f"/td[{column}]",
                            meaning,
                            raw_record=html.tostring(element, encoding="unicode", with_tail=False),
                        ),
                        step_id=identity(
                            RULE,
                            "2024-2025",
                            "40034220" if key == "vedtak359" else document.id,
                            digest,
                            interpretation.id,
                            chapter,
                            post,
                        ),
                        raw_value=raw_value,
                        amount_text=raw_value,
                        amount_kr=value,
                        chapter_raw=chapter,
                        post_raw=post,
                        chapter=chapter,
                        post=post,
                        chapter_name=chapter_name,
                        purpose=purpose,
                        detail_level="post",
                        budget_year=2024,
                        year_evidence=interpretation.round_evidence,
                        unit_raw="Kroner",
                        currency="NOK",
                        multiplier="1",
                        precision="hele kroner",
                        conversion_rule=interpretation.normalization_rule,
                        normalization_evidence=source_id,
                        figure_type="komiteforslag" if key == "inns95" else "stortingsvedtak",
                        proposal_identity=document.id if key == "inns95" else None,
                        proposal_role="tilraading" if key == "inns95" else None,
                        proposal_author=actor if key == "inns95" else None,
                        round="nysaldering",
                        round_evidence=interpretation.round_evidence,
                        stage_raw=document.title,
                        meaning=meaning,
                        scope="enkeltledd",
                        classification_evidence=source_id,
                        structure_status="strukturert",
                    )
                    observations.append(o)
                    trio.append(o.id)
                    contexts.append(
                        identified(
                            "innstilling95-context",
                            TreatmentContext(
                                "",
                                o.id,
                                document.id,
                                "nysaldering",
                                stage,
                                actor,
                                "kildeverifisert",
                                (source_id,) + evidence if stage == "vedtak" else (source_id,),
                            ),
                        )
                    )
                inventory.append(
                    identified(
                        "innstilling95-inventory",
                        InventoryItem(
                            "",
                            document.id,
                            source_id,
                            row.getroottree().getpath(row),
                            chapter,
                            post,
                            "endringstabell",
                            "strukturert_T6",
                            row.text_content() + levels.text_content(),
                            2024,
                            tuple(trio),
                        ),
                    )
                )
        roman_specs = (
            AUTH_SPECS
            if key == "inns95"
            else tuple(
                s
                for s in AUTH_SPECS
                if s[0] == ("I", "II", "III", "IV", "V", "VI")[int(key[6:]) - 359]
            )
        )
        for roman, point, role, accounts, frame in roman_specs:
            section = _roman(root, roman)
            # Alle vilkår bevares samlet; atomisk lokator skiller de enkelte punktene.
            selector = (
                ".//tbody/tr[" + str(int(point) + 1) + "]"
                if roman == "III"
                else ".//li[" + point + "]"
                if roman in {"V", "VI"}
                else ".//p[last()]"
            )
            atom = section.xpath(selector)
            if not atom:
                raise ValueError("T6: fullmaktspunkt mangler")
            authorization = identified(
                "innstilling95-authorization",
                Authorization(
                    "",
                    document.id,
                    source_id,
                    atom[0].getroottree().getpath(atom[0]),
                    roman,
                    point,
                    stage + ":" + role,
                    {
                        "II": "2024; fremtidige år; nye bestillinger og gammelt ansvar",
                        "III": "2024; nye tilsagn og gammelt ansvar",
                        "IV": "2024; fremtidige år; nye forpliktelser og gammelt ansvar",
                    }.get(roman, "2024"),
                    accounts,
                    frame,
                    section.text_content(),
                    html.tostring(section, encoding="unicode", with_tail=False),
                    "kildebundet_inventar_ikke_bevilgningsdelta",
                ),
            )
            authorizations.append(authorization)
            for account in accounts:
                chapter, post = account.split("/")
                inventory.append(
                    identified(
                        "innstilling95-inventory",
                        InventoryItem(
                            "",
                            document.id,
                            source_id,
                            authorization.locator,
                            chapter,
                            post,
                            stage + ":fullmakt:" + roman + "." + point,
                            "fullmaktsinventar_ikke_delta",
                            authorization.text,
                            2024,
                            (),
                        ),
                    )
                )
        # Hele logiske seksjoner + presise partimerknader. Sluttopplysninger ligger i m4.
        sections = root.xpath("//*[@data-bigdoc-section]") if key == "inns95" else [root]
        for section in sections:
            title = (
                compact(section.xpath(".//h2")[0].text_content())
                if section.xpath(".//h2")
                else document.title
            )
            statements.append(
                identified(
                    "innstilling95-statement",
                    Statement(
                        "",
                        document.id,
                        source_id,
                        section.getroottree().getpath(section),
                        section.text_content(),
                        html.tostring(section, encoding="unicode", with_tail=False),
                        "fulltekst_inventar",
                        "sammensatt_se_presise_utsagn" if key == "inns95" else actor,
                        "2024; øvrige perioder i råtekst",
                        "bevart_ikke_fulltolket",
                        (),
                        (title,),
                    ),
                )
            )
        if key == "inns95":
            posts = root.get_element_by_id("m3").xpath(".//p")
            for index, paragraph in enumerate(posts):
                who = {7: "Ap/Sp/SV", 8: "Høyre", 9: "Fremskrittspartiet"}.get(
                    index, "samlet_komite"
                )
                account_scope = {
                    2: ("1420/62",),
                    3: ("1420/74",),
                    4: ("1420/75",),
                    5: ("4481/1",),
                    7: ("1420/32",),
                    9: ("1420/74",),
                }.get(index, ())
                statements.append(
                    identified(
                        "innstilling95-statement",
                        Statement(
                            "",
                            document.id,
                            source_id,
                            paragraph.getroottree().getpath(paragraph),
                            paragraph.text_content(),
                            html.tostring(paragraph, encoding="unicode", with_tail=False),
                            "merknad_ikke_tallfestet_alternativ",
                            who,
                            "2024; historisk/fremtidig kontekst i råtekst",
                            "kildebundet_avsender_ikke_stortingets_begrunnelse",
                            account_scope,
                            ("Komiteens merknader", who),
                        ),
                    )
                )
    prop = next(d for d in old.documents if d.key == "prop16")
    decision_by_key = {d.key: d for d in documents}
    # Punktidentitet er lokal i hvert dokument. De åtte atomiske koblingene
    # er adskilt fra de fem formelle fullmaktsvedtakene og dokumentlenkene.
    for left in authorizations:
        if left.document_id != inns.id:
            continue
        number = {"II": 360, "III": 361, "IV": 362, "V": 363, "VI": 364}[left.roman]
        target = decision_by_key["vedtak" + str(number)]
        right = next(
            (
                a
                for a in authorizations
                if a.document_id == target.id and a.roman == left.roman and a.point == left.point
            ),
            None,
        )
        if right is None:
            issues.append("fullmaktspunkt_mangler:" + target.key + ":" + left.point)
            continue
        relations.append(
            identified(
                "innstilling95-relation",
                PilotRelation(
                    "",
                    left.id,
                    right.id,
                    f"95.{left.roman}.{left.point}→{number}.{right.roman}.{right.point}",
                    "lokale_dokumentpunkter;fullmakt_ikke_bevilgningsdelta;" + left.period,
                    "kildeverifisert" if support_ok else "uavklart",
                    left.accounts,
                    (inns.id, target.id, left.source_id, right.source_id, *evidence),
                    2024,
                ),
            )
        )
    for target in documents:
        roman = ("I", "II", "III", "IV", "V", "VI")[int(target.key[6:]) - 359]
        accounts = target.accounts
        if target.raw_coverage == "mangler":
            continue
        relations.append(
            identified(
                "innstilling95-relation",
                PilotRelation(
                    "",
                    inns.id,
                    target.id,
                    "95" + roman + "→" + target.key,
                    "lokalt_romertall=" + roman + ";sak100889;enstemmig;2024",
                    "kildeverifisert" if support_ok else "uavklart",
                    accounts,
                    (original.id, *target.source_ids, *evidence),
                    2024,
                ),
            )
        )
    table_accounts = decision_by_key["vedtak359"].accounts
    common = tuple(a for a in table_accounts if a != "1420/32")
    relations.append(
        identified(
            "innstilling95-relation",
            PilotRelation(
                "",
                prop.id,
                inns.id,
                "PropI→95I",
                "35_felles_trioer;32_mangler_i_Prop",
                "kildeverifisert",
                common,
                (original.id, prop.id),
                2024,
            ),
        )
    )
    for a in authorizations:
        if a.document_id != inns.id:
            continue
        prior = tuple(
            p.id
            for p in t5_basis.authorizations
            if p.roman == a.roman and p.point == a.point and p.accounts == a.accounts
        )
        relations.append(
            identified(
                "innstilling95-relation",
                PilotRelation(
                    "",
                    prop.id,
                    inns.id,
                    "Prop" + a.roman + "." + a.point + "→95" + a.roman + "." + a.point,
                    "fullmakt_ikke_delta;lokale_punkter;2024",
                    "kildeverifisert",
                    a.accounts,
                    (*prior, a.id),
                    2024,
                ),
            )
        )
    bindings = tuple(
        identified("innstilling95-binding", FieldBinding("", i.id, i.observation_ids))
        for i in inventory
        if i.role == "endringstabell"
    )
    coverage = []
    for document in (inns, *documents):
        fields = sum(c.document_id == document.id for c in contexts)
        accounts = tuple(
            dict.fromkeys(
                i.chapter + "/" + i.post
                for i in inventory
                if i.document_id == document.id and i.chapter
            )
        )
        coverage.append(
            identified(
                "innstilling95-coverage",
                CoverageOverlay(
                    "",
                    document.id,
                    fields // 3,
                    fields,
                    accounts,
                    "108_strukturerte_tabellfelt"
                    if fields == 108
                    else "fullmaktsinventar"
                    if document.key not in {"inns95", "vedtak359"}
                    and document.raw_coverage != "mangler"
                    else "tabellstadium_mangler",
                    "fast_tabell_og_inventar_ikke_all_tekst_faglig_avklart",
                    "historisk_T1/T5:ikke_strukturert_T6" if document.key == "inns95" else "",
                ),
            )
        )
    return identified(
        "innstilling95-basis",
        Basis(
            "",
            RULE,
            t5_basis,
            sources,
            recipes,
            tuple(documents),
            tuple(inventory),
            tuple(statements),
            tuple(observations),
            tuple(contexts),
            tuple(relations),
            bindings,
            tuple(coverage),
            tuple(authorizations),
            tuple(issues),
        ),
    )


def validate_basis(basis: Basis, prepared: PilotInput) -> None:
    # Egen profil: aldri send union339 til T1s historiske256-grense.
    counts = (
        (
            len(basis.t5_basis.t1_basis.sources) + len(basis.t5_basis.sources) + len(basis.sources),
            64 - len(prepared.basis.sources),
        ),
        (len(basis.t5_basis.t1_basis.documents) + len(basis.documents), 16),
        (len(basis.t5_basis.t1_basis.inventory) + len(basis.inventory), 4096),
        (len(basis.t5_basis.t1_basis.statements) + len(basis.statements), 1024),
        (
            len(basis.t5_basis.t1_basis.observations)
            + len(basis.t5_basis.observations)
            + len(basis.observations),
            512,
        ),
        (len(basis.t5_basis.t1_basis.relations) + len(basis.relations), 4096),
    )
    if any(count > limit for count, limit in counts):
        raise ValueError("T6: ressursprofil overskredet")
    if basis != structure_basis(basis.t5_basis, prepared, basis.sources):
        raise ValueError("T6: basis avviker fra originaler, identitet, roller eller dekning")
