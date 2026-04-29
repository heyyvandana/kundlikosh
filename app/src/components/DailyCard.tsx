// "Today's Reading" — Tarabala + Chandra Bala + composite verdict for the user.
// Real Vedic transit data, not horoscope templates.
import React from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from './PaperCard';
import type { DailyResponse } from '@/api/types';

interface Props {
  data: DailyResponse;
}

const QUALITY_COLOR: Record<string, string> = {
  very_auspicious: '#1B6B2A',
  auspicious: '#2E7D32',
  mixed: '#9C6B16',
  inauspicious: '#9A3D1F',
  very_inauspicious: '#7E1B14',
};

export function DailyCard({ data }: Props) {
  const t = data.tarabala;
  const cb = data.chandra_bala;
  const verdictColor = data.overall_score >= 6 ? colors.gold : data.overall_score >= 4 ? colors.saffron : colors.maroon;

  return (
    <PaperCard inset={16}>
      <View style={s.headerRow}>
        <Text style={s.scoreBig}>{data.overall_score}<Text style={s.scoreOf}>/10</Text></Text>
        <View style={{ flex: 1, marginLeft: 12 }}>
          <Text style={[s.verdictEn, { color: verdictColor }]}>{data.verdict_en}</Text>
          <Text style={s.verdictHi}>{data.verdict_hi}</Text>
        </View>
      </View>

      <View style={s.section}>
        <View style={s.metricHeader}>
          <Text style={s.metricLabelEn}>Tarabala</Text>
          <Text style={s.metricLabelHi}>तारबल</Text>
          <Text style={[s.metricBadge, { backgroundColor: QUALITY_COLOR[t.quality] }]}>
            {t.position} · {t.name}
          </Text>
        </View>
        <Text style={s.metricNoteEn}>{t.note_en}</Text>
        <Text style={s.metricNoteHi}>{t.note_hi}</Text>
      </View>

      <View style={s.section}>
        <View style={s.metricHeader}>
          <Text style={s.metricLabelEn}>Chandra Bala</Text>
          <Text style={s.metricLabelHi}>चन्द्र बल</Text>
          <Text
            style={[
              s.metricBadge,
              { backgroundColor: cb.favorable ? '#2E7D32' : '#9A3D1F' },
            ]}
          >
            {cb.position}H · {cb.favorable ? 'favourable' : 'weak'}
          </Text>
        </View>
        <Text style={s.metricNoteEn}>
          {cb.favorable
            ? `Moon transits a supportive house from your natal Moon. Emotional momentum is with you.`
            : `Moon transits a heavy house from your natal Moon. Pace yourself; rest is medicine today.`}
        </Text>
      </View>
    </PaperCard>
  );
}

const s = StyleSheet.create({
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderColor: colors.border,
    marginBottom: 8,
  },
  scoreBig: {
    fontFamily: 'Cormorant-Bold',
    fontSize: 44,
    color: colors.saffronDeep,
    lineHeight: 46,
  },
  scoreOf: { fontSize: 18, color: colors.maroon },
  verdictEn: { ...text.cardTitle, fontSize: 18 },
  verdictHi: { ...text.hi, color: colors.maroon, marginTop: 2 },
  section: { paddingVertical: 8 },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  metricLabelEn: {
    ...text.small,
    color: colors.saffronDeep,
    fontFamily: 'Spectral-SemiBold',
  },
  metricLabelHi: { ...text.small, color: colors.maroon, fontFamily: 'TiroDevanagari' },
  metricBadge: {
    color: '#FFF8E1',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 999,
    fontSize: 11,
    overflow: 'hidden',
    marginLeft: 'auto',
    fontFamily: 'Spectral-SemiBold',
  },
  metricNoteEn: { ...text.body, color: colors.maroon },
  metricNoteHi: { ...text.hi, color: colors.maroon, marginTop: 1 },
});
