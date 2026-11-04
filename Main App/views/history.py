from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from services.persistence.exercise_repository import get_users_exercises
from ui.topbar import render_topbar

CSS = """
@keyframes fcUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes fcSlideA{from{opacity:0;transform:translateX(18px)}to{opacity:1;transform:none}}
@keyframes fcSlideB{from{opacity:0;transform:translateX(18px)}to{opacity:1;transform:none}}
@keyframes fcPulse{0%,100%{box-shadow:0 0 0 0 rgba(94,234,212,.4)}50%{box-shadow:0 0 0 8px rgba(94,234,212,0)}}

.fc-story-hero{border:1px solid #1f2a3d;border-radius:16px;padding:clamp(28px,5vw,48px);margin-bottom:20px;
  background:radial-gradient(circle at 20% 0%,rgba(94,234,212,.10),#111a2b 70%);animation:fcUp .7s ease both}
.fc-story-hero h2{margin:0 0 8px;padding:0;font-size:clamp(1.6rem,4vw,2.4rem);color:#f8fafc}
.fc-story-hero p{margin:0;color:#cbd5e1;max-width:680px;line-height:1.6}

.fc-sec{margin:26px 0 8px;font-size:1.4rem;font-weight:700;color:#f8fafc}
.fc-sec-sub{color:#94a3b8;margin:0 0 14px}

.fc-tl{position:relative;margin:12px 0 28px;padding-left:36px}
.fc-tl::before{content:"";position:absolute;left:11px;top:8px;bottom:8px;width:2px;
  background:linear-gradient(#5eead4,#3b82f6,rgba(59,130,246,0))}
.fc-tl-item{position:relative;margin-bottom:16px;animation:fcUp .6s ease both}
.fc-tl-item:nth-child(1){animation-delay:.05s}.fc-tl-item:nth-child(2){animation-delay:.15s}
.fc-tl-item:nth-child(3){animation-delay:.25s}.fc-tl-item:nth-child(4){animation-delay:.35s}
.fc-tl-item:nth-child(5){animation-delay:.45s}.fc-tl-item:nth-child(6){animation-delay:.55s}
.fc-tl-item:nth-child(7){animation-delay:.65s}
.fc-tl-dot{position:absolute;left:-36px;top:16px;width:24px;height:24px;border-radius:50%;background:#0b1120;
  border:2px solid #5eead4;animation:fcPulse 2.4s infinite}
.fc-tl-card{background:#111a2b;border:1px solid #1f2a3d;border-radius:14px;padding:16px 18px;
  transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease,background .25s ease}
.fc-tl-card:hover{transform:translateX(6px);border-color:#2e3e59;background:#162238;box-shadow:0 8px 24px -6px rgba(0,0,0,.5)}
.fc-tl-title{font-weight:700;color:#f8fafc;font-size:1.05rem;margin-bottom:4px}
.fc-tl-text{color:#94a3b8;font-size:.92rem;line-height:1.6}
.fc-chip{display:inline-block;padding:3px 11px;border-radius:999px;background:rgba(94,234,212,.1);color:#5eead4;
  font-size:.76rem;margin:8px 6px 0 0;transition:transform .2s ease,background .2s ease}
.fc-chip:hover{transform:translateY(-2px);background:rgba(94,234,212,.22)}
.fc-chip.next{background:rgba(251,146,60,.14);color:#fb923c}

.fc-prog{height:6px;border-radius:999px;background:#1f2a3d;margin:10px 0 14px;overflow:hidden}
.fc-prog span{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#5eead4,#3b82f6);
  transition:width .6s cubic-bezier(.4,0,.2,1)}
.fc-detail{display:flex;gap:18px;align-items:flex-start;background:#111a2b;border:1px solid #1f2a3d;
  border-radius:16px;padding:22px;animation-duration:.45s;animation-fill-mode:both;animation-timing-function:ease}
.fc-detail-icon{font-size:2.6rem;line-height:1}
.fc-detail-title{font-weight:700;font-size:1.2rem;color:#f8fafc;margin-bottom:6px}
.fc-detail-text{color:#cbd5e1;line-height:1.6;margin-bottom:8px}
.fc-detail-why{color:#94a3b8;line-height:1.6}
.fc-detail-why b{color:#5eead4}

.fc-grid .fc-card{animation:fcUp .5s ease both}
.fc-grid .fc-card:nth-child(2){animation-delay:.08s}.fc-grid .fc-card:nth-child(3){animation-delay:.16s}
.fc-grid .fc-card:nth-child(4){animation-delay:.24s}

@supports (animation-timeline: view()){
  .fc-tl-item{animation:fcUp linear both;animation-timeline:view();animation-range:entry 0% entry 55%}
}
@media (max-width:640px){
  .fc-detail{flex-direction:column;gap:8px}
  .fc-tl{padding-left:30px}
  .fc-tl-dot{left:-30px}
  .fc-tl::before{left:5px}
}
@media (prefers-reduced-motion:reduce){
  .fc-story-hero,.fc-tl-item,.fc-tl-dot,.fc-detail,.fc-grid .fc-card{animation:none !important}
  .fc-tl-card,.fc-chip,.fc-prog span{transition:none !important}
}
"""

JOURNEY = [
    ("💡", "The idea",
     "Many people train alone, with no coach to say whether their form is right. Poor form slows progress and can "
     "cause injuries. FlexCheck started with one question: can an ordinary webcam do a coach's first job?",
     ["Problem", "Research"], False),
    ("🦴", "Seeing the body",
     "MediaPipe Pose finds 33 body landmarks in every video frame using only a normal webcam. "
     "No wearables and no special sensors.",
     ["MediaPipe", "WebRTC", "OpenCV"], False),
    ("📐", "Turning points into meaning",
     "Landmarks become joint angles (knee, hip, elbow, shoulder, back). Each exercise has its own detector "
     "with rules for depth, alignment and range of motion.",
     ["Joint angles", "5 exercise detectors"], False),
    ("🔢", "Counting honest reps",
     "A small state machine follows the movement (up, down, up) and counts a rep only when the full range "
     "is reached. Jitter and half reps are ignored.",
     ["State machine", "Depth check"], False),
    ("🗣️", "A coach that talks",
     "At key moments (start, set complete, form issue) an AI model writes a short coaching line and a "
     "text-to-speech voice says it aloud.",
     ["Groq LLM", "gTTS voice"], False),
    ("📊", "Tracking progress",
     "Every workout is saved. Streaks, calories, BMI, the weekly planner and charts turn single sessions "
     "into a long-term habit.",
     ["SQLite", "Plotly", "Streamlit"], False),
    ("🚀", "Next: squat form classifier",
     "The next milestone is classifying squat posture (correct, shallow, forward lean, knees caving in) "
     "from joint-angle features.",
     ["Planned"], True),
]

PIPELINE = [
    ("📷", "Camera", "Live video comes in",
     "Your browser sends live video to the app through WebRTC. Any laptop or phone camera works.",
     "No equipment is needed, so you can train at home.", ["WebRTC", "Webcam"]),
    ("🦴", "Pose", "33 landmarks per frame",
     "MediaPipe finds shoulders, elbows, hips, knees, ankles and more, on every frame.",
     "It sees your whole body position, which a single photo or a timer cannot.", ["MediaPipe"]),
    ("📐", "Angles", "Points become angles",
     "Three landmarks make an angle, for example hip, knee and ankle give the knee angle.",
     "Angles are the language of good form: depth, back alignment and balance.", ["Geometry", "NumPy"]),
    ("🔢", "Reps and form", "Counting and checking",
     "A state machine counts reps. Simple rules check depth, posture and range of motion.",
     "You get honest counts and an instant signal when your form slips.", ["State machine"]),
    ("🗣️", "Coach", "Spoken guidance",
     "Short tips are generated at the right moments and spoken aloud.",
     "You keep your eyes on the movement instead of the screen.", ["Groq LLM", "gTTS"]),
    ("📊", "Progress", "Saved and charted",
     "Results go into your account: history, streaks, calories, BMI and your weekly plan.",
     "Seeing trends keeps you consistent, and consistency is what changes your body.", ["SQLite", "Plotly"]),
]

GUIDE = {
    "🎬 Before": [
        ("📍", "Show your whole body", "Stand 2 to 3 metres from the camera so your head and feet are both visible."),
        ("💡", "Use good light", "Face the light. Avoid a bright window behind you."),
        ("👕", "Wear fitted clothes", "Loose clothes hide your joints, so tracking gets less accurate."),
        ("🎯", "Plan your session", "Pick the exercise, sets and reps in the Workout sidebar first."),
    ],
    "💪 During": [
        ("🐢", "Slow and controlled", "Fast reps confuse tracking and raise injury risk."),
        ("👂", "Listen to the coach", "Fix one thing at a time instead of changing everything."),
        ("🫁", "Breathe", "Breathe out on the effort and in on the way back."),
        ("🛑", "Stop if it hurts", "Muscle burn is normal. Sharp or joint pain is not."),
    ],
    "📈 After": [
        ("🗂️", "Check your history", "Look at reps and sets across days, not just today."),
        ("📅", "Update your plan", "Add a rep or a set when the current plan feels easy."),
        ("😴", "Recover", "Sleep and rest days are when your body actually improves."),
        ("⚖️", "Log your weight weekly", "Use the Body & BMI tab to track your progress."),
    ],
}


def chips(items, next_=False):
    cls = "fc-chip next" if next_ else "fc-chip"
    return "".join(f'<span class="{cls}">{c}</span>' for c in items)


def timeline_html():
    out = ""
    for icon, title, text, tags, nxt in JOURNEY:
        out += (
            f'<div class="fc-tl-item"><div class="fc-tl-dot"></div><div class="fc-tl-card">'
            f'<div class="fc-tl-title">{icon} {title}</div><div class="fc-tl-text">{text}</div>'
            f'{chips(tags, nxt)}</div></div>'
        )
    return f'<div class="fc-tl">{out}</div>'


def cards_html(items):
    return '<div class="fc-grid">' + "".join(
        f'<div class="fc-card"><div class="fc-card-icon">{i}</div><div class="fc-card-title">{t}</div>'
        f'<div class="fc-card-text">{d}</div></div>' for i, t, d in items
    ) + "</div>"


render_topbar()
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
uid = st.session_state["user_id"]

tab_story, tab_hist = st.tabs(["🛠️ How FlexCheck is built", "📜 My workout history"])

# ======================= STORY =======================
with tab_story:
    st.markdown(
        '<div class="fc-story-hero"><h2>From a webcam to a personal coach</h2>'
        '<p>FlexCheck turns an ordinary camera into a form-checking, rep-counting training partner. '
        'Here is how it was built, and how to get the most out of it.</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        cards_html([
            ("🧍", "No coach nearby", "Most people train alone and never get feedback."),
            ("🔍", "Mistakes stay hidden", "Small form errors are hard to see on yourself."),
            ("📉", "Progress is invisible", "Without records, it is hard to stay consistent."),
        ]),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="fc-sec">The development journey</div>'
                '<p class="fc-sec-sub">Each step builds on the one before it.</p>', unsafe_allow_html=True)
    st.markdown(timeline_html(), unsafe_allow_html=True)

    st.markdown('<div class="fc-sec">How one rep becomes feedback</div>'
                '<p class="fc-sec-sub">Tap a stage to explore the pipeline.</p>', unsafe_allow_html=True)
    labels = [f"{p[0]} {p[1]}" for p in PIPELINE]
    choice = st.pills("Pipeline stage", labels, default=labels[0], label_visibility="collapsed", key="pipe_stage")
    i = labels.index(choice) if choice in labels else 0
    icon, _, title, what, why, tags = PIPELINE[i]
    pct = round((i + 1) / len(PIPELINE) * 100)
    anim = "fcSlideA" if i % 2 else "fcSlideB"  # alternating names restart the animation on each change
    st.markdown(
        f'<div class="fc-prog"><span style="width:{pct}%"></span></div>'
        f'<div class="fc-detail" style="animation-name:{anim}"><div class="fc-detail-icon">{icon}</div><div>'
        f'<div class="fc-detail-title">{title}</div><div class="fc-detail-text">{what}</div>'
        f'<div class="fc-detail-why"><b>Why it helps your training:</b> {why}</div>{chips(tags)}</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="fc-sec">Train better on your own</div>'
                '<p class="fc-sec-sub">A simple routine for every session.</p>', unsafe_allow_html=True)
    g_tabs = st.tabs(list(GUIDE))
    for tab, items in zip(g_tabs, GUIDE.values()):
        with tab:
            st.markdown(cards_html(items), unsafe_allow_html=True)

    st.markdown("&nbsp;", unsafe_allow_html=True)
    if st.button("🚀  Try it now", key="story_cta"):
        st.switch_page("views/workout.py")

# ======================= MY HISTORY =======================
with tab_hist:
    rows = get_users_exercises(uid)
    if not rows:
        st.info("No workouts yet. Finish a workout and it will appear here.")
        if st.button("Start a workout", key="hist_start"):
            st.switch_page("views/workout.py")
    else:
        df = pd.DataFrame([
            {"Exercise": r["exercise_name"], "Reps": r["reps"], "Sets": r["sets"],
             "Time (sec)": r["time"], "Date": r["created_at"]} for r in rows
        ])
        local_tz = datetime.now().astimezone().tzinfo
        df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_convert(local_tz).dt.date

        agg = (df.groupby(["Date", "Exercise"], as_index=False)
                 .agg({"Reps": "sum", "Sets": "sum", "Time (sec)": "sum"})
                 .sort_values("Date", ascending=False))

        m1, m2, m3 = st.columns(3)
        m1.metric("Workout days", df["Date"].nunique())
        m2.metric("Total reps", int(df["Reps"].sum()))
        m3.metric("Total minutes", round(df["Time (sec)"].sum() / 60, 1))

        fig = px.bar(agg, x="Date", y="Reps", color="Exercise", title="Reps per day")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=0, r=0, t=40, b=0), height=340, legend_title_text="")
        st.plotly_chart(fig, width="stretch")

        st.dataframe(agg, width="stretch", hide_index=True)