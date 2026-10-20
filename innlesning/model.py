"""Datakontrakt v1: ett valgt endelig vedtak, bevart som én importkjøring."""

from dataclasses import dataclass, field


@dataclass
class Decision:
    id: str
    number: str
    session: str
    date: str
    date_raw: str
    case_id: str
    api_type: str
    title: str
    url: str
    url_raw: str
    html: str
    budget_year: int | None = None


@dataclass
class Allocation:
    locator: str
    chapter: str
    chapter_name: str
    post: str
    purpose: str
    amount_text: str
    amount_kr: int | None
    direction: str
    raw_html: str
    meaning: str = "opprinnelig bevilgning"
    status: str = "strukturert"
    control_reason: str = ""


@dataclass
class Report:
    run_id: str
    source_sha256: str
    source_metadata: dict[str, object]
    historical_sample: bool
    decision: Decision | None = None
    lines: list[Allocation] = field(default_factory=list)
    source_totals: dict[str, int | None] = field(default_factory=dict)
    controls: list[str] = field(default_factory=list)
    status: str = "strukturert"
    contract_version: str = "1"

    @property
    def approved_totals(self) -> dict[str, int | None]:
        """Ingen godkjent sum når målvedtakets strukturering er ufullstendig."""
        if self.status != "strukturert":
            return {"utgift": None, "inntekt": None}
        return {
            direction: sum(
                line.amount_kr
                for line in self.lines
                if line.direction == direction and line.amount_kr is not None
            )
            for direction in ("utgift", "inntekt")
        }
