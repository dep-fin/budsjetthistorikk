"""Les en uttrykkelig valgt P2-kontrollmatrise uten database, nett eller aktivering."""

import argparse
import hashlib
import json
import math
import re
from datetime import date
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any

SCHEMA = "historical-control-matrix-1"
WORKBOOK_SHA256 = "870d30d55b4f7f6791fe48ea2a15aa3e98d61946393385d0411e46a0169f60f3"
MAX_BYTES = 2 * 1024 * 1024
MAX_EVIDENCE_READ_BYTES = 2 * 1024 * 1024
EVIDENCE_NAMES = {
    "precision-summary.json",
    "decisions-evidence.json",
    "stages-evidence.json",
    "stage-residuals.json",
}
AXES = {
    "G": ("nivaa", "regjeringsforslag", "opprinnelig"),
    "H": ("nivaa", "stortingsvedtak", "opprinnelig"),
    "I": ("endring", "regjeringsforslag", "rnb"),
    "J": ("nivaa", "stortingsvedtak", "inkludert_rnb"),
    "K": ("endring", "stortingsvedtak", "forste_halvar_inkludert_rnb"),
    "L": ("endring", "kildeavhengig_forslag_eller_vedtak", "ovrig_etter_rnb"),
    "M": ("uavklart", "uavklart", "lonn_ikke_separat_avklart"),
    "N": ("endring", "regjeringsforslag", "nysaldering"),
    "docD": ("endring", "stortingsvedtak", "dokumentavhengig"),
}
STATUSES = {
    "VERIFIED_RAW_SOURCE",
    "VERIFIED_SOURCE_CORRESPONDENCE",
    "CONTROL_HYPOTHESIS",
    "PROPOSED_NORMALIZATION",
    "OPEN_QUESTION",
}
# Originalfeltene som v1 uttrykkelig avgrenser G/I til; ingen reservebevis.
PROPOSAL_ANCHORS: dict[str, dict[str, Any]] = {
    "G": {
        "cell": "G2",
        "key": ["1", "1"],
        "amount_kr": "14768000",
        "sha256": "09fca3a509d9b2d342187fee691b5faf378373fe25992538c8f6735cbe194bd8",
        "url": "https://www.regjeringen.no/no/dokumenter/prop.-1-s-gul-bok-20232024/id2998593/?ch=10",
        "xpath": "/html/body/main/div/div[3]/div[3]/div/div[1]/div/div[1]/table/tbody/tr[4]",
    },
    "I": {
        "cell": "I70",
        "key": ["151", "70"],
        "amount_kr": "-20000000",
        "sha256": "94cb91928eb173665de6111d13de6562b663fad8a4eddcdd01daab7b7fdf4594",
        "url": "https://www.regjeringen.no/no/dokumenter/prop.-104-s-20232024/id3039096/?ch=2",
        "xpath": "/html/body/main/div/div[3]/div[3]/div[33]/p",
    },
}


def proposed_h2024_integer(lexical: str) -> int | None:
    """Reproduser kun tallvilkårene i H2024-forslag-1, uten referanseinput.

    Gjelder forskningskandidaten for den bundne originalens numeriske H-felt.
    En kandidat er ingen kildeobservert, normalisert eller godkjent NOK-verdi.
    Formel-/kildeomfang må kontrolleres separat før denne tallfunksjonen brukes.
    """
    if len(lexical) > 128:
        return None
    try:
        with localcontext() as context:
            context.prec = 80
            raw = Decimal(lexical)
            if not raw.is_finite():
                return None
            binary = float(raw)
            if not math.isfinite(binary):
                return None
            factor = Decimal(1000000)
            ulp = Decimal.from_float(math.ulp(binary))
            if ulp * factor >= Decimal("0.5"):
                return None
            integer = (raw * factor).to_integral_value(rounding=ROUND_HALF_EVEN)
            ideal = integer / factor
            if abs(raw - ideal) <= ulp and binary == float(ideal):
                return int(integer)
    except (InvalidOperation, OverflowError, ValueError):
        return None
    return None


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Forventet JSON-objekt")
    return value


def _list(value: Any) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError("Forventet ikke-tom JSON-liste")
    return value


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"Gjentatt JSON-felt: {key}")
        result[key] = value
    return result


def _load(path: Path, *, limit: int = MAX_BYTES) -> tuple[bytes, Any]:
    with path.open("rb") as source:
        raw = source.read(limit + 1)
    _require(len(raw) <= limit, "Kontrollfil overstiger tillatt bytegrense")
    return raw, json.loads(raw, object_pairs_hook=_unique)


def _pointer(document: Any, pointer: Any) -> Any:
    _require(isinstance(pointer, str) and pointer.startswith("/"), "Ugyldig JSON-peker")
    try:
        for token in pointer[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(document, list):
                _require(re.fullmatch(r"0|[1-9][0-9]*", token) is not None, "Ugyldig listepeker")
                document = document[int(token)]
            else:
                document = document[token]
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise ValueError(f"Mangler bevis ved {pointer}") from error
    _require(document is not None and document != [] and document != {}, "Tomt kildebevis")
    return document


def _hash(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _original_proposals(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    prior = _list(matrix.get("prior_controls"))
    _require(len(prior) == 2, "Mangler G/I-originalbevis")
    leaves: dict[str, dict[str, Any]] = {}
    for index, (raw_control, column) in enumerate(zip(prior, ("G", "I"), strict=True)):
        control = _object(raw_control)
        anchor = PROPOSAL_ANCHORS[column]
        meaning, figure_type, stage = AXES[column]
        _require(
            set(control) == {"column", "cells", "meaning", "references", "sources"}
            and control["column"] == column
            and control["cells"] == [anchor["cell"]]
            and control["meaning"] == meaning,
            "Feil originalforslagskontroll",
        )
        sources = _list(control["sources"])
        references = _list(control["references"])
        _require(len(sources) == len(references) == 1, "Krever ett entydig originalforslagsbevis")
        source = _object(sources[0])
        _require(
            set(source) == {"sha256", "bytes", "url", "retrieved_date", "kind"}
            and source["sha256"] == anchor["sha256"]
            and source["url"] == anchor["url"]
            and type(source["bytes"]) is int
            and source["bytes"] > 0
            and isinstance(source["retrieved_date"], str)
            and isinstance(source["kind"], str)
            and bool(source["kind"].strip()),
            "Ugyldig originalforslagskilde",
        )
        _require(
            date.fromisoformat(source["retrieved_date"]).isoformat() == source["retrieved_date"],
            "Ugyldig hentedato",
        )
        reference = _object(references[0])
        _require(
            set(reference) == {"key", "amount_kr", "pointers", "scope", "source_budget_year"}
            and reference["key"] == anchor["key"]
            and reference["amount_kr"] == anchor["amount_kr"]
            and type(reference["source_budget_year"]) is int
            and reference["source_budget_year"] == 2024,
            "Ugyldig originalforslagsreferanse",
        )
        expected_scope = {
            "budget_year": 2024,
            "unit": "NOK",
            "candidate_multiplier": "1",
            "figure_type": figure_type,
            "stage": stage,
            "meaning": meaning,
            "period": "budsjettåret" if column == "G" else "rnb",
            "detail_level": "post",
            "budget_side": "begge",
            "reference_basis": "observert_kildefelt",
        }
        scope = _object(reference["scope"])
        _require(
            set(scope) == set(expected_scope)
            and all(
                type(scope[key]) is type(value) and scope[key] == value
                for key, value in expected_scope.items()
            ),
            "Uforenlig originalforslagsomfang",
        )
        pointers = _list(reference["pointers"])
        _require(len(pointers) == 1, "Krever én entydig originalforslagslokator")
        pointer = _object(pointers[0])
        _require(
            set(pointer) == {"source_sha256", "xpath", "short_evidence"}
            and pointer["source_sha256"] == source["sha256"]
            and pointer["xpath"] == anchor["xpath"]
            and isinstance(pointer["short_evidence"], str)
            and bool(pointer["short_evidence"].strip()),
            "Ugyldig eller ubundet originalforslagslokator",
        )
        leaves[f"/prior_controls/{index}"] = reference
    return leaves


def _evidence(
    refs: Any,
    column: str,
    matrix: dict[str, Any],
    documents: dict[str, Any],
    proposals: dict[str, dict[str, Any]],
) -> None:
    _require(isinstance(refs, list) and bool(refs), "Mangler kildebevis")
    expected = {"G": "/prior_controls/0", "I": "/prior_controls/1"}.get(column)
    if expected is not None:
        _require(refs == [{"matrix_pointer": expected}], "Mangler bundet G/I-originalreferanse")
    for raw_ref in refs:
        ref = _object(raw_ref)
        if set(ref) == {"matrix_pointer"}:
            # V1s kontrollpeker betegner det eneste, validerte referansebladet.
            pointer = ref["matrix_pointer"]
            _require(
                expected is not None and pointer == expected,
                "Ustøttet intern bevispeker",
            )
            _require(
                _pointer(matrix, f"{pointer}/references/0") == proposals[pointer],
                "Intern peker mangler validert originalforslagsreferanse",
            )
        else:
            _require(set(ref) == {"file", "pointer"}, "Ugyldig bevisreferanse")
            _require(ref["file"] in documents, "Ukjent bevisfil")
            _pointer(documents[ref["file"]], ref["pointer"])


def read_control_matrix(path: str | Path, *, expected_sha256: str | None = None) -> dict[str, Any]:
    """Valider valgt versjon, faglige akser og alle bundne bevisbyte/JSON-pekere.

    En forventet hash fra kontrollkvitteringen binder også selve matrisens byte.
    Funksjonen godkjenner ingen beløp og leses aldri fra innlesningsløpet.
    """
    matrix, _ = _load_control_matrix(path, expected_sha256=expected_sha256)
    return matrix


def _load_control_matrix(
    path: str | Path, *, expected_sha256: str | None = None
) -> tuple[dict[str, Any], str]:
    path = Path(path)
    raw, value = _load(path)
    sha256 = hashlib.sha256(raw).hexdigest()
    matrix = _object(value)
    if expected_sha256 is not None:
        _require(_hash(expected_sha256), "Ugyldig forventet SHA-256")
        _require(sha256 == expected_sha256, "Matrisehash avviker")
    _require(matrix.get("schema") == SCHEMA, "Ustøttet matriseskjema")
    _require(
        type(matrix.get("version")) is int and matrix["version"] == 1, "Ustøttet matriseversjon"
    )
    _require(matrix.get("id") == "p13-p2-2024-1", "Ustøttet matriseidentitet")
    _require(
        type(matrix.get("budget_year")) is int and matrix["budget_year"] == 2024,
        "Ustøttet budsjettår",
    )
    _require(matrix.get("created_date") == "2026-10-22", "Ustøttet matriserevisjon")
    _require(matrix.get("activation") == "NONE", "Matrisen kan ikke aktivere en tolkning")
    _require(matrix.get("normalized_values_changed") is False, "Ingen normalisering tillates")
    _require(matrix.get("year_coverage") == "NOT_ESTABLISHED", "Ingen årsdekning godkjennes")
    approval = {"status": "OPEN", "actor": None}
    _require(matrix.get("professional_approval") == approval, "Ustøttet godkjenning")
    binding = _object(_object(matrix.get("source_input_bindings")).get("workbook"))
    _require(
        binding.get("sha256") == WORKBOOK_SHA256 and binding.get("bytes") == 257569,
        "Ustøttet originalgrunnlag",
    )
    documents: dict[str, Any] = {}
    files = _list(matrix.get("evidence_files"))
    _require(len(files) == len(EVIDENCE_NAMES), "Krever nøyaktig fire bevisfiler")
    names: set[str] = set()
    read_budget = 0
    for entry in files:
        entry = _object(entry)
        _require(set(entry) == {"path", "sha256", "bytes", "kind"}, "Ugyldig bevismetadata")
        name = entry.get("path")
        _require(
            isinstance(name, str) and bool(re.fullmatch(r"[a-z0-9-]+\.json", name)),
            "Bevisfil må være et enkelt JSON-filnavn",
        )
        _require(name in EVIDENCE_NAMES, "Ukjent bevisfil")
        _require(name not in names, "Gjentatt bevisfil")
        names.add(name)
        _require(_hash(entry.get("sha256")), "Ugyldig bevishash")
        _require(
            type(entry["bytes"]) is int and 0 < entry["bytes"] < MAX_BYTES,
            "Ugyldig bevisstørrelse",
        )
        _require(
            entry["kind"] == "derived_research_summary_with_primary_locators",
            "Ukjent bevistype",
        )
        # Ett ekstra byte per fil oppdager overskridelse innen samlet lesebudsjett.
        read_budget += entry["bytes"] + 1
        _require(read_budget <= MAX_EVIDENCE_READ_BYTES, "Samlet bevisgrunnlag overstiger 2 MiB")
        _require(not (path.parent / name).is_symlink(), "Bevisfil kan ikke være symbolsk lenke")
    for entry in files:
        name = entry["path"]
        evidence_raw, evidence = _load(path.parent / name, limit=entry["bytes"])
        _require(hashlib.sha256(evidence_raw).hexdigest() == entry["sha256"], "Bevishash avviker")
        _require(len(evidence_raw) == entry.get("bytes"), "Bevisstørrelse avviker")
        documents[name] = evidence
    proposals = _original_proposals(matrix)
    rows = _list(matrix.get("rows"))
    _require(len(rows) == 9, "Krever alle ni kolonner")
    _require([_object(row).get("column") for row in rows] == list(AXES), "Feil kolonneomfang")
    for row in rows:
        column = row["column"]
        _require(row.get("id") == f"2024-{column}", "Ustøttet radidentitet")
        _require(row.get("budget_year") == 2024, "Feil radår")
        _require(
            row.get("sheet") == ("Dokumentiltknyntning2024" if column == "docD" else "Rådata"),
            "Feil arkomfang",
        )
        _require(
            tuple(row.get(k) for k in ("economic_meaning", "figure_type", "stage")) == AXES[column],
            "Ustøttet betydning, talltype eller stadium",
        )
        _require(
            row.get("source_factor") == ("1" if column == "docD" else "1000000"),
            "Ustøttet kildefaktor",
        )
        unit = _object(row.get("unit"))
        _require(
            unit.get("currency") == "NOK" and unit.get("universal_column_year_approval") is False,
            "Ustøttet enhet/generell godkjenning",
        )
        _require(row.get("raw_status") == "VERIFIED_RAW_SOURCE", "Ustøttet råstatus")
        _require(
            row.get("source_correspondence_status")
            in {"VERIFIED_RAW_SOURCE", "VERIFIED_SOURCE_CORRESPONDENCE"},
            "Ustøttet kildekontrollstatus",
        )
        _require(row.get("inference_status") == "CONTROL_HYPOTHESIS", "Ustøttet slutningsstatus")
        _require(row.get("professional_approval") == approval, "Ustøttet radgodkjenning")
        for field in (
            "period_cutoff",
            "hierarchy",
            "control_hypothesis",
            "remaining_question",
            "responsible_decision",
            "next_proof",
        ):
            _require(
                isinstance(row.get(field), str) and bool(row[field].strip()), f"Mangler {field}"
            )
        for field in ("allowed_control_use", "prohibited_analytic_use"):
            items = row.get(field)
            _require(
                isinstance(items, list)
                and bool(items)
                and all(isinstance(item, str) and bool(item.strip()) for item in items),
                f"Mangler {field}",
            )
        precision = _object(row.get("precision"))
        _require(
            precision.get("status") == "UNAPPROVED_NORMALIZATION"
            and precision.get("normalization_rule") is None
            and bool(precision.get("arithmetic")),
            "Ufullstendig eller aktivert presisjonsregel",
        )
        if column == "H":
            proposal = _object(precision.get("proposal"))
            _require(
                precision.get("proposal_status") == "PROPOSED_NORMALIZATION"
                and precision.get("proposal_applied") is False,
                "H-forslaget er ikke aktivert",
            )
            _require(
                proposal == documents["precision-summary.json"]["rule_proposal"],
                "H-forslag avviker fra målt bevis",
            )
        _evidence(row.get("source_evidence"), column, matrix, documents, proposals)
        scopes = row.get("subscopes")
        _require(isinstance(scopes, list) and bool(scopes), "Mangler avgrenset bruksomfang")
        ids: set[str] = set()
        for scope in scopes:
            scope = _object(scope)
            _require(
                isinstance(scope.get("id"), str) and scope["id"] not in ids,
                "Ugyldig eller gjentatt omfangsidentitet",
            )
            ids.add(scope["id"])
            _require(scope.get("status") in STATUSES, "Ustøttet omfangsstatus")
            _require(bool(scope.get("description")), "Mangler omfangsbeskrivelse")
            _evidence(scope.get("evidence"), column, matrix, documents, proposals)
    return matrix, sha256


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path, help="Eksakt matriseversjon; ingen automatisk siste")
    parser.add_argument("--sha256", help="Forventet matrisehash fra kontrollkvitteringen")
    args = parser.parse_args()
    try:
        matrix, sha256 = _load_control_matrix(args.matrix, expected_sha256=args.sha256)
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"status": "invalid", "error": str(error)}, ensure_ascii=False))
        return 1
    print(
        json.dumps(
            {
                "status": "valid",
                "id": matrix["id"],
                "budget_year": matrix["budget_year"],
                "columns": len(matrix["rows"]),
                "activation": matrix["activation"],
                "sha256": sha256,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
