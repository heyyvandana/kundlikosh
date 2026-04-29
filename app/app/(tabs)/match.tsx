// Compatibility tab — placeholder until Phase 5 (form will collect partner birth data).
import React from 'react';
import { LinearGradient } from 'expo-linear-gradient';
import { Text, View, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';

export default function Match() {
  const insets = useSafeAreaInsets();
  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <View style={{ padding: 16, paddingTop: insets.top + 12 }}>
        <SectionTitle en="Guna Milan" hi="गुण मिलन" />
        <PaperCard inset={20}>
          <Text style={s.title}>Compatibility — coming soon</Text>
          <Text style={s.body}>
            The 36-point Ashtakoot Guna Milan engine is built and tested. The UI for entering a partner's
            birth data lands in Phase 2c.
          </Text>
        </PaperCard>
      </View>
    </LinearGradient>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  title: { ...text.cardTitle, fontSize: 22, color: colors.saffronDeep, textAlign: 'center' },
  body: { ...text.body, color: colors.maroon, textAlign: 'center', marginTop: 8 },
});
