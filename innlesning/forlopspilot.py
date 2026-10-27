"""T3: fem nye kildefelt, helinventar og eksplisitte byteoppskrifter. Ingen analyse."""

import gzip
import hashlib
import io
import json
import re
from dataclasses import replace
from functools import lru_cache
from pathlib import Path

from lxml import etree, html

from .forlopspilot_model import RULE, Basis
from .komitepilot import LegacyPayloads, _payload, payload_bytes
from .komitepilot_model import Payload, Source
from .observations import AmountObservation, Interpretation, SourcePointer, encode, identity
from .omtale import compact, identified
from .visningspilot import _doc, _xml
from .visningspilot_model import (
    InventoryItem,
    PilotBasis,
    PilotDocument,
    PilotRelation,
    Statement,
    TreatmentContext,
)

ROOT = "docs/research/to-visninger-37/originals/aar/"
PARENT = ROOT + "session-2023-2024.xml.gz"
META = ROOT + "session-2023-2024.meta.json"
MANIFEST = ROOT + "manifest.json"
CONTROL = "tests/fixtures/b3/40033719.xml"
MAX_SOURCE = 16 * 1024 * 1024
MAX_PARENT = 32 * 1024 * 1024
MAX_INVENTORY = 4096  # 153 + 1488 autentiske tabellrader, med rom for tekstinventar.
PARENT_SHA = "66aa3ac5e93598fbbf2c02577c025395ea43a6bb7148e83a79f639bac9b09a57"
CATALOG = {
    PARENT: (
        "forelder2023",
        "application/gzip",
        "d083055643de38008fa373e54ea556cb06f5348f5d7d4978a323bba25e3f303f",
    ),
    META: (
        "forelder2023",
        "application/json",
        "56372509ffb4d04a7a265b969932327872b54d0279e43dfb762ef76f24b0f743",
    ),
    MANIFEST: (
        "forskningsmanifest",
        "application/json",
        "1f8a76b53c3e31b389561f95e01a009b29ccdf2eabc902bed6fd22ee4accee9d",
    ),
    CONTROL: (
        "kontroll857",
        "application/xml",
        "4113b987c8f939256d30ef6a4401cda358d9da90b5af19cbbbc37d0ec9d312b0",
    ),
    "tests/fixtures/b3/40033719.json": (
        "kontroll857",
        "application/json",
        "88da1ed5332372eba1a861111cf374da55133de1419aaa58d8c7e7b66afd502f",
    ),
}
# api -> start, slutt, objekt-SHA, konvolutt-SHA, separator, nummer, dato, radantall
RECIPES = {
    "40032928": (
        6092492,
        6209173,
        "5c753687510813c4f4241705670764b4e9903e87343d61ee71e55c872ae53857",
        "73bbcdc1d83a539ab4f3c2fad7b2b2972e003e742a5391a003d19c38149b6e71",
        b"\n",
        "341",
        "2023-12-19",
        153,
    ),
    "40033719": (
        2552391,
        3817852,
        "a22a2fe3ae4e26f57d1570b27a0f962ddfda9937944b1204262cf8759ef4f392",
        "252544da8756b038d54f6e935323fb33227b7ef16ee4c540a1badb7c5245517f",
        b"",
        "857",
        "2024-06-21",
        1488,
    ),
}
GAPS = (
    "opprinnelig_forslag_og_tilleggsforslag_mangler",
    "opprinnelig_Innst14_og_postvist_vedtakelsesbevis_mangler",
    "rnb_Prop104_kapittel5_original_og_postkobling_mangler",
    "rnb_Innst447_gjenlesbar_tilraading_og_rolle_mangler",
    "rnb_postvist_vedtakelsesbevis_mangler",
    "ovrige_endringer_ukjent_kontoomfang",
    "vedtak_uten_proposisjon_ikke_undersokt",
    "uttommende_periodeinventar_og_aarsavslutningsavstemming_mangler",
    "aarsdekning_delvis:ingen_godkjent_aarsbalanse",
    "kontokontinuitet_ikke_dokumentert",
    "faglig_godkjenning_ikke_utfort",
    "driftsaksept_ikke_utfort:#10_aapen",
    "857_gammel_554e_forelder_mangler:66aa_er_ny_representasjon",
)


def _parent(raw: bytes) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as handle:
        expanded = handle.read(MAX_PARENT + 1)
    if len(expanded) != 6816165 or hashlib.sha256(expanded).hexdigest() != PARENT_SHA:
        raise ValueError("T3s dekomprimerte fullsesjonsforelder avviker")
    return expanded


def derived_xml(parent: bytes, api_id: str) -> bytes:
    start, end, object_pin, envelope_pin, separator, *_ = RECIPES[api_id]
    if (
        len(parent) != 6816165
        or hashlib.sha256(parent).hexdigest() != PARENT_SHA
        or hashlib.sha256(parent[start:end]).hexdigest() != object_pin
    ):
        raise ValueError("T3-forelder/objektgrenser avviker")
    raw = parent[:317] + parent[start:end] + separator + parent[6816110:]
    if hashlib.sha256(raw).hexdigest() != envelope_pin:
        raise ValueError("T3s avledede konvolutt avviker")
    return raw


def _source(name: str, payload: Payload | None, error: str | None = None) -> Source:
    key, mime, pin = CATALOG[name]
    metadata = {
        "repository_path": name,
        "transport_reference": CATALOG[META][2] + "#/"
        if name in {PARENT, META}
        else CATALOG[MANIFEST][2] + "#/sources/" + ("2" if name == CONTROL else "3")
        if key == "kontroll857"
        else "repository:forskningsmanifest_37",
    }
    if error:
        metadata["error_type"] = error
    return identified(
        "forlopskilde-1",
        Source(
            "",
            name,
            key,
            mime,
            pin,
            payload.id if payload else None,
            "mangler"
            if payload is None
            else "kildeverifisert"
            if payload.sha256 == pin
            else "motstrid",
            encode(metadata),
        ),
    )


def _derived_source(api_id: str, parent: Source) -> Source:
    start, end, pin, envelope, separator, number, *_ = RECIPES[api_id]
    return identified(
        "forlopskilde-1",
        Source(
            "",
            "derived:" + api_id,
            "vedtak" + number,
            "application/xml",
            envelope,
            parent.payload_id,
            "avledet_kildeverifisert" if parent.status == "kildeverifisert" else "mangler",
            encode(
                {
                    "kind": "avledet_ikke_http",
                    "parent_source_id": parent.id,
                    "parent_sha256": PARENT_SHA,
                    "parent_bytes": 6816165,
                    "prefix_bytes": 317,
                    "object_start_byte_0": start,
                    "object_end_byte_0_exclusive": end,
                    "object_sha256": pin,
                    "separator_hex": separator.hex(),
                    "suffix_start_byte_0": 6816110,
                }
            ),
        ),
    )


def import_basis(
    root: Path,
    *,
    legacy_json: str = "",
    legacy: LegacyPayloads = (),
    previous: PilotBasis | None = None,
) -> Basis:
    payloads: dict[str, Payload] = {}
    sources = []
    for name in CATALOG:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("T3-kilde utenfor valgt rot")
        try:
            with path.open("rb") as handle:
                raw = handle.read(MAX_SOURCE + 1)
            if len(raw) > MAX_SOURCE:
                raise ValueError("T3-payload overstiger 16 MiB")
            payload = _payload(raw, legacy)
            payloads.setdefault(payload.id, payload)
            source = _source(name, payload)
        except (OSError, ValueError) as error:
            source = _source(name, None, type(error).__name__)
        sources.append(source)
    return structure_basis(tuple(payloads.values()), tuple(sources), legacy_json, legacy, previous)


def _field(node: etree._Element, name: str) -> str:
    return str(node.xpath(f'string(./*[local-name()="{name}"])'))


def _inventory_rows(
    rows: list[html.HtmlElement],
) -> tuple[tuple[int, html.HtmlElement, str, str, str], ...]:
    result = []
    chapter = post = ""
    for n, row in enumerate(rows, 1):
        cells = [compact(c.text_content()) for c in row]
        if cells and cells[0].isdigit():
            chapter, post = str(int(cells[0])), ""
        explicit_post = len(cells) > 1 and cells[1].isdigit()
        if explicit_post:
            post = str(int(cells[1]))
        purpose = cells[2] if len(cells) > 2 else ""
        levels = purpose.startswith("fra kr")
        total = purpose.lower().startswith(("totale ", "sum:"))
        component = bool(re.match(r"\d+ ", purpose)) and not explicit_post
        role = (
            "ustrukturert_postrad"
            if explicit_post
            else "for_etter_ustrukturert"
            if levels
            else "total_eller_kontekst"
            if total
            else "ustrukturert_spesifikasjon"
            if component
            else "kapittel_eller_kontekst"
        )
        # Bare en uttrykkelig postkolonne eller dens tilgrensende før/etter-rad gir postkobling.
        result.append((n, row, chapter, post if explicit_post or levels else "", role))
    return tuple(result)


def _statement(
    doc: PilotDocument,
    source: Source,
    node: html.HtmlElement,
    locator: str,
    role: str,
    accounts: tuple[str, ...] = (),
) -> Statement:
    return identified(
        "forlopsutsagn-1",
        Statement(
            "",
            doc.id,
            source.id,
            locator,
            node.text_content(),
            html.tostring(node, encoding="unicode", with_tail=False),
            role,
            "stortinget",
            "2024",
            "kildeverifisert",
            accounts,
            (doc.title, role, locator),
        ),
    )


def _amount(
    doc: PilotDocument,
    source: Source,
    row: html.HtmlElement,
    *,
    post: str,
    meaning: str,
    raw: str,
    value: int,
    row_number: int,
    column: int,
    delta_row: int,
    round: str,
    api_id: str,
) -> AmountObservation:
    interpretation = Interpretation(
        adapter_version=RULE,
        round=round,
        round_evidence=doc.title + "; tekst sier budsjett 2024",
        reason="T3: valgt komplett vedtaksobjekt; fem eksakte felt",
    )
    return AmountObservation(
        dataset="prove",
        source_system="forlopspilot",
        source_unit_id=doc.key,
        source_revision_id=source.expected_sha256,
        interpretation_id=interpretation.id,
        pointer=SourcePointer(
            source.expected_sha256,
            f"table[1]/tr[{row_number}]/td[{column}]",
            meaning,
            raw_record=html.tostring(row, encoding="unicode", with_tail=False),
        ),
        step_id=identity(RULE, doc.id, "1429", post, delta_row),
        raw_value=raw,
        amount_text=raw,
        amount_kr=value,
        chapter_raw="1429",
        post_raw=post,
        chapter="1429",
        post=post,
        chapter_name="Riksantikvaren",
        purpose=compact(row[2].text_content()),
        detail_level="post",
        budget_year=2024,
        year_evidence="Uttrykkelig statsbudsjett 2024 i tittel/vedtakstekst",
        decision_date=doc.date,
        decision_session=doc.session,
        api_id=api_id,
        event_id="341" if round == "opprinnelig" else "857",
        unit_raw="Kroner",
        currency="NOK",
        multiplier="1",
        precision="hele kroner",
        conversion_rule=interpretation.normalization_rule,
        normalization_evidence=source.id,
        figure_type="stortingsvedtak",
        proposal_identity=doc.id,
        proposal_author="stortinget",
        round=round,
        round_evidence=interpretation.round_evidence,
        stage_raw=doc.title,
        meaning=meaning,
        scope="enkeltledd",
        classification_evidence=source.id,
        structure_status="strukturert",
        professional_status="ikke_faglig_godkjent",
    )


@lru_cache(maxsize=3)
def structure_basis(
    payloads: tuple[Payload, ...],
    sources: tuple[Source, ...],
    legacy_json: str = "",
    legacy: LegacyPayloads = (),
    previous: PilotBasis | None = None,
) -> Basis:
    if len(payloads) > 64 or len(sources) not in {len(CATALOG), len(CATALOG) + 2}:
        raise ValueError("T3-kildeinventar overstiger/avviker fra kontrakt")
    if bool(legacy_json) != bool(previous):
        raise ValueError("T3-kapsel krever ett typet validert tidligere grunnlag")
    by_payload = {p.id: p for p in payloads}
    if len(by_payload) != len(payloads):
        raise ValueError("Duplisert T3-payload")
    raws = {p.id: payload_bytes(p, legacy) for p in payloads}
    if any(p != _payload(raws[p.id], legacy) for p in payloads):
        raise ValueError("T3-payload kopierer tidligere original")
    initial = sources[: len(CATALOG)]
    if tuple(s.name for s in initial) != tuple(CATALOG):
        raise ValueError("T3-kildekatalog avviker")
    if {s.payload_id for s in initial if s.payload_id} != set(by_payload):
        raise ValueError("Ubrukt eller ukjent T3-payloadreferanse")
    for s in initial:
        metadata = json.loads(s.metadata_json)
        allowed = {"repository_path", "transport_reference"}
        if s.payload_id is None:
            allowed.add("error_type")
        if not isinstance(metadata, dict) or set(metadata) != allowed:
            raise ValueError("T3s lokale metadata avviker")
        error = metadata.get("error_type")
        if s.payload_id is None and (not isinstance(error, str) or not error):
            raise ValueError("T3-kildefravær krever feilkategori")
        if s != _source(s.name, by_payload.get(s.payload_id or ""), error):
            raise ValueError("T3-kildestatus/proveniens/ID avviker")
    by_name = {s.name: s for s in initial}
    derived = tuple(_derived_source(api, by_name[PARENT]) for api in RECIPES)
    if len(sources) > len(initial) and sources[len(initial) :] != derived:
        raise ValueError("T3s avledede kildeoppskrift avviker")
    sources = initial + derived
    issues = list(GAPS)
    issues.extend(s.status + ":" + s.name for s in initial if s.status != "kildeverifisert")
    if previous is None:
        issues.append("nysaldering_210_T1_grunnlag_mangler")
    documents, inventory, statements, observations, contexts, relations = [], [], [], [], [], []
    ready = by_name[PARENT].status == by_name[META].status == "kildeverifisert"
    parent = _parent(raws[by_name[PARENT].payload_id or ""]) if ready else None
    if parent is None:
        issues.append("341_857_forelder_eller_transport_mangler:ingen_nye_belop")
    elif by_name[CONTROL].status == "kildeverifisert":
        old = raws[by_name[CONTROL].payload_id or ""]
        control_block = re.search(rb"    <stortingsvedtak>.*?</stortingsvedtak>\r\n", old, re.S)
        if not control_block or control_block[0] != parent[2552391:3817852]:
            raise ValueError("857s gamle og nye komplette objektbyte avviker")
        issues.append("857_kontrollobjekt_byteidentisk:554e_forelder_ikke_gjenlest")
    for source in derived:
        api_id = source.name.removeprefix("derived:")
        recipe = RECIPES[api_id]
        number, date, row_count = recipe[5:]
        doc = identified(
            "forlopsdokument-1",
            PilotDocument(
                "",
                source.document_key,
                f"Vedtak {number} – statsbudsjettet 2024",
                "stortingsvedtak",
                "2023-2024",
                date,
                "komplett vedtaksobjekt; delvis sesjon; avledet_ikke_http"
                if parent
                else "forelderbyte bevart; transport/struktur ikke kontrollert"
                if by_name[PARENT].status == "kildeverifisert"
                else "mangler komplett vedtaksobjekt",
                "ustrukturert: kilde/transport mangler"
                if parent is None
                else "delvis: bare 1429/1 og /22 strukturert; øvrige rader ustrukturert"
                if number == "341"
                else (
                    "delvis: bare 1429/1 strukturert; /22 avgrenset fravær; "
                    "øvrige rader ustrukturert"
                ),
                "ikke_faglig_godkjent",
                (source.id,),
                (),
            ),
        )
        documents.append(doc)
        if parent is None:
            continue
        raw = derived_xml(parent, api_id)
        root = _xml(raw)
        nodes = root.xpath('//*[local-name()="stortingsvedtak"]')
        if len(nodes) != 1:
            raise ValueError("T3 krever ett komplett vedtaksobjekt")
        node = nodes[0]

        if (
            _field(node, "id") != api_id
            or _field(node, "sak_id") != {"341": "95776", "857": "98919"}[number]
            or _field(root, "sesjon_id") != "2023-2024"
            or _field(node, "stortingsvedtak_nummer") != number
            or _field(node, "stortingsvedtak_dato_tid")[:10] != date
            or "2024" not in _field(node, "stortingsvedtak_tittel")
        ):
            raise ValueError("T3s autoritative vedtaksidentitet/dato/budsjettår avviker")
        markup = _field(node, "stortingsvedtak_tekst")
        tree = _doc(markup.encode("utf8"))
        tables = tree.xpath(".//table")
        if len(tables) != 1:
            raise ValueError("T3s tabellinventar avviker")
        rows = tables[0].xpath(".//tr")
        if len(rows) != row_count:
            raise ValueError("T3s komplette radinventar avviker")
        row_inventory = _inventory_rows(rows)
        doc = identified(
            "forlopsdokument-1",
            replace(
                doc,
                id="",
                title=f"Vedtak {number}: " + _field(node, "stortingsvedtak_tittel"),
                accounts=tuple(
                    dict.fromkeys(
                        chapter + "/" + post
                        for _, _, chapter, post, _ in row_inventory
                        if chapter and post
                    )
                ),
            ),
        )
        documents[-1] = doc
        full = _statement(
            doc, source, tree, "stortingsvedtak_tekst", "fulltekst_delvis_strukturert"
        )
        statements.append(full)
        chosen = []
        round = "opprinnelig" if number == "341" else "rnb"
        if number == "341":
            if compact(rows[100][0].text_content()) != "1429":
                raise ValueError("341s kapittelgrense avviker")
            for n, post in ((102, "1"), (104, "22")):
                row = rows[n - 1]
                if compact(row[1].text_content()) != post:
                    raise ValueError("341s postlokator avviker")
                value = compact(row[3].text_content())
                chosen.append(
                    _amount(
                        doc,
                        source,
                        row,
                        post=post,
                        meaning="nivaa",
                        raw=value,
                        value=int(value.replace(" ", "")),
                        row_number=n,
                        column=4,
                        delta_row=n,
                        round=round,
                        api_id=api_id,
                    )
                )
        else:
            if (
                compact(rows[821][0].text_content()) != "1429"
                or compact(rows[830][0].text_content()) != "1432"
            ):
                raise ValueError("857s avgrensede 1429-blokk avviker")
            if any(compact(r[1].text_content()) == "22" for r in rows[821:830]):
                raise ValueError("857s avgrensede /22-fravær avviker")
            block = html.Element("div")
            for row in rows[821:831]:
                block.append(html.fromstring(html.tostring(row, encoding="unicode")))
            absence = _statement(
                doc,
                source,
                block,
                "table[1]/tr[822:831]",
                "857_1429_22_fravaer_kun_tr822_830_for_1432",
                ("1429/22",),
            )
            statements.append(absence)
            issues.append(
                "857_1429_22:ingen_belopsrad_i_tr822_830_for_tr831_1432;ingen_nullhendelse"
            )
            row, levels = rows[822], rows[823]
            match = re.fullmatch(
                r"fra kr ([\d ]+) til kr ([\d ]+)", compact(levels[2].text_content())
            )
            if (
                compact(row[1].text_content()) != "1"
                or match is None
                or "reduseres med" not in compact(row[2].text_content())
            ):
                raise ValueError("857s post/betydning/fortegn avviker")
            delta = compact(row[4].text_content())
            for meaning, value, target, rn, col in (
                ("for_belop", match[1].strip(), levels, 824, 3),
                ("endring", delta, row, 823, 5),
                ("etter_belop", match[2].strip(), levels, 824, 3),
            ):
                chosen.append(
                    _amount(
                        doc,
                        source,
                        target,
                        post="1",
                        meaning=meaning,
                        raw=value,
                        value=int(value.replace(" ", "")) * (-1 if meaning == "endring" else 1),
                        row_number=rn,
                        column=col,
                        delta_row=823,
                        round=round,
                        api_id=api_id,
                    )
                )
        observations.extend(chosen)
        for o in chosen:
            contexts.append(
                identified(
                    "forlopskontekst-1",
                    TreatmentContext(
                        "",
                        o.id,
                        doc.id,
                        round,
                        "vedtak",
                        "stortinget",
                        "kildeverifisert",
                        (full.id,),
                    ),
                )
            )
        for n, row, chapter, post, role in row_inventory:
            ids = tuple(o.id for o in chosen if o.pointer.locator.startswith(f"table[1]/tr[{n}]/"))
            inventory.append(
                identified(
                    "forlopsinventar-1",
                    InventoryItem(
                        "",
                        doc.id,
                        source.id,
                        f"table[1]/tr[{n}]",
                        chapter,
                        post,
                        "belopsrad" if ids else role,
                        "strukturert" if ids else "ustrukturert",
                        row.text_content(),
                        2024,
                        ids,
                    ),
                )
            )
    if len(documents) == 2 and parent is not None:
        evidence = tuple(s.id for s in statements if s.role == "fulltekst_delvis_strukturert")
        relations.append(
            identified(
                "forlopsrelasjon-1",
                PilotRelation(
                    "",
                    documents[0].id,
                    documents[1].id,
                    "senere_vedtatt_runde",
                    "avgrenset kronologi; ingen uttømmende årsdekning",
                    "kildeverifisert",
                    ("1429/1",),
                    evidence,
                    2024,
                ),
            )
        )
        if previous:
            final = next((d for d in previous.documents if d.key == "vedtak210"), None)
            if final:
                final_evidence = tuple(
                    dict.fromkeys(
                        sid
                        for c in previous.contexts
                        if c.document_id == final.id
                        for sid in c.evidence_ids
                    )
                )
                for start, accounts in ((documents[1], ("1429/1",)), (documents[0], ("1429/22",))):
                    relations.append(
                        identified(
                            "forlopsrelasjon-1",
                            PilotRelation(
                                "",
                                start.id,
                                final.id,
                                "senere_vedtatt_runde",
                                "avgrenset kronologi; ingen uttømmende årsdekning",
                                "kildeverifisert",
                                accounts,
                                evidence + final_evidence,
                                2024,
                            ),
                        )
                    )
    return identified(
        "forlopsgrunnlag-1",
        Basis(
            "",
            RULE,
            payloads,
            sources,
            tuple(documents),
            tuple(inventory),
            tuple(statements),
            tuple(observations),
            tuple(contexts),
            tuple(relations),
            tuple(dict.fromkeys(issues)),
            legacy_json,
        ),
    )


def validate_basis(
    basis: Basis, legacy: LegacyPayloads = (), previous: PilotBasis | None = None
) -> None:
    if any(
        len(items) > cap
        for items, cap in (
            (basis.documents, 16),
            (basis.inventory, MAX_INVENTORY),
            (basis.statements, 512),
            (basis.observations, 256),
            (basis.relations, 1024),
        )
    ):
        raise ValueError("T3-objekter overstiger kontraktens ressursgrense")
    if basis != structure_basis(basis.payloads, basis.sources, basis.legacy_json, legacy, previous):
        raise ValueError("T3-grunnlaget avviker fra kildebyte/roller/bevis/ID-er")
