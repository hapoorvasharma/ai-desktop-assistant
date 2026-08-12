import sqlite3
from datetime import datetime, date
from utils.logger import get_logger

logger = get_logger(__name__)

DB_PATH = "assistant_memory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    """)

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")


# ---------- Command history ----------

def save_command(command: str) -> None:
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT command, timestamp FROM command_history ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return results


# ---------- Favorite apps ----------

def add_favorite_app(app_name: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO favorite_apps (app_name) VALUES (?)",
            (app_name.lower().strip(),)
        )
        conn.commit()
        logger.info(f"Added favorite app: {app_name}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"App already in favorites: {app_name}")
        return False
    finally:
        conn.close()


def get_favorite_apps() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT app_name FROM favorite_apps")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


# ---------- Preferences ----------

def set_preference(key: str, value: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO preferences (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value)
    )
    conn.commit()
    conn.close()
    logger.info(f"Set preference: {key} = {value}")


def get_preference(key: str, default=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return default


# ---------- To-Do list ----------

def add_todo(task: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO todos (task, completed, created_at) VALUES (?, 0, ?)",
        (task.strip(), timestamp)
    )
    conn.commit()
    conn.close()
    logger.info(f"Added todo: {task}")


def complete_todo(task_keyword: str):
    """
    Marks the first matching, not-yet-completed todo as done.
    Returns the full task text if found, else None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, task FROM todos WHERE completed = 0 AND task LIKE ? LIMIT 1",
        (f"%{task_keyword.strip()}%",)
    )
    row = cursor.fetchone()

    if row:
        todo_id, task_text = row
        cursor.execute("UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,))
        conn.commit()
        logger.info(f"Completed todo: {task_text}")

    conn.close()
    return row[1] if row else None


def uncomplete_todo(task_keyword: str):
    """
    Reverses a completed todo back to not-done.
    Returns the full task text if found, else None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, task FROM todos WHERE completed = 1 AND task LIKE ? LIMIT 1",
        (f"%{task_keyword.strip()}%",)
    )
    row = cursor.fetchone()

    if row:
        todo_id, task_text = row
        cursor.execute("UPDATE todos SET completed = 0 WHERE id = ?", (todo_id,))
        conn.commit()
        logger.info(f"Un-completed todo: {task_text}")

    conn.close()
    return row[1] if row else None


def get_todos() -> list:
    """
    Returns all todos as a list of (id, task, completed) tuples.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM todos ORDER BY id ASC")
    results = cursor.fetchall()
    conn.close()
    return results


# ---------- Habit tracker ----------

def add_habit(habit_name: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO habits (habit_name) VALUES (?)",
            (habit_name.lower().strip(),)
        )
        conn.commit()
        logger.info(f"Added habit: {habit_name}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Habit already exists: {habit_name}")
        return False
    finally:
        conn.close()


def log_habit(habit_name: str) -> bool:
    """
    Logs today's completion of a habit. Returns False if already
    logged today, or if the habit doesn't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM habits WHERE habit_name = ?",
        (habit_name.lower().strip(),)
    )
    habit_row = cursor.fetchone()

    if not habit_row:
        conn.close()
        logger.warning(f"Habit not found: {habit_name}")
        return False

    habit_id = habit_row[0]
    today = date.today().strftime("%Y-%m-%d")

    cursor.execute(
        "SELECT id FROM habit_logs WHERE habit_id = ? AND log_date = ?",
        (habit_id, today)
    )
    already_logged = cursor.fetchone()

    if already_logged:
        conn.close()
        logger.info(f"Habit already logged today: {habit_name}")
        return False

    cursor.execute(
        "INSERT INTO habit_logs (habit_id, log_date) VALUES (?, ?)",
        (habit_id, today)
    )
    conn.commit()
    conn.close()
    logger.info(f"Logged habit: {habit_name}")
    return True


def get_habits() -> list:
    """
    Returns all habits with their total log count, as a list of
    (habit_name, total_count) tuples.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT habits.habit_name, COUNT(habit_logs.id)
        FROM habits
        LEFT JOIN habit_logs ON habits.id = habit_logs.habit_id
        GROUP BY habits.habit_name
    """)
    results = cursor.fetchall()
    conn.close()
    return results