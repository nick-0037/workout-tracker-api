from fastapi import APIRouter, Depends, status
from api.services.workout_service import WorkoutService
from api.models.workout_plan import WorkoutPlanResponse, WorkoutPlanCreate
from api.models.workout_plan_exercise import (
    WorkoutPlanExerciseResponse,
    WorkoutPlanExerciseCreate,
)
from typing import List
from api.dependencies.auth import get_current_user
from api.dependencies.repositories import get_workout_repo

router = APIRouter(prefix="/workouts", tags=["Workouts"])


def get_service(workout_repo=Depends(get_workout_repo)):
    """Dependency to inject the service with repository and DB."""
    return WorkoutService(workout_repository=workout_repo)


@router.get(
    "/",
    response_model=List[WorkoutPlanResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all workout plans",
    description="""
    Returns a list of all workout plans.
    """,
    responses={
        200: {"description": "List of workout plans returned successfully"},
        401: {"description": "Missing or invalid authentication token"},
        422: {"description": "Validation error"},
    },
)
async def get_all_workouts(
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    return await service.get_all_workout_plans(user_id=current_user)


@router.get(
    "/{workout_plan_id}",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a workout plan by ID",
    description="""
    Fetch a specific workout plan using its ID.
    """,
    responses={
        200: {"description": "Workout plan retrieved successfully"},
        401: {"description": "Missing or invalid authentication token"},
        404: {"description": "Workout plan not found"},
        422: {"description": "Validation error"},
    },
)
async def get_workout_plan_by_id(
    workout_plan_id: int,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    return await service.get_workout_plan_by_id(
        workout_plan_id=workout_plan_id, user_id=current_user
    )


@router.post(
    "/",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new workout plan",
    description="""
    Creates a new  workout plan for the authenticated user.
    """,
    responses={
        201: {"description": "Workout plan created successfully"},
        400: {"description": "Invalid workout data"},
        401: {"description": "Missing or invalid authentication token"},
        422: {"description": "Validation error"},
    },
)
async def create_workout_plan(
    workout_data: WorkoutPlanCreate,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    return await service.create_workout_plan(
        user_id=current_user,
        name=workout_data.name,
        description=workout_data.description,
    )


@router.patch(
    "/{workout_plan_id}",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing workout plan",
    description="""
    Updates the name or description of a workout plan.
    """,
    responses={
        200: {"description": "Workout plan updated successfully"},
        400: {"description": "Invalid update data"},
        401: {"description": "Missing or invalid authentication token"},
        404: {"description": "Workout plan not found"},
        422: {"description": "Validation error"},
    },
)
async def update_workout_plan(
    workout_plan_id: int,
    workout_data: WorkoutPlanCreate,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    return await service.update_workout_plan(
        workout_plan_id=workout_plan_id,
        user_id=current_user,
        name=workout_data.name,
        description=workout_data.description,
    )


@router.delete(
    "/{workout_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a workout plan",
    description="""
    Deletes a workout plan by ID.
    """,
    responses={
        204: {"description": "Workout plan deleted successfully"},
        401: {"description": "Missing or invalid authentication token"},
        404: {"description": "Workout plan not found"},
        422: {"description": "Validation error"},
    },
)
async def delete_workout_plan(
    workout_plan_id: int,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    await service.delete_workout_plan(
        workout_plan_id=workout_plan_id, user_id=current_user
    )


@router.post(
    "/{workout_plan_id}/exercises",
    response_model=WorkoutPlanExerciseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add an exercise to a workout plan",
    description="""
    Assigns an exercise to a workout plan.
    """,
    responses={
        201: {"description": "Exercise added to workout plan"},
        400: {"description": "Invalid exercise data"},
        401: {"description": "Missing or invalid authentication token"},
        404: {"description": "Workout plan or exercise not found"},
        422: {"description": "Validation error"},
    },
)
async def add_exercise_to_plan(
    workout_plan_id: int,
    exercise_data: WorkoutPlanExerciseCreate,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    return await service.add_exercise_to_plan(
        workout_plan_id=workout_plan_id,
        user_id=current_user,
        exercise_data=exercise_data,
    )


@router.delete(
    "/{workout_plan_id}/exercises/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove an exercise from a workout plan",
    description="""
    Removes an exercise from a workout plan.
    """,
    responses={
        204: {"description": "Exercise removed successfully"},
        401: {"description": "Missing or invalid authentication token"},
        404: {"description": "Exercise not found in this workout plan"},
        422: {"description": "Validation error"},
    },
)
async def remove_exercise_from_plan(
    workout_plan_id: int,
    exercise_id: int,
    current_user: int = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    await service.remove_exercise_from_plan(
        workout_plan_id=workout_plan_id,
        user_id=current_user,
        exercise_id=exercise_id,
    )
