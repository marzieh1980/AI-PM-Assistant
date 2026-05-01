"""
storage.py  —  SQLite persistence for AI PM Assistant
Tables:
    users          (id, username, password_hash, created_at)
    user_settings  (user_id, model_name, font_size, accent_color, sidebar_color)
    chats          (id, user_id, tab, name, system_prompt, created_at, updated_at)
    messages       (id, chat_id, role, text, created_at)
    uploaded_files (id, chat_id, filename)
    prompts        (id, user_id, tab, name, prompt_text, created_at, updated_at)
"""

import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "aipm_data.db")


def _conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with _conn() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            username     TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at   TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS user_settings (
            user_id       INTEGER PRIMARY KEY REFERENCES users(id),
            model_name    TEXT DEFAULT 'llama-3.2-3b-instruct:2',
            font_size     INTEGER DEFAULT 15,
            accent_color  TEXT DEFAULT '#4F8EF7',
            sidebar_color TEXT DEFAULT '#1C2333'
        );

        CREATE TABLE IF NOT EXISTS chats (
            id            TEXT PRIMARY KEY,
            user_id       INTEGER REFERENCES users(id),
            tab           TEXT NOT NULL,
            name          TEXT NOT NULL,
            system_prompt TEXT DEFAULT '',
            created_at    TEXT DEFAULT (datetime('now')),
            updated_at    TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id    TEXT REFERENCES chats(id) ON DELETE CASCADE,
            role       TEXT NOT NULL,
            text       TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS uploaded_files (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id    TEXT REFERENCES chats(id) ON DELETE CASCADE,
            filename   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS prompts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER REFERENCES users(id),
            tab          TEXT NOT NULL,
            name         TEXT NOT NULL,
            prompt_text  TEXT NOT NULL,
            created_at   TEXT DEFAULT (datetime('now')),
            updated_at   TEXT DEFAULT (datetime('now'))
        );
        """)


# ─── AUTH ────────────────────────────────────────────────
def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def register_user(username: str, password: str) -> dict | None:
    """Returns user dict on success, None if username taken."""
    try:
        with _conn() as con:
            cur = con.execute(
                "INSERT INTO users (username, password_hash) VALUES (?,?)",
                (username.strip(), _hash(password))
            )
            uid = cur.lastrowid
            con.execute("INSERT INTO user_settings (user_id) VALUES (?)", (uid,))
            return {"id": uid, "username": username.strip()}
    except sqlite3.IntegrityError:
        return None


def login_user(username: str, password: str) -> dict | None:
    """Returns user dict on success, None on failure."""
    with _conn() as con:
        row = con.execute(
            "SELECT id, username FROM users WHERE username=? AND password_hash=?",
            (username.strip(), _hash(password))
        ).fetchone()
    return dict(row) if row else None


# ─── SETTINGS ────────────────────────────────────────────
def load_settings(user_id: int) -> dict:
    with _conn() as con:
        row = con.execute(
            "SELECT * FROM user_settings WHERE user_id=?", (user_id,)
        ).fetchone()
    if row:
        return dict(row)
    return {
        "model_name": "llama-3.2-3b-instruct:2",
        "font_size": 15,
        "accent_color": "#4F8EF7",
        "sidebar_color": "#1C2333",
    }


def save_settings(user_id: int, model_name: str, font_size: int,
                  accent_color: str, sidebar_color: str):
    with _conn() as con:
        con.execute("""
            INSERT INTO user_settings (user_id, model_name, font_size, accent_color, sidebar_color)
            VALUES (?,?,?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET
                model_name=excluded.model_name,
                font_size=excluded.font_size,
                accent_color=excluded.accent_color,
                sidebar_color=excluded.sidebar_color
        """, (user_id, model_name, font_size, accent_color, sidebar_color))


# ─── CHATS ───────────────────────────────────────────────
def load_chats(user_id: int) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM chats WHERE user_id=? ORDER BY updated_at DESC",
            (user_id,)
        ).fetchall()
    chats = []
    for row in rows:
        c = dict(row)
        c["messages"]       = load_messages(c["id"])
        c["uploaded_files"] = load_chat_files(c["id"])
        c["upload_db"]      = None   # vector DBs are not persisted to disk
        c["meeting_output"] = ""
        c["risk_output"]    = ""
        chats.append(c)
    return chats


def save_chat(user_id: int, chat: dict):
    now = datetime.now().isoformat()
    with _conn() as con:
        con.execute("""
            INSERT INTO chats (id, user_id, tab, name, system_prompt, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                system_prompt=excluded.system_prompt,
                updated_at=excluded.updated_at
        """, (chat["id"], user_id, chat["tab"], chat["name"],
              chat.get("system_prompt", ""), chat.get("created_at", now), now))


def delete_chat_db(chat_id: str):
    with _conn() as con:
        con.execute("DELETE FROM messages WHERE chat_id=?", (chat_id,))
        con.execute("DELETE FROM uploaded_files WHERE chat_id=?", (chat_id,))
        con.execute("DELETE FROM chats WHERE id=?", (chat_id,))


# ─── MESSAGES ────────────────────────────────────────────
def load_messages(chat_id: str) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT role, text FROM messages WHERE chat_id=? ORDER BY id ASC",
            (chat_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def append_message(chat_id: str, role: str, text: str):
    with _conn() as con:
        con.execute(
            "INSERT INTO messages (chat_id, role, text) VALUES (?,?,?)",
            (chat_id, role, text)
        )
    # update chat timestamp
    with _conn() as con:
        con.execute(
            "UPDATE chats SET updated_at=? WHERE id=?",
            (datetime.now().isoformat(), chat_id)
        )


def clear_messages(chat_id: str):
    with _conn() as con:
        con.execute("DELETE FROM messages WHERE chat_id=?", (chat_id,))


# ─── UPLOADED FILES ──────────────────────────────────────
def load_chat_files(chat_id: str) -> list[str]:
    with _conn() as con:
        rows = con.execute(
            "SELECT filename FROM uploaded_files WHERE chat_id=?", (chat_id,)
        ).fetchall()
    return [r["filename"] for r in rows]


def save_chat_files(chat_id: str, filenames: list[str]):
    with _conn() as con:
        con.execute("DELETE FROM uploaded_files WHERE chat_id=?", (chat_id,))
        for fn in filenames:
            con.execute(
                "INSERT INTO uploaded_files (chat_id, filename) VALUES (?,?)",
                (chat_id, fn)
            )


# ─── PROMPTS ─────────────────────────────────────────────
def load_prompts(user_id: int, tab: str | None = None) -> list[dict]:
    with _conn() as con:
        if tab:
            rows = con.execute(
                "SELECT * FROM prompts WHERE user_id=? AND tab=? ORDER BY name ASC",
                (user_id, tab)
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT * FROM prompts WHERE user_id=? ORDER BY tab, name ASC",
                (user_id,)
            ).fetchall()
    return [dict(r) for r in rows]


def save_prompt(user_id: int, tab: str, name: str, prompt_text: str) -> int:
    now = datetime.now().isoformat()
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO prompts (user_id, tab, name, prompt_text, created_at, updated_at) VALUES (?,?,?,?,?,?)",
            (user_id, tab, name, prompt_text, now, now)
        )
        return cur.lastrowid


def update_prompt(prompt_id: int, name: str, prompt_text: str):
    now = datetime.now().isoformat()
    with _conn() as con:
        con.execute(
            "UPDATE prompts SET name=?, prompt_text=?, updated_at=? WHERE id=?",
            (name, prompt_text, now, prompt_id)
        )


def delete_prompt(prompt_id: int):
    with _conn() as con:
        con.execute("DELETE FROM prompts WHERE id=?", (prompt_id,))


# Initialise on import
init_db()
