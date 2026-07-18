import Listing from '../../../components/Listing';

export const dynamic = 'force-dynamic';
export const metadata = { title: 'Series' };

export default function SeriesPage({ searchParams }) {
  return <Listing type="series" searchParams={searchParams} />;
}
