import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from main import app
from api.models.scheduled_workout import ScheduledWorkoutResponse
from api.dependencies.auth import get_current_user
from api.controllers.scheduled_workout_controller import get_service
from datetime import datetime
from api.services.scheduled_workout_service import ScheduledWorkoutService


@pytest.fixture
def mock_service():
    service = AsyncMock(spec=ScheduledWorkoutService)
    return service


@pytest.fixture
def client(mock_service):
    original_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: 1

    yield TestClient(app)

    app.dependency_overrides = original_overrides


def test_create_scheduled_workout_success(client, mock_service):
    # Arrange
    payload = {"workout_plan_id": 3, "scheduled_date": "2024-01-04T12:00:00"}

    mock_service.schedule_workout.return_value = ScheduledWorkoutResponse(
        id=10,
        workout_plan_id=3,
        user_id=1,
        scheduled_date="2024-01-04T12:00:00",
    )

    # Act
    response = client.post("/scheduled-workouts", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 10
    assert data["workout_plan_id"] == 3

    mock_service.schedule_workout.assert_called_once_with(
        user_id=1, workout_plan_id=3, scheduled_date=datetime(2024, 1, 4, 12, 0)
    )


def test_list_scheduled_workouts_success(client, mock_service):
    # Arrange
    mock_service.list_scheduled_workouts.return_value = [
        ScheduledWorkoutResponse(
            id=10,
            workout_plan_id=1,
            user_id=1,
            scheduled_date="2024-01-01T10:00:00",
            status="pending",
        ),
        ScheduledWorkoutResponse(
            id=11,
            workout_plan_id=2,
            user_id=1,
            scheduled_date="2024-01-03T18:00:00",
            status="active",
        ),
    ]

    # Act
    response = client.get("/scheduled-workouts")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for s in data:
        print(f"------", s)

    assert len(data) == 2
    assert data[0]["id"] == 10

    mock_service.list_scheduled_workouts.assert_called_once_with(user_id=1)
