# Security Model, Threat Summary & Review (Phase 9)

## Model (recap)

Two enforcement walls (ADR-003):

1. **FastAPI is the authority** for all writes and sensitive reads — verifies the Firebase ID
   token, resolves role from **custom claims**, applies business rules, and audits mutations.
2. **Firestore/Storage rules** are the default-deny second wall: public clients read only
   `content where visibility=='published'` + their own per-user subcollections; published `public/`
   images are world-readable; all client writes to catalog/storage are denied (server-only via Admin SDK).

## Verified by tests

| Control                                                                             | Test                                                       |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Invalid / missing token → 401                                                       | `test_auth.py`                                             |
| Normal user → admin route → 403; editor → admin-only → 403                          | `test_auth.py`, `test_admin_catalog.py`                    |
| Draft content hidden from public (API 404 + rules deny)                             | `test_public_*`, `firestore.rules.test.mjs`                |
| Client writes to catalog denied                                                     | `firestore.rules.test.mjs`                                 |
| Cross-user library access denied; unauth library → 401                              | `firestore.rules.test.mjs`, `test_library.py`, library e2e |
| Public images readable; client storage writes denied; originals not client-readable | `storage.rules.test.mjs`                                   |
| Upload content-type validated                                                       | `test_admin_catalog.py`                                    |
| Rate limiting (per-IP) → 429; security headers present                              | `test_security.py`                                         |

## Threat summary (STRIDE-lite) & mitigations

- **Spoofing** — Firebase ID-token verification (`check_revoked`); role never trusted from body.
- **Tampering** — writes server-only; rules default-deny; audit log on every admin mutation.
- **Repudiation** — `audit_logs` records actor/action/entity/before/after/timestamp.
- **Information disclosure** — public API strips internal fields; drafts hidden; media via short-TTL
  signed URLs; logs never contain tokens/secrets/PII.
- **Denial of service** — per-IP rate limiting (in-memory MVP; Redis when scaled); Firestore
  query shapes constrained by indexes.
- **Elevation of privilege** — roles set only via a protected path (admin/script), never client input.

## Residual risks / follow-ups

- **App Check** not yet enforced (adds client-attestation) — recommended before public launch.
- **Rate limiter is per-process** (in-memory) — move to Redis when running >1 instance.
- **API uses the shared root `.venv`** in dev — production should use an isolated venv/container
  for `services/api` (the shared venv also carries unrelated MCP tooling with its own pins).
- **CORS/App Check/CSP** to be finalized per real deploy origins in Phase 10.

## Dependency audit (2026-07-18)

- Runtime-facing **Next.js** advisory patched: `next` → `14.2.35` (stayed on 14.2 line, non-breaking);
  web build re-verified green.
- Remaining `npm audit` findings (28) are **transitive in Expo / firebase-tools build toolchains**
  (`tar`, `glob`, `@xmldom/xmldom`, …) — used at build/CLI time, not in the shipped web bundle or
  Hermes bundle. Their only fixes are **breaking** major upgrades (Expo 57, Next 16, firebase-tools 14/16);
  scheduled as a deliberate upgrade task in Phase 10, not applied here to avoid destabilizing the MVP.
- Python: our pins (fastapi/pydantic/firebase-admin) are internally consistent; a `pip check` warning
  about `mcp`/`sse-starlette` comes from unrelated tooling sharing the dev venv (see follow-up above).
