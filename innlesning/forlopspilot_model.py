"""T3s separate immutable opt-in-filkontrakt; ingen endring i eldre formater."""

from dataclasses import dataclass

from .komitepilot_model import Payload, Source
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

FORMAT = "visningspilot-3"
RULE = "forlop1429-2024-1"


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
    version: str = "forlopsgrunnlag-1"


@dataclass(frozen=True)
class Calculation:
    id: str
    account: str
    budget_year: int
    rule: str
    status: str
    reason: str
    input_ids: tuple[str, ...]
    check_ids: tuple[str, ...]
    amount_kr: int | None
    observed_kr: int | None


@dataclass(frozen=True)
class Report:
    id: str
    basis: Basis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: PilotView
    calculations: tuple[Calculation, ...]
    version: str = FORMAT
