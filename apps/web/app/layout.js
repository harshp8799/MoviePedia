import './globals.css';

export const metadata = {
  title: {
    default: 'Movie Pedia',
    template: '%s · Movie Pedia',
  },
  description: 'Browse movies and TV series on Movie Pedia.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-bg text-text antialiased">{children}</body>
    </html>
  );
}
