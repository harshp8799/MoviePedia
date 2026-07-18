'use client';

// Single API client for the web app — injects a fresh Firebase ID token on authed calls.

import { createApiClient } from '@moviepedia/api-client';

import { auth } from './firebase';

export const api = createApiClient({
  baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1',
  getToken: async () => (auth.currentUser ? auth.currentUser.getIdToken() : null),
});
