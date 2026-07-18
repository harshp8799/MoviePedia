'use client';

import { useEffect, useState } from 'react';

import { useRouter } from 'next/navigation';

import { useAuth } from '../../../providers/AuthProvider';

export default function LoginPage() {
  const { user, signIn, signUp, signInWithGoogle } = useAuth();
  const router = useRouter();
  const [mode, setMode] = useState('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (user) router.replace('/');
  }, [user, router]);

  async function submit(e) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (mode === 'signin') await signIn(email, password);
      else await signUp(email, password);
      router.replace('/');
    } catch (err) {
      setError(err.code || err.message || 'Authentication failed');
    } finally {
      setBusy(false);
    }
  }

  async function google() {
    setError(null);
    try {
      await signInWithGoogle();
      router.replace('/');
    } catch (err) {
      setError(err.code || err.message || 'Google sign-in failed');
    }
  }

  return (
    <div className="mx-auto max-w-sm">
      <h1 className="mb-1 text-2xl font-bold">
        {mode === 'signin' ? 'Sign in' : 'Create account'}
      </h1>
      <p className="mb-6 text-sm text-muted">Save titles to your watchlist and track history.</p>

      <form onSubmit={submit} className="flex flex-col gap-3">
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
          {busy ? 'Please wait…' : mode === 'signin' ? 'Sign in' : 'Sign up'}
        </button>
      </form>

      <button onClick={google} className="mt-3 w-full rounded bg-surfaceAlt px-4 py-2 text-sm">
        Continue with Google
      </button>

      <button
        onClick={() => setMode((m) => (m === 'signin' ? 'signup' : 'signin'))}
        className="mt-4 text-sm text-muted hover:text-text"
      >
        {mode === 'signin' ? 'No account? Sign up' : 'Have an account? Sign in'}
      </button>
    </div>
  );
}
