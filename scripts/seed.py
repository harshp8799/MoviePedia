#!/usr/bin/env python3
"""Seed sample catalog + demo accounts into the Firebase EMULATOR (never production).

Reuses the Python firebase-admin SDK already installed for the API. Safety: this script
FORCES the emulator hosts and refuses to run against a real project, so it can never write
to production data.

Usage:
    .venv/bin/python scripts/seed.py            # from repo root, emulators running
"""

from __future__ import annotations

import os
import re
import sys

# ---- Safety: force emulator targets before importing firebase_admin --------
PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "movie-pedia-local")
os.environ.setdefault("FIRESTORE_EMULATOR_HOST", "localhost:8080")
os.environ.setdefault("FIREBASE_AUTH_EMULATOR_HOST", "localhost:9099")
os.environ.setdefault("GCLOUD_PROJECT", PROJECT_ID)

if "prod" in PROJECT_ID or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    print("[seed] Refusing to run: looks like a real/production target. Emulator only.")
    sys.exit(1)

import google.auth.credentials  # noqa: E402
import firebase_admin  # noqa: E402
from firebase_admin import auth, credentials, firestore  # noqa: E402


class _EmulatorCredentials(credentials.Base):
    """Anonymous credential so the Admin SDK never resolves ADC against the emulator."""

    def get_credential(self):
        return google.auth.credentials.AnonymousCredentials()


firebase_admin.initialize_app(_EmulatorCredentials(), {"projectId": PROJECT_ID})
db = firestore.client()
TS = firestore.SERVER_TIMESTAMP


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80]


def search_tokens(title: str, keywords: list[str], max_prefix: int = 8) -> list[str]:
    words = re.sub(r"[^a-z0-9\s]", " ", f"{title} {' '.join(keywords)}".lower()).split()
    out: set[str] = set()
    for w in words:
        for i in range(1, min(len(w), max_prefix) + 1):
            out.add(w[:i])
    return sorted(out)


def content_doc(type_, title, year, genres, visibility="published", **extra):
    return {
        "type": type_,
        "slug": slugify(title),
        "title": title,
        "originalTitle": title,
        "shortDescription": f"{title} — sample seed entry.",
        "fullDescription": f"A longer description for {title}, inserted by the seed script.",
        "releaseYear": year,
        "durationMinutes": extra.get("duration"),
        "ageRating": extra.get("ageRating", "PG-13"),
        "genres": genres,
        "languages": ["en"],
        "countries": ["US"],
        "poster": {"url": f"https://placehold.co/500x750?text={slugify(title)}"},
        "backdrop": {"url": f"https://placehold.co/1280x720?text={slugify(title)}"},
        "visibility": visibility,
        "featured": extra.get("featured", False),
        "trendingScore": extra.get("trendingScore", 50.0),
        "popularity": extra.get("popularity", 100),
        "searchTokens": search_tokens(title, genres),
        "schemaVersion": 1,
        "createdAt": TS,
        "updatedAt": TS,
        "publishedAt": TS if visibility == "published" else None,
        "createdBy": "seed",
        "updatedBy": "seed",
    }


GENRES = ["action", "drama", "comedy", "thriller", "sci-fi", "romance", "horror"]

MOVIES = [
    content_doc("movie", "Neon Horizon", 2024, ["sci-fi", "action"], duration=118, featured=True, trendingScore=92.0, popularity=1500),
    content_doc("movie", "Quiet Harbor", 2023, ["drama", "romance"], duration=104, popularity=800),
    content_doc("movie", "Midnight Circuit", 2025, ["thriller", "action"], duration=131, trendingScore=88.0, popularity=1200),
    # A DRAFT — must be invisible to public reads (verified by rules tests).
    content_doc("movie", "Unreleased Draft", 2026, ["drama"], visibility="draft", popularity=0),
]

SERIES = content_doc("series", "The Long Winter", 2022, ["drama", "thriller"], featured=True, popularity=1100)
SEASONS = [
    {"seasonNumber": 1, "title": "Season 1", "episodeCount": 2},
]
EPISODES = [
    {"episodeNumber": 1, "title": "First Frost", "durationMinutes": 52, "visibility": "published"},
    {"episodeNumber": 2, "title": "Deep Freeze", "durationMinutes": 49, "visibility": "published"},
]

DEMO_USERS = [
    ("admin@moviepedia.test", "Passw0rd!", "admin", "Demo Admin"),
    ("editor@moviepedia.test", "Passw0rd!", "editor", "Demo Editor"),
    ("user@moviepedia.test", "Passw0rd!", "user", "Demo User"),
]


def seed_catalog() -> list[str]:
    for g in GENRES:
        db.collection("genres").document(g).set(
            {"id": g, "name": g.replace("-", " ").title(), "createdAt": TS}
        )

    published_ids: list[str] = []
    for m in MOVIES:
        ref = db.collection("content").document()
        ref.set(m)
        if m["visibility"] == "published":
            published_ids.append(ref.id)

    series_ref = db.collection("content").document()
    series_ref.set(SERIES)
    published_ids.append(series_ref.id)
    for s in SEASONS:
        season_ref = series_ref.collection("seasons").document()
        season_ref.set({**s, "createdAt": TS})
        for e in EPISODES:
            season_ref.collection("episodes").document().set({**e, "createdAt": TS})

    # Curated homepage rail referencing published content by id (batched-get pattern).
    db.collection("homepage_sections").document("featured").set(
        {
            "title": "Featured",
            "rank": 0,
            "contentIds": published_ids[:5],
            "updatedAt": TS,
        }
    )
    return published_ids


def seed_users() -> None:
    for email, password, role, name in DEMO_USERS:
        try:
            user = auth.get_user_by_email(email)
        except auth.UserNotFoundError:
            user = auth.create_user(email=email, password=password, display_name=name)
        auth.set_custom_user_claims(user.uid, {"role": role})
        db.collection("users").document(user.uid).set(
            {"uid": user.uid, "email": email, "displayName": name, "role": role, "createdAt": TS}
        )
        print(f"[seed] user {email} -> role={role} uid={user.uid}")


def main() -> None:
    print(f"[seed] target emulator project={PROJECT_ID} firestore={os.environ['FIRESTORE_EMULATOR_HOST']}")
    ids = seed_catalog()
    seed_users()
    print(f"[seed] done: {len(ids)} published content docs, {len(GENRES)} genres, {len(DEMO_USERS)} users.")


if __name__ == "__main__":
    main()
