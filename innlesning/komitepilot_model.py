"""T2s immutable filkontrakt. Gamle visningspilotmodeller beholder sin betydning."""

from dataclasses import dataclass

from .observations import AmountObservation
from .visningspilot_model import (
    InventoryItem,
    PilotDocument,
    PilotRelation,
    PilotSelection,
    PilotView,
    Statement,
    TreatmentContext,
)

FORMAT = "visningspilot-2"
RULE = "komite315-visning-1"


@dataclass(frozen=True)
class Payload:
    id: str
    sha256: str
    byte_count: int
    content_base64: str | None
    legacy_source_id: str | None


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    document_key: str
    media_type: str
    expected_sha256: str
    payload_id: str | None
    status: str
    metadata_json: str


@dataclass(frozen=True)
class Basis:
    id: str
    rule: str
    payloads: tuple[Payload, ...]
    sources: tuple[Source, ...]
    documents: tuple[PilotDocument, ...]
    inventory: tuple[InventoryItem, ...]
    statements: tuple[Statement, ...]
    observations: tuple[AmountObservation, ...]
    contexts: tuple[TreatmentContext, ...]
    relations: tuple[PilotRelation, ...]
    issues: tuple[str, ...]
    legacy_json: str = ""
    version: str = "komitegrunnlag-1"


@dataclass(frozen=True)
class Report:
    id: str
    basis: Basis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: PilotView
    version: str = FORMAT
