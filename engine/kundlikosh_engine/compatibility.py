"""Ashtakoot Guna Milan — 36-point Vedic marriage compatibility.

Eight kootas with weighted points:
    1. Varna       — 1
    2. Vashya      — 2
    3. Tara        — 3
    4. Yoni        — 4
    5. Graha Maitri— 5
    6. Gana        — 6
    7. Bhakoot     — 7
    8. Nadi        — 8

Plus dosha checks: Mangal (Manglik), Bhakoot, Nadi.

Reference: Muhurta Chintamani, ch. on Vivaha; standard modern jyotish convention.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from . import constants as K
from .chart import Chart, PlanetPosition, nakshatra_info


# --- Helpers ---------------------------------------------------------------
def _moon_long(chart: Chart) -> float:
    return next(p.longitude for p in chart.planets if p.name == "Moon")

def _moon_sign_index(chart: Chart) -> int:
    return next(p.sign_index for p in chart.planets if p.name == "Moon")

def _moon_nakshatra_index(chart: Chart) -> int:
    nk_idx, _ = nakshatra_info(_moon_long(chart))
    return nk_idx


# --- 1. Varna (1 point) ---------------------------------------------------
# Moon-sign caste: water signs = Brahmin, fire = Kshatriya, air = Vaishya, earth = Shudra
# Score: full 1 if groom >= bride; else 0
_VARNA_BY_SIGN = {
    "Cancer": 4, "Scorpio": 4, "Pisces": 4,        # Brahmin
    "Aries":  3, "Leo":     3, "Sagittarius": 3,   # Kshatriya
    "Gemini": 2, "Libra":   2, "Aquarius":    2,   # Vaishya
    "Taurus": 1, "Virgo":   1, "Capricorn":   1,   # Shudra
}

def koota_varna(bride: Chart, groom: Chart) -> tuple[float, str]:
    b = _VARNA_BY_SIGN[bride.moon_sign]
    g = _VARNA_BY_SIGN[groom.moon_sign]
    return (1.0 if g >= b else 0.0), f"Bride={bride.moon_sign}({b}), Groom={groom.moon_sign}({g})"


# --- 2. Vashya (2 points) -------------------------------------------------
_VASHYA_GROUP = {
    "Aries": "Chatushpada", "Taurus": "Chatushpada", "Sagittarius": "Chatushpada",
    "Capricorn": "Chatushpada",
    "Leo": "Vanachara",
    "Cancer": "Jalachara", "Pisces": "Jalachara",
    "Scorpio": "Keeta",
    "Gemini": "Manava", "Virgo": "Manava", "Libra": "Manava", "Aquarius": "Manava",
}
# Compatibility matrix — Pradeep Astrology / Muhurta Chintamani convention
_VASHYA_MATRIX = {
    "Chatushpada":  {"Chatushpada": 2.0, "Manava": 1.0, "Jalachara": 1.0,
                     "Vanachara": 0.5, "Keeta": 1.0},
    "Manava":       {"Manava": 2.0, "Chatushpada": 1.0, "Jalachara": 0.5,
                     "Vanachara": 0.5, "Keeta": 0.5},
    "Jalachara":    {"Jalachara": 2.0, "Chatushpada": 1.0, "Manava": 0.5,
                     "Keeta": 1.0, "Vanachara": 0.5},
    "Vanachara":    {"Vanachara": 2.0, "Chatushpada": 0.5, "Jalachara": 1.0,
                     "Manava": 0.5, "Keeta": 0.5},
    "Keeta":        {"Keeta": 2.0, "Jalachara": 1.0, "Chatushpada": 1.0,
                     "Manava": 0.5, "Vanachara": 0.5},
}

def koota_vashya(bride: Chart, groom: Chart) -> tuple[float, str]:
    b = _VASHYA_GROUP[bride.moon_sign]
    g = _VASHYA_GROUP[groom.moon_sign]
    score = _VASHYA_MATRIX.get(b, {}).get(g, 0.0)
    return score, f"Bride={b}, Groom={g}"


# --- 3. Tara (3 points) ---------------------------------------------------
def _tara_score_for(reference_nk: int, partner_nk: int) -> int:
    diff = (partner_nk - reference_nk) % 9 + 1   # 1..9
    return diff

def koota_tara(bride: Chart, groom: Chart) -> tuple[float, str]:
    b_nk = _moon_nakshatra_index(bride)
    g_nk = _moon_nakshatra_index(groom)
    # Each side counts from itself; auspicious taras are 2,4,6,8,9 (=Sampat,Kshema,Sadhaka,Mitra,Ati-Mitra)
    AUSP = {2, 4, 6, 8, 9}
    g_from_b = (g_nk - b_nk) % 9 + 1
    b_from_g = (b_nk - g_nk) % 9 + 1
    auspicious_count = (1 if g_from_b in AUSP else 0) + (1 if b_from_g in AUSP else 0)
    score = (auspicious_count / 2.0) * 3.0
    return score, f"From bride: {g_from_b}/9, From groom: {b_from_g}/9"


# --- 4. Yoni (4 points) ---------------------------------------------------
# Each nakshatra has an animal symbol; 14 yonis paired by attraction/enmity
NAKSHATRA_YONI = [
    "Horse",  # Ashwini
    "Elephant",  # Bharani
    "Sheep",  # Krittika
    "Serpent",  # Rohini
    "Serpent",  # Mrigashira
    "Dog",  # Ardra
    "Cat",  # Punarvasu
    "Sheep",  # Pushya
    "Cat",  # Ashlesha
    "Rat",  # Magha
    "Rat",  # Purva Phalguni
    "Cow",  # Uttara Phalguni
    "Buffalo",  # Hasta
    "Tiger",  # Chitra
    "Buffalo",  # Swati
    "Tiger",  # Vishakha
    "Deer",  # Anuradha
    "Deer",  # Jyeshtha
    "Dog",  # Mula
    "Monkey",  # Purva Ashadha
    "Mongoose",  # Uttara Ashadha
    "Monkey",  # Shravana
    "Lion",  # Dhanishta
    "Horse",  # Shatabhisha
    "Lion",  # Purva Bhadrapada
    "Cow",  # Uttara Bhadrapada
    "Elephant",  # Revati
]
# Enemies (subtract 0 points), neutrals (2), friends (3), same yoni (4)
_YONI_ENEMIES = {
    ("Horse", "Buffalo"), ("Cow", "Tiger"), ("Elephant", "Lion"),
    ("Sheep", "Monkey"), ("Serpent", "Mongoose"), ("Cat", "Rat"),
    ("Dog", "Deer"),
}

def koota_yoni(bride: Chart, groom: Chart) -> tuple[float, str]:
    b_nk = _moon_nakshatra_index(bride)
    g_nk = _moon_nakshatra_index(groom)
    by = NAKSHATRA_YONI[b_nk]
    gy = NAKSHATRA_YONI[g_nk]
    pair1, pair2 = (by, gy), (gy, by)
    if by == gy:
        score = 4.0
    elif pair1 in _YONI_ENEMIES or pair2 in _YONI_ENEMIES:
        score = 0.0
    else:
        score = 2.0   # neutrals (simplified)
    return score, f"Bride={by}, Groom={gy}"


# --- 5. Graha Maitri (5 points) -------------------------------------------
_PLANET_FRIEND = {
    "Sun":     {"friend": ["Moon", "Mars", "Jupiter"], "enemy": ["Venus", "Saturn"], "neutral": ["Mercury"]},
    "Moon":    {"friend": ["Sun", "Mercury"], "enemy": [], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"]},
    "Mars":    {"friend": ["Sun", "Moon", "Jupiter"], "enemy": ["Mercury"], "neutral": ["Venus", "Saturn"]},
    "Mercury": {"friend": ["Sun", "Venus"], "enemy": ["Moon"], "neutral": ["Mars", "Jupiter", "Saturn"]},
    "Jupiter": {"friend": ["Sun", "Moon", "Mars"], "enemy": ["Mercury", "Venus"], "neutral": ["Saturn"]},
    "Venus":   {"friend": ["Mercury", "Saturn"], "enemy": ["Sun", "Moon"], "neutral": ["Mars", "Jupiter"]},
    "Saturn":  {"friend": ["Mercury", "Venus"], "enemy": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]},
}

def _moon_sign_lord(chart: Chart) -> str:
    return K.SIGN_LORDS[_moon_sign_index(chart)]

def koota_graha_maitri(bride: Chart, groom: Chart) -> tuple[float, str]:
    bl = _moon_sign_lord(bride)
    gl = _moon_sign_lord(groom)
    if bl == gl:
        score = 5.0; label = "same lord"
    elif gl in _PLANET_FRIEND[bl]["friend"] and bl in _PLANET_FRIEND[gl]["friend"]:
        score = 5.0; label = "mutual friends"
    elif gl in _PLANET_FRIEND[bl]["friend"] or bl in _PLANET_FRIEND[gl]["friend"]:
        score = 4.0; label = "one-way friend"
    elif gl in _PLANET_FRIEND[bl]["neutral"] or bl in _PLANET_FRIEND[gl]["neutral"]:
        score = 1.0; label = "neutral"
    else:
        score = 0.0; label = "enemy"
    return score, f"Bride lord={bl}, Groom lord={gl} ({label})"


# --- 6. Gana (6 points) ---------------------------------------------------
NAKSHATRA_GANA = [
    "Deva",     # Ashwini
    "Manushya", # Bharani
    "Rakshasa", # Krittika
    "Manushya", # Rohini
    "Deva",     # Mrigashira
    "Manushya", # Ardra
    "Deva",     # Punarvasu
    "Deva",     # Pushya
    "Rakshasa", # Ashlesha
    "Rakshasa", # Magha
    "Manushya", # Purva Phalguni
    "Manushya", # Uttara Phalguni
    "Deva",     # Hasta
    "Rakshasa", # Chitra
    "Deva",     # Swati
    "Rakshasa", # Vishakha
    "Deva",     # Anuradha
    "Rakshasa", # Jyeshtha
    "Rakshasa", # Mula
    "Manushya", # Purva Ashadha
    "Manushya", # Uttara Ashadha
    "Deva",     # Shravana
    "Rakshasa", # Dhanishta
    "Rakshasa", # Shatabhisha
    "Manushya", # Purva Bhadrapada
    "Manushya", # Uttara Bhadrapada
    "Deva",     # Revati
]

def koota_gana(bride: Chart, groom: Chart) -> tuple[float, str]:
    b = NAKSHATRA_GANA[_moon_nakshatra_index(bride)]
    g = NAKSHATRA_GANA[_moon_nakshatra_index(groom)]
    if b == g:
        score = 6.0
    elif {b, g} == {"Deva", "Manushya"}:
        score = 5.0   # one-side
    elif {b, g} == {"Manushya", "Rakshasa"}:
        score = 1.0
    else:
        score = 0.0   # Deva-Rakshasa
    return score, f"Bride={b}, Groom={g}"


# --- 7. Bhakoot (7 points) ------------------------------------------------
_BHAKOOT_BAD = {(2, 12), (5, 9), (6, 8)}    # 2-12, 5-9, 6-8 are doshic axes

def koota_bhakoot(bride: Chart, groom: Chart) -> tuple[float, str]:
    b_sign = _moon_sign_index(bride)
    g_sign = _moon_sign_index(groom)
    diff_a = ((g_sign - b_sign) % 12) + 1
    diff_b = ((b_sign - g_sign) % 12) + 1
    pair = tuple(sorted([diff_a, diff_b]))
    bad_pairs = {(2, 12), (5, 9), (6, 8)}
    if pair in bad_pairs:
        return 0.0, f"Bhakoot dosha ({pair[0]}-{pair[1]} axis)"
    if (diff_a == 1 and diff_b == 1):
        return 7.0, "Same sign — auspicious"
    return 7.0, f"{diff_a}-{diff_b} axis (auspicious)"


# --- 8. Nadi (8 points) ---------------------------------------------------
NAKSHATRA_NADI = [
    "Adi",    "Madhya", "Antya",
    "Antya",  "Madhya", "Adi",
    "Adi",    "Madhya", "Antya",
    "Antya",  "Madhya", "Adi",
    "Adi",    "Madhya", "Antya",
    "Antya",  "Madhya", "Adi",
    "Adi",    "Madhya", "Antya",
    "Antya",  "Madhya", "Adi",
    "Adi",    "Madhya", "Antya",
]

def koota_nadi(bride: Chart, groom: Chart) -> tuple[float, str]:
    b = NAKSHATRA_NADI[_moon_nakshatra_index(bride)]
    g = NAKSHATRA_NADI[_moon_nakshatra_index(groom)]
    if b == g:
        return 0.0, f"Both {b} — Nadi dosha (consider remedies)"
    return 8.0, f"Bride={b}, Groom={g}"


# --- Mangal Dosha Check ----------------------------------------------------
def manglik_status(chart: Chart) -> dict:
    mars = next(p for p in chart.planets if p.name == "Mars")
    moon = next(p for p in chart.planets if p.name == "Moon")
    venus = next(p for p in chart.planets if p.name == "Venus")
    bad_houses = {1, 4, 7, 8, 12}

    def from_(ref_idx: int) -> int:
        return ((mars.sign_index - ref_idx) % 12) + 1

    sources = []
    if mars.house in bad_houses:
        sources.append(f"Lagna ({mars.house}H)")
    if from_(moon.sign_index) in bad_houses:
        sources.append(f"Moon ({from_(moon.sign_index)}H from Moon)")
    if from_(venus.sign_index) in bad_houses:
        sources.append(f"Venus ({from_(venus.sign_index)}H from Venus)")
    cancelled = mars.dignity in ("own_sign", "exalted") or mars.sign in {"Aries", "Leo", "Sagittarius"}
    return {
        "is_manglik": bool(sources),
        "sources": sources,
        "softened": cancelled,
        "mars_sign": mars.sign,
        "mars_house": mars.house,
        "mars_dignity": mars.dignity,
    }


# --- Top-level Guna Milan --------------------------------------------------
@dataclass
class KootaResult:
    name: str
    score: float
    max_score: float
    note: str

@dataclass
class GunaMilanResult:
    bride: str
    groom: str
    kootas: list[KootaResult]
    total_score: float
    max_total: float
    bride_manglik: dict
    groom_manglik: dict
    manglik_balanced: bool


def guna_milan(bride: Chart, groom: Chart) -> GunaMilanResult:
    fns = [
        ("Varna",        koota_varna,        1),
        ("Vashya",       koota_vashya,       2),
        ("Tara",         koota_tara,         3),
        ("Yoni",         koota_yoni,         4),
        ("Graha Maitri", koota_graha_maitri, 5),
        ("Gana",         koota_gana,         6),
        ("Bhakoot",      koota_bhakoot,      7),
        ("Nadi",         koota_nadi,         8),
    ]
    results: list[KootaResult] = []
    total = 0.0
    for name, fn, mx in fns:
        score, note = fn(bride, groom)
        results.append(KootaResult(name=name, score=score, max_score=float(mx), note=note))
        total += score

    bm = manglik_status(bride)
    gm = manglik_status(groom)
    # When both are manglik, dosha cancels (symmetric); when neither is, it's fine; mismatch = real issue.
    balanced = (bm["is_manglik"] == gm["is_manglik"])

    return GunaMilanResult(
        bride=bride.name,
        groom=groom.name,
        kootas=results,
        total_score=total,
        max_total=36.0,
        bride_manglik=bm,
        groom_manglik=gm,
        manglik_balanced=balanced,
    )
