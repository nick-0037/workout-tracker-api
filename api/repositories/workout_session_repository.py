from api.models.scheduled_workout import ScheduledWorkoutResponse
from typing import List
from datetime import datetime
import aiosqlite


class ScheduledSessionRepository:
    def __init__(self, conn: aiosqlite.Connection):
        self.conn = conn

    async def schedule_session(
        self, user_id: int, workout_plan_id: int, scheduled_date: datetime
    ) -> ScheduledWorkoutResponse:
        """Schedule a new workout session and return ID"""

        query = """
            INSERT INTO workout_sessions (user_id, workout_plan_id, scheduled_date)
            VALUES (?, ?, ?)
        """

        await self.conn.execute(
            query,
            (user_id, workout_plan_id, scheduled_date),
        )

        await self.conn.commit()
        cursor = await self.conn.execute(
            """
            SELECT id, user_id, workout_plan_id, scheduled_date
            FROM workout_sessions
            WHERE user_id = ? AND workout_plan_id = ? AND scheduled_date = ?
            ORDER BY id DESC LIMIT 1
            """,
            (user_id, workout_plan_id, scheduled_date),
        )

        row = await cursor.fetchone()

        return ScheduledWorkoutResponse(
            id=row["id"],
            user_id=row["user_id"],
            workout_plan_id=row["workout_plan_id"],
            scheduled_date=row["scheduled_date"],
        )

    async def list_sessions(self, user_id: int) -> List[ScheduledWorkoutResponse]:
        """List all workout sessions for a user, ordered by date"""

        query = """
            SELECT id, user_id, workout_plan_id, scheduled_date, notes
            FROM workout_sessions
            WHERE user_id = ? AND status IN ('pending', 'active')
            ORDER BY scheduled_date ASC
        """

        cursor = await self.conn.execute(
            query,
            (user_id,),
        )

        rows = await cursor.fetchall()
        return [
            ScheduledWorkoutResponse(
                id=row["id"],
                user_id=row["user_id"],
                workout_plan_id=row["workout_plan_id"],
                scheduled_date=row["scheduled_date"],
                notes=row["notes"],
            )
            for row in rows
        ]
