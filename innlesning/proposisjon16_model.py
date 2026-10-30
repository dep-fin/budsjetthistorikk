"""T5s lukkede immutable tillegg til én uendret T1-basis."""

from dataclasses import dataclass

from .observations import AmountObservation
from .visningspilot_model import (
    PilotBasis,
    PilotSelection,
    PilotSource,
    PilotView,
    TreatmentContext,
)

FORMAT = "proposisjon16-1"
RULE = "prop16-tabell-1"


@dataclass(frozen=True)
class FieldBinding:
    id: str
    inventory_id: str
    observation_ids: tuple[str, ...]


@dataclass(frozen=True)
class DocumentCoverage:
    id: str
    document_id: str
    table_groups: int
    table_fields: int
    account_count: int
    status: str
    scope: str
    historical_issue: str


@dataclass(frozen=True)
class Authorization:
    id: str
    document_id: str
    source_id: str
    locator: str
    roman: str
    point: str
    role: str
    period: str
    accounts: tuple[str, ...]
    frame_kr: int | None
    text: str
    html: str
    status: str


@dataclass(frozen=True)
class Branch:
    id: str
    from_document_id: str
    to_document_id: str
    case_id: str
    accounts: tuple[str, ...]
    point: str
    committee_point: str
    decision_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    status: str
    amount_stage: str


@dataclass(frozen=True)
class Basis:
    id: str
    rule: str
    t1_basis: PilotBasis
    sources: tuple[PilotSource, ...]
    observations: tuple[AmountObservation, ...]
    contexts: tuple[TreatmentContext, ...]
    bindings: tuple[FieldBinding, ...]
    coverage: tuple[DocumentCoverage, ...]
    authorizations: tuple[Authorization, ...]
    branches: tuple[Branch, ...]
    issues: tuple[str, ...]
    version: str = "proposisjonsgrunnlag16-1"


@dataclass(frozen=True)
class Report:
    id: str
    basis: Basis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: PilotView
    version: str = FORMAT
