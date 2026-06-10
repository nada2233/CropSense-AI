"""Page 2 — Crop Recommendation."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.prediction import predict_top3, predict_all_proba
from utils.helpers import (
    CROP_EMOJIS, CROP_DESCRIPTIONS, MEDAL, MEDAL_COLOR,
    soil_type_label, climate_label, fertility_label,
)

# ── Per-medal card borders
CARD_BORDER = ["#f9a825", "#9e9e9e", "#8d6e63"]
CARD_BG     = ["#fffde7", "#fafafa", "#fff8f5"]


def render():
    st.markdown("# 🌱 Crop Recommendation")
    st.markdown(
        "Enter your **soil nutrients** and **environmental conditions** below. "
        "The XGBoost model will return the top 3 most suitable crops with confidence scores."
    )
    st.markdown("---")

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("rec_form"):
        st.markdown("### 🧪 Soil Nutrient Parameters")
        c1, c2, c3 = st.columns(3)
        with c1:
            N = st.slider("🟢 Nitrogen (N) — kg/ha",      0.0, 200.0, 70.0, 0.5,
                          help="Nitrogen: essential for leaf/vegetative growth.")
        with c2:
            P = st.slider("🟡 Phosphorus (P) — kg/ha",   10.0, 150.0, 40.0, 0.5,
                          help="Phosphorus: supports root development and energy transfer.")
        with c3:
            K = st.slider("🔵 Potassium (K) — kg/ha",    10.0, 350.0, 60.0, 0.5,
                          help="Potassium: improves disease resistance and water regulation.")

        st.markdown("### 🌡️ Environmental Conditions")
        c4, c5, c6, c7 = st.columns(4)
        with c4:
            temperature = st.slider("🌡️ Temperature (°C)", 15.0, 36.0, 25.0, 0.1)
        with c5:
            humidity    = st.slider("💧 Humidity (%)",       0.0, 100.0, 70.0, 0.5)
        with c6:
            ph          = st.slider("⚗️ Soil pH",            5.0,   8.5,  6.5, 0.01)
        with c7:
            rainfall    = st.slider("🌧️ Rainfall (mm)",    200.0, 3000.0, 800.0, 10.0)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍  Recommend Crops", use_container_width=True)

    # ── Results ───────────────────────────────────────────────────────────────
    if submitted:
        # Persist inputs for the assistant page
        st.session_state["last_inputs"] = dict(
            N=N, P=P, K=K,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
        )

        # Derived summary labels
        soil_lbl    = soil_type_label(ph)
        cli_lbl     = climate_label(temperature, humidity, rainfall)
        fert_val    = 0.4 * N + 0.3 * P + 0.3 * K
        fert_lbl    = fertility_label(fert_val)
        NPK_ratio   = N / (P + K + 1e-5)

        st.markdown("---")
        # Summary row
        st.markdown("### 📋 Input Summary")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Soil Type",       soil_lbl)
        m2.metric("Climate",         cli_lbl)
        m3.metric("Fertility Score", f"{fert_val:.1f} ({fert_lbl})")
        m4.metric("NPK Ratio",       f"{NPK_ratio:.2f}")
        m5.metric("pH",              f"{ph:.2f}")

        st.markdown("---")
        st.markdown("### 🏆 Top 3 Recommended Crops")

        top3 = predict_top3(N, P, K, temperature, humidity, ph, rainfall)

        # Cards
        card_cols = st.columns(3)
        for idx, ((crop, prob), col) in enumerate(zip(top3, card_cols)):
            emoji  = CROP_EMOJIS.get(crop, "🌿")
            medal  = MEDAL[idx]
            border = CARD_BORDER[idx]
            bg     = CARD_BG[idx]
            desc   = CROP_DESCRIPTIONS.get(crop, "")
            with col:
                st.markdown(f"""
                <div style="background:{bg};border-radius:14px;
                            border-left:5px solid {border};padding:24px 18px;
                            text-align:center;box-shadow:0 3px 12px rgba(0,0,0,.08);
                            min-height:230px;">
                    <div style="font-size:52px;line-height:1;">{emoji}</div>
                    <div style="font-size:24px;margin:6px 0;">{medal}</div>
                    <h3 style="color:#1b5e20;text-transform:capitalize;margin:4px 0;
                               font-size:1.25rem;">{crop}</h3>
                    <div style="font-size:2rem;font-weight:800;color:{border};
                                margin:4px 0;">{prob:.1f}%</div>
                    <p style="font-size:12px;color:#777;margin:8px 0 0;line-height:1.45;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Bar chart — top 3 ─────────────────────────────────────────────────
        fig = go.Figure(go.Bar(
            x=[c.capitalize() for c, _ in top3],
            y=[p for _, p in top3],
            marker_color=MEDAL_COLOR,
            text=[f"{p:.1f}%" for _, p in top3],
            textposition="outside",
            textfont=dict(size=14, color="#333"),
            width=0.45,
        ))
        fig.update_layout(
            title=dict(text="Top 3 Crop Recommendation Confidence", font=dict(size=17)),
            xaxis_title="Crop",
            yaxis_title="Probability (%)",
            yaxis=dict(range=[0, max(p for _, p in top3) * 1.25]),
            template="plotly_white",
            height=360,
            margin=dict(t=50, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Full probability distribution ─────────────────────────────────────
        with st.expander("📊 View All 22 Crop Probabilities"):
            all_p = predict_all_proba(N, P, K, temperature, humidity, ph, rainfall)
            pairs = sorted(all_p.items(), key=lambda x: x[1], reverse=True)
            fig2  = px.bar(
                x=[c.capitalize() for c, _ in pairs],
                y=[p for _, p in pairs],
                labels={"x": "Crop", "y": "Probability (%)"},
                title="Full Probability Distribution — All 22 Crops",
                color=[p for _, p in pairs],
                color_continuous_scale="Greens",
                text=[f"{p:.1f}%" for _, p in pairs],
            )
            fig2.update_traces(textposition="outside")
            fig2.update_layout(
                template="plotly_white", height=420,
                showlegend=False, coloraxis_showscale=False,
                margin=dict(t=50, b=30),
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.success(
            "💡 **Tip:** Go to **🤖 Agricultural Assistant** to ask follow-up questions "
            "about any crop using these same soil conditions.",
            icon=None,
        )

    else:
        # Placeholder when form not yet submitted
        st.markdown("""
        <div style="background:#f9fbe7;border-radius:12px;padding:32px;text-align:center;
                    border:2px dashed #c5e1a5;margin-top:16px;">
            <div style="font-size:52px;">🌿</div>
            <h3 style="color:#558b2f;">Adjust the sliders and click <em>Recommend Crops</em></h3>
            <p style="color:#777;font-size:14px;">
                The model will instantly return the top 3 crops with confidence percentages.
            </p>
        </div>
        """, unsafe_allow_html=True)
