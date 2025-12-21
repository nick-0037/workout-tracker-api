from pydantic import BaseModel, ConfigDict
from typing import Optional


class SessionExerciseBase(BaseModel):
    """Base model for exercise data within a workout session."""

    session_id: int
    exercise_id: int
    sets_completed: Optional[int] = None
    reps_completed: Optional[int] = None
    weight_used: Optional[float] = None
    notes: Optional[str] = None

    # Global configuration for DB compatibility and clean strings
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class SessionExerciseCreate(SessionExerciseBase):
    """Model used when creating a session exercise entry."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": 1,
                "exercise_id": 2,
                "sets_completed": 3,
                "reps_completed": 10,
                "weight_used": 15.5,
                "notes": "Last set was a struggle",
            }
        }
    )


class SessionExerciseResponse(SessionExerciseBase):
    """Response model for session exercises (includes IDs)."""

    id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 8,
                "session_id": 1,
                "exercise_id": 2,
                "sets_completed": 3,
                "reps_completed": 10,
                "weight_used": 15.5,
                "notes": "Great form throughout",
            }
        }
    )
