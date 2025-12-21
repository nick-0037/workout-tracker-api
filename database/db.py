import sqlite3
import aiosqlite
import os
from api.utils.security import hash_password
from api.config import ENV, DB_PATH
from datetime import datetime

# Register adapters and converters (sync)
sqlite3.register_adapter(datetime, lambda dt: dt.isoformat())
sqlite3.register_converter("timestamp", lambda s: datetime.fromisoformat(s.decode()))


def setup_db():
    """Ensure folder exists and report DB path (sync setup)"""
    if ENV == "test":
        return

    os.makedirs("database", exist_ok=True)
    print(f"📁 Folder created: database/")
    print(f"🗄️  Database: {DB_PATH}")
    return DB_PATH


# ---------- Async runtime connection ----------
async def connect_db(db_path: str):
    """Create and return an active aiosqlite.Connection (async)."""
    try:
        conn = await aiosqlite.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = aiosqlite.Row
        print("✅ Async database connection successful")
        return conn
    except aiosqlite.Error as e:
        print(f"❌ Error connecting to async DB: {e}")
        return None


async def get_db():
    """FastAPI dependency: yield an active aiosqlite.Connection and close it."""
    conn = await connect_db(DB_PATH)
    try:
        yield conn
    finally:
        if conn:
            await conn.close()


# ----------Sync helpers (Used only for migrations/seeding) ----------
def create_tables_sync(conn):
    """Create tables using sync (for initial setup)."""
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL,
                muscle_group TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS workout_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS workout_plan_exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_plan_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                sets INTEGER NOT NULL DEFAULT 1,
                reps INTEGER,
                weight REAL,
                notes TEXT,
                FOREIGN KEY (workout_plan_id) REFERENCES workout_plans (id) ON DELETE CASCADE,
                FOREIGN KEY (exercise_id) REFERENCES exercises (id)
            );
            CREATE TABLE IF NOT EXISTS workout_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_plan_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                scheduled_date TIMESTAMP NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (workout_plan_id) REFERENCES workout_plans (id)
            );
            CREATE TABLE IF NOT EXISTS sessions_exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                sets_completed INTEGER,
                reps_completed INTEGER,
                weight_used REAL,
                notes TEXT,
                FOREIGN KEY (session_id) REFERENCES workout_sessions (id) ON DELETE CASCADE,
                FOREIGN KEY (exercise_id) REFERENCES exercises (id)
            );
            """
        )

        conn.commit()
        print("✅ Tables created successfully (sync)")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error creating tables (sync): {e}")
        return None


def send_basic_exercises_sync(conn):
    basic_exercises = [
        ("Push-ups", "Bodyweight chest exercise", "strength", "chest", 1),
        ("Squats", "Lower body exercise", "strength", "legs", 1),
        ("Pull-ups", "Back exercise", "strength", "back", 1),
        ("Bench Press", "Chest press", "strength", "chest", 1),
        ("Deadlift", "Full body lift", "strength", "back", 1),
        ("Running", "Cardio exercise", "cardio", "full_body", 1),
        ("Cycling", "Low impact cardio", "cardio", "legs", 1),
        ("Stretching", "Flexibility work", "flexibility", "full_body", 1),
    ]

    conn.executemany(
        """
        INSERT OR IGNORE INTO exercises (name, description, category, muscle_group, user_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        basic_exercises,
    )
    conn.commit()
    print("✅ Basic exercises inserted successfully")


def create_demo_user_sync(conn):
    password_hash = hash_password("demo123")
    try:
        conn.execute(
            """
            INSERT OR IGNORE INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            ("demo", "demo@workout.com", password_hash),
        )
        conn.commit()
        print("✅ Demo user created successfully (sync)")
    except sqlite3.IntegrityError:
        print("⚠️  Demo user already exists (sync)")


def show_minimal_info_sync(conn):
    cur = conn.execute("SELECT COUNT(*) as count FROM users")
    users_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) as count FROM exercises")
    exercises_count = cur.fetchone()[0]

    print("\n" + "=" * 40)
    print("📊 DATABASE CREATED (sync)")
    print("=" * 40)
    print(f"👥 Users: {users_count}")
    print(f"🏋️  Available exercises: {exercises_count}")


# ---------- Sync main for setup ----------
def main():
    """Run DB setup/seed synchronously (called as script)."""
    print("🚀 MINIMAL SETUP - WORKOUT TRACKER")
    print("-" * 40)

    if ENV != "test":
        setup_db()

    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row

    conn = create_tables_sync(conn)
    if conn is None:
        return

    send_basic_exercises_sync(conn)
    create_demo_user_sync(conn)
    show_minimal_info_sync(conn)

    conn.close()

    print("\n✅ Minimal setup completed!")
    print(f"📂 Database: {DB_PATH}")


if __name__ == "__main__":
    main()
