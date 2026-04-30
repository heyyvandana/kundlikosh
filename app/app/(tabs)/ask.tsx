// Ask — AI Astrologer chat (Gemini Flash, grounded in chart + life-story).
import React, { useRef, useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api } from '@/api/client';
import type { ChatTurn } from '@/api/types';
import { PaperCard } from '@/components/PaperCard';
import { SectionTitle } from '@/components/SectionTitle';
import { colors } from '@/theme/colors';
import { text } from '@/theme/typography';
import { useProfile } from '@/store/profile';

interface Message {
  role: 'user' | 'model';
  text: string;
  isError?: boolean;
}

const SUGGESTED_EN = [
  'When will I get married?',
  'What does my career look like in the next 5 years?',
  'What remedies should I do right now?',
  'Tell me about my current Mahadasha.',
];

export default function Ask() {
  const insets = useSafeAreaInsets();
  const { profile } = useProfile();
  const scrollRef = useRef<ScrollView | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);

  const ask = async (q: string) => {
    if (!profile?.birth || !q.trim() || sending) return;
    const question = q.trim();

    const next: Message[] = [...messages, { role: 'user', text: question }];
    setMessages(next);
    setInput('');
    setSending(true);

    try {
      const history: ChatTurn[] = next
        .slice(0, -1)
        .map((m) => ({ role: m.role, text: m.text }));
      const res = await api.chat({
        ...profile.birth,
        message: question,
        history,
        locale: 'en',
      });
      setMessages((prev) => [...prev, { role: 'model', text: res.data.reply }]);
    } catch (e: any) {
      const detail =
        e?.response?.data?.detail ??
        e?.message ??
        'Something went wrong reaching the AI Astrologer.';
      setMessages((prev) => [
        ...prev,
        { role: 'model', text: detail, isError: true },
      ]);
    } finally {
      setSending(false);
      setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 50);
    }
  };

  return (
    <LinearGradient colors={[colors.indigoDeep, colors.indigo]} style={s.bg}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={insets.bottom + 60}
      >
        <View style={{ paddingHorizontal: 16, paddingTop: insets.top + 12 }}>
          <SectionTitle en="Ask the Sky" hi="आकाश से पूछें" />
        </View>

        <ScrollView
          ref={scrollRef}
          style={s.scroll}
          contentContainerStyle={{ padding: 16, paddingBottom: 24 }}
        >
          {messages.length === 0 && (
            <PaperCard inset={20}>
              <Text style={s.title}>AI Astrologer</Text>
              <Text style={s.subtitle}>एआई ज्योतिषी</Text>
              <Text style={s.body}>
                A Vedic-trained chat grounded in your real chart and life story.
                Ask about timing, career, marriage, remedies, doshas, dashas — anything.
              </Text>
              <Text style={[s.body, { marginTop: 14, color: colors.maroon }]}>
                Suggested questions:
              </Text>
              {SUGGESTED_EN.map((q) => (
                <Pressable
                  key={q}
                  style={s.suggest}
                  onPress={() => ask(q)}
                  disabled={sending}
                >
                  <Text style={s.suggestText}>{q}</Text>
                </Pressable>
              ))}
            </PaperCard>
          )}

          {messages.map((m, i) => (
            <View
              key={i}
              style={[s.bubble, m.role === 'user' ? s.bubbleUser : s.bubbleModel]}
            >
              <Text
                style={[
                  s.bubbleText,
                  m.role === 'user' ? s.bubbleTextUser : s.bubbleTextModel,
                  m.isError && { color: colors.maroon },
                ]}
              >
                {m.text}
              </Text>
            </View>
          ))}

          {sending && (
            <View style={[s.bubble, s.bubbleModel]}>
              <ActivityIndicator color={colors.saffronDeep} />
            </View>
          )}
        </ScrollView>

        <View style={[s.inputRow, { paddingBottom: insets.bottom + 8 }]}>
          <TextInput
            style={s.input}
            placeholder="Ask the sky…"
            placeholderTextColor="#8a7a5a"
            value={input}
            onChangeText={setInput}
            editable={!sending && !!profile?.birth}
            multiline
            onSubmitEditing={() => ask(input)}
            returnKeyType="send"
          />
          <Pressable
            style={[s.sendBtn, (!input.trim() || sending) && { opacity: 0.4 }]}
            onPress={() => ask(input)}
            disabled={!input.trim() || sending}
          >
            <Text style={s.sendBtnText}>Ask</Text>
          </Pressable>
        </View>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const s = StyleSheet.create({
  bg: { flex: 1 },
  scroll: { flex: 1 },
  title: { ...text.cardTitle, fontSize: 22, color: colors.saffronDeep, textAlign: 'center' },
  subtitle: {
    ...text.cardTitleHi, fontSize: 18, color: colors.saffronDeep,
    textAlign: 'center', marginTop: 4,
  },
  body: { ...text.body, color: colors.maroon, marginTop: 8 },
  suggest: {
    backgroundColor: colors.cream,
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 14,
    marginTop: 8,
    borderWidth: 1,
    borderColor: colors.saffronDeep,
  },
  suggestText: { ...text.body, color: colors.indigoDeep },
  bubble: {
    maxWidth: '88%',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 14,
    marginTop: 8,
  },
  bubbleUser: {
    alignSelf: 'flex-end',
    backgroundColor: colors.saffronDeep,
  },
  bubbleModel: {
    alignSelf: 'flex-start',
    backgroundColor: colors.cream,
    borderWidth: 1,
    borderColor: colors.gold,
  },
  bubbleText: { ...text.body, fontSize: 15, lineHeight: 22 },
  bubbleTextUser: { color: '#fff' },
  bubbleTextModel: { color: colors.indigoDeep },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: 12,
    paddingTop: 8,
    backgroundColor: 'rgba(0,0,0,0.25)',
    borderTopWidth: 1,
    borderTopColor: 'rgba(255,255,255,0.08)',
  },
  input: {
    flex: 1,
    minHeight: 40,
    maxHeight: 110,
    backgroundColor: colors.cream,
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 8,
    color: colors.indigoDeep,
    fontFamily: text.body.fontFamily,
    fontSize: 15,
  },
  sendBtn: {
    backgroundColor: colors.saffronDeep,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 12,
    marginLeft: 8,
  },
  sendBtnText: { ...text.bodySemi, color: '#fff', fontSize: 15 },
});
