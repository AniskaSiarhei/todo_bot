import sqlite3
from pathlib import Path
from typing import List, Tuple

# todo_bot/
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "todo.db"


class Database:
    def __init__(self):
        self._ensure_db()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _ensure_db(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_task(self, user_id: int, title: str):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO tasks (user_id, title) VALUES (?, ?)",
                (user_id, title)
            )
            conn.commit()

    def get_tasks(self, user_id: int) -> List[Tuple]:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, title, done FROM tasks WHERE user_id = ? ORDER BY id",
                (user_id,)
            )
            return cursor.fetchall()

    def mark_done(self, task_id: int, user_id: int):
        with self._connect() as conn:
            conn.execute(
                "UPDATE tasks SET done = 1 WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            conn.commit()

    def delete_task(self, task_id: int, user_id: int):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            conn.commit()

    def get_active_tasks(self, user_id: int):
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, title FROM tasks WHERE user_id = ? AND done = 0 ORDER BY id",
                (user_id,)
            )
            return cursor.fetchall()

    def get_completed_tasks(self, user_id: int):
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, title FROM tasks WHERE user_id = ? AND done = 1 ORDER BY id",
                (user_id,)
            )
            return cursor.fetchall()

    def delete_completed_tasks(self, user_id: int):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM tasks WHERE user_id = ? AND done = 1",
                (user_id,)
            )
            conn.commit()
