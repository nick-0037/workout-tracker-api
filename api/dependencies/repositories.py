from api.repositories.workout_session_repository import ScheduledSessionRepository
from api.repositories.workout_repository import WorkoutRepository
from api.repositories.exercise_repository import ExerciseRepository
from api.repositories.report_repository import ReportRepository
from api.repositories.user_repository import UserRepository
from fastapi import Depends
from database.db import get_db

async def get_session_repo(db=Depends(get_db)):
    return ScheduledSessionRepository(db)

async def get_workout_repo(db=Depends(get_db)):
    return WorkoutRepository(db)

async def get_exercise_repo(db=Depends(get_db)):
    return ExerciseRepository(db)

async def get_report_repo(db=Depends(get_db)):
    return ReportRepository(db)

async def get_auth_repo(db=Depends(get_db)):
    return UserRepository(db)

