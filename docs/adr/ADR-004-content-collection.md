# ADR-004: Single `content` collection with `type` discriminator

**Status:** Accepted · 2026-07-18

## Context

Home, trending, recent, search, and "similar" queries span both movies and series. Separate
`movies`/`series` collections would force union queries and duplicate index sets.

## Decision

One top-level `content` collection with `type: movie | series`. Seasons and episodes are
subcollections of a series content doc (`content/{id}/seasons/{sid}/episodes/{eid}`).

## Consequences

- ➕ Cross-type lists need one query + one index set.
- ➕ Seasons/episodes are bounded, naturally paginated, co-queried.
- ➖ Movie-only vs series-only fields coexist; kept manageable by not exploding optional fields and
  by validating shape per `type` in the domain layer.
