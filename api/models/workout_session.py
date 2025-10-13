from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkoutSessionBase(BaseModel):
    user_id: int
    workout_plan_id: int
    scheduled_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "completed"
    notes: Optional[str] = None
    
class WorkoutSessionCreate(WorkoutSessionBase):
    pass

class workoutSessionResponse(WorkoutSessionBase)
    id: int
    
