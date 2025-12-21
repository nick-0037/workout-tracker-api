import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock
from api.dependencies.auth import get_current_user
from api.services.report_service import ReportService
from api.controllers.report_controller import get_service


@pytest.fixture
def mock_service():
    service = AsyncMock(spec=ReportService)

    # Mock to get_summary
    service.get_summary.return_value = {
        "total_sessions": 1,
        "total_exercises": 2,
        "avg_reps": 10,
        "avg_weight": 20,
    }
    return service


@pytest.fixture
def client(mock_service):
    original_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_current_user] = lambda: 1
    app.dependency_overrides[get_service] = lambda: mock_service
    
    yield TestClient(app)

    app.dependency_overrides = original_overrides


@pytest.mark.asyncio
async def test_summary_endpoint(client, mock_service):
    response = client.get("/reports/summary")

    print(f"RESPONSE TEST SCHEDULED", response.json())
    assert response.status_code == 200
    data = response.json()

    assert data["total_sessions"] == 1

    mock_service.get_summary.assert_called_once_with(user_id=1)
