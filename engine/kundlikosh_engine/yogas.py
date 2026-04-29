"""Detect classical Vedic yogas and doshas in a chart.

This is a starter set; we'll keep adding detectors as Phase 1 progresses.
"""

from __future__ import annotations

from typing import Iterable

from .chart import Chart, PlanetPosition


def _by(name: str, planets: Iterable[PlanetPosition]) -> PlanetPosition | None:
    for p in planets:
        if p.name == name:
            return p
    return None


def detect_yogas(chart: Chart) -> list[dict]:
    yogas: list[dict] = []
    p = chart.planets

    sun     = _by("Sun", p)
    moon    = _by("Moon", p)
    mars    = _by("Mars", p)
    mercury = _by("Mercury", p)
    jupiter = _by("Jupiter", p)
    venus   = _by("Venus", p)
    saturn  = _by("Saturn", p)
    rahu    = _by("Rahu", p)
    ketu    = _by("Ketu", p)

    # 1. Gajakesari — Moon and Jupiter in mutual kendra (1, 4, 7, 10 from each other)
    if moon and jupiter:
        diff = (moon.sign_index - jupiter.sign_index) % 12
        if diff in (0, 3, 6, 9):
            yogas.append({
                "name": "Gajakesari Yoga",
                "name_hi": "गजकेसरी योग",
                "category": "auspicious",
                "description": "Moon and Jupiter in mutual kendra (1/4/7/10) — gives intelligence, dignity, eloquence, lasting respect.",
            })

    # 2. Budha-Aditya — Sun and Mercury in same sign (without combustion ruining it)
    if sun and mercury and sun.sign_index == mercury.sign_index:
        yogas.append({
            "name": "Budha-Aditya Yoga",
            "name_hi": "बुध-आदित्य योग",
            "category": "auspicious",
            "description": "Sun and Mercury together — sharp intelligence, communication ability, success in scholarly/professional work.",
        })

    # 3. Chandra-Mangal — Moon and Mars together
    if moon and mars and moon.sign_index == mars.sign_index:
        yogas.append({
            "name": "Chandra-Mangal Yoga",
            "name_hi": "चन्द्र-मंगल योग",
            "category": "wealth",
            "description": "Moon and Mars conjunction — strong drive, ability to earn through enterprise.",
        })

    # 4. Exalted lagna lord — generally great
    LAGNA_LORDS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
        "Pisces": "Jupiter",
    }
    lagna_lord_name = LAGNA_LORDS.get(chart.lagna_sign)
    lagna_lord = _by(lagna_lord_name, p) if lagna_lord_name else None
    if lagna_lord and lagna_lord.dignity == "exalted":
        yogas.append({
            "name": "Exalted Lagna Lord",
            "name_hi": "उच्च लग्नेश",
            "category": "auspicious",
            "description": f"{lagna_lord_name} (lagna lord) is exalted in {lagna_lord.sign} — strong sense of self, vitality, and life direction.",
        })

    # 5. Adhi Yoga — benefics (Mercury, Jupiter, Venus) in 6th, 7th, 8th from Moon
    if moon and mercury and jupiter and venus:
        moon_sign = moon.sign_index
        benefics = [mercury, jupiter, venus]
        houses_from_moon = {((b.sign_index - moon_sign) % 12) + 1 for b in benefics}
        if {6, 7, 8}.issubset(houses_from_moon):
            yogas.append({
                "name": "Adhi Yoga",
                "name_hi": "अधि योग",
                "category": "auspicious",
                "description": "Benefics in 6th, 7th, 8th from Moon — leadership, prosperity, longevity.",
            })

    # 6. Vipareeta Raja Yoga (Sarala) — Lord of 8th in 8th, or 6th lord in 6th, etc.,
    #    when malefic planet stays in dusthana but in own/exalted state.
    if mars and mars.house == 8 and mars.dignity == "own_sign":
        yogas.append({
            "name": "Sarala Yoga (Vipareeta Raja Yoga via 8th)",
            "name_hi": "सरल योग (विपरीत राजयोग)",
            "category": "transformative",
            "description": "Mars in own sign in the 8th — adversity converts to gain; hidden strength and resilience.",
        })

    # 7. Mangal Dosha (Manglik) — Mars in 1, 4, 7, 8, 12 from Lagna OR from Moon OR from Venus
    if mars:
        mars_house_lagna = mars.house
        moon_sign = moon.sign_index if moon else None
        venus_sign = venus.sign_index if venus else None

        def house_from(reference_sign_idx: int) -> int:
            return ((mars.sign_index - reference_sign_idx) % 12) + 1

        manglik_houses = {1, 4, 7, 8, 12}
        is_manglik = False
        sources = []
        if mars_house_lagna in manglik_houses:
            is_manglik = True
            sources.append("Lagna")
        if moon_sign is not None and house_from(moon_sign) in manglik_houses:
            is_manglik = True
            sources.append("Moon")
        if venus_sign is not None and house_from(venus_sign) in manglik_houses:
            is_manglik = True
            sources.append("Venus")

        # Cancellation if Mars is in own/exalted sign or in Aries/Leo/Sagittarius (fiery)
        cancelled = mars.dignity in ("own_sign", "exalted")

        if is_manglik:
            yogas.append({
                "name": "Mangal Dosha",
                "name_hi": "मंगल दोष",
                "category": "dosha",
                "description": (
                    f"Mars in marriage-sensitive house from {', '.join(sources)}. "
                    f"{'Severity reduced — Mars is in own/exalted sign.' if cancelled else 'Standard remedies recommended.'}"
                ),
                "is_cancelled": cancelled,
            })

    return yogas
