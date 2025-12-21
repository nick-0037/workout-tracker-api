from pydantic import BaseModel, ConfigDict
from typing import Optional


class ReportSummary(BaseModel):
    """Summary report of user workout activity."""

    total_sessions: int
    total_exercises: int
    avg_reps: Optional[float] = None
    avg_weight: Optional[float] = None

    # Essential for mapping database aggregation results (AVG, COUNT)
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "total_sessions": 12,
                "total_exercises": 48,
                "avg_reps": 10.5,
                "avg_weight": 22.3,
            }
        },
    )
