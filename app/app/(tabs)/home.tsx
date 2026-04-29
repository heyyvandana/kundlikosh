// Home — recreates the preview HTML in React Native: brand header, patron deity,
// today's mantra, kundli, yogas chips, planet table, dasha card.
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Pressable } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useProfile } from '@/store/profile';
import { api } from '@/api/client';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { strings, useLocale } from '@/i18n';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';
import { PatronDeityCard } from '@/components/PatronDeityCard';
import { NorthIndianKundli } from '@/components/NorthIndianKundli';
import { PlanetTable } from '@/components/PlanetTable';
import { DashaCard } from '@/components/DashaCard';
import type { DashaResponse, YogasResponse } from '@/api/types';

export default function Home() {
  const insets = useSafeAreaInsets();
  const profile = useProfile((s) => s.profile);
  const locale = useLocale((s) => s.locale);
  const T = strings[locale];

  const [dasha, setDasha] = useState<DashaResponse | null>(null);
  const [yogas, setYogas] = useState<YogasResponse | null>(null);
  const [loadErr, setLoadErr] = useState<string | null>(null);

  useEffect(() => {
    if (!profile) return;
    let cancelled = false;
    void (async () => {
      try {
        const [d, y] = await Promise.all([api.dasha(profile.birth, 5), api.yogas(profile.birth)]);
        if (!cancelled) {
          setDasha(d.data);
          setYogas(y.data);
        }
      } catch (e) {
        if (!cancelled) setLoadErr('Could not load dasha/yogas — check your connection.');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [profile]);

  if (!profile?.chart) {
    return (
      <View style={[s.bg, { justifyContent: 'center', alignItems: 'center' }]}>
        <Text style={{ color: colors.gold }}>Loading…</Text>
      </View>
    );
  }
  const chart = profile.chart;

  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <ScrollView
        contentContainerStyle={{ paddingTop: insets.top + 8, paddingBottom: insets.bottom + 24 }}
        showsVerticalScrollIndicator={false}
      >
        <View style={s.canvas}>
          {/* Header */}
          <View style={s.header}>
            <Text style={s.greet}>
              {T.namaste}, <Text style={{ fontFamily: 'Spectral-SemiBold', color: colors.maroon }}>{profile.birth.name}</Text>
            </Text>
            <View style={s.brandWrap}>
              <View style={s.logoSlot}>
                <Text style={s.logoSlotText}>your{`\n`}logo</Text>
              </View>
              <Text style={s.brand}>KundliKosh</Text>
              <Text style={s.brandHi}>कुंडलीकोश</Text>
              <View style={s.divider} />
            </View>
          </View>

          <SectionTitle en="Your Patron" hi="आपके आराध्य" />
          <PatronDeityCard deity={chart.patron_deity} />

          <SectionTitle en="Today's mantra" hi="आज का मंत्र" />
          <PaperCard inset={16}>
            <View style={{ alignItems: 'center' }}>
              <Text style={[s.omGlyph]}>ॐ</Text>
              <Text style={s.mantraHi}>ॐ चन्द्राय नमः</Text>
              <Text style={s.mantraTrans}>Om Chandraya Namaha · 108×</Text>
              <Text style={s.mantraNote}>
                Today is <Text style={s.bold}>Monday</Text> — Chandra's day. Chant 108 times in the morning for a peaceful mind. Wear something <Text style={s.bold}>white</Text> or pearl. Your Moon is exalted in {chart.moon_nakshatra}, so today's energy supports you specially.
              </Text>
            </View>
          </PaperCard>

          <SectionTitle en="Janma Kundli" hi="जन्म कुंडली" />
          <PaperCard inset={14}>
            <View style={s.kundliHead}>
              <Text style={s.kundliTitle}>
                Lagna · {chart.lagna_sign}{' '}
                <Text style={{ fontFamily: 'TiroDevanagari-Regular' }}>({chart.lagna_sign_hi})</Text>
              </Text>
              <Text style={s.kundliSmall}>
                {chart.lagna_degree_in_sign.toFixed(2)}° · {chart.lagna_nakshatra} P{chart.lagna_pada}
              </Text>
            </View>
            <View style={{ alignItems: 'center', marginTop: 6 }}>
              <NorthIndianKundli chart={chart} size={300} />
            </View>
            <Text style={s.kundliCaption}>
              North Indian style · 12 houses fixed, signs rotate from Lagna
            </Text>
          </PaperCard>

          {yogas && yogas.yogas.length > 0 && (
            <>
              <SectionTitle en="Detected" hi="आपके योग" />
              <View style={s.chips}>
                {yogas.yogas.map((y) => (
                  <View
                    key={y.name}
                    style={[
                      s.chip,
                      y.category === 'dosha' && { backgroundColor: 'rgba(126,29,29,0.2)', borderColor: '#7E1D1D' },
                    ]}
                  >
                    <Text
                      style={[
                        s.chipText,
                        y.category === 'dosha' ? { color: '#FCE9E9' } : { color: colors.maroon },
                      ]}
                    >
                      {y.name}
                    </Text>
                    <Text
                      style={[
                        s.chipTextHi,
                        y.category === 'dosha' ? { color: '#FCE9E9' } : { color: colors.saffronDeep },
                      ]}
                    >
                      · {y.name_hi}
                    </Text>
                  </View>
                ))}
              </View>
            </>
          )}

          <SectionTitle en="Planets" hi="ग्रह" />
          <PaperCard inset={14}>
            <PlanetTable planets={chart.planets} />
          </PaperCard>

          {dasha && (
            <>
              <SectionTitle en="Vimshottari Dasha" hi="विंशोत्तरी दशा" />
              <DashaCard dasha={dasha} />
            </>
          )}

          {loadErr && (
            <Pressable style={s.errBox}>
              <Text style={s.errText}>{loadErr}</Text>
            </Pressable>
          )}
        </View>
      </ScrollView>
    </LinearGradient>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  canvas: {
    backgroundColor: colors.parchment,
    margin: 12,
    borderRadius: 22,
    padding: 14,
    borderWidth: 2,
    borderColor: colors.gold,
  },
  header: { alignItems: 'center', paddingVertical: 4 },
  greet: { alignSelf: 'flex-end', color: colors.saffronDeep, fontFamily: 'Cormorant-Italic', fontSize: 13 },
  brandWrap: { alignItems: 'center', marginTop: 8 },
  logoSlot: {
    width: 64,
    height: 64,
    borderRadius: 32,
    borderWidth: 1.5,
    borderStyle: 'dashed',
    borderColor: colors.saffron,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255,248,231,0.4)',
    marginBottom: 6,
  },
  logoSlotText: {
    color: 'rgba(91,31,0,0.55)',
    fontFamily: 'Cormorant-Italic',
    fontSize: 11,
    textAlign: 'center',
  },
  brand: {
    ...text.brand,
    fontSize: 28,
    color: colors.saffronDeep,
  },
  brandHi: { ...text.brandHi, color: colors.maroon, marginTop: 2 },
  divider: {
    width: 80,
    height: 1.5,
    backgroundColor: colors.gold,
    marginTop: 8,
    opacity: 0.6,
  },
  omGlyph: {
    fontSize: 56,
    color: colors.saffron,
    fontFamily: 'TiroDevanagari-Regular',
  },
  mantraHi: {
    fontFamily: 'TiroDevanagari-Regular',
    fontSize: 22,
    color: colors.maroon,
    marginTop: 4,
    textAlign: 'center',
  },
  mantraTrans: {
    fontFamily: 'Cormorant-Italic',
    fontSize: 13,
    color: colors.saffronDeep,
    marginTop: 2,
  },
  mantraNote: {
    ...text.body,
    color: colors.maroon,
    marginTop: 12,
    textAlign: 'center',
  },
  bold: { fontFamily: 'Spectral-SemiBold' },
  kundliHead: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    marginBottom: 4,
  },
  kundliTitle: { ...text.section, fontSize: 16, color: colors.saffronDeep },
  kundliSmall: { ...text.small, color: colors.maroon },
  kundliCaption: {
    ...text.small,
    color: colors.saffronDeep,
    fontFamily: 'Cormorant-Italic',
    textAlign: 'center',
    marginTop: 6,
  },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 999,
    backgroundColor: colors.parchment,
    borderWidth: 1,
    borderColor: colors.gold,
    flexDirection: 'row',
    alignItems: 'center',
  },
  chipText: { ...text.bodySemi, fontSize: 12 },
  chipTextHi: { ...text.hiSmall, marginLeft: 4 },
  errBox: {
    marginTop: 16,
    padding: 12,
    borderRadius: 8,
    backgroundColor: 'rgba(126,29,29,0.15)',
  },
  errText: { ...text.body, color: '#7E1D1D', textAlign: 'center' },
});
