import ContentCard from '../../../components/ContentCard';
import { apiGet } from '../../../lib/publicApi';

export const dynamic = 'force-dynamic';
export const metadata = { title: 'Search' };

export default async function SearchPage({ searchParams }) {
  const q = (searchParams?.q || '').trim();
  let data = null;
  if (q) {
    try {
      data = await apiGet(`/search?q=${encodeURIComponent(q)}`);
    } catch {
      data = { items: [] };
    }
  }

  return (
    <div>
      <h1 className="mb-4 text-2xl font-bold">Search</h1>
      <form action="/search" className="mb-6">
        <input
          type="search"
          name="q"
          defaultValue={q}
          placeholder="Search movies & series"
          aria-label="Search titles"
          className="w-full max-w-md rounded bg-surface px-3 py-2 outline-none ring-1 ring-border focus:ring-primary"
        />
      </form>

      {!q && <p className="text-muted">Type a query above to search the catalog.</p>}
      {q && data && data.items.length === 0 && <p className="text-muted">No results for “{q}”.</p>}
      {data && data.items.length > 0 && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 md:grid-cols-6">
          {data.items.map((item) => (
            <ContentCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}
