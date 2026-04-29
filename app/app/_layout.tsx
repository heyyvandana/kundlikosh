// Root layout: load fonts, hydrate profile, route between onboarding & main app.
import React, { useEffect } from 'react';
import { Stack } from 'expo-router';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { fontMap } from '@/theme/typography';
import { useProfile } from '@/store/profile';

SplashScreen.preventAutoHideAsync().catch(() => {});

export default function RootLayout() {
  const [fontsLoaded] = useFonts(fontMap);
  const hydrate = useProfile((s) => s.hydrate);
  const hydrated = useProfile((s) => s.hydrated);

  useEffect(() => {
    void hydrate();
  }, [hydrate]);

  useEffect(() => {
    if (fontsLoaded && hydrated) {
      SplashScreen.hideAsync().catch(() => {});
    }
  }, [fontsLoaded, hydrated]);

  if (!fontsLoaded || !hydrated) return null;

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <StatusBar style="light" />
        <Stack
          screenOptions={{
            headerShown: false,
            contentStyle: { backgroundColor: '#0A0726' },
          }}
        />
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
