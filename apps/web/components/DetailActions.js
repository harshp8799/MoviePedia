'use client';

import { useEffect, useState } from 'react';

import Link from 'next/link';

import { useAddToList, useRecordView, useRemoveFromList } from '../features/library/hooks';
import { useAuth } from '../providers/AuthProvider';

// Client actions on a detail page: watchlist/favorite toggles + record a view for history.
export default function DetailActions({ contentId }) {
  const { user, loading } = useAuth();
  const [inWatchlist, setInWatchlist] = useState(false);
  const [favorited, setFavorited] = useState(false);

  const addWatch = useAddToList('watchlist');
  const removeWatch = useRemoveFromList('watchlist');
  const addFav = useAddToList('favorites');
  const removeFav = useRemoveFromList('favorites');
  const recordView = useRecordView();

  useEffect(() => {
    if (user) recordView.mutate(contentId);
    // record a view once per mount when authenticated
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, contentId]);

  if (loading) return null;
  if (!user) {
    return (
      <Link href="/login" className="mt-4 inline-block text-sm text-primary hover:underline">
        Sign in to save &amp; track →
      </Link>
    );
  }

  const toggleWatch = () => {
    if (inWatchlist) removeWatch.mutate(contentId);
    else addWatch.mutate(contentId);
    setInWatchlist((v) => !v);
  };
  const toggleFav = () => {
    if (favorited) removeFav.mutate(contentId);
    else addFav.mutate(contentId);
    setFavorited((v) => !v);
  };

  return (
    <div className="mt-4 flex gap-2">
      <button onClick={toggleWatch} className="rounded bg-primary px-4 py-2 text-sm font-semibold">
        {inWatchlist ? 'In Watchlist ✓' : '+ Watchlist'}
      </button>
      <button onClick={toggleFav} className="rounded bg-surfaceAlt px-4 py-2 text-sm">
        {favorited ? '★ Favorited' : '☆ Favorite'}
      </button>
    </div>
  );
}
