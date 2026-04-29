// "Today's Panchang" card — the 5-limb Vedic calendar shown on the home screen.
import React from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from './PaperCard';
import type { PanchangResponse } from '@/api/types';

interface Props {
  data: PanchangResponse;
}

export function PanchangCard({ data }: Props) {
  const rows: Array<[string, string, string, string]> = [
    ['Tithi', 'तिथि', `${data.tithi_name} (${data.paksha})`, `${data.tithi_name_hi} · ${data.paksha_hi} पक्ष`],
    ['Vara', 'वार', `${data.weekday} · ${data.weekday_lord}`, data.weekday_hi],
    ['Nakshatra', 'नक्षत्र', `${data.nakshatra} · ${data.nakshatra_lord}`, data.nakshatra_hi],
    ['Yoga', 'योग', data.yoga, data.yoga_hi],
    ['Karana', 'करण', data.karana, data.karana_hi],
  ];

  return (
    <PaperCard inset={16}>
      <View style={s.headerRow}>
        <Text style={s.dateBig}>{formatDate(data.date)}</Text>
      </View>
      {rows.map(([labelEn, labelHi, valEn, valHi]) => (
        <View key={labelEn} style={s.row}>
          <View style={s.labelCol}>
            <Text style={s.labelEn}>{labelEn}</Text>
            <Text style={s.labelHi}>{labelHi}</Text>
          </View>
          <View style={s.valueCol}>
            <Text style={s.valueEn}>{valEn}</Text>
            <Text style={s.valueHi}>{valHi}</Text>
          </View>
        </View>
      ))}
    </PaperCard>
  );
}

function formatDate(iso: string): string {
  const [y, m, d] = iso.split('-').map((x) => parseInt(x, 10));
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ];
  return `${d} ${months[m - 1]} ${y}`;
}

const s = StyleSheet.create({
  headerRow: {
    alignItems: 'center',
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderColor: colors.border,
    marginBottom: 6,
  },
  dateBig: {
    ...text.cardTitle,
    fontSize: 18,
    color: colors.saffronDeep,
  },
  row: {
    flexDirection: 'row',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderColor: colors.border,
    alignItems: 'flex-start',
  },
  labelCol: { flexBasis: 96 },
  valueCol: { flex: 1 },
  labelEn: { ...text.small, color: colors.saffronDeep, fontFamily: 'Spectral-SemiBold' },
  labelHi: { ...text.small, color: colors.maroon, fontFamily: 'TiroDevanagari', marginTop: 1 },
  valueEn: { ...text.body, color: colors.maroon },
  valueHi: { ...text.hi, color: colors.maroon, marginTop: 1 },
});
