from api.models.report import ReportSummary
from typing import Dict, Any

class ReportService:
    def __init__(self, report_repository):
        self.report_repo = report_repository

    async def get_summary(self, user_id: int) -> ReportSummary:
        raw_summary_data: Dict[str, Any] =  await self.report_repo.get_summary(user_id=user_id)
        
        if not raw_summary_data:
            return ReportSummary()
        
        summary = ReportSummary.model_validate(raw_summary_data)
        print("Retrieved session summary:", summary)
        return summary
