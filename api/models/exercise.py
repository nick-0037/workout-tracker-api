from pydantic import BaseModel, ConfigDict
from typing import Optional

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    muscle_group: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass
    
class ExerciseResponse(ExerciseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
       