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

## Phase 4 — Backend Foundation ✅

- [x] App factory, config, health/ready (from Phase 2/3) + request-id logging middleware
- [x] Consistent error envelope `{error:{code,message,details}}` via exception handlers (AppError, validation, unhandled)
- [x] Firebase token verification (`AuthPort` → `FirebaseAuthAdapter`, check_revoked)
- [x] RBAC dependencies: `get_current_user` + `require_role(*roles)`, deny-by-default; role read only from verified claims
- [x] RBAC probe routes: `/users/me`, `/admin/ping` (admin), `/admin/editorial` (admin+editor)
- [x] Base repository (`FirestoreRepository`) + `FirestoreContentRepository` (get_by_slug, create, list_published)
- [x] Response schemas: error envelope, cursor `Page`, `CurrentUser`
- [x] Validated: 11 auth/RBAC/health tests pass · repo adapter test passes vs live emulator · ruff clean
- [ ] Commit + push (pending your go-ahead)

## Phase 5 — Catalog & Admin MVP 🚧

### Part A — Backend catalog/admin API ✅

- [x] Domain rules (`content_rules`): slug, search tokens, publish state machine, doc assembly
- [x] Value objects: ContentType / Visibility / Role enums
- [x] Ports: ContentRepository (get/create/update/set_visibility/list/seasons/episodes) + GenreRepository
- [x] Firestore adapters: content, genre, audit-log, storage (signed URLs; emulator fallback)
- [x] `CatalogService` use-cases (genres, movies, series, seasons, episodes, publish/archive, upload-url) — audits every mutation
- [x] Admin routers: genres CRUD, movie/series create, content update, publish/archive/unpublish, seasons/episodes, upload-url, catalog list
- [x] Validation via Pydantic request schemas; RBAC (editor+admin; genre delete admin-only)
- [x] Tests: 6 domain-rule + 9 admin-catalog (fakes) + 2 emulator integration — all pass; ruff clean
- [ ] Commit + push Part A (pending your go-ahead)

### Part B — Admin web UI ✅

- [x] Firebase Web SDK init (Auth emulator locally) + shared API client with token injection
- [x] AuthProvider (context, role from claims) + QueryProvider (TanStack Query)
- [x] Protected `/admin` layout with auth+role guard; `/admin/login` page
- [x] Dashboard: create movie/series form, catalog table with publish/archive/unpublish, genres add/list, audit-log viewer (admin)
- [x] Backend: added `GET /admin/audit-logs` (admin) + AuditLogPort.list
- [x] Validated: `next build` compiles /admin + /admin/login · web lint clean · **full e2e proven** (Firebase sign-in → ID token w/ role → API verify → RBAC: admin 201, user 403, no-token 401)
- [ ] Commit + push Part B (pending your go-ahead)
- Note: interactive browser flow (button clicks) needs manual verification; API contract + auth chain are proven

## Phase 6 — Public Web MVP ✅

### Part A — Public catalog read API ✅

- [x] ContentRepository public reads: query_published (filters + cursor pagination), get_published_by_slug, search_published, similar_published, list_seasons/episodes
- [x] `PublicCatalogService`: home rails (trending/popular/recent), listings, detail (+seasons/episodes/similar), search, genres — strips internal fields
- [x] Public routes (no auth): `/home`, `/genres`, `/movies`, `/series`, `/movies/{slug}`, `/series/{slug}`, `/search`
- [x] Added composite index (visibility, popularity)
- [x] Tests: 3 shaping unit + fakes + 3 emulator integration; ruff clean
- [x] Live HTTP smoke: home rails, listings, detail+seasons, search, draft→404 all correct
- [ ] Commit + push Part A

### Part B — Public web pages ✅

- [x] `(public)` route group + Nav (with search) + shared components (ContentCard, Rail, Listing, DetailView)
- [x] Homepage rails (trending/popular/recent), movies/series listings with sort + genre filters
- [x] Detail pages (movie + series with seasons/episodes + similar), SSR + dynamic SEO/OG metadata, 404 handling
- [x] Search page (no-JS form), empty/error states, responsive grid, reads public API server-side
- [x] Validated: build compiles, web lint clean, **live SSR render** (home rails + seed titles + `<title>`/og:title + series episodes + unknown-slug→404)
- [ ] Commit + push Part B

### Part C — Public auth + user library ✅

- [x] UserLibraryRepository port + Firestore adapter (owner-scoped subcollections)
- [x] UserLibraryService: watchlist/favorites, recently-viewed history, watch progress (continue-watching); denormalized summaries
- [x] Routes (auth): `/library/{watchlist|favorites}`, `/history`, `/progress` + PUT
- [x] Public auth UI: `/login` (sign in / sign up / Google), auth-aware Nav
- [x] Library + History pages, DetailActions (watchlist/favorite toggle + record view) on detail
- [x] Tests: 7 library (fakes) + 1 emulator integration; ruff clean
- [x] Validated: web build compiles, lint clean; full library e2e via token (add/list/progress/history/remove; unauth→401)

## Phase 7 — Android MVP ✅

- [x] Firebase auth (email/password) w/ Auth emulator (10.0.2.2 host mapping), shared api-client with token injection
- [x] Auth + Query providers; Expo Router tabs (Home, Search, Library, Profile) + content detail route
- [x] Home rails, Search, Detail (seasons/episodes + similar + add-to-watchlist + record view), Library (watchlist/history)
- [x] Profile: sign in / sign up / sign out + push-notification foundation (permission + token via expo-notifications)
- [x] Validated: **Metro bundle succeeds** (`expo export` → 1124 modules → Hermes bundle); all imports resolve
- Known limitation: on-device render + jest-expo/Detox tests need an Android emulator (deferred to Phase 9); Google sign-in on mobile deferred (needs expo-auth-session)

## Phase 8 — Authorized Media Playback ⏳ (deferred pipeline; Mux)

## Phase 9 — Hardening ✅

- [x] Security headers middleware (nosniff, DENY, no-referrer) + per-IP rate limiting (429) with tests
- [x] Storage security-rules tests (public read, deny writes, originals hidden) — `test:rules` now runs Firestore + Storage (11/11 pass)
- [x] Security review + threat summary (STRIDE-lite) → `docs/SECURITY.md`
- [x] Dependency audit: patched Next.js to 14.2.35 (runtime advisory, non-breaking); remaining findings are Expo/firebase-tools build-tooling transitive — scheduled for Phase 10 upgrade
- [x] Cost & scaling review → `docs/COSTS.md`
- [x] Validated: backend 40 passed / 4 skipped, ruff clean; web build + lint clean; 11 rules tests
- Deferred to Phase 10 / follow-up: App Check, Redis-backed rate limiter, isolated API venv, mobile on-device + jest-expo/Detox tests, major dep upgrades (Expo 57 / Next 16)

## Phase 10 — Deployment 🚧 (prep complete; cloud provisioning needs your credentials)

- [x] API production container: `services/api/Dockerfile` (gunicorn + uvicorn workers, non-root, `$PORT`) + `.dockerignore`
- [x] Runtime/dev requirements split (`requirements.txt` / `requirements-dev.txt`)
- [x] CI pipeline: api (lint+test), rules (Firestore+Storage emulator), web (format+lint+build), mobile (Metro bundle)
- [x] Deploy workflows: staging (auto) + production (manual, environment-gated) for Firebase rules/indexes
- [x] Hosting configs: `render.yaml` (free API), `apps/web/vercel.json`, `apps/mobile/eas.json`
- [x] `docs/DEPLOYMENT.md` runbook (provisioning, per-component deploy, monitoring, rollback, secrets checklist)
- [x] Validated: Docker image builds + runs (gunicorn serving /health, security headers); all CI/deploy YAML + JSON parse
- [ ] **(you)** create staging/prod Firebase projects, set GitHub secrets, provision Render/Vercel/EAS, enable Blaze + budget alerts

## Phase 11 — Post-MVP ⏳

## Phase 11 — Post-MVP ⏳
