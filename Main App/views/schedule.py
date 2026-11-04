from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.analytics.bmi import (
    CATEGORY_COLORS, bmi_category, bmi_cutoffs, calculate_bmi, healthy_weight_range,
)
from services.analytics.calories import MET, estimate_kcal
from services.analytics.nutrition import ACTIVITY, GOALS, daily_targets, safe_goal
from services.content.tips import get_tips, starter_plan
from services.persistence.body_repo import (
    add_body_entry, get_body_entries, get_daily_exercise_time, get_profile,
    get_schedule, init_body_tables, latest_weight, replace_schedule, save_profile,
)
from ui.topbar import render_topbar

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def style(fig, height=320):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0), height=height, legend_title_text="",
    )
    return fig


def idx(options, value):
    return options.index(value) if value in options else 0


render_topbar()
init_body_tables()

uid = st.session_state["user_id"]
profile = get_profile(uid)

st.title("Schedule & Analytics")

flash = st.session_state.pop("flash", None)
if flash:
    st.success(flash)

tab_plan, tab_cal, tab_body, tab_tips = st.tabs(
    ["📅 Planner", "🔥 Calories", "⚖️ Body & BMI", "💡 Tips"]
)

# ======================= PLANNER =======================
with tab_plan:
    st.subheader("Weekly workout planner")
    st.caption("Add rows with the + at the bottom of the table, delete rows by selecting them, then press Save.")

    version = st.session_state.get("plan_v", 0)
    df = pd.DataFrame(get_schedule(uid), columns=["Workout", "Day", "Sets", "Reps"])
    df = df.astype({"Sets": "int64", "Reps": "int64"})

    edited = st.data_editor(
        df, num_rows="dynamic", width="stretch", hide_index=True, key=f"planner_{version}",
        column_config={
            "Workout": st.column_config.SelectboxColumn("Workout", options=list(MET), required=True),
            "Day": st.column_config.SelectboxColumn("Day", options=DAYS, required=True),
            "Sets": st.column_config.NumberColumn("Sets", min_value=1, max_value=10, step=1, default=3),
            "Reps": st.column_config.NumberColumn("Reps", min_value=1, max_value=50, step=1, default=10),
        },
    )

    if st.button("💾 Save plan", key="save_plan"):
        clean = edited.dropna(subset=["Workout", "Day"])
        replace_schedule(uid, clean.to_dict("records"))
        st.session_state["plan_v"] = version + 1
        st.session_state["flash"] = "Plan saved."
        st.rerun()

    plan = edited.dropna(subset=["Workout", "Day"]).copy()
    if plan.empty:
        st.info("Your plan is empty. Add a row above, or use the Tips tab to get a starter plan.")
    else:
        plan["Sets"] = plan["Sets"].fillna(0)
        a, b = st.columns(2)
        a.metric("Training days", plan["Day"].nunique())
        b.metric("Total sets per week", int(plan["Sets"].sum()))
        fig = px.bar(plan, x="Day", y="Sets", color="Workout", category_orders={"Day": DAYS})
        st.plotly_chart(style(fig), width="stretch")

# ======================= CALORIES =======================
with tab_cal:
    st.subheader("Calories burned")
    weight = latest_weight(uid)
    if weight is None:
        st.info("No weight saved yet, so 70 kg is used. Save your weight in the Body & BMI tab for better estimates.")
        weight = 70.0

    data = get_daily_exercise_time(uid)
    if not data:
        st.info("Complete a workout to see your calorie charts.")
    else:
        d = pd.DataFrame(data)
        d["kcal"] = [estimate_kcal(e, s, weight) for e, s in zip(d["Exercise"], d["Seconds"])]
        d["Date"] = pd.to_datetime(d["Date"])

        daily = d.groupby("Date")["kcal"].sum()
        daily = daily.reindex(pd.date_range(end=pd.Timestamp.today().normalize(), periods=30), fill_value=0)

        goal_kcal = st.number_input("Daily calorie goal (kcal)", 50, 2000, 300, step=50, key="cal_goal")

        m1, m2, m3 = st.columns(3)
        m1.metric("Today", f"{daily.iloc[-1]:.0f} kcal")
        m2.metric("Last 7 days", f"{daily.iloc[-7:].sum():.0f} kcal")
        m3.metric("Last 30 days", f"{daily.sum():.0f} kcal")

        fig = px.bar(x=daily.index, y=daily.values, labels={"x": "Date", "y": "kcal"}, title="Daily calories")
        fig.add_hline(y=goal_kcal, line_dash="dash", line_color="#fb923c", annotation_text="Goal")
        st.plotly_chart(style(fig), width="stretch")

        c1, c2 = st.columns(2)
        weekly = daily.resample("W").sum()
        fig = px.bar(x=weekly.index, y=weekly.values, labels={"x": "Week ending", "y": "kcal"}, title="Weekly total")
        c1.plotly_chart(style(fig), width="stretch")

        by_ex = d.groupby("Exercise")["kcal"].sum().sort_values()
        fig = px.bar(x=by_ex.values, y=by_ex.index, orientation="h", labels={"x": "kcal", "y": ""}, title="By exercise")
        c2.plotly_chart(style(fig), width="stretch")

    st.caption("Estimate = MET value x your weight x workout time. Real burn varies from person to person.")

# ======================= BODY & BMI =======================
with tab_body:
    st.subheader("BMI calculator and tracker")

    c1, c2 = st.columns(2)
    height = c1.number_input("Height (cm)", 100.0, 230.0, float(profile["height_cm"]), step=0.5, key="bmi_height")
    weight_in = c2.number_input("Weight (kg)", 30.0, 250.0, float(latest_weight(uid) or 70.0), step=0.1, key="bmi_weight")
    asian = st.toggle("Use Asian BMI cut-offs (overweight from 23)", value=bool(profile["asian_bmi"]), key="bmi_asian")

    bmi = calculate_bmi(weight_in, height)
    category = bmi_category(bmi, asian)
    low, over, obese = bmi_cutoffs(asian)

    g1, g2 = st.columns([1, 1], vertical_alignment="center")
    with g1:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=bmi,
            gauge={
                "axis": {"range": [10, 40]}, "bar": {"color": "#e2e8f0"},
                "steps": [
                    {"range": [10, low], "color": CATEGORY_COLORS["Underweight"]},
                    {"range": [low, over], "color": CATEGORY_COLORS["Normal"]},
                    {"range": [over, obese], "color": CATEGORY_COLORS["Overweight"]},
                    {"range": [obese, 40], "color": CATEGORY_COLORS["Obese"]},
                ],
            },
        ))
        st.plotly_chart(style(gauge, 260), width="stretch")
    with g2:
        st.metric("Your BMI", bmi)
        st.markdown(f"**Category:** :{ {'Underweight': 'blue', 'Normal': 'green', 'Overweight': 'orange', 'Obese': 'red'}[category] }[{category}]")
        lo_w, hi_w = healthy_weight_range(height, asian)
        st.caption(f"Healthy weight range for your height: {lo_w} to {hi_w} kg")

    if st.button("💾 Save today's entry", key="save_body"):
        add_body_entry(uid, date.today().isoformat(), weight_in, height, bmi)
        save_profile(uid, height_cm=height, asian_bmi=int(asian))
        st.session_state["flash"] = "Entry saved."
        st.rerun()

    entries = get_body_entries(uid)
    if not entries:
        st.info("Save an entry to start tracking your progress.")
    else:
        e = pd.DataFrame(entries)
        e["entry_date"] = pd.to_datetime(e["entry_date"])
        t1, t2 = st.columns(2)
        fig = px.line(e, x="entry_date", y="weight_kg", markers=True, labels={"entry_date": "Date", "weight_kg": "kg"}, title="Weight")
        t1.plotly_chart(style(fig, 280), width="stretch")
        fig = px.line(e, x="entry_date", y="bmi", markers=True, labels={"entry_date": "Date", "bmi": "BMI"}, title="BMI")
        t2.plotly_chart(style(fig, 280), width="stretch")
        if len(e) < 2:
            st.caption("Save entries on different days to see a trend line.")

# ======================= TIPS =======================
with tab_tips:
    st.subheader("Personal health tips")
    weight = latest_weight(uid)
    if weight is None:
        st.info("Save your height and weight in the Body & BMI tab first.")
    else:
        sexes = ["Male", "Female"]
        activities = list(ACTIVITY)
        a1, a2, a3, a4 = st.columns(4)
        age = a1.number_input("Age", 10, 90, int(profile["age"]), key="tip_age")
        sex = a2.selectbox("Sex", sexes, index=idx(sexes, profile["sex"]), key="tip_sex")
        activity = a3.selectbox("Activity level", activities, index=idx(activities, profile["activity"]), key="tip_activity")
        goal = a4.selectbox("Goal", GOALS, index=idx(GOALS, profile["goal"]), key="tip_goal")
        st.caption("Activity: Light = 1-3 workout days a week, Moderate = 3-5, Very active = 6-7.")

        h = float(profile["height_cm"])
        bmi_now = calculate_bmi(weight, h)
        cat_now = bmi_category(bmi_now, bool(profile["asian_bmi"]))
        goal_used, note = safe_goal(goal, age, cat_now)
        if note:
            st.warning(note)

        t = daily_targets(weight, h, age, sex, activity, goal_used)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Daily calories", f"{t['target_kcal']} kcal")
        k2.metric("Protein", f"{t['protein_g']} g")
        k3.metric("Water", f"{t['water_l']} L")
        k4.metric("Expected change", f"{t['weekly_change_kg']:+} kg/week")
        st.caption(f"Based on BMI {bmi_now} ({cat_now}), BMR {t['bmr']} kcal and maintenance {t['tdee']} kcal.")

        tips = get_tips(cat_now, goal_used)
        if tips["warning"]:
            st.info(tips["warning"])

        f, tr, lf = st.columns(3)
        f.markdown("#### 🥗 Food\n" + "\n".join(f"- {x}" for x in tips["food"]))
        tr.markdown("#### 🏋️ Training\n" + "\n".join(f"- {x}" for x in tips["training"]))
        lf.markdown("#### 😴 Lifestyle\n" + "\n".join(f"- {x}" for x in tips["lifestyle"]))

        b1, b2 = st.columns(2)
        if b1.button("💾 Save my profile", key="save_profile", width="stretch"):
            save_profile(uid, age=int(age), sex=sex, activity=activity, goal=goal)
            st.session_state["flash"] = "Profile saved."
            st.rerun()
        if b2.button("📅 Apply a starter plan to my Planner", key="apply_plan", width="stretch"):
            replace_schedule(uid, starter_plan(goal_used, cat_now))
            st.session_state["plan_v"] = st.session_state.get("plan_v", 0) + 1
            st.session_state["flash"] = "Starter plan added. Open the Planner tab to review it."
            st.rerun()

    st.caption("General guidance, not medical advice. If you have a health condition, are pregnant, "
               "or are underweight, check with a doctor before changing your diet or training.")