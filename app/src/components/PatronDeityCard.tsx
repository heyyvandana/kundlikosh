// Patron deity card — centerpiece of home screen. Currently illustrates Brahma;
// other deities will land in deity/index.ts as we add their SVGs.
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import type { PatronDeity } from '@/api/types';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from './PaperCard';
import { BrahmaSVG } from './BrahmaSVG';

interface Props {
  deity: PatronDeity;
}

export function PatronDeityCard({ deity }: Props) {
  return (
    <PaperCard inset={20}>
      <View style={s.svgWrap}>
        {/* For Phase 1 we ship Brahma; other deities reuse a generic devotional medallion. */}
        {deity.deity === 'Brahma' ? <BrahmaSVG size={150} /> : <DefaultDeityMedallion size={150} />}
      </View>
      <Text style={s.name}>{deity.deity}</Text>
      <Text style={s.nameHi}>{deity.deity_hi}</Text>
      <Text style={s.line}>
        “The cosmic creator. Born under <Text style={s.lineEm}>{deity.nakshatra}</Text>, you carry
        the seed of creation — creative, nurturing, quietly powerful.”
      </Text>
      <View style={s.metaRow}>
        <MetaCol label="Nakshatra" value={deity.nakshatra} valueHi={deity.nakshatra_hi} />
        <MetaCol label="Symbol" value={deity.symbol} />
        <MetaCol label="Lord" value={deity.ruling_planet} />
      </View>
    </PaperCard>
  );
}

function MetaCol({ label, value, valueHi }: { label: string; value: string; valueHi?: string }) {
  return (
    <View style={s.metaCol}>
      <Text style={s.metaLabel}>{label}</Text>
      <Text style={s.metaValue}>{value}</Text>
      {valueHi ? <Text style={s.metaValueHi}>{valueHi}</Text> : null}
    </View>
  );
}

function DefaultDeityMedallion({ size }: { size: number }) {
  // Simple sun-disc medallion for deities we haven't custom-illustrated yet
  return (
    <View
      style={{
        width: size,
        height: size,
        borderRadius: size / 2,
        backgroundColor: colors.goldBright,
        borderWidth: 2,
        borderColor: colors.maroon,
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Text style={{ fontSize: 56, color: colors.maroon }}>ॐ</Text>
    </View>
  );
}

const s = StyleSheet.create({
  svgWrap: { alignItems: 'center', marginVertical: 6 },
  name: {
    textAlign: 'center',
    color: colors.saffronDeep,
    marginTop: 8,
    ...text.cardTitle,
  },
  nameHi: {
    textAlign: 'center',
    color: colors.maroon,
    marginBottom: 8,
    ...text.cardTitleHi,
  },
  line: {
    textAlign: 'center',
    color: colors.maroon,
    paddingHorizontal: 8,
    ...text.bodyItalic,
  },
  lineEm: { fontFamily: 'Cormorant-Bold', fontStyle: 'normal' },
  metaRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 14,
  },
  metaCol: { alignItems: 'center', flex: 1 },
  metaLabel: { ...text.small, color: colors.saffronDeep, marginBottom: 2 },
  metaValue: { ...text.bodySemi, color: colors.maroon, fontSize: 13 },
  metaValueHi: { ...text.hiSmall, color: colors.maroon, marginTop: 2 },
});
