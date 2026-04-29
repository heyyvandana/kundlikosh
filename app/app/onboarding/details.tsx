// Single-page form to collect: name, DOB, time, latitude, longitude.
// Phase 1 keeps it manual (no geocoding, no map picker) — pre-fill Surat for
// Vandana's test case so first run is friction-free.
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  Pressable,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors } from '@/theme/colors';
import { strings, useLocale } from '@/i18n';
import { api } from '@/api/client';
import { useProfile } from '@/store/profile';

export default function Details() {
  const insets = useSafeAreaInsets();
  const locale = useLocale((s) => s.locale);
  const T = strings[locale].onb;
  const saveProfile = useProfile((s) => s.saveProfile);

  const [name, setName] = useState('');
  const [date, setDate] = useState('2003-12-08');
  const [time, setTime] = useState('13:30');
  const [latStr, setLatStr] = useState('21.1702');
  const [lonStr, setLonStr] = useState('72.8311');
  const [tz, setTz] = useState('Asia/Kolkata');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const onSubmit = async () => {
    setErr(null);
    if (!name.trim()) {
      setErr(locale === 'hi' ? 'कृपया अपना नाम लिखें' : 'Please enter your name');
      return;
    }
    const lat = Number(latStr);
    const lon = Number(lonStr);
    if (Number.isNaN(lat) || Number.isNaN(lon)) {
      setErr(locale === 'hi' ? 'अक्षांश/देशांतर सही नहीं है' : 'Latitude / longitude looks invalid');
      return;
    }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      setErr(locale === 'hi' ? 'तिथि का प्रारूप: YYYY-MM-DD' : 'Date must be YYYY-MM-DD');
      return;
    }
    if (!/^\d{2}:\d{2}$/.test(time)) {
      setErr(locale === 'hi' ? 'समय का प्रारूप: HH:MM' : 'Time must be HH:MM (24h)');
      return;
    }

    setBusy(true);
    try {
      const birth = {
        name: name.trim(),
        date,
        time,
        timezone: tz,
        latitude: lat,
        longitude: lon,
      };
      const { data } = await api.chart(birth);
      await saveProfile({ birth, chart: data, savedAt: new Date().toISOString() });
      router.replace('/(tabs)/home');
    } catch (e) {
      const msg =
        e && typeof e === 'object' && 'message' in e ? String((e as { message: unknown }).message) : 'Network error';
      setErr(msg);
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
          contentContainerStyle={[
            s.container,
            { paddingTop: insets.top + 24, paddingBottom: insets.bottom + 32 },
          ]}
          keyboardShouldPersistTaps="handled"
        >
          <Text style={s.crumb}>1 / 1</Text>

          <Text style={s.h1}>{T.nameTitle}</Text>
          <TextInput
            style={s.input}
            placeholder={T.namePh}
            placeholderTextColor="rgba(245,230,202,0.4)"
            value={name}
            onChangeText={setName}
            autoCapitalize="words"
          />

          <Text style={s.h2}>{T.dobTitle}</Text>
          <Text style={s.hint}>{T.dobHint}</Text>
          <View style={s.row}>
            <Field label={T.dateLabel} value={date} onChangeText={setDate} placeholder="YYYY-MM-DD" flex={1.2} />
            <Field label={T.timeLabel} value={time} onChangeText={setTime} placeholder="HH:MM" flex={0.9} />
          </View>

          <Text style={s.h2}>{T.placeTitle}</Text>
          <View style={s.row}>
            <Field label={T.latLabel} value={latStr} onChangeText={setLatStr} placeholder="21.1702" flex={1} />
            <Field label={T.lonLabel} value={lonStr} onChangeText={setLonStr} placeholder="72.8311" flex={1} />
          </View>
          <Field label={T.tzLabel} value={tz} onChangeText={setTz} placeholder="Asia/Kolkata" />

          {err ? <Text style={s.err}>{err}</Text> : null}

          <Pressable
            style={({ pressed }) => [s.cta, (pressed || busy) && { opacity: 0.7 }]}
            disabled={busy}
            onPress={onSubmit}
          >
            <Text style={s.ctaText}>{busy ? T.computing : T.next}</Text>
          </Pressable>
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
  flex,
}: {
  label: string;
  value: string;
  onChangeText: (v: string) => void;
  placeholder: string;
  flex?: number;
}) {
  return (
    <View style={[s.field, flex !== undefined && { flex }]}>
      <Text style={s.label}>{label}</Text>
      <TextInput
        style={s.input}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor="rgba(245,230,202,0.4)"
        autoCapitalize="none"
        autoCorrect={false}
      />
    </View>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  container: { paddingHorizontal: 24 },
  crumb: { color: colors.gold, fontFamily: 'Spectral-SemiBold', fontSize: 12, marginBottom: 16 },
  h1: {
    color: colors.goldBright,
    fontFamily: 'Cormorant-SemiBold',
    fontSize: 22,
    marginBottom: 8,
  },
  h2: {
    color: colors.goldBright,
    fontFamily: 'Cormorant-SemiBold',
    fontSize: 18,
    marginTop: 22,
    marginBottom: 6,
  },
  hint: {
    color: 'rgba(245,230,202,0.7)',
    fontFamily: 'Cormorant-Italic',
    fontSize: 14,
    marginBottom: 8,
  },
  row: { flexDirection: 'row', gap: 10 },
  field: { marginTop: 10, flex: 1 },
  label: { color: colors.gold, fontFamily: 'Spectral-SemiBold', fontSize: 11, marginBottom: 4, letterSpacing: 0.5 },
  input: {
    backgroundColor: 'rgba(255,248,231,0.08)',
    borderWidth: 1,
    borderColor: 'rgba(201,162,39,0.4)',
    color: colors.offwhite,
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 10,
    fontFamily: 'Spectral-Regular',
    fontSize: 15,
  },
  err: {
    color: '#FF8E7A',
    fontFamily: 'Spectral-SemiBold',
    fontSize: 13,
    marginTop: 16,
    textAlign: 'center',
  },
  cta: {
    marginTop: 28,
    backgroundColor: colors.saffron,
    paddingVertical: 14,
    borderRadius: 999,
    borderWidth: 1.5,
    borderColor: colors.gold,
    alignItems: 'center',
  },
  ctaText: {
    color: colors.offwhite,
    fontFamily: 'Cormorant-Bold',
    fontSize: 17,
    letterSpacing: 1,
  },
});
