'use client';

import { useEffect } from 'react';

import { usePathname, useRouter } from 'next/navigation';

import { AuthProvider, useAuth } from '../../providers/AuthProvider';
import { QueryProvider } from '../../providers/QueryProvider';

const ADMIN_ROLES = ['admin', 'editor'];

function Guard({ children }) {
  const { user, role, loading, signOut } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const isLogin = pathname === '/admin/login';

  useEffect(() => {
    if (loading) return;
    if (!user && !isLogin) router.replace('/admin/login');
  }, [user, loading, isLogin, router]);

  if (loading) return <div className="p-8 text-muted">Loading…</div>;
  if (isLogin) return children;
  if (!user) return null;

  if (!ADMIN_ROLES.includes(role)) {
    return (
      <div className="mx-auto max-w-md p-8 text-center">
        <h1 className="mb-2 text-xl font-bold">Not authorized</h1>
        <p className="mb-4 text-muted">
          Your account ({user.email}) has role “{role}”. Admin or editor is required.
        </p>
        <button onClick={signOut} className="rounded bg-surfaceAlt px-4 py-2">
          Sign out
        </button>
      </div>
    );
  }
  return children;
}

export default function AdminLayout({ children }) {
  return (
    <QueryProvider>
      <AuthProvider>
        <Guard>{children}</Guard>
      </AuthProvider>
    </QueryProvider>
  );
}
