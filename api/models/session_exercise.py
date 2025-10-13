from pydantic import BaseModel
from typing import Optional

class SessionExerciseBase(BaseModel):
    session_id: int
    exercise_id: int
    sets_completed: Optional[int] = None
    reps_completed: Optional[int] = None
    weight_used: Optional[float] = None
    notes: Optional[str] = None

class SessionExerciseCreate(SessionExerciseBase):
    pass

class SessionExerciseResponse(SessionExerciseBase):
    id: int
    
