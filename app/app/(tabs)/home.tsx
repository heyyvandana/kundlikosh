// Home — recreates the preview HTML in React Native: brand header, patron deity,
// today's mantra, kundli, yogas chips, planet table, dasha card.
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Pressable, Image } from 'react-native';
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
import { PanchangCard } from '@/components/PanchangCard';
import type { DashaResponse, PanchangResponse, YogasResponse } from '@/api/types';

const MANTRAS: Record<string, { hi: string; trans: string }> = {
  Sun: { hi: 'ॐ सूर्याय नमः', trans: 'Om Suryaya Namaha' },
  Moon: { hi: 'ॐ चन्द्राय नमः', trans: 'Om Chandraya Namaha' },
  Mars: { hi: 'ॐ अंगारकाय नमः', trans: 'Om Angarakaya Namaha' },
  Mercury: { hi: 'ॐ बुधाय नमः', trans: 'Om Budhaya Namaha' },
  Jupiter: { hi: 'ॐ बृहस्पतये नमः', trans: 'Om Brihaspataye Namaha' },
  Venus: { hi: 'ॐ शुक्राय नमः', trans: 'Om Shukraya Namaha' },
  Saturn: { hi: 'ॐ शनैश्चराय नमः', trans: 'Om Shanaishcharaya Namaha' },
};
const COLORS_BY_LORD: Record<string, string> = {
  Sun: 'red or saffron',
  Moon: 'white or pearl',
  Mars: 'red or coral',
  Mercury: 'green',
  Jupiter: 'yellow',
  Venus: 'white or silver',
  Saturn: 'dark blue or black',
};
const mantraForLord = (lord: string) => MANTRAS[lord] ?? MANTRAS.Moon;
const colorForLord = (lord: string) => COLORS_BY_LORD[lord] ?? 'white';

export default function Home() {
  const insets = useSafeAreaInsets();
  const profile = useProfile((s) => s.profile);
  const locale = useLocale((s) => s.locale);
  const T = strings[locale];

  const [dasha, setDasha] = useState<DashaResponse | null>(null);
  const [yogas, setYogas] = useState<YogasResponse | null>(null);
  const [panchang, setPanchang] = useState<PanchangResponse | null>(null);
  const [loadErr, setLoadErr] = useState<string | null>(null);

  useEffect(() => {
    if (!profile) return;
    let cancelled = false;
    const today = new Date().toISOString().slice(0, 10);
    void (async () => {
      try {
        const [d, y, pa] = await Promise.all([
          api.dasha(profile.birth, 5),
          api.yogas(profile.birth),
          api.panchang({
            date: today,
            timezone: profile.birth.timezone ?? 'Asia/Kolkata',
            latitude: profile.birth.latitude,
            longitude: profile.birth.longitude,
          }),
        ]);
        if (!cancelled) {
          setDasha(d.data);
          setYogas(y.data);
          setPanchang(pa.data);
        }
      } catch (e) {
        if (!cancelled) setLoadErr('Could not load dasha/yogas/panchang — check your connection.');
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
              <Image
                source={require('../../assets/brand/logo-mark.png')}
                style={s.logoMark}
                resizeMode="contain"
              />
              <Text style={s.brand}>KundliKosh</Text>
              <Text style={s.brandHi}>कुंडलीकोश</Text>
              <View style={s.divider} />
            </View>
          </View>

          {panchang && (
            <>
              <SectionTitle en="Today’s Panchang" hi="आज का पंचांग" />
              <PanchangCard data={panchang} />
            </>
          )}

          <SectionTitle en="Your Patron" hi="आपके आराध्य" />
          <PatronDeityCard deity={chart.patron_deity} />

          <SectionTitle en="Today's mantra" hi="आज का मंत्र" />
          <PaperCard inset={16}>
            <View style={{ alignItems: 'center' }}>
              <Text style={[s.omGlyph]}>ॐ</Text>
              <Text style={s.mantraHi}>{mantraForLord(panchang?.weekday_lord ?? 'Moon').hi}</Text>
              <Text style={s.mantraTrans}>{mantraForLord(panchang?.weekday_lord ?? 'Moon').trans} · 108×</Text>
              <Text style={s.mantraNote}>
                Today is <Text style={s.bold}>{panchang?.weekday ?? 'Monday'}</Text> — {panchang?.weekday_lord ?? 'Moon'}'s day. Chant 108 times in the morning. Wear <Text style={s.bold}>{colorForLord(panchang?.weekday_lord ?? 'Moon')}</Text>. Your Moon is exalted in {chart.moon_nakshatra}.
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
  logoMark: {
    width: 96,
    height: 96,
    marginBottom: 4,
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
