import pytest
from unittest.mock import AsyncMock
from api.services.exercise_service import ExerciseService
from api.models.exercise import ExerciseResponse
from api.core.error_handler import AppException

@pytest.fixture
def exercise_service(mock_exercise_repository):
    return ExerciseService(mock_exercise_repository)


@pytest.mark.asyncio
async def test_get_all_exercises(exercise_service, mock_exercise_repository):
    # Arrange
    expected_exercises = [
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

    mock_exercise_repository.get_all_exercises = AsyncMock(
        return_value=expected_exercises
    )

    # Act
    result = await exercise_service.get_all_exercises(user_id=1)

    # Assert
    assert len(result) == 2
    assert result[0].name == "Push Up"
    assert result[1].name == "Squat"
    mock_exercise_repository.get_all_exercises.assert_called_once_with(user_id=1)


@pytest.mark.asyncio
async def test_get_exercise_by_id_success(exercise_service, mock_exercise_repository):
    # Arrange
    expected_exercise = ExerciseResponse(
        id=1,
        name="Push Up",
        description="A basic push up exercise",
        category="Strength",
        muscle_group="Chest",
    )

    mock_exercise_repository.get_exercise_by_id = AsyncMock(
        return_value=expected_exercise
    )

    # Act
    result = await exercise_service.get_exercise_by_id(user_id=1, exercise_id=12)

    # Assert
    assert result.name == "Push Up"
    mock_exercise_repository.get_exercise_by_id.assert_called_once_with(
        user_id=1, exercise_id=12
    )


@pytest.mark.asyncio
async def test_get_exercise_by_id_not_found(exercise_service, mock_exercise_repository):
    # Arrange
    mock_exercise_repository.get_exercise_by_id = AsyncMock(return_value=None)
    exercise_service = ExerciseService(mock_exercise_repository)

    # Act & Assert
    with pytest.raises(AppException) as exc_info:
        await exercise_service.get_exercise_by_id(user_id=1, exercise_id=12)

    assert exc_info.value.code == 404
    mock_exercise_repository.get_exercise_by_id.assert_called_once_with(
        user_id=1, exercise_id=12
    )
