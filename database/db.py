import sqlite3
import os
import hashlib
from api.config import ENV, DB_PATH

def setup_db():
    """Creates the folder and sets up the database"""
    if ENV == "test":
        return 

    # Create database folder if it doesn't exist
    os.makedirs("database", exist_ok=True)

    print(f"📁 Folder created: database/")
    print(f"🗄️  Database: {DB_PATH}")

    return DB_PATH


def connect_db(db_path):
    """Connects to the SQLite database"""

    try:
        conn = sqlite3.connect(db_path)

        conn.row_factory = sqlite3.Row  # Allows column access by name

        print("✅ Database connection successful")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None


def create_tables(conn):
    """Creates the initial tables in the database"""

    try:
        # Users table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Exercises table (catalog)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL,
                muscle_group TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        )

        # Workout plans table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
        )

        # Exercises in workout plans table (many-to-many relationship)
        conn.execute(
            """
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
            )
            """
        )

        # Workout sessions table (completed workouts - for tracking and reports)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_plan_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                scheduled_date TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT DEFAULT 'completed',
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (workout_plan_id) REFERENCES workout_plans (id)
            )
            """
        )

        # Session exercises table (performed exercises - for tracking)
        conn.execute(
            """
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
            )
            """
        )

        conn.commit()
        print("✅ Tables created successfully")

        return conn
    except sqlite3.Error as e:
        print(f"❌ Error creating tables: {e}")
        return None


def send_basic_exercises(conn):
    """Insert only basic necessary exercises"""

    basic_exercises = [
        # STRENGTH
        ("Push-ups", "Bodyweight chest exercise", "strength", "chest"),
        ("Squats", "Lower body exercise", "strength", "legs"),
        ("Pull-ups", "Back exercise", "strength", "back"),
        ("Bench Press", "Chest press", "strength", "chest"),
        ("Deadlift", "Full body lift", "strength", "back"),
        # CARDIO
        ("Running", "Cardio exercise", "cardio", "full_body"),
        ("Cycling", "Low impact cardio", "cardio", "legs"),
        # FLEXIBILITY
        ("Stretching", "Flexibility work", "flexibility", "full_body"),
    ]

    conn.executemany(
        """
        INSERT OR IGNORE INTO exercises (name, description, category, muscle_group)
        VALUES (?, ?, ?, ?)
        
        """,
        basic_exercises,
    )

    conn.commit()
    print("✅ Basic exercises inserted successfully")


def get_db():
    """Dependency for FastAPI: open and close connection per-request"""
    db_path = "database/app.db"
    conn = connect_db(db_path)
    try:
        yield conn
    finally:
        conn.close()


def create_demo_user(conn):
    """Demo user"""

    password_hash = hashlib.sha256("demo123".encode()).hexdigest()
    try:
        conn.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            ("demo", "demo@workout.com", password_hash),
        )

        conn.commit()
        print("✅ Demo user created successfully")
    except sqlite3.IntegrityError:
        print("⚠️  Demo user already exists")


def show_minimal_info(conn):
    """Basic DB info"""

    print("\n" + "=" * 40)
    print("📊 DATABASE CREATED")
    print("=" * 40)

    users_count = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()[
        "count"
    ]
    exercises_count = conn.execute(
        "SELECT COUNT(*) as count FROM exercises"
    ).fetchone()["count"]

    print(f"👥 Users: {users_count}")
    print(f"🏋️  Available exercises: {exercises_count}")

    print(f"\n📋 TABLES CREATED:")
    print(f"  • users (authentication)")
    print(f"  • exercises (exercise catalog)")
    print(f"  • workout_plans (user workout plans)")
    print(f"  • workout_plan_exercises (exercises in plans)")
    print(f"  • workout_sessions (completed workouts)")
    print(f"  • session_exercises (progress tracking)")


def main():
    """Minimal setup according to requirements"""
    print("🚀 MINIMAL SETUP - WORKOUT TRACKER")
    print("-" * 40)

    if ENV != "test":
        setup_db()
    
    conn = connect_db(DB_PATH)
    if conn is None:
        return

    conn = create_tables(conn)
    if conn is None:
        return

    send_basic_exercises(conn)

    create_demo_user(conn)

    show_minimal_info(conn)

    conn.close()

    print(f"\n✅ Minimal setup completed!")
    print(f"📂 Database: {DB_PATH}")
    print("\n🎯 READY FOR:")
    print("  • User auth (sign-up, login, JWT)")
    print("  • Create/update/delete workout plans")
    print("  • Track progress")
    print("  • Generate reports on past workouts")


if __name__ == "__main__":
    main()