'use client';

import Link from 'next/link';

import ContentCard from '../../../components/ContentCard';
import { useHistory } from '../../../features/library/hooks';
import { useAuth } from '../../../providers/AuthProvider';

export default function HistoryPage() {
  const { user, loading } = useAuth();
  const history = useHistory(!!user);

  if (loading) return <p className="text-muted">Loading…</p>;
  if (!user) {
    return (
      <p className="text-muted">
        Please{' '}
        <Link href="/login" className="text-primary hover:underline">
          sign in
        </Link>{' '}
        to view your history.
      </p>
    );
  }

  const items = history.data?.items || [];

  return (
    <div>
      <h1 className="mb-4 text-2xl font-bold">Recently viewed</h1>
      {items.length === 0 ? (
        <p className="text-sm text-muted">No viewing history yet.</p>
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 md:grid-cols-6">
          {items.map((item) => (
            <ContentCard key={item.contentId} item={{ ...item, id: item.contentId }} />
          ))}
        </div>
      )}
    </div>
  );
}
