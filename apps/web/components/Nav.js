import Link from 'next/link';

// Public site header with primary nav and a no-JS search form.
export default function Nav() {
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
        </nav>
        <form action="/search" className="ml-auto">
          <input
            type="search"
            name="q"
            placeholder="Search…"
            aria-label="Search titles"
            className="w-40 rounded bg-surface px-3 py-1.5 text-sm outline-none ring-1 ring-border focus:w-56 focus:ring-primary sm:w-56"
          />
        </form>
      </div>
    </header>
  );
}
