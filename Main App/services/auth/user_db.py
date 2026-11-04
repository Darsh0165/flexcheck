import hashlib
import hmac
import os
import re
import sqlite3
from pathlib import Path

_DB_PATH = str(Path(__file__).parent.parent.parent / "users.db")


def _conn():
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_user_db():
    """Creates users.db and the table if they don't exist."""
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT UNIQUE NOT NULL,
                email         TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt          BLOB NOT NULL,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _hash(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000).hex()


def register_user(username, email, password, confirm):
    if not username or not email or not password:
        return False, "All fields are required."
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
        return False, "Username: 3-20 letters, numbers or underscore."
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if password != confirm:
        return False, "Passwords do not match."

    salt = os.urandom(16)
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
                (username, email, _hash(password, salt), salt),
            )
    except sqlite3.IntegrityError:
        return False, "Username already taken."

    return True, "Account created. Please log in."


def verify_user(username, password):
    """Returns the user row if the credentials match, otherwise None."""
    with _conn() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

    if user is None:
        return None
    if hmac.compare_digest(user["password_hash"], _hash(password, user["salt"])):
        return user
    return None