CATEGORY_COLORS = {
    "Underweight": "#38bdf8",
    "Normal": "#22c55e",
    "Overweight": "#f59e0b",
    "Obese": "#ef4444",
}


def calculate_bmi(weight_kg, height_cm):
    h = height_cm / 100
    return round(weight_kg / (h * h), 1)


def bmi_cutoffs(asian=True):
    """(underweight below, overweight from, obese from)"""
    return (18.5, 23.0, 25.0) if asian else (18.5, 25.0, 30.0)


def bmi_category(bmi, asian=True):
    low, over, obese = bmi_cutoffs(asian)
    if bmi < low:
        return "Underweight"
    if bmi < over:
        return "Normal"
    if bmi < obese:
        return "Overweight"
    return "Obese"


def healthy_weight_range(height_cm, asian=True):
    h = height_cm / 100
    low, over, _ = bmi_cutoffs(asian)
    return round(low * h * h, 1), round((over - 0.1) * h * h, 1)