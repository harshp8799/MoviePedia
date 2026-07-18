// Firebase init for the Expo app. Uses a namespace import for firebase/auth so RN builds don't
// break on optional exports (getReactNativePersistence), and connects to the Auth emulator by
// default. On the Android emulator, host localhost is reachable as 10.0.2.2.

import { getApp, getApps, initializeApp } from 'firebase/app';
import * as fbAuth from 'firebase/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';

const config = {
  apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY || 'demo-key',
  authDomain: 'movie-pedia-local.firebaseapp.com',
  projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID || 'movie-pedia-local',
  appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID || 'demo-app',
};

const app = getApps().length ? getApp() : initializeApp(config);

function makeAuth() {
  if (typeof fbAuth.getReactNativePersistence === 'function') {
    try {
      return fbAuth.initializeAuth(app, {
        persistence: fbAuth.getReactNativePersistence(AsyncStorage),
      });
    } catch {
      // already initialized on fast refresh
    }
  }
  return fbAuth.getAuth(app);
}

export const auth = makeAuth();

const useEmulator = process.env.EXPO_PUBLIC_USE_FIREBASE_EMULATOR !== 'false';
const authEmulatorUrl = process.env.EXPO_PUBLIC_AUTH_EMULATOR_URL || 'http://10.0.2.2:9099';
if (useEmulator && !globalThis.__mpAuthEmu) {
  try {
    fbAuth.connectAuthEmulator(auth, authEmulatorUrl, { disableWarnings: true });
    globalThis.__mpAuthEmu = true;
  } catch {
    // already connected
  }
}

export { fbAuth };
