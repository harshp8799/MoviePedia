// Push-notification foundation. Requests permission and retrieves a push token.
// Real Expo push tokens need an EAS projectId; without one this still requests permission
// and reports status (the plumbing is in place for Phase 8+ FCM delivery).

import * as Notifications from 'expo-notifications';

export async function registerForPush() {
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return { granted: false, token: null };
  try {
    const token = await Notifications.getExpoPushTokenAsync();
    return { granted: true, token: token.data };
  } catch (err) {
    // Typically missing EAS projectId in bare local dev — permission is still granted.
    return { granted: true, token: null, error: String(err) };
  }
}
