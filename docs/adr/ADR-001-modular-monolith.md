# ADR-001: Modular monolith over microservices

**Status:** Accepted · 2026-07-18

## Context

Solo/small team, free Firebase plan, MVP scope. Microservices add deployment, networking, and
debugging overhead disproportionate to current scale.

## Decision

Ship a single deployable FastAPI modular monolith. Modules (`auth, catalog, media, user_library,
admin, search, notifications, analytics`) have clear boundaries and communicate via use-cases/ports,
not by reaching into each other's data adapters.

## Consequences

- ➕ Lower cost/complexity, easier debugging, one deploy target.
- ➕ Module boundaries become future service seams if scale demands extraction.
- ➖ Requires discipline to keep boundaries clean inside one process (enforced via dependency rule).
