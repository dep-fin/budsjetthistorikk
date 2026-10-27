"""Immutable modeller bare for den eksplisitte T1-filkontrakten."""

from dataclasses import dataclass

from .observations import AmountObservation, Extraction
from .omtale import OmtaleBasis

RULE = "innst81-visning-1"
BASIS_VERSION = "visningsgrunnlag-1"
FORMAT = "visningspilot-1"


@dataclass(frozen=True)
class PilotInput:
    """Validert analysekonvolutt og typet kildegrunnlag til den separate adapteren."""

    o2b_json: str
    basis: OmtaleBasis
    issues: tuple[str, ...]
    extraction: Extraction
    adopted: tuple[AmountObservation, ...]


@dataclass(frozen=True)
class PilotSource:
    id: str
    name: str
    document_key: str
    media_type: str
    expected_sha256: str
    content_base64: str | None
    sha256: str | None
    byte_count: int | None
    status: str
    metadata_json: str


@dataclass(frozen=True)
class PilotDocument:
    id: str
    key: str
    title: str
    kind: str
    session: str
    date: str
    raw_coverage: str
    structured_coverage: str
    professional_status: str
    source_ids: tuple[str, ...]
    accounts: tuple[str, ...]


@dataclass(frozen=True)
class InventoryItem:
    id: str
    document_id: str
    source_id: str
    locator: str
    chapter: str
    post: str
    role: str
    structure_status: str
    text: str
    budget_year: int
    observation_ids: tuple[str, ...]


@dataclass(frozen=True)
class Statement:
    id: str
    document_id: str
    source_id: str
    locator: str
    text: str
    html: str
    role: str
    actor: str
    period: str
    status: str
    accounts: tuple[str, ...]
    hierarchy: tuple[str, ...]


@dataclass(frozen=True)
class PilotRelation:
    id: str
    from_id: str
    to_id: str
    role: str
    scope: str
    status: str
    accounts: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    budget_year: int


@dataclass(frozen=True)
class TreatmentContext:
    id: str
    observation_id: str
    document_id: str
    round: str
    stage: str
    actor: str
    status: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class PilotBasis:
    id: str
    rule: str
    o2b_json: str
    sources: tuple[PilotSource, ...]
    documents: tuple[PilotDocument, ...]
    inventory: tuple[InventoryItem, ...]
    statements: tuple[Statement, ...]
    observations: tuple[AmountObservation, ...]
    relations: tuple[PilotRelation, ...]
    contexts: tuple[TreatmentContext, ...]
    issues: tuple[str, ...]
    version: str = BASIS_VERSION


@dataclass(frozen=True)
class PilotSelection:
    mode: str = "accounts"
    document_id: str | None = None
    years: tuple[int, ...] = ()
    chapters: tuple[str, ...] = ()
    accounts: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class StageComparison:
    id: str
    meaning: str
    account: str
    status: str
    reason: str
    rule: str
    left_id: str | None
    right_id: str | None
    null_reason: str | None
    difference_kr: int | None


@dataclass(frozen=True)
class PilotView:
    document_ids: tuple[str, ...]
    inventory_ids: tuple[str, ...]
    statement_ids: tuple[str, ...]
    observation_ids: tuple[str, ...]
    adopted_observation_ids: tuple[str, ...]
    adopted_event_ids: tuple[str, ...]
    comparisons: tuple[StageComparison, ...]


@dataclass(frozen=True)
class PilotReport:
    id: str
    basis: PilotBasis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: PilotView
    version: str = FORMAT
