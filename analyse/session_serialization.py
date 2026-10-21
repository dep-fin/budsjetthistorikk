"""Versjonert JSON for en frosset B6-vurdering; aldri pickle eller dynamiske klasser."""

import json
import types
from dataclasses import asdict, fields, is_dataclass
from typing import Any, cast, get_args, get_origin, get_type_hints

from innlesning.observations import encode

from .session import SessionReport

MAX_REPORT_BYTES = 128 * 1024 * 1024


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value in pairs:
        if name in result:
            raise ValueError("Duplisert JSON-felt i frosset rapport")
        result[name] = value
    return result


def _constant(value: str) -> None:
    raise ValueError("Ugyldig JSON-tall i frosset rapport")


def _decode(kind: Any, value: Any) -> Any:
    if kind in (Any, object):
        return value
    origin, args = get_origin(kind), get_args(kind)
    if origin is types.UnionType:
        for alternative in args:
            try:
                return _decode(alternative, value)
            except (ValueError, TypeError):
                pass
        raise ValueError("Rapportfelt passer ingen tillatt type")
    if kind is type(None):
        if value is not None:
            raise ValueError("Forventet null")
        return None
    if origin in (tuple, list):
        if not isinstance(value, list):
            raise ValueError("Rapportfelt krever liste")
        if origin is tuple and len(args) > 1 and args[-1] is not Ellipsis:
            if len(args) != len(value):
                raise ValueError("Feil lengde i rapportfelt")
            return tuple(_decode(t, v) for t, v in zip(args, value, strict=True))
        result = [_decode(args[0], v) for v in value]
        return tuple(result) if origin is tuple else result
    if origin is dict:
        if not isinstance(value, dict):
            raise ValueError("Rapportfelt krever objekt")
        return {_decode(args[0], k): _decode(args[1], v) for k, v in value.items()}
    if is_dataclass(kind):
        if not isinstance(value, dict) or set(value) != {f.name for f in fields(kind)}:
            raise ValueError("Ukjente eller manglende rapportfelt")
        hints = get_type_hints(kind)
        return cast(Any, kind)(**{k: _decode(hints[k], v) for k, v in value.items()})
    if kind in (str, int, bool, float) and type(value) is kind:
        return value
    raise ValueError("Feil type i rapportfelt")


def report_to_json(report: SessionReport) -> str:
    raw = encode({"format": "b6-frozen-1", "report": asdict(report)})
    if len(raw.encode("utf-8")) > MAX_REPORT_BYTES:
        raise ValueError("Frosset rapport overstiger 128 MiB")
    return raw


def report_from_json(raw: str) -> SessionReport:
    if len(raw.encode("utf-8")) > MAX_REPORT_BYTES:
        raise ValueError("Frosset rapport overstiger 128 MiB")
    data = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
    if not isinstance(data, dict) or set(data) != {"format", "report"}:
        raise ValueError("Ukjent rapportkonvolutt")
    if data["format"] != "b6-frozen-1":
        raise ValueError("Ukjent rapportversjon")
    report: SessionReport = _decode(SessionReport, data["report"])
    if report.coverage.professional_complete or any(
        c.professional_complete for c in report.supplemental_coverage
    ):
        raise ValueError("B6 kan ikke erklære uttømmende faglig dekning")
    return report
