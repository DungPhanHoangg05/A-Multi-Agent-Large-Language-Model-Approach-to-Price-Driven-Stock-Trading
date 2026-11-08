"""Kiểm observer thuần chẩn đoán, không mạng hoặc đổi hợp đồng runtime khoa học."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from uuid import uuid4

import httpx

from core.historical_transport_observer import exception_chain, observe_transport, record_error, source_bindings

ROOT = Path(__file__).resolve().parents[1]


class ObserverTests(unittest.TestCase):
    """Response/request/exception được giữ nguyên; không retry hoặc lưu secret."""

    def test_exception_chain_omits_messages_and_handles_cycles(self) -> None:
        error = httpx.ReadError("SECRET_KEY")
        cause = OSError(10054, "SECRET_BODY")
        error.__cause__ = cause
        cause.__context__ = error
        chain = exception_chain(error)
        self.assertEqual(len(chain), 2)
        self.assertEqual(chain[1]["errno"], 10054)
        self.assertNotIn("SECRET", str(chain))

    def test_unanchored_observer_is_rejected(self) -> None:
        with patch("core.historical_transport_observer.subprocess.check_output", return_value=b"wrong"):
            with self.assertRaisesRegex(ValueError, "neo Git"):
                source_bindings(ROOT)

    def test_error_record_has_no_headers_body_or_error_text(self) -> None:
        from core.historical_evaluation_journal import load
        with TemporaryDirectory() as folder, redirect_stderr(StringIO()) as console:
            identifier = str(uuid4())
            row = {"id": identifier, "checkpoint_attempt_id": str(uuid4()), "role": "pattern"}
            transport = SimpleNamespace(clients=SimpleNamespace(book=SimpleNamespace(
                directory=Path(folder), uuid=str(uuid4()), signature="scope")),
                pacer=SimpleNamespace(state={"requests": [row]}))
            request = httpx.Request("POST", "https://api.groq.com", content=b"SECRET_BODY",
                                    headers={"authorization": "SECRET_KEY"},
                                    extensions={"timeout": {"read": 120, "secret": "SECRET"}})
            record_error(transport, request, httpx.ReadTimeout("SECRET_ERROR"), {})
            result = load(Path(folder) / "diagnostics" / (identifier + ".json"))
            self.assertEqual(result["timeouts"], {"read": 120})
            self.assertEqual(result["request_bytes"], len(b"SECRET_BODY"))
            self.assertNotIn("SECRET", str(result) + console.getvalue())
            self.assertEqual(row, {"id": identifier, "checkpoint_attempt_id": row["checkpoint_attempt_id"], "role": "pattern"})

    def test_observer_preserves_request_response_and_restores_method(self) -> None:
        from core.historical_evaluation_clients import RawHTTP
        request = httpx.Request("POST", "https://api.groq.com", content=b"payload")
        response = httpx.Response(200)
        with patch.object(RawHTTP, "handle_request", return_value=response) as original, \
                patch("core.historical_transport_observer.source_bindings", return_value={}):
            transport = object.__new__(RawHTTP)
            with observe_transport(ROOT):
                self.assertIs(transport.handle_request(request), response)
            self.assertIs(RawHTTP.handle_request, original)
            original.assert_called_once_with(transport, request)

    def test_observer_reraises_same_exception_without_retry_even_if_logging_fails(self) -> None:
        from core.historical_evaluation_clients import RawHTTP
        error = httpx.ReadTimeout("SECRET_ERROR")
        with patch.object(RawHTTP, "handle_request", side_effect=error) as original, \
                patch("core.historical_transport_observer.source_bindings", return_value={}), \
                patch("core.historical_transport_observer.record_error", side_effect=OSError()), \
                redirect_stderr(StringIO()) as console:
            transport = object.__new__(RawHTTP)
            with observe_transport(ROOT):
                with self.assertRaises(httpx.ReadTimeout) as caught:
                    transport.handle_request(httpx.Request("POST", "https://api.groq.com"))
            self.assertIs(caught.exception, error)
            self.assertEqual(original.call_count, 1)
            self.assertNotIn("SECRET", console.getvalue())


if __name__ == "__main__":
    unittest.main()
