from pydantic import BaseModel, Field
from typing import Optional, List
from api.models.workout_plan_exercise import WorkoutPlanExerciseResponse
from typing import List


class WorkoutPlanBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


class WorkoutPlanResponse(WorkoutPlanBase):
    id: int
    user_id: int


class WorkoutPlanWithExercises(WorkoutPlanResponse):
    exercises: List[WorkoutPlanExerciseResponse] = Field(default_factory=list)
