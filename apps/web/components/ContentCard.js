import Link from 'next/link';

// Poster card linking to a movie/series detail page. Server component (pure markup).
export default function ContentCard({ item }) {
  const href = `/${item.type === 'series' ? 'series' : 'movies'}/${item.slug}`;
  return (
    <Link href={href} className="group block w-full">
      <div className="aspect-[2/3] overflow-hidden rounded bg-surface ring-1 ring-border">
        {item.poster?.url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={item.poster.url}
            alt={item.title}
            className="h-full w-full object-cover transition group-hover:scale-105"
            loading="lazy"
          />
        ) : (
          <div className="flex h-full items-center justify-center p-2 text-center text-xs text-muted">
            {item.title}
          </div>
        )}
      </div>
      <div className="mt-2">
        <p className="truncate text-sm font-medium">{item.title}</p>
        <p className="text-xs text-muted">
          {item.releaseYear || '—'} · {item.type}
        </p>
      </div>
    </Link>
  );
}
