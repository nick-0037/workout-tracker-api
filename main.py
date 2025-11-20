from fastapi import FastAPI
from api.controllers.auth_controller import router as user_router
from api.controllers.exercise_controller import router as exercise_router
from api.controllers.workout_controller import router as workout_router
from api.config import ENV, DB_PATH
from contextlib import asynccontextmanager

app = FastAPI(title="Workout Tracker API")

app.include_router(user_router)
app.include_router(exercise_router)
app.include_router(workout_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"📦 Config loaded → ENV={ENV}, DB_PATH={DB_PATH}")
    yield


@app.get("/")
def read_root():
    return {"message": "Workout Tracker API"}
