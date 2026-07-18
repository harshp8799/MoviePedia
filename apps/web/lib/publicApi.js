// Server-side fetch helper for public catalog reads. No auth; runs in Server Components.
// Responses are cached/revalidated by Next so public pages stay fast and SEO-friendly.

const BASE =
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  'http://localhost:8000/api/v1';

export async function apiGet(path, { revalidate = 60 } = {}) {
  const res = await fetch(`${BASE}${path}`, { next: { revalidate } });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`API request failed: ${res.status} ${path}`);
  return res.json();
}
