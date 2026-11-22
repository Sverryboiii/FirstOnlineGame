from src.server.entities import player
from src.server import data
from pathlib import Path
import sqlite3, os

base_path = Path(__file__).parent.resolve()

users_db = os.path.join(base_path, "DB/users.db")

def create_user(name, password, UID):
    with sqlite3.connect(users_db) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT,
                name TEXT,
                password TEXT
            )
        """)
        db.execute("INSERT INTO users (uid, name, password) VALUES (?, ?, ?)", (str(UID, name, password)))

def connect_user(name, password):
    data.SESSION_ID += 1
    with sqlite3.connect(users_db) as db:
        row = db.execute(
            "SELECT uid, password FROM users WHERE name = ?",
            (name,)
        ).fetchall()
        if row:
            if row[1] == password:
                return {
                    "STATUS": 1,
                    "UID": row[0],
                    "SESSION": data.SESSION_ID,
                    "player": player.Player(50, 50)
                }
        return {
            "STATUS": 0
        }

def register_user(un, pw):
    data.UID += 1
    data.SESSION_ID += 1
    create_user(data.UID, un, pw)
    return {
        "STATUS": 1,
        "player": player.Player(50, 50),
        "SESSION": data.SESSION_ID
    }