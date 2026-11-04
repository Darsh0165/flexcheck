import streamlit as st

from ui.topbar import render_topbar

# ---- edit these two lines to show your own details ----
PROJECT_BY = "Your Name"
CONTACT = "your.email@example.com"

CSS = """
@keyframes fcUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}

.fc-about-hero{border:1px solid #1f2a3d;border-radius:16px;padding:clamp(28px,5vw,52px);margin-bottom:20px;
  background:radial-gradient(circle at 80% 0%,rgba(59,130,246,.14),#111a2b 70%);animation:fcUp .7s ease both}
.fc-about-hero h2{margin:0 0 10px;padding:0;font-size:clamp(1.7rem,4vw,2.5rem);color:#f8fafc}
.fc-about-hero p{margin:0;color:#cbd5e1;max-width:700px;line-height:1.65}

.fc-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:0 0 8px}
.fc-stat{background:#111a2b;border:1px solid #1f2a3d;border-radius:14px;padding:16px;text-align:center;
  animation:fcUp .5s ease both;transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease}
.fc-stat:nth-child(2){animation-delay:.08s}.fc-stat:nth-child(3){animation-delay:.16s}.fc-stat:nth-child(4){animation-delay:.24s}
.fc-stat:hover{transform:translateY(-4px);border-color:#5eead4;box-shadow:0 8px 24px -8px rgba(94,234,212,.35)}
.fc-stat-num{font-size:2rem;font-weight:800;color:#5eead4;line-height:1.1}
.fc-stat-label{color:#94a3b8;font-size:.85rem;margin-top:4px}

.fc-sec{margin:28px 0 8px;font-size:1.4rem;font-weight:700;color:#f8fafc}
.fc-sec-sub{color:#94a3b8;margin:0 0 14px}
.fc-chip{display:inline-block;padding:4px 12px;border-radius:999px;background:rgba(94,234,212,.1);color:#5eead4;
  font-size:.8rem;margin:0 8px 8px 0;transition:transform .2s ease,background .2s ease}
.fc-chip:hover{transform:translateY(-2px);background:rgba(94,234,212,.22)}

.fc-grid .fc-card{animation:fcUp .5s ease both}
.fc-grid .fc-card:nth-child(2){animation-delay:.08s}.fc-grid .fc-card:nth-child(3){animation-delay:.16s}

.fc-contact{margin-top:26px;background:#111a2b;border:1px solid #1f2a3d;border-radius:14px;padding:18px 20px;
  color:#cbd5e1;line-height:1.7;animation:fcUp .5s ease both}
.fc-contact b{color:#f8fafc}

/* ---------- Q&A (st.expander styled) ---------- */
.st-key-faq [data-testid="stExpander"]{
  background:#111a2b;border:1px solid #1f2a3d !important;border-radius:12px !important;margin-bottom:10px;
  overflow:hidden;animation:fcUp .45s ease both;
  transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease,background .2s ease}
.st-key-faq [data-testid="stExpander"]:hover{
  border-color:#2e3e59 !important;background:#162238;transform:translateX(4px);box-shadow:0 6px 20px -6px rgba(0,0,0,.5)}
.st-key-faq [data-testid="stExpander"] details{border:none !important;background:transparent !important}
.st-key-faq [data-testid="stExpander"] summary{padding:.9rem 1rem;font-weight:600;color:#f8fafc}
.st-key-faq [data-testid="stExpanderDetails"]{color:#cbd5e1;line-height:1.7;animation:fcUp .35s ease both}

@media (prefers-reduced-motion:reduce){
  .fc-about-hero,.fc-stat,.fc-grid .fc-card,.fc-contact,.st-key-faq [data-testid="stExpander"],
  .st-key-faq [data-testid="stExpanderDetails"]{animation:none !important}
  .fc-stat,.fc-chip,.st-key-faq [data-testid="stExpander"]{transition:none !important}
}
"""

FAQ = [
    ("General", "What is FlexCheck?",
     "FlexCheck is a web app that uses your webcam to watch your movement, count your reps and give live "
     "form feedback, like a coach who is always available."),
    ("General", "Which exercises are supported?",
     "Squats, push-ups, biceps curls (dumbbell), shoulder press and lunges. A detailed squat posture "
     "classifier is the next planned feature."),
    ("General", "Does FlexCheck replace a personal trainer?",
     "No. It is a helpful guide for training alone, but it is not a substitute for a qualified trainer or "
     "for medical advice. If you have an injury or a health condition, talk to a professional first."),
    ("Using the app", "How do I start a workout?",
     "Go to **Overview** and press **Start Workout**. In the sidebar pick your exercise, sets and reps, "
     "press **Start Workout** again and allow camera access."),
    ("Using the app", "Where should I place my camera?",
     "Place it 2 to 3 metres away so your whole body is visible from head to feet. A side view usually shows "
     "knee, hip and back angles best. Use good light and fitted clothes."),
    ("Using the app", "Why is my rep not being counted?",
     "Usually one of these: you did not reach the full range of motion, part of your body is outside the "
     "frame, the light is poor, or you moved very fast. Slow down and check that your joints are visible."),
    ("Using the app", "How is my streak calculated?",
     "Every day with a saved workout adds 1 to your streak. You can miss up to 2 days in a row and keep it. "
     "Missing a third day in a row resets it."),
    ("Using the app", "How are calories calculated?",
     "FlexCheck estimates calories as MET value x your weight x workout time. It is an estimate, and real "
     "burn varies from person to person. Save your weight in **Body & BMI** for better numbers."),
    ("Using the app", "How do I use the planner and BMI tracker?",
     "Open **Schedule & Analytics**. The Planner tab lets you add and save a weekly plan, Body & BMI tracks "
     "your weight and BMI over time, and Tips gives food and training advice for your goal."),
    ("Privacy & data", "Is my video recorded or saved?",
     "FlexCheck analyses the camera frames to find your body landmarks. What it saves is your workout "
     "results (exercise, sets, reps, time), not your video."),
    ("Privacy & data", "How are passwords stored?",
     "Passwords are never stored as plain text. They are salted and hashed (PBKDF2) before being saved, "
     "so even the database does not contain your real password."),
    ("Privacy & data", "What does the AI coach receive?",
     "Only short text about workout events, such as the exercise name, rep counts or a form issue. "
     "It is used to write a coaching sentence. No video is sent."),
    ("Technical", "Which technologies does FlexCheck use?",
     "Python and Streamlit for the interface, MediaPipe for pose tracking, WebRTC for the live camera, "
     "SQLite for storage, Plotly for charts, and an AI model plus text-to-speech for the voice coach."),
    ("Technical", "Why does it ask for camera permission?",
     "The camera is the only sensor FlexCheck uses. Without it, the app cannot see your movement. "
     "You can block the permission at any time in your browser."),
    ("Technical", "Does it work offline?",
     "Pose tracking and rep counting run inside the app itself, but the AI coach and its voice need an "
     "internet connection. Without them, FlexCheck still counts reps and shows simple text feedback."),
    ("Technical", "What is the squat form classifier?",
     "A planned feature that will label each squat as correct, shallow, forward lean, knees caving in, "
     "heels off the ground or asymmetric, using joint-angle measurements."),
]
CATS = ["All", "General", "Using the app", "Privacy & data", "Technical"]


def cards_html(items):
    return '<div class="fc-grid">' + "".join(
        f'<div class="fc-card"><div class="fc-card-icon">{i}</div><div class="fc-card-title">{t}</div>'
        f'<div class="fc-card-text">{d}</div></div>' for i, t, d in items
    ) + "</div>"


render_topbar()
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

st.markdown(
    '<div class="fc-about-hero"><h2>About FlexCheck</h2>'
    '<p>FlexCheck is an AI workout coach that runs in your browser. It watches your movement through the '
    'webcam, counts your reps, points out form mistakes in real time and keeps a record of your progress, '
    'so you can train alone with more confidence.</p></div>',
    unsafe_allow_html=True,
)

stats = [("5", "Exercises"), ("33", "Body landmarks tracked"), ("0", "Special hardware"), ("Live", "Voice feedback")]
st.markdown(
    '<div class="fc-stats">' + "".join(
        f'<div class="fc-stat"><div class="fc-stat-num">{n}</div><div class="fc-stat-label">{l}</div></div>'
        for n, l in stats) + "</div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="fc-sec">What makes it useful</div>', unsafe_allow_html=True)
st.markdown(
    cards_html([
        ("🎯", "Form-aware", "It checks joint angles, not just movement, so depth and posture matter."),
        ("🧘", "Made for self-training", "No gym, trainer or wearable needed. Just a camera and some space."),
        ("📈", "Built to last", "History, streaks, calories, BMI and a planner keep you consistent."),
    ]),
    unsafe_allow_html=True,
)

st.markdown('<div class="fc-sec">Built with</div>', unsafe_allow_html=True)
st.markdown(
    "".join(f'<span class="fc-chip">{c}</span>' for c in
            ["Python", "Streamlit", "MediaPipe", "WebRTC", "OpenCV", "SQLite", "Plotly", "Groq LLM", "gTTS"]),
    unsafe_allow_html=True,
)

# ======================= Q&A =======================
st.markdown('<div class="fc-sec">Questions & answers</div>'
            '<p class="fc-sec-sub">Pick a category or search for a word.</p>', unsafe_allow_html=True)

c1, c2 = st.columns([2, 1], vertical_alignment="center")
cat = c1.pills("Category", CATS, default="All", label_visibility="collapsed", key="faq_cat") or "All"
query = c2.text_input("Search", placeholder="🔍 Search questions", label_visibility="collapsed", key="faq_q").strip().lower()

items = [
    (c, q, a) for c, q, a in FAQ
    if (cat == "All" or c == cat) and (not query or query in q.lower() or query in a.lower())
]
st.caption(f"Showing {len(items)} of {len(FAQ)} questions")

with st.container(key="faq"):
    if not items:
        st.info("No questions match your search. Try another word or choose All.")
    for _, question, answer in items:
        with st.expander(question):
            st.markdown(answer)

st.markdown(
    f'<div class="fc-contact"><b>Still have a question?</b><br>'
    f'FlexCheck is a project by <b>{PROJECT_BY}</b>. Contact: {CONTACT}<br>'
    f'<span style="color:#94a3b8;font-size:.85rem">General guidance only, not medical advice.</span></div>',
    unsafe_allow_html=True,
)
