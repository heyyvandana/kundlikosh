// First screen — devotional welcome. Cosmic indigo background with constellation
// pattern + saffron accents. CSS-only "human-made" feel: no AI raster art.
import React from 'react';
import { View, Text, StyleSheet, Pressable, ScrollView, Image } from 'react-native';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
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

        {/* Hand-drawn mandala-in-hands logo */}
        <View style={s.logoWrap}>
          <Image
            source={require('../../assets/brand/logo-mark.png')}
            style={s.logo}
            resizeMode="contain"
          />
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
  logoWrap: { alignItems: 'center', marginTop: 4, marginBottom: 8 },
  logo: { width: 220, height: 220 },
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
