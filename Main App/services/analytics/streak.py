from datetime import date

# Streak survives up to this many missed days in a row. A third missed day breaks it.
MAX_MISSED_DAYS = 2


def compute_streak(days, today=None):
    """days: list of dates with a workout, newest first. Returns (streak, done_today)."""
    today = today or date.today()
    if not days:
        return 0, False
    if (today - days[0]).days - 1 > MAX_MISSED_DAYS:
        return 0, False

    streak = 1
    for newer, older in zip(days, days[1:]):
        if (newer - older).days - 1 > MAX_MISSED_DAYS:
            break
        streak += 1
    return streak, days[0] == today


def get_streak(user_id):
    from services.persistence.exercise_repository import _get_connection

    rows = _get_connection().execute(
        """
        SELECT DISTINCT date(created_at, 'localtime') AS d
        FROM exercises WHERE user_id = ? ORDER BY d DESC
        """,
        (user_id,),
    ).fetchall()
    return compute_streak([date.fromisoformat(r["d"]) for r in rows])
