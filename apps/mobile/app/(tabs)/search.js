import { useState } from 'react';
import { FlatList, StyleSheet, Text, TextInput, View } from 'react-native';

import PosterCard from '../../components/PosterCard';
import { useSearch } from '../../features/catalog/hooks';

export default function SearchScreen() {
  const [query, setQuery] = useState('');
  const trimmed = query.trim();
  const { data } = useSearch(trimmed.length > 0 ? trimmed : '');
  const items = data?.items || [];

  return (
    <View style={styles.screen}>
      <TextInput
        value={query}
        onChangeText={setQuery}
        placeholder="Search movies & series"
        placeholderTextColor="#9aa4b2"
        autoCorrect={false}
        style={styles.input}
      />
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        numColumns={3}
        columnWrapperStyle={styles.row}
        contentContainerStyle={{ gap: 16, paddingBottom: 24 }}
        renderItem={({ item }) => <PosterCard item={item} width={100} />}
        ListEmptyComponent={
          <Text style={styles.muted}>{trimmed ? 'No results.' : 'Type to search.'}</Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#0b0d12', padding: 16 },
  input: {
    backgroundColor: '#151922',
    color: '#f5f7fa',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  row: { gap: 12, justifyContent: 'flex-start' },
  muted: { color: '#9aa4b2', marginTop: 24 },
});
