// API response types — mirror api/app.py shapes.
export interface PlanetPosition {
  name: string;
  name_hi: string;
  longitude: number;
  sign: string;
  sign_hi: string;
  sign_index: number;
  degree_in_sign: number;
  house: number;
  nakshatra: string;
  nakshatra_hi: string;
  pada: number;
  retrograde: boolean;
  dignity: 'exalted' | 'debilitated' | 'own_sign' | 'neutral';
}

export interface PatronDeity {
  nakshatra: string;
  nakshatra_hi: string;
  deity: string;
  deity_hi: string;
  symbol: string;
  yoni: string;
  ruling_planet: string;
}

export interface ChartResponse {
  name: string;
  birth_dt_utc: string;
  birth_dt_local: string;
  timezone: string;
  latitude: number;
  longitude: number;
  ayanamsa: number;
  lagna_longitude: number;
  lagna_sign: string;
  lagna_sign_hi: string;
  lagna_sign_index: number;
  lagna_degree_in_sign: number;
  lagna_nakshatra: string;
  lagna_pada: number;
  moon_sign: string;
  moon_sign_hi: string;
  moon_nakshatra: string;
  moon_nakshatra_hi: string;
  moon_nakshatra_lord: string;
  moon_pada: number;
  sun_sign: string;
  patron_deity: PatronDeity;
  planets: PlanetPosition[];
}

export interface DashaPeriod {
  planet: string;
  planet_hi?: string;
  start: string;
  end: string;
  years: number;
}

export interface DashaResponse {
  current: {
    mahadasha: DashaPeriod;
    antardasha?: DashaPeriod;
  };
  timeline: Array<{
    planet: string;
    start: string;
    end: string;
    years: number;
  }>;
}

export interface YogaItem {
  name: string;
  name_hi: string;
  category: string;
  description: string;
}

export interface YogasResponse {
  yogas: YogaItem[];
}

export interface BirthInput {
  name: string;
  date: string; // YYYY-MM-DD
  time: string; // HH:MM
  timezone?: string;
  latitude: number;
  longitude: number;
  use_lmt?: boolean;
}

export interface KootaResult {
  name: string;
  score: number;
  max_score: number;
  note: string;
}

export interface ManglikStatus {
  is_manglik: boolean;
  sources: string[];
  softened: boolean;
  mars_sign: string;
  mars_house: number;
  mars_dignity: string;
}

export interface CompatibilityResponse {
  bride: string;
  groom: string;
  kootas: KootaResult[];
  total_score: number;
  max_total: number;
  bride_manglik: ManglikStatus;
  groom_manglik: ManglikStatus;
  manglik_balanced: boolean;
}

export interface GunaMilanInput {
  bride: BirthInput;
  groom: BirthInput;
}

export interface PanchangInput {
  date: string;
  timezone: string;
  latitude: number;
  longitude: number;
}

export interface DailyInput extends BirthInput {
  on_date: string; // YYYY-MM-DD
}

export interface TarabalaInfo {
  position: number; // 1..9
  name: string;
  name_hi: string;
  quality: 'very_auspicious' | 'auspicious' | 'mixed' | 'inauspicious' | 'very_inauspicious';
  note_en: string;
  note_hi: string;
}

export interface ChandraBalaInfo {
  position: number; // 1..12
  favorable: boolean;
}

export interface DailyResponse {
  date: string;
  panchang: PanchangResponse;
  tarabala: TarabalaInfo;
  chandra_bala: ChandraBalaInfo;
  overall_score: number; // 0..10
  verdict_en: string;
  verdict_hi: string;
}

export interface PanchangResponse {
  date: string;
  weekday: string;
  weekday_hi: string;
  weekday_lord: string;
  sun_longitude: number;
  moon_longitude: number;
  tithi_index: number;
  tithi_name: string;
  tithi_name_hi: string;
  paksha: string;
  paksha_hi: string;
  nakshatra_index: number;
  nakshatra: string;
  nakshatra_hi: string;
  nakshatra_lord: string;
  yoga_index: number;
  yoga: string;
  yoga_hi: string;
  karana_index: number;
  karana: string;
  karana_hi: string;
}

export interface LifeStoryInput extends BirthInput {
  on_date?: string;
  num_future?: number;
}

export interface RemediesBlock {
  gemstone: string;
  metal: string;
  mantra: string;
  charity: string;
  fast: string;
  deity: string;
}

export interface PhalitChapter {
  lord: string;
  lord_hi: string;
  start: string;
  end: string;
  start_age: number;
  end_age: number;
  duration_years: number;
  house: number;
  sign: string;
  sign_hi: string;
  dignity: 'exalted' | 'own_sign' | 'debilitated' | 'neutral';
  dignity_label_en: string;
  dignity_label_hi: string;
  retrograde: boolean;
  karakas_en: string[];
  karakas_hi: string[];
  house_theme_en: string;
  house_theme_hi: string;
  conjunctions: string[];
  aspects_received: string[];
  themes_en: string[];
  themes_hi: string[];
  summary_en: string;
  summary_hi: string;
  timing_notes_en: string[];
  timing_notes_hi: string[];
  remedies_en: RemediesBlock;
  remedies_hi: RemediesBlock;
  is_past: boolean;
  is_current: boolean;
  is_future: boolean;
}

export interface LifeStoryResponse {
  name: string;
  today: string;
  past: PhalitChapter[];
  current: PhalitChapter | null;
  future: PhalitChapter[];
  overall_signature_en: string;
  overall_signature_hi: string;
}

export interface ChatTurn {
  role: 'user' | 'model';
  text: string;
}

export interface ChatInput extends BirthInput {
  message: string;
  history?: ChatTurn[];
  locale?: 'en' | 'hi';
  on_date?: string;
}

export interface ChatResponse {
  ok: boolean;
  reply: string;
  model: string;
}
