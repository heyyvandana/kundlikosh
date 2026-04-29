// Tiny i18n shim. Hindi-first project so we keep both strings always available.
// Components decide which to render (often we render both — EN + HI side by side).
import { create } from 'zustand';

export type Locale = 'en' | 'hi';

export const strings = {
  en: {
    appName: 'KundliKosh',
    namaste: 'Namaste',
    yourPatron: 'Your Patron',
    todaysMantra: "Today's Mantra",
    janmaKundli: 'Janma Kundli',
    detected: 'Detected',
    planets: 'Planets',
    vimshottari: 'Vimshottari Dasha',
    currentlyRunning: 'Currently running',
    nextMahadashas: 'Next mahadashas',

    home: 'Home',
    kundli: 'Kundli',
    story: 'Story',
    match: 'Match',
    devalok: 'Devalok',
    ask: 'Ask',

    onb: {
      welcomeTitle: 'Welcome to KundliKosh',
      welcomeSub: 'Your treasury of authentic Vedic insight.',
      welcomeBody:
        'KundliKosh computes your real birth chart from the same Swiss Ephemeris used by professional Vedic software. No templates, no guesswork.',
      cta: 'Begin',
      nameTitle: 'What name shall we call you?',
      namePh: 'Your full name',
      dobTitle: 'When were you born?',
      dobHint: 'As accurate as possible — even minutes matter.',
      dateLabel: 'Birth date',
      timeLabel: 'Birth time',
      placeTitle: 'Where were you born?',
      placePh: 'City, state, country',
      latLabel: 'Latitude',
      lonLabel: 'Longitude',
      tzLabel: 'Time zone',
      next: 'Next',
      back: 'Back',
      computing: 'Reading the heavens…',
      done: 'Continue',
    },

    table: {
      graha: 'Graha',
      sign: 'Sign',
      house: 'House',
      nakshatra: 'Nakshatra',
    },
    dignity: {
      exalted: 'exalted',
      debilitated: 'debilitated',
      own_sign: 'own sign',
      neutral: 'neutral',
    },

    legal: {
      disclaimer:
        'KundliKosh is for guidance and reflection only. Not a substitute for medical, financial, or legal advice.',
    },
  },
  hi: {
    appName: 'कुंडलीकोश',
    namaste: 'नमस्ते',
    yourPatron: 'आपके आराध्य',
    todaysMantra: 'आज का मंत्र',
    janmaKundli: 'जन्म कुंडली',
    detected: 'आपके योग',
    planets: 'ग्रह',
    vimshottari: 'विंशोत्तरी दशा',
    currentlyRunning: 'वर्तमान दशा',
    nextMahadashas: 'आने वाली दशाएँ',

    home: 'गृह',
    kundli: 'कुंडली',
    story: 'फलादेश',
    match: 'मेल',
    devalok: 'देवलोक',
    ask: 'पूछें',

    onb: {
      welcomeTitle: 'कुंडलीकोश में आपका स्वागत है',
      welcomeSub: 'सच्चे वैदिक ज्ञान का कोश।',
      welcomeBody:
        'कुंडलीकोश आपकी कुंडली स्विस एफिमेरिस से बनाता है — वही सटीकता जो पेशेवर ज्योतिषी प्रयोग करते हैं।',
      cta: 'आरंभ करें',
      nameTitle: 'आपका नाम क्या है?',
      namePh: 'आपका पूरा नाम',
      dobTitle: 'आपका जन्म कब हुआ था?',
      dobHint: 'जितना सटीक उतना अच्छा — मिनट भी मायने रखते हैं।',
      dateLabel: 'जन्म तिथि',
      timeLabel: 'जन्म समय',
      placeTitle: 'आपका जन्म स्थान?',
      placePh: 'शहर, राज्य, देश',
      latLabel: 'अक्षांश',
      lonLabel: 'देशांतर',
      tzLabel: 'समय क्षेत्र',
      next: 'आगे',
      back: 'पीछे',
      computing: 'आकाश पढ़ा जा रहा है…',
      done: 'जारी रखें',
    },

    table: {
      graha: 'ग्रह',
      sign: 'राशि',
      house: 'भाव',
      nakshatra: 'नक्षत्र',
    },
    dignity: {
      exalted: 'उच्च',
      debilitated: 'नीच',
      own_sign: 'स्वगृही',
      neutral: 'सामान्य',
    },

    legal: {
      disclaimer:
        'कुंडलीकोश केवल मार्गदर्शन एवं चिंतन हेतु है। यह चिकित्सा, वित्तीय या कानूनी सलाह का स्थान नहीं है।',
    },
  },
} as const;

interface LocaleStore {
  locale: Locale;
  setLocale: (l: Locale) => void;
}

export const useLocale = create<LocaleStore>((set) => ({
  locale: 'en',
  setLocale: (locale) => set({ locale }),
}));

export const t = (key: keyof typeof strings.en, locale: Locale) =>
  (strings[locale] as Record<string, unknown>)[key] as string;
