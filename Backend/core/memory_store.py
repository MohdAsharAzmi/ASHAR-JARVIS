
import os
import sqlite3

from datetime import datetime, timezone
from contextlib import contextmanager


# Database location
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.getenv(
    "JARVIS_DATA_DIR",
    os.path.join(BASE_DIR, "data")
)

DB_PATH = os.path.join(
    DATA_DIR,
    "jarvis_memory.db"
)


@contextmanager
def database():

    os.makedirs(DATA_DIR, exist_ok=True)

    connection = sqlite3.connect(
        DB_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def initialize_database():

    with database() as db:

        db.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_memory(content):

    content = content.strip()

    if not content:
        raise ValueError("Memory cannot be empty")

    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    with database() as db:

        cursor = db.execute(
            """
            INSERT INTO memories (content, created_at)
            VALUES (?, ?)
            """,
            (content, created_at)
        )

        memory_id = cursor.lastrowid

    return {
        "id": memory_id,
        "content": content,
        "created_at": created_at
    }


def get_memories(limit=50):

    with database() as db:

        rows = db.execute(
            """
            SELECT * FROM memories
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [dict(row) for row in rows]


def search_memories(query, limit=50):

    query = query.strip()

    if not query:
        return []

    with database() as db:

        rows = db.execute(
            """
            SELECT * FROM memories
            WHERE content LIKE ?
            ORDER BY id DESC
            LIMIT ?
            """,
            ("%" + query + "%", limit)
        ).fetchall()

    return [dict(row) for row in rows]


def delete_memory(memory_id):

    with database() as db:

        cursor = db.execute(
            "DELETE FROM memories WHERE id = ?",
            (memory_id,)
        )

        deleted = cursor.rowcount > 0

    return deleted


# Initialize database
initialize_database()
