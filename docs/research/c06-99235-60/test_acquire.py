"""Offline negative transport probes; no real network requests."""

import tempfile
import unittest
import urllib.request
from pathlib import Path

from acquire import NoRedirect, capture, validate_url


class BoundaryTests(unittest.TestCase):
    def test_urllib_redirect_policy_never_follows_automatically(self):
        handler = NoRedirect()
        result = handler.redirect_request(
            urllib.request.Request("https://www.stortinget.no/a"),
            None,
            302,
            "Found",
            {},
            "https://evil.example/b",
        )
        self.assertIsNone(result)

    def test_identifier_rejected_before_request(self):
        for identifier in ("../escape", "..", "C:/escape", "a\\b", "a:b", "a\n"):
            calls = []
            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
                with self.assertRaises(ValueError):
                    capture(
                        identifier,
                        "https://www.stortinget.no/a",
                        Path(directory),
                        lambda req, calls=calls: calls.append(req),
                    )
            self.assertEqual(calls, [])

    def test_existing_attempt_not_overwritten(self):
        calls = []

        def fake(req):
            calls.append(req.full_url)
            return Reply(200, {}, b"original\r\n\x00\xc3\xb8")

        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            capture("once", "https://www.stortinget.no/a", Path(directory), fake)
            previous = {p.name: p.read_bytes() for p in Path(directory).iterdir()}
            with self.assertRaises(FileExistsError):
                capture("once", "https://www.stortinget.no/a", Path(directory), fake)
            self.assertEqual(previous, {p.name: p.read_bytes() for p in Path(directory).iterdir()})
        self.assertEqual(len(calls), 1)

    def test_start_rejected_before_request(self):
        invalid = [
            "http://data.stortinget.no/x",
            "https://data.stortinget.no.evil.example/x",
            "https://evil.example/x",
            "https://data.stortinget.no:8443/x",
            "https://name:secret@data.stortinget.no/x",
            "https://data.stortinget.no./x",
            "https://www.stortinget.no\\@evil.example/x",
        ]
        for url in invalid:
            calls = []
            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
                with self.assertRaises(ValueError):
                    capture(
                        "negative",
                        url,
                        Path(directory),
                        opener=lambda req, calls=calls: calls.append(req),
                    )
            self.assertEqual(calls, [])

    def test_allowed(self):
        for host in ("data.stortinget.no", "www.stortinget.no", "www.regjeringen.no"):
            validate_url("https://" + host + "/x")

    def test_every_redirect_rejected_before_next_request(self):
        for location in (
            "https://evil.example/leak",
            "http://www.stortinget.no/x",
            "https://www.stortinget.no:8080/x",
            "https://user@www.stortinget.no/x",
            "//data.stortinget.no.evil.example/x",
        ):
            calls = []

            def fake(req, calls=calls, location=location):
                calls.append(req.full_url)
                return Reply(302, {"Location": location}, b"redirect body")

            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
                meta = capture("redirect", "https://www.stortinget.no/a", Path(directory), fake)
                self.assertEqual(meta["state"], "redirect_rejected")
                self.assertEqual(meta["hops"][0]["bytes"], 13)
            self.assertEqual(calls, ["https://www.stortinget.no/a"])

    def test_relative_and_second_redirect(self):
        calls = []

        def fake(req):
            calls.append(req.full_url)
            if len(calls) == 1:
                return Reply(302, {"Location": "/b"}, b"first")
            return Reply(302, {"Location": "https://evil.example/third"}, b"second")

        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            meta = capture("chain", "https://www.stortinget.no/a", Path(directory), fake)
            self.assertEqual(meta["state"], "redirect_rejected")
            self.assertEqual(len(meta["hops"]), 2)
        self.assertEqual(calls, ["https://www.stortinget.no/a", "https://www.stortinget.no/b"])

    def test_partial_body_preserved(self):
        class Partial(Reply):
            def read(self, size):
                if self.body:
                    return super().read(size)
                raise TimeoutError("offline interruption")

        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            meta = capture(
                "partial",
                "https://www.stortinget.no/a",
                Path(directory),
                lambda req: Partial(200, {}, b"partial body"),
            )
            self.assertEqual(meta["state"], "transport_failed")
            self.assertEqual(meta["hops"][0]["bytes"], 12)
            self.assertFalse(meta["hops"][0]["body_complete"])

    def test_complete_error_body_preserved(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            meta = capture(
                "error",
                "https://www.stortinget.no/a",
                Path(directory),
                lambda req: Reply(500, {}, b"error page"),
            )
            self.assertEqual(meta["state"], "http_error")
            self.assertTrue(meta["hops"][0]["body_complete"])


class Reply:
    def __init__(self, status, headers, body):
        self.status, self.headers, self.body = status, headers, body

    def read(self, size):
        body, self.body = self.body[:size], self.body[size:]
        return body

    def close(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
