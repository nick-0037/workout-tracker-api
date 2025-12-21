from fastapi import FastAPI
from api.controllers.auth_controller import router as user_router
from api.controllers.exercise_controller import router as exercise_router
from api.controllers.workout_controller import router as workout_router
from api.controllers.report_controller import router as report_router
from api.controllers.scheduled_workout_controller import router as scheduled_router
from api.config import ENV, DB_PATH
from contextlib import asynccontextmanager
from api.core.error_handler import app_exception_handler, validation_exception_handler
from api.core.exceptions import AppException
from fastapi.exceptions import RequestValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"📦 Config loaded → ENV={ENV}, DB_PATH={DB_PATH}")
    yield
    print("🚀 Shutting down... Closing connections.")


app = FastAPI(
    title="Workout Tracker API",
    lifespan=lifespan,
    description="API to manage users, workouts and exercises",
    version="1.0.0",
    openapi_tags=[
        {"name": "Auth", "description": "User registration and login"},
        {"name": "Exercises", "description": "Manage exercises"},
        {"name": "Workouts", "description": "Manage workout plans and exercises"},
        {"name": "Reports", "description": "Generate reports"},
        {"name": "Scheduled Workouts", "description": "Manage scheduled workouts"},
    ],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(user_router)
app.include_router(exercise_router)
app.include_router(workout_router)
app.include_router(report_router)
app.include_router(scheduled_router)


@app.get("/")
def read_root():
    return {"message": "Workout Tracker API"}
