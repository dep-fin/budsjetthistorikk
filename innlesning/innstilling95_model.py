"""T6s lukkede immutable tillegg til én uendret T5-kapsel."""

from dataclasses import dataclass

from .observations import AmountObservation
from .proposisjon16_model import Authorization, FieldBinding
from .proposisjon16_model import Basis as T5Basis
from .visningspilot_model import (
    InventoryItem,
    PilotDocument,
    PilotRelation,
    PilotSelection,
    PilotSource,
    PilotView,
    Statement,
    TreatmentContext,
)

FORMAT = "innstilling95-1"
RULE = "innst95-tabell-1"


@dataclass(frozen=True)
class SourceRecipe:
    id: str
    document_key: str
    parent_source_id: str
    sidecar_source_id: str
    object_start: int
    object_end: int
    prefix_bytes: int
    suffix_start: int
    separator_base64: str
    expected_sha256: str
    expected_bytes: int
    status: str


@dataclass(frozen=True)
class CoverageOverlay:
    id: str
    document_id: str
    table_groups: int
    table_fields: int
    accounts: tuple[str, ...]
    status: str
    scope: str
    historical_issue: str


@dataclass(frozen=True)
class Basis:
    id: str
    rule: str
    t5_basis: T5Basis
    sources: tuple[PilotSource, ...]
    recipes: tuple[SourceRecipe, ...]
    documents: tuple[PilotDocument, ...]
    inventory: tuple[InventoryItem, ...]
    statements: tuple[Statement, ...]
    observations: tuple[AmountObservation, ...]
    contexts: tuple[TreatmentContext, ...]
    relations: tuple[PilotRelation, ...]
    bindings: tuple[FieldBinding, ...]
    coverage: tuple[CoverageOverlay, ...]
    authorizations: tuple[Authorization, ...]
    issues: tuple[str, ...]
    version: str = "innstillingsgrunnlag95-1"


@dataclass(frozen=True)
class Report:
    id: str
    basis: Basis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: PilotView
    version: str = FORMAT
