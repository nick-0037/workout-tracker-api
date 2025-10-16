from api.models.exercise import ExerciseCreate, ExerciseResponse
from typing import List
from fastapi import HTTPException, status


class ExerciseService:
    def __init__(self, exercise_repository):
        self.exercise_repository = exercise_repository

    async def get_all_exercises(self) -> List[ExerciseResponse]:
        exercises = await self.exercise_repository.get_all_exercises()
        return exercises

    async def get_exercise_by_id(self, exercise_id: int) -> ExerciseResponse:
        exercise = await self.exercise_repository.get_exercise_by_id(exercise_id)

        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
            )

        return exercise
