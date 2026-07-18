import { FlatList, StyleSheet, Text, View } from 'react-native';

import PosterCard from './PosterCard';

// Horizontal rail of poster cards (home rails, similar titles).
export default function Rail({ title, items }) {
  if (!items || items.length === 0) return null;
  return (
    <View style={styles.section}>
      {title ? <Text style={styles.title}>{title}</Text> : null}
      <FlatList
        horizontal
        data={items}
        keyExtractor={(item) => item.id}
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.row}
        renderItem={({ item }) => <PosterCard item={item} />}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  section: { marginBottom: 20 },
  title: {
    color: '#f5f7fa',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    paddingHorizontal: 16,
  },
  row: { paddingHorizontal: 12, gap: 12 },
});
