"""Avstemming med navngitt periode, beløpsbegrep, enhet og kildebevis."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .session import SessionReport, SessionRow


def _sha(value: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise ValueError("Kildereferansen krever SHA-256")


def _amount(value: int | None) -> None:
    if value is not None and (type(value) is not int or abs(value) > 9_007_199_254_740_991):
        raise ValueError("Forventet verdi må være et Excel-eksakt heltall i kroner")


def _text(*values: str) -> None:
    if any(not isinstance(v, str) or not v.strip() for v in values):
        raise ValueError("Kontrollen krever ikke-tom kildehenvisning, lokator og begrunnelse")


@dataclass(frozen=True)
class AmountScope:
    budget_year: int
    period_start: str
    period_end: str
    concept: str
    detail_level: str = "post"
    currency: str = "NOK"
    multiplier: str = "1"

    def __post_init__(self) -> None:
        if type(self.budget_year) is not int or not 1000 <= self.budget_year <= 9999:
            raise ValueError("Avstemming krever firesifret budsjettår")
        start, end = date.fromisoformat(self.period_start), date.fromisoformat(self.period_end)
        if (
            start.isoformat() != self.period_start
            or end.isoformat() != self.period_end
            or start > end
        ):
            raise ValueError("Avstemmingsperioden krever ordnede ISO-datoer")
        if self.concept not in {
            "saldert",
            "arets_bevilgning",
            "avgrenset_endring",
            "rekneskap",
            "samla_loyving",
        }:
            raise ValueError("Ukjent beløpsbegrep i avstemming")
        if (
            self.detail_level not in {"post", "underpost"}
            or self.currency not in {"NOK", "EUR", "USD"}
            or self.multiplier not in {"1", "1000", "1000000"}
        ):
            raise ValueError("Avstemming krever uttrykkelig nivå, valuta og multiplikator")


@dataclass(frozen=True)
class ReferenceValue:
    chapter: str
    post: str
    expected_amount_kr: int | None
    absent: bool
    reference: str
    sha256: str
    locator: str
    reason: str
    subpost: str | None = None

    def __post_init__(self) -> None:
        for code in (self.chapter, self.post, self.subpost):
            if code is not None and (
                not isinstance(code, str)
                or not code.isascii()
                or not code.isdigit()
                or str(int(code)) != code
            ):
                raise ValueError("Avstemming krever normalisert konto")
        if not self.chapter or not self.post or type(self.absent) is not bool:
            raise ValueError("Avstemming krever konto og uttrykkelig fraværsflagg")
        _amount(self.expected_amount_kr)
        if self.absent != (self.expected_amount_kr is None):
            raise ValueError("Oppgi forventet verdi ELLER uttrykkelig fravær; null er ikke 0")
        _sha(self.sha256)
        _text(self.reference, self.locator, self.reason)


@dataclass(frozen=True)
class Reconciliation:
    name: str
    actual_scope: AmountScope
    reference_scope: AmountScope
    observation_ids: tuple[str, ...]
    references: tuple[ReferenceValue, ...]
    controlled_chain_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.name)
        for values in (self.observation_ids, self.controlled_chain_ids):
            if (
                not isinstance(values, tuple)
                or len(set(values)) != len(values)
                or any(not isinstance(v, str) or not v for v in values)
            ):
                raise ValueError("Avstemming krever ulike eksplisitte ID-er")
        keys = [(r.chapter, r.post, r.subpost) for r in self.references]
        if len(set(keys)) != len(keys):
            raise ValueError("Kontrollgrunnlaget kan bare ha én forventning per konto")
        if not self.observation_ids and not self.controlled_chain_ids and not self.references:
            raise ValueError("Tom avstemming er ikke utført kontroll")
        if any(
            (r.subpost is None) != (self.reference_scope.detail_level == "post")
            for r in self.references
        ):
            raise ValueError("Referansens konto må svare til valgt detaljnivå")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Reconciliation:
        values = dict(data)
        if not {"actual_scope", "reference_scope", "name"} <= values.keys():
            raise ValueError("Avstemming krever navn og begge omfangsbeskrivelser")
        values["actual_scope"] = AmountScope(**values["actual_scope"])
        values["reference_scope"] = AmountScope(**values["reference_scope"])
        for key in ("observation_ids", "references", "controlled_chain_ids"):
            if key in values and not isinstance(values[key], list):
                raise ValueError(f"{key} krever JSON-liste")
        values["observation_ids"] = tuple(values.get("observation_ids", ()))
        values["controlled_chain_ids"] = tuple(values.get("controlled_chain_ids", ()))
        values["references"] = tuple(ReferenceValue(**r) for r in values.get("references", ()))
        return cls(**values)


@dataclass(frozen=True)
class ReconciliationRow:
    chapter: str | None
    post: str | None
    subpost: str | None
    actual_amount_kr: int | None
    expected_amount_kr: int | None
    reference_absent: bool | None
    status: str
    difference_kr: int | None
    observation_ids: tuple[str, ...]
    reference: ReferenceValue | None
    reason: str


@dataclass(frozen=True)
class ReconciliationResult:
    specification: Reconciliation
    rows: tuple[ReconciliationRow, ...]
    status: str
    boundary: str = "Kontroll av eksplisitt valgt omfang; ingen automatisk kjede- eller årsdekning"


def reconcile(report: SessionReport, check: Reconciliation) -> ReconciliationResult:
    by_id = {r.observation.id: r for r in report.rows}
    if not set(check.observation_ids) <= set(by_id):
        raise ValueError("Avstemming viser til observasjoner utenfor eksportens utvalg")
    actual: dict[tuple[str | None, str | None, str | None], list[SessionRow]] = defaultdict(list)
    for identifier in check.observation_ids:
        row = by_id[identifier]
        o = row.observation
        actual[(o.chapter, o.post, o.subpost)].append(row)
    references: dict[tuple[str | None, str | None, str | None], ReferenceValue] = {
        (r.chapter, r.post, r.subpost): r for r in check.references
    }
    chains: dict[tuple[str | None, str | None, str | None], tuple[int | None, str]] = {}
    controlled = {r.id: r for r in report.controlled_results}
    histories = {h.id: h for h in report.histories}
    for identifier in check.controlled_chain_ids:
        if identifier not in controlled:
            raise ValueError("Avstemming krever eksplisitt valgt kontrollert kjederesultat")
        result = controlled[identifier]
        if result.technical_calculation_id not in histories:
            raise ValueError("Velg kjedens lagrede historikkberegning uttrykkelig")
        history = histories[result.technical_calculation_id]
        if not set(history.input_observation_ids) <= set(by_id):
            raise ValueError("Kjedeavstemming viser til observasjoner utenfor eksportens utvalg")
        scope = check.actual_scope
        chain_key = history.selection.chapter, history.selection.post, history.selection.subpost
        if chain_key in chains or chain_key in actual:
            raise ValueError("Samme konto kan ikke ha flere alternative faktiske verdier")
        compatible = (
            history.selection.budget_year == scope.budget_year
            and history.selection.detail_level == scope.detail_level
            and scope.concept == "arets_bevilgning"
            and scope.period_start == f"{scope.budget_year}-01-01"
            and scope.period_end == f"{scope.budget_year}-12-31"
            and all(
                step.decision_date is not None and step.decision_date <= scope.period_end
                for step in history.steps
            )
        )
        chains[chain_key] = (
            result.approved_chain_balance
            if compatible and history.freshness == "samme kildegrunnlag"
            else None,
            "" if compatible else "uforenlig_omfang",
        )
    scope = check.actual_scope
    scope_ok = (
        scope == check.reference_scope
        and scope.currency == "NOK"
        and scope.multiplier == "1"
        and scope.concept in {"saldert", "arets_bevilgning", "avgrenset_endring"}
    )
    result_rows: list[ReconciliationRow] = []
    for key in sorted(set(actual) | set(references) | set(chains), key=str):
        ref = references.get(key)
        rows = actual.get(key, [])
        compatible = scope_ok
        reasons: list[str] = []
        for row in rows:
            o = row.observation
            for observed, expected_field in (
                (o.budget_year, scope.budget_year),
                (o.detail_level, scope.detail_level),
                (o.currency, scope.currency),
                (o.figure_type, "stortingsvedtak"),
                (o.information_type, "bevilgning"),
                (o.scope, "enkeltledd"),
            ):
                if observed in (None, "uavklart"):
                    reasons.append("Uavklart år, nivå, enhet eller faglig klassifikasjon")
                elif observed != expected_field:
                    compatible = False
            if scope.concept == "saldert":
                if o.meaning == "uavklart" or o.round == "uavklart":
                    reasons.append("Uavklart beløpsbetydning eller behandlingsrunde")
                else:
                    compatible = compatible and o.meaning == "nivaa" and o.round == "opprinnelig"
            elif scope.concept == "avgrenset_endring":
                if o.meaning == "uavklart":
                    reasons.append("Uavklart beløpsbetydning")
                else:
                    compatible = compatible and o.meaning == "endring"
            else:
                compatible = False  # Årets bevilgning krever en godkjent valgt kjede.
            if o.decision_date is None:
                reasons.append("Uavklart vedtaksdato")
            elif not scope.period_start <= o.decision_date <= scope.period_end:
                compatible = False
            if (
                row.approved_amount_kr is None
                or row.selection_status != "treff"
                or o.chapter is None
                or o.post is None
            ):
                reasons.append("Beløpet/kontoen er ikke gjeldende faglig godkjent")
        if scope.concept == "saldert" and len(rows) > 1:
            reasons.append("Flere alternative nivåobservasjoner")
        actual_amount: int | None = None
        if key in chains:
            actual_amount, chain_issue = chains[key]
            compatible = compatible and not chain_issue
            if actual_amount is None:
                reasons.append("Kjedesaldoen er ikke gjeldende faglig godkjent")
        elif rows and compatible and not reasons:
            actual_amount = sum(
                r.approved_amount_kr for r in rows if r.approved_amount_kr is not None
            )
        expected = ref.expected_amount_kr if ref else None
        if not compatible:
            status = "uforenlig_omfang"
            actual_amount = None
        elif key[0] is None or key[1] is None:
            status = "ikke_vurderbar"
        elif not ref:
            status = "mangler_i_kontrollgrunnlag"
        elif not rows and key not in chains:
            status = "ikke_vurderbar" if ref.absent else "mangler_i_uttrekk"
            reasons.append("Fravær i valgt uttrekk er ikke bevis for fravær i hele perioden")
        elif reasons or actual_amount is None:
            status = "ikke_vurderbar"
        elif ref.absent:
            status = "mangler_i_kontrollgrunnlag"
        else:
            status = "samsvar" if actual_amount == expected else "belopsavvik"
        result_rows.append(
            ReconciliationRow(
                *key,
                actual_amount,
                expected,
                ref.absent if ref else None,
                status,
                actual_amount - expected
                if actual_amount is not None and expected is not None
                else None,
                tuple(r.observation.id for r in rows),
                ref,
                "; ".join(reasons)
                or (
                    "Like perioder, beløpsbegrep, nivå og enhet"
                    if compatible
                    else "Ulike/uforenlige perioder, år, beløpsbegrep, nivå eller enhet"
                ),
            )
        )
    return ReconciliationResult(
        check,
        tuple(result_rows),
        "samsvar" if result_rows and all(r.status == "samsvar" for r in result_rows) else "avvik",
    )


@dataclass(frozen=True)
class SourceExpectation:
    observation_id: str
    expected_raw_amount_kr: int | None
    expected_effective_amount_kr: int | None
    sha256: str
    locator: str
    amount_field: str
    reference: str
    reason: str

    def __post_init__(self) -> None:
        _text(self.observation_id, self.locator, self.amount_field, self.reference, self.reason)
        _sha(self.sha256)
        _amount(self.expected_raw_amount_kr)
        _amount(self.expected_effective_amount_kr)


@dataclass(frozen=True)
class SourceCheck:
    expectation: SourceExpectation
    actual_raw_amount_kr: int | None
    actual_effective_amount_kr: int | None
    status: str


def check_source(report: SessionReport, expectation: SourceExpectation) -> SourceCheck:
    rows = {r.observation.id: r for r in report.rows}
    if expectation.observation_id not in rows:
        return SourceCheck(expectation, None, None, "mangler_i_uttrekk")
    row = rows[expectation.observation_id]
    o = row.observation
    status = "samsvar"
    if (o.pointer.artifact_id, o.pointer.locator, o.pointer.amount_field) != (
        expectation.sha256,
        expectation.locator,
        expectation.amount_field,
    ):
        status = "uforenlig_kildegrunnlag"
    elif o.amount_kr != expectation.expected_raw_amount_kr:
        status = "belopsavvik"
    elif expectation.expected_effective_amount_kr is not None and row.approved_amount_kr is None:
        status = "ikke_vurderbar"
    elif row.approved_amount_kr != expectation.expected_effective_amount_kr:
        status = "belopsavvik"
    return SourceCheck(expectation, o.amount_kr, row.approved_amount_kr, status)
