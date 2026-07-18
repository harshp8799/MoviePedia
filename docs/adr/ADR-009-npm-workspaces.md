# ADR-009: npm workspaces; no Turborepo/Nx in MVP

**Status:** Accepted · 2026-07-18

## Context

The monorepo has web, mobile, and shared JS packages. Build orchestrators (Turborepo/Nx) add tooling
and config overhead not justified at MVP scale, and pnpm's symlinked layout can break Expo/Metro.

## Decision

Use built-in **npm workspaces**. Python service is managed separately via its own venv +
`requirements.txt`.

## Consequences

- ➕ Zero extra tooling; Metro/Expo-friendly node_modules layout.
- ➖ No cached task graph; fine at current size, revisit only if build times hurt.
