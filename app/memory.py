import sqlite3
from pathlib import Path
from typing import Any

class MemoryStore:
    """SQLite persistence for conversations, facts, tasks and audit events."""
    def __init__(self, database_path: str | Path = "data/remoteai.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.database_path)
        db.row_factory = sqlite3.Row
        return db

    def initialize(self) -> None:
        with self._connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS facts (id INTEGER PRIMARY KEY AUTOINCREMENT, fact TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS audit_events (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, detail TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            """)

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        with self._connect() as db:
            db.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)", (conversation_id, role, content))

    def get_messages(self, conversation_id: str, limit: int = 30) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT role, content, created_at FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT ?", (conversation_id, limit)).fetchall()
        return [dict(row) for row in reversed(rows)]

    def add_fact(self, fact: str) -> int:
        with self._connect() as db:
            return int(db.execute("INSERT INTO facts (fact) VALUES (?)", (fact,)).lastrowid)

    def list_facts(self) -> list[dict[str, Any]]:
        with self._connect() as db:
            return [dict(r) for r in db.execute("SELECT id, fact, created_at FROM facts ORDER BY id DESC").fetchall()]

    def add_task(self, title: str) -> int:
        with self._connect() as db:
            return int(db.execute("INSERT INTO tasks (title) VALUES (?)", (title,)).lastrowid)

    def list_tasks(self) -> list[dict[str, Any]]:
        with self._connect() as db:
            return [dict(r) for r in db.execute("SELECT id, title, status, created_at FROM tasks ORDER BY id DESC").fetchall()]

    def audit(self, action: str, detail: str = "") -> None:
        with self._connect() as db:
            db.execute("INSERT INTO audit_events (action, detail) VALUES (?, ?)", (action, detail))
