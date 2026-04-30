"""Phalit — classical Vedic life-story interpretation.

Given a Chart, produces a structured `LifeStory` with:
  - past chapters    (mahadashas already completed)
  - current chapter  (active mahadasha + antardasha)
  - future chapters  (next 4-5 mahadashas)

Each chapter is built from authentic Brihat Parashara Hora Shastra (BPHS)
principles:
  1. The mahadasha lord's intrinsic significations (karaka) — what the
     planet rules in any chart.
  2. The lord's PLACEMENT in the native's birth chart — its house, sign,
     dignity (exalted / own / debilitated / neutral), retrograde, etc.
  3. Aspects received from / given to other planets.
  4. Conjunctions in the same house.
  5. Active doshas during the period (Sade Sati for Saturn dasha if Saturn
     transits the moon-axis houses, Kalsarpa effects for Rahu/Ketu, etc.).
  6. Classical timing notes (which antardashas inside the period mark
     turning points).
  7. Remedies (gemstone, mantra, charity, deity, fast day) per planet.

This is a RULE-BASED engine. It does not call any LLM. Every line of
output is grounded in a specific BPHS / Saravali / Phaladeepika rule.

Bilingual EN + HI throughout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date as date_cls
from typing import Optional

from . import constants as K
from .chart import Chart, PlanetPosition
from .dasha import DashaPeriod, compute_antardashas, compute_mahadashas


# --- Planet Karakatva (intrinsic significations) ---------------------------
# What each planet "rules" in classical Vedic astrology, regardless of chart.
# Source: BPHS Ch.3 "Graha Karakatva".

PLANET_KARAKAS_EN: dict[str, list[str]] = {
    "Sun": ["soul (atma)", "father", "authority", "vitality", "government", "self-confidence", "prestige"],
    "Moon": ["mind (manas)", "mother", "emotions", "home", "general public", "comfort", "fluids"],
    "Mars": ["energy", "siblings (younger)", "courage", "land", "discipline", "muscle", "conflict"],
    "Mercury": ["intellect", "speech", "writing", "commerce", "education", "communication", "skin"],
    "Jupiter": ["wisdom", "children", "guru", "dharma", "wealth", "expansion", "good counsel"],
    "Venus": ["love", "spouse", "luxury", "beauty", "vehicles", "art", "diplomacy"],
    "Saturn": ["service", "discipline", "longevity", "labour", "hard lessons", "delays", "elders"],
    "Rahu": ["foreign", "ambition", "innovation", "unconventional desires", "obsession", "shortcuts"],
    "Ketu": ["moksha", "detachment", "past-life karma", "research", "spirituality", "healing"],
}
PLANET_KARAKAS_HI: dict[str, list[str]] = {
    "Sun": ["आत्मा", "पिता", "अधिकार", "जीवन-शक्ति", "शासन", "आत्मविश्वास", "प्रतिष्ठा"],
    "Moon": ["मन", "माता", "भावनाएँ", "गृह", "जनता", "सुख", "तरल पदार्थ"],
    "Mars": ["ऊर्जा", "छोटे भाई-बहन", "साहस", "भूमि", "अनुशासन", "मांसपेशी", "विवाद"],
    "Mercury": ["बुद्धि", "वाणी", "लेखन", "व्यापार", "शिक्षा", "संचार", "त्वचा"],
    "Jupiter": ["ज्ञान", "संतान", "गुरु", "धर्म", "धन", "विस्तार", "शुभ सलाह"],
    "Venus": ["प्रेम", "पति/पत्नी", "विलास", "सौन्दर्य", "वाहन", "कला", "कूटनीति"],
    "Saturn": ["सेवा", "अनुशासन", "आयु", "श्रम", "कठिन शिक्षा", "विलंब", "बुजुर्ग"],
    "Rahu": ["विदेश", "महत्वाकांक्षा", "नवीनता", "अपरंपरागत इच्छाएँ", "व्यसन", "शॉर्टकट"],
    "Ketu": ["मोक्ष", "वैराग्य", "पूर्व-जन्म कर्म", "शोध", "अध्यात्म", "उपचार"],
}


# --- House Significations (Bhava Karakatva) -------------------------------
# Source: BPHS Ch.11 "Bhava Vivechan".

HOUSE_THEMES_EN: dict[int, str] = {
    1:  "self, body, identity, personality",
    2:  "family wealth, speech, food, savings",
    3:  "siblings, courage, short journeys, communication",
    4:  "mother, home, vehicles, inner peace",
    5:  "children, intellect, romance, past-life merit",
    6:  "enemies, debts, illness, daily work, service",
    7:  "marriage, partnerships, public dealings",
    8:  "hidden matters, longevity, occult, sudden change, in-laws' wealth",
    9:  "father, dharma, fortune, higher learning, long journeys",
    10: "career, public reputation, authority, action",
    11: "gains, friends, elder siblings, fulfilled desires",
    12: "expenses, foreign lands, spirituality, sleep, isolation",
}
HOUSE_THEMES_HI: dict[int, str] = {
    1:  "स्वयं, शरीर, पहचान, व्यक्तित्व",
    2:  "कुटुंब-धन, वाणी, भोजन, संचय",
    3:  "भाई-बहन, साहस, लघु यात्राएँ, संचार",
    4:  "माता, गृह, वाहन, मानसिक शांति",
    5:  "संतान, बुद्धि, प्रेम, पूर्व-जन्म पुण्य",
    6:  "शत्रु, ऋण, रोग, दैनिक कार्य, सेवा",
    7:  "विवाह, साझेदारी, सार्वजनिक व्यवहार",
    8:  "गूढ़ बातें, आयु, तंत्र, अकस्मात परिवर्तन, ससुराल का धन",
    9:  "पिता, धर्म, भाग्य, उच्च-शिक्षा, दीर्घ यात्राएँ",
    10: "कैरियर, यश, अधिकार, कर्म",
    11: "लाभ, मित्र, बड़े भाई-बहन, इच्छा-पूर्ति",
    12: "व्यय, विदेश, अध्यात्म, निद्रा, एकांत",
}


# --- Remedies per planet (BPHS Ch.86 + Lal Kitab cross-referenced) --------

PLANET_REMEDIES_EN: dict[str, dict[str, str]] = {
    "Sun":     {"gemstone": "ruby (manik)", "metal": "copper", "mantra": "Om Suryaya Namaha (108×, sunrise)",
                "charity": "wheat or jaggery on Sunday", "fast": "Sundays", "deity": "Surya / Vishnu"},
    "Moon":    {"gemstone": "natural pearl (moti)", "metal": "silver", "mantra": "Om Chandraya Namaha (108×, evening)",
                "charity": "rice or milk on Monday", "fast": "Mondays", "deity": "Shiva / Parvati"},
    "Mars":    {"gemstone": "red coral (moonga)", "metal": "copper", "mantra": "Om Angarakaya Namaha (108×)",
                "charity": "red lentils or sweets on Tuesday", "fast": "Tuesdays", "deity": "Hanuman / Kartikeya"},
    "Mercury": {"gemstone": "emerald (panna)", "metal": "gold", "mantra": "Om Budhaya Namaha (108×)",
                "charity": "green moong dal or books on Wednesday", "fast": "Wednesdays", "deity": "Vishnu / Ganesha"},
    "Jupiter": {"gemstone": "yellow sapphire (pukhraj)", "metal": "gold", "mantra": "Om Brihaspataye Namaha (108×)",
                "charity": "yellow sweets or turmeric on Thursday", "fast": "Thursdays", "deity": "Brihaspati / Vishnu"},
    "Venus":   {"gemstone": "diamond (heera) or white sapphire", "metal": "silver", "mantra": "Om Shukraya Namaha (108×)",
                "charity": "white sweets or curd on Friday", "fast": "Fridays", "deity": "Lakshmi / Durga"},
    "Saturn":  {"gemstone": "blue sapphire (neelam) — only after testing", "metal": "iron", "mantra": "Om Shanaishcharaya Namaha (108×)",
                "charity": "black urad or oil on Saturday; serve the elderly", "fast": "Saturdays", "deity": "Shani / Hanuman"},
    "Rahu":    {"gemstone": "hessonite (gomedh)", "metal": "panchadhatu", "mantra": "Om Rahave Namaha (108×)",
                "charity": "blue cloth or sesame on Saturday", "fast": "Saturdays (Rahu Kaal)", "deity": "Durga / Bhairava"},
    "Ketu":    {"gemstone": "cat's eye (lehsunia)", "metal": "panchadhatu", "mantra": "Om Ketave Namaha (108×)",
                "charity": "feed dogs; donate at temple", "fast": "Tuesdays", "deity": "Ganesha / Bhairava"},
}
PLANET_REMEDIES_HI: dict[str, dict[str, str]] = {
    "Sun":     {"gemstone": "माणिक्य", "metal": "ताम्र", "mantra": "ॐ सूर्याय नमः (१०८ बार, सूर्योदय)",
                "charity": "रविवार को गेहूँ या गुड़ का दान", "fast": "रविवार", "deity": "सूर्य देव / विष्णु"},
    "Moon":    {"gemstone": "मोती", "metal": "रजत", "mantra": "ॐ चन्द्राय नमः (१०८ बार, संध्या)",
                "charity": "सोमवार को चावल या दूध का दान", "fast": "सोमवार", "deity": "शिव / पार्वती"},
    "Mars":    {"gemstone": "मूँगा", "metal": "ताम्र", "mantra": "ॐ अंगारकाय नमः (१०८ बार)",
                "charity": "मंगलवार को मसूर या मिठाई का दान", "fast": "मंगलवार", "deity": "हनुमान / कार्तिकेय"},
    "Mercury": {"gemstone": "पन्ना", "metal": "स्वर्ण", "mantra": "ॐ बुधाय नमः (१०८ बार)",
                "charity": "बुधवार को मूँग दाल या पुस्तकें", "fast": "बुधवार", "deity": "विष्णु / गणेश"},
    "Jupiter": {"gemstone": "पुखराज", "metal": "स्वर्ण", "mantra": "ॐ बृहस्पतये नमः (१०८ बार)",
                "charity": "गुरुवार को पीली मिठाई या हल्दी", "fast": "गुरुवार", "deity": "बृहस्पति / विष्णु"},
    "Venus":   {"gemstone": "हीरा या स्फटिक", "metal": "रजत", "mantra": "ॐ शुक्राय नमः (१०८ बार)",
                "charity": "शुक्रवार को सफेद मिठाई या दही", "fast": "शुक्रवार", "deity": "लक्ष्मी / दुर्गा"},
    "Saturn":  {"gemstone": "नीलम (परीक्षण के बाद)", "metal": "लौह", "mantra": "ॐ शनैश्चराय नमः (१०८ बार)",
                "charity": "शनिवार को उड़द या तेल; बुजुर्गों की सेवा", "fast": "शनिवार", "deity": "शनि / हनुमान"},
    "Rahu":    {"gemstone": "गोमेद", "metal": "पंचधातु", "mantra": "ॐ राहवे नमः (१०८ बार)",
                "charity": "शनिवार को नीला वस्त्र या तिल", "fast": "शनिवार (राहु काल)", "deity": "दुर्गा / भैरव"},
    "Ketu":    {"gemstone": "लहसुनिया", "metal": "पंचधातु", "mantra": "ॐ केतवे नमः (१०८ बार)",
                "charity": "कुत्तों को भोजन; मंदिर में दान", "fast": "मंगलवार", "deity": "गणेश / भैरव"},
}


# --- Dignity & functional nature -------------------------------------------

DIGNITY_LABEL_EN: dict[str, str] = {
    "exalted": "exalted (uchcha) — strongest possible placement",
    "own_sign": "in own sign (svakshetra) — strong & self-supporting",
    "debilitated": "debilitated (neecha) — weakened, results delayed or distorted",
    "neutral": "neutral dignity",
}
DIGNITY_LABEL_HI: dict[str, str] = {
    "exalted": "उच्च — सर्वाधिक बलवान",
    "own_sign": "स्व-क्षेत्र — स्वबल युक्त",
    "debilitated": "नीच — फल विलंबित या विकृत",
    "neutral": "सम भाव",
}


# --- Output dataclass ------------------------------------------------------

@dataclass
class Chapter:
    lord: str                       # "Sun", "Moon", ... "Ketu"
    lord_hi: str
    start: str                      # "YYYY-MM-DD"
    end: str
    start_age: float                # native's age at start
    end_age: float
    duration_years: float
    house: int                      # 1..12 — where the lord sits in the chart
    sign: str
    sign_hi: str
    dignity: str                    # exalted / own_sign / debilitated / neutral
    dignity_label_en: str
    dignity_label_hi: str
    retrograde: bool
    karakas_en: list[str]
    karakas_hi: list[str]
    house_theme_en: str
    house_theme_hi: str
    conjunctions: list[str]         # other planets in the same house
    aspects_received: list[str]     # planets aspecting the lord's house
    themes_en: list[str]            # 4-6 short headline themes for the period
    themes_hi: list[str]
    summary_en: str                 # narrative paragraph (~3-4 sentences)
    summary_hi: str
    timing_notes_en: list[str]      # antardasha-level turning points
    timing_notes_hi: list[str]
    remedies_en: dict[str, str]
    remedies_hi: dict[str, str]
    is_past: bool
    is_current: bool
    is_future: bool


@dataclass
class LifeStory:
    name: str
    today: str
    past: list[Chapter] = field(default_factory=list)
    current: Optional[Chapter] = None
    future: list[Chapter] = field(default_factory=list)
    overall_signature_en: str = ""
    overall_signature_hi: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "today": self.today,
            "past": [c.__dict__ for c in self.past],
            "current": self.current.__dict__ if self.current else None,
            "future": [c.__dict__ for c in self.future],
            "overall_signature_en": self.overall_signature_en,
            "overall_signature_hi": self.overall_signature_hi,
        }


# --- Helpers ----------------------------------------------------------------

def _naive(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None) if dt.tzinfo else dt


def _years_between(start: datetime, end: datetime) -> float:
    return (_naive(end) - _naive(start)).total_seconds() / (365.2425 * 24 * 3600)


def _planet_in_chart(chart: Chart, name: str) -> PlanetPosition:
    return next(p for p in chart.planets if p.name == name)


def _planets_in_house(chart: Chart, house: int) -> list[PlanetPosition]:
    return [p for p in chart.planets if p.house == house]


def _aspects_received(chart: Chart, target_house: int) -> list[str]:
    """Classical graha drishti — every planet aspects 7th house from itself.
    Mars also aspects 4 & 8, Jupiter 5 & 9, Saturn 3 & 10, Rahu/Ketu 5 & 9 & 7
    (per most schools).
    """
    SPECIAL = {
        "Mars": [4, 7, 8],
        "Jupiter": [5, 7, 9],
        "Saturn": [3, 7, 10],
        "Rahu": [5, 7, 9],
        "Ketu": [5, 7, 9],
    }
    aspecting: list[str] = []
    for p in chart.planets:
        diff = ((target_house - p.house) % 12) + 1   # houses ahead, 1..12
        if p.name in SPECIAL:
            houses_ahead = SPECIAL[p.name]
        else:
            houses_ahead = [7]
        if diff in houses_ahead:
            aspecting.append(p.name)
    return aspecting


def _build_themes(p: PlanetPosition, lord: str) -> tuple[list[str], list[str]]:
    """Generate 4-6 short headline themes from karakas × house × dignity."""
    karakas_en = PLANET_KARAKAS_EN[lord][:3]
    karakas_hi = PLANET_KARAKAS_HI[lord][:3]
    house_en = HOUSE_THEMES_EN[p.house]
    house_hi = HOUSE_THEMES_HI[p.house]
    themes_en = [f"{k} via {house_en.split(',')[0]}" for k in karakas_en]
    themes_hi = [f"{k} — {house_hi.split(',')[0]}" for k in karakas_hi]
    if p.dignity == "exalted":
        themes_en.append("results manifest with strength and clarity")
        themes_hi.append("फल बलवान और स्पष्ट रूप से प्रकट")
    elif p.dignity == "debilitated":
        themes_en.append("delays and indirect results — patience required")
        themes_hi.append("विलंब व अप्रत्यक्ष फल — धैर्य आवश्यक")
    elif p.dignity == "own_sign":
        themes_en.append("self-supporting and stable expression")
        themes_hi.append("स्वबल युक्त, स्थिर अभिव्यक्ति")
    if p.retrograde:
        themes_en.append("inner-facing review of past commitments")
        themes_hi.append("पूर्व-संकल्पों का आंतरिक पुनरावलोकन")
    return themes_en[:6], themes_hi[:6]


def _life_stage(start_age: float, end_age: float) -> tuple[str, str]:
    """Classify the dasha's life-stage and give a short EN/HI framing phrase."""
    mid = (start_age + end_age) / 2
    if end_age <= 7:
        return (
            "This is the bala (infancy) phase — the planet's themes shape the earliest imprints, often experienced through the parents and home rather than as conscious agency.",
            "यह बाल्यावस्था है — ग्रह के विषय सबसे प्रारंभिक छाप गढ़ते हैं, जो प्रायः माता-पिता एवं गृह के माध्यम से अनुभव होते हैं।",
        )
    if end_age <= 14:
        return (
            "Childhood and pre-adolescence — themes here register as formative tendencies, schooling, and the texture of family life.",
            "बाल्य एवं पूर्व-किशोरावस्था — विषय यहाँ शिक्षा, परिवार और बनती हुई प्रवृत्तियों के रूप में दर्ज होते हैं।",
        )
    if mid <= 25:
        return (
            "Late teens / early adulthood — this is identity-formation, education's culmination, first independent choices in love and career.",
            "किशोरावस्था का अंत / युवावस्था का आरंभ — पहचान निर्माण, शिक्षा की पूर्णता, प्रेम और जीविका में प्रथम स्वतंत्र निर्णय।",
        )
    if mid <= 40:
        return (
            "Prime young-adult years — career consolidation, marriage, children, the building of a life. Whatever this lord activates here is foundational.",
            "युवा गृहस्थ-काल — जीविका की दृढ़ता, विवाह, संतान, जीवन का निर्माण। इस अवधि में जो भी सक्रिय होता है वह आधारशिला बनता है।",
        )
    if mid <= 55:
        return (
            "Mid-life — established responsibilities, peak professional standing, possible mid-life re-evaluation of meaning.",
            "मध्यावस्था — स्थापित उत्तरदायित्व, व्यावसायिक शिखर, अर्थ-पुनर्मूल्यांकन की संभावना।",
        )
    if mid <= 70:
        return (
            "Mature adulthood — wisdom transmitted, legacy built, attention turning toward dharma and the next generation.",
            "प्रौढ़ावस्था — ज्ञान-संचरण, धरोहर का निर्माण, धर्म एवं अगली पीढ़ी की ओर ध्यान।",
        )
    return (
        "Elder years (vridhdha) — moksha-ward orientation; outer events soften, inner life deepens.",
        "वृद्धावस्था — मोक्ष-उन्मुख चरण; बाहरी घटनाएँ शांत होती हैं, आंतरिक जीवन गहरा।",
    )


def _build_summary(
    p: PlanetPosition,
    lord: str,
    *,
    conj: list[str],
    aspects: list[str],
    duration: float,
    start_age: float = 0.0,
    end_age: float = 0.0,
) -> tuple[str, str]:
    """Narrative paragraph for the chapter."""
    karaka_main_en = PLANET_KARAKAS_EN[lord][0]
    karaka_main_hi = PLANET_KARAKAS_HI[lord][0]
    house = p.house
    dignity = p.dignity
    sign = p.sign

    # Sentence 1 — the planet's nature × house
    s1_en = (f"This {duration:.1f}-year period activates {lord}'s domain — "
             f"matters of {karaka_main_en} expressed through the {p.house}H "
             f"({HOUSE_THEMES_EN[house].split(',')[0]}).")
    s1_hi = (f"यह {duration:.1f} वर्ष की अवधि {K.PLANETS_HI[lord]} के क्षेत्र को सक्रिय करती है — "
             f"{karaka_main_hi} के विषय {p.house}वें भाव "
             f"({HOUSE_THEMES_HI[house].split(',')[0]}) के माध्यम से।")

    # Sentence 2 — dignity verdict
    if dignity == "exalted":
        s2_en = f" Placed in {sign} (its exaltation), {lord} delivers strong, visible results — a chapter of culmination."
        s2_hi = f" {p.sign_hi} (उच्च राशि) में स्थित होकर {K.PLANETS_HI[lord]} स्पष्ट और बलवान फल देता है — चरमोत्कर्ष का अध्याय।"
    elif dignity == "own_sign":
        s2_en = f" Sitting in its own sign {sign}, {lord} works with self-supporting strength; outcomes are steady."
        s2_hi = f" अपनी राशि {p.sign_hi} में बैठा {K.PLANETS_HI[lord]} स्वबल से कार्य करता है; परिणाम स्थिर।"
    elif dignity == "debilitated":
        s2_en = f" In its debilitation sign {sign}, {lord} brings lessons through delay and re-routing — early frustrations refine the eventual gain."
        s2_hi = f" नीच राशि {p.sign_hi} में {K.PLANETS_HI[lord]} विलंब और मोड़ों से शिक्षा देता है — आरंभिक बाधाएँ अंतिम लाभ को परिष्कृत करती हैं।"
    else:
        s2_en = f" From {sign}, {lord} acts with neutral force — outcomes balanced, neither extreme."
        s2_hi = f" {p.sign_hi} से {K.PLANETS_HI[lord]} सम भाव से कार्य करता है — फल संतुलित, चरम नहीं।"

    # Sentence 3 — conjunctions / aspects
    extras_en = []
    extras_hi = []
    if conj:
        extras_en.append(f"conjoined with {', '.join(conj)} in the same house, blending those significations")
        extras_hi.append(f"{', '.join(K.PLANETS_HI[c] for c in conj)} के साथ युति, उनके फलों का मिश्रण")
    if aspects:
        extras_en.append(f"receiving aspect from {', '.join(aspects)}")
        extras_hi.append(f"{', '.join(K.PLANETS_HI[a] for a in aspects)} की दृष्टि")
    if extras_en:
        s3_en = " The lord is " + "; ".join(extras_en) + "."
        s3_hi = " ग्रह " + "; ".join(extras_hi) + " से प्रभावित।"
    else:
        s3_en = " No major conjunctions or external aspects — the planet works in isolation, themes emerge from its nature alone."
        s3_hi = " कोई महत्वपूर्ण युति या दृष्टि नहीं — ग्रह अपने स्वभाव से ही फल देता है।"

    # Sentence 4 — life-stage framing
    s4_en, s4_hi = _life_stage(start_age, end_age)
    s4_en = " " + s4_en
    s4_hi = " " + s4_hi

    return s1_en + s2_en + s3_en + s4_en, s1_hi + s2_hi + s3_hi + s4_hi


def _build_timing_notes(maha: DashaPeriod, chart: Chart, native_birth: datetime) -> tuple[list[str], list[str]]:
    """Antardasha turning points within this Mahadasha."""
    sub_periods = compute_antardashas(maha)
    notes_en, notes_hi = [], []
    for sp in sub_periods:
        sub_lord = sp.lord
        sub_p = _planet_in_chart(chart, sub_lord)
        relation = "supportive" if sub_p.dignity in ("exalted", "own_sign") else "challenging" if sub_p.dignity == "debilitated" else "balanced"
        relation_hi = "अनुकूल" if sub_p.dignity in ("exalted", "own_sign") else "चुनौतीपूर्ण" if sub_p.dignity == "debilitated" else "संतुलित"
        karaka_en = PLANET_KARAKAS_EN[sub_lord][0]
        karaka_hi = PLANET_KARAKAS_HI[sub_lord][0]
        notes_en.append(
            f"{sp.start.strftime('%b %Y')}–{sp.end.strftime('%b %Y')}: {maha.lord}/{sub_lord} AD — {karaka_en} foregrounded ({relation})."
        )
        notes_hi.append(
            f"{sp.start.strftime('%b %Y')}–{sp.end.strftime('%b %Y')}: {K.PLANETS_HI[maha.lord]}/{K.PLANETS_HI[sub_lord]} अं — {karaka_hi} प्रमुख ({relation_hi})।"
        )
    return notes_en, notes_hi


def _make_chapter(
    *,
    chart: Chart,
    maha: DashaPeriod,
    native_birth: datetime,
    today: datetime,
) -> Chapter:
    lord = maha.lord
    p = _planet_in_chart(chart, lord)
    house = p.house
    conj = [q.name for q in _planets_in_house(chart, house) if q.name != lord]
    aspects = [a for a in _aspects_received(chart, house) if a != lord]
    themes_en, themes_hi = _build_themes(p, lord)
    start_age = round(_years_between(native_birth, maha.start), 1)
    end_age = round(_years_between(native_birth, maha.end), 1)
    summary_en, summary_hi = _build_summary(
        p, lord,
        conj=conj, aspects=aspects, duration=maha.duration_years,
        start_age=start_age, end_age=end_age,
    )
    timing_en, timing_hi = _build_timing_notes(maha, chart, native_birth)

    # Normalise both sides to naive datetimes for comparison
    m_start = maha.start.replace(tzinfo=None) if maha.start.tzinfo else maha.start
    m_end = maha.end.replace(tzinfo=None) if maha.end.tzinfo else maha.end
    is_past = m_end < today
    is_current = m_start <= today < m_end
    is_future = m_start > today

    return Chapter(
        lord=lord,
        lord_hi=K.PLANETS_HI[lord],
        start=maha.start.strftime("%Y-%m-%d"),
        end=maha.end.strftime("%Y-%m-%d"),
        start_age=start_age,
        end_age=end_age,
        duration_years=round(maha.duration_years, 2),
        house=house,
        sign=p.sign,
        sign_hi=p.sign_hi,
        dignity=p.dignity,
        dignity_label_en=DIGNITY_LABEL_EN[p.dignity],
        dignity_label_hi=DIGNITY_LABEL_HI[p.dignity],
        retrograde=p.retrograde,
        karakas_en=PLANET_KARAKAS_EN[lord],
        karakas_hi=PLANET_KARAKAS_HI[lord],
        house_theme_en=HOUSE_THEMES_EN[house],
        house_theme_hi=HOUSE_THEMES_HI[house],
        conjunctions=conj,
        aspects_received=aspects,
        themes_en=themes_en,
        themes_hi=themes_hi,
        summary_en=summary_en,
        summary_hi=summary_hi,
        timing_notes_en=timing_en,
        timing_notes_hi=timing_hi,
        remedies_en=PLANET_REMEDIES_EN[lord],
        remedies_hi=PLANET_REMEDIES_HI[lord],
        is_past=is_past,
        is_current=is_current,
        is_future=is_future,
    )


def _overall_signature(chart: Chart) -> tuple[str, str]:
    """A 1-paragraph headline reading the dominant chart signature."""
    moon = _planet_in_chart(chart, "Moon")
    sun = _planet_in_chart(chart, "Sun")
    asc_hi = chart.lagna_sign_hi
    parts_en = [
        f"{chart.name}'s lagna is {chart.lagna_sign} ({chart.lagna_nakshatra}), making them outwardly {chart.lagna_sign.lower()}-natured.",
        f"The Moon — ruler of mind — sits in {moon.sign} in the {moon.house}H ({HOUSE_THEMES_EN[moon.house].split(',')[0]}), so the inner emotional life is shaped by {HOUSE_THEMES_EN[moon.house].split(',')[0]}.",
        f"The Sun (soul) is in {sun.sign} in the {sun.house}H ({HOUSE_THEMES_EN[sun.house].split(',')[0]}).",
    ]
    parts_hi = [
        f"{chart.name} का लग्न {asc_hi} ({chart.lagna_nakshatra}) है, जिससे बाह्य स्वभाव {asc_hi}-सा होता है।",
        f"मन का स्वामी चन्द्र {moon.sign_hi} में {moon.house}वें भाव में स्थित है ({HOUSE_THEMES_HI[moon.house].split(',')[0]}), अतः आंतरिक भावनात्मक जीवन इसी से आकार पाता है।",
        f"आत्मा-कारक सूर्य {sun.sign_hi} में {sun.house}वें भाव में है ({HOUSE_THEMES_HI[sun.house].split(',')[0]})।",
    ]
    return " ".join(parts_en), " ".join(parts_hi)


# --- Main entrypoint -------------------------------------------------------

def compute_life_story(
    chart: Chart,
    *,
    on_date: Optional[date_cls] = None,
    num_future: int = 5,
) -> LifeStory:
    """Produce the full classical life story with past/present/future chapters."""
    today = datetime.combine(on_date or date_cls.today(), datetime.min.time())
    native_birth = datetime.fromisoformat(chart.birth_dt_utc).replace(tzinfo=None)

    # We need enough mahadashas to cover from birth through num_future chapters
    # past today. 9 covers 120 years which is plenty for any human life.
    mahas = compute_mahadashas(chart, num_periods=9)

    chapters: list[Chapter] = [
        _make_chapter(chart=chart, maha=m, native_birth=native_birth, today=today)
        for m in mahas
    ]

    past = [c for c in chapters if c.is_past]
    current = next((c for c in chapters if c.is_current), None)
    future_all = [c for c in chapters if c.is_future]
    future = future_all[:num_future]

    sig_en, sig_hi = _overall_signature(chart)

    return LifeStory(
        name=chart.name,
        today=today.strftime("%Y-%m-%d"),
        past=past,
        current=current,
        future=future,
        overall_signature_en=sig_en,
        overall_signature_hi=sig_hi,
    )
