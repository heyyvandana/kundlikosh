// KundliKosh palette — devotional + cosmic, hand-crafted feel.
// Mirrors the HTML preview so we maintain visual continuity.
export const colors = {
  saffron: '#C8501A',
  saffronDeep: '#8E2A0A',
  gold: '#C9A227',
  goldBright: '#E8C547',
  indigo: '#1B1340',
  indigoDeep: '#0A0726',
  indigoLight: '#2A1A4F',
  maroon: '#5B1F00',
  cream: '#F5E6CA',
  parchment: '#FBF3E2',
  offwhite: '#FFF8E7',
  greenTulasi: '#2F5D3F',

  // Functional
  textPrimary: '#5B1F00',
  textMuted: '#8E2A0A',
  border: 'rgba(91,31,0,0.15)',
  borderStrong: '#C9A227',

  // Dignity pills
  exalted: '#1F5C1F',
  exaltedBg: '#E8F5E8',
  debilitated: '#7E1D1D',
  debilitatedBg: '#FCE9E9',
  ownSign: '#7A5210',
  ownSignBg: '#FFF1D6',
} as const;

export type ColorKey = keyof typeof colors;
