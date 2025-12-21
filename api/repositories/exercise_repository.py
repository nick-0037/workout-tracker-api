from api.models.exercise import ExerciseResponse


class ExerciseRepository:
    def __init__(self, db):
        self.db = db

    async def get_all_exercises(self, user_id) -> list[ExerciseResponse]:
        cursor = await self.db.execute(
            "SELECT * FROM exercises WHERE user_id = ?", (user_id,)
        )
        rows = await cursor.fetchall()
        await cursor.close()

        return [dict(row) for row in rows]

    async def get_exercise_by_id(
        self, exercise_id: int, user_id
    ) -> ExerciseResponse | None:
        cursor = await self.db.execute(
            "SELECT * FROM exercises WHERE id = ? AND user_id = ? ",
            (exercise_id, user_id),
        )

        row = await cursor.fetchone()
        await cursor.close()

        if row:
            return dict(row)

        return None
