import hashlib
import hmac
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


DATABASE_PATH = Path(
    os.getenv(
        "APP_DATABASE_PATH",
        Path(__file__).resolve().parents[2] / "data" / "app.sqlite3",
    )
)


def _connect() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_auth_database() -> None:
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                expires_at TEXT NOT NULL
            );
            """
        )


def _hash_password(password: str, salt: bytes | None = None) -> str:
    actual_salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), actual_salt, 310_000
    )
    return f"pbkdf2_sha256$310000${actual_salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$")
    if algorithm != "pbkdf2_sha256":
        return False
    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt_hex),
        int(iterations),
    )
    return hmac.compare_digest(candidate.hex(), digest_hex)


def create_user(email: str, password: str) -> dict[str, str]:
    initialize_auth_database()
    now = datetime.now(timezone.utc).isoformat()
    try:
        with _connect() as connection:
            cursor = connection.execute(
                "INSERT INTO users(email, password_hash, created_at) VALUES (?, ?, ?)",
                (email.lower(), _hash_password(password), now),
            )
            return {"id": str(cursor.lastrowid), "email": email.lower()}
    except sqlite3.IntegrityError as error:
        raise ValueError("An account with this email already exists.") from error


def create_session(email: str, password: str) -> tuple[str, dict[str, str]]:
    initialize_auth_database()
    with _connect() as connection:
        user = connection.execute(
            "SELECT id, email, password_hash FROM users WHERE email = ?",
            (email.lower(),),
        ).fetchone()
        if user is None or not _verify_password(password, user["password_hash"]):
            raise ValueError("Invalid email or password.")

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        connection.execute(
            "INSERT INTO sessions(token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (token_hash, user["id"], expires_at.isoformat()),
        )
        return token, {"id": str(user["id"]), "email": user["email"]}
