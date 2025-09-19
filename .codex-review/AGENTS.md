# AGENTS.md — Guidance for Local Coding Agents
- Python: Ruff + PEP 8, type hints; pytest.
- JS/TS: ESLint (+sonarjs), Prettier, TS strict; vitest/jest.
- Go: gofumpt, golangci-lint; `go test ./...`
- DRY: extract shared util modules with minimal APIs and list call sites.
- Gate on P0/P1 or HIGH per config.
