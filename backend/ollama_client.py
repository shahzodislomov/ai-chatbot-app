"""Small, testable boundary around the Ollama HTTP API."""

import requests

if __package__:
    from .config import OLLAMA_BASE_URL, OLLAMA_MODEL
else:  # Support running ``python backend/main.py``.
    from config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaServiceError(RuntimeError):
    """Raised when Ollama cannot produce a usable response."""


def call_ollama(prompt: str, context: str = "") -> str:
    """Return an Ollama response without exposing transport error details."""
    full_prompt = f"""You are a helpful AI assistant.

{f'Previous context: {context}' if context else ''}

User: {prompt}
Assistant:"""

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=300,
        )
        response.raise_for_status()
        generated_text = response.json()["response"]
        if not isinstance(generated_text, str):
            raise TypeError("Ollama response field must be a string")
        return generated_text.strip()
    except (requests.RequestException, KeyError, TypeError, ValueError) as error:
        raise OllamaServiceError("Ollama service request failed") from error
