"""SQLite lagrer råbyte og strukturerte rader i samme transaksjon."""

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .model import Allocation, Decision, Report

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
  sha256 TEXT PRIMARY KEY, raw_response BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY, source_sha256 TEXT NOT NULL REFERENCES sources(sha256),
  source_metadata TEXT NOT NULL, historical_sample INTEGER NOT NULL,
  status TEXT NOT NULL, contract_version TEXT NOT NULL, decision_json TEXT,
  source_totals_json TEXT NOT NULL, controls_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS allocations (
  run_id TEXT NOT NULL REFERENCES runs(run_id), ordinal INTEGER NOT NULL,
  locator TEXT NOT NULL, chapter TEXT NOT NULL, chapter_name TEXT NOT NULL,
  post TEXT NOT NULL, purpose TEXT NOT NULL, amount_text TEXT NOT NULL,
  amount_kr INTEGER, direction TEXT NOT NULL, raw_html TEXT NOT NULL,
  meaning TEXT NOT NULL, status TEXT NOT NULL, control_reason TEXT NOT NULL,
  PRIMARY KEY (run_id, ordinal)
);
"""


SCHEMA_VERSION = 2


def check_schema(connection: sqlite3.Connection) -> None:
    version = connection.execute("PRAGMA user_version").fetchone()[0]
    if version not in (0, SCHEMA_VERSION):
        raise ValueError(f"Ukjent databaseskjema: {version}")


def initialize(connection: sqlite3.Connection) -> None:
    """Additiv initialisering i kallerens transaksjon; ingen skjulte commits."""
    check_schema(connection)
    expected = {
        "sources": ["sha256", "raw_response"],
        "runs": [
            "run_id",
            "source_sha256",
            "source_metadata",
            "historical_sample",
            "status",
            "contract_version",
            "decision_json",
            "source_totals_json",
            "controls_json",
        ],
        "allocations": [
            "run_id",
            "ordinal",
            "locator",
            "chapter",
            "chapter_name",
            "post",
            "purpose",
            "amount_text",
            "amount_kr",
            "direction",
            "raw_html",
            "meaning",
            "status",
            "control_reason",
        ],
    }
    tables = {
        row[0]
        for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
        if row[0] != "sqlite_sequence"
    }
    if tables and not expected.keys() <= tables:
        raise ValueError("Ukjent eller ufullstendig databaseskjema; B1-tabeller mangler")
    for table, columns in expected.items():
        actual = [row[1] for row in connection.execute(f"PRAGMA table_info({table})")]
        if actual and actual != columns:
            raise ValueError(f"Ukjent tabellskjema: {table}")
    for statement in SCHEMA.split(";"):
        if statement.strip():
            connection.execute(statement)


def save_report_in(connection: sqlite3.Connection, raw: bytes, report: Report) -> None:
    connection.execute(
        "INSERT OR IGNORE INTO sources (sha256, raw_response) VALUES (?, ?)",
        (report.source_sha256, raw),
    )
    connection.execute(
        "INSERT INTO runs (run_id, source_sha256, source_metadata, historical_sample, status, "
        "contract_version, decision_json, source_totals_json, controls_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            report.run_id,
            report.source_sha256,
            json.dumps(report.source_metadata),
            report.historical_sample,
            report.status,
            report.contract_version,
            json.dumps(asdict(report.decision)) if report.decision else None,
            json.dumps(report.source_totals),
            json.dumps(report.controls),
        ),
    )
    for ordinal, line in enumerate(report.lines):
        connection.execute(
            "INSERT INTO allocations (run_id, ordinal, locator, chapter, chapter_name, post, "
            "purpose, amount_text, amount_kr, direction, raw_html, meaning, status, "
            "control_reason) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (report.run_id, ordinal, *asdict(line).values()),
        )


def save_report(database: Path, raw: bytes, report: Report) -> None:
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")
        initialize(connection)
        save_report_in(connection, raw, report)


def read_report(database: Path, run_id: str) -> Report:
    """Les ett lagret uttrekk; API-et summerer aldri flere importkjøringer."""
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as connection:
        check_schema(connection)
        connection.row_factory = sqlite3.Row
        row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if row is None:
            raise ValueError(f"Ukjent kjøring: {run_id}")
        records = connection.execute(
            "SELECT * FROM allocations WHERE run_id = ? ORDER BY ordinal", (run_id,)
        ).fetchall()
    decision: dict[str, Any] | None = (
        json.loads(row["decision_json"]) if row["decision_json"] else None
    )
    return Report(
        run_id=run_id,
        source_sha256=row["source_sha256"],
        source_metadata=json.loads(row["source_metadata"]),
        historical_sample=bool(row["historical_sample"]),
        status=row["status"],
        contract_version=row["contract_version"],
        decision=Decision(**decision) if decision else None,
        lines=[
            Allocation(
                **{key: record[key] for key in record.keys() if key not in ("run_id", "ordinal")}
            )
            for record in records
        ],
        source_totals=json.loads(row["source_totals_json"]),
        controls=json.loads(row["controls_json"]),
    )


def read_source(database: Path, sha256: str) -> bytes:
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as connection:
        check_schema(connection)
        row = connection.execute(
            "SELECT raw_response FROM sources WHERE sha256 = ?", (sha256,)
        ).fetchone()
    if row is None:
        raise ValueError(f"Ukjent kildeversjon: {sha256}")
    return bytes(row[0])
