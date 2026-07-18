import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { AuthProvider } from '../providers/AuthProvider';
import { QueryProvider } from '../providers/QueryProvider';

export default function RootLayout() {
  return (
    <QueryProvider>
      <AuthProvider>
        <SafeAreaProvider>
          <StatusBar style="light" />
          <Stack
            screenOptions={{
              headerStyle: { backgroundColor: '#151922' },
              headerTintColor: '#f5f7fa',
              contentStyle: { backgroundColor: '#0b0d12' },
            }}
          >
            <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
            <Stack.Screen name="content/[type]/[slug]" options={{ title: '' }} />
          </Stack>
        </SafeAreaProvider>
      </AuthProvider>
    </QueryProvider>
  );
}
