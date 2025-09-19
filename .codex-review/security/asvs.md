## OWASP ASVS Notes

Guidance aligns with the [OWASP Application Security Verification Standard (ASVS) v5.0.0](https://owasp.org/www-project-application-security-verification-standard/) (released 30 May 2025). See the [v5.0.0 release announcement](https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release) for canonical control definitions.

- **V1 Architecture & Design**: Classify data, diagram trust boundaries, and keep security controls centralized. Document mitigations for third-party services and secrets management plans.
- **V2 Authentication**: Enforce MFA-ready flows, lock accounts on brute-force attacks, and validate federated identity tokens server-side.
- **V3 Session Management**: Use secure, HttpOnly cookies with SameSite=strict/lax, regenerate session identifiers on privilege changes, and expire idle sessions. Include CSRF protections for state-changing requests.
- **V4 Access Control**: Apply server-side authorization checks on every request, prefer role/attribute-based checks, and forbid insecure direct object references.
- **V5 Validation/Sanitization**: Validate input length, type, and range; use allowlists; normalize before validation; encode output contextually to prevent injection.
- **V6 Stored Crypto**: Use vetted algorithms (AES-GCM, Argon2id), rotate keys, and keep key material out of source control. Use envelope encryption for cloud KMS.
- **V7 Error Handling & Logging**: Return generic errors to clients, log structured events with trace IDs, and scrub secrets/PII. Route security logs to immutable storage.
- **V8 Data Protection**: Prefer TLS 1.3 (minimum 1.2) with modern ciphers; enforce HTTP security headers (HSTS, CSP) and consider COOP/COEP as applicable. Redact sensitive fields before logging.
- **V9 Communication**: Guard SSRF, DNS rebinding, and outbound calls with allowlists and timeouts. Use parameterized queries / prepared statements for SQL and safe driver-level builders for NoSQL.
- **V10 Malicious Code**: Pin dependencies, generate an SBOM, scan for known vulnerabilities (SCA), and review supply-chain updates before rollout.
