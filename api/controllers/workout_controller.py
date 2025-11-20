from fastapi import APIRouter, Depends, status, HTTPException
from api.services.workout_service import WorkoutService
from api.models.workout_plan import WorkoutPlanResponse, WorkoutPlanCreate
from api.models.workout_plan_exercise import (
    WorkoutPlanExerciseResponse,
    WorkoutPlanExerciseCreate,
)
from api.repositories.workout_repository import WorkoutRepository
from database.db import get_db
from typing import List
from api.dependencies.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["Workouts"])


def get_workout_service(db=Depends(get_db)):
    """Dependency to inject the service with repository and DB."""
    repo = WorkoutRepository(db)
    return WorkoutService(repo)


@router.get(
    "/", response_model=List[WorkoutPlanResponse], status_code=status.HTTP_200_OK
)
async def get_all_workouts(
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_workout_service),
):
    return await service.get_all_workout_plans(current_user)


@router.get(
    "/{workout_id}", response_model=WorkoutPlanResponse, status_code=status.HTTP_200_OK
)
async def get_workout_plan_by_id(
    workout_id: int,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_workout_service),
):
    return await service.get_workout_plan_by_id(workout_id, current_user)


@router.post(
    "/", response_model=WorkoutPlanResponse, status_code=status.HTTP_201_CREATED
)
async def create_workout_plan(
    workout_data: WorkoutPlanCreate,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_workout_service),
):
    return await service.create_workout_plan(current_user, workout_data.name, workout_data.description
    )


@router.patch(
    "/{workout_plan_id}",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_200_OK,
)
async def update_workout_plan(
    workout_plan_id: int,
    workout_data: WorkoutPlanCreate,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_workout_service),
):
    return await service.update_workout_plan(
        workout_plan_id,
        current_user,
        workout_data.name,
        workout_data.description,
    )


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_plan(
    workout_id: int,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_workout_service),
):
    await service.delete_workout_plan(workout_id, current_user)


@router.post(
    "/{workout_plan_id}/exercises",
    response_model=WorkoutPlanExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_exercise_to_plan(
    workout_plan_id: int,
    exercise_data: WorkoutPlanExerciseCreate,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_workout_service),
):
    return await service.add_exercise_to_plan(workout_plan_id, current_user, exercise_data)


@router.delete(
    "/{workout_plan_id}/exercises/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_exercise_from_plan(
    workout_plan_id: int,
    exercise_id: int,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_workout_service),
):
    await service.remove_exercise_from_plan(workout_plan_id, current_user, exercise_id)
