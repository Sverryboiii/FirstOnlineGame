from src.server.entities import player
from src.server import data
from pathlib import Path
from contextlib import closing
import sqlite3, os

base_path = Path(__file__).parent.resolve()

users_db = os.path.join(base_path, "DB/users.db")

def register_databases():
    # Users
    with closing(sqlite3.connect(users_db, timeout=10.0)) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT,
                name TEXT,
                password TEXT,
                x SMALLINT,
                y SMALLINT
            )
        """)
        with db:
            db.execute("PRAGMA journal_mode=WAL;")
    print("Successfully created users table...")

def create_user(name, password, UID):
    if user_exists(name):
        return {
            "STATUS": 0
        }
    with closing(sqlite3.connect(users_db, timeout=10.0)) as db:
        db.execute("PRAGMA journal_mode=WAL;")
        with db:
            db.execute(
                "INSERT INTO users (uid, name, password, x, y) VALUES (?, ?, ?, ?, ?)",
                (str(UID), name, password, 100, 100)
            )
    return {
        "STATUS": 1
    }

def save_user(_player: player.Player):
    with closing(sqlite3.connect(users_db, timeout=5.0)) as db:

        with db:

            db.execute(
                f"""
                 UPDATE users
                 SET x = {_player.x},
                     y = {_player.y}
                 WHERE uid={_player.uid}
                """
            )

def connect_user(name, password):
    with sqlite3.connect(users_db) as db:
        with db:
            row = db.execute(
                "SELECT uid, password, x, y FROM users WHERE name = ?",
                (name,)
            ).fetchone()
        if row:
            if row[1] == password:
                return {
                    "STATUS": 1,
                    "UID": row[0],
                    "x": row[2],
                    "y": row[3]
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
    if not connection.get("STATUS"):
        return {
            "STATUS": 0
        }
    data.SESSION_ID += 1
    if connection.get("UID", 0) == 0:
        data.UID += 1
    return {
        "STATUS": 1,
        "player": player.Player(
            uid=str(connection.get("UID", data.UID)),
            username=un,
            x=connection.get("x", 50),
            y=connection.get("y", 50)
        ),
        "SESSION": data.SESSION_ID
    }