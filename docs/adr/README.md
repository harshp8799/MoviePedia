# Architecture Decision Records

Short, immutable records of significant decisions. Format: Context → Decision → Consequences.

| ADR | Title                                                                        | Status   |
| --- | ---------------------------------------------------------------------------- | -------- |
| 001 | Modular monolith over microservices                                          | Accepted |
| 002 | Clean Architecture / Ports & Adapters (pragmatic)                            | Accepted |
| 003 | FastAPI is the write/authz authority; clients read only published + own data | Accepted |
| 004 | Single `content` collection with `type` discriminator                        | Accepted |
| 005 | Firestore-native search behind `SearchPort` for MVP                          | Accepted |
| 006 | No in-house transcoding in MVP; signed authorized URLs only                  | Accepted |
| 007 | Separate Firebase project per environment                                    | Accepted |
| 008 | JavaScript-only + Zod/JSDoc guardrails instead of TypeScript                 | Accepted |
| 009 | npm workspaces; no Turborepo/Nx in MVP                                       | Accepted |
