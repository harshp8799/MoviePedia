'use client';

// Firebase Web SDK init for the admin app. Connects to the Auth emulator locally (free);
// point at a real project by setting NEXT_PUBLIC_FIREBASE_* and NEXT_PUBLIC_USE_FIREBASE_EMULATOR=false.

import { getApp, getApps, initializeApp } from 'firebase/app';
import { connectAuthEmulator, getAuth } from 'firebase/auth';

const config = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || 'demo-key',
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || 'movie-pedia-local.firebaseapp.com',
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || 'movie-pedia-local',
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || 'demo-app',
};

export const firebaseApp = getApps().length ? getApp() : initializeApp(config);
export const auth = getAuth(firebaseApp);

const useEmulator = process.env.NEXT_PUBLIC_USE_FIREBASE_EMULATOR !== 'false';
if (useEmulator && typeof window !== 'undefined' && !globalThis.__mpAuthEmulator) {
  try {
    connectAuthEmulator(auth, 'http://localhost:9099', { disableWarnings: true });
    globalThis.__mpAuthEmulator = true;
  } catch {
    // already connected (hot reload) — ignore
  }
}
