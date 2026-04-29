// Reusable parchment card with double-border decor. The "human-made" look
// is achieved by stacking two borders + dashed inner accent — same as preview.
import React, { type PropsWithChildren } from 'react';
import { View, StyleSheet, type ViewStyle } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { colors } from '@/theme/colors';

export function PaperCard({
  children,
  style,
  inset = 16,
}: PropsWithChildren<{ style?: ViewStyle; inset?: number }>) {
  return (
    <LinearGradient
      colors={[colors.parchment, colors.cream]}
      start={{ x: 0, y: 0 }}
      end={{ x: 0, y: 1 }}
      style={[s.card, style]}
    >
      <View style={s.outerBorder} pointerEvents="none" />
      <View style={[s.innerBorder, { inset: 10 } as ViewStyle]} pointerEvents="none" />
      <View style={{ padding: inset }}>{children}</View>
    </LinearGradient>
  );
}

const s = StyleSheet.create({
  card: {
    borderRadius: 18,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOpacity: 0.15,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
  outerBorder: {
    position: 'absolute',
    top: 6,
    bottom: 6,
    left: 6,
    right: 6,
    borderRadius: 14,
    borderWidth: 1.5,
    borderColor: colors.saffron,
  },
  innerBorder: {
    position: 'absolute',
    top: 10,
    bottom: 10,
    left: 10,
    right: 10,
    borderRadius: 12,
    borderStyle: 'dashed',
    borderWidth: 1,
    borderColor: 'rgba(91,31,0,0.3)',
  },
});
