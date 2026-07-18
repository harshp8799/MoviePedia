import Nav from '../../components/Nav';
import PublicProviders from '../../components/PublicProviders';

export default function PublicLayout({ children }) {
  return (
    <PublicProviders>
      <Nav />
      <main className="mx-auto max-w-6xl px-4 py-6">{children}</main>
    </PublicProviders>
  );
}
