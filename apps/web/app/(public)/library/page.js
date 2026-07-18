'use client';

import Link from 'next/link';

import ContentCard from '../../../components/ContentCard';
import { useContinueWatching, useList } from '../../../features/library/hooks';
import { useAuth } from '../../../providers/AuthProvider';

function Grid({ items }) {
  if (!items || items.length === 0) return <p className="text-sm text-muted">Nothing here yet.</p>;
  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 md:grid-cols-6">
      {items.map((item) => (
        <ContentCard key={item.contentId} item={{ ...item, id: item.contentId }} />
      ))}
    </div>
  );
}

export default function LibraryPage() {
  const { user, loading } = useAuth();
  const enabled = !!user;
  const watchlist = useList('watchlist', enabled);
  const favorites = useList('favorites', enabled);
  const continueWatching = useContinueWatching(enabled);

  if (loading) return <p className="text-muted">Loading…</p>;
  if (!user) {
    return (
      <p className="text-muted">
        Please{' '}
        <Link href="/login" className="text-primary hover:underline">
          sign in
        </Link>{' '}
        to view your library.
      </p>
    );
  }

  return (
    <div className="space-y-8">
      <section>
        <h2 className="mb-3 text-lg font-semibold">Continue watching</h2>
        <Grid items={continueWatching.data?.items} />
      </section>
      <section>
        <h2 className="mb-3 text-lg font-semibold">Watchlist</h2>
        <Grid items={watchlist.data?.items} />
      </section>
      <section>
        <h2 className="mb-3 text-lg font-semibold">Favorites</h2>
        <Grid items={favorites.data?.items} />
      </section>
    </div>
  );
}
