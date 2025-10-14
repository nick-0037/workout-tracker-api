import sqlite3
import os
import hashlib
from datetime import datetime
from api.config import ENV, DB_PATH

def setup_db():
    """Crea la carpeta y configura la base de datos"""
    if ENV == "test":
        return 

    # Crear carpeta database si no existe
    os.makedirs("database", exist_ok=True)

    print(f"📁 Carpeta creada: database/")
    print(f"🗄️  Base de datos: {DB_PATH}")

    return DB_PATH


def connect_db(db_path):
    """Conecta a la base de datos SQLite"""

    try:
        conn = sqlite3.connect(db_path)

        conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre

        print("✅ Conexión a la base de datos exitosa")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None


def create_tables(conn):
    """Crea las tablas iniciales en la base de datos"""

    try:
        # Tabla de usuarios
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

        # tablas de ejercicios (catalogos)
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

        # tabla de rutinas (planes de entrenamiento)
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

        # tabla de ejercicios en rutinas (relación muchos a muchos)
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

        # tabla de sesiones de rutinas (entrenamientos completados - para tracking y reportes)
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

        # tabla de sesiones de ejercicios (ejercicios realizados - para tracking)
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
        print("✅ Tablas creadas exitosamente")

        return conn
    except sqlite3.Error as e:
        print(f"❌ Error al crear las tablas: {e}")
        return None


def send_basic_exercises(conn):
    """Solo ejercicios basicos necesarios"""

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
    print("✅ Ejercicios basicos insertados exitosamente")


def get_db():
    """Dependency to FastAPI: open and close connection per-request"""
    db_path = "database/app.db"
    conn = connect_db(db_path)
    try:
        yield conn
    finally:
        conn.close()


def create_demo_user(conn):
    """Usuario de prueba"""

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
        print("✅ Usuario demo creado exitosamente")
    except sqlite3.IntegrityError:
        print("⚠️  El usuario demo ya existe")


def show_minimal_info(conn):
    """Info básica de la DB"""

    print("\n" + "=" * 40)
    print("📊 BASE DE DATOS CREADA")
    print("=" * 40)

    # Contar usuarios y ejercicios
    users_count = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()[
        "count"
    ]
    exercises_count = conn.execute(
        "SELECT COUNT(*) as count FROM exercises"
    ).fetchone()["count"]

    print(f"👥 Usuarios: {users_count}")
    print(f"🏋️  Ejercicios disponibles: {exercises_count}")

    print(f"\n📋 TABLAS CREADAS:")
    print(f"  • users (authentication)")
    print(f"  • exercises (exercise catalog)")
    print(f"  • workout_plans (user workout plans)")
    print(f"  • workout_plan_exercises (exercises in plans)")
    print(f"  • workout_sessions (completed workouts)")
    print(f"  • session_exercises (progress tracking)")


def main():
    """ "Setup mínimo según requirements"""
    print("🚀 SETUP MÍNIMO - WORKOUT TRACKER")
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

    print(f"\n✅ Setup mínimo completado!")
    print(f"📂 Base de datos: {DB_PATH}")
    print("\n🎯 LISTO PARA:")
    print("  • User auth (sign-up, login, JWT)")
    print("  • Create/update/delete workout plans")
    print("  • Track progress")
    print("  • Generate reports on past workouts")


if __name__ == "__main__":
    main()
