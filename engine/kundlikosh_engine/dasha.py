"""Vimshottari Dasha — 120-year planetary period system.

Birth dasha is determined by the Moon's nakshatra. The balance of that
dasha is proportional to the unfilled portion of the nakshatra at birth.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from . import constants as K
from .chart import Chart, nakshatra_info


@dataclass
class DashaPeriod:
    lord: str
    start: datetime
    end: datetime
    duration_years: float


def _years_to_timedelta(years: float) -> timedelta:
    # 365.2425-day year (Gregorian) is the convention used by most jyotish software
    return timedelta(days=years * 365.2425)


def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def compute_mahadashas(chart: Chart, num_periods: int = 9) -> list[DashaPeriod]:
    """Return Vimshottari mahadashas starting from birth.

    `num_periods` defaults to 9 (one full cycle = 120 years).
    """
    moon_long = next(p.longitude for p in chart.planets if p.name == "Moon")
    nk_idx, _ = nakshatra_info(moon_long)
    birth_lord = K.NAKSHATRA_LORDS[nk_idx]

    # Position of Moon within its nakshatra (in degrees)
    nk_size = 360.0 / 27
    deg_into_nk = moon_long - (nk_idx * nk_size)
    fraction_consumed = deg_into_nk / nk_size
    balance_years = K.DASHA_YEARS[birth_lord] * (1 - fraction_consumed)

    birth_dt = datetime.fromisoformat(chart.birth_dt_utc)
    periods: list[DashaPeriod] = []

    # 1. Birth dasha balance
    cur_start = birth_dt
    cur_end = birth_dt + _years_to_timedelta(balance_years)
    periods.append(DashaPeriod(birth_lord, cur_start, cur_end, balance_years))

    # 2. Subsequent dashas in order
    order_start = K.DASHA_ORDER.index(birth_lord)
    for i in range(1, num_periods):
        lord = K.DASHA_ORDER[(order_start + i) % len(K.DASHA_ORDER)]
        years = K.DASHA_YEARS[lord]
        start = cur_end
        end = start + _years_to_timedelta(years)
        periods.append(DashaPeriod(lord, start, end, years))
        cur_end = end

    return periods


def compute_antardashas(maha: DashaPeriod) -> list[DashaPeriod]:
    """Sub-periods (bhukti) inside a mahadasha — the same 9 lords proportional
    to their dasha years, summing to the mahadasha's length."""
    total_years = maha.duration_years
    out: list[DashaPeriod] = []
    start = maha.start
    order_start = K.DASHA_ORDER.index(maha.lord)
    for i in range(9):
        sub_lord = K.DASHA_ORDER[(order_start + i) % 9]
        sub_years = total_years * K.DASHA_YEARS[sub_lord] / 120.0
        end = start + _years_to_timedelta(sub_years)
        out.append(DashaPeriod(sub_lord, start, end, sub_years))
        start = end
    return out


def current_dasha(chart: Chart, now: Optional[datetime] = None) -> dict:
    """Return current mahadasha + antardasha at `now` (defaults to UTC now)."""
    from datetime import timezone as _tz
    now = now or datetime.now(_tz.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=_tz.utc)

    mahas = compute_mahadashas(chart, num_periods=9)
    cur_md = next((m for m in mahas if m.start <= now < m.end), None)
    if cur_md is None:
        return {"mahadasha": None, "antardasha": None}

    bhuktis = compute_antardashas(cur_md)
    cur_bd = next((b for b in bhuktis if b.start <= now < b.end), None)

    return {
        "mahadasha": {
            "lord": cur_md.lord,
            "start": _fmt(cur_md.start),
            "end": _fmt(cur_md.end),
            "duration_years": round(cur_md.duration_years, 2),
        },
        "antardasha": {
            "lord": cur_bd.lord,
            "start": _fmt(cur_bd.start),
            "end": _fmt(cur_bd.end),
            "duration_years": round(cur_bd.duration_years, 3),
        } if cur_bd else None,
    }


def dasha_timeline(chart: Chart, num_mahadashas: int = 5) -> list[dict]:
    """Human-readable timeline of next `num_mahadashas` mahadashas with bhuktis."""
    mahas = compute_mahadashas(chart, num_periods=num_mahadashas)
    out = []
    for m in mahas:
        bhuktis = compute_antardashas(m)
        out.append({
            "lord": m.lord,
            "start": _fmt(m.start),
            "end": _fmt(m.end),
            "duration_years": round(m.duration_years, 2),
            "antardashas": [
                {
                    "lord": b.lord,
                    "start": _fmt(b.start),
                    "end": _fmt(b.end),
                } for b in bhuktis
            ],
        })
    return out
