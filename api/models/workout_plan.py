from pydantic import BaseModel
from typing import Optional

class WorkoutPlanBase(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None

class WorkoutPlanCreate(WorkoutPlanBase):
    pass

class workoutPlanResponse(WorkoutPlanBase):
    id: int