"""Vedic birth-chart calculator.

Uses Swiss Ephemeris (sidereal / Lahiri ayanamsa) to compute planetary
positions, ascendant, houses (Whole-Sign), and nakshatras for any birth
moment + location.

This is the *brain* of KundliKosh.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional

import pytz
import swisseph as swe

from . import constants as K

# --- Swiss Ephemeris setup ---------------------------------------------------
# We use the built-in MOSEPH (Moshier) ephemeris fallback so we don't need to
# bundle the large Swiss Ephemeris data files for accuracy within ~1 arc-second
# in the modern era. For tighter accuracy in production, point swe.set_ephe_path
# to the downloaded ephemeris directory.
swe.set_sid_mode(swe.SIDM_LAHIRI)

PLANET_IDS = {
    "Sun":     swe.SUN,
    "Moon":    swe.MOON,
    "Mars":    swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus":   swe.VENUS,
    "Saturn":  swe.SATURN,
    # We use the *true* node for Rahu (more accurate than mean node)
    "Rahu":    swe.TRUE_NODE,
}

FLAGS = swe.FLG_SIDEREAL | swe.FLG_SPEED | swe.FLG_MOSEPH


# --- Dataclasses -------------------------------------------------------------
@dataclass
class PlanetPosition:
    name: str
    name_hi: str
    longitude: float          # 0..360 sidereal
    sign: str
    sign_hi: str
    sign_index: int           # 0..11
    degree_in_sign: float
    house: int                # 1..12 whole-sign from lagna
    nakshatra: str
    nakshatra_hi: str
    nakshatra_lord: str
    nakshatra_deity: str
    nakshatra_deity_hi: str
    pada: int                 # 1..4
    retrograde: bool
    dignity: str              # "exalted" | "debilitated" | "own" | "neutral"


@dataclass
class Chart:
    name: str
    birth_dt_utc: str
    birth_dt_local: str
    timezone: str
    latitude: float
    longitude: float
    ayanamsa: float
    lagna_longitude: float
    lagna_sign: str
    lagna_sign_hi: str
    lagna_sign_index: int
    lagna_degree_in_sign: float
    lagna_nakshatra: str
    lagna_pada: int
    moon_sign: str
    moon_sign_hi: str
    moon_nakshatra: str
    moon_nakshatra_hi: str
    moon_nakshatra_lord: str
    moon_pada: int
    sun_sign: str
    patron_deity: dict        # nakshatra-based personal devata
    planets: list[PlanetPosition] = field(default_factory=list)


# --- Helpers -----------------------------------------------------------------
def to_julian_day_utc(dt_utc: datetime) -> float:
    """Swiss-Ephemeris Julian Day (UT)."""
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_utc = dt_utc.astimezone(timezone.utc)
    hour = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour)


def localize_birth(
    date_str: str,
    time_str: str,
    tz_name: str,
    *,
    use_lmt_for_longitude: float | None = None,
) -> tuple[datetime, datetime]:
    """date_str = 'YYYY-MM-DD', time_str = 'HH:MM' (24h), tz_name e.g. 'Asia/Kolkata'.

    For historical births before standard timezones were established (India: pre-1906),
    pass ``use_lmt_for_longitude=<lon°E>`` and we derive Local Mean Time from longitude
    (offset = longitude / 15 hours east of UTC). The ``tz_name`` is then used only as
    a label.
    """
    naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    if use_lmt_for_longitude is not None:
        # LMT offset purely from longitude
        offset_hours = use_lmt_for_longitude / 15.0
        from datetime import timedelta as _td
        offset = _td(hours=offset_hours)
        local = naive.replace(tzinfo=timezone(offset))
        return local, local.astimezone(timezone.utc)
    tz = pytz.timezone(tz_name)
    local = tz.localize(naive)
    return local, local.astimezone(timezone.utc)


def normalize_360(deg: float) -> float:
    return deg % 360.0


def sign_index_of(longitude: float) -> int:
    return int(longitude // 30) % 12


def degree_in_sign(longitude: float) -> float:
    return longitude - (sign_index_of(longitude) * 30)


def nakshatra_info(longitude: float) -> tuple[int, int]:
    """Returns (nakshatra_index 0..26, pada 1..4)."""
    nk_size = 360.0 / 27        # 13°20'
    pada_size = nk_size / 4     # 3°20'
    nk_index = int(longitude // nk_size) % 27
    pada = int((longitude - nk_index * nk_size) // pada_size) + 1
    pada = max(1, min(4, pada))
    return nk_index, pada


def whole_sign_house(planet_sign_idx: int, lagna_sign_idx: int) -> int:
    return ((planet_sign_idx - lagna_sign_idx) % 12) + 1


def planet_dignity(planet: str, sign_name: str) -> str:
    if planet in K.EXALTATION and K.EXALTATION[planet][0] == sign_name:
        return "exalted"
    if planet in K.DEBILITATION and K.DEBILITATION[planet][0] == sign_name:
        return "debilitated"
    if planet in K.OWN_SIGNS and sign_name in K.OWN_SIGNS[planet]:
        return "own_sign"
    return "neutral"


# --- Main computation --------------------------------------------------------
def compute_chart(
    name: str,
    date: str,                          # 'YYYY-MM-DD'
    time: str,                          # 'HH:MM' 24h local
    timezone_name: str,                 # IANA tz e.g. 'Asia/Kolkata'
    latitude: float,
    longitude: float,
    *,
    use_lmt: bool = False,              # historical births (pre-standard-time)
) -> Chart:
    local_dt, utc_dt = localize_birth(
        date, time, timezone_name,
        use_lmt_for_longitude=longitude if use_lmt else None,
    )
    jd = to_julian_day_utc(utc_dt)

    ayanamsa = swe.get_ayanamsa(jd)

    # --- Ascendant + houses (Whole-Sign) ---
    # We still ask Swiss for the ASC longitude using the 'W' (whole) house
    # system — but we only consume the asc longitude itself; house assignment
    # below is done with the whole-sign rule (same sign as Lagna == 1H).
    cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b'W',
                                 swe.FLG_SIDEREAL)
    asc_long = normalize_360(ascmc[0])
    lagna_idx = sign_index_of(asc_long)
    lagna_deg = degree_in_sign(asc_long)
    lagna_nk_idx, lagna_pada = nakshatra_info(asc_long)

    planets: list[PlanetPosition] = []
    moon_pos: Optional[PlanetPosition] = None
    sun_pos: Optional[PlanetPosition] = None

    for pname in K.PLANETS_EN:
        if pname == "Ketu":
            # Ketu = Rahu + 180°
            rahu = next(p for p in planets if p.name == "Rahu")
            lon = normalize_360(rahu.longitude + 180.0)
            speed = -1  # Ketu is always retrograde-coded
        else:
            pid = PLANET_IDS[pname]
            xx, _ = swe.calc_ut(jd, pid, FLAGS)
            lon = normalize_360(xx[0])
            speed = xx[3]

        sidx = sign_index_of(lon)
        sname = K.SIGNS_EN[sidx]
        nk_idx, pada = nakshatra_info(lon)
        nk = K.NAKSHATRAS[nk_idx]
        retrograde = speed < 0 and pname not in ("Sun", "Moon", "Rahu", "Ketu")
        dignity = planet_dignity(pname, sname)

        pp = PlanetPosition(
            name=pname,
            name_hi=K.PLANETS_HI[pname],
            longitude=lon,
            sign=sname,
            sign_hi=K.SIGNS_HI[sidx],
            sign_index=sidx,
            degree_in_sign=degree_in_sign(lon),
            house=whole_sign_house(sidx, lagna_idx),
            nakshatra=nk["name"],
            nakshatra_hi=nk["name_hi"],
            nakshatra_lord=nk["lord"],
            nakshatra_deity=nk["deity"],
            nakshatra_deity_hi=nk["deity_hi"],
            pada=pada,
            retrograde=retrograde,
            dignity=dignity,
        )
        planets.append(pp)
        if pname == "Moon":
            moon_pos = pp
        if pname == "Sun":
            sun_pos = pp

    assert moon_pos is not None and sun_pos is not None

    moon_nk = K.NAKSHATRAS[nakshatra_info(moon_pos.longitude)[0]]
    patron = {
        "nakshatra": moon_nk["name"],
        "nakshatra_hi": moon_nk["name_hi"],
        "deity": moon_nk["deity"],
        "deity_hi": moon_nk["deity_hi"],
        "symbol": moon_nk["symbol"],
        "lord": moon_nk["lord"],
    }

    return Chart(
        name=name,
        birth_dt_utc=utc_dt.isoformat(),
        birth_dt_local=local_dt.isoformat(),
        timezone=timezone_name,
        latitude=latitude,
        longitude=longitude,
        ayanamsa=ayanamsa,
        lagna_longitude=asc_long,
        lagna_sign=K.SIGNS_EN[lagna_idx],
        lagna_sign_hi=K.SIGNS_HI[lagna_idx],
        lagna_sign_index=lagna_idx,
        lagna_degree_in_sign=lagna_deg,
        lagna_nakshatra=K.NAKSHATRAS[lagna_nk_idx]["name"],
        lagna_pada=lagna_pada,
        moon_sign=moon_pos.sign,
        moon_sign_hi=moon_pos.sign_hi,
        moon_nakshatra=moon_pos.nakshatra,
        moon_nakshatra_hi=moon_pos.nakshatra_hi,
        moon_nakshatra_lord=moon_pos.nakshatra_lord,
        moon_pada=moon_pos.pada,
        sun_sign=sun_pos.sign,
        patron_deity=patron,
        planets=planets,
    )


def chart_to_dict(c: Chart) -> dict:
    d = asdict(c)
    return d
