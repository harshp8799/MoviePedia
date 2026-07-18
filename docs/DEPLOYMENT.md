# Deployment Runbook

Everything in this repo is validated locally on the free emulator. This runbook covers taking it
to real environments. Steps marked **(you)** need your accounts/credentials and are run
interactively (in Claude Code, prefix with `!` to run in-session).

## Environments

| Env        | Firebase project               | Web                 | API              | Notes                                                   |
| ---------- | ------------------------------ | ------------------- | ---------------- | ------------------------------------------------------- |
| local      | `movie-pedia-local` (emulator) | `localhost:3000`    | `localhost:8000` | $0, no cloud                                            |
| staging    | `movie-pedia-staging`          | Vercel preview/prod | Render/Cloud Run | Auth + Firestore free on Spark; **Storage needs Blaze** |
| production | `movie-pedia-prod`             | Vercel prod         | Render/Cloud Run | enable **budget alerts** before Blaze                   |

Never share one Firebase project across environments (ADR-007). Aliases live in `.firebaserc`.

## 1. One-time provisioning (you)

1. **Create the Firebase projects** (staging, prod) in the console. Enable **Authentication →
   Email/Password + Google**. Create a Cloud Firestore database (production mode).
2. **Service account** for the API: Project settings → Service accounts → Generate key. Store the
   JSON as a secret (Render Secret File / Cloud Run Secret Manager). **Never commit it.**
3. **First admin**: create a user, then grant the role:
   ```
   ! GOOGLE_APPLICATION_CREDENTIALS=/path/sa.json FIREBASE_PROJECT_ID=movie-pedia-staging \
       .venv/bin/python scripts/set_admin_claims.py you@example.com admin
   ```
4. **GitHub deploy secrets** (repo → Settings): `FIREBASE_TOKEN` (from `npx firebase-tools login:ci`),
   and environment vars `FIREBASE_STAGING_PROJECT`, `FIREBASE_PROD_PROJECT`. Configure
   **Environments → production** with a required reviewer (gates prod deploys).

## 2. Firestore & Storage rules + indexes

Deployed by CI:

- **Staging**: auto on push to `main` (`.github/workflows/deploy-staging.yml`).
- **Production**: manual `workflow_dispatch` (`deploy-production.yml`), requires approval.

Manual equivalent **(you)**:

```
! npx firebase-tools deploy --only firestore:rules,firestore:indexes,storage --project movie-pedia-staging
```

Composite indexes build asynchronously; the first queries needing a new index may 400 until it's ready.

## 3. API (Render free — recommended $0, or Cloud Run)

**Render** (`render.yaml` blueprint): New → Blueprint → point at this repo. Set env in the dashboard:
`FIREBASE_ADMIN_PROJECT_ID`, `FIREBASE_STORAGE_BUCKET`, `API_CORS_ORIGINS`
(your web origin), and upload the SA JSON as a **Secret File**, setting
`GOOGLE_APPLICATION_CREDENTIALS` to its path. Health check: `/api/v1/health`.

**Cloud Run** alternative (needs Blaze):

```
! gcloud run deploy moviepedia-api --source services/api --region <r> \
    --set-env-vars USE_FIREBASE_EMULATOR=false,FIREBASE_ADMIN_PROJECT_ID=<proj> --allow-unauthenticated
```

Container is validated: `docker build -t api services/api && docker run -p 8098:8080 api` serves health.

## 4. Web (Vercel Hobby — free)

Import the repo in Vercel. **Root Directory = `apps/web`**; Install Command `npm install` (run at repo
root for workspaces). Set env vars: `NEXT_PUBLIC_FIREBASE_*` (from the Firebase web app config),
`NEXT_PUBLIC_API_BASE_URL` (your API URL), `NEXT_PUBLIC_USE_FIREBASE_EMULATOR=false`. Vercel
auto-deploys on push to `main`.

## 5. Android (EAS Build)

`eas.json` defines development/preview/production profiles.

```
! npx eas-cli build --platform android --profile preview    # internal APK
! npx eas-cli build --platform android --profile production  # AAB for Play
```

Set `EXPO_PUBLIC_API_BASE_URL` + `EXPO_PUBLIC_FIREBASE_*` as EAS env/secrets. Push tokens need an
EAS `projectId`. Submit to Play via `eas submit` (internal → closed → production tracks).

## 6. Monitoring & health

- API liveness `/api/v1/health`, readiness `/api/v1/ready` (checks Firestore). Wire host health checks
  to `/health`. Structured JSON logs include request id, route, status, duration.
- Add error monitoring (e.g. Sentry) and a Firestore usage/budget alert before launch.

## 7. Rollback

- **Web**: Vercel → Deployments → promote the previous deployment (instant).
- **API (Render)**: Rollback to the prior deploy; **(Cloud Run)** route traffic to the previous revision.
- **Rules/indexes**: `git revert` the change and re-run the deploy workflow (rules are versioned here).
- **Android**: halt rollout / roll back in the Play Console; ship a patched build.
- **Data**: schedule Firestore exports before risky migrations; restore from export if needed.

## Secrets checklist (never commit)

Service-account JSON · `FIREBASE_TOKEN` · `.env` files · Android keystore/signing · any API keys.
All covered by `.gitignore`; deploy secrets live in Render/Vercel/EAS/GitHub secret stores.
