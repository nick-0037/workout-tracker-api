import sys
import pytest
import sqlite3
from pathlib import Path
from unittest.mock import Mock
from database.db import send_basic_exercises
from api.config import DB_PATH

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_db():
    """Create a test database for the session."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Create tables (copy from database schema)

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

    # Insert some basic exercises for testing
    send_basic_exercises(conn)

    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def mock_user_repository():
    """Mock user repository for service tests."""
    return Mock()


@pytest.fixture
def mock_exercise_repository():
    """Mock exercise repository for service tests."""
    return Mock()


pytest_plugins = ("pytest_asyncio",)
