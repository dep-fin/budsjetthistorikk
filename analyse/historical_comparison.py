"""Uavhengige, eksplisitte kontrollgrunnlag og full nøkkelunion; ingen godkjenning."""

import json
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any

from innlesning.historical_excel import (
    HistoricalSnapshot,
    _connect,
    candidate_control_basis,
    read_historical_workbook,
)
from innlesning.historical_xlsx import decimal_value
from innlesning.observations import encode, identity

VERSION = "historisk-sammenligning-2"
LEGACY_VERSION = "historisk-sammenligning-1"


def historical_control_scope(column: str, *, component: bool = False) -> dict[str, Any]:
    """Explicit candidate hypothesis; reference NOK amounts have multiplier 1."""
    return candidate_control_basis(column, component=component)


def _validate_scope(snapshot: HistoricalSnapshot, control: dict[str, Any]) -> None:
    selector, scope = control["selector"], control["scope"]
    column = selector["column"]
    component = scope.get("reference_basis") == "avledet_komponentdifferanse"
    expected = historical_control_scope(column, component=component)
    if set(scope) - (set(expected) | {"aggregation", "representation"}):
        raise ValueError("Ukjent felt i avstemmingsomfang")
    if any(
        scope.get(key) != value or type(scope.get(key)) is not type(value)
        for key, value in expected.items()
    ):
        raise ValueError(
            "Forslag og vedtak, år, enhet og betydning må samsvare med valgt kandidatgrunnlag"
        )
    sheet = "Dokumentiltknyntning2024" if column == "D" else "Rådata"
    if selector.get("sheet") != sheet or selector.get("key_fields") != (
        ["group", "chapter", "post", "subpost"] if column == "D" else ["chapter", "post"]
    ):
        raise ValueError("Utvalg og omfang har ulik kilde eller detaljeringsnivå")
    rule = next(r for r in snapshot.column_rules if (r["sheet"], r["column"]) == (sheet, column))
    if expected not in rule.get("comparison_profiles", []):
        raise ValueError(
            "Uttrekket mangler en bundet og forenlig kontrollhypotese; ny tolkning kreves"
        )
    if (rule["candidate_currency"], rule["candidate_multiplier"]) != (
        scope["unit"],
        scope["candidate_multiplier"],
    ):
        raise ValueError("Kandidatens faktiske enhetsgrunnlag er uforenlig")
    if column == "D" and (
        not selector.get("groups")
        or selector.get("subposts") != (["1", "2", "3", "4", "5", "6"] if component else ["0"])
    ):
        raise ValueError("Dokumentdelta og avledede komponentkontroller må velges separat")
    observations = {o.id: o for o in snapshot.extraction.observations}
    candidates = {c["observation_id"]: c for c in snapshot.candidates}
    for group in _candidate_groups(snapshot, control).values():
        for item in group:
            observation = observations[item["observation_id"]]
            if candidates[observation.id].get("comparison_basis") != expected:
                raise ValueError("Valgt kronekandidat har ukjent eller uforenlig kontrollgrunnlag")
            if observation.budget_year != scope["budget_year"] or observation.budget_side not in {
                "utgift",
                "inntekt",
            }:
                raise ValueError("Valgte kildeobservasjoner har uforenlig år eller budsjettside")
    reference_scope = {**expected, "candidate_multiplier": "1"}
    for reference in control["references"]:
        if reference.get("scope") != reference_scope:
            raise ValueError("Referansens eget kildeomfang må være uttrykkelig og forenlig")
        if reference.get("source_budget_year") != scope["budget_year"]:
            raise ValueError("Referansens faktiske kildeår er uforenlig med utvalget")
        if bool(reference.get("derived")) != component or (
            component and len(reference["pointers"]) != 2
        ):
            raise ValueError(
                "Avledet komponent krever begge innganger og separat referansegrunnlag"
            )


SCHEMA = """
CREATE TABLE IF NOT EXISTS historical_control_specs (
  spec_id TEXT PRIMARY KEY, extraction_id TEXT NOT NULL, content_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS historical_comparisons (
  comparison_id TEXT PRIMARY KEY, extraction_id TEXT NOT NULL, content_json TEXT NOT NULL
);
"""


def freeze_historical_controls(
    database: Path, extraction_id: str, specification: dict[str, Any]
) -> str:
    """Bevar forventninger før beregning; senere innhold får annen ID."""
    snapshot = read_historical_workbook(database, extraction_id)
    if (
        specification.get("version") != VERSION
        or not specification.get("controls")
        or len(encode(specification)) > 16 * 1024 * 1024
    ):
        raise ValueError("Versjonert kontrollspesifikasjon kreves")
    identifiers: set[str] = set()
    for control in specification["controls"]:
        if control["id"] in identifiers or control.get("tolerance") != "0":
            raise ValueError("Unik kontroll-ID og eksakt sammenligning kreves")
        identifiers.add(control["id"])
        if control.get("status") == "ikke_utfort":
            if not control.get("reason"):
                raise ValueError("Uprøvd kontroll krever grunn")
            continue
        if not control.get("scope") or not control.get("sources") or not control.get("references"):
            raise ValueError("Kontrollen krever eksplisitt omfang, kilder og uavhengige referanser")
        _validate_scope(snapshot, control)
        selector = control["selector"]
        expected_figure = {
            "G": "regjeringsforslag",
            "H": "stortingsvedtak",
            "I": "regjeringsforslag",
            "N": "regjeringsforslag",
        }
        if (
            selector["sheet"] == "Rådata"
            and selector["column"] in expected_figure
            and control["scope"].get("figure_type") != expected_figure[selector["column"]]
        ):
            raise ValueError("Forslag og vedtak må ha samme eksplisitte sammenligningsomfang")
        keys: set[tuple[str, ...]] = set()
        for reference in control["references"]:
            key = tuple(reference["key"])
            if key in keys or not reference.get("pointers"):
                raise ValueError("Unik referansenøkkel og kildepeker kreves")
            keys.add(key)
            value = reference["amount_kr"]
            if not isinstance(value, str) or decimal_value(value) is None:
                raise ValueError("Referansebeløpet må være en endelig Decimal-streng")
    payload = {"extraction_id": extraction_id, "specification": specification}
    spec_id = identity(VERSION, payload)
    with _connect(database, writable=True) as connection:
        for statement in SCHEMA.split(";"):
            if statement.strip():
                connection.execute(statement)
        connection.execute(
            "INSERT OR IGNORE INTO historical_control_specs "
            "(spec_id,extraction_id,content_json) VALUES (?,?,?)",
            (spec_id, extraction_id, encode(payload)),
        )
    return spec_id


def _candidate_groups(
    snapshot: HistoricalSnapshot, control: dict[str, Any]
) -> dict[tuple[str, ...], list[dict[str, Any]]]:
    candidates = {item["observation_id"]: item for item in snapshot.candidates}
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    selector = control["selector"]
    for observation in snapshot.extraction.observations:
        if (observation.pointer.sheet, observation.pointer.column) != (
            selector["sheet"],
            selector["column"],
        ):
            continue
        if "cells" in selector and observation.pointer.cell not in selector["cells"]:
            continue
        if "subposts" in selector and observation.subpost not in selector["subposts"]:
            continue
        group = next((d.raw_code for d in observation.documents if d.source_column == "F"), None)
        if "groups" in selector and group not in selector["groups"]:
            continue
        values = {
            "chapter": observation.chapter,
            "post": observation.post,
            "subpost": observation.subpost,
            "group": group,
        }
        key = tuple(
            str(values[field]) if values[field] is not None else "<ukjent>"
            for field in selector["key_fields"]
        )
        if "keys" in selector and list(key) not in selector["keys"]:
            continue
        groups[key].append(
            {
                "observation_id": observation.id,
                "cell_id": candidates[observation.id]["cell_id"],
                "pointer": observation.pointer.locator,
                "candidate_kr": candidates[observation.id]["candidate_kr"],
                "raw_value": observation.raw_value,
            }
        )
    return dict(groups)


def compare_historical_controls(database: Path, spec_id: str) -> dict[str, Any]:
    with _connect(database) as connection:
        found = connection.execute(
            "SELECT content_json FROM historical_control_specs WHERE spec_id=?", (spec_id,)
        ).fetchone()
    if found is None:
        raise ValueError("Ukjent frosset kontrollgrunnlag")
    payload = json.loads(found[0])
    version = payload["specification"]["version"]
    if version not in {VERSION, LEGACY_VERSION} or identity(version, payload) != spec_id:
        raise ValueError("Kontrollgrunnlaget er endret")
    snapshot = read_historical_workbook(database, payload["extraction_id"])
    rows: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    for control in payload["specification"]["controls"]:
        control_rows: list[dict[str, Any]] = []
        if control.get("status") == "ikke_utfort":
            control_rows.append(
                {
                    "control": control["id"],
                    "status": "ikke_utfort",
                    "reason": control["reason"],
                    "professional_approval": False,
                    "year_complete": False,
                }
            )
        else:
            if version == VERSION:
                _validate_scope(snapshot, control)
            groups = _candidate_groups(snapshot, control)
            refs = {tuple(item["key"]): item for item in control["references"]}
            for key in sorted(set(groups) | set(refs)):
                excel, reference = groups.get(key), refs.get(key)
                candidate: Decimal | None = None
                expected = Decimal(reference["amount_kr"]) if reference is not None else None
                if excel is not None and all(item["candidate_kr"] is not None for item in excel):
                    with localcontext() as context:
                        context.prec = 256
                        candidate = sum(
                            (Decimal(item["candidate_kr"]) for item in excel), Decimal(0)
                        )
                status = (
                    "missing_excel"
                    if excel is None
                    else "missing_reference"
                    if reference is None
                    else "unresolved"
                    if candidate is None
                    else "fractional_kr"
                    if candidate != candidate.to_integral_value()
                    else "match"
                    if candidate == expected
                    else "difference"
                )
                with localcontext() as context:
                    context.prec = 256
                    difference = (
                        candidate - expected
                        if candidate is not None and expected is not None
                        else None
                    )
                control_rows.append(
                    {
                        "control": control["id"],
                        "key": list(key),
                        "status": status,
                        "excel_inputs": excel,
                        "reference": reference,
                        "candidate_kr": str(candidate) if candidate is not None else None,
                        "reference_kr": str(expected) if expected is not None else None,
                        "difference_kr": str(difference) if difference is not None else None,
                        "scope": control["scope"],
                        "tolerance": "0",
                        "professional_approval": False,
                        "year_complete": False,
                        "derived_control_aggregate": bool(excel and len(excel) > 1),
                    }
                )
        rows.extend(control_rows)
        summaries[control["id"]] = dict(Counter(row["status"] for row in control_rows))
    report = {
        "version": version,
        "extraction_id": snapshot.extraction.id,
        "spec_id": spec_id,
        "specification": payload["specification"],
        "rows": rows,
        "summary": summaries,
        "professional_approval": False,
        "year_complete": False,
        "blocked_chains": ["1860/1", "4860/1", "5999/90"],
        "status": "utfort_med_aapne_faglige_sporsmaal",
    }
    comparison_id = identity(version, report)
    with _connect(database, writable=True) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO historical_comparisons "
            "(comparison_id,extraction_id,content_json) VALUES (?,?,?)",
            (comparison_id, snapshot.extraction.id, encode(report)),
        )
    return {"id": comparison_id, **report}


def read_historical_comparison(database: Path, comparison_id: str) -> dict[str, Any]:
    with _connect(database) as connection:
        row = connection.execute(
            "SELECT content_json FROM historical_comparisons WHERE comparison_id=?",
            (comparison_id,),
        ).fetchone()
    if row is None:
        raise ValueError("Ukjent historisk sammenligning")
    report: dict[str, Any] = json.loads(row[0])
    if (
        report.get("version") not in {VERSION, LEGACY_VERSION}
        or identity(report["version"], report) != comparison_id
    ):
        raise ValueError("Sammenligningsrapporten er endret")
    return {"id": comparison_id, **report}
