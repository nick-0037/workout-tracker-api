import pytest
from fastapi.testclient import TestClient
from main import app
from api.models.user import UserResponse, Token
from api.services.auth_service import AuthService
from fastapi import HTTPException, status

client = TestClient(app)


def test_create_user_endpoint(monkeypatch):
    # Mock service
    async def fake_create_user(self, user_data):
        return UserResponse(
            id=1,
            username=user_data.username,
            email=user_data.email,
        )

    monkeypatch.setattr(AuthService, "create_user", fake_create_user)

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


def test_create_user_with_existing_email_returns_400(monkeypatch):
    # Mock service
    async def fake_create_user_fails(self, user_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    monkeypatch.setattr(AuthService, "create_user", fake_create_user_fails)

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


def test_login_user_endpoint(monkeypatch):
    # Mock service
    async def fake_login(self, credentials):
        return Token(access_token="fake-jwt-token", token_type="bearer")

    # Replace real method of service
    monkeypatch.setattr(AuthService, "login", fake_login)

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


def test_login_with_invalid_credentials_returns_401(monkeypatch):
    # Mock service
    async def fake_login_fails(self, credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    monkeypatch.setattr(AuthService, "login", fake_login_fails)

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
