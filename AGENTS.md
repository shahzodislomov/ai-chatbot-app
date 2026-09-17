# Engineering guidance

- Preserve the local-first privacy boundary: prompts, responses, embeddings, and histories must not leave user-controlled services.
- Never commit databases, Chroma collections, model files, environment files, credentials, or TLS private keys.
- Keep browser origins explicit when credentials are allowed; never combine wildcard CORS with credentials.
- Isolate Ollama and persistence boundaries so tests do not require a running model or mutate real conversations.
- Add focused tests for configuration, session lifecycle, error handling, and destructive memory operations.
- Do not expose raw internal exception details to API clients.
