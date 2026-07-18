# Movie Pedia

A legally-operated movie & TV-series catalog platform: public web app (Next.js), Android app
(Expo React Native), and a secure Python (FastAPI) backend over Firebase (Auth, Firestore,
Storage, FCM).

> **Architecture:** Modular monolith backend with Clean Architecture / Ports & Adapters.
> FastAPI is the authority for all writes and sensitive reads; clients read only _published_
> catalog + their own data directly from Firestore. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Monorepo layout

```
apps/web         Next.js App Router (JS/JSX, Tailwind) — public + user + admin
apps/mobile      Expo React Native (JS, Expo Router) — Android-first
services/api      FastAPI (Clean Architecture) — the write/authz authority
packages/*        api-client, shared-config, design-tokens, shared-utils (shared JS)
firebase/        Firestore/Storage rules, indexes, emulator config
scripts/         seed, reset-dev-data, set-admin-claims (zsh/node)
docs/            architecture dossier + ADRs
```

## Prerequisites

- Node.js >= 20 (tested on 22)
- Python 3.12
- Firebase CLI (`npm i -g firebase-tools`) — for the Emulator Suite
- macOS/Linux shell (zsh/bash)

## Local setup (free — runs entirely on Firebase Emulator Suite)

```bash
# 1. Install JS workspace deps
npm install

# 2. Backend deps (uses the repo .venv). Use requirements-dev.txt for tests/lint.
.venv/bin/pip install -r services/api/requirements-dev.txt

# 3. Environment
cp .env.example .env        # fill in / keep emulator defaults

# 4. Start Firebase emulators (Auth + Firestore + Storage + UI)
npm run emulators

# 5. Backend API  (new terminal)
cd services/api && ../../.venv/bin/uvicorn app.main:app --reload --port 8000
#   -> http://localhost:8000/api/v1/health   ·   docs at /docs

# 6. Web  (new terminal)
npm run dev:web             # -> http://localhost:3000

# 7. Mobile  (new terminal)
npm run dev:mobile          # Expo — press 'a' for Android
```

## Security notes

- Never commit `.env`, service-account JSON, or signing credentials (see `.gitignore`).
- Admin actions are authorized by the FastAPI backend, not by frontend route guards alone.
- Each environment (local/dev/staging/prod) uses a **separate Firebase project**.

## Status

MVP under construction — see [`TASKS.md`](TASKS.md) for live phase progress.
