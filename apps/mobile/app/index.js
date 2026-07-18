import { View, Text, StyleSheet } from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.badge}>Phase 2</Text>
      <Text style={styles.title}>Movie Pedia</Text>
      <Text style={styles.subtitle}>
        Mobile bootstrap is live. Home, catalog, and details arrive in Phase 7.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    gap: 12,
    backgroundColor: '#0b0d12',
  },
  badge: {
    backgroundColor: '#e50914',
    color: '#fff',
    fontWeight: '600',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 999,
    overflow: 'hidden',
  },
  title: { color: '#f5f7fa', fontSize: 32, fontWeight: '700' },
  subtitle: { color: '#9aa4b2', textAlign: 'center' },
});
