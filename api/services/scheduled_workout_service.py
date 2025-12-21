from datetime import datetime
from api.models.scheduled_workout import ScheduledWorkoutResponse
from typing import List
from api.core.error_handler import AppException


class ScheduledWorkoutService:
    def __init__(self, session_repository, workout_repository):
        self.session_repo = session_repository
        self.workout_repo = workout_repository

    async def schedule_workout(
        self, user_id: int, workout_plan_id: int, scheduled_date: datetime
    ) -> ScheduledWorkoutResponse:
        workout_plan = await self.workout_repo.get_workout_plan_by_id(
            workout_plan_id=workout_plan_id, user_id=user_id
        )
        if not workout_plan:
            raise AppException("Workout plan not found", 404)

        # Schedule the workout session
        session = await self.session_repo.schedule_session(
            user_id=user_id,
            workout_plan_id=workout_plan_id,
            scheduled_date=scheduled_date,
        )
        return session

    async def list_scheduled_workouts(
        self, user_id: int
    ) -> List[ScheduledWorkoutResponse]:
        sessions = await self.session_repo.list_sessions(user_id=user_id)
        return [ScheduledWorkoutResponse(**s.model_dump()) for s in sessions]
