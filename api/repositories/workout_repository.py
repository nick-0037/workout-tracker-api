from api.models.workout_plan import WorkoutPlanResponse
from api.models.workout_plan_exercise import (
    WorkoutPlanExerciseResponse,
)
from typing import List, Optional, Dict


class WorkoutRepository:
    def __init__(self, db):
        self.db = db

    async def get_all_workout_plans(self, user_id: int) -> List[Dict]:
        async with self.db.execute(
            "SELECT id, user_id, name, description FROM workout_plans WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            rows = await cursor.fetchall()

        return [dict(row) for row in rows]

    async def get_workout_plan_by_id(
        self, workout_plan_id: int, user_id: int
    ) -> Optional[Dict]:
        async with self.db.execute(
            "SELECT * FROM workout_plans WHERE id = ? AND user_id = ?",
            (workout_plan_id, user_id),
        ) as cursor:
            row = await cursor.fetchone()

        return dict(row) if row else None

    async def create_workout_plan(
        self, user_id: int, name: str, description: Optional[str] = None
    ) -> Dict:
        cursor = await self.db.execute(
            "INSERT INTO workout_plans (user_id, name, description) VALUES (?, ?, ?)",
            (user_id, name, description),
        )
        await self.db.commit()
        new_id = cursor.lastrowid

        return await self.get_workout_plan_by_id(new_id, user_id)

    async def update_workout_plan(
        self,
        user_id: int,
        workout_plan_id: int,
        name: str,
        description: Optional[str],
    ) -> Optional[Dict]:
        await self.db.execute(
            """
            UPDATE workout_plans
            SET name = ?, description = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                name,
                description,
                workout_plan_id,
                user_id,
            ),
        )
        await self.db.commit()

        return await self.get_workout_plan_by_id(workout_plan_id, user_id)

    async def delete_workout_plan(self, workout_plan_id: int, user_id: int) -> bool:
        cursor = None
        try:
            cursor = await self.db.execute(
                "DELETE FROM workout_plans WHERE id = ? AND user_id = ?",
                (workout_plan_id, user_id),
            )
            await self.db.commit()
            return cursor.rowcount > 0
        finally:
            if cursor:
                await cursor.close()

    async def add_exercise_to_plan(
        self,
        workout_plan_id: int,
        exercise_id: int,
        sets: int,
        weight: float,
        reps: int,
    ) -> Dict:

        cursor = await self.db.execute(
            """
            INSERT INTO workout_plan_exercises (workout_plan_id, exercise_id, sets, weight, reps)
            VALUES (?, ?, ?, ?, ?)
            """,
            (workout_plan_id, exercise_id, sets, weight, reps),
        )
        await self.db.commit()
        new_id = cursor.lastrowid

        return await self.get_exercise_in_plan_by_id(new_id)

    async def remove_exercise_from_plan(
        self, workout_plan_id: int, exercise_id: int
    ) -> bool:
        cursor = await self.db.execute(
            """
            DELETE FROM workout_plan_exercises
            WHERE workout_plan_id = ? AND exercise_id = ?
            """,
            (workout_plan_id, exercise_id),
        )
        await self.db.commit()
        return cursor.rowcount > 0

    async def get_exercise_in_plan_by_id(self, wpe_id: int) -> Optional[Dict]:
        """
         Retrieve a workout plan exercise by its ID.
        """
        cursor = await self.db.execute(
            """
            SELECT 
                wpe.*, 
                e.name as exercise_name, 
                e.category, 
                e.muscle_group
            FROM workout_plan_exercises wpe
            JOIN exercises e ON wpe.exercise_id = e.id
            WHERE wpe.id = ?
            """,
            (wpe_id,),
        )
        row = await cursor.fetchone()
        await cursor.close()

        return dict(row) if row else None
