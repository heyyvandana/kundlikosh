// Detailed birth chart screen — same kundli larger + planet table.
import React from 'react';
import { Text, ScrollView, StyleSheet, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useProfile } from '@/store/profile';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';
import { NorthIndianKundli } from '@/components/NorthIndianKundli';
import { PlanetTable } from '@/components/PlanetTable';

export default function Kundli() {
  const insets = useSafeAreaInsets();
  const profile = useProfile((s) => s.profile);
  if (!profile?.chart) return <Text style={{ color: '#fff' }}>Loading…</Text>;
  const chart = profile.chart;

  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <ScrollView
        contentContainerStyle={{ padding: 16, paddingTop: insets.top + 12, paddingBottom: insets.bottom + 24 }}
      >
        <SectionTitle en="Janma Kundli" hi="जन्म कुंडली" />
        <PaperCard inset={14}>
          <View style={{ alignItems: 'center' }}>
            <Text style={s.head}>
              {chart.lagna_sign}{' '}
              <Text style={{ fontFamily: 'TiroDevanagari-Regular', color: colors.maroon }}>
                ({chart.lagna_sign_hi})
              </Text>
            </Text>
            <Text style={s.headSmall}>
              {chart.lagna_degree_in_sign.toFixed(2)}° · {chart.lagna_nakshatra} P{chart.lagna_pada}
            </Text>
            <NorthIndianKundli chart={chart} size={320} />
            <Text style={s.foot}>
              Birth: {profile.birth.date} · {profile.birth.time} · {profile.birth.timezone}
            </Text>
            <Text style={s.foot}>
              Ayanamsa (Lahiri): {chart.ayanamsa.toFixed(4)}°
            </Text>
          </View>
        </PaperCard>

        <SectionTitle en="Planets" hi="ग्रह" />
        <PaperCard inset={14}>
          <PlanetTable planets={chart.planets} />
        </PaperCard>
      </ScrollView>
    </LinearGradient>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  head: { ...text.cardTitle, color: colors.saffronDeep },
  headSmall: { ...text.small, color: colors.maroon, marginBottom: 8 },
  foot: { ...text.small, color: colors.saffronDeep, marginTop: 6, fontFamily: 'Cormorant-Italic' },
});
