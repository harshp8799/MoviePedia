'use client';

import Link from 'next/link';

import { useAuth } from '../providers/AuthProvider';

// Public site header: nav, no-JS search form, and auth-aware account controls.
export default function Nav() {
  const { user, signOut, loading } = useAuth();

  return (
    <header className="sticky top-0 z-10 border-b border-border bg-bg/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3">
        <Link href="/" className="text-lg font-bold text-primary">
          Movie Pedia
        </Link>
        <nav className="flex gap-3 text-sm text-muted">
          <Link href="/movies" className="hover:text-text">
            Movies
          </Link>
          <Link href="/series" className="hover:text-text">
            Series
          </Link>
          {user && (
            <>
              <Link href="/library" className="hover:text-text">
                Library
              </Link>
              <Link href="/history" className="hover:text-text">
                History
              </Link>
            </>
          )}
        </nav>
        <form action="/search" className="ml-auto">
          <input
            type="search"
            name="q"
            placeholder="Search…"
            aria-label="Search titles"
            className="w-32 rounded bg-surface px-3 py-1.5 text-sm outline-none ring-1 ring-border focus:w-48 focus:ring-primary sm:w-48"
          />
        </form>
        {!loading &&
          (user ? (
            <button onClick={signOut} className="rounded bg-surfaceAlt px-3 py-1.5 text-sm">
              Sign out
            </button>
          ) : (
            <Link href="/login" className="rounded bg-primary px-3 py-1.5 text-sm font-semibold">
              Sign in
            </Link>
          ))}
      </div>
    </header>
  );
}
