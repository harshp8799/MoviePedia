#!/usr/bin/env node
// Seed sample catalog + demo admin into the Firebase EMULATOR (never production).
// Full implementation lands in Phase 3 (needs Firestore collections + Admin SDK wiring).
// Usage: node scripts/seed.mjs

const host = process.env.FIRESTORE_EMULATOR_HOST || 'localhost:8080';
console.log(`[seed] target emulator: ${host}`);
console.log('[seed] Not implemented yet — wired in Phase 3 (Firebase Foundation).');
console.log('[seed] Will insert: genres, sample movies/series, demo admin & editor accounts.');
process.exit(0);
