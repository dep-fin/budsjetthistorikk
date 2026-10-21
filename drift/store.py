"""Kortvarige SQLite-transaksjoner for datojobb, kvitteringer og varig outbox."""

import hashlib
import json
import os
import socket
from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

from innlesning.maintenance_store import now, reading, writing
from innlesning.observations import encode, identity
from innlesning.source_attempts import initialize_attempts

from .config import Config

SCHEMA = """
CREATE TABLE IF NOT EXISTS daily_jobs (
 id TEXT PRIMARY KEY, pipeline TEXT NOT NULL, local_date TEXT NOT NULL,
 config_hash TEXT NOT NULL, config_json TEXT NOT NULL, state_json TEXT NOT NULL,
 status TEXT NOT NULL, result_json TEXT, UNIQUE(pipeline,local_date));
CREATE TABLE IF NOT EXISTS daily_attempts (
 id TEXT PRIMARY KEY, job_id TEXT NOT NULL, owner TEXT NOT NULL, started_utc TEXT NOT NULL,
 completed_utc TEXT, status TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS daily_reports (
 id TEXT PRIMARY KEY, job_id TEXT NOT NULL, report_json TEXT NOT NULL, sha256 TEXT NOT NULL,
 output_path TEXT NOT NULL, output_sha256 TEXT);
CREATE TABLE IF NOT EXISTS daily_run_artifacts (
 attempt_id TEXT PRIMARY KEY, output_path TEXT NOT NULL, sha256 TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS notification_outbox (
 id TEXT PRIMARY KEY, repository TEXT NOT NULL, anomaly_key TEXT NOT NULL,
 job_id TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL,
 status TEXT NOT NULL, error TEXT, UNIQUE(repository,anomaly_key,job_id));
CREATE TABLE IF NOT EXISTS github_issue_bindings (
 repository TEXT NOT NULL, anomaly_key TEXT NOT NULL, issue_number INTEGER NOT NULL,
 PRIMARY KEY(repository,anomaly_key));
"""


def start_day(
    config: Config, day: str
) -> tuple[str, str | None, dict[str, Any], dict[str, Any] | None]:
    config_data = {
        **asdict(config),
        "database": str(config.database.resolve()),
        "output_directory": str(config.output_directory.resolve()),
    }
    config_json = encode(config_data)
    digest = hashlib.sha256(config_json.encode()).hexdigest()
    job = identity("b7-date-1", config.pipeline_id, day)
    with writing(config.database) as connection:
        initialize_attempts(connection)
        for statement in SCHEMA.split(";"):
            if statement.strip():
                connection.execute(statement)
        # Kalleren eier OS-låsen; en gammel lease gir ingen overtakelsesrett.
        connection.execute(
            "UPDATE daily_attempts SET status='avbrutt',completed_utc=? WHERE status='kjorer'",
            (now(),),
        )
        existing = connection.execute(
            "SELECT config_hash,state_json,status,result_json FROM daily_jobs WHERE id=?", (job,)
        ).fetchone()
        if existing and existing[0] != digest:
            raise ValueError("Dagens konfigurasjon er frosset; bruk separat pipeline ved endring")
        if existing and existing[2] == "fullfort":
            return job, None, json.loads(existing[1]), json.loads(existing[3])
        if not existing:
            previous = connection.execute(
                "SELECT max(local_date) FROM daily_jobs WHERE pipeline=? AND local_date<?",
                (config.pipeline_id, day),
            ).fetchone()[0]
            first = (
                date.fromisoformat(previous) + timedelta(days=1)
                if previous
                else (
                    date.fromisoformat(config.first_date)
                    if config.first_date
                    else date.fromisoformat(day)
                )
            )
            while first < date.fromisoformat(day):
                missed = first.isoformat()
                connection.execute(
                    "INSERT OR IGNORE INTO daily_jobs VALUES (?,?,?,?,?,?,'uteblitt',NULL)",
                    (
                        identity("b7-date-1", config.pipeline_id, missed),
                        config.pipeline_id,
                        missed,
                        digest,
                        config_json,
                        "{}",
                    ),
                )
                first += timedelta(days=1)
            connection.execute(
                "INSERT INTO daily_jobs VALUES (?,?,?,?,?,?,'venter',NULL)",
                (job, config.pipeline_id, day, digest, config_json, "{}"),
            )
        state = json.loads(existing[1]) if existing else {}
        attempt = str(uuid4())
        connection.execute(
            "INSERT INTO daily_attempts VALUES (?,?,?,?,NULL,'kjorer')",
            (attempt, job, f"{socket.gethostname()}:{os.getpid()}", now()),
        )
        return job, attempt, state, None


def save_state(database: Path, job: str, state: dict[str, Any]) -> None:
    with writing(database) as connection:
        connection.execute("UPDATE daily_jobs SET state_json=? WHERE id=?", (encode(state), job))


def finish_day(database: Path, job: str, attempt: str, result: dict[str, Any]) -> None:
    with writing(database) as connection:
        connection.execute(
            "UPDATE daily_jobs SET status=?,result_json=? WHERE id=?",
            (
                {"full": "fullfort", "partial": "delvis", "failed": "feilet"}[result["outcome"]],
                encode(result),
                job,
            ),
        )
        connection.execute(
            "UPDATE daily_attempts SET status=?,completed_utc=? WHERE id=?",
            (result["outcome"], now(), attempt),
        )
        if result.get("run_report"):
            path = Path(result["run_report"])
            connection.execute(
                "INSERT INTO daily_run_artifacts VALUES (?,?,?)",
                (attempt, str(path), hashlib.sha256(path.read_bytes()).hexdigest()),
            )


def read_daily(database: Path, pipeline: str) -> tuple[dict[str, Any], ...]:
    if not database.exists():
        return ()
    with reading(database) as connection:
        if not connection.execute("SELECT 1 FROM sqlite_master WHERE name='daily_jobs'").fetchone():
            return ()
        jobs = connection.execute(
            "SELECT id,local_date,status,result_json FROM daily_jobs WHERE pipeline=? "
            "ORDER BY local_date",
            (pipeline,),
        ).fetchall()
        result = []
        for row in jobs:
            attempts = [
                dict(
                    zip(
                        ("id", "owner", "started_utc", "completed_utc", "status"),
                        attempt,
                        strict=True,
                    )
                )
                for attempt in connection.execute(
                    "SELECT id,owner,started_utc,completed_utc,status FROM daily_attempts "
                    "WHERE job_id=? ORDER BY rowid",
                    (row[0],),
                )
            ]
            result.append(
                {
                    "id": row[0],
                    "date": row[1],
                    "status": row[2],
                    "result": json.loads(row[3]) if row[3] else None,
                    "attempts": attempts,
                }
            )
        return tuple(result)


def freeze_report(database: Path, job: str, report_id: str, raw: str, output: Path) -> None:
    from analyse.session_serialization import report_from_json

    if report_from_json(raw).id != report_id:
        raise ValueError("Rapport-ID passer ikke innholdet")
    digest = hashlib.sha256(raw.encode()).hexdigest()
    with writing(database) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO daily_reports VALUES (?,?,?,?,?,NULL)",
            (report_id, job, raw, digest, str(output)),
        )


def read_frozen_report(database: Path, identifier: str) -> tuple[str, Path, str | None]:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT report_json,output_path,output_sha256,sha256 FROM daily_reports WHERE id=?",
            (identifier,),
        ).fetchone()
    if row is None or hashlib.sha256(row[0].encode()).hexdigest() != row[3]:
        raise ValueError("Ukjent eller endret rapportartefakt")
    return row[0], Path(row[1]), row[2]


def acknowledge_excel(database: Path, identifier: str, output: Path) -> None:
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    with writing(database) as connection:
        connection.execute(
            "UPDATE daily_reports SET output_sha256=? WHERE id=?", (digest, identifier)
        )


def enqueue(database: Path, job: str, repository: str, key: str, title: str, body: str) -> str:
    enqueue_many(database, job, repository, [(key, title, body)])
    return identity("github-outbox-1", repository, key, job)


def enqueue_many(
    database: Path, job: str, repository: str, notices: list[tuple[str, str, str]]
) -> None:
    rows = []
    for key, title, body in notices:
        if len(title) > 256 or len(body) > 60000:
            raise ValueError("GitHub-varsel overskrider lengdegrensen")
        identifier = identity("github-outbox-1", repository, key, job)
        rows.append((identifier, repository, key, job, title, body))
    with writing(database) as connection:
        connection.executemany(
            "UPDATE notification_outbox SET status='erstattet',error=? "
            "WHERE repository=? AND anomaly_key=? AND status='venter' AND job_id IN "
            "(SELECT id FROM daily_jobs WHERE local_date < "
            "(SELECT local_date FROM daily_jobs WHERE id=?))",
            [("erstattet_av:" + row[0], repository, row[2], job) for row in rows],
        )
        connection.executemany(
            "INSERT INTO notification_outbox VALUES (?,?,?,?,?,?,'venter',NULL) "
            "ON CONFLICT(repository,anomaly_key,job_id) DO UPDATE SET title=excluded.title, "
            "body=excluded.body,status=CASE WHEN notification_outbox.status='uavklart_post' "
            "THEN 'uavklart_post' ELSE 'venter' END",
            rows,
        )


def update_delivery(database: Path, job: str, result: dict[str, Any]) -> None:
    with writing(database) as connection:
        connection.execute("UPDATE daily_jobs SET result_json=? WHERE id=?", (encode(result), job))


def pending_notifications(database: Path, *, limit: int = -1) -> tuple[dict[str, Any], ...]:
    with reading(database) as connection:
        return tuple(
            dict(zip(("id", "repository", "key", "job", "title", "body", "status"), r, strict=True))
            for r in connection.execute(
                "SELECT id,repository,anomaly_key,job_id,title,body,status "
                "FROM notification_outbox "
                "WHERE status NOT IN ('levert','erstattet') ORDER BY rowid LIMIT ?",
                (limit,),
            )
        )


def uncertain_notifications(database: Path) -> set[tuple[str, str]]:
    with reading(database) as connection:
        return {
            (r[0], r[1])
            for r in connection.execute(
                "SELECT repository,anomaly_key FROM notification_outbox "
                "WHERE status='uavklart_post'"
            )
        }


def notification_status(
    database: Path, identifier: str, status: str, error: str | None = None
) -> None:
    with writing(database) as connection:
        connection.execute(
            "UPDATE notification_outbox SET status=?,error=? WHERE id=?",
            (status, error, identifier),
        )


def issue_binding(
    database: Path, repository: str, key: str, issue_number: int | None = None
) -> int | None:
    if issue_number is not None:
        with writing(database) as connection:
            connection.execute(
                "INSERT INTO github_issue_bindings VALUES (?,?,?) "
                "ON CONFLICT(repository,anomaly_key) "
                "DO UPDATE SET issue_number=excluded.issue_number",
                (repository, key, issue_number),
            )
    with reading(database) as connection:
        row = connection.execute(
            "SELECT issue_number FROM github_issue_bindings WHERE repository=? AND anomaly_key=?",
            (repository, key),
        ).fetchone()
    return int(row[0]) if row else None


def notification_count(database: Path, job: str) -> int:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT count(*) FROM notification_outbox WHERE job_id=?", (job,)
        ).fetchone()
    return int(row[0])
