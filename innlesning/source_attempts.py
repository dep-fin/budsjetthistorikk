"""Varig forsøk før HTTP. Ingen råhash oppfinnes når kildebyte ikke finnes."""

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from .maintenance_store import now, reading, writing

SCHEMA = """
CREATE TABLE IF NOT EXISTS source_attempts (
 sequence INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL UNIQUE,
 dataset TEXT NOT NULL, session TEXT NOT NULL, started_utc TEXT NOT NULL,
 after_job_sequence INTEGER NOT NULL, status TEXT NOT NULL, error TEXT,
 job_id TEXT UNIQUE, source_sha256 TEXT, metadata_json TEXT, completed_utc TEXT
);
"""


def initialize_attempts(connection: sqlite3.Connection) -> None:
    from .sync import initialize_sync_storage

    initialize_sync_storage(connection)
    connection.execute(SCHEMA)
    version = connection.execute("PRAGMA user_version").fetchone()[0]
    connection.execute(f"PRAGMA user_version={max(version, 5)}")


@dataclass(frozen=True)
class SourceAttempt:
    id: str
    dataset: str
    session: str
    started_utc: str
    status: str
    error: str | None
    job_id: str | None
    source_sha256: str | None
    metadata: dict[str, object] | None


def begin_source_attempt(database: Path, dataset: str, session: str) -> str:
    if dataset not in ("produksjon", "prove"):
        raise ValueError("Ukjent datasett")
    identifier = str(uuid4())
    with writing(database) as connection:
        initialize_attempts(connection)
        sequence = connection.execute("SELECT coalesce(max(sequence),0) FROM sync_jobs").fetchone()[
            0
        ]
        connection.execute(
            "INSERT INTO source_attempts "
            "(id,dataset,session,started_utc,after_job_sequence,status) "
            "VALUES (?,?,?,?,?,'venter')",
            (identifier, dataset, session, now(), sequence),
        )
    return identifier


def fail_source_attempt(database: Path, identifier: str, error_class: str) -> None:
    """Kun en kontrollert feilkode; unntakstekst/URL kan inneholde hemmeligheter."""
    if error_class not in {
        "transportfeil",
        "httpfeil",
        "ugyldig_kilde",
        "avbrutt",
        "behandlingsfeil",
    }:
        raise ValueError("Ukjent feilklasse")
    with writing(database) as connection:
        row = connection.execute(
            "SELECT job_id FROM source_attempts WHERE id=?", (identifier,)
        ).fetchone()
        if row is None:
            raise ValueError("Ukjent kildeforsøk")
        if row[0] is not None:
            raise ValueError("Et staged forsøk fullføres gjennom B2")
        connection.execute(
            "UPDATE source_attempts SET status='feilet',error=?,completed_utc=? WHERE id=?",
            (error_class, now(), identifier),
        )


def save_attempt_response(
    database: Path,
    identifier: str,
    raw: bytes,
    metadata: dict[str, object],
    *,
    complete: bool = False,
) -> None:
    from .ingestion import MAX_BYTES

    retrieved = datetime.fromisoformat(str(metadata.get("retrieved_utc", "")))
    if retrieved.tzinfo is None or retrieved.utcoffset() is None:
        raise ValueError("Hentetid krever tidssone")
    if (
        len(raw) > MAX_BYTES
        or metadata.get("sha256") != hashlib.sha256(raw).hexdigest()
        or metadata.get("bytes") != len(raw)
        or metadata.get("status") != 200
    ):
        raise ValueError("Kilderesponsens proveniens er ugyldig")
    with writing(database) as connection:
        existing = connection.execute(
            "SELECT source_sha256,metadata_json FROM source_attempts WHERE id=?", (identifier,)
        ).fetchone()
        if (
            existing
            and existing[0] is not None
            and (existing[0] != metadata["sha256"] or json.loads(existing[1]) != metadata)
        ):
            raise ValueError("Ny respons kan ikke erstatte et allerede bevart forsøk")
        connection.execute(
            "INSERT OR IGNORE INTO sources (sha256,raw_response) VALUES (?,?)",
            (metadata["sha256"], raw),
        )
        cursor = connection.execute(
            "UPDATE source_attempts SET source_sha256=?,metadata_json=?,status=?,completed_utc=? "
            "WHERE id=? AND status='venter' AND job_id IS NULL",
            (
                metadata["sha256"],
                json.dumps(metadata),
                "fullfort" if complete else "venter",
                now() if complete else None,
                identifier,
            ),
        )
        if cursor.rowcount != 1:
            raise ValueError("Kildeforsøket er ikke ventende")


def read_source_attempt(database: Path, identifier: str) -> SourceAttempt:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT a.id,a.dataset,a.session,a.started_utc,coalesce(j.status,a.status),"
            "a.error,a.job_id,a.source_sha256,a.metadata_json "
            "FROM source_attempts a LEFT JOIN sync_jobs j ON a.job_id=j.job_id WHERE a.id=?",
            (identifier,),
        ).fetchone()
        if row is None:
            raise ValueError("Ukjent kildeforsøk")
        values = list(row)
        values[-1] = json.loads(values[-1]) if values[-1] is not None else None
        return SourceAttempt(*values)


def bind_attempt(
    connection: sqlite3.Connection,
    identifier: str,
    dataset: str,
    session: str,
    job_id: str,
    metadata: dict[str, object],
) -> None:
    """Kalles i B2s stagingtransaksjon; tapt acknowledgement kan slås opp igjen."""
    row = connection.execute(
        "SELECT dataset,session,status,job_id,source_sha256,metadata_json "
        "FROM source_attempts WHERE id=?",
        (identifier,),
    ).fetchone()
    if row is None or tuple(row[:4]) != (dataset, session, "venter", None):
        raise ValueError("Kildeforsøket passer ikke jobben eller er allerede bundet")
    if row[4] is not None and (row[4] != metadata["sha256"] or json.loads(row[5]) != metadata):
        raise ValueError("Staging passer ikke bevart HTTP-respons i kildeforsøket")
    connection.execute(
        "UPDATE source_attempts SET status='staged',job_id=?,source_sha256=?,metadata_json=? "
        "WHERE id=?",
        (job_id, metadata["sha256"], json.dumps(metadata), identifier),
    )


def latest_unstaged(
    connection: sqlite3.Connection, dataset: str, session: str, job_sequence: int
) -> sqlite3.Row | tuple[object, ...] | None:
    if not connection.execute(
        "SELECT 1 FROM sqlite_master WHERE name='source_attempts'"
    ).fetchone():
        return None
    row: sqlite3.Row | tuple[object, ...] | None = connection.execute(
        "SELECT id,status,error,source_sha256 FROM source_attempts WHERE dataset=? AND session=? "
        "AND job_id IS NULL AND after_job_sequence>=? ORDER BY sequence DESC LIMIT 1",
        (dataset, session, job_sequence),
    ).fetchone()
    return row
