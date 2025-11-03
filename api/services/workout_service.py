from fastapi import HTTPException, status
from api.models.workout_plan import WorkoutPlanResponse
from api.models.workout_plan_exercise import (
    WorkoutPlanExerciseCreate,
    WorkoutPlanExerciseResponse,
)


class WorkoutService:
    def __init__(self, workout_repository):
        self.workout_repository = workout_repository

    async def get_all_workout_plans(self, user_id: int) -> list[WorkoutPlanResponse]:
        workouts = await self.workout_repository.get_all_workout_plans_by_user(user_id)
        return workouts

    async def get_workout_plan_by_id(
        self, workout_id: int, user_id: int
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.get_workout_plan_by_id(
            workout_id, user_id
        )
        if not workout:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workout plan not found"
            )
        return workout

    async def create_workout_plan(
        self, user_id: int, name: str, description: str
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.create_workout_plan(
            user_id, name, description
        )
        if not workout:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create workout plan",
            )
        return workout

    async def update_workout_plan(
        self, workout_id: int, user_id: int, name: str, description: str
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.update_workout_plan(
            workout_id, user_id, name, description
        )
        if not workout:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update workout plan",
            )
        return workout

    async def delete_workout_plan(
        self, workout_id: int, user_id: int
    ) -> WorkoutPlanResponse:
        workout = await self.workout_repository.delete_workout_plan(workout_id, user_id)
        if not workout:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workout plan not found"
            )
        return workout

    async def add_exercise_to_plan(
        self,
        workout_plan_id: int,
        user_id: int,
        exercise_data: WorkoutPlanExerciseCreate,
    ) -> WorkoutPlanExerciseResponse:
        workout_plan = await self.workout_repository.get_workout_plan_by_id(
            workout_plan_id, user_id
        )
        if not workout_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workout plan not found"
            )

        exercise_with_plan = WorkoutPlanExerciseCreate(
            workout_plan_id=workout_plan_id, **exercise_data.model_dump()
        )

        return await self.workout_repository.add_exercise_to_plan(exercise_with_plan)

    async def remove_exercise_from_plan(
        self, workout_plan_id: int, user_id: int, exercise_id: int
    ) -> WorkoutPlanExerciseResponse:
        workout = await self.workout_repository.get_workout_plan_by_id(
            workout_plan_id, user_id
        )
        if not workout:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workout plan not found"
            )

        removed_exercise = await self.workout_repository.remove_exercise_from_plan(
            workout_plan_id, exercise_id
        )
        if not removed_exercise:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove exercise",
            )
        return True
