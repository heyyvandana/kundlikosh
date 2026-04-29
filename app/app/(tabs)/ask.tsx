// Ask — AI Astrologer (Gemini Flash). Placeholder until Phase 4.
import React from 'react';
import { LinearGradient } from 'expo-linear-gradient';
import { Text, View, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';

export default function Ask() {
  const insets = useSafeAreaInsets();
  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <View style={{ padding: 16, paddingTop: insets.top + 12 }}>
        <SectionTitle en="Ask the Sky" hi="आकाश से पूछें" />
        <PaperCard inset={20}>
          <Text style={s.title}>AI Astrologer — coming soon</Text>
          <Text style={s.body}>
            A Vedic-trained chat assistant grounded in your real chart. Built on Google Gemini Flash (free tier).
            Lands in Phase 4.
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
