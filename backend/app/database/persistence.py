import json
from datetime import datetime, timezone

from app.database.core import connect
from app.models.portfolio import Portfolio
from app.models.profile import InvestorProfile


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def initialize_persistence_database() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS investor_profiles (
                user_id INTEGER PRIMARY KEY,
                data_json TEXT NOT NULL,
                calculated_risk_profile_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                cash REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                sector TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS financial_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                target_amount REAL,
                target_date TEXT,
                data_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                calculation_run_id INTEGER,
                content_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS calculation_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                calculation_type TEXT NOT NULL,
                input_json TEXT NOT NULL,
                output_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS rag_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source_url TEXT,
                publisher TEXT,
                published_at TEXT,
                reliability REAL NOT NULL DEFAULT 0.5,
                content TEXT NOT NULL,
                embedding_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def save_profile(user_id: int, profile: InvestorProfile, risk_profile: dict) -> dict:
    initialize_persistence_database()
    now = _now()
    data = profile.model_dump(mode="json")
    with connect() as connection:
        connection.execute(
            """
            INSERT INTO investor_profiles(user_id, data_json, calculated_risk_profile_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                data_json = excluded.data_json,
                calculated_risk_profile_json = excluded.calculated_risk_profile_json,
                updated_at = excluded.updated_at
            """,
            (user_id, json.dumps(data), json.dumps(risk_profile), now, now),
        )
    return {"profile": data, "risk_profile": risk_profile, "updated_at": now}


def get_profile(user_id: int) -> dict | None:
    initialize_persistence_database()
    with connect() as connection:
        row = connection.execute(
            "SELECT data_json, calculated_risk_profile_json, created_at, updated_at FROM investor_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    if row is None:
        return None
    return {
        "profile": json.loads(row["data_json"]),
        "risk_profile": json.loads(row["calculated_risk_profile_json"] or "{}"),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def save_portfolio(user_id: int, name: str, portfolio: Portfolio) -> dict:
    initialize_persistence_database()
    now = _now()
    with connect() as connection:
        cursor = connection.execute(
            "INSERT INTO portfolios(user_id, name, cash, created_at, updated_at) VALUES (?, ?, ?, ?, ?) RETURNING id",
            (user_id, name.strip(), portfolio.cash, now, now),
        )
        portfolio_id = cursor.fetchone()["id"]
        connection.executemany(
            "INSERT INTO positions(portfolio_id, symbol, quantity, price, sector, asset_type) VALUES (?, ?, ?, ?, ?, ?)",
            [(portfolio_id, p.symbol.upper(), p.quantity, p.price, p.sector, p.asset_type) for p in portfolio.positions],
        )
    return get_portfolio(user_id, int(portfolio_id))  # type: ignore[return-value]


def list_portfolios(user_id: int) -> list[dict]:
    initialize_persistence_database()
    with connect() as connection:
        rows = connection.execute(
            "SELECT id FROM portfolios WHERE user_id = ? ORDER BY updated_at DESC, id DESC",
            (user_id,),
        ).fetchall()
    return [get_portfolio(user_id, int(row["id"])) for row in rows]


def get_portfolio(user_id: int, portfolio_id: int) -> dict | None:
    initialize_persistence_database()
    with connect() as connection:
        portfolio = connection.execute(
            "SELECT id, name, cash, created_at, updated_at FROM portfolios WHERE id = ? AND user_id = ?",
            (portfolio_id, user_id),
        ).fetchone()
        if portfolio is None:
            return None
        positions = connection.execute(
            "SELECT symbol, quantity, price, sector, asset_type FROM positions WHERE portfolio_id = ? ORDER BY id",
            (portfolio_id,),
        ).fetchall()
    return {
        "id": portfolio["id"],
        "name": portfolio["name"],
        "portfolio": {
            "cash": portfolio["cash"],
            "positions": [dict(position) for position in positions],
        },
        "created_at": portfolio["created_at"],
        "updated_at": portfolio["updated_at"],
    }


def delete_portfolio(user_id: int, portfolio_id: int) -> bool:
    initialize_persistence_database()
    with connect() as connection:
        result = connection.execute(
            "DELETE FROM portfolios WHERE id = ? AND user_id = ?",
            (portfolio_id, user_id),
        )
    return result.rowcount > 0


def create_conversation(user_id: int, title: str | None = None) -> int:
    initialize_persistence_database()
    now = _now()
    with connect() as connection:
        cursor = connection.execute(
            "INSERT INTO conversations(user_id, title, created_at, updated_at) VALUES (?, ?, ?, ?) RETURNING id",
            (user_id, title, now, now),
        )
        return int(cursor.fetchone()["id"])


def add_message(user_id: int, conversation_id: int, role: str, content: str) -> bool:
    initialize_persistence_database()
    now = _now()
    with connect() as connection:
        allowed = connection.execute(
            "SELECT id FROM conversations WHERE id = ? AND user_id = ?",
            (conversation_id, user_id),
        ).fetchone()
        if allowed is None:
            return False
        connection.execute(
            "INSERT INTO messages(conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (conversation_id, role, content, now),
        )
        connection.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    return True


def get_conversation(user_id: int, conversation_id: int) -> dict | None:
    initialize_persistence_database()
    with connect() as connection:
        conversation = connection.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ? AND user_id = ?",
            (conversation_id, user_id),
        ).fetchone()
        if conversation is None:
            return None
        messages = connection.execute(
            "SELECT role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY id",
            (conversation_id,),
        ).fetchall()
    return {**dict(conversation), "messages": [dict(message) for message in messages]}
