"""
CGrowSmart — Multi-page Streamlit Application
Entry point: main.py
Run with:  streamlit run main.py
"""
import streamlit as st

st.set_page_config(
    page_title="GrowSmart",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a3a2a 0%, #0d2318 100%) !important;
    border-right: 1px solid #2d5a3d;
}
[data-testid="stSidebar"] * {
    color: #d4edda !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 15px;
    padding: 8px 4px;
    cursor: pointer;
    border-radius: 6px;
    transition: background .15s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,.08);
}

/* ---- Headings ---- */
h1 { color: #1b5e20 !important; font-weight: 700; }
h2 { color: #2e7d32 !important; }
h3 { color: #388e3c !important; }

/* ---- Metric tiles ---- */
div[data-testid="metric-container"] {
    background: #f1f8e9;
    border-left: 4px solid #4caf50;
    border-radius: 10px;
    padding: 14px 18px;
}

/* ---- Primary buttons ---- */
div.stButton > button {
    background: linear-gradient(135deg, #2e7d32, #66bb6a) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all .2s;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #1b5e20, #4caf50) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(46,125,50,.35) !important;
}

/* ---- Form submit button ---- */
div.stFormSubmitButton > button {
    background: linear-gradient(135deg, #2e7d32, #66bb6a) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 12px 24px !important;
}

/* ---- Info / success boxes ---- */
div[data-testid="stAlert"] { border-radius: 10px; }

/* ---- Plotly chart containers ---- */
div[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,.07);
}

/* ---- Hide default multi-page nav ---- */
[data-testid="stSidebarNav"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px;">
        <div style="font-size:52px;">🌾</div>
        <h2 style="color:#a5d6a7!important;font-size:1.3rem;margin:4px 0;">GrowSmart</h2>
        <p style="color:#81c784!important;font-size:12px;margin:0;">
            Intelligent Crop Recommendation
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2d5a3d;margin:8px 0 16px;'>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        options=[
            "🏠  Home",
            "🌱  Crop Recommendation",
            "🤖  Agricultural Assistant",
            "📊  Insights Dashboard",
            "📘  About Project",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#2d5a3d;margin:16px 0 10px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;font-size:11px;color:#81c784!important;line-height:1.7;">
        🤖 Model: <b style='color:#a5d6a7!important;'>XGBoost</b><br>
        🎯 Test Accuracy: <b style='color:#a5d6a7!important;'>94.17%</b><br>
        🌿 22 Crop Varieties<br>
        📊 65,506 Training Samples
    </div>
    """, unsafe_allow_html=True)

# ── Route to correct page ─────────────────────────────────────────────────────
if   "🏠"  in page:
    from pages.page_home           import render
elif "🌱"  in page:
    from pages.page_recommendation import render
elif "🤖"  in page:
    from pages.page_assistant      import render
elif "📊"  in page:
    from pages.page_insights       import render
else:
    from pages.page_about          import render

render()
