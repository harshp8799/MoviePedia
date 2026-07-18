'use client';

// Public user-library hooks — all authenticated, via the shared API client.

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '../../lib/apiClient';

const authed = { auth: true };

export function useList(listType, enabled) {
  return useQuery({
    queryKey: ['library', listType],
    enabled,
    queryFn: () => api.get(`/library/${listType}`, authed),
  });
}

export function useHistory(enabled) {
  return useQuery({ queryKey: ['history'], enabled, queryFn: () => api.get('/history', authed) });
}

export function useContinueWatching(enabled) {
  return useQuery({
    queryKey: ['progress'],
    enabled,
    queryFn: () => api.get('/progress', authed),
  });
}

export function useAddToList(listType) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (contentId) => api.post(`/library/${listType}`, { contentId }, authed),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['library', listType] }),
  });
}

export function useRemoveFromList(listType) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (contentId) => api.del(`/library/${listType}/${contentId}`, authed),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['library', listType] }),
  });
}

export function useRecordView() {
  return useMutation({ mutationFn: (contentId) => api.post('/history', { contentId }, authed) });
}
