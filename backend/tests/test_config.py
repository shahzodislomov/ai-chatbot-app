import unittest

from backend.config import DEFAULT_FRONTEND_ORIGIN, parse_cors_origins


class ParseCorsOriginsTests(unittest.TestCase):
    def test_uses_local_frontend_by_default(self) -> None:
        self.assertEqual(parse_cors_origins(None), (DEFAULT_FRONTEND_ORIGIN,))

    def test_normalizes_multiple_origins(self) -> None:
        self.assertEqual(
            parse_cors_origins(" https://chat.example.test/, http://localhost:4173 "),
            ("https://chat.example.test", "http://localhost:4173"),
        )

    def test_rejects_wildcard_with_credentials(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot contain"):
            parse_cors_origins("*")

    def test_rejects_non_http_origins(self) -> None:
        with self.assertRaisesRegex(ValueError, "must start"):
            parse_cors_origins("file:///tmp/chat.html")


if __name__ == "__main__":
    unittest.main()
