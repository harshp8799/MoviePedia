export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col items-center justify-center gap-4 px-6 text-center">
      <span className="rounded-full bg-primary px-3 py-1 text-sm font-semibold">Phase 2</span>
      <h1 className="text-4xl font-bold">Movie Pedia</h1>
      <p className="text-muted">
        Web app bootstrap is live. Catalog, search, and detail pages arrive in Phase 6.
      </p>
      <code className="rounded bg-surface px-3 py-2 text-sm text-muted">
        API: {process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}
      </code>
    </main>
  );
}
