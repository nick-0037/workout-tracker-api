from fastapi import APIRouter, Depends, status
from api.models.exercise import ExerciseResponse
from api.services.exercise_service import ExerciseService
from api.repositories.exercise_repository import ExerciseRepository
from database.db import get_db
from typing import List

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", response_model=List[ExerciseResponse], status_code=status.HTTP_200_OK)
async def get_all_exercises(db=Depends(get_db)):
    repository = ExerciseRepository(db)
    service = ExerciseService(repository)
    return await service.get_all_exercises()


@router.get(
    "/{exercise_id}", response_model=ExerciseResponse, status_code=status.HTTP_200_OK
)
async def get_exercise_by_id(exercise_id: int, db=Depends(get_db)):
    repository = ExerciseRepository(db)
    service = ExerciseService(repository)
    return await service.get_exercise_by_id(exercise_id)
