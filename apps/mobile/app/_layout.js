import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: '#151922' },
          headerTintColor: '#f5f7fa',
          contentStyle: { backgroundColor: '#0b0d12' },
        }}
      >
        <Stack.Screen name="index" options={{ title: 'Movie Pedia' }} />
      </Stack>
    </SafeAreaProvider>
  );
}
