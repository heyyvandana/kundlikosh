"""End-to-end test: compute Vandana's chart, her D9/D10, and her compatibility
with the two Navsari boys we discussed earlier.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from kundlikosh_engine import (
    compute_chart, compute_varga, guna_milan, manglik_status, current_dasha
)


def line(t=""):
    print("\n" + "=" * 72)
    if t:
        print(t)
        print("=" * 72)


def show_varga(v):
    line(f"{v.name} Chart  ·  Lagna: {v.lagna_sign}")
    print(f"{'Planet':<10}{'Sign':<14}{'House':>5}")
    print("-" * 30)
    for p in v.placements:
        print(f"{p['name']:<10}{p['sign']:<14}{p['house']:>5}")


def show_match(m):
    line(f"GUNA MILAN  ·  {m.bride}  ↔  {m.groom}")
    print(f"{'Koota':<14}{'Score':>10}{'  Note'}")
    print("-" * 60)
    for k in m.kootas:
        print(f"{k.name:<14}{k.score:>5.1f}/{int(k.max_score)}    {k.note}")
    print("-" * 60)
    print(f"{'TOTAL':<14}{m.total_score:>5.1f}/{int(m.max_total)}")
    print()
    print(f"Bride Manglik?  {'Yes' if m.bride_manglik['is_manglik'] else 'No'}  "
          f"(Mars in {m.bride_manglik['mars_sign']} H{m.bride_manglik['mars_house']}, "
          f"{', '.join(m.bride_manglik['sources']) or 'no sources'})"
          f"{' [softened]' if m.bride_manglik['softened'] else ''}")
    print(f"Groom Manglik?  {'Yes' if m.groom_manglik['is_manglik'] else 'No'}  "
          f"(Mars in {m.groom_manglik['mars_sign']} H{m.groom_manglik['mars_house']}, "
          f"{', '.join(m.groom_manglik['sources']) or 'no sources'})"
          f"{' [softened]' if m.groom_manglik['softened'] else ''}")
    print(f"Manglik balance:  {'BOTH-Manglik OR neither — neutral' if m.manglik_balanced else '⚠ MISMATCH (one Manglik, other not)'}")


def main() -> None:
    bride = compute_chart(
        name="Vandana", date="2003-12-08", time="13:30",
        timezone_name="Asia/Kolkata",
        latitude=21.1702, longitude=72.8311,
    )
    groom1 = compute_chart(
        name="Vadodara boy", date="2001-08-07", time="09:14",
        timezone_name="Asia/Kolkata",
        latitude=22.3072, longitude=73.1812,
    )
    groom2 = compute_chart(
        name="Navsari boy (19 Feb)", date="2003-02-19", time="11:45",
        timezone_name="Asia/Kolkata",
        latitude=20.9467, longitude=72.9520,
    )
    groom3 = compute_chart(
        name="Navsari boy (13 Feb)", date="2003-02-13", time="11:45",
        timezone_name="Asia/Kolkata",
        latitude=20.9467, longitude=72.9520,
    )

    line("VANDANA — Birth Chart Summary")
    print(f"Lagna: {bride.lagna_sign} {bride.lagna_degree_in_sign:.2f}°  ({bride.lagna_nakshatra} P{bride.lagna_pada})")
    print(f"Moon : {bride.moon_sign}  ({bride.moon_nakshatra} P{bride.moon_pada})")
    print(f"Sun  : {bride.sun_sign}")
    cur = current_dasha(bride)
    if cur["mahadasha"]:
        md = cur["mahadasha"]; bd = cur["antardasha"]
        print(f"Now  : {md['lord']} mahadasha  /  {bd['lord']} antardasha"
              f"  ({bd['start']} → {bd['end']})")

    # D9 + D10
    show_varga(compute_varga(bride, "D9"))
    show_varga(compute_varga(bride, "D10"))

    # Compatibility
    show_match(guna_milan(bride, groom1))
    show_match(guna_milan(bride, groom2))
    show_match(guna_milan(bride, groom3))


if __name__ == "__main__":
    main()
