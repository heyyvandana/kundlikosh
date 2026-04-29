"""Panchang — the 5 limbs of the Vedic calendar for any given date / location.

The five limbs (panch + ang = "five limbs"):
    1. Tithi      — lunar day (Sun-Moon angular separation / 12°)
    2. Vara       — weekday
    3. Nakshatra  — Moon's nakshatra
    4. Yoga       — Sun + Moon longitude / 13°20'
    5. Karana     — half of a tithi (60 in a lunar month, 11 unique types)

All values use Lahiri sidereal longitudes — same convention as the rest of
KundliKosh. Sources: Surya Siddhanta, Drik Panchang, BPHS.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

import swisseph as swe

from .chart import to_julian_day_utc  # reuse the same JD computation
from .constants import NAKSHATRAS

# 30 tithis: 15 waxing (Shukla Paksha) + 15 waning (Krishna Paksha).
# The 15th of each paksha is special — Purnima (full) and Amavasya (new).
TITHI_NAMES_EN = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
]

TITHI_NAMES_HI = [
    "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी",
    "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी",
    "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा",
    "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी",
    "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी",
    "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "अमावस्या",
]

# Vara (weekday) — Sunday is index 0 for Surya, etc.
VARA_NAMES_EN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
VARA_NAMES_HI = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"]
VARA_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# 27 Yogas (sum of Sun + Moon longitudes / 13°20')
YOGA_NAMES_EN = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]
YOGA_NAMES_HI = [
    "विष्कम्भ", "प्रीति", "आयुष्मान्", "सौभाग्य", "शोभन",
    "अतिगण्ड", "सुकर्मा", "धृति", "शूल", "गण्ड",
    "वृद्धि", "ध्रुव", "व्याघात", "हर्षण", "वज्र",
    "सिद्धि", "व्यतिपात", "वरीयान्", "परिघ", "शिव",
    "सिद्ध", "साध्य", "शुभ", "शुक्ल", "ब्रह्मा",
    "इन्द्र", "वैधृति",
]

# Karana — 11 unique types. 7 cycling karanas appear 8 times in a month;
# 4 fixed karanas (Shakuni, Chatushpada, Naga, Kimstughna) appear once
# at the boundary of the lunar month.
KARANA_NAMES_EN = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja",
    "Vanija", "Vishti",  # 7 cycling
    "Shakuni", "Chatushpada", "Naga", "Kimstughna",  # 4 fixed
]
KARANA_NAMES_HI = [
    "बव", "बालव", "कौलव", "तैतिल", "गर",
    "वणिज", "विष्टि",
    "शकुनि", "चतुष्पद", "नाग", "किंस्तुघ्न",
]


@dataclass
class Panchang:
    date: str           # ISO date, local
    weekday: str        # English
    weekday_hi: str
    weekday_lord: str   # planetary lord (Sun/Moon/Mars/...)
    sun_longitude: float
    moon_longitude: float
    tithi_index: int    # 1..30
    tithi_name: str
    tithi_name_hi: str
    paksha: str         # "Shukla" or "Krishna"
    paksha_hi: str
    nakshatra_index: int  # 1..27
    nakshatra: str
    nakshatra_hi: str
    nakshatra_lord: str
    yoga_index: int     # 1..27
    yoga: str
    yoga_hi: str
    karana_index: int   # 1..11 (in our reduced list)
    karana: str
    karana_hi: str

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "weekday": self.weekday,
            "weekday_hi": self.weekday_hi,
            "weekday_lord": self.weekday_lord,
            "sun_longitude": self.sun_longitude,
            "moon_longitude": self.moon_longitude,
            "tithi_index": self.tithi_index,
            "tithi_name": self.tithi_name,
            "tithi_name_hi": self.tithi_name_hi,
            "paksha": self.paksha,
            "paksha_hi": self.paksha_hi,
            "nakshatra_index": self.nakshatra_index,
            "nakshatra": self.nakshatra,
            "nakshatra_hi": self.nakshatra_hi,
            "nakshatra_lord": self.nakshatra_lord,
            "yoga_index": self.yoga_index,
            "yoga": self.yoga,
            "yoga_hi": self.yoga_hi,
            "karana_index": self.karana_index,
            "karana": self.karana,
            "karana_hi": self.karana_hi,
        }


def _karana_index_from_half(half: int) -> int:
    """Map the 0..59 'half-tithi' of the lunar month to a karana index.

    First half of Shukla Pratipada (half=0) is Kimstughna (fixed).
    Halves 1..56 cycle through the 7 cycling karanas (8 cycles).
    Halves 57, 58, 59 are Shakuni, Chatushpada, Naga (fixed).

    Returns 0..10 indexing into KARANA_NAMES_*.
    """
    if half == 0:
        return 10  # Kimstughna
    if half == 57:
        return 7   # Shakuni
    if half == 58:
        return 8   # Chatushpada
    if half == 59:
        return 9   # Naga
    # Cycling: half 1..56 maps to karana index 0..6 cycling
    return (half - 1) % 7


def compute_panchang(
    *,
    on_date: date,
    latitude: float,
    longitude: float,
    timezone_str: str = "Asia/Kolkata",
    sunrise_hint_hour: int = 6,
) -> Panchang:
    """Compute the panchang for a given local date.

    Convention: panchang values are taken at local sunrise (we approximate
    via 6 AM local time — for higher precision pass an explicit sunrise via
    Drik panchang in a future version). This is the Drik / Vedic convention:
    the tithi/nakshatra/yoga at sunrise is "today's" panchang.
    """
    tz = ZoneInfo(timezone_str)
    local_dt = datetime(
        on_date.year, on_date.month, on_date.day, sunrise_hint_hour, 0, tzinfo=tz
    )
    utc_dt = local_dt.astimezone(timezone.utc)
    jd = to_julian_day_utc(utc_dt)

    # Sidereal longitudes
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED | swe.FLG_MOSEPH
    sun_lon = swe.calc_ut(jd, swe.SUN, flags)[0][0] % 360.0
    moon_lon = swe.calc_ut(jd, swe.MOON, flags)[0][0] % 360.0

    # Tithi: angular separation from Sun to Moon, divided into 12° slabs.
    elong = (moon_lon - sun_lon) % 360.0
    tithi_index = int(elong // 12.0) + 1  # 1..30
    paksha_en = "Shukla" if tithi_index <= 15 else "Krishna"
    paksha_hi = "शुक्ल" if tithi_index <= 15 else "कृष्ण"

    # Nakshatra: Moon's longitude / (360/27) = / 13.333°
    nak_index = int(moon_lon // (360.0 / 27.0))  # 0..26
    nak = NAKSHATRAS[nak_index]

    # Yoga: (Sun + Moon) longitude / 13°20' = (Sun + Moon) / (360/27)
    yoga_lon = (sun_lon + moon_lon) % 360.0
    yoga_index = int(yoga_lon // (360.0 / 27.0))  # 0..26

    # Karana: half-tithi index 0..59, mapped to one of 11 karana names
    half = int(elong // 6.0)  # 0..59
    karana_idx = _karana_index_from_half(half)

    # Vara: ISO weekday → Vedic weekday (Sun=0). Python's weekday() has Mon=0.
    # Vedic convention: vara starts at sunrise. Use the local date's weekday.
    # Python: Mon=0, Sun=6. Convert to Sun=0, Sat=6:
    py_weekday = local_dt.weekday()  # 0=Mon..6=Sun
    vara_idx = (py_weekday + 1) % 7  # 0=Sun..6=Sat

    return Panchang(
        date=on_date.isoformat(),
        weekday=VARA_NAMES_EN[vara_idx],
        weekday_hi=VARA_NAMES_HI[vara_idx],
        weekday_lord=VARA_LORDS[vara_idx],
        sun_longitude=round(sun_lon, 4),
        moon_longitude=round(moon_lon, 4),
        tithi_index=tithi_index,
        tithi_name=TITHI_NAMES_EN[tithi_index - 1],
        tithi_name_hi=TITHI_NAMES_HI[tithi_index - 1],
        paksha=paksha_en,
        paksha_hi=paksha_hi,
        nakshatra_index=nak_index + 1,
        nakshatra=nak["name"],
        nakshatra_hi=nak["name_hi"],
        nakshatra_lord=nak["lord"],
        yoga_index=yoga_index + 1,
        yoga=YOGA_NAMES_EN[yoga_index],
        yoga_hi=YOGA_NAMES_HI[yoga_index],
        karana_index=karana_idx + 1,
        karana=KARANA_NAMES_EN[karana_idx],
        karana_hi=KARANA_NAMES_HI[karana_idx],
    )
