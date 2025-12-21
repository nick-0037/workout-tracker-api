import pytest
from api.models.scheduled_workout import (
    ScheduledWorkoutCreate,
    ScheduledWorkoutResponse,
)
from api.services.scheduled_workout_service import ScheduledWorkoutService
from datetime import datetime


@pytest.fixture
def scheduled_service(mock_session_repository, mock_workout_repository):
    return ScheduledWorkoutService(mock_session_repository, mock_workout_repository)


@pytest.mark.asyncio
async def test_create_scheduled_workout(
    scheduled_service, mock_session_repository, mock_workout_repository
):
    # Arrange
    scheduled_workout = ScheduledWorkoutCreate(
        workout_plan_id=1, scheduled_date=datetime(2024, 1, 1, 10, 0)
    )

    mock_workout_repository.get_workout_plan_by_id.return_value = {"id": 1}

    mock_session_repository.schedule_session.return_value = ScheduledWorkoutResponse(
        id=10,
        workout_plan_id=1,
        user_id=1,
        scheduled_date=scheduled_workout.scheduled_date,
    )

    # Act
    result = await scheduled_service.schedule_workout(
        user_id=1,
        workout_plan_id=scheduled_workout.workout_plan_id,
        scheduled_date=scheduled_workout.scheduled_date,
    )

    # Assert
    assert isinstance(result, ScheduledWorkoutResponse)
    assert result.id == 10
    assert result.workout_plan_id == 1
    assert result.user_id == 1

    mock_session_repository.schedule_session.assert_awaited_once_with(
        user_id=1, workout_plan_id=1, scheduled_date=scheduled_workout.scheduled_date
    )


@pytest.mark.asyncio
async def test_list_scheduled_workouts(scheduled_service, mock_session_repository):
    # Arrange
    mock_session_repository.list_sessions.return_value = [
        ScheduledWorkoutResponse(
            id=5,
            workout_plan_id=2,
            user_id=1,
            scheduled_date=datetime(2024, 2, 1, 9, 0),
        ),
        ScheduledWorkoutResponse(
            id=6,
            workout_plan_id=3,
            user_id=1,
            scheduled_date=datetime(2024, 2, 2, 18, 0),
        ),
    ]

    # Act
    result = await scheduled_service.list_scheduled_workouts(user_id=1)
    print("RESULT =", result)
    for r in result:
        print(r.model_dump())

    # Assert
    assert len(result) == 2
    assert all(isinstance(r, ScheduledWorkoutResponse) for r in result)

    mock_session_repository.list_sessions.assert_awaited_once_with(user_id=1)
