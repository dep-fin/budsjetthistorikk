"""Reproduser #2-kontroll fra bevarte felt; aldri regnskapsimport eller årsdekning.

Denne avgrensede kontrollen bruker hashfestede, avledede 2024-artefakter. Den
leser ikke tidligere verification.json, normaliserte DFØ-felt eller saldoledgere.
"""

import csv
import hashlib
import io
import json
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

INPUTS = {
    "aar/dfo2024.csv": "1b6d9bed4bfa9fccd991aa2d56d6a32c75c859089fce0a2fccce3292a990fff6",
    "statsrekneskap2024-posts.csv": (
        "2dbb699d7e17dd4d02c36f7abce94cbd90611148d4982a9d146bf21e958671c6"
    ),
    "aar/blaabok_posts.json": "7f85002b543a57b3948170f102dc581f66d5ca1b5c1372198433ecd05b0b337e",
    "aar/api_events.csv": "ab9ef8abe7f1b508d54ca17e6f88209d061a6a6e2c8f312d5444894686642e31",
    "aar/session_inventory.csv": "229ad23d556ff68c4fd62933afefe46f5c2e878d57fa8a8553a19fba3f82b345",
    "aar/scope_residual_ledger.json": (
        "0e37ea82b25adbfcf11147c16d50b5a7d1272395125ed1d0a31578919b1158b5"
    ),
}


@dataclass(frozen=True)
class PreservedResidual:
    account: str
    dfo_amount_kr: int | None
    pdf_amount_kr: int | None
    classification: str
    status: str


@dataclass(frozen=True)
class PreservedControl:
    input_hashes: tuple[tuple[str, str], ...]
    dfo_row_count: int
    dfo_post_count: int
    pdf_post_count: int
    common_count: int
    amount_difference_count: int
    residuals: tuple[PreservedResidual, ...]
    original_post_count: int
    original_difference_count: int
    session_inventory_count: int
    session_counts: tuple[tuple[str, int], ...]
    api_type_counts: tuple[tuple[str, int], ...]
    dfo_annual_expense_kr: int
    dfo_annual_income_kr: int
    professional_chain_complete: bool = False
    boundary: str = (
        "Budsjettår 2024: DFØ årets bevilgning mot Statsrekneskapens Løyving, "
        "og opprinnelige bevilgningsfelt mot Blå bok. Avledede, hashfestede kilder; "
        "ingen ny kontroll av original-PDF eller HTTP-byte. Tre kjedekonflikter "
        "1860/1, 4860/1 og 5999/90 består. Dette avstemmer ikke automatisk sesjonseksporten."
    )


def _whole(value: Decimal) -> int:
    if not value.is_finite() or value != value.to_integral_value():
        raise ValueError("Kontrollgrunnlaget har ikke hele kroner")
    return int(value)


def audit_preserved_2024(directory: Path) -> PreservedControl:
    raw: dict[str, bytes] = {}
    for filename, expected in INPUTS.items():
        path = directory / filename
        if path.stat().st_size > 8 * 1024 * 1024:
            raise ValueError("Bevart kontrollartefakt er for stor")
        value = path.read_bytes()
        if hashlib.sha256(value).hexdigest() != expected:
            raise ValueError(f"Kontrollartefaktens SHA-256 stemmer ikke: {filename}")
        raw[filename] = value
    dfo: dict[str, int] = defaultdict(int)
    dfo_rows = list(
        csv.DictReader(io.StringIO(raw["aar/dfo2024.csv"].decode("utf-8-sig")), delimiter=";")
    )
    for row in dfo_rows:
        if row["År"] != "2024" or row["Periode"] != "202401":
            raise ValueError("DFØ-kontrollen gjelder bare bevart 2024-periode")
        chapter = int(row["Kapittel_id"])
        account = row["Post_id"].zfill(6)
        if account[:4] != str(chapter).zfill(4):
            raise ValueError("DFØs kapittel/post-identitet stemmer ikke")
        annual = Decimal(row["Bevilgning_beløp"].replace(",", ".")) - Decimal(
            row["Bevilgning_overført_beløp"].replace(",", ".")
        )
        if 3000 <= chapter <= 5999:
            annual = -annual  # Bare den kildekontrollerte 2024-fortegnsregelen.
        elif not 1 <= chapter <= 2999:
            raise ValueError("DFØ-kontrollen krever budsjettkapittel")
        dfo[account] += _whole(annual)
    pdf: dict[str, int] = {}
    for row in csv.DictReader(io.StringIO(raw["statsrekneskap2024-posts.csv"].decode("utf-8-sig"))):
        key = row["kapittel"].zfill(4) + row["post"].zfill(2)
        if key in pdf:
            raise ValueError("Gjentatt konto i PDF-uttrekket")
        # Samla løyving og Rekneskap leses aldri som årets bevilgning.
        pdf[key] = _whole(Decimal(row["loyving_1000kr"]) * 1000)
    explanations = {r["post"]: r for r in json.loads(raw["aar/scope_residual_ledger.json"])}
    residuals: list[PreservedResidual] = []
    for key in sorted(set(dfo) ^ set(pdf)):
        explanation = explanations.get(key)
        a, b = dfo.get(key), pdf.get(key)
        explained = bool(
            explanation
            and explanation["dfo_annual"] == a
            and explanation["pdf_annual"] == b
            and explanation.get("classification")
        )
        residuals.append(
            PreservedResidual(
                key,
                a,
                b,
                explanation["classification"] if explanation else "uforklart",
                "forklart_omfangsforskjell" if explained else "uavklart",
            )
        )
    blue_rows = json.loads(raw["aar/blaabok_posts.json"])
    blue = {r["post"]: r["amount"] for r in blue_rows}
    if len(blue) != len(blue_rows):
        raise ValueError("Gjentatt Blå bok-konto")
    originals: dict[str, int] = {}
    for row in csv.DictReader(
        io.StringIO(raw["aar/api_events.csv"].decode("utf-8-sig")), delimiter=";"
    ):
        if row["kind"] == "original":
            if row["post"] in originals:
                raise ValueError("Gjentatt opprinnelig API-bevilgning")
            originals[row["post"]] = int(row["amount"])
    inventory = list(
        csv.DictReader(
            io.StringIO(raw["aar/session_inventory.csv"].decode("utf-8-sig")), delimiter=";"
        )
    )
    if len({(r["session"], r["id"]) for r in inventory}) != len(inventory):
        raise ValueError("Gjentatt inventaridentitet")
    sessions: dict[str, int] = defaultdict(int)
    types: dict[str, int] = defaultdict(int)
    for row in inventory:
        sessions[row["session"]] += 1
        types[row["type"]] += 1
    return PreservedControl(
        tuple(INPUTS.items()),
        len(dfo_rows),
        len(dfo),
        len(pdf),
        len(set(dfo) & set(pdf)),
        sum(dfo[k] != pdf[k] for k in set(dfo) & set(pdf)),
        tuple(residuals),
        len(originals),
        sum(originals.get(k) != blue.get(k) for k in set(originals) | set(blue)),
        len(inventory),
        tuple(sorted(sessions.items())),
        tuple(sorted(types.items())),
        sum(v for k, v in dfo.items() if int(k[:4]) < 3000),
        sum(v for k, v in dfo.items() if 3000 <= int(k[:4]) <= 5999),
    )
