# ADR-006: No in-house transcoding in MVP; signed authorized URLs only

**Status:** Accepted · 2026-07-18

## Context

Full video hosting (upload → FFmpeg/managed transcode → HLS → CDN → DRM) is a project in itself with
significant egress cost. Firebase Storage is a poor video origin at scale. The user is on the free plan.

## Decision

MVP serves trailers, external authorized playback URLs, and small owner-uploaded clips — all via
signed, time-limited URLs after an authorization/visibility check. No transcoding. The full pipeline
is designed behind `StoragePort`/signed-URL abstractions and built in Phase 8 using **Mux** (managed).

## Consequences

- ➕ Ships a working "watch" experience legally and at $0 on the free plan.
- ➕ Phase 8 upgrade is localized behind ports.
- ➖ No adaptive multi-rendition streaming until Phase 8; DRM/offline = Phase 11.
