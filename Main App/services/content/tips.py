_FOOD = {
    "Lose fat": [
        "Aim for a small daily calorie deficit, not a crash diet.",
        "Fill half your plate with vegetables and add a protein food to every meal.",
        "Cut sugary drinks and deep-fried snacks first. It is the easiest saving.",
        "Prefer whole grains and pulses (oats, brown rice, dal, chana).",
    ],
    "Maintain": [
        "Eat regular meals and keep calories near your daily target.",
        "Include protein in every meal (eggs, dal, curd, paneer, chicken, fish, tofu).",
        "Eat fruit and vegetables every day.",
    ],
    "Build muscle": [
        "Eat slightly above maintenance so your body has energy to build muscle.",
        "Spread protein over 3 to 4 meals and eat a protein food within 2 hours after training.",
        "Add healthy calories: milk, nuts, banana, peanut butter, rice.",
    ],
}

_TRAINING = {
    "Lose fat": [
        "Do your strength sessions 3 to 4 days a week. Muscle helps keep your metabolism up.",
        "Add 20 to 30 minutes of walking on other days.",
        "Squats and lunges use big muscles, so they burn the most calories.",
    ],
    "Maintain": [
        "Train each major muscle group about twice a week.",
        "Mix lower body (squats, lunges), push (push-ups, shoulder press) and arms (curls).",
    ],
    "Build muscle": [
        "Use progressive overload: add a rep or a set every week while keeping good form.",
        "Train each muscle twice a week with 8 to 12 reps and rest 60 to 90 seconds.",
        "Rest days matter. Muscles grow while you recover.",
    ],
}

_LIFESTYLE = [
    "Sleep 7 to 9 hours. Poor sleep increases hunger and slows recovery.",
    "Drink water through the day, especially around workouts.",
    "Weigh yourself once a week at the same time, not every day.",
]

_PLANS = {
    "Lose fat": [("Squats", "Monday", 3, 12), ("Push-ups", "Tuesday", 3, 10),
                 ("Lunges", "Thursday", 3, 12), ("Squats", "Saturday", 3, 15)],
    "Maintain": [("Squats", "Monday", 3, 10), ("Push-ups", "Wednesday", 3, 10),
                 ("Lunges", "Friday", 3, 10), ("Shoulder Press", "Saturday", 3, 10)],
    "Build muscle": [("Squats", "Monday", 4, 10), ("Push-ups", "Tuesday", 4, 10),
                     ("Shoulder Press", "Thursday", 4, 10), ("Lunges", "Friday", 3, 12),
                     ("Biceps Curls (Dumbbell)", "Saturday", 3, 12)],
}


def get_tips(category, goal):
    warning = None
    if category == "Underweight":
        warning = ("Your BMI is in the underweight range. Focus on eating enough and building strength. "
                   "If this is unexpected, talk to a doctor.")
    elif category == "Obese":
        warning = ("Start gently and build up slowly. If you have joint pain, diabetes, high blood pressure "
                   "or a heart condition, check with a doctor before starting.")
    elif category == "Overweight":
        warning = "Start at a comfortable pace and increase gradually. Consistency matters more than intensity."
    return {
        "food": _FOOD[goal],
        "training": _TRAINING[goal],
        "lifestyle": _LIFESTYLE,
        "warning": warning,
    }


def starter_plan(goal, category):
    """Rows for the planner. Fewer sets for beginners in higher BMI categories."""
    easier = category in ("Obese", "Underweight")
    return [
        {"Workout": w, "Day": d, "Sets": max(2, s - 1) if easier else s, "Reps": r}
        for w, d, s, r in _PLANS[goal]
    ]