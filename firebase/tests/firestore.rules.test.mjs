// Firestore security-rules tests (ADR-003). Run against the emulator via:
//   npm run test:rules   (wraps `firebase emulators:exec`)
// Proves: draft content is hidden, client writes to catalog are denied, and per-user data is
// strictly owner-scoped.

import { test, before, after } from 'node:test';
import assert from 'node:assert';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import {
  initializeTestEnvironment,
  assertFails,
  assertSucceeds,
} from '@firebase/rules-unit-testing';
import { doc, getDoc, setDoc } from 'firebase/firestore';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rulesPath = path.resolve(__dirname, '../firestore.rules');

let testEnv;

before(async () => {
  testEnv = await initializeTestEnvironment({
    projectId: 'movie-pedia-local',
    firestore: { rules: readFileSync(rulesPath, 'utf8') },
  });

  // Seed baseline docs with rules bypassed (simulates the Admin SDK / server).
  await testEnv.withSecurityRulesDisabled(async (ctx) => {
    const db = ctx.firestore();
    await setDoc(doc(db, 'content/pub1'), { visibility: 'published', title: 'Published' });
    await setDoc(doc(db, 'content/draft1'), { visibility: 'draft', title: 'Draft' });
    await setDoc(doc(db, 'genres/action'), { name: 'Action' });
    await setDoc(doc(db, 'user_libraries/userA/items/x'), { listType: 'watchlist' });
  });
});

after(async () => {
  await testEnv.cleanup();
});

test('anyone can read PUBLISHED content', async () => {
  const db = testEnv.unauthenticatedContext().firestore();
  await assertSucceeds(getDoc(doc(db, 'content/pub1')));
});

test('DRAFT content is hidden from the public', async () => {
  const db = testEnv.unauthenticatedContext().firestore();
  await assertFails(getDoc(doc(db, 'content/draft1')));
});

test('clients cannot write to the catalog (server-only)', async () => {
  const db = testEnv.authenticatedContext('userA').firestore();
  await assertFails(setDoc(doc(db, 'content/hack'), { visibility: 'published' }));
});

test('genres are publicly readable but not client-writable', async () => {
  const pub = testEnv.unauthenticatedContext().firestore();
  await assertSucceeds(getDoc(doc(pub, 'genres/action')));
  const authed = testEnv.authenticatedContext('userA').firestore();
  await assertFails(setDoc(doc(authed, 'genres/evil'), { name: 'Evil' }));
});

test('a user can read/write their OWN library', async () => {
  const db = testEnv.authenticatedContext('userA').firestore();
  await assertSucceeds(getDoc(doc(db, 'user_libraries/userA/items/x')));
  await assertSucceeds(setDoc(doc(db, 'user_libraries/userA/items/y'), { listType: 'favorite' }));
});

test("a user CANNOT touch another user's library", async () => {
  const db = testEnv.authenticatedContext('userB').firestore();
  await assertFails(getDoc(doc(db, 'user_libraries/userA/items/x')));
  await assertFails(setDoc(doc(db, 'user_libraries/userA/items/z'), { listType: 'watchlist' }));
});

test('unauthenticated users cannot write library data', async () => {
  const db = testEnv.unauthenticatedContext().firestore();
  await assertFails(setDoc(doc(db, 'user_libraries/userA/items/w'), { listType: 'watchlist' }));
});
