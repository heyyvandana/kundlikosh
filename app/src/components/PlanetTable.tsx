import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import type { PlanetPosition } from '@/api/types';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { useLocale, strings } from '@/i18n';

interface Props {
  planets: PlanetPosition[];
}

export function PlanetTable({ planets }: Props) {
  const locale = useLocale((s) => s.locale);
  const T = strings[locale].table;
  const D = strings[locale].dignity;
  return (
    <View style={s.wrap}>
      <View style={s.headerRow}>
        <Text style={[s.cell, s.h, { flex: 1.1 }]}>{T.graha}</Text>
        <Text style={[s.cell, s.h, { flex: 1.5 }]}>{T.sign}</Text>
        <Text style={[s.cell, s.h, { width: 38, textAlign: 'center' }]}>{T.house}</Text>
        <Text style={[s.cell, s.h, { flex: 1.6 }]}>{T.nakshatra}</Text>
        <Text style={[s.cell, s.h, { width: 70, textAlign: 'right' }]}> </Text>
      </View>
      {planets.map((p) => (
        <View key={p.name} style={s.row}>
          <View style={{ flex: 1.1 }}>
            <Text style={s.planet}>{p.name}</Text>
            <Text style={s.planetHi}>{p.name_hi}</Text>
          </View>
          <View style={{ flex: 1.5 }}>
            <Text style={s.cellMain}>{p.sign}</Text>
            <Text style={s.cellHi}>{p.sign_hi}</Text>
          </View>
          <Text style={[s.cellMain, { width: 38, textAlign: 'center' }]}>{p.house}</Text>
          <View style={{ flex: 1.6 }}>
            <Text style={s.cellMain}>{p.nakshatra}</Text>
            <Text style={s.cellHi}>P{p.pada}</Text>
          </View>
          <View style={{ width: 70, alignItems: 'flex-end' }}>
            <DignityPill dignity={p.dignity} label={D[p.dignity]} />
            {p.retrograde ? <Text style={s.r}>R</Text> : null}
          </View>
        </View>
      ))}
    </View>
  );
}

function DignityPill({
  dignity,
  label,
}: {
  dignity: PlanetPosition['dignity'];
  label: string;
}) {
  const map = {
    exalted: { fg: colors.exalted, bg: colors.exaltedBg },
    debilitated: { fg: colors.debilitated, bg: colors.debilitatedBg },
    own_sign: { fg: colors.ownSign, bg: colors.ownSignBg },
    neutral: { fg: colors.maroon, bg: 'rgba(91,31,0,0.06)' },
  } as const;
  const p = map[dignity];
  return (
    <View style={[s.pill, { backgroundColor: p.bg }]}>
      <Text style={[s.pillText, { color: p.fg }]}>{label}</Text>
    </View>
  );
}

const s = StyleSheet.create({
  wrap: { borderTopWidth: 1, borderColor: colors.border, marginTop: 4 },
  headerRow: {
    flexDirection: 'row',
    paddingVertical: 6,
    borderBottomWidth: 1,
    borderColor: colors.border,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderColor: colors.border,
  },
  cell: { ...text.body, color: colors.maroon },
  h: { ...text.small, color: colors.saffronDeep, fontFamily: 'Spectral-SemiBold' },
  planet: { ...text.bodySemi, fontSize: 13, color: colors.maroon },
  planetHi: { ...text.hiSmall, color: colors.maroon },
  cellMain: { ...text.body, fontSize: 13, color: colors.maroon },
  cellHi: { ...text.hiSmall, color: colors.maroon },
  pill: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 999,
  },
  pillText: { ...text.small, fontSize: 10, fontFamily: 'Spectral-SemiBold' },
  r: {
    marginTop: 3,
    fontSize: 10,
    color: colors.saffron,
    fontFamily: 'Spectral-SemiBold',
  },
});
