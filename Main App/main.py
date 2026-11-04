import os
from pathlib import Path

import streamlit as st

from services.auth.login_wall import render_login_wall
from services.persistence.exercise_repository import init_db
from services.ui.style_loader import load_css, inject_local_font

st.set_page_config(
    page_icon="🦵",
    page_title="FlexCheck",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css(os.path.join(os.getcwd(), "static", "style.css"))
inject_local_font(os.path.join(os.getcwd(), "static", "AdobeClean.otf"), "AdobeClean")

_extra_css = Path(__file__).parent / "static" / "flexcheck.css"
if _extra_css.exists():
    st.markdown(f"<style>{_extra_css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

init_db()

if not render_login_wall():
    st.stop()

pages = [
    st.Page("views/overview.py", title="Overview", icon="🏠", default=True),
    st.Page("views/history.py", title="History", icon="🗂️"),
    st.Page("views/schedule.py", title="Schedule & Analytics", icon="📈"),
    st.Page("views/about.py", title="About", icon="ℹ️"),
    st.Page("views/workout.py", title="Workout", icon="🏋️"),
]

st.navigation(pages, position="hidden").run()
