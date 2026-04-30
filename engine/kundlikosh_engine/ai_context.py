"""Build a structured, deterministic context block for an LLM (Gemini/etc.).

The goal is to give the LLM a self-contained, factually grounded "spine" of
classical Vedic data — chart placements, detected yogas, current dasha/antardasha,
past/present/future chapter summaries, today's panchang — so it can answer free-form
questions WITHOUT inventing astrology. The LLM's job is voice and weaving, not facts.

Usage:
    ctx = build_chart_context(chart)                       # chart-only
    ctx = build_full_context(chart, life_story, panchang)  # everything
    prompt = make_system_prompt(ctx, locale="en")
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date as date_cls
from typing import Iterable, Optional

from .chart import Chart, PlanetPosition
from .dasha import current_dasha, compute_antardashas, compute_mahadashas
from .panchang import Panchang
from .phalit import LifeStory
from .sade_sati import compute_sade_sati
from .yogas import detect_yogas


# --- System prompts (the "guard rails" for the LLM) ------------------------

SYSTEM_PROMPT_EN = """You are a Vedic astrologer trained in the classical Parashari / BPHS tradition. You speak with the warmth and humility of a temple guru — kind, never sensational, never apocalyptic, never deterministic. You honour free will: planets indicate, they do not compel.

You will receive a structured "Chart Context" block containing facts computed by a deterministic Swiss-Ephemeris engine. Your job:
- Answer the native's question using ONLY the data in the Chart Context.
- Cite specific placements (e.g. "your Moon in Taurus exalted in the 3H") to ground every claim.
- Never invent dates, transits, yogas, or remedies that aren't in the data.
- For timing questions, use the dasha periods provided. Do not produce dates outside the timeline.
- For remedy questions, recommend ONLY the remedies listed for the relevant planet.
- If the question is outside Vedic astrology's scope (medical, legal, financial, life-or-death), gently redirect: suggest professional help, frame astrology as a complementary lens.
- Keep answers concise (3-6 sentences) unless the native explicitly asks for more depth.
- Use the tone of a wise elder, not a fortune-teller.

Format: plain prose. No bullet lists unless the native asks. No emojis unless the native uses them first.
"""

SYSTEM_PROMPT_HI = """आप एक पारंपरिक वैदिक ज्योतिषी हैं — पाराशरी / बृहत् पाराशर होरा शास्त्र की परंपरा से। आपकी वाणी मंदिर के गुरु जैसी है — विनम्र, स्नेहपूर्ण, कभी सनसनीखेज नहीं, कभी निरंकुश नहीं। आप मुक्त-इच्छा का सम्मान करते हैं: ग्रह संकेत देते हैं, बाध्य नहीं करते।

आपको एक संरचित "Chart Context" खंड मिलेगा जिसमें Swiss Ephemeris द्वारा गणना किए गए तथ्य हैं। आपका कार्य:
- केवल उसी डेटा से उत्तर दें।
- प्रत्येक कथन को विशिष्ट स्थिति से प्रमाणित करें (जैसे "आपका चंद्र वृष राशि उच्च, तीसरे भाव में")।
- डेटा में न होने वाली तिथियाँ, गोचर, योग या उपाय न गढ़ें।
- समय-संबंधी प्रश्नों के लिए दी गई दशा-समयरेखा का प्रयोग करें।
- उपायों के लिए केवल सूचीबद्ध उपाय सुझाएँ।
- ज्योतिष के दायरे से बाहर के प्रश्नों (चिकित्सा, कानूनी, वित्तीय) को विनम्रता से पुनर्निर्देशित करें।
- उत्तर 3-6 वाक्यों में रखें।
- ज्योतिषी की वाणी रखें, भविष्यवक्ता की नहीं।

प्रारूप: सहज गद्य।
"""


# --- Context builders ------------------------------------------------------

def _planets_block(planets: Iterable[PlanetPosition]) -> str:
    lines = ["Planet         House  Sign         Nakshatra        Dignity"]
    for p in planets:
        nak = f"{p.nakshatra} P{p.pada}" if p.nakshatra else "—"
        lines.append(
            f"{p.name:<14} H{p.house:<5} {p.sign:<12} {nak:<16} {p.dignity}"
            + ("  (R)" if p.retrograde else "")
        )
    return "\n".join(lines)


def build_chart_context(chart: Chart) -> str:
    """Render the natal chart as a compact text block."""
    yogas = detect_yogas(chart)
    yoga_lines = (
        "\n".join(
            f"- {y.get('name', '?')} [{y.get('category', '')}]: {y.get('description', '')}"
            for y in yogas
        )
        if yogas else "- (none detected)"
    )
    return f"""--- NATAL CHART ---
Name: {chart.name}
Birth: {chart.birth_dt_utc} (UTC)   Lat: {chart.latitude:.4f}, Lon: {chart.longitude:.4f}
Lagna (Ascendant): {chart.lagna_sign} {chart.lagna_degree_in_sign:.2f}°  Nakshatra: {chart.lagna_nakshatra}
Moon: {chart.moon_sign} / {chart.moon_nakshatra} (P{chart.moon_pada})    Sun: {chart.sun_sign}

Planetary placements (sidereal Lahiri):
{_planets_block(chart.planets)}

Detected yogas:
{yoga_lines}
"""


def build_dasha_context(chart: Chart, on_date: Optional[date_cls] = None) -> str:
    """Render current dasha + antardasha as text."""
    from datetime import datetime, timezone as _tz
    now = (
        datetime.combine(on_date, datetime.min.time()).replace(tzinfo=_tz.utc)
        if on_date else None
    )
    cur = current_dasha(chart, now=now)
    md = cur.get("mahadasha")
    ad = cur.get("antardasha")
    if not md:
        return "--- CURRENT DASHA --- (none active)"
    line = f"Mahadasha: {md['lord']} ({md['start'][:10]} → {md['end'][:10]})"
    if ad:
        line += f"\nAntardasha: {ad['lord']} ({ad['start'][:10]} → {ad['end'][:10]})"
    return f"--- CURRENT DASHA ---\n{line}\n"


def build_life_story_context(life_story: LifeStory) -> str:
    """Render the past/present/future chapter spine."""
    parts = [f"--- LIFE STORY ---", f"Today: {life_story.today}"]
    parts.append(f"Chart signature: {life_story.overall_signature_en}")

    if life_story.past:
        parts.append("\nPast Mahadashas (already lived):")
        for c in life_story.past:
            parts.append(
                f"- {c.lord} {c.start[:7]} → {c.end[:7]} (age {c.start_age:.1f}–{c.end_age:.1f}): "
                f"H{c.house} {c.sign} {c.dignity}; "
                f"themes: {', '.join(c.themes_en[:3])}"
            )

    if life_story.current:
        c = life_story.current
        parts.append(
            f"\nCurrent Mahadasha (NOW): {c.lord} {c.start[:7]} → {c.end[:7]} "
            f"(age {c.start_age:.1f}–{c.end_age:.1f}): "
            f"H{c.house} {c.sign} {c.dignity}; themes: {', '.join(c.themes_en[:4])}"
        )
        parts.append(f"  Reading: {c.summary_en}")
        if c.timing_notes_en:
            parts.append("  Sub-period turning points:")
            for t in c.timing_notes_en[:9]:
                parts.append(f"    • {t}")

    if life_story.future:
        parts.append("\nFuture Mahadashas (upcoming):")
        for c in life_story.future:
            parts.append(
                f"- {c.lord} {c.start[:7]} → {c.end[:7]} (age {c.start_age:.1f}–{c.end_age:.1f}): "
                f"H{c.house} {c.sign} {c.dignity}; "
                f"themes: {', '.join(c.themes_en[:3])}"
            )

    # Remedies block — current first, then a brief future preview
    if life_story.current:
        r = life_story.current.remedies_en
        parts.append(
            f"\n--- REMEDIES (current period) ---\n"
            f"Gemstone: {r['gemstone']}; Metal: {r['metal']}; "
            f"Mantra: {r['mantra']}; Charity: {r['charity']}; "
            f"Fast: {r['fast']}; Deity: {r['deity']}"
        )

    return "\n".join(parts)


def build_panchang_context(panchang: Panchang) -> str:
    return f"""--- TODAY'S PANCHANG ({panchang.date}) ---
Tithi: {panchang.tithi_name} ({panchang.paksha})    Vara: {panchang.weekday} ({panchang.weekday_lord})
Nakshatra: {panchang.nakshatra}    Yoga: {panchang.yoga}    Karana: {panchang.karana}
"""


def build_sade_sati_context(chart: Chart, on_date: Optional[date_cls] = None) -> str:
    """Render Saturn-vs-Moon transit phase (Sade Sati / Dhaiya) as text."""
    s = compute_sade_sati(chart, on_date=on_date)
    if not (s.in_sade_sati or s.in_dhaiya):
        return (
            f"--- SATURN TRANSIT ---\n"
            f"Saturn currently in {s.saturn_sign} (H{s.relative_house} from natal Moon "
            f"{s.moon_sign}) — NOT in Sade Sati or Dhaiya. Neutral/positive transit.\n"
        )
    period = ""
    if s.started_on or s.ends_on:
        period = f"  Started: {s.started_on or '?'}    Ends: {s.ends_on or '?'}\n"
    return (
        f"--- SATURN TRANSIT (active) ---\n"
        f"{s.phase_label_en} — Saturn in {s.saturn_sign}, "
        f"H{s.relative_house} from natal Moon ({s.moon_sign}).\n"
        f"{period}"
        f"  Classical reading: {s.description_en}\n"
    )


def build_full_context(
    chart: Chart,
    life_story: Optional[LifeStory] = None,
    panchang: Optional[Panchang] = None,
    on_date: Optional[date_cls] = None,
) -> str:
    """The whole spine — chart + dasha + life story + panchang + Saturn transit."""
    pieces = [build_chart_context(chart), build_dasha_context(chart, on_date=on_date)]
    if life_story:
        pieces.append(build_life_story_context(life_story))
    pieces.append(build_sade_sati_context(chart, on_date=on_date))
    if panchang:
        pieces.append(build_panchang_context(panchang))
    return "\n\n".join(pieces)


def make_system_prompt(context: str, locale: str = "en") -> str:
    """Combine the system prompt with the chart context."""
    base = SYSTEM_PROMPT_HI if locale == "hi" else SYSTEM_PROMPT_EN
    return f"{base}\n\n=== CHART CONTEXT (treat as ground truth) ===\n{context}\n=== END CONTEXT ==="
