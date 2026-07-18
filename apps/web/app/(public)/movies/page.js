import Listing from '../../../components/Listing';

export const dynamic = 'force-dynamic';
export const metadata = { title: 'Movies' };

export default function MoviesPage({ searchParams }) {
  return <Listing type="movie" searchParams={searchParams} />;
}
