// Typography tokens. Fonts loaded via @expo-google-fonts/* in the root layout.
import {
  CormorantGaramond_400Regular,
  CormorantGaramond_600SemiBold,
  CormorantGaramond_700Bold,
  CormorantGaramond_400Regular_Italic,
} from '@expo-google-fonts/cormorant-garamond';
import { Spectral_400Regular, Spectral_600SemiBold } from '@expo-google-fonts/spectral';
import { TiroDevanagariSanskrit_400Regular } from '@expo-google-fonts/tiro-devanagari-sanskrit';

export const fontMap = {
  // English serif
  'Cormorant-Regular': CormorantGaramond_400Regular,
  'Cormorant-Italic': CormorantGaramond_400Regular_Italic,
  'Cormorant-SemiBold': CormorantGaramond_600SemiBold,
  'Cormorant-Bold': CormorantGaramond_700Bold,
  // English body
  'Spectral-Regular': Spectral_400Regular,
  'Spectral-SemiBold': Spectral_600SemiBold,
  // Hindi/Sanskrit (Devanagari) — designed for Vedic texts
  'TiroDevanagari-Regular': TiroDevanagariSanskrit_400Regular,
};

export const fonts = {
  serif: 'Cormorant-Regular',
  serifItalic: 'Cormorant-Italic',
  serifBold: 'Cormorant-Bold',
  serifSemi: 'Cormorant-SemiBold',
  body: 'Spectral-Regular',
  bodySemi: 'Spectral-SemiBold',
  devanagari: 'TiroDevanagari-Regular',
} as const;

export const text = {
  // Display
  brand: { fontFamily: fonts.serifBold, fontSize: 32, letterSpacing: 1.2, lineHeight: 34 },
  brandHi: { fontFamily: fonts.devanagari, fontSize: 18, letterSpacing: 1, lineHeight: 26 },
  // Section heads
  section: { fontFamily: fonts.serifSemi, fontSize: 20, letterSpacing: 0.5 },
  // Card titles
  cardTitle: { fontFamily: fonts.serifBold, fontSize: 26, lineHeight: 30 },
  cardTitleHi: { fontFamily: fonts.devanagari, fontSize: 22, lineHeight: 30 },
  // Body
  body: { fontFamily: fonts.body, fontSize: 14, lineHeight: 20 },
  bodySemi: { fontFamily: fonts.bodySemi, fontSize: 14, lineHeight: 20 },
  bodyItalic: { fontFamily: fonts.serifItalic, fontSize: 15, lineHeight: 22 },
  small: { fontFamily: fonts.body, fontSize: 12, lineHeight: 16 },
  hi: { fontFamily: fonts.devanagari, fontSize: 14, lineHeight: 22 },
  hiSmall: { fontFamily: fonts.devanagari, fontSize: 12, lineHeight: 18 },
} as const;
