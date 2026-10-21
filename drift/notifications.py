"""Varig GitHub-outbox. Usikker POST må avstemmes før noen ny opprettelse."""

import json
import os
from pathlib import Path
from typing import Any, Protocol
from urllib.request import Request, build_opener

from innlesning.http import NoRedirect

from .config import AUTHORIZED_REPOSITORY
from .store import (
    issue_binding,
    notification_status,
    pending_notifications,
    uncertain_notifications,
)


class GitHubPort(Protocol):
    def find(self, repository: str, marker: str) -> int | None: ...
    def read_body(self, repository: str, number: int) -> str: ...
    def create(self, repository: str, title: str, body: str) -> int: ...
    def update_body(self, repository: str, number: int, body: str) -> None: ...


def marker(key: str) -> str:
    return f"<!-- budsjetthistorikk:{key} -->"


def _section(key: str, text: str) -> str:
    return f"{marker(key)}\n{text}\n<!-- /budsjetthistorikk:{key} -->"


def _replace(old: str, key: str, text: str) -> str:
    start, end = marker(key), f"<!-- /budsjetthistorikk:{key} -->"
    if old.count(start) > 1 or old.count(end) > 1:
        raise ValueError("Tvetydig statusfelt i GitHub-issue")
    if start in old and end in old:
        a, b = old.index(start), old.index(end) + len(end)
        if b <= a:
            raise ValueError("Uordnet statusfelt i GitHub-issue")
        return old[:a] + _section(key, text) + old[b:]
    if start in old or end in old:
        raise ValueError("Ufullstendig statusfelt i GitHub-issue")
    return old + "\n\n" + _section(key, text)


def deliver(database: Path, github: GitHubPort) -> str:
    """Kall under driftslåsen. Ingest-resultatet endres ikke ved leveringsfeil."""
    uncertain = uncertain_notifications(database)
    for item in pending_notifications(database, limit=100):
        identifier, repo, key = item["id"], item["repository"], item["key"]
        ambiguous = item["status"] == "uavklart_post"
        try:
            number = issue_binding(database, repo, key)
            if number is None:
                number = github.find(repo, marker(key))
            if number is None:
                if (repo, key) in uncertain:
                    # GitHub kan være forsinket eller marker fjernet. Fravær er ikke
                    # bevis for at POST aldri ble utført. Operatør må avklare.
                    continue
                notification_status(database, identifier, "uavklart_post")
                uncertain.add((repo, key))
                ambiguous = True
                number = github.create(repo, item["title"], _section(key, item["body"]))
                issue_binding(database, repo, key, number)
            else:
                issue_binding(database, repo, key, number)
                old = github.read_body(repo, number)
                body = _replace(old, key, item["body"])
                if body != old:
                    github.update_body(repo, number, body)
            notification_status(database, identifier, "levert")
            uncertain.discard((repo, key))
        except Exception:
            # Bevar uavklart POST selv når feilen kommer etter ekstern sideeffekt.
            status = "uavklart_post" if ambiguous else "venter"
            notification_status(database, identifier, status, "github_leveringsfeil")
    return "venter" if pending_notifications(database, limit=1) else "levert"


class GitHubClient:
    """Fast HTTPS-vert/repo, eksisterende token, ingen redirect eller automatisk retry."""

    def __init__(self, token_environment: str, *, timeout: int = 30) -> None:
        self._token = os.environ.get(token_environment, "")
        self._timeout = timeout
        if not self._token or "\r" in self._token or "\n" in self._token:
            raise ValueError("Eksisterende GitHub-bakgrunnstilgang mangler")
        if not 1 <= timeout <= 120:
            raise ValueError("Timeout må være 1–120 sekunder")

    def _request(
        self,
        repository: str,
        suffix: str,
        method: str = "GET",
        payload: dict[str, str] | None = None,
    ) -> Any:
        if repository != AUTHORIZED_REPOSITORY:
            raise ValueError("Ikke autorisert GitHub-mottaker")
        data = json.dumps(payload).encode() if payload is not None else None
        request = Request(
            f"https://api.github.com/repos/{repository}/issues{suffix}",
            data=data,
            method=method,
            headers={
                "Authorization": "Bearer " + self._token,
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "budsjetthistorikk-B7/1",
                "Content-Type": "application/json",
            },
        )
        # Ingen råunntak gjøres til rapporter/logg; de kan inneholde requestdetaljer.
        try:
            with build_opener(NoRedirect()).open(request, timeout=self._timeout) as response:
                raw = response.read(8 * 1024 * 1024 + 1)
                if len(raw) > 8 * 1024 * 1024:
                    raise ValueError("For stor GitHub-respons")
                return json.loads(raw)
        except Exception:
            raise RuntimeError("github_httpfeil") from None

    def find(self, repository: str, marker: str) -> int | None:
        found: list[int] = []
        for page in range(1, 1001):
            data = self._request(repository, f"?state=all&per_page=100&page={page}")
            if not isinstance(data, list):
                raise ValueError("Ugyldig GitHub-liste")
            for issue in data:
                if not isinstance(issue, dict):
                    raise ValueError("Ugyldig GitHub-issue")
                if "pull_request" not in issue and marker in str(issue.get("body") or ""):
                    number = issue.get("number")
                    if type(number) is not int or number < 1:
                        raise ValueError("Ugyldig GitHub-nummer")
                    found.append(number)
            if len(data) < 100:
                if len(found) > 1:
                    raise ValueError("Flere GitHub-issues har samme stabile marker")
                return found[0] if found else None
        raise ValueError("GitHub-pagineringsgrensen nådd; ingen issue opprettes")

    def read_body(self, repository: str, number: int) -> str:
        data = self._request(repository, f"/{number}")
        if not isinstance(data, dict) or not isinstance(data.get("body"), str | type(None)):
            raise ValueError("Ugyldig GitHub-body")
        return str(data.get("body") or "")

    def create(self, repository: str, title: str, body: str) -> int:
        data = self._request(repository, "", "POST", {"title": title, "body": body})
        if not isinstance(data, dict) or type(data.get("number")) is not int or data["number"] < 1:
            raise ValueError("Ugyldig GitHub-opprettelsessvar")
        return int(data["number"])

    def update_body(self, repository: str, number: int, body: str) -> None:
        self._request(repository, f"/{number}", "PATCH", {"body": body})
