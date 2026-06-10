"""
Prediction utilities.
Replicates EXACTLY the feature engineering pipeline from the ML notebook:
  - NPK_Ratio      = N / (P + K + 1e-5)
  - soil_fertility = 0.4*N + 0.3*P + 0.3*K
  - temp_humidity  = temperature * humidity
  - rainfall_level : cut bins [0,500,1000,2000,5000] → Low/Medium/High/Extreme
  - soil_type      : ph < 6 → Acidic | ph ≤ 7.5 → Neutral | else → Alkaline
  - climate_type   : (temp>27 → hot else cool) + (hum>60 or rain>1000 → humid else dry)

The uploaded pipeline (crop_recommendation_model.pkl) handles:
  - StandardScaler on num_features
  - OrdinalEncoder on rainfall_level
  - OneHotEncoder  on [soil_type, climate_type]
  - XGBClassifier  (returns integer labels 0-21)

label_encoder.pkl maps integer labels → crop names (alphabetical order).
"""
import os
import warnings
import pandas as pd
import joblib

warnings.filterwarnings("ignore")

_BASE  = os.path.join(os.path.dirname(__file__), "..", "assets")
_MODEL = None
_LE    = None


def _load():
    global _MODEL, _LE
    if _MODEL is None:
        _MODEL = joblib.load(os.path.join(_BASE, "crop_recommendation_model.pkl"))
        _LE    = joblib.load(os.path.join(_BASE, "label_encoder.pkl"))


# ── Feature order MUST match ColumnTransformer fit order ──────────────────────
# num_features (10) + ordinal (1) + nominal (2) = 13 total input columns
NUM_FEATURES     = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall",
                    "NPK_Ratio", "soil_fertility", "temp_humidity"]
ORDINAL_FEATURES = ["rainfall_level"]
NOMINAL_FEATURES = ["soil_type", "climate_type"]


def _engineer(N, P, K, temperature, humidity, ph, rainfall) -> pd.DataFrame:
    """Build the 13-column DataFrame that the pipeline expects."""

    NPK_Ratio      = N / (P + K + 1e-5)
    soil_fertility = 0.4 * N + 0.3 * P + 0.3 * K
    temp_humidity  = temperature * humidity

    # rainfall_level — matches pd.cut bins from notebook
    if   rainfall <= 500:  rainfall_level = "Low"
    elif rainfall <= 1000: rainfall_level = "Medium"
    elif rainfall <= 2000: rainfall_level = "High"
    else:                  rainfall_level = "Extreme"

    # soil_type
    if   ph < 6:   soil_type = "Acidic"
    elif ph <= 7.5: soil_type = "Neutral"
    else:           soil_type = "Alkaline"

    # climate_type
    temp_cat    = "hot"   if temperature > 27 else "cool"
    hum_cat     = "humid" if (humidity > 60 or rainfall > 1000) else "dry"
    climate_type = f"{temp_cat}_{hum_cat}"

    return pd.DataFrame([{
        "N": N, "P": P, "K": K,
        "temperature": temperature,
        "humidity":    humidity,
        "ph":          ph,
        "rainfall":    rainfall,
        "NPK_Ratio":      NPK_Ratio,
        "soil_fertility": soil_fertility,
        "temp_humidity":  temp_humidity,
        "rainfall_level": rainfall_level,
        "soil_type":      soil_type,
        "climate_type":   climate_type,
    }])


def predict_top3(N, P, K, temperature, humidity, ph, rainfall):
    """Returns [(crop_name, probability_pct), ...] top 3 sorted desc."""
    _load()
    df   = _engineer(N, P, K, temperature, humidity, ph, rainfall)
    prob = _MODEL.predict_proba(df)[0]
    pairs = sorted(zip(_LE.classes_, prob), key=lambda x: x[1], reverse=True)
    return [(c, round(float(p) * 100, 2)) for c, p in pairs[:3]]


def predict_all_proba(N, P, K, temperature, humidity, ph, rainfall) -> dict:
    """Returns {crop_name: probability_pct} for all 22 crops."""
    _load()
    df   = _engineer(N, P, K, temperature, humidity, ph, rainfall)
    prob = _MODEL.predict_proba(df)[0]
    return {c: round(float(p) * 100, 2) for c, p in zip(_LE.classes_, prob)}


def get_crop_proba(crop_name: str, N, P, K, temperature, humidity, ph, rainfall) -> float:
    """Returns single crop probability (%) for assistant page."""
    all_p = predict_all_proba(N, P, K, temperature, humidity, ph, rainfall)
    return all_p.get(crop_name.lower(), 0.0)
