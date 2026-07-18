# Movie Pedia — Task Tracker

Single source of truth for progress. `[ ]` todo · `[~]` in progress · `[x]` done · `[-]` deferred.

Legend for phases from the master plan. One phase at a time; stop & report at each end.

---

## Confirmed Decisions (2026-07-18)

- **Firebase plan:** Spark (free). Entire MVP built + run locally on **Emulator Suite** ($0). Paid hosting = Phase 10 decision.
- **Playback (MVP):** trailers + external authorized URLs + small owner clips — all signed-URL/metadata based, **no transcoding**.
- **Web hosting:** Vercel Hobby (free, native Next.js SSR).
- **Package manager:** npm workspaces.
- **Scripts target OS:** macOS / zsh (bash-compatible).
- **Transcoding (Phase 8, deferred):** Mux (managed).

---

## Phase 0 — Discovery ✅

- [x] Scope, MVP, deferred features, risks, assumptions (delivered as architecture dossier)

## Phase 1 — Architecture ✅

- [x] MVC vs Modular Monolith + Clean Arch comparison
- [x] Final architecture recommendation + tech table
- [x] System / auth / media diagrams (Mermaid)
- [x] Backend module boundaries
- [x] Web + Android architecture
- [x] Repo structure, Firestore query matrix + collection design
- [x] API endpoint plan, security model, media strategy
- [x] Testing strategy, deployment, cost/scaling risks, ADRs

## Phase 2 — Repository Bootstrap 🚧 (current)

- [x] Git repo initialized
- [x] Root: `package.json` (npm workspaces), `.gitignore`, `.env.example`, `README.md`
- [x] Linting/formatting: Prettier + ESLint (JS), Ruff + Black (Python), EditorConfig
- [x] `docs/`: architecture summary + 9 ADRs
- [x] `packages/shared-config` (roles, statuses, enums, env keys)
- [x] `packages/design-tokens`
- [x] `packages/shared-utils` (slug, dates, formatting)
- [x] `packages/api-client` (fetch wrapper + Zod schemas)
- [x] `services/api` FastAPI Clean-Arch skeleton + health endpoint + config + logging
- [x] `services/api` starts successfully (validated: uvicorn boot + 2 pytest + ruff clean)
- [x] `apps/web` Next.js App Router (JS/JSX + Tailwind) minimal shell
- [x] `apps/web` builds successfully (validated: `next build` prerenders + lint clean)
- [x] `apps/mobile` Expo + Expo Router (JS) minimal shell + monorepo Metro config
- [x] `apps/mobile` config valid (validated: `expo config` resolves SDK 52; full Metro bundle needs an Android emulator)
- [x] `firebase/` config: rules stubs, indexes, emulator config, per-env `.firebaserc`
- [x] `scripts/` seed / reset-dev-data / set-admin-claims (safe stubs)
- [x] `.github/workflows/ci.yml` (lint+test+build gate)
- [x] Initial commit + pushed to origin (github.com/harshp8799/MoviePedia)
- [x] PHASE 2 COMPLETION REPORT

## Phase 3 — Firebase Foundation ✅

- [x] Per-env project strategy (`.firebaserc`), auth providers, Firestore collection design (`docs/FIRESTORE.md`)
- [x] Firestore composite indexes (9) + hardened security rules + Storage rules
- [x] Emulator config, Firebase Admin SDK integration (`services/api/.../infrastructure/firebase/admin.py`), readiness wired
- [x] Real seed data (`scripts/seed.py`): 7 genres, 3 movies + 1 draft, series+season+2 episodes, 3 demo accounts w/ roles
- [x] set-admin-claims + reset-dev-data scripts (emulator-guarded)
- [x] Rules tests (emulator): **7/7 pass** — draft hidden, catalog writes denied, owner-only user data
- [x] Validated: `npm run test:rules` (7/7) · seed populates emulator · API `/ready` → `firebase: ok` · pytest 2/2 · ruff clean
- [ ] Commit + push (pending your go-ahead)

## Phase 4 — Backend Foundation ⏳

- [ ] App factory, config, error handling, logging, health/ready
- [ ] Firebase token verification + RBAC deps
- [ ] Base repository ports + Firestore adapters
- [ ] API response conventions + test framework

## Phase 5 — Catalog & Admin MVP ⏳

## Phase 6 — Public Web MVP ⏳

## Phase 7 — Android MVP ⏳

## Phase 8 — Authorized Media Playback ⏳ (deferred pipeline)

## Phase 9 — Hardening ⏳

## Phase 10 — Deployment ⏳

## Phase 11 — Post-MVP ⏳
