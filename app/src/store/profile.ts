// Persistent user profile (birth data + computed chart) stored in AsyncStorage.
import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import type { BirthInput, ChartResponse } from '@/api/types';

const KEY_PROFILE = '@kundlikosh/profile/v1';

export interface Profile {
  birth: BirthInput;
  chart?: ChartResponse;
  savedAt: string;
}

interface ProfileStore {
  profile: Profile | null;
  hydrated: boolean;
  hydrate: () => Promise<void>;
  saveProfile: (p: Profile) => Promise<void>;
  clearProfile: () => Promise<void>;
}

export const useProfile = create<ProfileStore>((set) => ({
  profile: null,
  hydrated: false,
  hydrate: async () => {
    try {
      const raw = await AsyncStorage.getItem(KEY_PROFILE);
      const profile = raw ? (JSON.parse(raw) as Profile) : null;
      set({ profile, hydrated: true });
    } catch {
      set({ profile: null, hydrated: true });
    }
  },
  saveProfile: async (profile) => {
    await AsyncStorage.setItem(KEY_PROFILE, JSON.stringify(profile));
    set({ profile });
  },
  clearProfile: async () => {
    await AsyncStorage.removeItem(KEY_PROFILE);
    set({ profile: null });
  },
}));
