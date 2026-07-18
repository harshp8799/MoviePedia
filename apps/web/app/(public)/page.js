import Rail from '../../components/Rail';
import { apiGet } from '../../lib/publicApi';

export const dynamic = 'force-dynamic';

export const metadata = {
  description: 'Browse trending, popular, and recently added movies and TV series on Movie Pedia.',
};

export default async function HomePage() {
  let home;
  try {
    home = await apiGet('/home');
  } catch {
    home = null;
  }

  if (!home) {
    return (
      <p className="text-muted">
        Catalog unavailable. Start the API and run <code>npm run seed</code>.
      </p>
    );
  }

  return (
    <div>
      {home.sections.map((section) => (
        <Rail key={section.key} title={section.title} items={section.items} />
      ))}
    </div>
  );
}
