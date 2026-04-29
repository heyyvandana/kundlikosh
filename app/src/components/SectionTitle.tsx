import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';

interface Props {
  en: string;
  hi: string;
}

export function SectionTitle({ en, hi }: Props) {
  return (
    <View style={s.row}>
      <View style={s.line} />
      <Text style={s.text}>
        <Text>{en}</Text>
        <Text style={s.dot}> · </Text>
        <Text style={s.hi}>{hi}</Text>
      </Text>
      <View style={s.line} />
    </View>
  );
}

const s = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', marginVertical: 16, paddingHorizontal: 4 },
  line: { flex: 1, height: 1, backgroundColor: colors.gold, opacity: 0.6 },
  text: {
    paddingHorizontal: 12,
    color: colors.saffronDeep,
    ...text.section,
  },
  dot: { color: colors.gold },
  hi: { ...text.hi, color: colors.maroon },
});
