from api.models.workout_plan import WorkoutPlanCreate, WorkoutPlanResponse
from api.models.workout_plan_exercise import (
    WorkoutPlanExerciseCreate,
    WorkoutPlanExerciseResponse,
)
from api.services.workout_service import WorkoutService
from typing import List, Optional


class WorkoutRepository:
    def __init__(self, db):
        self.db = db

    async def get_all_workout_plans(self, user_id: int) -> List[WorkoutPlanResponse]:
        cursor = self.db.execute(
            "SELECT id, user_id, name, description FROM workout_plans WHERE user_id = ?",
            (user_id,),
        )
        rows = cursor.fetchall()

        return [
            WorkoutPlanResponse(
                id=row["id"],
                user_id=row["user_id"],
                name=row["name"],
                description=row["description"],
            )
            for row in rows
        ]

    async def get_workout_plan_by_id(
        self, workout_id: int, user_id: int
    ) -> Optional[WorkoutPlanResponse]:
        cursor = self.db.execute(
            "SELECT * FROM workout_plans WHERE id = ? AND user_id = ?",
            (
                workout_id,
                user_id,
            ),
        )
        row = cursor.fetchone()

        if not row:
            return None

        return WorkoutPlanResponse(
            id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            description=row["description"],
        )

    async def create_workout_plan(
        self, user_id: int, name: str, description: Optional[str] = None
    ) -> WorkoutPlanResponse:
        cursor = self.db.execute(
            "INSERT INTO workout_plans (user_id, name, description) VALUES (?, ?, ?)",
            (user_id, name, description),
        )
        self.db.commit()

        new_id = cursor.lastrowid

        return WorkoutPlanResponse(
            id=new_id,
            user_id=user_id,
            name=name,
            description=description,
        )

    async def update_workout_plan(
        self, user_id: int, workout_plan_id: int, name: str, description: Optional[str]
    ) -> Optional[WorkoutPlanResponse]:
        self.db.execute(
            """
        UPDATE workout_plans
        SET name = ?, description = ?
        WHERE id = ? AND user_id = ?
        """,
            (name, description, workout_plan_id, user_id),
        )
        self.db.commit()

        return await self.get_workout_plan_by_id(workout_plan_id, user_id)

    async def delete_workout_plan(self, workout_plan_id: int, user_id: int) -> bool:
        cursor = self.db.execute(
            "DELETE FROM workout_plans WHERE id = ? AND user_id = ?",
            (workout_plan_id, user_id),
        )
        self.db.commit()
        return cursor.rowcount > 0

    async def add_exercise_to_plan(
        self,
        workout_plan_id: int,
        exercise_id: int,
        sets: int,
        weight: float,
        reps: int,
    ) -> WorkoutPlanExerciseResponse:
        cursor = self.db.execute(
            """
            INSERT INTO workout_plan_exercises (workout_plan_id, exercise_id, sets, weight, reps)
            VALUES (?, ?, ?, ?, ?)
            """,
            (workout_plan_id, exercise_id, sets, weight, reps),
        )
        self.db.commit()

        new_id = cursor.lastrowid
        return WorkoutPlanExerciseResponse(
            id=new_id,
            workout_plan_id=workout_plan_id,
            exercise_id=exercise_id,
            sets=sets,
            weight=weight,
            reps=reps,
        )

    async def remove_exercise_from_plan(
        self, workout_plan_id: int, exercise_id: int
    ) -> bool:
        cursor = self.db.execute(
            """
            DELETE FROM workout_plan_exercises
            WHERE workout_plan_id = ? AND exercise_id = ?
            """,
            (workout_plan_id, exercise_id),
        )
        self.db.commit()
        return cursor.rowcount > 0
