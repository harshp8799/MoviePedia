import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import { auth, fbAuth } from '../lib/firebase';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    return fbAuth.onAuthStateChanged(auth, (u) => {
      setUser(u);
      setLoading(false);
    });
  }, []);

  const value = useMemo(
    () => ({
      user,
      loading,
      signIn: (email, password) => fbAuth.signInWithEmailAndPassword(auth, email, password),
      signUp: (email, password) => fbAuth.createUserWithEmailAndPassword(auth, email, password),
      signOut: () => fbAuth.signOut(auth),
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
