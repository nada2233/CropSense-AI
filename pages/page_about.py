"""Page 5 — About Project."""
import streamlit as st


def render():
    st.markdown("# 📘 About Project")
    st.markdown("A complete reference for the GrowSmart machine learning pipeline.")

    # ── Project Summary ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🌾 Project Summary")
    st.markdown("""
    **GrowSmart** is a data-driven crop recommendation system that predicts the most
    suitable crop for a given plot of land based on soil nutrient content and environmental
    conditions.  
    The system was built as a full machine learning project — from raw data cleaning and
    feature engineering through model selection, two rounds of hyperparameter tuning,
    cross-validation, and error analysis.
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style="background:#f1f8e9;border-radius:12px;padding:20px;
                    border-top:4px solid #4caf50;">
            <h4 style="color:#2e7d32;">📁 Dataset</h4>
            <ul style="color:#444;font-size:14px;line-height:1.9;margin:0;">
                <li><b>Raw dataset:</b> Crop_Dataset_updated.csv</li>
                <li><b>After engineering:</b> 65,506 rows × 15 features</li>
                <li><b>Target:</b> 22 crop classes</li>
                <li><b>Split:</b> 80% train / 20% test (stratified)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#e8f5e9;border-radius:12px;padding:20px;
                    border-top:4px solid #66bb6a;">
            <h4 style="color:#2e7d32;">🏆 Final Model</h4>
            <ul style="color:#444;font-size:14px;line-height:1.9;margin:0;">
                <li><b>Algorithm:</b> XGBoost (XGBClassifier)</li>
                <li><b>Train Accuracy:</b> 96.66%</li>
                <li><b>Test Accuracy:</b> 94.17%</li>
                <li><b>Test F1 (weighted):</b> 94.12%</li>
                <li><b>CV F1 (5-fold):</b> 93.52%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Feature Engineering ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🔬 Feature Engineering Summary")
    st.markdown("7 raw features → **13 model input features** after engineering:")

    features = [
        ("N", "Nitrogen (kg/ha)", "Raw",        "Soil nutrient — essential for vegetative growth"),
        ("P", "Phosphorus (kg/ha)", "Raw",       "Root development and energy transfer"),
        ("K", "Potassium (kg/ha)", "Raw",        "Disease resistance and water regulation"),
        ("temperature", "Temperature (°C)", "Raw","Average ambient temperature"),
        ("humidity", "Humidity (%)", "Raw",      "Relative humidity"),
        ("ph", "Soil pH", "Raw",                 "Soil acidity/alkalinity"),
        ("rainfall", "Rainfall (mm)", "Raw",     "Annual rainfall"),
        ("NPK_Ratio", "N / (P + K + ε)", "Engineered", "Overall nutrient balance ratio"),
        ("soil_fertility", "0.4N + 0.3P + 0.3K", "Engineered", "Weighted soil fertility index"),
        ("temp_humidity", "Temp × Humidity", "Engineered", "Climate interaction feature"),
        ("rainfall_level", "Low/Medium/High/Extreme", "Engineered (Ordinal)", "Cut bins: 0/500/1000/2000/5000 mm"),
        ("soil_type", "Acidic/Neutral/Alkaline", "Engineered (Nominal)", "pH < 6 / ≤ 7.5 / > 7.5"),
        ("climate_type", "hot_humid / cool_dry etc.", "Engineered (Nominal)", "Temp > 27°C = hot; Hum > 60% or Rain > 1000 = humid"),
    ]

    st.markdown("""
    <table style="width:100%;border-collapse:collapse;font-size:13.5px;">
      <tr style="background:#2e7d32;color:#fff;">
        <th style="padding:10px;text-align:left;">Feature</th>
        <th style="padding:10px;text-align:left;">Formula / Values</th>
        <th style="padding:10px;text-align:left;">Type</th>
        <th style="padding:10px;text-align:left;">Description</th>
      </tr>
    """ + "".join(
        f"""<tr style="background:{'#f9fbe7' if i%2==0 else '#fff'};">
              <td style="padding:9px 10px;font-weight:600;color:#2e7d32;">{f}</td>
              <td style="padding:9px 10px;font-family:monospace;">{formula}</td>
              <td style="padding:9px 10px;"><span style="background:{'#c8e6c9' if 'Raw' in t else '#fff9c4'};
                  color:#333;padding:2px 8px;border-radius:10px;font-size:12px;">{t}</span></td>
              <td style="padding:9px 10px;color:#555;">{desc}</td>
            </tr>"""
        for i, (f, formula, t, desc) in enumerate(features)
    ) + "</table>", unsafe_allow_html=True)

    # ── ML Workflow ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## ⚙️ Machine Learning Workflow")

    steps = [
        ("1", "Data Cleaning", "#e8f5e9", "#4caf50",
         "Removed rows with humidity > 100 (physically impossible). Applied domain-guided min-max rescaling for 7 crops (banana, coconut, coffee, mango, orange, papaya, maize) to correct unrealistic NPK ranges. Per-label IQR outlier removal across all 7 numeric features."),
        ("2", "Feature Engineering", "#e3f2fd", "#1e88e5",
         "Created 6 new features: NPK_Ratio, soil_fertility, temp_humidity, rainfall_level (ordinal), soil_type (nominal from pH), climate_type (nominal from temp+humidity+rainfall). crop_category added for EDA but excluded from model input."),
        ("3", "Preprocessing Pipeline", "#fff3e0", "#fb8c00",
         "ColumnTransformer: StandardScaler on 10 numeric features, OrdinalEncoder on rainfall_level (Low→Medium→High→Extreme), OneHotEncoder (drop='first') on [soil_type, climate_type]. Pipeline = make_pipeline(transformer, model)."),
        ("4", "Model Comparison", "#f3e5f5", "#8e24aa",
         "9 models compared via Modeling() function: LogisticRegression, KNN, GaussianNB, SVC, DecisionTree, RandomForest, AdaBoost, XGBoost, GradientBoosting. XGBoost and RandomForest led in F1 score."),
        ("5", "Hyperparameter Tuning Round 1", "#fce4ec", "#e91e63",
         "RandomizedSearchCV (n_iter=5, cv=3, f1_weighted) for both RF and XGBoost. XGBoost Tuning 1: Test Accuracy 94.17%, F1 93.79%. RF: Test Accuracy 94.17%, F1 92.48% — overfitting."),
        ("6", "Hyperparameter Tuning Round 2", "#e8eaf6", "#3f51b5",
         "Wider XGBoost search (n_iter=15, cv=3): n_estimators, max_depth, learning_rate, subsample, colsample_bytree, gamma, min_child_weight. Best: Test Accuracy 94.17%, F1 94.12% — selected as final model."),
        ("7", "Cross-Validation", "#e0f7fa", "#00acc1",
         "5-fold standard CV: mean F1 93.20%. StratifiedKFold (5 splits, shuffle=True, random_state=42): mean F1 93.52%, std ~0.4%. Strong generalisation confirmed."),
        ("8", "Error Analysis", "#fff8e1", "#f9a825",
         "Top confusion pairs: Blackgram↔Mungbean (61), Papaya↔Coconut (54), Maize↔Watermelon (50), Cotton↔Watermelon (48), Pigeonpeas↔Kidneybeans (43). All pairs share similar NPK, temp, humidity, pH and rainfall ranges."),
    ]

    for num, title, bg, color, desc in steps:
        st.markdown(f"""
        <div style="background:{bg};border-radius:12px;padding:16px 20px;margin:8px 0;
                    border-left:5px solid {color};">
            <span style="background:{color};color:#fff;border-radius:50%;width:26px;height:26px;
                         display:inline-flex;align-items:center;justify-content:center;
                         font-weight:700;font-size:13px;margin-right:10px;">{num}</span>
            <b style="color:#333;font-size:15px;">{title}</b>
            <p style="color:#555;font-size:13.5px;margin:8px 0 0;line-height:1.6;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Model Evaluation Table ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📊 Model Evaluation Metrics")
    st.markdown("""
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr style="background:#2e7d32;color:#fff;">
        <th style="padding:11px;">Model</th>
        <th style="padding:11px;">Train Acc</th>
        <th style="padding:11px;">Test Acc</th>
        <th style="padding:11px;">Train F1</th>
        <th style="padding:11px;">Test F1</th>
        <th style="padding:11px;">Notes</th>
      </tr>
      <tr style="background:#f9fbe7;">
        <td style="padding:10px;">Random Forest (Tuning 1)</td>
        <td style="padding:10px;text-align:center;">97.64%</td>
        <td style="padding:10px;text-align:center;">92.50%</td>
        <td style="padding:10px;text-align:center;">97.63%</td>
        <td style="padding:10px;text-align:center;">92.41%</td>
        <td style="padding:10px;color:#e65100;">Moderate Overfitting</td>
      </tr>
      <tr style="background:#fff;">
        <td style="padding:10px;">Random Forest (Tuning 2)</td>
        <td style="padding:10px;text-align:center;">100.00%</td>
        <td style="padding:10px;text-align:center;">92.57%</td>
        <td style="padding:10px;text-align:center;">100.00%</td>
        <td style="padding:10px;text-align:center;">92.48%</td>
        <td style="padding:10px;color:#c62828;">Strong Overfitting</td>
      </tr>
      <tr style="background:#f9fbe7;">
        <td style="padding:10px;">XGBoost (Tuning 1)</td>
        <td style="padding:10px;text-align:center;">95.11%</td>
        <td style="padding:10px;text-align:center;">93.86%</td>
        <td style="padding:10px;text-align:center;">95.07%</td>
        <td style="padding:10px;text-align:center;">93.79%</td>
        <td style="padding:10px;color:#2e7d32;">Good Generalisation</td>
      </tr>
      <tr style="background:#e8f5e9;font-weight:700;">
        <td style="padding:10px;">✅ XGBoost (Tuning 2)</td>
        <td style="padding:10px;text-align:center;">96.66%</td>
        <td style="padding:10px;text-align:center;">94.17%</td>
        <td style="padding:10px;text-align:center;">96.63%</td>
        <td style="padding:10px;text-align:center;">94.12%</td>
        <td style="padding:10px;color:#1b5e20;">🏆 Best Overall Model</td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

    # ── Key Insights ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 💡 Key Insights")
    insights = [
        ("🌧️", "Rainfall is King",
         "Rainfall varies by more than 1,800 mm across crops — the single most influential environmental feature for crop recommendation."),
        ("💧", "Humidity Drives Separation",
         "Humid climates (cool_humid + hot_humid) support far more crop varieties than dry climates. Hot-humid environments favour Rice, Cotton and Banana."),
        ("🧪", "Soil Fertility from N & K",
         "Soil fertility is highly dependent on Nitrogen (corr=0.82) and Potassium (corr=0.90). Phosphorus contributes less to overall fertility."),
        ("⚗️", "pH is Independent",
         "Soil pH shows near-zero correlation with all other features, making it a standalone discriminating factor — especially for Apple and Coffee."),
        ("🌡️", "Temp×Humidity Interaction Works",
         "The engineered temp_humidity feature effectively separates tropical crops (Rice, Coconut) from dry-climate crops (Chickpea, Mothbeans)."),
        ("🤝", "Hard Pairs",
         "Blackgram and Mungbean share nearly identical NPK/climate profiles — the most common source of model confusion."),
    ]
    for icon, title, desc in insights:
        st.markdown(f"""
        <div style="background:#f9fbe7;border-radius:10px;padding:14px 18px;margin:6px 0;
                    border-left:4px solid #8bc34a;">
            <b style="color:#33691e;">{icon} {title}</b>
            <p style="color:#555;font-size:13.5px;margin:5px 0 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Business Recommendations ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📋 Business Recommendations")
    recs = [
        "Farmers in **humid climates** should prioritise fruit and cash crops (Banana, Coffee, Coconut).",
        "Monitor **Nitrogen and Potassium** as the primary soil health indicators — they drive 80%+ of fertility variation.",
        "Conduct a **pH test** before planting Apple, Coffee or Grapes — these crops are very pH-sensitive.",
        "In **semi-arid regions**, focus on drought-tolerant legumes: Chickpea, Mothbeans, Pigeonpeas.",
        "When the top two model recommendations are **Blackgram and Mungbean**, a more detailed soil test is advised (hard-to-separate pair).",
        "Use the **climate_type** classification as a quick screening tool before running full ML predictions.",
    ]
    for i, rec in enumerate(recs, 1):
        st.markdown(f"""
        <div style="background:#{'e8f5e9' if i%2 else '#fff'};border-radius:8px;
                    padding:12px 16px;margin:5px 0;border-left:3px solid #4caf50;">
            <span style="color:#2e7d32;font-weight:700;">#{i}</span>
            <span style="color:#444;font-size:14px;margin-left:8px;">{rec}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;background:#1b5e20;border-radius:12px;
                padding:20px;color:#c8e6c9;font-size:14px;">
        🌾 <b>GrowSmart</b> · XGBoost · 22 Crops · 94.17% Test Accuracy ·
        Built with Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)
