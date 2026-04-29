// Thin axios client around the FastAPI engine.
// Base URL comes from app.json `extra.apiBaseUrl`; can be overridden at runtime
// via setApiBase() — handy for local testing against http://10.0.2.2:8000 (Android emulator)
// or your phone's LAN IP.

import axios, { AxiosInstance } from 'axios';
import Constants from 'expo-constants';
import type {
  BirthInput,
  ChartResponse,
  CompatibilityResponse,
  DashaResponse,
  GunaMilanInput,
  DailyInput,
  DailyResponse,
  LifeStoryInput,
  LifeStoryResponse,
  PanchangInput,
  PanchangResponse,
  YogasResponse,
} from './types';

const DEFAULT_BASE =
  (Constants.expoConfig?.extra as { apiBaseUrl?: string } | undefined)?.apiBaseUrl ??
  'http://localhost:8000';

let baseURL = DEFAULT_BASE;

let instance: AxiosInstance = axios.create({ baseURL, timeout: 20_000 });

export const setApiBase = (url: string) => {
  baseURL = url;
  instance = axios.create({ baseURL, timeout: 20_000 });
};

export const getApiBase = () => baseURL;

export const api = {
  health: () => instance.get<{ ok: boolean; service: string; version: string }>('/health'),
  chart: (body: BirthInput) => instance.post<ChartResponse>('/chart', body),
  dasha: (body: BirthInput, num_mahadashas = 5) =>
    instance.post<DashaResponse>(`/dasha?num_mahadashas=${num_mahadashas}`, body),
  yogas: (body: BirthInput) => instance.post<YogasResponse>('/yogas', body),
  compatibility: (body: GunaMilanInput) =>
    instance.post<CompatibilityResponse>('/compatibility', body),
  panchang: (body: PanchangInput) => instance.post<PanchangResponse>('/panchang', body),
  daily: (body: DailyInput) => instance.post<DailyResponse>('/daily', body),
  lifeStory: (body: LifeStoryInput) =>
    instance.post<LifeStoryResponse>('/life-story', body),
};
