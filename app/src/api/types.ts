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
