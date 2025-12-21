from pydantic import BaseModel, ConfigDict
from typing import Optional


class ExerciseBase(BaseModel):
    """Base model for exercise data."""

    name: str
    description: Optional[str] = None
    category: str
    muscle_group: Optional[str] = None

    # Global configuration for DB compatibility and clean strings
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class ExerciseCreate(ExerciseBase):
    """Model used for creating a new exercise."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Bench Press",
                "description": "A compound exercise targeting the chest.",
                "category": "Strength",
                "muscle_group": "Chest",
            }
        }
    )


class ExerciseResponse(ExerciseBase):
    """Response model for exercise data (includes IDs)."""

    id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Squat",
                "description": "Compound leg movement",
                "category": "Strength",
                "muscle_group": "Quads",
            }
        }
    )
