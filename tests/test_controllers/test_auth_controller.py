import pytest
from fastapi.testclient import TestClient
from main import app
from api.models.user import UserResponse, Token
from api.services.auth_service import AuthService
from fastapi import HTTPException, status
from unittest.mock import AsyncMock
from api.controllers.auth_controller import get_service


@pytest.fixture
def mock_service():
    service = AsyncMock(spec=AuthService)
    return service


@pytest.fixture
def client(mock_service):
    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides.clear()

    app.dependency_overrides[get_service] = lambda: mock_service

    yield TestClient(app)

    app.dependency_overrides = original_overrides


def test_create_user(client, mock_service):
    # Arrange
    mock_service.create_user.return_value = UserResponse(
        id=1,
        username="testusername",
        email="test@example.com",
    )

    # Act
    response = client.post(
        "/auth/register",
        json={
            "username": "testusername",
            "email": "test@example.com",
            "password": "pass123",
        },
    )

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "testusername"
    assert data["email"] == "test@example.com"

    mock_service.create_user.assert_called_once()


def test_create_user_with_existing_email_returns_400(client, mock_service):
    # Arrange
    mock_service.create_user.side_effect = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
    )

    # Act
    response = client.post(
        "/auth/register",
        json={
            "username": "testusername",
            "email": "duplicate@example.com",
            "password": "pass123",
        },
    )

    # Assert
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

    mock_service.create_user.assert_called_once()


def test_login_user(client, mock_service):
    # Arrange
    mock_service.login.return_value = Token(
        access_token="fake-jwt-token", token_type="bearer"
    )

    # Act
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "correctpass",
        },
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "fake-jwt-token"
    assert data["token_type"] == "bearer"

    mock_service.login.assert_called_once()


def test_login_with_invalid_credentials_returns_401(client, mock_service):
    # Arrange
    mock_service.login.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )

    # Act
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "wrongpass",
        },
    )

    # Assert
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

    mock_service.login.assert_called_once()
