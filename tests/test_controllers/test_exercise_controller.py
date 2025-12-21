import pytest
from fastapi.testclient import TestClient
from main import app
from api.models.exercise import ExerciseResponse
from api.services.exercise_service import ExerciseService
from fastapi import HTTPException, status
from unittest.mock import AsyncMock
from api.dependencies.repositories import get_exercise_repo
from api.dependencies.auth import get_current_user

@pytest.fixture
def mock_service():
    service = AsyncMock(spec=ExerciseService)
    return service


@pytest.fixture
def client(mock_service):
    original_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_exercise_repo] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: 1
    
    yield TestClient(app)

    app.dependency_overrides = original_overrides

def test_get_all_exercises(client, mock_service):
    # Arrange
    mock_service.get_all_exercises.return_value = [
        ExerciseResponse(
            id=1,
            name="Push Up",
            description="A basic push up exercise",
            category="Strength",
            muscle_group="Chest",
        ),
        ExerciseResponse(
            id=2,
            name="Squat",
            description="A basic squat exercise",
            category="Strength",
            muscle_group="Legs",
        ),
    ]

    # Act
    response = client.get("/exercises")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Push Up"
    assert data[1]["name"] == "Squat"

    mock_service.get_all_exercises.assert_called_once_with(user_id=1)


def test_get_exercise_by_id(client, mock_service):
    # Arrange
    mock_service.get_exercise_by_id.return_value = ExerciseResponse(
        id=1,
        name="Push up",
        description="A basic push up exercise",
        category="Strength",
        muscle_group="Chest",
    )

    # Act
    response = client.get("/exercises/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Push up"
    assert data["id"] == 1
    
    mock_service.get_exercise_by_id.assert_called_once_with(user_id=1, exercise_id=1)


def test_get_exercise_by_id_not_found(client, mock_service):
    # Arrange
    mock_service.get_exercise_by_id.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
    )

    # Act
    response = client.get("/exercises/12")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

    mock_service.get_exercise_by_id.assert_called_once_with(user_id=1, exercise_id=12)