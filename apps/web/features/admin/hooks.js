'use client';

// Admin data hooks — all requests are authenticated and go through the shared API client.

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '../../lib/apiClient';

const authed = { auth: true };

export function useCatalog() {
  return useQuery({
    queryKey: ['catalog'],
    queryFn: () => api.get('/admin/catalog', authed),
  });
}

export function useGenres() {
  return useQuery({ queryKey: ['genres'], queryFn: () => api.get('/admin/genres', authed) });
}

export function useAuditLogs(enabled) {
  return useQuery({
    queryKey: ['audit'],
    enabled,
    queryFn: () => api.get('/admin/audit-logs', authed),
  });
}

function useInvalidating(mutationFn, keys = ['catalog']) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn,
    onSuccess: () => keys.forEach((k) => qc.invalidateQueries({ queryKey: [k] })),
  });
}

export function useCreateContent() {
  return useInvalidating(({ type, ...body }) =>
    api.post(type === 'series' ? '/admin/series' : '/admin/movies', body, authed)
  );
}

export function useChangeVisibility() {
  return useInvalidating(({ id, action }) =>
    api.post(`/admin/content/${id}/${action}`, undefined, authed)
  );
}

export function useCreateGenre() {
  return useInvalidating((name) => api.post('/admin/genres', { name }, authed), ['genres']);
}
