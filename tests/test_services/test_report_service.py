import pytest
from api.services.report_service import ReportService


@pytest.fixture
def report_service(mock_report_repository):
    return ReportService(mock_report_repository)


@pytest.mark.asyncio
async def test_get_summary_success(report_service, mock_report_repository):
    # Arrange
    mock_report_repository.get_summary.return_value = {
        "total_sessions": 10,
        "total_exercises": 50,
        "avg_reps": 45,
        "avg_weight": 45,
    }

    # Act
    summary = await report_service.get_summary(user_id=1)

    # Assert
    assert summary.total_sessions == 10
    assert summary.total_exercises == 50
    assert summary.avg_reps == 45
    assert summary.avg_weight == 45
    mock_report_repository.get_summary.assert_awaited_once_with(user_id=1)
