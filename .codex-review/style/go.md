## Go Style
- Adhere to Effective Go naming, receiver, and error-handling patterns; keep exported APIs documented with `// Package` and `// Function` comments.
- Format with `gofumpt` (superset of `gofmt`) and run `goimports` to maintain grouped imports. Reject diffs that are not formatted.
- Use `golangci-lint` with linters `govet`, `staticcheck`, `errcheck`, `ineffassign`, `gosimple`, and `bodyclose`. Enable modules (`GO111MODULE=on`) and vendor only when required.
- Return wrapped errors (`fmt.Errorf("...: %w", err)`) and avoid panic in libraries. Prefer context-aware APIs and pass `context.Context` as the first param.
- Constrain goroutines with contexts or wait groups, close channels explicitly, and guard shared state with mutexes or use channel ownership.
- Tests: organize with table-driven tests, `t.Helper()` for shared assertions, and `go test ./...` in CI. Use benchmarks for hot-path changes.
