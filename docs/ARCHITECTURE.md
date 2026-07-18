# Movie Pedia — Architecture

Status: Phase 1 baseline. Authoritative summary; ADRs in [`adr/`](adr/).

## Core stances

1. **Modular monolith** FastAPI backend, **Clean Architecture / Ports & Adapters**. Domain never
   imports Firebase; adapters implement ports (`MovieRepository`, `SearchPort`, `StoragePort`,
   `NotificationPort`, `AuthPort`, `AuditLogPort`, `UserLibraryRepo`).
2. **FastAPI is the authority** for all writes and sensitive reads. Clients read only
   `content where visibility == 'published'` and their own subcollections directly from Firestore.
3. **Two security walls:** FastAPI authorization (primary) + Firestore rules default-deny (secondary).
4. **No in-house video transcoding in the MVP.** Trailers + external authorized URLs + small owner
   clips, all served via signed, time-limited URLs. Full upload→transcode→HLS→CDN pipeline is
   designed but deferred to Phase 8 (managed: Mux).
5. **Firestore-native search** behind a `SearchPort` for the MVP; dedicated engine (Typesense/Algolia)
   is a later swap.

## Data plane

- **Single `content` top-level collection** (`type: movie | series`) so home/trending/search/similar
  span both with one index set. Seasons/episodes are subcollections of a series content doc.
- Per-user subcollections: `user_libraries/{uid}/items`, `watch_progress/{uid}/items`,
  `viewing_history/{uid}/items` → natural owner-only rules, no unbounded arrays.
- Media binaries in Cloud Storage; Firestore holds only `media_assets` metadata + references.
- Every doc: server timestamps + `schemaVersion`. Random IDs for high-write collections. `watch_progress`
  doc id = `contentId` (idempotent upserts). Curated home rails via ordered-ID docs + batched `getAll`.

## Auth

Firebase Auth (email/password + Google) → client gets ID token → FastAPI `verify_id_token` (Admin SDK)
→ role from **custom claims** (`admin | editor | user`) → default-deny authorization. Role/UID never
trusted from request body. Roles set only via a protected admin endpoint.

## Media (MVP vs Phase 8)

- **MVP:** signed PUT upload URLs (server validates type/size), signed short-TTL GET playback URLs
  after visibility/availability check. Bytes never proxy through FastAPI.
- **Phase 8:** upload → Storage → `processing_job` → managed transcode (Mux) → HLS → video CDN →
  signed ABR playback. DRM/offline = Phase 11.

## Environments

Separate Firebase project per environment: `local` (emulator, free), `dev`, `staging`, `production`.
The whole MVP runs on the **Emulator Suite** at $0 (Spark plan).

## Diagrams, query matrix, endpoint plan, cost/scaling risks

See the Phase 0/1 dossier (delivered in project chat) and the per-topic docs added in later phases.
Query matrix and endpoint plan are reproduced in `docs/` as they stabilize (Phase 3/4).
