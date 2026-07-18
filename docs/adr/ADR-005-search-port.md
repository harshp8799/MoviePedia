# ADR-005: Firestore-native search behind `SearchPort` for MVP

**Status:** Accepted · 2026-07-18

## Context

Firestore is not a full-text search engine. A dedicated engine (Typesense/Algolia/Meilisearch) is
real infrastructure and cost we don't need at MVP scale (thousands–low-tens-of-thousands of titles).

## Decision

MVP search = normalized title fields + capped prefix `searchTokens` (`array-contains`) + facet
filters (genre/year/language/type/status) + composite indexes, implemented behind a `SearchPort`.

## Consequences

- ➕ Zero extra infra; adequate for MVP catalog size.
- ➕ Swap to Typesense/Algolia later by adding one adapter; callers unchanged.
- ➖ No typo-tolerance/relevance ranking beyond `popularity`; acceptable for MVP, revisit post-MVP.
