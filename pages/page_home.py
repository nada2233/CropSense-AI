"""Page 1 — Home (landing page)."""
import streamlit as st


def render():
    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1b5e20 0%,#2e7d32 55%,#43a047 100%);
                border-radius:18px;padding:52px 40px 44px;margin-bottom:32px;text-align:center;
                box-shadow:0 4px 20px rgba(46,125,50,.25);">
        <div style="font-size:70px;margin-bottom:10px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.3));">🌾</div>
        <h1 style="color:#ffffff!important;font-size:2.8rem;font-weight:800;margin:0;letter-spacing:-.5px;">
            GrowSmart
        </h1>
        <p style="color:#c8e6c9;font-size:1.15rem;margin:12px auto 0;max-width:580px;line-height:1.6;">
            Data-driven crop recommendation powered by XGBoost Machine Learning.
            Enter your soil and climate data — get the ideal crop in seconds.
        </p>
        <div style="margin-top:22px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
            <span style="background:rgba(255,255,255,.15);color:#fff;padding:7px 18px;
                         border-radius:20px;font-size:13px;font-weight:600;">✅ 22 Crop Varieties</span>
            <span style="background:rgba(255,255,255,.15);color:#fff;padding:7px 18px;
                         border-radius:20px;font-size:13px;font-weight:600;">🎯 94.17% Test Accuracy</span>
            <span style="background:rgba(255,255,255,.15);color:#fff;padding:7px 18px;
                         border-radius:20px;font-size:13px;font-weight:600;">📊 65,506 Training Samples</span>
            <span style="background:rgba(255,255,255,.15);color:#fff;padding:7px 18px;
                         border-radius:20px;font-size:13px;font-weight:600;">🔬 13 Engineered Features</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Objectives ───────────────────────────────────────────────────────────
    st.markdown("## 🎯 Project Objectives")
    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in zip(
        [c1, c2, c3],
        ["🔬", "🌍", "📈"],
        ["Data-Driven Decisions", "Support Farmers", "Optimise Yield"],
        [
            "Replace guesswork with ML-driven recommendations based on real soil and climate measurements.",
            "Empower farmers and agronomists with actionable, explainable insights to reduce risk.",
            "Match the right crop to the right environment using proven soil-science and climate data.",
        ],
    ):
        with col:
            st.markdown(f"""
            <div style="background:#f1f8e9;border-radius:14px;padding:24px 20px;
                        border-top:4px solid #4caf50;min-height:155px;
                        box-shadow:0 2px 6px rgba(0,0,0,.05);">
                <div style="font-size:34px;">{icon}</div>
                <h4 style="color:#2e7d32;margin:10px 0 6px;">{title}</h4>
                <p style="color:#555;font-size:13.5px;line-height:1.55;margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Key Features ─────────────────────────────────────────────────────────
    st.markdown("## ✨ Application Features")
    features = [
        ("🌱", "Crop Recommendation",
         "Input N, P, K, temperature, humidity, pH and rainfall — receive the top 3 crops with confidence scores and a probability bar chart."),
        ("🤖", "Agricultural Assistant",
         "Chat-style assistant powered by the ML model. Ask about any crop's suitability and get probability-based, rule-explained answers."),
        ("📊", "Insights Dashboard",
         "10+ interactive Plotly charts: crop distribution, climate patterns, soil fertility analysis, NPK breakdown, correlation heatmap."),
        ("🔬", "Feature Engineering",
         "7 raw features expanded to 13: Soil Fertility Index, NPK Ratio, Climate Type, Soil Type, Rainfall Level, Temp×Humidity interaction."),
        ("🏆", "XGBoost Model",
         "Best model after comparing 9 algorithms with two rounds of RandomizedSearchCV. Two-round tuning improved F1 from 93.79% → 94.12%."),
        ("📋", "Error Analysis",
         "Transparent reporting of top confusion pairs (Blackgram↔Mungbean, Papaya↔Coconut) — caused by shared agricultural profiles."),
    ]
    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, features[i:i+3]):
            with col:
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e8f5e9;border-radius:12px;
                            padding:20px;margin-bottom:14px;
                            box-shadow:0 2px 6px rgba(0,0,0,.04);transition:box-shadow .2s;">
                    <span style="font-size:30px;">{icon}</span>
                    <h4 style="color:#2e7d32;margin:10px 0 6px;font-size:15px;">{title}</h4>
                    <p style="color:#666;font-size:13px;line-height:1.55;margin:0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────────────────────
    st.markdown("## 📈 System at a Glance")
    stats = [
        ("🌾", "22",       "Crop Varieties"),
        ("📊", "65,506",   "Training Samples"),
        ("🎯", "94.17%",   "Test Accuracy"),
        ("🔬", "13",       "Input Features"),
        ("🏆", "XGBoost",  "Best Model"),
        ("🔁", "2× Tuned", "Hyperparameter Search"),
    ]
    cols = st.columns(len(stats))
    for col, (icon, val, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="text-align:center;background:#f9fbe7;border-radius:12px;
                        padding:18px 8px;border:1px solid #dcedc8;">
                <div style="font-size:28px;">{icon}</div>
                <div style="font-size:1.45rem;font-weight:700;color:#2e7d32;margin:4px 0;">{val}</div>
                <div style="font-size:11.5px;color:#777;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#e8f5e9,#f9fbe7);border-radius:12px;
                padding:20px 28px;text-align:center;border:1px solid #c8e6c9;">
        <p style="color:#2e7d32;font-size:15px;margin:0;font-weight:500;">
            👈 Use the sidebar to navigate &nbsp;·&nbsp;
            Start with <strong>🌱 Crop Recommendation</strong> to get your first prediction
        </p>
    </div>
    """, unsafe_allow_html=True)
