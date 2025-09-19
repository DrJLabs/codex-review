## Reviewer Checklist
- Design/API: backward compatibility.
- Correctness: edge cases, errors, concurrency.
- Security: validation, authN/Z, injection, path handling, secrets.
- Performance: N+1, hot loops, blocking I/O.
- Observability: logs, metrics, traces.
- Tests: missing unit/edge/property cases.
- Style/Docs: naming, comments, dead code.
- Duplication: propose shared module; minimal API + call sites.
- Dependencies: deprecated, vulnerable, unpinned.
