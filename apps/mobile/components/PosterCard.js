import { useRouter } from 'expo-router';
import { Image, Pressable, StyleSheet, Text, View } from 'react-native';

// Tappable poster that navigates to the content detail screen.
export default function PosterCard({ item, width = 120 }) {
  const router = useRouter();
  const height = width * 1.5;

  return (
    <Pressable onPress={() => router.push(`/content/${item.type}/${item.slug}`)} style={{ width }}>
      {item.poster?.url ? (
        <Image source={{ uri: item.poster.url }} style={[styles.poster, { width, height }]} />
      ) : (
        <View style={[styles.poster, styles.placeholder, { width, height }]}>
          <Text style={styles.placeholderText}>{item.title}</Text>
        </View>
      )}
      <Text numberOfLines={1} style={styles.title}>
        {item.title}
      </Text>
      <Text style={styles.year}>{item.releaseYear || '—'}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  poster: { borderRadius: 8, backgroundColor: '#151922' },
  placeholder: { alignItems: 'center', justifyContent: 'center', padding: 6 },
  placeholderText: { color: '#9aa4b2', fontSize: 11, textAlign: 'center' },
  title: { color: '#f5f7fa', marginTop: 6, fontSize: 13 },
  year: { color: '#9aa4b2', fontSize: 11 },
});
