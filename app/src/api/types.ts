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
