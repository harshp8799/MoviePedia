import DetailActions from './DetailActions';
import Rail from './Rail';

// Shared detail view for movies & series. For series, renders seasons + episodes.
export default function DetailView({ item }) {
  return (
    <article>
      {item.backdrop?.url && (
        <div className="mb-6 aspect-video overflow-hidden rounded">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={item.backdrop.url} alt="" className="h-full w-full object-cover" />
        </div>
      )}

      <div className="flex flex-col gap-6 sm:flex-row">
        {item.poster?.url && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={item.poster.url} alt={item.title} className="w-40 shrink-0 rounded" />
        )}
        <div>
          <h1 className="text-3xl font-bold">{item.title}</h1>
          <p className="mt-1 text-sm text-muted">
            {item.releaseYear || '—'} · {item.ageRating || 'NR'}
            {item.durationMinutes ? ` · ${item.durationMinutes}m` : ''}
          </p>
          <div className="mt-2 flex flex-wrap gap-2">
            {(item.genres || []).map((g) => (
              <span key={g} className="rounded bg-surfaceAlt px-2 py-0.5 text-xs">
                {g}
              </span>
            ))}
          </div>
          <p className="mt-4 max-w-2xl text-muted">
            {item.fullDescription || item.shortDescription}
          </p>
          <DetailActions contentId={item.id} />
        </div>
      </div>

      {item.seasons && item.seasons.length > 0 && (
        <section className="mt-8">
          <h2 className="mb-3 text-lg font-semibold">Episodes</h2>
          {item.seasons.map((season) => (
            <div key={season.id} className="mb-4">
              <h3 className="mb-2 font-medium">{season.title}</h3>
              <ul className="space-y-1 text-sm">
                {(season.episodes || []).map((ep) => (
                  <li key={ep.id} className="rounded bg-surface px-3 py-2">
                    {ep.episodeNumber}. {ep.title}
                    {ep.durationMinutes ? ` · ${ep.durationMinutes}m` : ''}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </section>
      )}

      {item.similar && item.similar.length > 0 && (
        <div className="mt-10">
          <Rail title="More like this" items={item.similar} />
        </div>
      )}
    </article>
  );
}
