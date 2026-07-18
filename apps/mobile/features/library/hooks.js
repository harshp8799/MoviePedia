import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '../../lib/api';

const authed = { auth: true };

export function useWatchlist(enabled) {
  return useQuery({
    queryKey: ['watchlist'],
    enabled,
    queryFn: () => api.get('/library/watchlist', authed),
  });
}

export function useHistory(enabled) {
  return useQuery({ queryKey: ['history'], enabled, queryFn: () => api.get('/history', authed) });
}

export function useAddToWatchlist() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (contentId) => api.post('/library/watchlist', { contentId }, authed),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['watchlist'] }),
  });
}

export function useRecordView() {
  return useMutation({ mutationFn: (contentId) => api.post('/history', { contentId }, authed) });
}
