"""Reproduser T6 fra offentlige repo-originaler, uten nett eller database."""

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analyse import innstilling95 as t6  # noqa: E402
from analyse import proposisjon16 as t5  # noqa: E402
from analyse.innstilling95_excel import export_originals, export_pair, read_excel  # noqa: E402
from innlesning.innstilling95 import reconstruct  # noqa: E402
from innlesning.visningspilot_model import PilotSelection  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--existing", type=Path)
    parser.add_argument("--legacy-t5", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    authentic = gzip.decompress(
        Path("tests/fixtures/t2/authentic-t1.json.gz").read_bytes()
    ).decode()
    old = t5.import_basis(authentic)
    old_json = t5.report_to_json(t5.build_report(old, PilotSelection()))
    basis = t6.import_basis(old_json)
    assert basis.t5_basis == old
    assert {r.role for r in basis.relations if r.role.startswith("95.")} == {
        "95.II.1→360.II.1",
        "95.III.1→361.III.1",
        "95.III.2→361.III.2",
        "95.IV.1→362.IV.1",
        "95.V.1→363.V.1",
        "95.V.2→363.V.2",
        "95.VI.1→364.VI.1",
        "95.VI.2→364.VI.2",
    }
    data = t6.contents(basis)
    assert len(data.observations) == 339
    assert sum(o.figure_type == "stortingsvedtak" for o in data.observations) == 114
    assert len({o.step_id for o in data.observations if o.figure_type == "stortingsvedtak"}) == 38
    oracle = json.loads(
        Path("docs/research/innstilling95-64/independent/original-fields.json").read_text("utf8")
    )
    fields = {
        (o.source_unit_id, o.chapter + "/" + o.post, o.meaning): o for o in basis.observations
    }
    for key, section in (("inns95", "innstilling_rows"), ("vedtak359", "decision_rows")):
        for row in oracle[section]:
            for meaning, value in (
                ("for_belop", "before_kr"),
                ("endring", "change_kr"),
                ("etter_belop", "after_kr"),
            ):
                observation = fields[key, row["account"], meaning]
                assert observation.amount_kr == row["values"][value]
                assert observation.pointer.artifact_id == row["pointers"][value]["source_sha256"]
                assert observation.raw_value == row["pointers"][value]["raw_number"]
    ids = {d.key: d.id for d in data.documents}
    cases = {
        "post32": PilotSelection(years=(2024,), accounts=(("1420", "32"),)),
        "utgift": PilotSelection(years=(2024,), accounts=(("1400", "1"),)),
        "null": PilotSelection(years=(2024,), accounts=(("4400", "2"),)),
        "fullmakt": PilotSelection(years=(2024,), accounts=(("1420", "66"),)),
        "delt-ramme": PilotSelection(
            years=(2024,), accounts=(("1420", "39"), ("1420", "69"), ("1420", "79"))
        ),
        "1429-1": PilotSelection(years=(2024,), accounts=(("1429", "1"),)),
        "1429-22": PilotSelection(years=(2024,), accounts=(("1429", "22"),)),
        "1429-60": PilotSelection(years=(2024,), accounts=(("1429", "60"),)),
        "1533-45": PilotSelection(years=(2024,), accounts=(("1533", "45"),)),
        "flere": PilotSelection(
            years=(2024,), chapters=("1429",), accounts=(("1420", "32"), ("4400", "2"))
        ),
        "kapittel": PilotSelection(years=(2024,), chapters=("4400",)),
        "tomt": PilotSelection(years=(2024,)),
        "mangler": PilotSelection(years=(2024,), accounts=(("999", "99"),)),
        "feil-aar": PilotSelection(years=(2025,), chapters=("1420",)),
        "uten-aar": PilotSelection(chapters=("1420",)),
        "cross-pair": PilotSelection(years=(2024,), accounts=(("1400", "1"), ("1420", "21"))),
        "begge1429": PilotSelection(years=(2024,), chapters=("1429",)),
        "hele-unionen": PilotSelection(
            years=(2024,),
            chapters=(
                "1400",
                "1410",
                "1411",
                "1412",
                "1420",
                "1423",
                "1429",
                "1471",
                "1474",
                "1481",
                "1482",
                "4400",
                "4420",
                "4471",
                "4481",
            ),
        ),
    }
    cases.update(
        {
            key: PilotSelection(mode="document", document_id=ids[key])
            for key in (
                "prop16",
                "inns95",
                "vedtak359",
                "vedtak360",
                "vedtak361",
                "vedtak362",
                "vedtak363",
                "vedtak364",
            )
        }
    )
    reports = {name: t6.build_report(basis, selection) for name, selection in cases.items()}
    reports["konto-dokument"] = t6.open_document(reports["flere"], ids["inns95"])
    reports["dokument-konto"] = t6.open_accounts(reports["inns95"], cases["flere"])
    results = []
    expected_counts = {
        "post32": (6, 3, 1),
        "utgift": (9, 3, 1),
        "null": (9, 3, 1),
        "delt-ramme": (9, 3, 1),
        "1429-1": (9, 3, 1),
        "1429-22": (9, 3, 1),
        "flere": (33, 12, 4),
        "kapittel": (18, 6, 2),
        "cross-pair": (18, 6, 2),
        "begge1429": (18, 6, 2),
        "hele-unionen": (339, 114, 38),
        "prop16": (111, 0, 0),
        "inns95": (108, 0, 0),
        "vedtak359": (108, 108, 36),
        "konto-dokument": (108, 0, 0),
        "dokument-konto": (33, 12, 4),
    }
    for name, expected in reports.items():
        directory = args.existing or args.output
        frozen, excel = directory / (name + ".json"), directory / (name + ".xlsx")
        if args.existing is None:
            export_pair(expected, frozen, excel)
        actual = t6.read_json(frozen)
        assert read_excel(excel) == actual == expected
        assert (
            len(actual.view.observation_ids),
            len(actual.view.adopted_observation_ids),
            len(actual.view.adopted_event_ids),
        ) == expected_counts.get(name, (0, 0, 0))
        results.append(
            {
                "case": name,
                "report_id": actual.id,
                "fields": len(actual.view.observation_ids),
                "adopted_fields": len(actual.view.adopted_observation_ids),
                "events": len(actual.view.adopted_event_ids),
                "comparisons": len(actual.view.comparisons),
                "json_sha256": hashlib.sha256(frozen.read_bytes()).hexdigest(),
                "xlsx_sha256": hashlib.sha256(excel.read_bytes()).hexdigest(),
            }
        )
    assert t6.go_back(reports["konto-dokument"]) == reports["flere"]
    assert t6.go_back(reports["dokument-konto"]) == reports["inns95"]
    original_directory = args.output / "originals"
    export_originals(reports["inns95"], original_directory)
    for recipe in basis.recipes:
        raw = reconstruct(basis.t5_basis, basis.sources, recipe)
        name = str(40034220 + int(recipe.document_key[6:]) - 359) + ".xml"
        assert raw == (original_directory / "vedtak" / name).read_bytes()
        assert (
            raw == Path("docs/research/to-visninger-37/originals/forgrening/" + name).read_bytes()
        )
    legacy = None
    if args.legacy_t5:
        before = hashlib.sha256(args.legacy_t5.read_bytes()).hexdigest()
        previous = t5.read_json(args.legacy_t5)
        assert t6.import_basis(t5.report_to_json(previous)).t5_basis == previous.basis
        assert hashlib.sha256(args.legacy_t5.read_bytes()).hexdigest() == before
        legacy = {"sha256": before, "report_id": previous.id, "basis_id": previous.basis.id}
    evidence = {
        "base": "9616fbe6a8ab15eec696f34de76888565a784f8f",
        "basis_id": basis.id,
        "old_t5_basis_id": old.id,
        "global_fields": len(data.observations),
        "adopted_fields": sum(o.figure_type == "stortingsvedtak" for o in data.observations),
        "events": len({o.step_id for o in data.observations if o.figure_type == "stortingsvedtak"}),
        "recipes": [r.document_key for r in basis.recipes],
        "pairs": results,
        "legacy_t5": legacy,
        "limits": (
            "Native Excel, full faglig teksttolkning, kontinuitet og årsdekning "
            "er ikke prøvd/etablert."
        ),
    }
    (args.output / "result.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf8", newline="\n"
    )
    print(
        json.dumps(
            {"pairs": len(results), "fields": len(data.observations), "events": evidence["events"]}
        )
    )


if __name__ == "__main__":
    main()
