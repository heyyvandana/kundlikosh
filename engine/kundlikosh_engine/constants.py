"""Vedic astrology constants — signs, planets, nakshatras, deities.

All Sanskrit names are romanized + Devanagari for the bilingual UI.
"""

from __future__ import annotations

SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGNS_SA = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena",
]

SIGNS_HI = [
    "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन",
]

SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]

PLANETS_EN = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
]

PLANETS_HI = {
    "Sun": "सूर्य",
    "Moon": "चन्द्र",
    "Mars": "मंगल",
    "Mercury": "बुध",
    "Jupiter": "गुरु",
    "Venus": "शुक्र",
    "Saturn": "शनि",
    "Rahu": "राहु",
    "Ketu": "केतु",
}

PLANET_DEITIES = {
    "Sun": {"deity": "Surya", "deity_hi": "सूर्य देव", "consort": "Sangya",
            "vahana": "Saptashva (seven-horse chariot)",
            "mantra": "ॐ सूर्याय नमः",
            "story_seed": "Surya, the radiant son of Aditi and Kashyapa, drives his seven-horse chariot across the heavens."},
    "Moon": {"deity": "Chandra", "deity_hi": "चन्द्र देव", "consort": "Rohini (and 26 other nakshatra wives)",
             "vahana": "Antelope/Deer chariot",
             "mantra": "ॐ चन्द्राय नमः",
             "story_seed": "Chandra was cursed by Daksha to wax and wane, after favouring Rohini above his other wives."},
    "Mars": {"deity": "Mangal / Skanda", "deity_hi": "मंगल देव",
             "vahana": "Ram",
             "mantra": "ॐ अं अंगारकाय नमः",
             "story_seed": "Mangal, born of Earth, is the warrior-protector who blesses courage and victory."},
    "Mercury": {"deity": "Budha", "deity_hi": "बुध देव",
                "vahana": "Lion-drawn chariot",
                "mantra": "ॐ बुं बुधाय नमः",
                "story_seed": "Budha, son of Chandra and Tara, embodies sharp intellect and articulate speech."},
    "Jupiter": {"deity": "Brihaspati", "deity_hi": "बृहस्पति",
                "vahana": "Elephant",
                "mantra": "ॐ बृं बृहस्पतये नमः",
                "story_seed": "Brihaspati is the guru of the gods, master of wisdom, prayer, and dharma."},
    "Venus": {"deity": "Shukra", "deity_hi": "शुक्र देव",
              "vahana": "Crocodile / Horse",
              "mantra": "ॐ शुं शुक्राय नमः",
              "story_seed": "Shukra is the guru of the asuras, master of love, beauty, and the sanjeevani vidya."},
    "Saturn": {"deity": "Shani", "deity_hi": "शनि देव",
               "vahana": "Crow / Buffalo",
               "mantra": "ॐ शं शनैश्चराय नमः",
               "story_seed": "Shani, son of Surya and Chhaya, is the strict but just judge who awards the fruits of karma."},
    "Rahu": {"deity": "Rahu (Svarbhanu)", "deity_hi": "राहु",
             "vahana": "Lion / Eight black horses",
             "mantra": "ॐ रां राहवे नमः",
             "story_seed": "The severed head of the asura Svarbhanu, who tasted amrit and was beheaded by Vishnu's Sudarshana."},
    "Ketu": {"deity": "Ketu", "deity_hi": "केतु",
             "vahana": "Vulture / Fish",
             "mantra": "ॐ कें केतवे नमः",
             "story_seed": "The headless body of Svarbhanu — Ketu represents moksha, detachment, and past-life karma."},
}

NAKSHATRAS = [
    {"name": "Ashwini",          "name_hi": "अश्विनी",        "lord": "Ketu",    "deity": "Ashwini Kumars",  "deity_hi": "अश्विनी कुमार",   "symbol": "Horse's head"},
    {"name": "Bharani",          "name_hi": "भरणी",          "lord": "Venus",   "deity": "Yama",            "deity_hi": "यम",              "symbol": "Yoni"},
    {"name": "Krittika",         "name_hi": "कृत्तिका",        "lord": "Sun",     "deity": "Agni",            "deity_hi": "अग्नि",            "symbol": "Razor / Flame"},
    {"name": "Rohini",           "name_hi": "रोहिणी",         "lord": "Moon",    "deity": "Brahma",          "deity_hi": "ब्रह्मा",           "symbol": "Ox-cart / Banyan"},
    {"name": "Mrigashira",       "name_hi": "मृगशिरा",        "lord": "Mars",    "deity": "Soma",            "deity_hi": "सोम",              "symbol": "Deer's head"},
    {"name": "Ardra",            "name_hi": "आर्द्रा",         "lord": "Rahu",    "deity": "Rudra",           "deity_hi": "रुद्र",             "symbol": "Teardrop / Diamond"},
    {"name": "Punarvasu",        "name_hi": "पुनर्वसु",        "lord": "Jupiter", "deity": "Aditi",           "deity_hi": "अदिति",            "symbol": "Quiver of arrows"},
    {"name": "Pushya",           "name_hi": "पुष्य",          "lord": "Saturn",  "deity": "Brihaspati",      "deity_hi": "बृहस्पति",          "symbol": "Cow's udder / Lotus"},
    {"name": "Ashlesha",         "name_hi": "आश्लेषा",        "lord": "Mercury", "deity": "Nagas",           "deity_hi": "नाग",              "symbol": "Coiled serpent"},
    {"name": "Magha",            "name_hi": "मघा",           "lord": "Ketu",    "deity": "Pitris (Ancestors)", "deity_hi": "पितृ",         "symbol": "Royal throne"},
    {"name": "Purva Phalguni",   "name_hi": "पूर्वा फाल्गुनी",  "lord": "Venus",   "deity": "Bhaga",           "deity_hi": "भग",              "symbol": "Front legs of a bed"},
    {"name": "Uttara Phalguni",  "name_hi": "उत्तरा फाल्गुनी", "lord": "Sun",     "deity": "Aryaman",         "deity_hi": "अर्यमा",           "symbol": "Back legs of a bed"},
    {"name": "Hasta",            "name_hi": "हस्त",          "lord": "Moon",    "deity": "Savitar",         "deity_hi": "सवित्र",           "symbol": "Open hand / Fist"},
    {"name": "Chitra",           "name_hi": "चित्रा",         "lord": "Mars",    "deity": "Vishvakarma",     "deity_hi": "विश्वकर्मा",        "symbol": "Bright jewel"},
    {"name": "Swati",            "name_hi": "स्वाति",         "lord": "Rahu",    "deity": "Vayu",            "deity_hi": "वायु",             "symbol": "Sword / Coral"},
    {"name": "Vishakha",         "name_hi": "विशाखा",        "lord": "Jupiter", "deity": "Indra-Agni",      "deity_hi": "इन्द्र-अग्नि",      "symbol": "Triumphal arch"},
    {"name": "Anuradha",         "name_hi": "अनुराधा",        "lord": "Saturn",  "deity": "Mitra",           "deity_hi": "मित्र",            "symbol": "Lotus / Staff"},
    {"name": "Jyeshtha",         "name_hi": "ज्येष्ठा",        "lord": "Mercury", "deity": "Indra",           "deity_hi": "इन्द्र",            "symbol": "Earring / Umbrella"},
    {"name": "Mula",             "name_hi": "मूल",           "lord": "Ketu",    "deity": "Nirriti",         "deity_hi": "निरृति",           "symbol": "Bunch of roots"},
    {"name": "Purva Ashadha",    "name_hi": "पूर्वाषाढा",      "lord": "Venus",   "deity": "Apas",            "deity_hi": "अप्",              "symbol": "Fan / Winnowing basket"},
    {"name": "Uttara Ashadha",   "name_hi": "उत्तराषाढा",     "lord": "Sun",     "deity": "Vishvedevas",     "deity_hi": "विश्वेदेवाः",       "symbol": "Elephant tusk"},
    {"name": "Shravana",         "name_hi": "श्रवण",          "lord": "Moon",    "deity": "Vishnu",          "deity_hi": "विष्णु",            "symbol": "Three footprints / Ear"},
    {"name": "Dhanishta",        "name_hi": "धनिष्ठा",        "lord": "Mars",    "deity": "Vasus",           "deity_hi": "अष्ट वसु",          "symbol": "Drum / Flute"},
    {"name": "Shatabhisha",      "name_hi": "शतभिषा",        "lord": "Rahu",    "deity": "Varuna",          "deity_hi": "वरुण",             "symbol": "Empty circle / 100 stars"},
    {"name": "Purva Bhadrapada", "name_hi": "पूर्व भाद्रपद",   "lord": "Jupiter", "deity": "Aja Ekapada",     "deity_hi": "अज एकपाद",        "symbol": "Front legs of funeral cot / Two-faced man"},
    {"name": "Uttara Bhadrapada","name_hi": "उत्तर भाद्रपद",  "lord": "Saturn",  "deity": "Ahir Budhnya",    "deity_hi": "अहिर्बुध्न्य",      "symbol": "Twin / Back of cot"},
    {"name": "Revati",           "name_hi": "रेवती",          "lord": "Mercury", "deity": "Pushan",          "deity_hi": "पूषन्",            "symbol": "Drum / Fish"},
]

# Vimshottari dasha periods (years)
DASHA_YEARS = {
    "Ketu":    7,
    "Venus":   20,
    "Sun":     6,
    "Moon":    10,
    "Mars":    7,
    "Rahu":    18,
    "Jupiter": 16,
    "Saturn":  19,
    "Mercury": 17,
}

# Dasha order — used to sequence after the birth dasha
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# Map nakshatra index (0..26) -> dasha lord
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
]

# Exaltation / debilitation degrees (sidereal sign + degree of peak)
EXALTATION = {
    "Sun":     ("Aries",       10),
    "Moon":    ("Taurus",      3),
    "Mars":    ("Capricorn",   28),
    "Mercury": ("Virgo",       15),
    "Jupiter": ("Cancer",      5),
    "Venus":   ("Pisces",      27),
    "Saturn":  ("Libra",       20),
    "Rahu":    ("Taurus",      20),
    "Ketu":    ("Scorpio",     20),
}

DEBILITATION = {
    "Sun":     ("Libra",       10),
    "Moon":    ("Scorpio",     3),
    "Mars":    ("Cancer",      28),
    "Mercury": ("Pisces",      15),
    "Jupiter": ("Capricorn",   5),
    "Venus":   ("Virgo",       27),
    "Saturn":  ("Aries",       20),
    "Rahu":    ("Scorpio",     20),
    "Ketu":    ("Taurus",      20),
}

OWN_SIGNS = {
    "Sun":     ["Leo"],
    "Moon":    ["Cancer"],
    "Mars":    ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus":   ["Taurus", "Libra"],
    "Saturn":  ["Capricorn", "Aquarius"],
}
