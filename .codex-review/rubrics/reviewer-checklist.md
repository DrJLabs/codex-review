## Reviewer Checklist
- **Scope & Context**: Confirm the PR is focused, links to the driving work item, and includes author self-review notes or test evidence so you can review efficiently. Small, purpose-built PRs catch defects faster than sweeping diffs.
- **Design & API**: Guard backward compatibility, hidden coupling, or undocumented behaviour changes. Shared contracts should call out versioning or rollout plans and remain observable post-merge.
- **Correctness**: Trace happy paths, edge conditions, failure handling, and concurrency. Validate data flow, state transitions, and cleanup logic. Require regression tests when fixing bugs.
- **Security**: Inspect inputs, authN/Z paths, data exposure, secrets handling, dependency updates, and credential storage. Map findings to ASVS control areas where possible.
- **Performance & Reliability**: Watch for N+1s, blocking calls in hot paths, use of caching, retries, rate limits, and resource clean-up. Flag long-running migrations or rollout risks.
- **Observability**: Ensure new behaviour emits structured logs/metrics/traces with actionable context and avoids leaking sensitive data.
- **Testing Strategy**: Require unit/integration coverage that demonstrates the change, especially for error paths. Ask for reproducible steps when manual validation is required.
- **Style & Maintainability**: Enforce project style guides, consistent naming, and removal of dead code. Prefer extraction over duplication; request follow-up tickets only for out-of-scope work.
- **Collaboration Hygiene**: Request clarifying docs or diagrams when necessary, ensure reviewers with relevant code ownership are tagged, and unblock quickly with async feedback or pairing.
