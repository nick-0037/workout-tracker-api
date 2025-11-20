import pytest
from fastapi.testclient import TestClient
from main import app
from api.models.workout_plan import WorkoutPlanResponse
from api.models.workout_plan_exercise import WorkoutPlanExerciseResponse
from api.services.workout_service import WorkoutService
from jose import jwt
from api.config import SECRET_KEY, ALGORITHM


client = TestClient(app)

token = jwt.encode({"sub": "1"}, SECRET_KEY, algorithm=ALGORITHM)
headers = {"Authorization": f"Bearer {token}"}


def test_get_all_workouts(monkeypatch):
    # Mock service
    async def fake_get_all_workouts(self, user_id):
        return [
            WorkoutPlanResponse(
                id=1, user_id=user_id, name="Push up", description="Push up description"
            ),
            WorkoutPlanResponse(
                id=2, user_id=user_id, name="Pull up", description="Pull up description"
            ),
        ]

    monkeypatch.setattr(WorkoutService, "get_all_workout_plans", fake_get_all_workouts)

    # Act
    response = client.get("/workouts", headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Push up"
    assert data[1]["description"] == "Pull up description"


def test_get_workout_plan_by_id(monkeypatch):
    # Mock service
    async def fake_get_workout_plan_by_id(self, workout_id, user_id):
        return WorkoutPlanResponse(
            id=workout_id,
            user_id=user_id,
            name="Push up",
            description="Push up description",
        )

    monkeypatch.setattr(
        WorkoutService, "get_workout_plan_by_id", fake_get_workout_plan_by_id
    )

    # Act
    response = client.get("/workouts/1", headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["name"] == "Push up"
    assert data["description"] == "Push up description"


def test_create_workout_plan(monkeypatch):
    # Mock service
    async def fake_create_workout_plan(self, user_id, name, description=None):
        return WorkoutPlanResponse(
            id=1,
            user_id=user_id,
            name=name,
            description=description,
        )

    monkeypatch.setattr(WorkoutService, "create_workout_plan", fake_create_workout_plan)

    # Act
    response = client.post(
        "/workouts",
        json={"name": "Leg Day", "description": "Leg workout"},
        headers=headers,
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["name"] == "Leg Day"
    assert data["description"] == "Leg workout"


def test_update_workout_plan(monkeypatch):
    # Mock service
    async def fake_update_workout_plan(
        self, workout_plan_id, user_id, name, description=None
    ):
        return WorkoutPlanResponse(
            id=workout_plan_id,
            user_id=user_id,
            name=name,
            description=description,
        )

    monkeypatch.setattr(WorkoutService, "update_workout_plan", fake_update_workout_plan)

    # Act
    response = client.patch(
        "/workouts/1",
        json={"name": "Updated Plan", "description": "Updated desc"},
        headers=headers,
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["name"] == "Updated Plan"
    assert data["description"] == "Updated desc"


def test_delete_workout_plan(monkeypatch):
    # Mock service
    async def fake_delete_workout_plan(self, workout_plan_id, user_id):
        return True

    monkeypatch.setattr(WorkoutService, "delete_workout_plan", fake_delete_workout_plan)

    # Act
    response = client.delete("/workouts/1", headers=headers)

    # Assert
    assert response.status_code == 204


def test_add_exercise_to_plan(monkeypatch):
    # Mock service
    async def fake_add_exercise_to_plan(self, workout_plan_id, user_id, exercise_data):
        return WorkoutPlanExerciseResponse(
            id=1,
            workout_plan_id=workout_plan_id,
            user_id=user_id,
            exercise_id=exercise_data.exercise_id,
            sets=exercise_data.sets,
            reps=exercise_data.reps,
            weight=exercise_data.weight,
        )

    monkeypatch.setattr(
        WorkoutService, "add_exercise_to_plan", fake_add_exercise_to_plan
    )

    # Act
    response = client.post(
        "/workouts/1/exercises",
        json={"exercise_id": 42, "sets": 3, "reps": 10, "weight": 50.0},
        headers=headers,
    )
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["workout_plan_id"] == 1
    assert data["exercise_id"] == 42
    assert data["sets"] == 3
    assert data["reps"] == 10
    assert data["weight"] == 50.0

def test_remove_exercise_from_plan(monkeypatch):
    # Mock service
    async def fake_remove_exercise_from_plan(self, workout_plan_id, user_id, exercise_data):
        return True

    monkeypatch.setattr(
        WorkoutService, "remove_exercise_from_plan", fake_remove_exercise_from_plan
    )

    # Act
    response = client.delete(
        "/workouts/1/exercises/42",
        headers=headers,
    )
    
    # Assert
    assert response.status_code == 204
