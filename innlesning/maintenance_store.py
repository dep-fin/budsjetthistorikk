"""Additiv SQL4-lagring for filer, register og faglige kontrollavgjørelser."""

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .observations import encode, identity, initialize_observations
from .storage import check_schema

SCHEMA = """
CREATE TABLE IF NOT EXISTS register_snapshots (id TEXT PRIMARY KEY, content TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS register_heads (
 singleton INTEGER PRIMARY KEY, snapshot_id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS maintenance_exports (
 id TEXT PRIMARY KEY, kind TEXT NOT NULL, content TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS maintenance_imports (
 id TEXT PRIMARY KEY, kind TEXT NOT NULL, sha256 TEXT NOT NULL, filename TEXT NOT NULL,
 raw BLOB, result TEXT NOT NULL, created_utc TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS control_bases (id TEXT PRIMARY KEY, description TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS control_activations (
 scope TEXT NOT NULL, generation INTEGER NOT NULL, content TEXT NOT NULL,
 created_utc TEXT NOT NULL, PRIMARY KEY(scope,generation));
CREATE TABLE IF NOT EXISTS professional_decisions (
 id TEXT PRIMARY KEY, observation_id TEXT NOT NULL, predecessor TEXT,
 content TEXT NOT NULL, created_utc TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS professional_decisions_observation
 ON professional_decisions(observation_id);
CREATE TABLE IF NOT EXISTS control_evidence (
 id TEXT PRIMARY KEY, content TEXT NOT NULL, raw BLOB NOT NULL, filename TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS controlled_results (id TEXT PRIMARY KEY, content TEXT NOT NULL);
"""


def now() -> str:
    return datetime.now(UTC).isoformat()


@contextmanager
def writing(database: Path) -> Iterator[sqlite3.Connection]:
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("BEGIN IMMEDIATE")
        initialize_observations(connection)
        for statement in SCHEMA.split(";"):
            if statement.strip():
                connection.execute(statement)
        version = connection.execute("PRAGMA user_version").fetchone()[0]
        connection.execute(f"PRAGMA user_version={max(version, 4)}")
        yield connection


@contextmanager
def reading(database: Path) -> Iterator[sqlite3.Connection]:
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as connection:
        check_schema(connection)
        yield connection


@dataclass(frozen=True)
class Diagnostic:
    sheet: str
    row: int
    field: str
    message: str


@dataclass(frozen=True)
class ImportResult:
    id: str
    kind: str
    new_ids: tuple[str, ...] = ()
    reused_ids: tuple[str, ...] = ()
    errors: tuple[Diagnostic, ...] = ()
    snapshot_id: str | None = None


def imported(connection: sqlite3.Connection, identifier: str) -> ImportResult | None:
    row = connection.execute(
        "SELECT result FROM maintenance_imports WHERE id=?", (identifier,)
    ).fetchone()
    if not row:
        return None
    data = json.loads(row[0])
    data["new_ids"] = tuple(data["new_ids"])
    data["reused_ids"] = tuple(data["reused_ids"])
    data["errors"] = tuple(Diagnostic(**item) for item in data["errors"])
    return ImportResult(**data)


def read_import(database: Path, identifier: str) -> ImportResult:
    with reading(database) as connection:
        result = imported(connection, identifier)
    if result is None:
        raise ValueError("Ukjent import-ID")
    return result


def read_import_source(database: Path, identifier: str) -> bytes:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT raw FROM maintenance_imports WHERE id=?", (identifier,)
        ).fetchone()
    if row is None:
        raise ValueError("Ukjent import-ID")
    if row[0] is None:
        raise ValueError("Filen ble avvist før innlesning; ingen råbyte er bevart")
    return bytes(row[0])


def save_import(
    connection: sqlite3.Connection, result: ImportResult, path: Path, raw: bytes | None, sha256: str
) -> None:
    from dataclasses import asdict

    connection.execute(
        "INSERT INTO maintenance_imports VALUES (?,?,?,?,?,?,?)",
        (result.id, result.kind, sha256, str(path.resolve()), raw, encode(asdict(result)), now()),
    )


def reject_large_file(database: Path, path: Path, kind: str, sheet: str) -> ImportResult:
    """Bevar avvisningen uten å lese en fil som overskrider den harde bytegrensen."""
    stat = path.stat()
    identifier = identity(
        "avvist-for-innlesning-v1", kind, str(path.resolve()), stat.st_size, stat.st_mtime_ns
    )
    with writing(database) as connection:
        previous = imported(connection, identifier)
        if previous:
            return previous
        result = ImportResult(
            identifier,
            kind,
            errors=(
                Diagnostic(
                    sheet,
                    0,
                    "fil",
                    f"Filen har {stat.st_size} byte og overstiger 8 MiB; "
                    "råbyte og filhash er ikke innlest",
                ),
            ),
        )
        save_import(connection, result, path, None, "")
    return result


def export_basis(connection: sqlite3.Connection, identifier: str, kind: str) -> dict[str, Any]:
    row = connection.execute(
        "SELECT content FROM maintenance_exports WHERE id=? AND kind=?", (identifier, kind)
    ).fetchone()
    if row is None:
        raise ValueError("Ukjent eksportert grunnlag")
    result: dict[str, Any] = json.loads(row[0])
    return result
