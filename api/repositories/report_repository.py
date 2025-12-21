from api.models.report import ReportSummary


class ReportRepository:
    def __init__(self, db):
        self.db = db

    async def get_summary(self, user_id: int) -> ReportSummary:
        cursor = await self.db.cursor()

        await cursor.execute(
            """
            SELECT COUNT(*)
            FROM workout_sessions
            WHERE user_id = ? AND status = 'completed'
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
        total_sessions = row[0] if row is not None else 0

        await cursor.execute(
            """
            SELECT COUNT(*)
            FROM sessions_exercises se
            JOIN workout_sessions ws ON ws.id = se.session_id
            WHERE ws.user_id = ?
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
        total_exercises = row[0] if row is not None else 0

        await cursor.execute(
            """
            SELECT COALESCE(AVG(reps_completed), 0)
            FROM sessions_exercises se
            JOIN workout_sessions ws ON ws.id = se.session_id
            WHERE ws.user_id = ? AND reps_completed IS NOT NULL
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
        avg_reps = row[0] if row is not None else 0

        await cursor.execute(
            """
            SELECT COALESCE(AVG(weight_used), 0)
            FROM sessions_exercises se
            JOIN workout_sessions ws on ws.id = se.session_id
            WHERE ws.user_id = ? AND weight_used IS NOT NULL
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
        avg_weight = row[0] if row is not None else 0

        await cursor.close()

        return {
            "total_sessions": total_sessions,
            "total_exercises": total_exercises,
            "avg_reps": avg_reps,
            "avg_weight": avg_weight,
        }
