"""P2s lukkede immutable tillegg; P1 er én uendret typet basis."""

from dataclasses import dataclass

from .forlopspilot_model import Calculation
from .komitepilot_model import Payload, Source
from .perioderegister_model import Basis as P1Basis
from .perioderegister_model import View as P1View
from .visningspilot_model import (
    InventoryItem,
    PilotDocument,
    PilotRelation,
    PilotSelection,
    Statement,
)

FORMAT = "perioderegister-r2-1"
RULE = "periode1429-r2-54-1"


@dataclass(frozen=True)
class Evidence:
    id: str
    key: str
    source_id: str
    locator: str
    nested_html_field_xpath: str | None
    representation_sha256: str
    kind: str
    role: str | None
    text: str
    rows_json: str | None


@dataclass(frozen=True)
class Finding:
    id: str
    key: str
    document_id: str
    case_id: str | None
    decision_api_id: str | None
    budget_year: int | None
    accounts: tuple[str, ...]
    conditional_accounts: tuple[str, ...]
    transfer_target_year: int | None
    post_link: str
    role: str
    actor: str
    status: str
    reason: str
    evidence_ids: tuple[str, ...]
    amounts_json: str
    proposal_ids: tuple[str, ...]
    voting_id: str | None


@dataclass(frozen=True)
class StatusUpdate:
    id: str
    case_candidate_id: str
    case_id: str
    index_session: str
    ordinal_1based: int
    status: str
    reason: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class CrossReference:
    id: str
    key: str
    from_text: str
    target: str
    status: str
    result: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class Basis:
    id: str
    rule: str
    p1_basis: P1Basis
    payloads: tuple[Payload, ...]
    sources: tuple[Source, ...]
    evidence: tuple[Evidence, ...]
    documents: tuple[PilotDocument, ...]
    inventory: tuple[InventoryItem, ...]
    statements: tuple[Statement, ...]
    relations: tuple[PilotRelation, ...]
    findings: tuple[Finding, ...]
    status_updates: tuple[StatusUpdate, ...]
    cross_references: tuple[CrossReference, ...]
    issues: tuple[str, ...]
    year_coverage: str = "partial"
    professional_annual_balance_approval: bool = False
    version: str = "periodegrunnlag-r2-1"


@dataclass(frozen=True)
class View:
    p1: P1View
    finding_ids: tuple[str, ...]
    document_ids: tuple[str, ...]
    status_update_ids: tuple[str, ...]
    cross_reference_ids: tuple[str, ...]


@dataclass(frozen=True)
class Report:
    id: str
    basis: Basis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: View
    calculations: tuple[Calculation, ...]
    version: str = FORMAT
