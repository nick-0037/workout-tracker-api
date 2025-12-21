from api.models.exercise import ExerciseResponse
from typing import List
from api.core.error_handler import AppException


class ExerciseService:
    def __init__(self, exercise_repository):
        self.exercise_repository = exercise_repository

    async def get_all_exercises(self, user_id: int) -> List[ExerciseResponse]:
        exercises = await self.exercise_repository.get_all_exercises(user_id=user_id)
        return exercises

    async def get_exercise_by_id(
        self, user_id: int, exercise_id: int
    ) -> ExerciseResponse:
        exercise = await self.exercise_repository.get_exercise_by_id(
            user_id=user_id, exercise_id=exercise_id
        )

        if not exercise:
            raise AppException("Exercise not found", 404)

        return exercise
