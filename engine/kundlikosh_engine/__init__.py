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
]

__version__ = "0.1.0"
