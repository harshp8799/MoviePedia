// Shared domain terminology & constants used across web, mobile, and (mirrored in) the API.
// Keep this in lockstep with the backend enums in services/api/app/domain.

/** User roles. Authorization source of truth is the backend; these are for UI hints + validation. */
export const ROLES = Object.freeze({
  ADMIN: 'admin',
  EDITOR: 'editor',
  USER: 'user',
});

/** Content type discriminator (single `content` collection). */
export const CONTENT_TYPES = Object.freeze({
  MOVIE: 'movie',
  SERIES: 'series',
});

/** Publish workflow / visibility. Only `published` is publicly readable. */
export const VISIBILITY = Object.freeze({
  DRAFT: 'draft',
  PUBLISHED: 'published',
  ARCHIVED: 'archived',
});

/** Personal library list types. */
export const LIST_TYPES = Object.freeze({
  WATCHLIST: 'watchlist',
  FAVORITE: 'favorite',
});

/** Media asset kinds. */
export const MEDIA_KINDS = Object.freeze({
  POSTER: 'poster',
  BACKDROP: 'backdrop',
  TRAILER: 'trailer',
  VIDEO: 'video',
  SUBTITLE: 'subtitle',
});

/** Playback source providers (MVP). */
export const PLAYBACK_PROVIDERS = Object.freeze({
  STORAGE: 'storage', // owner clip in Cloud Storage
  EXTERNAL: 'external', // authorized external URL
  HLS: 'hls', // owner-provided HLS manifest
});

/** Processing job status (Phase 8). */
export const JOB_STATUS = Object.freeze({
  QUEUED: 'queued',
  PROCESSING: 'processing',
  READY: 'ready',
  FAILED: 'failed',
});

/** Default pagination page size for cursor-based lists. */
export const DEFAULT_PAGE_SIZE = 24;

/** Upload validation limits (mirror server-side enforcement). */
export const UPLOAD_LIMITS = Object.freeze({
  IMAGE_MAX_BYTES: 5 * 1024 * 1024, // 5 MB
  IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/webp'],
  CLIP_MAX_BYTES: 200 * 1024 * 1024, // 200 MB (small owner clips, MVP)
  CLIP_TYPES: ['video/mp4', 'video/webm'],
});

/** Client-safe env keys (never put server secrets here). */
export const ENV_KEYS = Object.freeze({
  API_BASE_URL: 'API_BASE_URL',
  FIREBASE_PROJECT_ID: 'FIREBASE_PROJECT_ID',
});
