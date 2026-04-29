"""Varga (divisional) charts.

Implements the standard Parashari rules for the most important vargas:
    D-9  (Navamsa)   — marriage / inner self / dharma
    D-10 (Dashamsa)  — career / public life
    D-7  (Saptamsa)  — children / progeny
    D-3  (Drekkana)  — siblings / courage
    D-12 (Dwadashamsha) — parents / ancestry

Reference: Brihat Parashara Hora Shastra, ch. 6–8.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import constants as K
from .chart import Chart, PlanetPosition


# --- Navamsa (D-9) ---------------------------------------------------------
def navamsa_sign_index(longitude: float) -> int:
    """Return the navamsa sign (0..11) for a given sidereal ecliptic longitude.

    Rule:
        movable signs (Ari/Can/Lib/Cap) → navamsas start in same sign
        fixed   signs (Tau/Leo/Sco/Aqu) → navamsas start in 9th from sign
        dual    signs (Gem/Vir/Sag/Pis) → navamsas start in 5th from sign
    Each navamsa spans 3°20' (=200').
    """
    sign_idx = int(longitude // 30) % 12
    pos_in_sign = longitude - sign_idx * 30          # 0..30
    nav_idx_in_sign = min(8, int(pos_in_sign // (30 / 9)))   # 0..8

    nature = sign_idx % 3   # 0=movable, 1=fixed, 2=dual
    if nature == 0:
        start = sign_idx
    elif nature == 1:
        start = (sign_idx + 8) % 12      # 9th from
    else:
        start = (sign_idx + 4) % 12      # 5th from
    return (start + nav_idx_in_sign) % 12


# --- Dashamsa (D-10) -------------------------------------------------------
def dashamsa_sign_index(longitude: float) -> int:
    """Return the dashamsa sign (0..11).

    Each dashamsa spans 3° (=180'). Odd signs start from same sign,
    even signs from 9th from same sign.
    """
    sign_idx = int(longitude // 30) % 12
    pos_in_sign = longitude - sign_idx * 30
    dash_idx = min(9, int(pos_in_sign // 3.0))
    if sign_idx % 2 == 0:                  # odd-numbered sign in 1-based (Aries=1) -> sign_idx 0,2,4..
        start = sign_idx
    else:
        start = (sign_idx + 8) % 12
    return (start + dash_idx) % 12


# --- Saptamsa (D-7) --------------------------------------------------------
def saptamsa_sign_index(longitude: float) -> int:
    sign_idx = int(longitude // 30) % 12
    pos_in_sign = longitude - sign_idx * 30
    s_idx = min(6, int(pos_in_sign // (30 / 7)))
    if sign_idx % 2 == 0:
        start = sign_idx
    else:
        start = (sign_idx + 6) % 12
    return (start + s_idx) % 12


# --- Drekkana (D-3) --------------------------------------------------------
def drekkana_sign_index(longitude: float) -> int:
    sign_idx = int(longitude // 30) % 12
    pos_in_sign = longitude - sign_idx * 30
    d_idx = min(2, int(pos_in_sign // 10))
    return (sign_idx + 4 * d_idx) % 12


# --- Dwadashamsha (D-12) ---------------------------------------------------
def dwadashamsha_sign_index(longitude: float) -> int:
    sign_idx = int(longitude // 30) % 12
    pos_in_sign = longitude - sign_idx * 30
    d_idx = min(11, int(pos_in_sign // 2.5))
    return (sign_idx + d_idx) % 12


# --- Generic varga chart builder ------------------------------------------
@dataclass
class VargaChart:
    name: str          # e.g. "D9 Navamsa"
    lagna_sign: str
    lagna_sign_index: int
    placements: list[dict]   # [{name, sign, sign_hi, house}]


_VARGA_FUNCS = {
    "D9":  ("Navamsa",       navamsa_sign_index),
    "D10": ("Dashamsa",      dashamsa_sign_index),
    "D7":  ("Saptamsa",      saptamsa_sign_index),
    "D3":  ("Drekkana",      drekkana_sign_index),
    "D12": ("Dwadashamsha",  dwadashamsha_sign_index),
}


def compute_varga(chart: Chart, varga: str) -> VargaChart:
    if varga not in _VARGA_FUNCS:
        raise ValueError(f"Unknown varga: {varga}. Use one of {list(_VARGA_FUNCS)}")
    label, fn = _VARGA_FUNCS[varga]

    lagna_v = fn(chart.lagna_longitude)
    placements = []
    for p in chart.planets:
        s = fn(p.longitude)
        house = ((s - lagna_v) % 12) + 1
        placements.append({
            "name": p.name,
            "name_hi": p.name_hi,
            "sign": K.SIGNS_EN[s],
            "sign_hi": K.SIGNS_HI[s],
            "sign_index": s,
            "house": house,
            "retrograde": p.retrograde,
        })
    return VargaChart(
        name=f"{varga} {label}",
        lagna_sign=K.SIGNS_EN[lagna_v],
        lagna_sign_index=lagna_v,
        placements=placements,
    )
