import pytest
from unittest.mock import AsyncMock
from api.repositories.user_repository import UserRepository
from api.repositories.workout_repository import WorkoutRepository
from api.repositories.workout_session_repository import ScheduledSessionRepository
from api.repositories.exercise_repository import ExerciseRepository
from api.repositories.report_repository import ReportRepository
from database.db import connect_db, create_tables_sync
from api.config import DB_PATH
import pytest_asyncio


def _mock_repository(cls):
    """Factory function that returns a new asynchronous mock repository."""
    return AsyncMock(spec=cls)


@pytest.fixture
def mock_user_repository():
    return _mock_repository(UserRepository)


@pytest.fixture
def mock_exercise_repository():
    return _mock_repository(ExerciseRepository)


@pytest.fixture
def mock_workout_repository():
    return _mock_repository(WorkoutRepository)


@pytest.fixture
def mock_session_repository():
    return _mock_repository(ScheduledSessionRepository)


@pytest.fixture
def mock_report_repository():
    return _mock_repository(ReportRepository)


@pytest_asyncio.fixture
async def test_db_session():
    conn = await connect_db(DB_PATH)

    await create_tables_sync(conn)

    yield conn

    await conn.close()


@pytest.fixture
def real_report_repo(test_db_session):
    return ReportRepository(db=test_db_session)


@pytest.fixture
def real_exercise_repo(test_db_session):
    return ExerciseRepository(db=test_db_session)

@pytest.fixture
def real_user_repo(test_db_session):
    return UserRepository(db=test_db_session)

@pytest.fixture
def real_workout_repo(test_db_session):
    return WorkoutRepository(db=test_db_session)


pytest_plugins = ("pytest_asyncio",)
