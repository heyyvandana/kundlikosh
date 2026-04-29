// Devalok — mythology library. Placeholder for Phase 5.
import React from 'react';
import { LinearGradient } from 'expo-linear-gradient';
import { Text, View, StyleSheet, ScrollView } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';

const sections: Array<{ en: string; hi: string; teaser: string }> = [
  { en: '9 Grahas', hi: '९ ग्रह', teaser: 'Surya, Chandra, Mangal — their stories, mantras, vahanas' },
  { en: '12 Rashis', hi: '१२ राशियाँ', teaser: 'The zodiac wheel as the Vedas saw it' },
  { en: '27 Nakshatras', hi: '२७ नक्षत्र', teaser: 'Lunar mansions, deities, yoni, gana, symbols' },
  { en: 'Itihasa Charts', hi: 'इतिहास कुंडलियाँ', teaser: 'Ram, Krishna, Sita — compare with yours' },
];

export default function Devalok() {
  const insets = useSafeAreaInsets();
  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <ScrollView contentContainerStyle={{ padding: 16, paddingTop: insets.top + 12 }}>
        <SectionTitle en="Devalok" hi="देवलोक" />
        {sections.map((sec) => (
          <View key={sec.en} style={{ marginBottom: 12 }}>
            <PaperCard inset={16}>
              <Text style={s.title}>{sec.en}</Text>
              <Text style={s.titleHi}>{sec.hi}</Text>
              <Text style={s.body}>{sec.teaser}</Text>
              <Text style={s.tag}>Coming in Phase 5</Text>
            </PaperCard>
          </View>
        ))}
      </ScrollView>
    </LinearGradient>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  title: { ...text.cardTitle, fontSize: 20, color: colors.saffronDeep },
  titleHi: { ...text.cardTitleHi, fontSize: 18, color: colors.maroon, marginBottom: 4 },
  body: { ...text.body, color: colors.maroon },
  tag: { ...text.small, color: colors.saffron, marginTop: 8, fontFamily: 'Cormorant-Italic' },
});
