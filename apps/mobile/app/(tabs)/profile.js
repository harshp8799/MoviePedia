import { useState } from 'react';
import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';

import { registerForPush } from '../../lib/push';
import { useAuth } from '../../providers/AuthProvider';

export default function ProfileScreen() {
  const { user, signIn, signUp, signOut } = useAuth();
  const [mode, setMode] = useState('signin');
  const [email, setEmail] = useState('user@moviepedia.test');
  const [password, setPassword] = useState('Passw0rd!');
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [pushStatus, setPushStatus] = useState(null);

  async function submit() {
    setError(null);
    setBusy(true);
    try {
      if (mode === 'signin') await signIn(email, password);
      else await signUp(email, password);
    } catch (err) {
      setError(err.code || err.message || 'Failed');
    } finally {
      setBusy(false);
    }
  }

  async function enablePush() {
    const result = await registerForPush();
    setPushStatus(
      result.granted
        ? `Push ${result.token ? 'token acquired' : 'permission granted'}`
        : 'Push denied'
    );
  }

  if (user) {
    return (
      <View style={styles.screen}>
        <Text style={styles.heading}>Account</Text>
        <Text style={styles.muted}>{user.email}</Text>
        <Pressable onPress={enablePush} style={styles.secondary}>
          <Text style={styles.secondaryText}>Enable notifications</Text>
        </Pressable>
        {pushStatus && <Text style={styles.muted}>{pushStatus}</Text>}
        <Pressable onPress={signOut} style={styles.primary}>
          <Text style={styles.primaryText}>Sign out</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <View style={styles.screen}>
      <Text style={styles.heading}>{mode === 'signin' ? 'Sign in' : 'Create account'}</Text>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="Email"
        placeholderTextColor="#9aa4b2"
        autoCapitalize="none"
        keyboardType="email-address"
        style={styles.input}
      />
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        placeholderTextColor="#9aa4b2"
        secureTextEntry
        style={styles.input}
      />
      {error && <Text style={styles.error}>{error}</Text>}
      <Pressable onPress={submit} disabled={busy} style={styles.primary}>
        <Text style={styles.primaryText}>
          {busy ? 'Please wait…' : mode === 'signin' ? 'Sign in' : 'Sign up'}
        </Text>
      </Pressable>
      <Pressable onPress={() => setMode((m) => (m === 'signin' ? 'signup' : 'signin'))}>
        <Text style={styles.toggle}>
          {mode === 'signin' ? 'No account? Sign up' : 'Have an account? Sign in'}
        </Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#0b0d12', padding: 20, gap: 12 },
  heading: { color: '#f5f7fa', fontSize: 22, fontWeight: '700' },
  muted: { color: '#9aa4b2' },
  input: { backgroundColor: '#151922', color: '#f5f7fa', borderRadius: 8, padding: 12 },
  error: { color: '#ff4d4f' },
  primary: { backgroundColor: '#e50914', borderRadius: 8, padding: 14, alignItems: 'center' },
  primaryText: { color: '#fff', fontWeight: '600' },
  secondary: { backgroundColor: '#1e242f', borderRadius: 8, padding: 12, alignItems: 'center' },
  secondaryText: { color: '#f5f7fa' },
  toggle: { color: '#9aa4b2', textAlign: 'center', marginTop: 8 },
});
