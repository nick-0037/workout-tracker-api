from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ScheduledWorkoutBase(BaseModel):
    """Base model for a scheduled workout."""

    workout_plan_id: int
    scheduled_date: datetime

    # Global configuration for DB compatibility and clean strings
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class ScheduledWorkoutCreate(ScheduledWorkoutBase):
    """Model used when creating a scheduled workout."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"workout_plan_id": 3, "scheduled_date": "2025-02-10T09:00:00"}
        }
    )


class ScheduledWorkoutResponse(ScheduledWorkoutBase):
    """Response model for a scheduled workout (includes IDs)."""

    id: int
    user_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 15,
                "user_id": 4,
                "workout_plan_id": 3,
                "scheduled_date": "2025-02-10T09:00:00",
            }
        }
    )
