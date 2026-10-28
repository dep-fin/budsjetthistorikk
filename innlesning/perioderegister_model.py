"""P1s lukkede immutable typer. Eldre modeller beholdes ordrett."""

from dataclasses import dataclass

from .fleraarspilot_model import Basis as T4Basis
from .forlopspilot_model import Calculation
from .komitepilot_model import Payload, Source
from .visningspilot_model import (
    InventoryItem,
    PilotDocument,
    PilotRelation,
    PilotSelection,
    PilotView,
    Statement,
)

FORMAT = "perioderegister-1"
RULE = "periode1429-2024-1"


@dataclass(frozen=True)
class Evidence:
    id: str
    source_id: str
    locator: str
    representation_sha256: str
    role: str


@dataclass(frozen=True)
class PeriodEntry:
    id: str
    key: str
    document_id: str
    decision_api_id: str | None
    case_id: str | None
    budget_year: int | None
    accounts: tuple[str, ...]
    post_link: str
    role: str
    round: str
    actor: str
    status: str
    reason: str
    evidence_ids: tuple[str, ...]
    observation_ids: tuple[str, ...]
    event_ids: tuple[str, ...]
    professional_status: str


@dataclass(frozen=True)
class CaseCandidate:
    id: str
    index_session: str
    ordinal_1based: int
    case_id: str
    document_id: str
    metadata_json: str
    budget_year: int | None
    accounts: tuple[str, ...]
    post_link: str
    status: str
    reason: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class DecisionCandidate:
    id: str
    session: str
    decision_api_id: str
    number: str
    document_id: str
    budget_year: int | None
    accounts: tuple[str, ...]
    post_link: str
    status: str
    reason: str
    raw_preservation: str
    product_structuring: str
    professional_approval: str
    monetary_effect: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class CoverageGap:
    id: str
    key: str
    title: str
    status: str
    reason: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class Basis:
    id: str
    rule: str
    t4_basis: T4Basis
    payloads: tuple[Payload, ...]
    sources: tuple[Source, ...]
    evidence: tuple[Evidence, ...]
    documents: tuple[PilotDocument, ...]
    inventory: tuple[InventoryItem, ...]
    statements: tuple[Statement, ...]
    relations: tuple[PilotRelation, ...]
    entries: tuple[PeriodEntry, ...]
    case_candidates: tuple[CaseCandidate, ...]
    decision_candidates: tuple[DecisionCandidate, ...]
    gaps: tuple[CoverageGap, ...]
    issues: tuple[str, ...]
    year_coverage: str = "partial"
    professional_annual_balance_approval: bool = False
    version: str = "periodegrunnlag-1"


@dataclass(frozen=True)
class View:
    monetary: PilotView
    entry_ids: tuple[str, ...]
    document_ids: tuple[str, ...]
    case_candidate_ids: tuple[str, ...]
    decision_candidate_ids: tuple[str, ...]
    gap_ids: tuple[str, ...]


@dataclass(frozen=True)
class Report:
    id: str
    basis: Basis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: View
    calculations: tuple[Calculation, ...]
    version: str = FORMAT
