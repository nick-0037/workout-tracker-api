import pytest
from fastapi.testclient import TestClient
from main import app
from api.models.exercise import ExerciseResponse
from api.services.exercise_service import ExerciseService
from fastapi import HTTPException, status

client = TestClient(app)


def test_get_all_exercise_endpoint(monkeypatch):
    # Mock service
    async def fake_get_all_exercises(self):
        return [
            {
                "id": 1,
                "name": "Push Up",
                "description": "A basic push up exercise",
                "category": "Strength",
                "muscle_group": "Chest",
            },
            {
                "id": 2,
                "name": "Squat",
                "description": "A basic squat exercise",
                "category": "Strength",
                "muscle_group": "Legs",
            },
        ]

    monkeypatch.setattr(ExerciseService, "get_all_exercises", fake_get_all_exercises)

    # Act
    response = client.get("/exercises")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Push Up"
    assert data[1]["name"] == "Squat"


def test_get_exercise_by_id_endpoint(monkeypatch):
    # Mock service
    async def fake_get_exercise_by_id(self, exercise_id):
        return ExerciseResponse(
            id=exercise_id,
            name="Push up",
            description="A basic push up exercise",
            category="Strength",
            muscle_group="Chest",
        )

    monkeypatch.setattr(ExerciseService, "get_exercise_by_id", fake_get_exercise_by_id)

    # Act
    response = client.get("/exercises/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Push up"
    assert data["id"] == 1


def test_get_exercise_by_id_not_found(monkeypatch):
    # Mock service
    async def fake_get_exercise_by_id(self, exercise_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    monkeypatch.setattr(ExerciseService, "get_exercise_by_id", fake_get_exercise_by_id)

    # Act
    response = client.get("/exercises/12")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
