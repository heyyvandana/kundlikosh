// First screen — devotional welcome. Cosmic indigo background with constellation
// pattern + saffron accents. CSS-only "human-made" feel: no AI raster art.
import React from 'react';
import { View, Text, StyleSheet, Pressable, ScrollView } from 'react-native';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Circle, G, Line, Path } from 'react-native-svg';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { strings, useLocale } from '@/i18n';

export default function Welcome() {
  const insets = useSafeAreaInsets();
  const locale = useLocale((s) => s.locale);
  const setLocale = useLocale((s) => s.setLocale);
  const T = strings[locale].onb;

  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo, colors.indigoLight]} style={s.bg}>
      <ScrollView
        contentContainerStyle={[
          s.container,
          { paddingTop: insets.top + 24, paddingBottom: insets.bottom + 24 },
        ]}
      >
        {/* Locale toggle (top-right) */}
        <View style={s.localeRow}>
          <Pressable onPress={() => setLocale('en')}>
            <Text style={[s.localePill, locale === 'en' && s.localePillOn]}>EN</Text>
          </Pressable>
          <Pressable onPress={() => setLocale('hi')}>
            <Text style={[s.localePill, locale === 'hi' && s.localePillOn]}>हि</Text>
          </Pressable>
        </View>

        {/* Mandala-style decorative SVG */}
        <View style={s.mandalaWrap}>
          <Svg width={220} height={220} viewBox="0 0 220 220">
            <G stroke={colors.gold} strokeWidth={0.8} fill="none" opacity={0.85}>
              <Circle cx={110} cy={110} r={50} />
              <Circle cx={110} cy={110} r={70} />
              <Circle cx={110} cy={110} r={90} strokeDasharray="2 4" />
            </G>
            {/* 12 zodiac spoke marks */}
            {Array.from({ length: 12 }).map((_, i) => {
              const a = (i * 30 * Math.PI) / 180;
              const r1 = 50;
              const r2 = 90;
              return (
                <Line
                  key={i}
                  x1={110 + Math.cos(a) * r1}
                  y1={110 + Math.sin(a) * r1}
                  x2={110 + Math.cos(a) * r2}
                  y2={110 + Math.sin(a) * r2}
                  stroke={colors.gold}
                  strokeWidth={0.8}
                  opacity={0.6}
                />
              );
            })}
            {/* Sacred geometry petals */}
            <G stroke={colors.saffron} strokeWidth={1} fill="none" opacity={0.9}>
              {Array.from({ length: 8 }).map((_, i) => {
                const a = (i * 45 * Math.PI) / 180;
                return (
                  <Path
                    key={i}
                    d={`M${110 + Math.cos(a) * 30} ${110 + Math.sin(a) * 30} Q${110} ${110} ${
                      110 + Math.cos(a + 0.3) * 30
                    } ${110 + Math.sin(a + 0.3) * 30}`}
                  />
                );
              })}
            </G>
            {/* Center Om */}
            <SvgOm cx={110} cy={110} />
          </Svg>
        </View>

        <Text style={s.brand}>KundliKosh</Text>
        <Text style={s.brandHi}>कुंडलीकोश</Text>

        <View style={s.divider} />

        <Text style={s.title}>{T.welcomeTitle}</Text>
        <Text style={s.sub}>{T.welcomeSub}</Text>
        <Text style={s.body}>{T.welcomeBody}</Text>

        <Pressable
          style={({ pressed }) => [s.cta, pressed && { opacity: 0.85 }]}
          onPress={() => router.push('/onboarding/details')}
        >
          <Text style={s.ctaText}>{T.cta}</Text>
        </Pressable>

        <Text style={s.legal}>{strings[locale].legal.disclaimer}</Text>
      </ScrollView>
    </LinearGradient>
  );
}

function SvgOm({ cx, cy }: { cx: number; cy: number }) {
  // hand-drawn ॐ rendered as text via SVG to keep it crisp
  return (
    <G transform={`translate(${cx} ${cy})`}>
      <Circle r={26} fill="rgba(232,197,71,0.15)" stroke={colors.gold} strokeWidth={1} />
      {/* simple stylised glyph in saffron — SvgText omitted; use plain Path is overkill,
          so we keep it minimal with overlapping circles for a yantra feel */}
      <Circle r={18} fill="none" stroke={colors.saffron} strokeWidth={1.2} />
      <Circle r={10} fill="none" stroke={colors.saffron} strokeWidth={0.8} />
      <Circle r={3} fill={colors.goldBright} />
    </G>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  container: { paddingHorizontal: 24, alignItems: 'center' },
  localeRow: {
    alignSelf: 'flex-end',
    flexDirection: 'row',
    gap: 8,
    marginBottom: 8,
  },
  localePill: {
    color: colors.gold,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
    borderWidth: 1,
    borderColor: 'rgba(201,162,39,0.4)',
    fontFamily: 'Spectral-SemiBold',
    fontSize: 12,
  },
  localePillOn: {
    backgroundColor: 'rgba(232,197,71,0.18)',
    color: colors.goldBright,
    borderColor: colors.gold,
  },
  mandalaWrap: { alignItems: 'center', marginVertical: 12 },
  brand: {
    color: colors.goldBright,
    ...text.brand,
    textShadowColor: 'rgba(0,0,0,0.4)',
    textShadowRadius: 8,
  },
  brandHi: {
    color: colors.gold,
    marginTop: 4,
    ...text.brandHi,
  },
  divider: {
    height: 2,
    width: 60,
    backgroundColor: colors.gold,
    marginVertical: 18,
    opacity: 0.6,
    borderRadius: 999,
  },
  title: {
    color: colors.goldBright,
    fontFamily: 'Cormorant-SemiBold',
    fontSize: 22,
    textAlign: 'center',
    marginBottom: 6,
  },
  sub: {
    color: colors.gold,
    fontFamily: 'Cormorant-Italic',
    fontSize: 15,
    textAlign: 'center',
    marginBottom: 18,
  },
  body: {
    color: 'rgba(245,230,202,0.85)',
    fontFamily: 'Spectral-Regular',
    fontSize: 14,
    lineHeight: 22,
    textAlign: 'center',
    marginBottom: 28,
    paddingHorizontal: 6,
  },
  cta: {
    backgroundColor: colors.saffron,
    paddingVertical: 14,
    paddingHorizontal: 56,
    borderRadius: 999,
    borderWidth: 1.5,
    borderColor: colors.gold,
  },
  ctaText: {
    color: colors.offwhite,
    fontFamily: 'Cormorant-Bold',
    fontSize: 18,
    letterSpacing: 1,
  },
  legal: {
    color: 'rgba(245,230,202,0.55)',
    ...text.small,
    fontSize: 11,
    textAlign: 'center',
    marginTop: 28,
    paddingHorizontal: 12,
  },
});
