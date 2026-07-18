// Zod schemas — runtime type safety at the API boundary (ADR-008: JS-only + Zod guardrails).
// These mirror the backend Pydantic response schemas. Kept minimal for Phase 2; expanded per feature.

import { z } from 'zod';
import { CONTENT_TYPES, VISIBILITY } from '@moviepedia/shared-config';

export const imageRefSchema = z.object({
  assetId: z.string().optional(),
  url: z.string().url().or(z.string()).optional(),
  w: z.number().optional(),
  h: z.number().optional(),
});

export const contentSummarySchema = z.object({
  id: z.string(),
  type: z.enum([CONTENT_TYPES.MOVIE, CONTENT_TYPES.SERIES]),
  slug: z.string(),
  title: z.string(),
  releaseYear: z.number().nullable().optional(),
  poster: imageRefSchema.nullable().optional(),
  genres: z.array(z.string()).default([]),
});

export const contentDetailSchema = contentSummarySchema.extend({
  originalTitle: z.string().optional(),
  shortDescription: z.string().optional(),
  fullDescription: z.string().optional(),
  releaseDate: z.string().optional(),
  durationMinutes: z.number().nullable().optional(),
  ageRating: z.string().optional(),
  languages: z.array(z.string()).default([]),
  countries: z.array(z.string()).default([]),
  backdrop: imageRefSchema.nullable().optional(),
  visibility: z.enum([VISIBILITY.DRAFT, VISIBILITY.PUBLISHED, VISIBILITY.ARCHIVED]),
});

/** Cursor-paginated list envelope. */
export const paginatedSchema = (itemSchema) =>
  z.object({
    items: z.array(itemSchema),
    nextCursor: z.string().nullable().optional(),
  });

/** Consistent error envelope from the API. */
export const apiErrorSchema = z.object({
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.unknown().optional(),
  }),
});
