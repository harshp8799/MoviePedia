import Link from 'next/link';

import { apiGet } from '../lib/publicApi';
import ContentCard from './ContentCard';

const SORTS = [
  ['popularity', 'Popular'],
  ['trending', 'Trending'],
  ['recent', 'Recently added'],
  ['release', 'Newest'],
];

// Shared listing page for /movies and /series: sort + genre filters, responsive grid.
export default async function Listing({ type, searchParams }) {
  const path = type === 'series' ? 'series' : 'movies';
  const sort = SORTS.some((s) => s[0] === searchParams?.sort) ? searchParams.sort : 'popularity';
  const genre = searchParams?.genre || '';

  const params = new URLSearchParams({ sort, limit: '24' });
  if (genre) params.set('genre', genre);

  let data;
  let genres;
  try {
    [data, genres] = await Promise.all([apiGet(`/${path}?${params}`), apiGet('/genres')]);
  } catch {
    return <p className="text-muted">Catalog unavailable. Is the API running?</p>;
  }

  const linkTo = (nextSort, nextGenre) => {
    const p = new URLSearchParams({ sort: nextSort });
    if (nextGenre) p.set('genre', nextGenre);
    return `/${path}?${p}`;
  };

  return (
    <div>
      <h1 className="mb-4 text-2xl font-bold capitalize">{path}</h1>

      <div className="mb-3 flex flex-wrap gap-2 text-sm">
        {SORTS.map(([value, label]) => (
          <Link
            key={value}
            href={linkTo(value, genre)}
            className={`rounded px-3 py-1 ${sort === value ? 'bg-primary' : 'bg-surface'}`}
          >
            {label}
          </Link>
        ))}
      </div>

      <div className="mb-6 flex flex-wrap gap-2 text-xs">
        <Link
          href={linkTo(sort, '')}
          className={`rounded px-2 py-1 ${!genre ? 'bg-primary' : 'bg-surfaceAlt'}`}
        >
          All
        </Link>
        {(genres?.items || []).map((g) => (
          <Link
            key={g.id}
            href={linkTo(sort, g.id)}
            className={`rounded px-2 py-1 ${genre === g.id ? 'bg-primary' : 'bg-surfaceAlt'}`}
          >
            {g.name}
          </Link>
        ))}
      </div>

      {data.items.length === 0 ? (
        <p className="text-muted">No titles found.</p>
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 md:grid-cols-6">
          {data.items.map((item) => (
            <ContentCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}
