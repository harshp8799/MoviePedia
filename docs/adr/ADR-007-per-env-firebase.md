# ADR-007: Separate Firebase project per environment

**Status:** Accepted · 2026-07-18

## Context

Sharing one Firebase project across environments risks corrupting production data with test writes
and conflating rules/quotas.

## Decision

Distinct projects: `local` (Emulator Suite, free), `dev`, `staging`, `production`. `.firebaserc`
maps aliases; CI targets per-environment projects.

## Consequences

- ➕ Blast-radius isolation; safe rule/schema experiments.
- ➖ More projects to manage; mitigated by the emulator covering all local work at $0.
