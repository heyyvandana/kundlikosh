# 🪔 KundliKosh (कुंडलीकोश)

> Authentic Vedic astrology + Indian mythology — built for Indian seekers, on a tight budget.

A real, accurate, beautifully Indian Vedic astrology Android app. Powered by Swiss Ephemeris (the same calculation engine ₹50,000 professional software uses). Free to build. ₹2,100 one-time to launch.

## Status

**Phase 1a — Astrology Engine** · in progress

- [x] Project scaffolded
- [x] Swiss Ephemeris integration (Lahiri sidereal)
- [x] Birth-chart calculation (Lagna, planets, houses, nakshatras, padas, dignities)
- [x] Vimshottari Mahadasha + Antardasha
- [x] Indian-mythology integration (27 nakshatra deities, 9 graha deities, mantras)
- [x] First yogas/doshas detector (Gajakesari, Budha-Aditya, Adhi, Sarala/Vipareeta Raja, Mangal Dosha, etc.)
- [ ] Navamsa (D9) chart
- [ ] More vargas (D10, D7, D60)
- [ ] Ashtakavarga
- [ ] Compatibility / Guna Milan API
- [ ] FastAPI HTTP wrapper for the mobile app to consume

## Project layout

```
kundlikosh/
├── engine/          # Python · Vedic astrology calculation core
│   ├── kundlikosh_engine/
│   │   ├── chart.py        # Chart computation (Swiss Ephemeris)
│   │   ├── dasha.py        # Vimshottari dashas
│   │   ├── yogas.py        # Yoga / dosha detectors
│   │   └── constants.py    # Signs, nakshatras, deities (EN/HI/SA)
│   ├── scripts/
│   │   ├── verify_vandana.py
│   │   └── verify_gandhi.py
│   └── pyproject.toml
├── app/              # React Native (Expo) — to be added
└── docs/             # Roadmap, architecture, design notes
```

## Quick start (engine)

```bash
cd engine
pip install -e .
python scripts/verify_vandana.py
```

## License

MIT — but the Indian mythological content is offered with reverence and the spirit of public service.
