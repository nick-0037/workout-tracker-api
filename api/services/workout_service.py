from api.core.exceptions import AppException
from api.models.workout_plan import WorkoutPlanResponse
from api.models.workout_plan_exercise import (
    WorkoutPlanExerciseCreate,
    WorkoutPlanExerciseResponse,
)


class WorkoutService:
    def __init__(self, workout_repository):
        self.workout_repository = workout_repository

    async def get_all_workout_plans(self, user_id: int) -> list[WorkoutPlanResponse]:
        workouts = await self.workout_repository.get_all_workout_plans(user_id=user_id)
        return workouts

    async def get_workout_plan_by_id(
        self, workout_plan_id: int, user_id: int
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.get_workout_plan_by_id(
            workout_plan_id=workout_plan_id, user_id=user_id
        )
        if not workout:
            raise AppException("Workout plan not found", 404)
        return workout

    async def create_workout_plan(
        self, user_id: int, name: str, description: str
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.create_workout_plan(
            user_id=user_id, name=name, description=description
        )
        if not workout:
            raise AppException("Failed to create workout plan", 400)
        return workout

    async def update_workout_plan(
        self, workout_plan_id: int, user_id: int, name: str, description: str
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.update_workout_plan(
            workout_plan_id=workout_plan_id,
            user_id=user_id,
            name=name,
            description=description,
        )
        if not workout:
            raise AppException("Failed to update workout plan", 400)
        return workout

    async def delete_workout_plan(
        self, workout_plan_id: int, user_id: int
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.delete_workout_plan(
            workout_plan_id=workout_plan_id, user_id=user_id
        )
        if not workout:
            raise AppException("Workout plan not found", 404)
        return workout

    async def add_exercise_to_plan(
        self,
        workout_plan_id: int,
        user_id: int,
        exercise_data: WorkoutPlanExerciseCreate,
    ) -> WorkoutPlanExerciseResponse:
        workout_plan = await self.workout_repository.get_workout_plan_by_id(
            workout_plan_id=workout_plan_id, user_id=user_id
        )
        if not workout_plan:
            raise AppException("Workout plan not found", 404)

        return await self.workout_repository.add_exercise_to_plan(
            workout_plan_id=workout_plan_id, **exercise_data.model_dump()
        )

    async def remove_exercise_from_plan(
        self, workout_plan_id: int, user_id: int, exercise_id: int
    ) -> WorkoutPlanExerciseResponse:
        workout = await self.workout_repository.get_workout_plan_by_id(
            workout_plan_id=workout_plan_id, user_id=user_id
        )
        if not workout:
            raise AppException("Workout plan not found", 404)

        removed_exercise = await self.workout_repository.remove_exercise_from_plan(
            workout_plan_id=workout_plan_id, exercise_id=exercise_id
        )
        if not removed_exercise:
            raise AppException("Failed to remove exercise", 400)
        return True
