"""Sade Sati & Dhaiya — Saturn transit phases relative to the natal Moon.

Sade Sati = "seven-and-a-half" — the period when Saturn transits the 12th sign,
1st (Janma), and 2nd sign from the natal Moon. Each phase ~2.5 years; total ~7.5.

Dhaiya (also called Kantaka Sani / Ashtama Sani) = Saturn transiting the 4th or
8th sign from natal Moon — each ~2.5 years. Generally regarded as challenging.

This module computes:
- The current Saturn transit sign (sidereal Lahiri)
- Whether the native is currently in Sade Sati / Dhaiya
- Which phase, when it began, when it ends, what classical texts say about each
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import swisseph as swe

from . import constants as K
from .chart import Chart, sign_index_of


# Saturn moves slowly: ~12.4 years per zodiac (so ~2.4 years per sign on average,
# but varies due to retrogrades). For dating phase boundaries we sample daily.

PHASE_DESCRIPTIONS_EN = {
    "phase1": "First phase (Saturn in 12H from natal Moon) — testing of accumulated patterns; financial caution; introspection on losses and intangible attachments. Often shows up as restless transitions and quiet endings.",
    "peak":   "Peak phase (Saturn in Janma — same sign as natal Moon) — direct work on the self; physical/emotional fatigue is common; relationships and identity recalibrate; this is where deep reorientation happens.",
    "phase3": "Last phase (Saturn in 2H from natal Moon) — themes of family, finances, speech, and stored values. Discipline and slow rebuilding; foundations laid here become long-term assets.",
    "ashtama": "Ashtama Sani (Saturn in 8H from natal Moon) — chronic transformations, shared resources scrutinised, occult/research interests, partner's finances tested. Classical texts mark this as a heavy 2.5-year phase.",
    "kantaka": "Kantaka Sani (Saturn in 4H from natal Moon) — domestic discomfort, mother's health, property/vehicle delays, emotional cooling of the home. A 2.5-year phase that asks for inner shelter rather than outer.",
}

PHASE_DESCRIPTIONS_HI = {
    "phase1": "प्रथम चरण (शनि चंद्र से १२वें भाव में) — संचित प्रवृत्तियों की परीक्षा; आर्थिक सावधानी; अमूर्त लगावों पर आंतरिक चिंतन। प्रायः शांत समापन व चंचल परिवर्तन।",
    "peak":   "मध्य चरण (शनि जन्मराशि में) — स्वयं पर सीधा कार्य; शारीरिक/भावनात्मक थकान सामान्य; संबंध एवं पहचान का पुनर्निर्धारण।",
    "phase3": "अंतिम चरण (शनि चंद्र से २वें भाव में) — परिवार, धन, वाणी, संचित मूल्य। अनुशासन और मंद पुनर्निर्माण; यहाँ रखी नींव दीर्घकालिक होती है।",
    "ashtama": "अष्टम शनि (चंद्र से ८वें भाव में) — दीर्घ रूपांतरण, साझा संसाधनों की परीक्षा, गुप्त/शोध रुचियाँ। शास्त्रों में भारी अढ़ाई वर्ष।",
    "kantaka": "कंटक शनि (चंद्र से ४थे भाव में) — गृह असुविधा, माता का स्वास्थ्य, संपत्ति/वाहन में विलंब, गृह की भावनात्मक शीतलता।",
}


@dataclass
class SaturnTransitState:
    in_sade_sati: bool
    in_dhaiya: bool             # 4H or 8H from natal Moon
    phase: Optional[str]        # "phase1" | "peak" | "phase3" | "kantaka" | "ashtama" | None
    phase_label_en: Optional[str]
    phase_label_hi: Optional[str]
    description_en: Optional[str]
    description_hi: Optional[str]
    saturn_sign: str
    saturn_sign_hi: str
    moon_sign: str              # native's natal Moon sign
    relative_house: int         # which house from natal Moon Saturn currently transits (1..12)
    started_on: Optional[str]   # YYYY-MM-DD when current phase began
    ends_on: Optional[str]      # YYYY-MM-DD when current phase ends


def _saturn_sidereal_longitude(dt: datetime) -> float:
    """Sidereal Lahiri longitude of Saturn at `dt`."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    jd = swe.julday(
        dt.year, dt.month, dt.day,
        dt.hour + dt.minute / 60.0 + dt.second / 3600.0,
    )
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    pos, _flag = swe.calc_ut(jd, swe.SATURN, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
    return float(pos[0]) % 360.0


def _saturn_sign_index(dt: datetime) -> int:
    return sign_index_of(_saturn_sidereal_longitude(dt))


def _classify(rel_house: int) -> Optional[str]:
    """Map house-from-Moon (1..12) to phase identifier."""
    if rel_house == 12:
        return "phase1"
    if rel_house == 1:
        return "peak"
    if rel_house == 2:
        return "phase3"
    if rel_house == 4:
        return "kantaka"
    if rel_house == 8:
        return "ashtama"
    return None


def _find_boundary(
    *, target_sign_idx: int, start_dt: datetime, direction: int, max_days: int = 1100
) -> Optional[datetime]:
    """Find the date when Saturn first leaves/enters the target sign by walking
    `direction` days (forward=+1, backward=-1). Returns the boundary date or None."""
    cur = start_dt
    for _ in range(max_days):
        cur = cur + timedelta(days=direction)
        idx = _saturn_sign_index(cur)
        if direction > 0 and idx != target_sign_idx:
            # exited the target sign — boundary is yesterday
            return cur
        if direction < 0 and idx != target_sign_idx:
            return cur + timedelta(days=1)
    return None


def compute_sade_sati(chart: Chart, on_date: Optional[date] = None) -> SaturnTransitState:
    """Compute Saturn-vs-natal-Moon phase for a given date (defaults to today)."""
    on = on_date or date.today()
    dt = datetime(on.year, on.month, on.day, 12, 0, tzinfo=timezone.utc)

    natal_moon_idx = K.SIGNS_EN.index(chart.moon_sign)
    saturn_idx = _saturn_sign_index(dt)
    rel_house = ((saturn_idx - natal_moon_idx) % 12) + 1
    phase = _classify(rel_house)

    if phase is None:
        return SaturnTransitState(
            in_sade_sati=False,
            in_dhaiya=False,
            phase=None,
            phase_label_en=None,
            phase_label_hi=None,
            description_en=None,
            description_hi=None,
            saturn_sign=K.SIGNS_EN[saturn_idx],
            saturn_sign_hi=K.SIGNS_HI[saturn_idx],
            moon_sign=chart.moon_sign,
            relative_house=rel_house,
            started_on=None,
            ends_on=None,
        )

    in_sade_sati = phase in ("phase1", "peak", "phase3")
    in_dhaiya = phase in ("kantaka", "ashtama")

    label_en_map = {
        "phase1": "Sade Sati — first phase",
        "peak":   "Sade Sati — peak (Janma)",
        "phase3": "Sade Sati — last phase",
        "kantaka": "Kantaka Sani (4H)",
        "ashtama": "Ashtama Sani (8H)",
    }
    label_hi_map = {
        "phase1": "साढ़े साती — प्रथम चरण",
        "peak":   "साढ़े साती — मध्य (जन्म)",
        "phase3": "साढ़े साती — अंतिम चरण",
        "kantaka": "कंटक शनि (४)",
        "ashtama": "अष्टम शनि (८)",
    }

    started = _find_boundary(target_sign_idx=saturn_idx, start_dt=dt, direction=-1)
    ended = _find_boundary(target_sign_idx=saturn_idx, start_dt=dt, direction=+1)

    return SaturnTransitState(
        in_sade_sati=in_sade_sati,
        in_dhaiya=in_dhaiya,
        phase=phase,
        phase_label_en=label_en_map[phase],
        phase_label_hi=label_hi_map[phase],
        description_en=PHASE_DESCRIPTIONS_EN[phase],
        description_hi=PHASE_DESCRIPTIONS_HI[phase],
        saturn_sign=K.SIGNS_EN[saturn_idx],
        saturn_sign_hi=K.SIGNS_HI[saturn_idx],
        moon_sign=chart.moon_sign,
        relative_house=rel_house,
        started_on=started.date().isoformat() if started else None,
        ends_on=ended.date().isoformat() if ended else None,
    )
