import hashlib
from io import BytesIO
from pathlib import Path
from urllib.request import OpenerDirector, Request

import pytest


def test_http_adapter_only_fetches_fixed_session_url_with_bounded_timeout(monkeypatch) -> None:
    from innlesning import fetch_session

    raw = (Path(__file__).parent / "fixtures/40033944.derived.xml").read_bytes()

    class Response(BytesIO):
        status = 200
        headers = {"Content-Type": "text/xml; charset=utf-8"}

    def fake_open(self, request: Request, data=None, timeout=0):
        assert request.full_url == (
            "https://data.stortinget.no/eksport/stortingsvedtak?sesjonid=2024-2025"
        )
        assert timeout == 25
        assert request.get_header("Accept") == "text/xml"
        return Response(raw)

    monkeypatch.setattr(OpenerDirector, "open", fake_open)
    response, metadata = fetch_session("2024-2025", timeout=25)
    assert response == raw
    assert metadata["sha256"] == hashlib.sha256(raw).hexdigest()
    assert metadata["bytes"] == 15214
    assert metadata["fixture_kind"] == "http_original"
    assert metadata["status"] == 200
    with pytest.raises(ValueError, match="Sesjon"):
        fetch_session("https://127.0.0.1/private")


@pytest.mark.parametrize("timeout", [0, 121])
def test_http_timeout_is_bounded(timeout: int) -> None:
    from innlesning import fetch_session

    with pytest.raises(ValueError, match="Timeout"):
        fetch_session("2024-2025", timeout=timeout)


def test_http_response_size_is_bounded(monkeypatch) -> None:
    from innlesning import fetch_session

    class LargeResponse(BytesIO):
        status = 200
        headers = {}

        def read(self, size=-1):
            assert size == 33_554_433
            return b"X" * size

    monkeypatch.setattr(OpenerDirector, "open", lambda *args, **kwargs: LargeResponse())
    with pytest.raises(ValueError, match="32 MiB"):
        fetch_session("2024-2025")
