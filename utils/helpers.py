"""Shared constants, crop metadata, and rule-based explanation logic."""
import os
import pandas as pd

_BASE     = os.path.join(os.path.dirname(__file__), "..", "assets")
_DF_CACHE = None

CROP_LABELS = [
    "apple", "banana", "blackgram", "chickpea", "coconut", "coffee",
    "cotton", "grapes", "jute", "kidneybeans", "lentil", "maize",
    "mango", "mothbeans", "mungbean", "muskmelon", "orange", "papaya",
    "pigeonpeas", "pomegranate", "rice", "watermelon",
]

CROP_EMOJIS = {
    "apple": "🍎", "banana": "🍌", "blackgram": "🫘", "chickpea": "🫛",
    "coconut": "🥥", "coffee": "☕", "cotton": "🌿", "grapes": "🍇",
    "jute": "🌱", "kidneybeans": "🫘", "lentil": "🟤", "maize": "🌽",
    "mango": "🥭", "mothbeans": "🌿", "mungbean": "🌿", "muskmelon": "🍈",
    "orange": "🍊", "papaya": "🪴", "pigeonpeas": "🌾", "pomegranate": "🍎",
    "rice": "🌾", "watermelon": "🍉",
}

CROP_DESCRIPTIONS = {
    "apple":       "Cool-climate fruit; needs acidic soil, moderate humidity, well-drained land.",
    "banana":      "Tropical fruit; thrives in warm humid conditions with high potassium.",
    "blackgram":   "Drought-tolerant legume; suits semi-arid warm climates.",
    "chickpea":    "Cool-season legume; prefers low humidity and moderate rainfall.",
    "coconut":     "Tropical palm; requires high temperature, humidity and rainfall.",
    "coffee":      "Cool-humid highland cash crop; needs moderate nitrogen and acidic soil.",
    "cotton":      "Fiber crop; suited to hot humid conditions with moderate fertility.",
    "grapes":      "Vine fruit; prefers cool humid climates with acidic–neutral pH.",
    "jute":        "Fiber crop; needs high rainfall and warm humid climate.",
    "kidneybeans": "Cool-season legume; moderate water and nutrient needs.",
    "lentil":      "Cool-season legume; thrives in dry climates with low humidity.",
    "maize":       "Cereal crop; needs high temperature, fertility and moderate rainfall.",
    "mango":       "Tropical fruit; requires warm temperatures and moderate humidity.",
    "mothbeans":   "Drought-tolerant legume; suited to arid conditions.",
    "mungbean":    "Warm-season legume; moderate water and nutrient requirements.",
    "muskmelon":   "Fruit crop; suited to hot dry conditions with low rainfall.",
    "orange":      "Citrus fruit; thrives in warm temperatures with moderate humidity.",
    "papaya":      "Tropical fruit; needs high humidity, temperature and fertility.",
    "pigeonpeas":  "Drought-resistant legume; suited to tropical / subtropical climates.",
    "pomegranate": "Hardy fruit; tolerates dry conditions and high temperatures.",
    "rice":        "Staple cereal; requires high humidity, temperature and rainfall.",
    "watermelon":  "Fruit crop; suited to hot humid conditions with good soil fertility.",
}

CROP_CATEGORY = {
    "rice": "Cereal", "maize": "Cereal",
    "chickpea": "Legume", "lentil": "Legume", "mungbean": "Legume",
    "blackgram": "Legume", "pigeonpeas": "Legume", "mothbeans": "Legume",
    "kidneybeans": "Legume",
    "banana": "Fruit", "mango": "Fruit", "orange": "Fruit", "papaya": "Fruit",
    "apple": "Fruit", "grapes": "Fruit", "watermelon": "Fruit",
    "muskmelon": "Fruit", "pomegranate": "Fruit", "coconut": "Fruit",
    "coffee": "Cash Crop", "cotton": "Fiber Crop", "jute": "Fiber Crop",
}

MEDAL       = ["🥇", "🥈", "🥉"]
MEDAL_COLOR = ["#f9a825", "#9e9e9e", "#8d6e63"]


def load_data() -> pd.DataFrame:
    global _DF_CACHE
    if _DF_CACHE is None:
        _DF_CACHE = pd.read_csv(os.path.join(_BASE, "crop_recommendation_feature_engineered.csv"))
    return _DF_CACHE


def soil_type_label(ph: float) -> str:
    if ph < 6:    return "Acidic"
    if ph <= 7.5: return "Neutral"
    return "Alkaline"


def climate_label(temperature: float, humidity: float, rainfall: float) -> str:
    tc = "Hot"  if temperature > 27 else "Cool"
    hc = "Humid" if (humidity > 60 or rainfall > 1000) else "Dry"
    return f"{tc} & {hc}"


def fertility_label(f: float) -> str:
    if f < 40:  return "Low"
    if f < 80:  return "Moderate"
    if f < 120: return "Good"
    return "High"


def rule_based_explanation(
    crop: str, proba_pct: float,
    N, P, K, temperature, humidity, ph, rainfall,
) -> str:
    """
    Generates a structured rule-based explanation using
    the exact feature-engineering thresholds from the notebook.
    """
    fertility      = 0.4 * N + 0.3 * P + 0.3 * K
    soil_lbl       = soil_type_label(ph)
    climate_lbl    = climate_label(temperature, humidity, rainfall)
    fert_lbl       = fertility_label(fertility)
    crop_l         = crop.lower()

    parts = [
        f"**🧪 Soil:** N={N:.0f}, P={P:.0f}, K={K:.0f} — "
        f"Fertility {fertility:.1f} ({fert_lbl}), pH {ph:.2f} ({soil_lbl})",
        f"**🌡️ Climate:** {temperature:.1f}°C | {humidity:.1f}% humidity | "
        f"{rainfall:.0f} mm rainfall → {climate_lbl}",
    ]

    # Crop-specific rule checks
    if crop_l in ("rice", "jute"):
        if rainfall > 800 and humidity > 70:
            parts.append(f"✅ High rainfall ({rainfall:.0f} mm) and humidity ({humidity:.1f}%) "
                         f"strongly support **{crop}** cultivation.")
        else:
            parts.append(f"⚠️ **{crop.capitalize()}** typically needs rainfall > 800 mm and "
                         f"humidity > 70%. Current values may be limiting.")

    elif crop_l in ("apple", "grapes", "coffee", "lentil"):
        if temperature < 27:
            parts.append(f"✅ Cool temperature ({temperature:.1f}°C) suits **{crop}**, "
                         f"which thrives in cool-humid environments.")
        else:
            parts.append(f"⚠️ **{crop.capitalize()}** prefers temperatures below 27°C. "
                         f"Current {temperature:.1f}°C may reduce suitability.")

    elif crop_l in ("coconut", "banana", "papaya", "mango"):
        if temperature > 25 and humidity > 60:
            parts.append(f"✅ Warm temperature ({temperature:.1f}°C) and high humidity "
                         f"({humidity:.1f}%) match **{crop}**'s tropical requirements.")
        else:
            parts.append(f"⚠️ **{crop.capitalize()}** is tropical — needs temp > 25°C "
                         f"and humidity > 60%.")

    elif crop_l in ("chickpea", "lentil", "mothbeans", "muskmelon", "pomegranate"):
        if humidity < 60 and rainfall < 1000:
            parts.append(f"✅ Low humidity ({humidity:.1f}%) and moderate rainfall "
                         f"({rainfall:.0f} mm) suit **{crop}**'s drought-tolerant nature.")
        else:
            parts.append(f"⚠️ **{crop.capitalize()}** prefers drier conditions "
                         f"(humidity < 60%, rainfall < 1000 mm).")

    elif crop_l in ("maize", "cotton"):
        if temperature > 25 and N > 60:
            parts.append(f"✅ High temperature ({temperature:.1f}°C) and adequate nitrogen "
                         f"({N:.0f}) support **{crop}** growth.")
        else:
            parts.append(f"⚠️ **{crop.capitalize()}** needs warm temperatures (> 25°C) "
                         f"and nitrogen levels above 60.")

    return "\n\n".join(parts)
