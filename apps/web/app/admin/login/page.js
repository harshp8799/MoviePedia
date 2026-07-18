'use client';

import { useEffect, useState } from 'react';

import { useRouter } from 'next/navigation';

import { useAuth } from '../../../providers/AuthProvider';

export default function AdminLogin() {
  const { user, role, signIn } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('admin@moviepedia.test');
  const [password, setPassword] = useState('Passw0rd!');
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (user && ['admin', 'editor'].includes(role)) router.replace('/admin');
  }, [user, role, router]);

  async function onSubmit(e) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await signIn(email, password);
      router.replace('/admin');
    } catch (err) {
      setError(err.code || err.message || 'Sign-in failed');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-sm flex-col justify-center px-6">
      <h1 className="mb-1 text-2xl font-bold">Movie Pedia Admin</h1>
      <p className="mb-6 text-sm text-muted">Sign in with an admin or editor account.</p>
      <form onSubmit={onSubmit} className="flex flex-col gap-3">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="rounded bg-surface px-3 py-2 outline-none ring-1 ring-border focus:ring-primary"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="rounded bg-surface px-3 py-2 outline-none ring-1 ring-border focus:ring-primary"
        />
        {error && <p className="text-sm text-danger">{error}</p>}
        <button
          type="submit"
          disabled={busy}
          className="rounded bg-primary px-4 py-2 font-semibold disabled:opacity-60"
        >
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
      <p className="mt-4 text-xs text-muted">
        Local dev: seed demo accounts with <code>npm run seed</code>.
      </p>
    </div>
  );
}
