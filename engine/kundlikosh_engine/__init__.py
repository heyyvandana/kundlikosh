"""KundliKosh — Vedic astrology engine.

Real Lahiri-sidereal calculations powered by Swiss Ephemeris.
"""

from .chart import (
    Chart,
    PlanetPosition,
    chart_to_dict,
    compute_chart,
)
from .dasha import (
    DashaPeriod,
    compute_antardashas,
    compute_mahadashas,
    current_dasha,
    dasha_timeline,
)
from .yogas import detect_yogas
from .vargas import VargaChart, compute_varga
from .compatibility import (
    GunaMilanResult,
    KootaResult,
    guna_milan,
    manglik_status,
)
from .panchang import Panchang, compute_panchang
from .daily import DailyReading, compute_daily_reading
from .phalit import Chapter, LifeStory, compute_life_story

__all__ = [
    "Chart",
    "PlanetPosition",
    "chart_to_dict",
    "compute_chart",
    "DashaPeriod",
    "compute_antardashas",
    "compute_mahadashas",
    "current_dasha",
    "dasha_timeline",
    "detect_yogas",
    "VargaChart",
    "compute_varga",
    "GunaMilanResult",
    "KootaResult",
    "guna_milan",
    "manglik_status",
    "Panchang",
    "compute_panchang",
    "DailyReading",
    "compute_daily_reading",
    "Chapter",
    "LifeStory",
    "compute_life_story",
]

__version__ = "0.1.0"
