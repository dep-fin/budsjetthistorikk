"""Ubetrodde arbeidsfiler avvises samlet; opprinnelig kilde og kompatibilitet består."""

import sqlite3
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from test_b2 import RAW, metadata
from test_b4 import ingest

from innlesning import read_source, resume_sync, stage_sync
from innlesning.maintenance_store import read_import_source
from innlesning.registers import export_register, import_register, seed_register


@pytest.mark.parametrize("malformation", ["header", "zip", "xml", "rows", "cell"])
def test_invalid_files_are_preserved_and_error_is_readable(
    tmp_path: Path, malformation: str
) -> None:
    database = tmp_path / "files.sqlite"
    seed = seed_register(database)
    path = tmp_path / ("bad.xlsx" if malformation in {"zip", "xml"} else "bad.csv")
    if malformation == "zip":
        with ZipFile(path, "w", ZIP_DEFLATED) as archive:
            # Komprimert under 8 MiB; uakseptabelt antall ZIP-medlemmer.
            for i in range(129):
                archive.writestr(str(i), "x")
    elif malformation == "xml":
        with ZipFile(path, "w") as archive:
            archive.writestr("[Content_Types].xml", "<broken")
    else:
        export_register(database, seed.id, path)
        if malformation == "header":
            path.write_text("wrong\n", encoding="utf-8")
        elif malformation == "rows":
            with path.open("a", encoding="utf-8") as target:
                target.write("x\n" * 10001)
        else:
            with path.open("a", encoding="utf-8") as target:
                target.write("x" * 30001)
    raw = path.read_bytes()
    result = import_register(database, path)
    assert result.errors and not result.new_ids
    assert read_import_source(database, result.id) == raw


def test_export_does_not_overwrite_database_import_or_source_and_preserves_existing_on_error(
    tmp_path: Path,
) -> None:
    database = tmp_path / "data.sqlite"
    source = ingest(database, "40034443")
    seed = seed_register(database)
    with pytest.raises(ValueError, match="databasen"):
        export_register(database, seed.id, database)
    original_file = tmp_path / "original.csv"
    original_file.write_bytes(read_source(database, source.artifact.sha256))
    with pytest.raises(ValueError, match="original kildefil"):
        export_register(database, seed.id, original_file)
    imported_file = tmp_path / "register.csv"
    export_register(database, seed.id, imported_file)
    assert not import_register(database, imported_file).errors
    original = imported_file.read_bytes()
    with pytest.raises(ValueError, match="import-/kildefil"):
        export_register(database, seed.id, imported_file)
    assert imported_file.read_bytes() == original
    wrong_extension = tmp_path / "keep.txt"
    wrong_extension.write_bytes(b"preserved")
    with pytest.raises(ValueError, match=".xlsx"):
        export_register(database, seed.id, wrong_extension)
    assert wrong_extension.read_bytes() == b"preserved"


def test_sql4_keeps_pending_b2_resume_and_later_b3_writes_without_downgrade(tmp_path: Path) -> None:
    from innlesning import extract_revision, read_sync

    database = tmp_path / "migration.sqlite"
    pending = stage_sync(database, RAW, metadata(RAW), historical_sample=True)
    seed_register(database)
    resume_sync(database, pending)
    revision = read_sync(database, pending).entries[0].revision_id
    extract_revision(database, revision)
    with sqlite3.connect(database) as connection:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == 4
        connection.execute("PRAGMA user_version=6")
    with pytest.raises(ValueError, match="Ukjent databaseskjema: 6"):
        seed_register(database)


def test_size_rejection_is_durable_without_reading_or_claiming_raw_bytes(tmp_path: Path) -> None:
    from innlesning import read_import

    path = tmp_path / "large.csv"
    with path.open("wb") as target:
        target.seek(8 * 1024 * 1024)
        target.write(b"x")
    database = tmp_path / "limit.sqlite"
    result = import_register(database, path)
    assert result.errors and read_import(database, result.id) == result
    with pytest.raises(ValueError, match="ingen råbyte"):
        read_import_source(database, result.id)


def test_csv_preserves_literal_apostrophe_and_escapes_dangerous_prefixes(tmp_path: Path) -> None:
    from test_b5_register import edit_rows

    from innlesning import read_register

    database = tmp_path / "text.sqlite"
    seed = seed_register(database)
    path = tmp_path / "text.csv"
    export_register(database, seed.id, path)
    # Saksbehandleren skriver en tekstlig proveniens, ingen formelkjøring.
    edit_rows(path, lambda rows: rows[1].update(begrunnelse="''=literal"))
    imported = import_register(database, path)
    snapshot = read_register(database, imported.snapshot_id)
    assert snapshot.departments[0].reason == "'=literal"
    output = tmp_path / "next.csv"
    export_register(database, snapshot.id, output)
    roundtrip = import_register(database, output)
    assert not roundtrip.errors and roundtrip.snapshot_id == snapshot.id
    assert "''=literal" in output.read_text(encoding="utf-8-sig")
