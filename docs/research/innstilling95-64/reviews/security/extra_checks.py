"""New successful export plus source-pin and historical event identity probes."""

import argparse
import base64
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

from analyse import innstilling95 as t6
from analyse import innstilling95_excel as excel
from analyse.omtale_excel_guard import inspect_excel
from innlesning.observations import encode
from innlesning.omtale import identified

from .audit_checks import rehash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    report = t6.read_json(Path(".local/full-acceptance/t6-files0/tomt.json"))
    frozen, book_path = args.audit / "clean.json", args.audit / "clean.xlsx"
    excel.export_pair(report, frozen, book_path)
    assert t6.read_json(frozen) == excel.read_excel(book_path) == report
    rows = [
        {
            "name": "new_public_pair_written_closed_reread",
            "result": "pass",
            "json_sha256": hashlib.sha256(frozen.read_bytes()).hexdigest(),
            "xlsx_sha256": hashlib.sha256(book_path.read_bytes()).hexdigest(),
        }
    ]
    for name in ("source_verified", "source_expected_pin", "new_step", "old_step"):
        basis = report.basis
        if name.startswith("source"):
            source = next(s for s in basis.sources if s.name.endswith("sak-100889.xml"))
            original = base64.b64decode(source.content_base64, validate=True)
            malicious = original.replace(b"100889", b"100888")
            assert malicious != original
            changes = {
                "content_base64": base64.b64encode(malicious).decode(),
                "sha256": hashlib.sha256(malicious).hexdigest(),
                "byte_count": len(malicious),
            }
            if name == "source_expected_pin":
                changes["expected_sha256"] = changes["sha256"]
            fake = replace(source, **changes)
            basis = replace(basis, sources=tuple(fake if s == source else s for s in basis.sources))
        elif name == "new_step":
            obs = basis.observations[0]
            basis = replace(
                basis,
                observations=(replace(obs, step_id="invented-step"), *basis.observations[1:]),
            )
        else:
            prior = basis.t5_basis.t1_basis
            obs = prior.observations[0]
            prior = identified(
                "visningsgrunnlag-1",
                replace(
                    prior,
                    observations=(
                        replace(obs, step_id="invented-old-step"),
                        *prior.observations[1:],
                    ),
                ),
            )
            basis = replace(
                basis,
                t5_basis=identified(
                    "proposisjonsgrunnlag16-1", replace(basis.t5_basis, t1_basis=prior)
                ),
            )
        poisoned = identified("innstilling95-1", replace(report, basis=rehash(basis)))
        raw = encode({"format": "innstilling95-1", "report": asdict(poisoned)})
        json_path, xlsx_path = (
            args.audit / ("extra-" + name + ".json"),
            args.audit / ("extra-" + name + ".xlsx"),
        )
        with json_path.open("x", encoding="utf8") as handle:
            handle.write(raw)
        book = excel._book(poisoned, raw)
        book.save(xlsx_path)
        book.close()
        assert (
            inspect_excel(
                xlsx_path,
                sheet_names=excel.SHEET_NAMES,
                snapshot_name="Visningsgrunnlag",
                max_expanded_bytes=128 * 1024 * 1024,
            )[0]
            == raw
        )
        for kind, reader, path in (
            ("json", t6.read_json, json_path),
            ("xlsx", excel.read_excel, xlsx_path),
        ):
            try:
                reader(path)
            except ValueError as error:
                rows.append(
                    {"name": name + "_" + kind, "result": "rejected", "message": str(error)}
                )
            else:
                raise AssertionError("Hostile source/event identity was accepted")
    with (args.audit / "extra.json").open("x", encoding="utf8", newline="\n") as handle:
        handle.write(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"groups": len(rows), "all_expected": True}))


if __name__ == "__main__":
    main()
