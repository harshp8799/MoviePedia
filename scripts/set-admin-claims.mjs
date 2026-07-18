#!/usr/bin/env node
// Grant a role (admin|editor|user) to a user via Firebase custom claims (Admin SDK).
// Roles are the authorization source of truth (ADR-003). Full implementation lands in Phase 4.
// Usage: node scripts/set-admin-claims.mjs <uid> <role>

const [, , uid, role] = process.argv;
const ROLES = ['admin', 'editor', 'user'];

if (!uid || !ROLES.includes(role)) {
  console.error('Usage: node scripts/set-admin-claims.mjs <uid> <admin|editor|user>');
  process.exit(1);
}
console.log(`[claims] Would set role="${role}" on uid="${uid}". Not implemented yet — Phase 4.`);
process.exit(0);
