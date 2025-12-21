import pytest
from fastapi.testclient import TestClient
from main import app
from api.models.workout_plan import WorkoutPlanResponse
from api.models.workout_plan_exercise import WorkoutPlanExerciseResponse
from unittest.mock import AsyncMock
from api.controllers.workout_controller import get_service
from api.dependencies.auth import get_current_user
from api.services.workout_service import WorkoutService


@pytest.fixture
def mock_service():
    service = AsyncMock(spec=WorkoutService)
    return service


@pytest.fixture
def client(mock_service):
    original_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: 1

    yield TestClient(app)

    app.dependency_overrides = original_overrides


def test_get_all_workouts(client, mock_service):
    # Arrange
    mock_service.get_all_workout_plans.return_value = [
        WorkoutPlanResponse(id=1, user_id=1, name="Push up", description="desc"),
        WorkoutPlanResponse(id=2, user_id=1, name="Pull up", description="desc2"),
    ]

    # Act
    response = client.get("/workouts")

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data[0]["name"] == "Push up"
    assert data[1]["description"] == "desc2"

    mock_service.get_all_workout_plans.assert_called_once_with(user_id=1)


def test_get_workout_plan_by_id(client, mock_service):
    # Arrange
    mock_service.get_workout_plan_by_id.return_value = WorkoutPlanResponse(
        id=1,
        user_id=1,
        name="Push up",
        description="desc",
    )

    # Act
    response = client.get(
        "/workouts/1",
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["description"] == "desc"

    mock_service.get_workout_plan_by_id.assert_called_once_with(
        workout_plan_id=1, user_id=1
    )


def test_create_workout_plan(client, mock_service):
    # Arrange
    mock_service.create_workout_plan.return_value = WorkoutPlanResponse(
        id=1, user_id=1, name="Leg Day", description="Leg workout"
    )

    # Act
    response = client.post(
        "/workouts",
        json={"name": "Leg Day", "description": "Leg workout"},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["user_id"] == 1
    assert data["name"] == "Leg Day"
    assert data["description"] == "Leg workout"

    mock_service.create_workout_plan.assert_called_once_with(
        user_id=1,
        name="Leg Day",
        description="Leg workout",
    )


def test_update_workout_plan(client, mock_service):
    # Arrange
    mock_service.update_workout_plan.return_value = WorkoutPlanResponse(
        id="1",
        user_id="1",
        name="Updated",
        description="Updated desc",
    )

    # Act
    response = client.patch(
        "/workouts/1",
        json={"name": "Updated", "description": "Updated desc"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["name"] == "Updated"
    assert data["description"] == "Updated desc"

    mock_service.update_workout_plan.assert_called_once_with(
        workout_plan_id=1,
        user_id=1,
        name="Updated",
        description="Updated desc",
    )


def test_delete_workout_plan(client, mock_service):
    # Arrange
    mock_service.delete_workout_plan.return_value = True

    # Act
    response = client.delete("/workouts/1")

    # Assert
    assert response.status_code == 204

    mock_service.delete_workout_plan.assert_called_once_with(
        workout_plan_id=1, user_id=1
    )


def test_add_exercise_to_plan(client, mock_service):
    # Mock service
    mock_service.add_exercise_to_plan.return_value = WorkoutPlanExerciseResponse(
        id=1,
        workout_plan_id="1",
        user_id="1",
        exercise_id=1,
        sets=2,
        reps=8,
        weight=10.0,
    )

    # Act
    response = client.post(
        "/workouts/1/exercises",
        json={"exercise_id": 1, "sets": 2, "reps": 8, "weight": 10.0},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["workout_plan_id"] == 1
    assert data["exercise_id"] == 1

    mock_service.add_exercise_to_plan.assert_called_once()


def test_remove_exercise_from_plan(client, mock_service):
    # Mock service
    mock_service.remove_exercise_from_plan.return_value = True

    # Act
    response = client.delete(
        "/workouts/1/exercises/42",
    )

    # Assert
    assert response.status_code == 204

    mock_service.remove_exercise_from_plan.assert_called_once_with(
        workout_plan_id=1,
        user_id=1,
        exercise_id=42,
    )
