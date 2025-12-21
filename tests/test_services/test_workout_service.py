import pytest
from unittest.mock import AsyncMock
from api.services.workout_service import WorkoutService
from api.models.workout_plan import WorkoutPlanResponse
from api.models.workout_plan_exercise import (
    WorkoutPlanExerciseCreate,
    WorkoutPlanExerciseResponse,
)
from api.core.error_handler import AppException

@pytest.fixture
def workout_service(mock_workout_repository):
    return WorkoutService(mock_workout_repository)


@pytest.mark.asyncio
async def test_get_all_workout_plans(workout_service, mock_workout_repository):
    # Arrange
    user_id = 1
    expected_workout_plan = [
        WorkoutPlanResponse(
            user_id=user_id,
            id=1,
            name="Full Body Workout",
            description="A comprehensive full body workout plan",
        ),
        WorkoutPlanResponse(
            user_id=user_id,
            id=2,
            name="Cardio Blast",
            description="An intense cardio workout plan",
        ),
    ]
    mock_workout_repository.get_all_workout_plans = AsyncMock(
        return_value=expected_workout_plan
    )

    # Act
    result = await workout_service.get_all_workout_plans(user_id)

    # Assert
    assert len(result) == 2
    assert result[0].name == "Full Body Workout"
    mock_workout_repository.get_all_workout_plans.assert_called_once()


@pytest.mark.asyncio
async def test_get_workout_plan_by_id(workout_service, mock_workout_repository):
    # Arrange
    expected_workout_plan = WorkoutPlanResponse(
        user_id=1,
        id=2,
        name="Cardio Blast",
        description="An intense cardio workout plan",
    )

    mock_workout_repository.get_workout_plan_by_id = AsyncMock(
        return_value=expected_workout_plan
    )

    # Act
    result = await workout_service.get_workout_plan_by_id(workout_plan_id=2, user_id=1)

    # Assert
    assert result.id == 2
    assert result.name == "Cardio Blast"


@pytest.mark.asyncio
async def test_get_workout_plan_by_id_not_found(
    workout_service, mock_workout_repository
):
    # Arrange
    mock_workout_repository.get_workout_plan_by_id = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(AppException) as exc_info:
        await workout_service.get_workout_plan_by_id(workout_plan_id=12, user_id=1)

    assert exc_info.value.code == 404
    assert exc_info.value.message == "Workout plan not found"
    mock_workout_repository.get_workout_plan_by_id.assert_called_once_with(
        workout_plan_id=12, user_id=1
    )


@pytest.mark.asyncio
async def test_create_workout_plan_success(workout_service, mock_workout_repository):
    # Arrange
    expected_workout_plan = WorkoutPlanResponse(
        user_id=2,
        id=3,
        name="Strength Training",
        description="A workout plan focused on building strength",
    )

    mock_workout_repository.create_workout_plan = AsyncMock(
        return_value=expected_workout_plan
    )

    # Act
    result = await workout_service.create_workout_plan(
        user_id=2,
        name="Strength Training",
        description="A workout plan focused on building strength",
    )

    # Assert
    assert result.id == 3
    assert result.name == "Strength Training"
    mock_workout_repository.create_workout_plan.assert_called_once()


@pytest.mark.asyncio
async def test_create_workout_plan_failure(workout_service, mock_workout_repository):
    # Arrange
    mock_workout_repository.create_workout_plan = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(AppException) as exc_info:
        await workout_service.create_workout_plan(
            user_id=2,
            name="Strength Training",
            description="A workout plan focused on building strength",
        )

    assert exc_info.value.code == 400
    assert exc_info.value.message == "Failed to create workout plan"
    mock_workout_repository.create_workout_plan.assert_called_once()


@pytest.mark.asyncio
async def test_update_workout_plan_success(workout_service, mock_workout_repository):
    # Arrange
    expected_workout_plan = WorkoutPlanResponse(
        user_id=2,
        id=3,
        name="Updated Strength Training",
        description="An updated workout plan focused on building strength",
    )

    mock_workout_repository.update_workout_plan = AsyncMock(
        return_value=expected_workout_plan
    )

    # Act
    result = await workout_service.update_workout_plan(
        workout_plan_id=3,
        user_id=2,
        name="Updated Strength Training",
        description="An updated workout plan focused on building strength",
    )

    # Assert
    assert result.id == 3
    assert result.name == "Updated Strength Training"
    mock_workout_repository.update_workout_plan.assert_called_once()


@pytest.mark.asyncio
async def test_update_workout_plan_failure(workout_service, mock_workout_repository):
    # Arrange
    mock_workout_repository.update_workout_plan = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(AppException) as exc_info:
        await workout_service.update_workout_plan(
            workout_plan_id=3,
            user_id=2,
            name="Updated Strength Training",
            description="An updated workout plan focused on building strength",
        )

    assert exc_info.value.code == 400
    assert exc_info.value.message == "Failed to update workout plan"
    mock_workout_repository.update_workout_plan.assert_called_once()


@pytest.mark.asyncio
async def test_delete_workout_plan_success(workout_service, mock_workout_repository):
    # Arrange
    mock_workout_repository.delete_workout_plan = AsyncMock(return_value=True)

    # Act
    result = await workout_service.delete_workout_plan(workout_plan_id=3, user_id=2)

    # Assert
    assert result is True
    mock_workout_repository.delete_workout_plan.assert_called_once_with(
        workout_plan_id=3, user_id=2
    )


@pytest.mark.asyncio
async def test_delete_workout_plan_failure(workout_service, mock_workout_repository):
    # Arrange
    mock_workout_repository.delete_workout_plan = AsyncMock(return_value=False)

    # Act & Assert
    with pytest.raises(AppException) as exc_info:
        await workout_service.delete_workout_plan(workout_plan_id=3, user_id=2)

    assert exc_info.value.code == 404
    assert exc_info.value.message == "Workout plan not found"
    mock_workout_repository.delete_workout_plan.assert_called_once_with(
        workout_plan_id=3, user_id=2
    )


@pytest.mark.asyncio
async def test_add_to_exercise_plan_success(workout_service, mock_workout_repository):
    # Arrange
    workout = WorkoutPlanResponse(
        id=1,
        user_id=1,
        name="Push Day",
    )

    exercise_data = WorkoutPlanExerciseCreate(
        exercise_id=2, sets=3, reps=10, weight=50.0
    )

    expected_exercise = WorkoutPlanExerciseResponse(
        id=1,
        workout_plan_id=1,
        exercise_id=2,
        sets=3,
        reps=10,
        weight=50.0,
    )

    mock_workout_repository.get_workout_plan_by_id = AsyncMock(return_value=workout)
    mock_workout_repository.add_exercise_to_plan = AsyncMock(
        return_value=expected_exercise
    )

    # Act
    result = await workout_service.add_exercise_to_plan(
        user_id=1, workout_plan_id=2, exercise_data=exercise_data
    )

    # Assert
    assert result.exercise_id == 2
    assert result.sets == 3
    mock_workout_repository.add_exercise_to_plan.assert_called_once()


@pytest.mark.asyncio
async def test_remove_exercise_from_plan_success(
    workout_service, mock_workout_repository
):
    # Arrange
    workout = WorkoutPlanResponse(
        id=1,
        user_id=1,
        name="Push Day",
    )

    mock_workout_repository.get_workout_plan_by_id = AsyncMock(return_value=workout)
    mock_workout_repository.remove_exercise_from_plan = AsyncMock(return_value=True)

    # Act & Assert
    result = await workout_service.remove_exercise_from_plan(
        user_id=1, workout_plan_id=1, exercise_id=1
    )

    assert result is True
