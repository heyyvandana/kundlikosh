// Story tab — full classical phalit (past / present / future life narrative).
// Powered by /life-story endpoint.
import React, { useEffect, useState } from 'react';
import { LinearGradient } from 'expo-linear-gradient';
import { ActivityIndicator, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api } from '@/api/client';
import type { LifeStoryResponse, PhalitChapter } from '@/api/types';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { useProfile } from '@/store/profile';

const dignityColor: Record<PhalitChapter['dignity'], string> = {
  exalted: '#1B6B2A',
  own_sign: '#3F6E1A',
  neutral: '#5B1F00',
  debilitated: '#7E1B14',
};

function ChapterCard({ ch, kind }: { ch: PhalitChapter; kind: 'past' | 'current' | 'future' }) {
  const accent =
    kind === 'current' ? colors.saffronDeep : kind === 'past' ? colors.maroon : colors.indigoDeep;
  return (
    <View style={{ marginBottom: 14 }}>
      <PaperCard inset={16}>
        <View style={s.headerRow}>
          <View style={{ flex: 1 }}>
            <Text style={[s.lord, { color: accent }]}>{ch.lord} Mahadasha</Text>
            <Text style={s.lordHi}>{ch.lord_hi} महादशा</Text>
          </View>
          {kind === 'current' && (
            <View style={[s.pill, { backgroundColor: colors.saffronDeep }]}>
              <Text style={s.pillTxt}>Now • अभी</Text>
            </View>
          )}
        </View>

        <Text style={s.dates}>
          {fmt(ch.start)} → {fmt(ch.end)}   ·   {ch.duration_years} yrs
        </Text>
        <Text style={s.ages}>
          age {ch.start_age.toFixed(1)} → {ch.end_age.toFixed(1)}
        </Text>

        <View style={s.placementRow}>
          <Text style={s.place}>
            {ch.lord} in {ch.house}H · {ch.sign}
          </Text>
          <View style={[s.dignityChip, { backgroundColor: dignityColor[ch.dignity] }]}>
            <Text style={s.dignityChipTxt}>{ch.dignity_label_en.split(' (')[0]}</Text>
          </View>
        </View>
        <Text style={s.placeHi}>
          {ch.lord_hi} {ch.house}वें भाव में · {ch.sign_hi} · {ch.dignity_label_hi}
        </Text>

        <View style={s.divider} />

        {/* Themes */}
        <Text style={s.subhead}>Themes • मुख्य विषय</Text>
        {ch.themes_en.map((th, i) => (
          <Text key={i} style={s.theme}>
            • {th}{ch.themes_hi[i] ? `   (${ch.themes_hi[i]})` : ''}
          </Text>
        ))}

        <View style={s.divider} />

        {/* Narrative summary */}
        <Text style={s.subhead}>Reading • फलादेश</Text>
        <Text style={s.summary}>{ch.summary_en}</Text>
        <Text style={s.summaryHi}>{ch.summary_hi}</Text>

        {(ch.conjunctions.length > 0 || ch.aspects_received.length > 0) && (
          <View style={s.aspectBox}>
            {ch.conjunctions.length > 0 && (
              <Text style={s.aspectTxt}>
                ⊕ Conjoined: {ch.conjunctions.join(', ')}
              </Text>
            )}
            {ch.aspects_received.length > 0 && (
              <Text style={s.aspectTxt}>
                ◊ Aspect from: {ch.aspects_received.join(', ')}
              </Text>
            )}
          </View>
        )}

        {/* Timing notes — only for current chapter */}
        {kind === 'current' && ch.timing_notes_en.length > 0 && (
          <>
            <View style={s.divider} />
            <Text style={s.subhead}>Sub-period turning points • अंतर्दशा</Text>
            {ch.timing_notes_en.slice(0, 9).map((t, i) => (
              <Text key={i} style={s.timing}>
                {t}
              </Text>
            ))}
          </>
        )}

        {/* Remedies */}
        <View style={s.divider} />
        <Text style={s.subhead}>Remedies • उपाय</Text>
        <Text style={s.remedy}>💎 {ch.remedies_en.gemstone}   ·   {ch.remedies_hi.gemstone}</Text>
        <Text style={s.remedy}>🕉 {ch.remedies_en.mantra}</Text>
        <Text style={s.remedy}>🪷 {ch.remedies_en.charity}</Text>
        <Text style={s.remedy}>📿 Fast: {ch.remedies_en.fast}</Text>
        <Text style={s.remedy}>🛕 Deity: {ch.remedies_en.deity}</Text>
      </PaperCard>
    </View>
  );
}

function fmt(iso: string): string {
  // YYYY-MM-DD → MMM YYYY
  const [y, m] = iso.split('-');
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return `${months[parseInt(m, 10) - 1]} ${y}`;
}

export default function Story() {
  const insets = useSafeAreaInsets();
  const profile = useProfile((s) => s.profile);
  const [data, setData] = useState<LifeStoryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!profile) return;
    let cancelled = false;
    (async () => {
      try {
        const r = await api.lifeStory({
          ...profile.birth,
          on_date: new Date().toISOString().slice(0, 10),
          num_future: 5,
        });
        if (!cancelled) setData(r.data);
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'failed to load';
        if (!cancelled) setError(msg);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [profile]);

  if (!profile) {
    return (
      <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
        <View style={s.center}>
          <Text style={s.intro}>Complete onboarding to see your life story.</Text>
        </View>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <ScrollView contentContainerStyle={{ padding: 16, paddingTop: insets.top + 12, paddingBottom: 32 }}>
        <SectionTitle en="Your Life Story" hi="आपका फलादेश" />

        {!data && !error && (
          <View style={s.center}>
            <ActivityIndicator color={colors.gold} />
            <Text style={s.loading}>Reading your dashas…</Text>
          </View>
        )}
        {error && (
          <PaperCard inset={16}>
            <Text style={s.errorTxt}>Could not load: {error}</Text>
          </PaperCard>
        )}

        {data && (
          <>
            <PaperCard inset={16}>
              <Text style={s.subhead}>Chart Signature • जन्म-कुंडली का सार</Text>
              <Text style={s.summary}>{data.overall_signature_en}</Text>
              <Text style={s.summaryHi}>{data.overall_signature_hi}</Text>
            </PaperCard>

            {data.current && (
              <>
                <Text style={s.section}>● Now Running</Text>
                <Text style={s.sectionHi}>● वर्तमान दशा</Text>
                <ChapterCard ch={data.current} kind="current" />
              </>
            )}

            {data.future.length > 0 && (
              <>
                <Text style={s.section}>→ The Future</Text>
                <Text style={s.sectionHi}>→ भविष्य के अध्याय</Text>
                {data.future.map((c) => (
                  <ChapterCard key={c.start} ch={c} kind="future" />
                ))}
              </>
            )}

            {data.past.length > 0 && (
              <>
                <Text style={s.section}>← The Past</Text>
                <Text style={s.sectionHi}>← पूर्व के अध्याय</Text>
                {data.past.map((c) => (
                  <ChapterCard key={c.start} ch={c} kind="past" />
                ))}
              </>
            )}
          </>
        )}
      </ScrollView>
    </LinearGradient>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  center: { alignItems: 'center', padding: 24 },
  loading: { ...text.body, color: colors.cream, marginTop: 12 },
  intro: { ...text.body, color: colors.cream, textAlign: 'center' },
  errorTxt: { ...text.body, color: '#7E1B14' },

  section: {
    ...text.cardTitle,
    color: colors.gold,
    fontSize: 22,
    marginTop: 14,
    marginBottom: 0,
    paddingHorizontal: 4,
  },
  sectionHi: {
    ...text.cardTitleHi,
    color: colors.cream,
    fontSize: 16,
    marginBottom: 8,
    paddingHorizontal: 4,
  },

  headerRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  lord: { ...text.cardTitle, fontSize: 22 },
  lordHi: { ...text.cardTitleHi, color: colors.maroon, fontSize: 16, marginTop: -2 },

  pill: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 14 },
  pillTxt: { color: colors.cream, fontFamily: 'Spectral-SemiBold', fontSize: 11 },

  dates: { ...text.body, color: colors.maroon, marginTop: 6 },
  ages: { ...text.small, color: colors.saffronDeep, fontStyle: 'italic' },

  placementRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 8,
    flexWrap: 'wrap',
  },
  place: { ...text.body, color: colors.indigoDeep, flex: 1, marginRight: 8 },
  placeHi: { ...text.hi, color: colors.indigoDeep, marginTop: 2 },
  dignityChip: { paddingHorizontal: 10, paddingVertical: 3, borderRadius: 10 },
  dignityChipTxt: { color: '#fff', fontFamily: 'Spectral-SemiBold', fontSize: 11 },

  divider: { height: 1, backgroundColor: 'rgba(91,31,0,0.18)', marginVertical: 10 },

  subhead: { ...text.cardTitle, color: colors.saffronDeep, fontSize: 14, marginBottom: 4 },
  theme: { ...text.body, color: colors.maroon, marginBottom: 2 },

  summary: { ...text.body, color: colors.indigoDeep, lineHeight: 21 },
  summaryHi: { ...text.hi, color: colors.maroon, marginTop: 4, lineHeight: 22 },

  aspectBox: {
    marginTop: 8,
    padding: 8,
    backgroundColor: 'rgba(200,80,26,0.07)',
    borderRadius: 6,
  },
  aspectTxt: { ...text.small, color: colors.maroon, marginBottom: 2 },

  timing: { ...text.small, color: colors.indigoDeep, marginBottom: 3, fontFamily: 'Spectral-Regular' },

  remedy: { ...text.body, color: colors.maroon, marginBottom: 3 },
});
