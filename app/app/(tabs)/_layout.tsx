// Bottom tab bar in saffron, matching the preview HTML.
import React from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { Tabs } from 'expo-router';
import { colors } from '@/theme/colors';
import { strings, useLocale } from '@/i18n';

const Icon = ({ char, focused }: { char: string; focused: boolean }) => (
  <View style={[s.iconWrap, focused && s.iconWrapOn]}>
    <Text style={[s.iconChar, focused && { color: colors.goldBright }]}>{char}</Text>
  </View>
);

export default function TabsLayout() {
  const locale = useLocale((s) => s.locale);
  const T = strings[locale];
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: colors.saffronDeep,
          borderTopColor: colors.saffron,
          borderTopWidth: 1,
          paddingTop: 6,
          height: 64,
        },
        tabBarLabelStyle: {
          fontFamily: 'Spectral-SemiBold',
          fontSize: 11,
          marginTop: 2,
        },
        tabBarActiveTintColor: colors.goldBright,
        tabBarInactiveTintColor: 'rgba(245,230,202,0.6)',
      }}
    >
      <Tabs.Screen
        name="home"
        options={{
          title: T.home,
          tabBarIcon: ({ focused }) => <Icon char="ॐ" focused={focused} />,
        }}
      />
      <Tabs.Screen
        name="kundli"
        options={{
          title: T.kundli,
          tabBarIcon: ({ focused }) => <Icon char="◇" focused={focused} />,
        }}
      />
      <Tabs.Screen
        name="match"
        options={{
          title: T.match,
          tabBarIcon: ({ focused }) => <Icon char="❤" focused={focused} />,
        }}
      />
      <Tabs.Screen
        name="devalok"
        options={{
          title: T.devalok,
          tabBarIcon: ({ focused }) => <Icon char="✦" focused={focused} />,
        }}
      />
      <Tabs.Screen
        name="ask"
        options={{
          title: T.ask,
          tabBarIcon: ({ focused }) => <Icon char="?" focused={focused} />,
        }}
      />
    </Tabs>
  );
}

const s = StyleSheet.create({
  iconWrap: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconWrapOn: {
    backgroundColor: 'rgba(232,197,71,0.2)',
  },
  iconChar: {
    fontSize: 16,
    color: 'rgba(245,230,202,0.7)',
  },
});
