// Storage security-rules tests. Proves: public/ images are world-readable, direct client writes
// are denied everywhere, and non-public paths (originals) are not client-readable (ADR-006).

import { test, before, after } from 'node:test';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import {
  initializeTestEnvironment,
  assertFails,
  assertSucceeds,
} from '@firebase/rules-unit-testing';
import { ref, uploadString, getBytes } from 'firebase/storage';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rulesPath = path.resolve(__dirname, '../storage.rules');

let testEnv;

before(async () => {
  testEnv = await initializeTestEnvironment({
    projectId: 'movie-pedia-local',
    storage: { rules: readFileSync(rulesPath, 'utf8'), host: '127.0.0.1', port: 9199 },
  });
  await testEnv.withSecurityRulesDisabled(async (ctx) => {
    const storage = ctx.storage();
    await uploadString(ref(storage, 'public/posters/p1.jpg'), 'img');
    await uploadString(ref(storage, 'originals/movie1.mp4'), 'video');
  });
});

after(async () => {
  await testEnv.cleanup();
});

test('public images are world-readable', async () => {
  const storage = testEnv.unauthenticatedContext().storage();
  await assertSucceeds(getBytes(ref(storage, 'public/posters/p1.jpg')));
});

test('clients cannot write to public/ (uploads go via signed URLs)', async () => {
  const storage = testEnv.authenticatedContext('userA').storage();
  await assertFails(uploadString(ref(storage, 'public/posters/hack.jpg'), 'x'));
});

test('non-public originals are not client-readable', async () => {
  const storage = testEnv.authenticatedContext('userA').storage();
  await assertFails(getBytes(ref(storage, 'originals/movie1.mp4')));
});

test('clients cannot write outside public/', async () => {
  const storage = testEnv.authenticatedContext('userA').storage();
  await assertFails(uploadString(ref(storage, 'originals/evil.mp4'), 'x'));
});
