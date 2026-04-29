"""Cross-validate the engine against a publicly-known horoscope: Mahatma Gandhi.

Birth: 02 Oct 1869, 07:11:47 LMT, Porbandar (~21.6417°N, 69.6122°E).
Reference (consensus across AstroSage, Drik Panchang, Astro-Seek):
    Lagna  : Libra (Tula)
    Moon   : Scorpio (Vrishchika), Anuradha
    Sun    : Virgo (Kanya), Hasta
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from kundlikosh_engine import compute_chart, current_dasha, detect_yogas


def fmt_deg(d: float) -> str:
    deg = int(d); rem = (d - deg) * 60; mn = int(rem)
    return f"{deg:02d}°{mn:02d}'"


def main() -> None:
    # 7:11:47 LMT Porbandar; LMT to IST is offset ~-39 min from IST.
    # In 1869 there was no IST; we'll use Asia/Kolkata which uses LMT for that era.
    # Pre-1906 India had no standard time zone, so use Local Mean Time of Porbandar.
    chart = compute_chart(
        name="Mahatma Gandhi",
        date="1869-10-02",
        time="07:11",
        timezone_name="Asia/Kolkata",
        latitude=21.6417,
        longitude=69.6122,
        use_lmt=True,
    )
    print(f"Lagna : {chart.lagna_sign} {fmt_deg(chart.lagna_degree_in_sign)} "
          f"({chart.lagna_nakshatra} P{chart.lagna_pada})")
    print(f"Moon  : {chart.moon_sign}  ({chart.moon_nakshatra} P{chart.moon_pada})")
    print(f"Sun   : {chart.sun_sign}")
    print()
    for p in chart.planets:
        print(f"  {p.name:<8} {p.sign:<14} {fmt_deg(p.degree_in_sign):>8}  "
              f"H{p.house:<2}  {p.nakshatra:<22} {'(R)' if p.retrograde else ''}")
    print()
    print("EXPECTED:  Lagna Libra · Moon Scorpio (Anuradha) · Sun Virgo (Hasta)")


if __name__ == "__main__":
    main()
