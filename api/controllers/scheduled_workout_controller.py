from fastapi import APIRouter, Depends
from api.models.scheduled_workout import (
    ScheduledWorkoutCreate,
    ScheduledWorkoutResponse,
)
from api.services.scheduled_workout_service import ScheduledWorkoutService
from typing import List
from api.dependencies.auth import get_current_user
from api.dependencies.repositories import get_session_repo, get_workout_repo

router = APIRouter(prefix="/scheduled-workouts", tags=["Scheduled Workouts"])


def get_service(
    session_repo=Depends(get_session_repo),
    workout_repo=Depends(get_workout_repo),
):
    """Dependency to inject the service with repository and DB."""
    return ScheduledWorkoutService(
        session_repository=session_repo, workout_repository=workout_repo
    )


@router.post(
    "/",
    response_model=ScheduledWorkoutResponse,
    summary="Schedule a workout",
    description="""
    Creates a scheduled workout.
    """,
    responses={
        400: {"description": "Invalid workout plan"},
        401: {"description": "Unauthorized"},
        404: {"description": "Workout plan not found"},
    },
)
async def create_scheduled_workout(
    data: ScheduledWorkoutCreate,
    current_user: int = Depends(get_current_user),
    service: ScheduledWorkoutService = Depends(get_service),
):
    return await service.schedule_workout(
        user_id=current_user,
        workout_plan_id=data.workout_plan_id,
        scheduled_date=data.scheduled_date,
    )


@router.get(
    "/",
    response_model=List[ScheduledWorkoutResponse],
    summary="List scheduled workouts",
    description="""
    Returns all scheduled workouts.
    """,
    responses={
        401: {"description": "Unauthorized"},
    },
)
async def list_scheduled_workouts(
    current_user: int = Depends(get_current_user),
    service: ScheduledWorkoutService = Depends(get_service),
):
    return await service.list_scheduled_workouts(user_id=current_user)
