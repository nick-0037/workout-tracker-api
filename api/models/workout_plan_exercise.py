from pydantic import BaseModel, ConfigDict
from typing import Optional


class WorkoutPlanExerciseBase(BaseModel):
    """Base model for exercises inside a workout plan."""

    exercise_id: int
    sets: int
    reps: Optional[int] = None
    weight: Optional[float] = None
    notes: Optional[str] = None

    # Global configuration for DB compatibility and clean strings
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class WorkoutPlanExerciseCreate(WorkoutPlanExerciseBase):
    """Model used when creating a workout plan exercise entry."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "exercise_id": 1,
                "sets": 4,
                "reps": 12,
                "weight": 30.0,
                "notes": "Focus on slow eccentric phase",
            }
        }
    )


class WorkoutPlanExerciseResponse(WorkoutPlanExerciseBase):
    """Response model for workout plan exercises (includes IDs)."""

    id: int
    workout_plan_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 10,
                "workout_plan_id": 2,
                "exercise_id": 1,
                "sets": 3,
                "reps": 10,
                "weight": 12.5,
                "notes": "First set as warm-up",
            }
        }
    )
