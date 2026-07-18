#!/usr/bin/env node
// Reset LOCAL development data by clearing the Firestore emulator.
// SAFETY: refuses to run unless FIRESTORE_EMULATOR_HOST is set (never touches production).
// Full implementation lands in Phase 3.  Usage: node scripts/reset-dev-data.mjs

const host = process.env.FIRESTORE_EMULATOR_HOST;
if (!host) {
  console.error('[reset] Refusing to run: FIRESTORE_EMULATOR_HOST is not set.');
  console.error('[reset] This script only ever clears the local emulator, never production.');
  process.exit(1);
}
console.log(`[reset] Would clear emulator data at ${host}. Not implemented yet — Phase 3.`);
process.exit(0);
