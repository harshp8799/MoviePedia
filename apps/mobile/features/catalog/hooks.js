import { useQuery } from '@tanstack/react-query';

import { api } from '../../lib/api';

export function useHome() {
  return useQuery({ queryKey: ['home'], queryFn: () => api.get('/home') });
}

export function useSearch(query) {
  return useQuery({
    queryKey: ['search', query],
    enabled: !!query,
    queryFn: () => api.get(`/search?q=${encodeURIComponent(query)}`),
  });
}

export function useDetail(type, slug) {
  const path = type === 'series' ? 'series' : 'movies';
  return useQuery({
    queryKey: ['detail', type, slug],
    enabled: !!slug,
    queryFn: () => api.get(`/${path}/${slug}`),
  });
}
