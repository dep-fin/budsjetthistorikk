"""Én lokal kalenderdato, aldri 24 timer som erstatning for neste dag."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

OSLO = ZoneInfo("Europe/Oslo")


def due_date(now: datetime) -> str | None:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Kjøretid krever tidssone")
    local = now.astimezone(OSLO)
    return local.date().isoformat() if local.time() >= time(6) else None


def next_due(now: datetime) -> datetime:
    due_date(now)
    local = now.astimezone(OSLO)
    day = local.date() + timedelta(days=local.time() >= time(6))
    return datetime.combine(day, time(6), OSLO)
