import sqlite3
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

DB_PATH = "assistant_memory.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Creates the necessary tables if they don't already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS command_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")


def save_command(command: str) -> None:
    """
    Saves a command to the command history, with the current timestamp.
    """
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO command_history (command, timestamp) VALUES (?, ?)",
        (command, timestamp)
    )

    conn.commit()
    conn.close()
    logger.info(f"Saved command to history: '{command}'")


def get_recent_commands(limit: int = 10) -> list:
    """
    Retrieves the most recent commands from history, newest first.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT command, timestamp FROM command_history ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    results = cursor.fetchall()

    conn.close()
    return results