import { ActivityIndicator, ScrollView, StyleSheet, Text, View } from 'react-native';

import Rail from '../../components/Rail';
import { useHome } from '../../features/catalog/hooks';

export default function HomeScreen() {
  const { data, isLoading, isError } = useHome();

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator color="#e50914" />
      </View>
    );
  }
  if (isError || !data) {
    return (
      <View style={styles.center}>
        <Text style={styles.muted}>Couldn’t load the catalog. Is the API running?</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={{ paddingVertical: 16 }}>
      {data.sections.map((section) => (
        <Rail key={section.key} title={section.title} items={section.items} />
      ))}
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
  muted: { color: '#9aa4b2', textAlign: 'center' },
});
