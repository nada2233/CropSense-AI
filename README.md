# 🌾 GrowSmart — Crop Recommendation System

A professional multi-page Streamlit application powered by a trained XGBoost model.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run main.py
```

## 📁 Project Structure

```
crop_streamlit/
├── main.py                      ← Entry point (sidebar navigation)
├── requirements.txt
├── README.md
│
├── pages/
│   ├── page_home.py             ← Page 1: Landing page
│   ├── page_recommendation.py  ← Page 2: Crop prediction (predict_proba)
│   ├── page_assistant.py        ← Page 3: Rule-based ML assistant
│   ├── page_insights.py         ← Page 4: Plotly insights dashboard
│   └── page_about.py            ← Page 5: Project documentation
│
├── utils/
│   ├── prediction.py            ← Feature engineering + model inference
│   └── helpers.py               ← Constants, rule-based explanations
│
└── assets/
    ├── crop_recommendation_model.pkl   ← Trained XGBoost pipeline
    ├── label_encoder.pkl               ← LabelEncoder (0-21 → crop names)
    └── crop_recommendation_feature_engineered.csv
```

## 🤖 Model Details

| Property | Value |
|---|---|
| Algorithm | XGBoost (XGBClassifier) |
| Pipeline | ColumnTransformer → XGBClassifier |
| Train Accuracy | 96.66% |
| Test Accuracy | **94.17%** |
| Test F1 (weighted) | **94.12%** |
| CV F1 (5-fold stratified) | 93.52% |
| Classes | 22 crops |
| Training samples | 65,506 |

## 🔬 Feature Engineering (13 inputs)

7 raw → 13 engineered:
- **NPK_Ratio** = N / (P + K + ε)
- **soil_fertility** = 0.4·N + 0.3·P + 0.3·K
- **temp_humidity** = temperature × humidity
- **rainfall_level** = Low/Medium/High/Extreme (cut bins)
- **soil_type** = Acidic/Neutral/Alkaline (from pH)
- **climate_type** = hot_humid/hot_dry/cool_humid/cool_dry

## ⚠️ sklearn Version Note

The saved model was trained with **scikit-learn 1.6.1**.  
Pin `scikit-learn==1.6.1` in requirements.txt to avoid unpickling errors.
