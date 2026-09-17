# Roadmap

## Foundation

- [x] Protect local databases, vector data, environments, dependencies, and key material from Git.
- [x] Replace wildcard credentialed CORS with validated configured origins.
- [ ] Separate application construction from database and Chroma initialization.
- [ ] Add backend linting, formatting, typing, and test configuration.

## Reliability and privacy

- [ ] Return stable upstream-service errors without exposing internal exception text.
- [ ] Use dependency-managed database sessions with rollback behavior.
- [ ] Scope destructive memory deletion to an explicit session or require deliberate global confirmation.
- [ ] Add request validation limits and structured application logging without prompt content.

## Product quality

- [ ] Add mocked Ollama and persistence integration tests.
- [ ] Add frontend loading, empty, initialization-error, and retry states.
- [ ] Add accessible dialog behavior and keyboard navigation.
- [ ] Add CI for backend tests and frontend production builds.
