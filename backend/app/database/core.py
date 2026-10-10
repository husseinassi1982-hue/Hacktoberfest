import os
import re
import sqlite3
from pathlib import Path
from typing import Any

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
DATABASE_PATH = Path(os.getenv("APP_DATABASE_PATH", Path(__file__).resolve().parents[2] / "data" / "app.sqlite3"))


def using_postgres() -> bool:
    return DATABASE_URL.startswith(("postgres://", "postgresql://"))


class PostgresConnection:
    def __init__(self, connection: Any):
        self._connection = connection

    def __enter__(self):
        self._connection.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._connection.__exit__(exc_type, exc_value, traceback)

    @staticmethod
    def _sql(sql: str) -> str:
        return sql.replace("?", "%s")

    def execute(self, sql: str, parameters=()):
        return self._connection.execute(self._sql(sql), parameters)

    def executemany(self, sql: str, parameters):
        return self._connection.executemany(self._sql(sql), parameters)

    def executescript(self, script: str):
        normalized = re.sub(r"INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY", script, flags=re.IGNORECASE)
        for statement in normalized.split(";"):
            statement = statement.strip()
            if statement:
                self.execute(statement)


def connect():
    if using_postgres():
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as error:
            raise RuntimeError("DATABASE_URL uses PostgreSQL but psycopg is not installed.") from error
        return PostgresConnection(psycopg.connect(DATABASE_URL, row_factory=dict_row))

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
