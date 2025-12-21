from fastapi import APIRouter, Depends
from api.services.report_service import ReportService
from api.models.report import ReportSummary
from api.dependencies.auth import get_current_user
from api.dependencies.repositories import get_report_repo

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_service(report_repo=Depends(get_report_repo)):
    """Dependency to inject the service with repository and DB."""
    return ReportService(report_repository=report_repo)


@router.get(
    "/summary",
    response_model=ReportSummary,
    summary="Retrieve workout performance summary",
    description="""
    Returns a statistical summary of the user's workout performance.
    """,
    responses={
        401: {"description": "Unauthorized"},
    },
)
async def list_workouts(
    current_user: int = Depends(get_current_user),
    service: ReportService = Depends(get_service),
):
    return await service.get_summary(user_id=current_user)
