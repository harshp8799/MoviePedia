import { useEffect } from 'react';

import { useLocalSearchParams } from 'expo-router';
import {
  ActivityIndicator,
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import Rail from '../../../components/Rail';
import { useDetail } from '../../../features/catalog/hooks';
import { useAddToWatchlist, useRecordView } from '../../../features/library/hooks';
import { useAuth } from '../../../providers/AuthProvider';

export default function DetailScreen() {
  const { type, slug } = useLocalSearchParams();
  const { data, isLoading } = useDetail(type, slug);
  const { user } = useAuth();
  const addToWatchlist = useAddToWatchlist();
  const recordView = useRecordView();

  useEffect(() => {
    if (user && data?.id) recordView.mutate(data.id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, data?.id]);

  if (isLoading || !data) {
    return (
      <View style={styles.center}>
        <ActivityIndicator color="#e50914" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={{ padding: 16 }}>
      {data.backdrop?.url && <Image source={{ uri: data.backdrop.url }} style={styles.backdrop} />}
      <Text style={styles.title}>{data.title}</Text>
      <Text style={styles.meta}>
        {data.releaseYear || '—'} · {data.ageRating || 'NR'}
        {data.durationMinutes ? ` · ${data.durationMinutes}m` : ''}
      </Text>
      <Text style={styles.desc}>{data.fullDescription || data.shortDescription}</Text>

      {user && (
        <Pressable
          onPress={() => addToWatchlist.mutate(data.id)}
          style={styles.button}
          disabled={addToWatchlist.isPending}
        >
          <Text style={styles.buttonText}>
            {addToWatchlist.isSuccess ? 'In Watchlist ✓' : '+ Watchlist'}
          </Text>
        </Pressable>
      )}

      {data.seasons?.map((season) => (
        <View key={season.id} style={styles.season}>
          <Text style={styles.seasonTitle}>{season.title}</Text>
          {(season.episodes || []).map((ep) => (
            <Text key={ep.id} style={styles.episode}>
              {ep.episodeNumber}. {ep.title}
            </Text>
          ))}
        </View>
      ))}

      {data.similar?.length > 0 && (
        <View style={{ marginTop: 16 }}>
          <Rail title="More like this" items={data.similar} />
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#0b0d12' },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#0b0d12' },
  backdrop: { width: '100%', aspectRatio: 16 / 9, borderRadius: 8, marginBottom: 12 },
  title: { color: '#f5f7fa', fontSize: 26, fontWeight: '700' },
  meta: { color: '#9aa4b2', marginTop: 4 },
  desc: { color: '#c9d1dc', marginTop: 12, lineHeight: 20 },
  button: {
    backgroundColor: '#e50914',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
    marginTop: 16,
  },
  buttonText: { color: '#fff', fontWeight: '600' },
  season: { marginTop: 16 },
  seasonTitle: { color: '#f5f7fa', fontWeight: '600', marginBottom: 6 },
  episode: { color: '#c9d1dc', paddingVertical: 4 },
});
