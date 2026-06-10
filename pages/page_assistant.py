"""
Page 3 — Agricultural Assistant.
Powered ONLY by the trained XGBoost model + rule-based logic.
No LLM, no API calls.
"""
import re
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.prediction import predict_top3, get_crop_proba
from utils.helpers import CROP_LABELS, CROP_EMOJIS, rule_based_explanation

# ── Regex keyword lists ────────────────────────────────────────────────────────
_WHY_KEYWORDS    = ("why", "explain", "reason", "because", "هليه", "سبب", "لماذا")
_BEST_KEYWORDS   = ("best", "top", "recommend", "suggest", "أفضل", "افضل", "توصية")
_CANNOT_KEYWORDS = ("can i", "can i grow", "suitable", "is", "أزرع", "أنزع", "هل يمكن", "هل")


def _detect_crop(text: str):
    """Return the first crop name found in the user text, or None."""
    t = text.lower()
    for crop in CROP_LABELS:
        if crop in t:
            return crop
    return None


def _has_inputs() -> bool:
    return bool(st.session_state.get("last_inputs"))


def _inputs():
    return st.session_state.get("last_inputs", {})


def _suitability_response(crop: str, inp: dict) -> str:
    prob = get_crop_proba(crop, **inp)
    emoji = CROP_EMOJIS.get(crop, "🌿")
    cap   = crop.capitalize()

    if prob >= 70:
        verdict = (
            f"### {emoji} Yes — **{cap}** is highly recommended!\n\n"
            f"The model assigns a confidence of **{prob:.1f}%**, "
            f"placing it among the top choices for your current soil and climate conditions."
        )
    elif prob >= 40:
        verdict = (
            f"### {emoji} Maybe — **{cap}** is possible but not optimal.\n\n"
            f"The model gives {cap} a probability of **{prob:.1f}%**. "
            f"It can be grown, but conditions are not ideal."
        )
    else:
        verdict = (
            f"### {emoji} Not recommended — **{cap}** is unlikely to succeed.\n\n"
            f"The model gives {cap} only **{prob:.1f}%** confidence under the current conditions."
        )

    explanation = rule_based_explanation(crop, prob, **inp)
    return f"{verdict}\n\n---\n\n{explanation}"


def _top3_response(inp: dict) -> str:
    top3  = predict_top3(**inp)
    lines = ["### 🏆 Top 3 Recommended Crops for Your Conditions\n"]
    medals = ["🥇", "🥈", "🥉"]
    for i, (crop, prob) in enumerate(top3):
        emoji = CROP_EMOJIS.get(crop, "🌿")
        lines.append(f"{medals[i]} **{crop.capitalize()}** — {prob:.1f}% confidence {emoji}")
    lines.append(
        "\n\nYou can ask me *why* any of these crops is recommended, "
        "or whether a specific crop is suitable."
    )
    return "\n".join(lines)


def _why_response(crop: str, inp: dict) -> str:
    prob        = get_crop_proba(crop, **inp)
    emoji       = CROP_EMOJIS.get(crop, "🌿")
    explanation = rule_based_explanation(crop, prob, **inp)
    return (
        f"### {emoji} Why **{crop.capitalize()}** — {prob:.1f}% confidence\n\n"
        f"{explanation}"
    )


def _generate_response(user_text: str) -> str:
    inp  = _inputs()
    text = user_text.lower()
    crop = _detect_crop(user_text)

    # No soil data yet
    if not _has_inputs():
        return (
            "⚠️ I don't have any soil data yet.\n\n"
            "Please go to **🌱 Crop Recommendation**, enter your soil and climate values, "
            "and run a prediction first. Then come back here and I'll answer your questions "
            "using those exact conditions."
        )

    # "Why is X recommended / not recommended?"
    if crop and any(k in text for k in _WHY_KEYWORDS):
        return _why_response(crop, inp)

    # "Can I grow X?" / "Is X suitable?"
    if crop:
        return _suitability_response(crop, inp)

    # "What is the best crop?"
    if any(k in text for k in _BEST_KEYWORDS):
        return _top3_response(inp)

    # Greeting / small talk
    if any(k in text for k in ("hello", "hi", "hey", "مرحبا", "السلام")):
        inp_summary = inp
        fert = 0.4 * inp_summary["N"] + 0.3 * inp_summary["P"] + 0.3 * inp_summary["K"]
        return (
            f"👋 Hello! I'm your Agricultural Assistant powered by the GrowSmart XGBoost model.\n\n"
            f"I have your last soil reading loaded:\n"
            f"- N={inp_summary['N']:.0f}, P={inp_summary['P']:.0f}, K={inp_summary['K']:.0f}\n"
            f"- Temperature={inp_summary['temperature']:.1f}°C, "
            f"Humidity={inp_summary['humidity']:.1f}%, "
            f"Rainfall={inp_summary['rainfall']:.0f}mm, pH={inp_summary['ph']:.2f}\n"
            f"- Soil Fertility={fert:.1f}\n\n"
            f"Ask me things like:\n"
            f"- *Can I grow rice?*\n"
            f"- *Why is coffee recommended?*\n"
            f"- *What is the best crop?*"
        )

    # Fallback
    return (
        "🤔 I'm not sure what you're asking. Try one of these:\n\n"
        "- **'Can I grow [crop]?'** — suitability check with probability\n"
        "- **'Why is [crop] recommended?'** — detailed explanation\n"
        "- **'What is the best crop?'** — top 3 recommendations\n\n"
        f"Crops I know about: {', '.join(c.capitalize() for c in CROP_LABELS)}"
    )


# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.markdown("# 🤖 Agricultural Assistant")
    st.markdown(
        "Ask me anything about crop suitability for **your soil conditions**. "
        "I use the trained XGBoost model + rule-based logic — no external AI."
    )

    # ── Soil context banner ───────────────────────────────────────────────────
    if _has_inputs():
        inp  = _inputs()
        fert = 0.4 * inp["N"] + 0.3 * inp["P"] + 0.3 * inp["K"]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#e8f5e9,#f1f8e9);
                    border-radius:10px;padding:14px 20px;margin-bottom:16px;
                    border-left:4px solid #4caf50;font-size:13.5px;">
            <b style="color:#2e7d32;">🌿 Active Soil Context:</b>
            &nbsp; N={inp['N']:.0f} · P={inp['P']:.0f} · K={inp['K']:.0f} &nbsp;|&nbsp;
            Temp={inp['temperature']:.1f}°C · Humidity={inp['humidity']:.1f}% ·
            Rainfall={inp['rainfall']:.0f}mm · pH={inp['ph']:.2f} ·
            Fertility={fert:.1f}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(
            "⚠️ No soil data found. Go to **🌱 Crop Recommendation**, run a prediction first, "
            "then come back to ask questions."
        )

    st.markdown("---")

    # ── Quick-question chips ──────────────────────────────────────────────────
    st.markdown("**Quick questions:**")
    qcols = st.columns(4)
    quick_qs = [
        "What is the best crop?",
        "Can I grow rice?",
        "Can I grow banana?",
        "Why is coffee recommended?",
    ]
    for col, q in zip(qcols, quick_qs):
        with col:
            if st.button(q, use_container_width=True):
                if "messages" not in st.session_state:
                    st.session_state["messages"] = []
                st.session_state["messages"].append({"role": "user",    "text": q})
                st.session_state["messages"].append({"role": "assistant","text": _generate_response(q)})
                st.rerun()

    st.markdown("---")

    # ── Chat history ──────────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background:#e8f5e9;border-radius:12px 12px 2px 12px;
                        padding:12px 16px;margin:8px 0;max-width:80%;
                        margin-left:auto;text-align:right;">
                <b style="color:#1b5e20;">You:</b><br>{msg['text']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#f9fbe7;border-radius:12px 12px 12px 2px;
                        padding:14px 18px;margin:8px 0;max-width:88%;
                        border-left:3px solid #8bc34a;">
                <b style="color:#558b2f;">🤖 Assistant:</b><br>
            </div>
            """, unsafe_allow_html=True)
            # Use st.markdown for rich formatting
            st.markdown(msg["text"])

    # ── Input box ─────────────────────────────────────────────────────────────
    with st.form("chat_form", clear_on_submit=True):
        user_q = st.text_input(
            "Ask a question…",
            placeholder="e.g.  Can I grow mango?  /  Why is rice recommended?",
            label_visibility="collapsed",
        )
        send = st.form_submit_button("Send ➤", use_container_width=False)

    if send and user_q.strip():
        response = _generate_response(user_q.strip())
        st.session_state["messages"].append({"role": "user",     "text": user_q.strip()})
        st.session_state["messages"].append({"role": "assistant","text": response})
        st.rerun()

    if st.session_state["messages"]:
        if st.button("🗑️ Clear conversation"):
            st.session_state["messages"] = []
            st.rerun()
