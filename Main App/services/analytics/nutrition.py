ACTIVITY = {
    "Sedentary": 1.2,    # little or no exercise
    "Light": 1.375,      # 1-3 days per week
    "Moderate": 1.55,    # 3-5 days per week
    "Very active": 1.725,  # 6-7 days per week
}
GOALS = ["Lose fat", "Maintain", "Build muscle"]

_ADJUST = {"Lose fat": -400, "Maintain": 0, "Build muscle": 300}
_PROTEIN_PER_KG = {"Lose fat": 1.8, "Maintain": 1.4, "Build muscle": 1.8}
_MIN_KCAL = {"Male": 1500, "Female": 1200}


def safe_goal(goal, age, category):
    """Never suggest a calorie deficit to minors or underweight users."""
    if goal == "Lose fat":
        if age < 18:
            return "Maintain", "Under 18: a calorie deficit is not recommended, so Maintain is used instead."
        if category == "Underweight":
            return "Maintain", "Your BMI is underweight: losing weight is not recommended, so Maintain is used instead."
    return goal, None


def daily_targets(weight_kg, height_cm, age, sex, activity, goal):
    # Mifflin-St Jeor equation
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + (5 if sex == "Male" else -161)
    tdee = bmr * ACTIVITY.get(activity, 1.375)
    target = max(tdee + _ADJUST[goal], _MIN_KCAL.get(sex, 1200))
    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "target_kcal": round(target),
        "protein_g": round(weight_kg * _PROTEIN_PER_KG[goal]),
        "water_l": round(weight_kg * 0.035, 1),
        "weekly_change_kg": round((target - tdee) * 7 / 7700, 2),  # about 7700 kcal per kg
    }