"""Verify the engine by computing Vandana's chart.

Birth: 08 Dec 2003, 13:30 IST, Surat (Gujarat).
Expected (from the manual reading the founder received earlier):
    Lagna       : Pisces (~4°), Uttara Bhadrapada
    Moon        : Taurus (~18°), Rohini  -> exalted
    Sun         : Scorpio (~22°)
    Jupiter     : Cancer (~23°)          -> exalted, in 5th
    Saturn (R)  : Gemini, in 4th
    Mars        : Aquarius, in 12th
    Mercury+Venus: Sagittarius, in 10th
    Rahu        : Aries, in 2nd
    Ketu        : Libra, in 8th
"""

from __future__ import annotations
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from kundlikosh_engine import (
    compute_chart,
    chart_to_dict,
    current_dasha,
    dasha_timeline,
    detect_yogas,
)


def fmt_deg(d: float) -> str:
    deg = int(d)
    rem = (d - deg) * 60
    minu = int(rem)
    sec = int((rem - minu) * 60)
    return f"{deg:02d}°{minu:02d}'{sec:02d}\""


def print_section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main() -> None:
    chart = compute_chart(
        name="Vandana",
        date="2003-12-08",
        time="13:30",
        timezone_name="Asia/Kolkata",
        latitude=21.1702,    # Surat
        longitude=72.8311,
    )

    print_section("KUNDLIKOSH ENGINE  ·  VERIFICATION CHART")
    print(f"Name              : {chart.name}")
    print(f"Birth (local)     : {chart.birth_dt_local}")
    print(f"Birth (UTC)       : {chart.birth_dt_utc}")
    print(f"Latitude          : {chart.latitude}°")
    print(f"Longitude         : {chart.longitude}°")
    print(f"Ayanamsa (Lahiri) : {fmt_deg(chart.ayanamsa)}")

    print_section("LAGNA & CORE")
    print(f"Lagna (Ascendant) : {chart.lagna_sign} ({chart.lagna_sign_hi})  "
          f"{fmt_deg(chart.lagna_degree_in_sign)}  "
          f"·  Nakshatra: {chart.lagna_nakshatra} pada {chart.lagna_pada}")
    print(f"Moon Sign (Rashi) : {chart.moon_sign} ({chart.moon_sign_hi})  "
          f"·  Nakshatra: {chart.moon_nakshatra} pada {chart.moon_pada}  "
          f"(lord: {chart.moon_nakshatra_lord})")
    print(f"Sun Sign (Vedic)  : {chart.sun_sign}")

    print_section("PATRON DEITY (from Moon's nakshatra)")
    p = chart.patron_deity
    print(f"  Nakshatra : {p['nakshatra']} ({p['nakshatra_hi']})")
    print(f"  Devata    : {p['deity']} ({p['deity_hi']})")
    print(f"  Symbol    : {p['symbol']}")

    print_section("PLANETS")
    header = f"{'Planet':<8} {'Sign':<14} {'Deg':>10}  {'House':>5}  {'Nakshatra':<22} {'Pada':>4}  {'Dignity':<12} {'R'}"
    print(header)
    print("-" * len(header))
    for pp in chart.planets:
        retro = "R" if pp.retrograde else " "
        print(
            f"{pp.name:<8} {pp.sign:<14} {fmt_deg(pp.degree_in_sign):>10}  "
            f"{pp.house:>5}  {pp.nakshatra + ' (P' + str(pp.pada) + ')':<22} "
            f"{pp.pada:>4}  {pp.dignity:<12} {retro}"
        )

    print_section("VIMSHOTTARI DASHA — current period")
    cur = current_dasha(chart)
    if cur["mahadasha"]:
        md = cur["mahadasha"]
        print(f"Mahadasha    : {md['lord']:<8}  {md['start']}  →  {md['end']}  "
              f"({md['duration_years']} years)")
    if cur["antardasha"]:
        bd = cur["antardasha"]
        print(f"Antardasha   : {bd['lord']:<8}  {bd['start']}  →  {bd['end']}")

    print_section("DASHA TIMELINE — first 4 mahadashas")
    timeline = dasha_timeline(chart, num_mahadashas=4)
    for md in timeline:
        print(f"\n  {md['lord']:<8}  ({md['duration_years']} yr)  "
              f"{md['start']}  →  {md['end']}")
        for bd in md["antardashas"]:
            print(f"     └─ {bd['lord']:<8} {bd['start']} → {bd['end']}")

    print_section("DETECTED YOGAS / DOSHAS")
    yogas = detect_yogas(chart)
    if not yogas:
        print("  (none detected by current ruleset)")
    for y in yogas:
        flag = ""
        if y.get("is_cancelled"):
            flag = "   [cancelled]"
        print(f"  • {y['name']} ({y.get('name_hi','')})  [{y['category']}]{flag}")
        print(f"      {y['description']}")

    print_section("RAW CHART JSON  (truncated)")
    j = chart_to_dict(chart)
    snippet = json.dumps(j, indent=2, default=str)[:1200]
    print(snippet + "\n  ...")


if __name__ == "__main__":
    main()
