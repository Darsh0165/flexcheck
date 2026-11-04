import streamlit as st

from services.analytics.streak import get_streak
from ui.hero import render_hero
from ui.topbar import render_topbar

render_topbar()
render_hero()

streak, done_today = get_streak(st.session_state["user_id"])

left, right = st.columns([3, 1], vertical_alignment="center")

with left:
    if st.button("🚀  Start Workout", type="primary", width="stretch", key="hero_start"):
        st.switch_page("views/workout.py")

with right:
    note = "Done today ✅" if done_today else "Work out today to keep it"
    st.markdown(
        f"""
        <div class="fc-streak">
            <div class="fc-streak-num">🔥 {streak}</div>
            <div class="fc-streak-label">day streak</div>
            <div class="fc-streak-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### What FlexCheck does")

features = [
    ("🎯", "Live form check", "Checks your posture and joint angles from webcam pose landmarks."),
    ("🔢", "Smart rep counter", "Counts only full, clean reps and ignores jitter and half reps."),
    ("🏋️", "5 exercises", "Squats, push-ups, biceps curls, shoulder press and lunges."),
    ("📊", "Progress analytics", "Charts for volume, calories and BMI trends over time."),
]
for col, (icon, title, text) in zip(st.columns(4), features):
    col.markdown(
        f"""
        <div class="fc-card">
            <div class="fc-card-icon">{icon}</div>
            <div class="fc-card-title">{title}</div>
            <div class="fc-card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### How it works")
a, b, c = st.columns(3)
a.markdown("**1. Plan**  \nPick your exercise, sets and reps.")
b.markdown("**2. Move**  \nAllow the camera. Everything is processed on your own device.")
c.markdown("**3. Improve**  \nGet live feedback, then review your history and trends.")
