import unittest
from unittest.mock import Mock, patch

import requests

from backend.ollama_client import OllamaServiceError, call_ollama


class CallOllamaTests(unittest.TestCase):
    @patch("backend.ollama_client.requests.post")
    def test_returns_trimmed_generated_text(self, post: Mock) -> None:
        response = post.return_value
        response.json.return_value = {"response": "  Hello there.  "}

        self.assertEqual(call_ollama("Hello"), "Hello there.")
        response.raise_for_status.assert_called_once_with()

    @patch("backend.ollama_client.requests.post")
    def test_replaces_transport_details_with_stable_error(self, post: Mock) -> None:
        sensitive_detail = "connection refused at http://internal-host:11434?token=secret"
        post.side_effect = requests.ConnectionError(sensitive_detail)

        with self.assertRaises(OllamaServiceError) as raised:
            call_ollama("Hello")

        self.assertEqual(str(raised.exception), "Ollama service request failed")
        self.assertNotIn("internal-host", str(raised.exception))
        self.assertNotIn("secret", str(raised.exception))

    @patch("backend.ollama_client.requests.post")
    def test_rejects_malformed_response_without_exposing_payload(self, post: Mock) -> None:
        response = post.return_value
        response.json.return_value = {"unexpected": "private diagnostic"}

        with self.assertRaisesRegex(OllamaServiceError, "service request failed"):
            call_ollama("Hello")


if __name__ == "__main__":
    unittest.main()
