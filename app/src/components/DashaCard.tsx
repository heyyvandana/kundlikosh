import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import type { DashaResponse } from '@/api/types';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from './PaperCard';
import { strings, useLocale } from '@/i18n';

interface Props {
  dasha: DashaResponse;
}

const ymd = (s: string) => s.split('T')[0];

export function DashaCard({ dasha }: Props) {
  const locale = useLocale((s) => s.locale);
  const T = strings[locale];
  const md = dasha.current.mahadasha;
  const ad = dasha.current.antardasha;
  const upcoming = dasha.timeline.slice(1, 3);

  return (
    <PaperCard inset={16}>
      <View style={s.head}>
        <Text style={s.title}>{T.currentlyRunning}</Text>
        <Text style={s.titleHi}>{T.vimshottari}</Text>
      </View>
      <Row primary={`${md.planet} Mahadasha`} secondary={`${ymd(md.start)} → ${ymd(md.end)}`} years={md.years} />
      {ad ? (
        <Row primary={`${ad.planet} Antardasha`} secondary={`${ymd(ad.start)} → ${ymd(ad.end)}`} years={ad.years} small />
      ) : null}

      <Text style={[s.title, { marginTop: 14 }]}>{T.nextMahadashas}</Text>
      {upcoming.map((u) => (
        <Row
          key={u.start}
          primary={u.planet}
          secondary={`${ymd(u.start)} → ${ymd(u.end)}`}
          years={u.years}
        />
      ))}
    </PaperCard>
  );
}

function Row({
  primary,
  secondary,
  years,
  small,
}: {
  primary: string;
  secondary: string;
  years: number;
  small?: boolean;
}) {
  return (
    <View style={s.row}>
      <View style={{ flex: 1 }}>
        <Text style={[s.primary, small && { fontSize: 14 }]}>{primary}</Text>
        <Text style={s.secondary}>{secondary}</Text>
      </View>
      <Text style={s.years}>{years} yr</Text>
    </View>
  );
}

const s = StyleSheet.create({
  head: { marginBottom: 8 },
  title: { ...text.section, fontSize: 16, color: colors.saffronDeep },
  titleHi: { ...text.hi, color: colors.maroon },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 6,
    borderBottomWidth: 1,
    borderColor: colors.border,
  },
  primary: { ...text.bodySemi, fontSize: 15, color: colors.maroon },
  secondary: { ...text.small, color: colors.saffronDeep },
  years: { ...text.bodySemi, color: colors.saffron, fontSize: 13, marginLeft: 8 },
});
