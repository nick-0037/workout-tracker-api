from fastapi import APIRouter, Depends, status
from api.models.exercise import ExerciseResponse
from api.services.exercise_service import ExerciseService
from typing import List
from api.dependencies.repositories import get_exercise_repo
from api.dependencies.auth import get_current_user

router = APIRouter(prefix="/exercises", tags=["Exercises"])


def get_service(exercise_repo=Depends(get_exercise_repo)):
    """Dependency to inject the service with repository and DB."""
    return ExerciseService(exercise_repository=exercise_repo)


@router.get(
    "/",
    response_model=List[ExerciseResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all exercises",
    description="""
    Returns a list of all available exercises for the authenticated user.
    """,
    responses={
        401: {"description": "Unauthorized"},
    },
)
async def get_all_exercises(
    current_user: int = Depends(get_current_user),
    service: ExerciseService = Depends(get_service),
):
    return await service.get_all_exercises(user_id=current_user)


@router.get(
    "/{exercise_id}",
    response_model=ExerciseResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve an exercise by ID",
    description="""
    Fetches a single exercise by its unique ID.
    """,
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Exercise not found"},
    },
)
async def get_exercise_by_id(
    exercise_id: int,
    current_user: int = Depends(get_current_user),
    service: ExerciseService = Depends(get_service),
):
    return await service.get_exercise_by_id(
        user_id=current_user, exercise_id=exercise_id
    )
