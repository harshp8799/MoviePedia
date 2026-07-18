# ADR-003: FastAPI is the write/authz authority; clients read only published + own data

**Status:** Accepted · 2026-07-18

## Context

Firestore rules alone are hard to keep correct for complex business workflows; but routing all reads
through the API is expensive and slow for a public catalog.

## Decision

All writes and sensitive reads go through FastAPI (token verified, role resolved, business rules
applied). Clients may read `content where visibility=='published'` and their own per-user
subcollections directly from Firestore. Firestore rules are a second, default-deny wall.

## Consequences

- ➕ Cheap, cacheable, real-time public reads without double-charging through the API.
- ➕ Business logic and authorization centralized and testable.
- ➖ Two enforcement points to keep in sync (API + rules) — covered by rules tests + security tests.
