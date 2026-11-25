from src.server.entities import player
from src.server import data
from pathlib import Path
from contextlib import closing
import sqlite3, os

base_path = Path(__file__).parent.resolve()

users_db = os.path.join(base_path, "DB/users.db")

def register_databases():
    with closing(sqlite3.connect(users_db, timeout=10.0)) as db:
        with db:
            db.execute("PRAGMA journal_mode=WAL;")

def create_user(name, password, UID):
    if user_exists(name):
        return {
            "STATUS": 0
        }
    print("creating table")
    with closing(sqlite3.connect(users_db, timeout=10.0)) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT,
                name TEXT,
                password TEXT
            )
        """)
        db.execute("PRAGMA journal_mode=WAL;")
        print("table created, adding user")
        with db:
            db.execute(
                "INSERT INTO users (uid, name, password) VALUES (?, ?, ?)",
                (str(UID), name, password)
            )
    print("Success")
    return {
        "STATUS": 1
    }

def connect_user(name, password):
    data.SESSION_ID += 1
    with sqlite3.connect(users_db) as db:
        with db:
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
                    "player": player.Player(name, 50, 50)
                }
        return {
            "STATUS": 0
        }

def user_exists(name):
    with closing(sqlite3.connect(users_db, timeout=5.0)) as db:
        with db:
            row = db.execute(
                "SELECT uid, password FROM users WHERE name = ?",
                (name,)
            )
            return row.fetchone() is not None

def register_user(un, pw):
    connection = connect_user(un, pw)\
        if user_exists(un) else create_user(un, pw, data.UID + 1)
    print("connection", connection)
    if not connection.get("STATUS"):
        return {
            "STATUS": 0
        }
    data.SESSION_ID += 1
    data.UID += 1
    return {
        "STATUS": 1,
        "player": player.Player(un, 50, 50),
        "SESSION": data.SESSION_ID
    }