from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from api.models.workout_plan_exercise import WorkoutPlanExerciseResponse


class WorkoutPlanBase(BaseModel):
    """Base model for workout plan data."""

    name: str
    description: Optional[str] = None

    # Global configuration for DB compatibility and clean strings
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class WorkoutPlanCreate(WorkoutPlanBase):
    """Model used when creating a new workout plan."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Push Day Routine",
                "description": "Workout plan focused on chest, shoulders, and triceps.",
            }
        }
    )


class WorkoutPlanResponse(WorkoutPlanBase):
    """Response model for a workout plan (includes IDs)."""

    id: int
    user_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 3,
                "user_id": 12,
                "name": "Push Day Routine",
                "description": "Workout plan focused on chest, shoulders, and triceps.",
            }
        }
    )


class WorkoutPlanWithExercises(WorkoutPlanResponse):
    """Response model that includes the workout plan and its related exercises."""

    exercises: list[WorkoutPlanExerciseResponse] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 3,
                "user_id": 12,
                "name": "Push Day Routine",
                "description": "Workout plan focused on chest, shoulders, and triceps.",
                "exercises": [
                    {
                        "id": 10,
                        "workout_plan_id": 3,
                        "exercise_id": 1,
                        "sets": 3,
                        "reps": 12,
                        "weight": 23.0,
                        "notes": "Warm up included",
                    }
                ],
            }
        }
    )
