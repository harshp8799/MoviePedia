# ADR-008: JavaScript-only + Zod/JSDoc guardrails instead of TypeScript

**Status:** Accepted · 2026-07-18

## Context

Project constraint: JavaScript/JSX only, no TypeScript. This removes compile-time type safety at the
API boundary where mistakes are costliest.

## Decision

Keep JS/JSX. Recover boundary safety with **Zod** runtime schemas in the shared `api-client` and
JSDoc `@typedef` annotations for editor hints. Backend uses Pydantic for the same guarantee server-side.

## Consequences

- ➕ Honors the constraint; runtime validation catches malformed API payloads.
- ➖ No static type checking across the JS codebase; discipline + tests compensate.
