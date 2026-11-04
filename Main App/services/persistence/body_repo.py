from services.persistence.exercise_repository import _get_connection

_DEFAULTS = {
    "height_cm": 170.0,
    "age": 25,
    "sex": "Male",
    "activity": "Light",
    "goal": "Maintain",
    "asian_bmi": 1,
}


def init_body_tables():
    """Adds the new tables to the existing data.db. Safe to run on every page load."""
    conn = _get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                height_cm REAL, age INTEGER, sex TEXT,
                activity TEXT, goal TEXT, asian_bmi INTEGER DEFAULT 1
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS body_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_date TEXT NOT NULL,
                weight_kg REAL, height_cm REAL, bmi REAL,
                UNIQUE (user_id, entry_date)
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schedule_rows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                workout TEXT, day TEXT, sets INTEGER, reps INTEGER
            )""")


# ---------------- profile ----------------
def get_profile(user_id):
    row = _get_connection().execute(
        "SELECT * FROM profiles WHERE user_id = ?", (user_id,)
    ).fetchone()
    profile = dict(_DEFAULTS)
    if row:
        profile.update({k: row[k] for k in _DEFAULTS if row[k] is not None})
    return profile


def save_profile(user_id, **fields):
    p = get_profile(user_id)
    p.update(fields)
    conn = _get_connection()
    with conn:
        conn.execute("""
            INSERT INTO profiles (user_id, height_cm, age, sex, activity, goal, asian_bmi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                height_cm = excluded.height_cm, age = excluded.age, sex = excluded.sex,
                activity = excluded.activity, goal = excluded.goal, asian_bmi = excluded.asian_bmi
        """, (user_id, p["height_cm"], p["age"], p["sex"], p["activity"], p["goal"], int(p["asian_bmi"])))


# ---------------- body metrics ----------------
def add_body_entry(user_id, entry_date, weight_kg, height_cm, bmi):
    """One entry per day. Saving again on the same day updates it."""
    conn = _get_connection()
    with conn:
        conn.execute("""
            INSERT INTO body_metrics (user_id, entry_date, weight_kg, height_cm, bmi)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, entry_date) DO UPDATE SET
                weight_kg = excluded.weight_kg, height_cm = excluded.height_cm, bmi = excluded.bmi
        """, (user_id, entry_date, weight_kg, height_cm, bmi))


def get_body_entries(user_id):
    rows = _get_connection().execute(
        "SELECT entry_date, weight_kg, height_cm, bmi FROM body_metrics "
        "WHERE user_id = ? ORDER BY entry_date", (user_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def latest_weight(user_id):
    row = _get_connection().execute(
        "SELECT weight_kg FROM body_metrics WHERE user_id = ? ORDER BY entry_date DESC LIMIT 1",
        (user_id,),
    ).fetchone()
    return row["weight_kg"] if row else None


# ---------------- schedule ----------------
def get_schedule(user_id):
    rows = _get_connection().execute(
        "SELECT workout, day, sets, reps FROM schedule_rows WHERE user_id = ? ORDER BY id",
        (user_id,),
    ).fetchall()
    return [{"Workout": r["workout"], "Day": r["day"], "Sets": r["sets"], "Reps": r["reps"]} for r in rows]


def replace_schedule(user_id, rows):
    conn = _get_connection()
    with conn:
        conn.execute("DELETE FROM schedule_rows WHERE user_id = ?", (user_id,))
        for r in rows:
            conn.execute(
                "INSERT INTO schedule_rows (user_id, workout, day, sets, reps) VALUES (?, ?, ?, ?, ?)",
                (user_id, r["Workout"], r["Day"], int(r.get("Sets") or 3), int(r.get("Reps") or 10)),
            )


# ---------------- workout time per day (from the existing exercises table) ----------------
def get_daily_exercise_time(user_id):
    rows = _get_connection().execute("""
        SELECT date(created_at, 'localtime') AS d, exercise_name, SUM(time) AS secs
        FROM exercises WHERE user_id = ?
        GROUP BY d, exercise_name
    """, (user_id,)).fetchall()
    return [{"Date": r["d"], "Exercise": r["exercise_name"], "Seconds": r["secs"] or 0} for r in rows]