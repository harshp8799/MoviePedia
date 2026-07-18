# Cost & Scaling Review (Phase 9)

## Today: $0

The entire MVP builds and runs locally on the **Firebase Emulator Suite** (Spark plan). No
billing is enabled. Nothing built through Phase 7 requires a paid tier.

## What triggers cost (Blaze plan / paid services)

| Trigger                     | Service                        | Notes                                                                                                                    |
| --------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Deploying the API           | **Cloud Run** (or Render/Fly)  | Cloud Run needs a billing account (Blaze); has a free tier under Blaze. Render free tier is an alternative (spins down). |
| Production Storage          | **Cloud Storage for Firebase** | New Firebase projects require Blaze to use Storage.                                                                      |
| Firestore beyond free quota | **Firestore**                  | Free: 50k reads / 20k writes / 20k deletes per day, 1 GiB.                                                               |
| Web hosting                 | **Vercel Hobby**               | Free for the current scale.                                                                                              |
| Video (Phase 8)             | **Mux + video CDN**            | The real cost driver — see below.                                                                                        |

## Firestore cost risks (ranked)

1. **Read amplification on home/browse** — every rail + infinite scroll = reads × users.
   Mitigations in place: published-only queries, cursor pagination, summary shaping (1 read/card),
   home rails as one query per rail. Add ISR/CDN caching of public pages in Phase 10.
2. **Composite-index sprawl** — each filter+sort combo needs an index (write cost). Keep the
   supported filter set constrained (the query matrix in `docs/FIRESTORE.md`); don't offer arbitrary
   permutations. Prod indexes finalized in Phase 10 from real query needs.
3. **`searchTokens` array size** — capped prefixes (max 8) to bound doc size + index entries.
4. **Progress writes during playback** (Phase 8) — throttle client-side (e.g., every 15–30s), not
   every second, to avoid write-quota burn.

## Phase 8 (video) — be budget-aware before building

The upload → transcode → HLS → CDN pipeline is where costs become real and non-trivial:

- **Egress** is the dominant cost; adaptive streaming multiplies it. Never proxy bytes through the
  API; use a dedicated video CDN with signed short-TTL URLs and aggressive caching.
- **Firebase Storage is a poor video origin at scale** (egress pricing); use it for images/trailers
  only. Route real video through Mux (managed transcode + delivery) — behind `StoragePort`.
- Treat Phase 8 as a separate, metered project with a spending cap and alerts, not part of the free MVP.

## Recommendation

Stay on the free/local setup through Phase 9. Enable Blaze only when deploying (Phase 10), with a
**budget alert** configured first. Defer Phase 8 until the media strategy + budget are explicitly approved.
