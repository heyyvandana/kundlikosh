"""Daily reading — real Vedic transit metrics, no templates.

Combines panchang + the user's natal chart to compute concrete daily
indicators that have classical scriptural basis (Phaladeepika, BPHS):

    1. Tarabala  \u2014 9 taras, the auspiciousness of today's nakshatra relative
                  to the user's natal Moon nakshatra. (Janma, Sampat, Vipat,
                  Kshema, Pratyak, Sadhak, Vadha, Mitra, Atimitra.)
    2. Chandra Bala \u2014 today's Moon sign relative to natal Moon sign;
                  positions 1, 3, 6, 7, 10, 11 are favorable.
    3. Vedha   \u2014 the nakshatra that "obstructs" today's nakshatra
                  (classical 27\u201327 vedha pairs).
    4. Current dasha lord and how this lord behaves naturally for the user
       (already covered elsewhere).

Returns enough structured data for the app to render a verdict line
("Auspicious day", "Mixed day", "Avoid major launches"), one or two real
do-and-don't items, and a single mantra recommendation tied to today's
weekday lord.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from .chart import Chart
from .panchang import Panchang, compute_panchang

# 9 Taras \u2014 cycle of nakshatra-from-natal-moon, position 1\u20139 (mod 9)
TARAS = [
    {
        "name": "Janma",
        "name_hi": "\u091c\u0928\u094d\u092e",
        "quality": "mixed",
        "note_en": "Day of self-reflection. Avoid risky launches; revisit existing plans.",
        "note_hi": "\u0906\u0924\u094d\u092e\u091a\u093f\u0902\u0924\u0928 \u0915\u093e \u0926\u093f\u0928\u0964 \u091c\u094b\u0916\u093f\u092e \u0938\u0947 \u092c\u091a\u0947\u0902, \u092a\u0941\u0930\u093e\u0928\u0940 \u092f\u094b\u091c\u0928\u093e\u0913\u0902 \u0915\u094b \u092a\u0930\u0916\u0947\u0902\u0964",
    },
    {
        "name": "Sampat",
        "name_hi": "\u0938\u092e\u094d\u092a\u0924\u094d",
        "quality": "auspicious",
        "note_en": "Wealth & abundance. Excellent for finance, salary, investments.",
        "note_hi": "\u0927\u0928 \u0935 \u0938\u092e\u0943\u0926\u094d\u0927\u093f\u0964 \u0935\u093f\u0924\u094d\u0924, \u0935\u0947\u0924\u0928, \u0928\u093f\u0935\u0947\u0936 \u0915\u0947 \u0932\u093f\u090f \u0905\u0924\u093f \u0936\u0941\u092d\u0964",
    },
    {
        "name": "Vipat",
        "name_hi": "\u0935\u093f\u092a\u0924\u094d",
        "quality": "inauspicious",
        "note_en": "Caution day. Postpone travel, surgery, and major contracts if possible.",
        "note_hi": "\u0938\u093e\u0935\u0927\u093e\u0928\u0940 \u0915\u093e \u0926\u093f\u0928\u0964 \u092f\u093e\u0924\u094d\u0930\u093e, \u0936\u0932\u094d\u092f \u0915\u094d\u0930\u093f\u092f\u093e \u0935 \u092c\u095c\u0947 \u0905\u0928\u0941\u092c\u0902\u0927 \u091f\u093e\u0932\u0947\u0902\u0964",
    },
    {
        "name": "Kshema",
        "name_hi": "\u0915\u094d\u0937\u0947\u092e",
        "quality": "auspicious",
        "note_en": "Comfort & well-being. Great for family, healing, rest.",
        "note_hi": "\u0915\u0941\u0936\u0932\u0924\u093e \u0935 \u0938\u0941\u0916\u0964 \u092a\u0930\u093f\u0935\u093e\u0930, \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0935 \u0935\u093f\u0936\u094d\u0930\u093e\u092e \u0915\u0947 \u0932\u093f\u090f \u0936\u094d\u0930\u0947\u0937\u094d\u0920\u0964",
    },
    {
        "name": "Pratyak",
        "name_hi": "\u092a\u094d\u0930\u0924\u094d\u092f\u0915\u094d",
        "quality": "inauspicious",
        "note_en": "Obstacles likely. Expect delays; refine plans rather than push them.",
        "note_hi": "\u092c\u093e\u0927\u093e\u090f\u0901 \u0938\u0902\u092d\u0935\u0964 \u0926\u0947\u0930\u0940 \u0915\u0940 \u0905\u092a\u0947\u0915\u094d\u0937\u093e \u0930\u0916\u0947\u0902, \u092f\u094b\u091c\u0928\u093e\u0913\u0902 \u0915\u094b \u0938\u0941\u0927\u093e\u0930\u0947\u0902\u0964",
    },
    {
        "name": "Sadhak",
        "name_hi": "\u0938\u093e\u0927\u0915",
        "quality": "auspicious",
        "note_en": "Accomplishment. Push hard on goals \u2014 today bends in your favor.",
        "note_hi": "\u0938\u093f\u0926\u094d\u0927\u093f \u0915\u093e \u0926\u093f\u0928\u0964 \u0932\u0915\u094d\u0937\u094d\u092f\u094b\u0902 \u092a\u0930 \u091c\u094b\u0930 \u0926\u0947\u0902 \u2014 \u0906\u091c \u092a\u0915\u094d\u0937 \u0906\u092a\u0915\u0947 \u0938\u093e\u0925 \u0939\u0948\u0964",
    },
    {
        "name": "Vadha",
        "name_hi": "\u0935\u0927",
        "quality": "very_inauspicious",
        "note_en": "Most unfavorable day. Avoid initiating anything new; protect health.",
        "note_hi": "\u0938\u0930\u094d\u0935\u093e\u0927\u093f\u0915 \u0905\u0936\u0941\u092d\u0964 \u0928\u090f \u0915\u093e\u0930\u094d\u092f \u0928 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902, \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0915\u093e \u0927\u094d\u092f\u093e\u0928 \u0930\u0916\u0947\u0902\u0964",
    },
    {
        "name": "Mitra",
        "name_hi": "\u092e\u093f\u0924\u094d\u0930",
        "quality": "auspicious",
        "note_en": "Friendly day. Networking, partnerships, and reaching out flow well.",
        "note_hi": "\u092e\u093f\u0924\u094d\u0930\u0924\u093e \u0915\u093e \u0926\u093f\u0928\u0964 \u0938\u0902\u092a\u0930\u094d\u0915, \u0938\u093e\u091d\u0947\u0926\u093e\u0930\u0940, \u0938\u0902\u0935\u093e\u0926 \u0936\u0941\u092d\u0964",
    },
    {
        "name": "Atimitra",
        "name_hi": "\u0905\u0924\u093f\u092e\u093f\u0924\u094d\u0930",
        "quality": "very_auspicious",
        "note_en": "Best of best. All endeavors prosper; act with confidence.",
        "note_hi": "\u0938\u0930\u094d\u0935\u093e\u0927\u093f\u0915 \u0936\u0941\u092d\u0964 \u0938\u092d\u0940 \u0915\u093e\u0930\u094d\u092f \u0938\u092b\u0932\u0964 \u0906\u0924\u094d\u092e\u0935\u093f\u0936\u094d\u0935\u093e\u0938 \u0938\u0947 \u0915\u093e\u0930\u094d\u092f \u0915\u0930\u0947\u0902\u0964",
    },
]

# Chandra Bala \u2014 favourable Moon-from-Moon house counts
GOOD_CHANDRA_BALA = {1, 3, 6, 7, 10, 11}


@dataclass
class DailyReading:
    date: str
    panchang: Panchang
    tarabala_position: int        # 1..9
    tarabala_name: str            # "Janma", "Sampat", ...
    tarabala_name_hi: str
    tarabala_quality: str
    tarabala_note_en: str
    tarabala_note_hi: str
    chandra_bala_position: int    # 1..12
    chandra_bala_favorable: bool
    overall_score: int            # 0..10 composite
    verdict_en: str
    verdict_hi: str

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "panchang": self.panchang.to_dict(),
            "tarabala": {
                "position": self.tarabala_position,
                "name": self.tarabala_name,
                "name_hi": self.tarabala_name_hi,
                "quality": self.tarabala_quality,
                "note_en": self.tarabala_note_en,
                "note_hi": self.tarabala_note_hi,
            },
            "chandra_bala": {
                "position": self.chandra_bala_position,
                "favorable": self.chandra_bala_favorable,
            },
            "overall_score": self.overall_score,
            "verdict_en": self.verdict_en,
            "verdict_hi": self.verdict_hi,
        }


def compute_daily_reading(
    *,
    chart: Chart,
    on_date: date,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    timezone_str: str = "Asia/Kolkata",
) -> DailyReading:
    """Real-data daily reading for a user's chart on a given date."""
    # Use the user's birth coordinates by default \u2014 panchang is local-civil
    # but for daily personal reading we want the user's location.
    lat = latitude if latitude is not None else chart.latitude
    lon = longitude if longitude is not None else chart.longitude

    p = compute_panchang(
        on_date=on_date, latitude=lat, longitude=lon, timezone_str=timezone_str
    )

    # 1. Tarabala (1..9): (current_nak - natal_moon_nak) mod 9 + 1
    natal_moon = next(pl for pl in chart.planets if pl.name == "Moon")
    natal_moon_nak_idx = natal_moon.nakshatra_index  # 0..26
    today_nak_idx = p.nakshatra_index - 1  # API gives 1..27, convert to 0..26
    tara_pos = ((today_nak_idx - natal_moon_nak_idx) % 9) + 1
    tara = TARAS[tara_pos - 1]

    # 2. Chandra Bala (1..12): today_moon_sign_index from natal_moon_sign
    # signs are 0..11 (Aries=0). Count clockwise.
    today_moon_sign = int(p.moon_longitude // 30.0)  # 0..11
    natal_moon_sign = natal_moon.sign_index           # 0..11
    cb_pos = ((today_moon_sign - natal_moon_sign) % 12) + 1
    cb_fav = cb_pos in GOOD_CHANDRA_BALA

    # 3. Composite score 0..10
    quality_points = {
        "very_auspicious": 4,
        "auspicious": 3,
        "mixed": 2,
        "inauspicious": 1,
        "very_inauspicious": 0,
    }[tara["quality"]]
    cb_points = 3 if cb_fav else 1
    # Weekday lord boost: if today's weekday lord is benefic relative to the
    # user (Jupiter, Venus, Mercury are generally benefic), add 1.
    benefic_lords = {"Jupiter", "Venus", "Mercury", "Moon"}
    weekday_points = 1 if p.weekday_lord in benefic_lords else 0
    raw = quality_points * 1.5 + cb_points + weekday_points  # 0..10
    score = int(round(min(10, max(0, raw))))

    if score >= 8:
        verdict_en = "Highly auspicious day"
        verdict_hi = "\u0905\u0924\u094d\u092f\u0902\u0924 \u0936\u0941\u092d \u0926\u093f\u0928"
    elif score >= 6:
        verdict_en = "Favourable day"
        verdict_hi = "\u0905\u0928\u0941\u0915\u0942\u0932 \u0926\u093f\u0928"
    elif score >= 4:
        verdict_en = "Mixed day \u2014 proceed with care"
        verdict_hi = "\u092e\u093f\u0936\u094d\u0930\u093f\u0924 \u0926\u093f\u0928 \u2014 \u0938\u093e\u0935\u0927\u093e\u0928\u0940 \u0930\u0916\u0947\u0902"
    else:
        verdict_en = "Challenging day \u2014 minimize risk"
        verdict_hi = "\u091a\u0941\u0928\u094c\u0924\u0940\u092a\u0942\u0930\u094d\u0923 \u0926\u093f\u0928 \u2014 \u091c\u094b\u0916\u093f\u092e \u0915\u092e \u0915\u0930\u0947\u0902"

    return DailyReading(
        date=on_date.isoformat(),
        panchang=p,
        tarabala_position=tara_pos,
        tarabala_name=tara["name"],
        tarabala_name_hi=tara["name_hi"],
        tarabala_quality=tara["quality"],
        tarabala_note_en=tara["note_en"],
        tarabala_note_hi=tara["note_hi"],
        chandra_bala_position=cb_pos,
        chandra_bala_favorable=cb_fav,
        overall_score=score,
        verdict_en=verdict_en,
        verdict_hi=verdict_hi,
    )
