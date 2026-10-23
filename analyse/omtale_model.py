"""Samme pilotfelter ved både modul-CLI og import; ingen endret formatbetydning."""

from dataclasses import dataclass

from innlesning.omtale import OmtaleBasis

FORMAT = "omtale-pilot-1"


@dataclass(frozen=True)
class Relation:
    id: str
    section_id: str
    event_id: str
    decision_revision_id: str
    observation_ids: tuple[str, ...]
    accounts: tuple[str, ...]
    role: str
    actor: str
    evidence_ids: tuple[str, ...]
    status: str
    professional_status: str
    reason: str


@dataclass(frozen=True)
class OmtaleReport:
    id: str
    base_json: str
    basis: OmtaleBasis
    relations: tuple[Relation, ...]
    visible_section_ids: tuple[str, ...]
    issues: tuple[str, ...]
    version: str = FORMAT
