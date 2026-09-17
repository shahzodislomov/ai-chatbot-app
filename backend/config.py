"""Environment-backed configuration with secure local defaults."""

from __future__ import annotations

import os

DEFAULT_FRONTEND_ORIGIN = "http://localhost:5173"


def parse_cors_origins(value: str | None) -> tuple[str, ...]:
    """Parse a comma-separated origin allowlist and reject credentialed wildcards."""
    origins = tuple(origin.strip().rstrip("/") for origin in (value or "").split(",") if origin.strip())
    if not origins:
        return (DEFAULT_FRONTEND_ORIGIN,)
    if "*" in origins:
        raise ValueError("CORS_ORIGINS cannot contain '*' when credentials are enabled")
    if any(not origin.startswith(("http://", "https://")) for origin in origins):
        raise ValueError("Every CORS origin must start with http:// or https://")
    return origins


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
CORS_ORIGINS = parse_cors_origins(os.getenv("CORS_ORIGINS") or os.getenv("FRONTEND_URL"))
