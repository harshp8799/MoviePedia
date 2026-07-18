# ADR-002: Clean Architecture / Ports & Adapters (pragmatic)

**Status:** Accepted · 2026-07-18

## Context

Firebase-specific code must not spread through business logic; search/storage/notifications must be
swappable. But empty abstraction layers are a real over-engineering risk.

## Decision

Layered dependency rule: Presentation → Application → Domain ← Infrastructure. Domain imports no
framework/Firebase code. **A layer/port exists only if it holds real logic or an interface with
more than one implementation or caller** (or imminently will). No pass-through `*ServiceImpl`.

## Consequences

- ➕ Domain + use-cases unit-testable with fakes; adapters tested against the emulator.
- ➕ Swapping Firestore/search/storage is localized to one adapter.
- ➖ Slightly steeper onboarding; mitigated by the module map and this rule.
