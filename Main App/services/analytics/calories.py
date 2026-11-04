# Approximate MET values (Compendium of Physical Activities). They are estimates.
MET = {
    "Squats": 5.0,
    "Push-ups": 6.0,
    "Biceps Curls (Dumbbell)": 3.5,
    "Shoulder Press": 4.0,
    "Lunges": 5.0,
}


def estimate_kcal(exercise, seconds, weight_kg):
    """kcal = MET x weight (kg) x hours"""
    met = MET.get(exercise, 4.5)
    return round(met * weight_kg * (seconds or 0) / 3600, 1)