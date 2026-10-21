"""Eksplisitt driftsgrunnlag; ingen hemmeligheter lagres i konfigurasjonen."""

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from innlesning.ingestion import START_SESSION, session_url

AUTHORIZED_REPOSITORY = "depmartin/budsjetthistorikk"


@dataclass(frozen=True)
class Config:
    pipeline_id: str
    database: Path
    output_directory: Path
    register_snapshot: str
    repository: str = AUTHORIZED_REPOSITORY
    dataset: str = "produksjon"
    first_session: str = START_SESSION
    first_date: str | None = None
    token_environment: str = "BUDSJETTHISTORIKK_GITHUB_TOKEN"
    timeout: int = 30
    control_basis: str | None = None

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", self.pipeline_id):
            raise ValueError("Pipeline-ID krever 1–80 bokstaver/tall/understrek/bindestrek")
        if self.repository != AUTHORIZED_REPOSITORY:
            raise ValueError("GitHub-mottaker må være det autoriserte repoet")
        if self.dataset not in ("produksjon", "prove"):
            raise ValueError("Ukjent datasett")
        session_url(self.first_session)
        if self.dataset == "produksjon" and self.first_session != START_SESSION:
            raise ValueError("Produksjon skal kontrollere alle sesjoner fra 2026-2027")
        if (
            not isinstance(self.register_snapshot, str)
            or not self.register_snapshot.strip()
            or type(self.timeout) is not int
            or not 1 <= self.timeout <= 120
        ):
            raise ValueError("Eksplisitt registersnapshot og timeout 1–120 kreves")
        if self.control_basis is not None and (
            not isinstance(self.control_basis, str) or not self.control_basis.strip()
        ):
            raise ValueError("Kontrollgrunnlag krever eksakt ikke-tom ID")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]{0,100}", self.token_environment):
            raise ValueError("Token angis bare som navn på miljøvariabel")
        if self.first_date is not None:
            date.fromisoformat(self.first_date)
        if not self.database.is_absolute() or not self.output_directory.is_absolute():
            raise ValueError("Database og rapportmappe krever absolutte baner")
        if self.database.resolve() == self.output_directory.resolve():
            raise ValueError("Database og rapportmappe må være ulike")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        values = dict(data)
        values["database"] = Path(values["database"])
        values["output_directory"] = Path(values["output_directory"])
        return cls(**values)
