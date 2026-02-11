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
            # Основная таблица
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Проверяем наличие колонки deadline
            cursor = conn.execute("PRAGMA table_info(tasks)")
            columns = [col[1] for col in cursor.fetchall()]

            if "deadline" not in columns:
                conn.execute("""
                    ALTER TABLE tasks
                    ADD COLUMN deadline TEXT
                """)

                print("✅ Column 'deadline' added")

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
            cursor = conn.execute("""
                SELECT id, title, deadline
                FROM tasks
                WHERE user_id = ?
                AND done = 0
                ORDER BY id
            """, (user_id,))

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

    def restore_task(self, task_id: int, user_id: int):
        with self._connect() as conn:
            conn.execute(
                "UPDATE tasks SET done = 0 WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            conn.commit()

    def update_task(self, task_id: int, user_id: int, text: str):
        with self._connect() as conn:
            conn.execute("""
                UPDATE tasks
                SET title = ?
                WHERE id = ? AND user_id = ?
            """, (text, task_id, user_id))

    def get_task_by_id(self, task_id: int, user_id: int):
        with self._connect() as conn:
            cur = conn.execute("""
                SELECT title
                FROM tasks
                WHERE id = ? AND user_id = ?
            """, (task_id, user_id))

            return cur.fetchone()

    def set_deadline(self, task_id: int, user_id: int, deadline: str):
        with self._connect() as conn:
            conn.execute("""
                UPDATE tasks
                SET deadline = ?
                WHERE id = ? AND user_id = ?
            """, (deadline, task_id, user_id))

            conn.commit()

    def get_tasks_with_deadline(self):
        with self._connect() as conn:
            cur = conn.execute("""
                SELECT id, user_id, title, deadline
                FROM tasks
                WHERE done = 0
                AND deadline IS NOT NULL
            """)

            conn.commit()

            return cur.fetchall()


