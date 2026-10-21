"""GitHub ved HTTPS-grensen, med begrenset transport og varig tvetydighetsvern."""

import json
import shutil
from pathlib import Path

import pytest
from test_b7 import FakeGitHub

from drift import Config
from drift.notifications import GitHubClient, deliver, marker
from drift.store import enqueue, pending_notifications, start_day
from innlesning.organization_register import REGISTER_SNAPSHOT


class Response:
    def __init__(self, value: object, *, oversized: bool = False):
        self.raw = json.dumps(value).encode()
        self.oversized = oversized

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self, size: int) -> bytes:
        assert size == 8 * 1024 * 1024 + 1
        return b"x" * size if self.oversized else self.raw


def test_https_client_paginates_all_states_excludes_prs_and_preserves_closed_binding(monkeypatch):
    requests = []
    key = marker("persistent")

    class Transport:
        def open(self, request, *, timeout):
            requests.append(request)
            assert timeout == 17
            assert request.full_url.startswith(
                "https://api.github.com/repos/depmartin/budsjetthistorikk/issues"
            )
            if request.full_url.endswith("&page=1"):
                assert "state=all&per_page=100" in request.full_url
                return Response(
                    [{"number": 1, "body": key, "pull_request": {}}]
                    + [{"number": i, "body": "human"} for i in range(2, 101)]
                )
            if request.full_url.endswith("&page=2"):
                return Response([{"number": 987, "body": key, "state": "closed"}])
            if request.method == "PATCH":
                body = json.loads(request.data)
                assert set(body) == {"body"} and "state" not in body
                return Response({"number": 987, "body": body["body"]})
            return Response({"number": 987, "body": "Menneskets tekst"})

    monkeypatch.setenv("TEST_GITHUB_TOKEN", "synthetic-token")
    monkeypatch.setattr("drift.notifications.build_opener", lambda *args: Transport())
    github = GitHubClient("TEST_GITHUB_TOKEN", timeout=17)
    assert github.find("depmartin/budsjetthistorikk", key) == 987
    assert github.read_body("depmartin/budsjetthistorikk", 987) == "Menneskets tekst"
    github.update_body("depmartin/budsjetthistorikk", 987, "Menneskets tekst\nstatus")
    assert all(r.get_header("Authorization") == "Bearer synthetic-token" for r in requests)
    with pytest.raises(ValueError, match="autorisert"):
        github.find("other/repository", key)


def test_https_client_refuses_oversized_or_duplicate_marker_results(monkeypatch):
    class Transport:
        oversized = False

        def open(self, request, *, timeout):
            return Response(
                [{"number": 1, "body": "marker"}, {"number": 2, "body": "marker"}],
                oversized=self.oversized,
            )

    transport = Transport()
    monkeypatch.setenv("TEST_GITHUB_TOKEN", "synthetic-token")
    monkeypatch.setattr("drift.notifications.build_opener", lambda *args: transport)
    github = GitHubClient("TEST_GITHUB_TOKEN")
    with pytest.raises(ValueError, match="Flere"):
        github.find("depmartin/budsjetthistorikk", "marker")
    transport.oversized = True
    with pytest.raises(RuntimeError, match="github_httpfeil"):
        github.find("depmartin/budsjetthistorikk", "marker")


def test_backup_restore_reconciles_uncertain_post_without_duplicate(tmp_path: Path):
    config = Config("restore", tmp_path / "before.sqlite", tmp_path / "reports", REGISTER_SNAPSHOT)
    job, _, _, _ = start_day(config, "2026-10-21")
    enqueue(config.database, job, config.repository, "persistent", "Avvik", "Status")
    github = FakeGitHub()
    github.lose_post_ack = True
    assert deliver(config.database, github) == "venter"
    restored = tmp_path / "restored.sqlite"
    shutil.copyfile(config.database, restored)
    github.lose_post_ack = False
    assert deliver(restored, github) == "levert"
    assert github.creates == 1 and not pending_notifications(restored)


def test_missing_background_access_is_explicit_and_does_not_create_credentials(monkeypatch):
    monkeypatch.delenv("NO_SUCH_EXISTING_ACCESS", raising=False)
    with pytest.raises(ValueError, match="bakgrunnstilgang"):
        GitHubClient("NO_SUCH_EXISTING_ACCESS")


def test_pending_daily_statuses_are_coalesced_without_losing_uncertain_post(tmp_path: Path):
    config = Config("backlog", tmp_path / "backlog.sqlite", tmp_path / "reports", REGISTER_SNAPSHOT)
    first, _, _, _ = start_day(config, "2026-10-21")
    enqueue(config.database, first, config.repository, "same", "Avvik", "gammel status")
    second, _, _, _ = start_day(config, "2026-10-22")
    enqueue(config.database, second, config.repository, "same", "Avvik", "dagens status")
    assert len(pending_notifications(config.database)) == 1
    github = FakeGitHub()
    assert deliver(config.database, github) == "levert"
    assert "dagens status" in github.issues[1]["body"]
    assert github.creates == 1
