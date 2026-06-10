"""Page 4 — Insights Dashboard (all charts from the insights notebook)."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.helpers import load_data

GREEN_SEQ  = "Greens"
TEAL_SEQ   = "Teal"
PLOTLY_TPL = "plotly_white"


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_data()


def _section(title: str, icon: str = ""):
    st.markdown(f"### {icon} {title}")


def render():
    st.markdown("# 📊 Insights Dashboard")
    st.markdown(
        "Interactive visualisations derived from the feature-engineered dataset "
        "(65,506 samples · 22 crops · 15 features)."
    )

    df = get_data()

    # ── Filter sidebar controls ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("#### 🔽 Dashboard Filters")
        sel_climate = st.multiselect(
            "Climate Type",
            options=sorted(df["climate_type"].unique()),
            default=sorted(df["climate_type"].unique()),
        )
        sel_category = st.multiselect(
            "Crop Category",
            options=sorted(df["crop_category"].unique()),
            default=sorted(df["crop_category"].unique()),
        )

    df_f = df[
        df["climate_type"].isin(sel_climate) &
        df["crop_category"].isin(sel_category)
    ]

    if df_f.empty:
        st.warning("No data matches the selected filters. Please adjust the sidebar.")
        return

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 1 — Distribution overview
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("Crop & Climate Distribution", "🌍")
    col1, col2 = st.columns(2)

    with col1:
        cat_cnt = (
            df_f["crop_category"].value_counts().reset_index()
            .rename(columns={"crop_category": "Category", "count": "Count"})
        )
        fig = px.bar(
            cat_cnt, x="Category", y="Count", color="Category",
            title="Crop Category Distribution",
            text="Count", template=PLOTLY_TPL,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        clim_cnt = df_f["climate_type"].value_counts().reset_index()
        clim_cnt.columns = ["Climate", "Count"]
        fig = px.pie(
            clim_cnt, names="Climate", values="Count",
            title="Climate Type Distribution",
            color_discrete_sequence=px.colors.sequential.Greens_r,
        )
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 2 — Soil Fertility
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("Soil Fertility Analysis", "🧪")
    col3, col4 = st.columns(2)

    with col3:
        fert_cat = (
            df_f.groupby("crop_category")["soil_fertility"]
            .mean().reset_index().sort_values("soil_fertility", ascending=False).round(2)
        )
        fert_cat.columns = ["Category", "Avg Fertility"]
        fig = px.bar(
            fert_cat, x="Category", y="Avg Fertility",
            color="Avg Fertility", color_continuous_scale=GREEN_SEQ,
            title="Average Soil Fertility by Crop Category",
            text="Avg Fertility", template=PLOTLY_TPL,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        top_fert = (
            df_f.groupby("label")["soil_fertility"]
            .mean().sort_values(ascending=False).head(10).reset_index().round(1)
        )
        top_fert.columns = ["Crop", "Avg Fertility"]
        fig = px.bar(
            top_fert, x="Crop", y="Avg Fertility",
            color="Avg Fertility", color_continuous_scale=GREEN_SEQ,
            title="Top 10 Crops by Average Soil Fertility",
            text="Avg Fertility", template=PLOTLY_TPL,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 3 — Rainfall & Temperature
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("Rainfall & Temperature Analysis", "🌧️")
    col5, col6 = st.columns(2)

    with col5:
        rain_cnt = df_f["rainfall_level"].value_counts().reset_index()
        rain_cnt.columns = ["Level", "Count"]
        fig = px.bar(
            rain_cnt, x="Level", y="Count", color="Level",
            title="Rainfall Level Distribution",
            text="Count",
            category_orders={"Level": ["Low", "Medium", "High", "Extreme"]},
            template=PLOTLY_TPL,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        rain_crop = (
            df_f.groupby("label")["rainfall"]
            .mean().sort_values(ascending=False).reset_index().round(1)
        )
        rain_crop.columns = ["Crop", "Avg Rainfall (mm)"]
        fig = px.bar(
            rain_crop, x="Crop", y="Avg Rainfall (mm)",
            color="Avg Rainfall (mm)", color_continuous_scale=TEAL_SEQ,
            title="Average Rainfall Requirement by Crop",
            text="Avg Rainfall (mm)", template=PLOTLY_TPL,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    # Temperature
    temp_crop = (
        df_f.groupby("label")["temperature"]
        .mean().sort_values(ascending=False).reset_index().round(2)
    )
    temp_crop.columns = ["Crop", "Avg Temperature (°C)"]
    fig = px.bar(
        temp_crop, x="Crop", y="Avg Temperature (°C)",
        color="Avg Temperature (°C)",
        color_continuous_scale="RdYlGn_r",
        title="Average Temperature Requirement by Crop",
        text="Avg Temperature (°C)", template=PLOTLY_TPL,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(coloraxis_showscale=False, height=380)
    st.plotly_chart(fig, use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 4 — NPK Analysis
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("NPK & Soil Chemistry", "⚗️")

    npk = df_f.groupby("label")[["N", "P", "K"]].mean().reset_index()
    fig = px.bar(
        npk, x="label", y=["N", "P", "K"],
        barmode="group",
        title="Average NPK Levels by Crop",
        labels={"label": "Crop", "value": "Mean (kg/ha)", "variable": "Nutrient"},
        template=PLOTLY_TPL, height=420,
        color_discrete_map={"N": "#43a047", "P": "#fb8c00", "K": "#1e88e5"},
    )
    st.plotly_chart(fig, use_container_width=True)

    col7, col8 = st.columns(2)
    with col7:
        ratio_crop = (
            df_f.groupby("label")["NPK_Ratio"]
            .mean().sort_values(ascending=False).reset_index().round(2)
        )
        ratio_crop.columns = ["Crop", "NPK Ratio"]
        fig = px.bar(
            ratio_crop, x="Crop", y="NPK Ratio",
            color="NPK Ratio", color_continuous_scale=GREEN_SEQ,
            title="Average NPK Ratio by Crop  (N / P+K)",
            text="NPK Ratio", template=PLOTLY_TPL,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col8:
        ph_cat = (
            df_f.groupby("crop_category")["ph"]
            .mean().reset_index().sort_values("ph", ascending=False).round(2)
        )
        ph_cat.columns = ["Category", "Avg pH"]
        fig = px.bar(
            ph_cat, x="Category", y="Avg pH",
            color="Avg pH", color_continuous_scale="RdBu",
            title="Average Soil pH by Crop Category",
            text="Avg pH", template=PLOTLY_TPL,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, height=360)
        st.plotly_chart(fig, use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 5 — Climate × Crops
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("Crop Recommendation Across Climate Types", "🌤️")

    climate_crop = pd.crosstab(df_f["climate_type"], df_f["crop_category"])
    fig = px.imshow(
        climate_crop, text_auto=True, aspect="auto",
        title="Crop Category vs Climate Type (Count)",
        color_continuous_scale=GREEN_SEQ,
    )
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)

    # Top 5 crops per climate
    top_cli = (
        df_f.groupby(["climate_type", "label"])
        .size().reset_index(name="Count")
        .sort_values(["climate_type", "Count"], ascending=[True, False])
        .groupby("climate_type").head(5)
    )
    fig = px.bar(
        top_cli, x="climate_type", y="Count", color="label",
        title="Top 5 Recommended Crops per Climate Type",
        text="Count", template=PLOTLY_TPL, height=420,
        labels={"climate_type": "Climate", "label": "Crop"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 6 — Soil Type Distribution
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("Soil Type Distribution", "🏔️")

    soil_crop = pd.crosstab(df_f["soil_type"], df_f["label"])
    fig = px.imshow(
        soil_crop, text_auto=True, aspect="auto",
        title="Crop Distribution Across Soil Types",
        color_continuous_scale="Greens",
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 7 — Correlation Heatmap
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("Correlation Heatmap", "🔗")

    corr = df_f.select_dtypes(include="number").corr().round(2)
    fig = px.imshow(
        corr, text_auto=True, aspect="auto",
        title="Feature Correlation Matrix",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
    )
    fig.update_layout(height=520)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="background:#f1f8e9;border-radius:10px;padding:14px 20px;
                border-left:4px solid #4caf50;margin-top:8px;">
        <b style="color:#2e7d32;">Key Correlations:</b>
        <ul style="margin:6px 0 0;color:#444;font-size:13.5px;line-height:1.8;">
            <li><b>soil_fertility</b> ↔ <b>N</b> (0.82) and <b>K</b> (0.90) — expected by design</li>
            <li><b>temp_humidity</b> combines temperature and humidity effectively</li>
            <li><b>ph</b> is largely independent — an important standalone factor</li>
            <li><b>rainfall</b> shows moderate positive correlation with N and K</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # ROW 8 — Temp-Humidity Interaction
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section("Temperature-Humidity Interaction", "🌡️")

    th_crop = (
        df_f.groupby("label")["temp_humidity"]
        .mean().sort_values(ascending=False).reset_index().round(0)
    )
    th_crop.columns = ["Crop", "Temp×Humidity"]
    fig = px.bar(
        th_crop, x="Crop", y="Temp×Humidity",
        color="Temp×Humidity", color_continuous_scale="Oranges",
        title="Temperature × Humidity Interaction by Crop",
        text="Temp×Humidity", template=PLOTLY_TPL,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(coloraxis_showscale=False, height=380)
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "🌴 **Rice, Coconut, and Cotton** have the highest Temp×Humidity values — "
        "indicating a strong preference for warm, humid environments.\n\n"
        "❄️ **Chickpea and Kidneybeans** have the lowest — better adapted to cool, dry conditions."
    )
