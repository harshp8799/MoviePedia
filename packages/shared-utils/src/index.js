// Pure, dependency-free formatting/domain helpers shared by web + mobile.

/** Convert a title to a URL-safe slug. Mirror of the backend slug rule. */
export function slugify(input) {
  return String(input)
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '') // strip accents
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80);
}

/** Generate capped prefix search tokens for Firestore-native search (see ADR-005). */
export function buildSearchTokens(title, keywords = [], maxPrefix = 8) {
  const words = `${title} ${keywords.join(' ')}`
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
  const tokens = new Set();
  for (const w of words) {
    for (let i = 1; i <= Math.min(w.length, maxPrefix); i++) {
      tokens.add(w.slice(0, i));
    }
  }
  return Array.from(tokens);
}

/** Format minutes as "2h 3m" / "48m". */
export function formatDuration(minutes) {
  if (!minutes || minutes < 0) return '';
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

/** Extract a 4-digit year from an ISO date or Date. */
export function releaseYear(dateInput) {
  if (!dateInput) return null;
  const d = dateInput instanceof Date ? dateInput : new Date(dateInput);
  return Number.isNaN(d.getTime()) ? null : d.getUTCFullYear();
}

/** Human-friendly "3 days ago" style relative time. */
export function timeAgo(dateInput, now = new Date()) {
  const d = dateInput instanceof Date ? dateInput : new Date(dateInput);
  const secs = Math.floor((now.getTime() - d.getTime()) / 1000);
  const units = [
    ['year', 31536000],
    ['month', 2592000],
    ['day', 86400],
    ['hour', 3600],
    ['minute', 60],
  ];
  for (const [name, size] of units) {
    const v = Math.floor(secs / size);
    if (v >= 1) return `${v} ${name}${v > 1 ? 's' : ''} ago`;
  }
  return 'just now';
}

/** Playback progress percentage (0–100), clamped. */
export function progressPercent(positionSec, durationSec) {
  if (!durationSec || durationSec <= 0) return 0;
  return Math.max(0, Math.min(100, Math.round((positionSec / durationSec) * 100)));
}
