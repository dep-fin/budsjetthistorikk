"""T4s egne immutable filtyper; eldre kontrakter beholdes."""

from dataclasses import dataclass

from .forlopspilot_model import Basis as PathBasis
from .forlopspilot_model import Calculation
from .visningspilot_model import PilotSelection, PilotView

FORMAT = "visningspilot-4"
RULE = "fleraar1429-2024-2025-1"


@dataclass(frozen=True)
class Basis(PathBasis):
    version: str = "fleraarsgrunnlag-1"


@dataclass(frozen=True)
class Report:
    id: str
    basis: Basis
    selection: PilotSelection
    return_selection: PilotSelection | None
    view: PilotView
    calculations: tuple[Calculation, ...]
    version: str = FORMAT
