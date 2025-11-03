from pydantic import BaseModel
from typing import Optional


class WorkoutPlanExerciseBase(BaseModel):
    exercise_id: int
    sets: int
    reps: Optional[int] = None
    weight: Optional[float] = None
    notes: Optional[str] = None


class WorkoutPlanExerciseCreate(WorkoutPlanExerciseBase):
    pass


class WorkoutPlanExerciseResponse(WorkoutPlanExerciseBase):
    id: int
    workout_plan_id: int
