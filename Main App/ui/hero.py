import base64
from pathlib import Path

import streamlit as st

SLOGAN = "Train smarter. Perfect every rep."
SUBTEXT = (
    "Real-time AI form checking, automatic rep counting and voice coaching "
    "for all exercises all from your own webcam."
)

_IMG = Path(__file__).parent.parent / "static" / "hero.jpg"


def _background() -> str:
    overlay = "linear-gradient(180deg, rgba(5,8,15,.55) 0%, rgba(5,8,15,.92) 100%)"
    if _IMG.exists():
        b64 = base64.b64encode(_IMG.read_bytes()).decode()
        return f"{overlay}, url(data:image/jpeg;base64,{b64}) center/cover no-repeat"
    return "linear-gradient(135deg, #0b1220 0%, #12263f 50%, #0b3d3a 100%)"


def render_hero():
    st.markdown(
        f"""
        <div class="fc-hero" style="background:{_background()};">
            <p class="fc-kicker">AI · REAL-TIME · FORM ANALYSIS</p>
            <h1 class="fc-slogan">{SLOGAN}</h1>
            <p class="fc-sub">{SUBTEXT}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
