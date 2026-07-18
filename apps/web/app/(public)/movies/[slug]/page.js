import { notFound } from 'next/navigation';

import DetailView from '../../../../components/DetailView';
import { apiGet } from '../../../../lib/publicApi';

export const dynamic = 'force-dynamic';

const getMovie = (slug) => apiGet(`/movies/${slug}`);

export async function generateMetadata({ params }) {
  const item = await getMovie(params.slug);
  if (!item) return { title: 'Not found' };
  return {
    title: item.title,
    description: item.shortDescription || undefined,
    openGraph: {
      title: item.title,
      description: item.shortDescription || undefined,
      images: item.backdrop?.url ? [item.backdrop.url] : [],
    },
  };
}

export default async function MovieDetailPage({ params }) {
  const item = await getMovie(params.slug);
  if (!item) notFound();
  return <DetailView item={item} />;
}
