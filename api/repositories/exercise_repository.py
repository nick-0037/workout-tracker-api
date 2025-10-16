from api.models.exercise import ExerciseCreate, ExerciseResponse


class ExerciseRepository:
    def __init__(self, db):
        self.db = db

    async def get_all_exercises(self) -> list[ExerciseResponse]:
        cursor = self.db.cursor()
        rows = cursor.execute("SELECT * FROM exercises").fetchall()

        return [
            ExerciseResponse(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                category=row["category"],
                muscle_group=row["muscle_group"],
            )
            for row in rows
        ]

    async def get_exercise_by_id(self, exercise_id: int) -> ExerciseResponse | None:
        cursor = self.db.cursor()
        row = cursor.execute(
            "SELECT * FROM exercises WHERE id = ?", (exercise_id,)
        ).fetchone()

        if row:
            return ExerciseResponse(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                category=row["category"],
                muscle_group=row["muscle_group"],
            )

        return None
