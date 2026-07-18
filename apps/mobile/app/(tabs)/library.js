import { FlatList, ScrollView, StyleSheet, Text, View } from 'react-native';

import PosterCard from '../../components/PosterCard';
import { useHistory, useWatchlist } from '../../features/library/hooks';
import { useAuth } from '../../providers/AuthProvider';

function Section({ title, items }) {
  const mapped = (items || []).map((i) => ({ ...i, id: i.contentId }));
  return (
    <View style={styles.section}>
      <Text style={styles.heading}>{title}</Text>
      {mapped.length === 0 ? (
        <Text style={styles.muted}>Nothing here yet.</Text>
      ) : (
        <FlatList
          horizontal
          data={mapped}
          keyExtractor={(i) => i.contentId}
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={{ gap: 12 }}
          renderItem={({ item }) => <PosterCard item={item} width={110} />}
        />
      )}
    </View>
  );
}

export default function LibraryScreen() {
  const { user } = useAuth();
  const watchlist = useWatchlist(!!user);
  const history = useHistory(!!user);

  if (!user) {
    return (
      <View style={styles.center}>
        <Text style={styles.muted}>Sign in on the Profile tab to see your library.</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={{ padding: 16 }}>
      <Section title="Watchlist" items={watchlist.data?.items} />
      <Section title="Recently viewed" items={history.data?.items} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#0b0d12' },
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0b0d12',
    padding: 24,
  },
  section: { marginBottom: 24 },
  heading: { color: '#f5f7fa', fontSize: 16, fontWeight: '600', marginBottom: 10 },
  muted: { color: '#9aa4b2' },
});
