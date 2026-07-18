// Shared API client for the mobile app — injects the Firebase ID token on authed calls.
// Default base URL targets the Android emulator's host mapping (10.0.2.2 -> host localhost).

import { createApiClient } from '@moviepedia/api-client';

import { auth } from './firebase';

const baseUrl = process.env.EXPO_PUBLIC_API_BASE_URL || 'http://10.0.2.2:8000/api/v1';

export const api = createApiClient({
  baseUrl,
  getToken: async () => (auth.currentUser ? auth.currentUser.getIdToken() : null),
});
