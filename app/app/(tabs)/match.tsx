// Compatibility tab — partner birth-data form -> Ashtakoot Guna Milan + Manglik balance.
import React, { useState } from 'react';
import {
  ScrollView,
  Text,
  View,
  StyleSheet,
  TextInput,
  Pressable,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';
import { useProfile } from '@/store/profile';
import { api } from '@/api/client';
import type { CompatibilityResponse } from '@/api/types';

export default function Match() {
  const insets = useSafeAreaInsets();
  const profile = useProfile((s) => s.profile);

  const [pName, setPName] = useState('');
  const [pDate, setPDate] = useState('2001-08-07');
  const [pTime, setPTime] = useState('06:30');
  const [pLat, setPLat] = useState('22.3072');
  const [pLon, setPLon] = useState('73.1812');
  const [pTz, setPTz] = useState('Asia/Kolkata');

  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [result, setResult] = useState<CompatibilityResponse | null>(null);

  const onSubmit = async () => {
    if (!profile?.birth) return;
    setErr(null);
    if (!pName.trim()) {
      setErr('Please enter your partner’s name');
      return;
    }
    const lat = Number(pLat);
    const lon = Number(pLon);
    if (Number.isNaN(lat) || Number.isNaN(lon)) {
      setErr('Latitude / longitude looks invalid');
      return;
    }
    setBusy(true);
    setResult(null);
    try {
      const { data } = await api.compatibility({
        bride: profile.birth,
        groom: {
          name: pName.trim(),
          date: pDate,
          time: pTime,
          timezone: pTz,
          latitude: lat,
          longitude: lon,
        },
      });
      setResult(data);
    } catch (e) {
      setErr(
        e && typeof e === 'object' && 'message' in e
          ? String((e as { message: unknown }).message)
          : 'Network error',
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        style={{ flex: 1 }}
      >
        <ScrollView
          contentContainerStyle={{
            padding: 16,
            paddingTop: insets.top + 12,
            paddingBottom: insets.bottom + 24,
          }}
          keyboardShouldPersistTaps="handled"
        >
          <SectionTitle en="Guna Milan" hi="गुण मिलन" />
          <PaperCard inset={16}>
            <Text style={s.intro}>
              The 36-point Vedic compatibility system. Enter your partner’s birth details
              and we’ll compute all 8 kootas + Mangal Dosha balance using Parashari rules.
            </Text>
          </PaperCard>

          <SectionTitle en="Partner’s details" hi="साथी का विवरण" />
          <PaperCard inset={16}>
            <Field label="Name" value={pName} onChangeText={setPName} placeholder="Full name" />
            <View style={s.row2}>
              <Field label="Birth date" value={pDate} onChangeText={setPDate} placeholder="YYYY-MM-DD" />
              <Field label="Birth time" value={pTime} onChangeText={setPTime} placeholder="HH:MM" />
            </View>
            <View style={s.row2}>
              <Field label="Latitude" value={pLat} onChangeText={setPLat} placeholder="22.3072" />
              <Field label="Longitude" value={pLon} onChangeText={setPLon} placeholder="73.1812" />
            </View>
            <Field label="Time zone" value={pTz} onChangeText={setPTz} placeholder="Asia/Kolkata" />

            {err ? <Text style={s.err}>{err}</Text> : null}

            <Pressable
              style={({ pressed }) => [s.cta, (pressed || busy) && { opacity: 0.7 }]}
              onPress={onSubmit}
              disabled={busy}
            >
              <Text style={s.ctaText}>{busy ? 'Computing…' : 'Match'}</Text>
            </Pressable>
          </PaperCard>

          {result ? <Result data={result} /> : null}
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

function Field({
  label,
  value,
  onChangeText,
  placeholder,
}: {
  label: string;
  value: string;
  onChangeText: (v: string) => void;
  placeholder: string;
}) {
  return (
    <View style={{ marginBottom: 10, flex: 1 }}>
      <Text style={s.label}>{label}</Text>
      <TextInput
        style={s.input}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor="rgba(91,31,0,0.35)"
        autoCapitalize="none"
        autoCorrect={false}
      />
    </View>
  );
}

function Result({ data }: { data: CompatibilityResponse }) {
  const pct = (data.total_score / data.max_total) * 100;
  const verdict =
    pct >= 80
      ? { en: 'Excellent match', hi: 'उत्तम मेल', color: colors.exalted }
      : pct >= 65
      ? { en: 'Very good match', hi: 'बहुत अच्छा', color: colors.exalted }
      : pct >= 50
      ? { en: 'Acceptable match', hi: 'स्वीकार्य', color: colors.saffron }
      : { en: 'Weak match', hi: 'कमज़ोर', color: colors.debilitated };

  return (
    <>
      <SectionTitle en="Result" hi="परिणाम" />
      <PaperCard inset={20}>
        <View style={{ alignItems: 'center' }}>
          <Text style={s.scoreBig}>
            {data.total_score} <Text style={s.scoreSmall}>/ {data.max_total}</Text>
          </Text>
          <Text style={[s.verdict, { color: verdict.color }]}>{verdict.en}</Text>
          <Text style={s.verdictHi}>{verdict.hi}</Text>
        </View>
      </PaperCard>

      <SectionTitle en="8 Kootas breakdown" hi="आठ कूट" />
      <PaperCard inset={14}>
        {data.kootas.map((k) => (
          <View key={k.name} style={s.kRow}>
            <View style={{ flex: 1 }}>
              <Text style={s.kName}>{k.name}</Text>
              <Text style={s.kNote}>{k.note}</Text>
            </View>
            <Text
              style={[
                s.kScore,
                k.score === k.max_score && { color: colors.exalted },
                k.score === 0 && { color: colors.debilitated },
              ]}
            >
              {k.score}/{k.max_score}
            </Text>
          </View>
        ))}
      </PaperCard>

      <SectionTitle en="Mangal Dosha balance" hi="मंगल दोष" />
      <PaperCard inset={14}>
        <ManglikRow label="You" m={data.bride_manglik} />
        <View style={{ height: 8 }} />
        <ManglikRow label="Partner" m={data.groom_manglik} />
        <Text style={[s.balanced, data.manglik_balanced && { color: colors.exalted }]}>
          {data.manglik_balanced
            ? 'Balanced — both same Manglik status, dosha is mutually cancelled'
            : 'Imbalanced — one Manglik, one not. Remedies recommended.'}
        </Text>
      </PaperCard>
    </>
  );
}

function ManglikRow({ label, m }: { label: string; m: CompatibilityResponse['bride_manglik'] }) {
  return (
    <View>
      <Text style={s.mLabel}>{label}</Text>
      <Text style={s.mBody}>
        Mars in <Text style={s.bold}>{m.mars_sign}</Text> · house{' '}
        <Text style={s.bold}>{m.mars_house}</Text> · {m.mars_dignity}
      </Text>
      <Text style={s.mBody}>
        {m.is_manglik
          ? `Manglik (sources: ${m.sources.join(', ') || 'lagna'}${m.softened ? ', softened' : ''})`
          : 'Not Manglik'}
      </Text>
    </View>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  intro: { ...text.body, color: colors.maroon, textAlign: 'center' },
  row2: { flexDirection: 'row', gap: 10 },
  label: { ...text.small, color: colors.saffronDeep, fontFamily: 'Spectral-SemiBold', marginBottom: 4 },
  input: {
    backgroundColor: 'rgba(255,248,231,0.6)',
    borderWidth: 1,
    borderColor: 'rgba(91,31,0,0.25)',
    color: colors.maroon,
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 10,
    fontFamily: 'Spectral-Regular',
    fontSize: 15,
  },
  err: {
    color: colors.debilitated,
    fontFamily: 'Spectral-SemiBold',
    fontSize: 13,
    marginTop: 8,
    textAlign: 'center',
  },
  cta: {
    marginTop: 16,
    backgroundColor: colors.saffron,
    paddingVertical: 12,
    borderRadius: 999,
    borderWidth: 1.5,
    borderColor: colors.gold,
    alignItems: 'center',
  },
  ctaText: { color: colors.offwhite, fontFamily: 'Cormorant-Bold', fontSize: 17, letterSpacing: 1 },
  scoreBig: {
    fontFamily: 'Cormorant-Bold',
    fontSize: 56,
    color: colors.saffronDeep,
    lineHeight: 60,
  },
  scoreSmall: { fontFamily: 'Cormorant-Italic', fontSize: 22, color: colors.maroon },
  verdict: { ...text.cardTitle, fontSize: 22, marginTop: 4 },
  verdictHi: { ...text.cardTitleHi, fontSize: 18, color: colors.maroon },
  kRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderColor: colors.border,
  },
  kName: { ...text.bodySemi, color: colors.maroon, fontSize: 14 },
  kNote: { ...text.small, color: colors.saffronDeep, marginTop: 2 },
  kScore: { ...text.bodySemi, color: colors.maroon, fontSize: 16, marginLeft: 8 },
  mLabel: { ...text.small, color: colors.saffronDeep, fontFamily: 'Spectral-SemiBold' },
  mBody: { ...text.body, color: colors.maroon, marginTop: 2 },
  bold: { fontFamily: 'Spectral-SemiBold' },
  balanced: { ...text.body, color: colors.saffron, marginTop: 12, textAlign: 'center', fontFamily: 'Cormorant-Italic' },
});
