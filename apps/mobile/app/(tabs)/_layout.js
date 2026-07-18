import { Tabs } from 'expo-router';

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerStyle: { backgroundColor: '#151922' },
        headerTintColor: '#f5f7fa',
        tabBarStyle: { backgroundColor: '#151922', borderTopColor: '#2a313d' },
        tabBarActiveTintColor: '#e50914',
        tabBarInactiveTintColor: '#9aa4b2',
        sceneContainerStyle: { backgroundColor: '#0b0d12' },
      }}
    >
      <Tabs.Screen name="index" options={{ title: 'Home' }} />
      <Tabs.Screen name="search" options={{ title: 'Search' }} />
      <Tabs.Screen name="library" options={{ title: 'Library' }} />
      <Tabs.Screen name="profile" options={{ title: 'Profile' }} />
    </Tabs>
  );
}
