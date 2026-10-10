import hashlib
import hmac
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from app.database.core import connect
from app.database.persistence import initialize_persistence_database


def initialize_auth_database() -> None:
    with connect() as connection:
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
                user_id INTEGER NOT NULL,
                expires_at TEXT NOT NULL,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );
            """
        )
    initialize_persistence_database()


def _hash_password(
    password: str,
    salt: bytes | None = None
) -> str:

    actual_salt = (
        salt
        if salt is not None
        else secrets.token_bytes(16)
    )

    iterations = 310_000

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        actual_salt,
        iterations
    )

    return (
        f"pbkdf2_sha256$"
        f"{iterations}$"
        f"{actual_salt.hex()}$"
        f"{digest.hex()}"
    )


def _verify_password(
    password: str,
    stored_hash: str
) -> bool:

    try:
        (
            algorithm,
            iterations,
            salt_hex,
            digest_hex
        ) = stored_hash.split("$")

    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt_hex),
        int(iterations)
    )

    return hmac.compare_digest(
        candidate.hex(),
        digest_hex
    )


def create_user(
    email: str,
    password: str
) -> dict[str, str]:

    initialize_auth_database()

    email = email.strip().lower()

    now = datetime.now(
        timezone.utc
    ).isoformat()

    try:
        with connect() as connection:

            cursor = connection.execute(
                """
                INSERT INTO users(
                    email,
                    password_hash,
                    created_at
                )
                VALUES (?, ?, ?)
                RETURNING id
                """,
                (
                    email,
                    _hash_password(password),
                    now
                ),
            )

            return {
                "id": str(cursor.fetchone()["id"]),
                "email": email
            }

    except Exception as error:

        # sqlite UNIQUE constraint
        if "UNIQUE constraint failed" in str(error):
            raise ValueError(
                "An account with this email already exists."
            ) from error

        raise


def create_session(
    email: str,
    password: str
) -> tuple[str, dict[str, str]]:

    initialize_auth_database()

    email = email.strip().lower()

    with connect() as connection:

        user = connection.execute(
            """
            SELECT
                id,
                email,
                password_hash
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        if not _verify_password(
            password,
            user["password_hash"]
        ):
            raise ValueError(
                "Invalid email or password."
            )

        # Raw token returned to the client
        token = secrets.token_urlsafe(32)

        # Only the hash is stored in the database
        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(days=7)
        )

        connection.execute(
            """
            INSERT INTO sessions(
                token_hash,
                user_id,
                expires_at
            )
            VALUES (?, ?, ?)
            """,
            (
                token_hash,
                user["id"],
                expires_at.isoformat()
            ),
        )

        return token, {
            "id": str(user["id"]),
            "email": user["email"]
        }


def get_user_from_token(
    token: str
) -> dict[str, str] | None:

    initialize_auth_database()

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    with connect() as connection:

        session = connection.execute(
            """
            SELECT
                users.id,
                users.email,
                sessions.expires_at
            FROM sessions
            JOIN users
                ON users.id = sessions.user_id
            WHERE sessions.token_hash = ?
            """,
            (token_hash,),
        ).fetchone()

        if session is None:
            return None

        expires_at = datetime.fromisoformat(
            session["expires_at"]
        )

        now = datetime.now(
            timezone.utc
        )

        if expires_at <= now:

            connection.execute(
                """
                DELETE FROM sessions
                WHERE token_hash = ?
                """,
                (token_hash,),
            )

            return None

        return {
            "id": str(session["id"]),
            "email": session["email"]
        }


def delete_session(
    token: str
) -> None:

    initialize_auth_database()

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    with connect() as connection:

        connection.execute(
            """
            DELETE FROM sessions
            WHERE token_hash = ?
            """,
            (token_hash,),
        )
