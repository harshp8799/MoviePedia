# Firestore Data Model & Query Matrix

Concrete data layer for Movie Pedia (Phase 3). Rules: `firebase/firestore.rules` ·
Indexes: `firebase/firestore.indexes.json` · Tests: `firebase/tests/`.

## Collections

| Collection                                  | Key         | Access                                   | Notes                                                 |
| ------------------------------------------- | ----------- | ---------------------------------------- | ----------------------------------------------------- |
| `content/{id}`                              | random      | public read if `published`; server write | movies **and** series (`type` discriminator, ADR-004) |
| `content/{id}/seasons/{sid}`                | random      | read if parent published                 | series only                                           |
| `content/{id}/seasons/{sid}/episodes/{eid}` | random      | read if parent published                 | series only                                           |
| `genres/{slug}`                             | slug        | public read; server write                | reference data                                        |
| `homepage_sections/{id}`                    | id          | public read; server write                | ordered `contentIds[]` → batched get (no N+1)         |
| `collections/{id}`                          | id          | public read; server write                | curated groupings                                     |
| `people/{id}`                               | id          | public read; server write                | cast/crew                                             |
| `users/{uid}`                               | uid         | owner read; server write                 | profile + role mirror                                 |
| `user_libraries/{uid}/items/{id}`           | random      | owner read+write                         | watchlist/favorites                                   |
| `watch_progress/{uid}/items/{contentId}`    | `contentId` | owner read+write                         | idempotent upserts                                    |
| `viewing_history/{uid}/items/{id}`          | random      | owner read+write                         | history                                               |
| `media_assets/{id}`                         | random      | server only                              | storage refs (never client-read)                      |
| `audit_logs/{id}`                           | random      | server only                              | admin mutations                                       |
| `processing_jobs/{id}`                      | random      | server only                              | Phase 8                                               |
| `app_config/{id}`                           | id          | server only                              | feature flags                                         |

## `content` document (canonical)

See `scripts/seed.py::content_doc` for the authoritative shape. Fields: `type, slug, title,
originalTitle, shortDescription, fullDescription, releaseDate/Year, durationMinutes, ageRating,
genres[], languages[], countries[], poster, backdrop, trailer?, visibility, featured,
trendingScore, popularity, searchTokens[], schemaVersion, createdAt, updatedAt, publishedAt,
createdBy, updatedBy`.

## Query matrix → index

| Feature            | Query                                                                 | Index (composite)                        |
| ------------------ | --------------------------------------------------------------------- | ---------------------------------------- |
| Movies/series list | `type== · visibility=='published'` sort `popularity`                  | `(type, visibility, popularity)`         |
| Browse by year     | `type== · visibility==` sort `releaseYear`                            | `(type, visibility, releaseYear)`        |
| Recently added     | `visibility==` sort `publishedAt`                                     | `(visibility, publishedAt)`              |
| Trending           | `visibility==` sort `trendingScore`                                   | `(visibility, trendingScore)`            |
| Similar / by genre | `genres array-contains · visibility==` sort `popularity`              | `(genres, visibility, popularity)`       |
| Search             | `searchTokens array-contains prefix · visibility==` sort `popularity` | `(searchTokens, visibility, popularity)` |
| Admin catalog      | `type==` sort `updatedAt`                                             | `(type, updatedAt)`                      |
| Watchlist          | `items where listType==` sort `addedAt`                               | `(listType, addedAt)`                    |
| Continue watching  | `items where completed==false` sort `updatedAt`                       | `(completed, updatedAt)`                 |

All list reads use cursor pagination. Public list queries always constrain `visibility=='published'`,
so that field is part of nearly every composite index by design.

## Conventions

Server timestamps everywhere · `schemaVersion` on every doc for migrations · random IDs for
high-write collections (avoid hotspotting) · `watch_progress` keyed by `contentId` for idempotency ·
no unbounded arrays (`genres`/`searchTokens` capped; rails via ordered-ID docs) · binaries in Storage,
never Firestore.
